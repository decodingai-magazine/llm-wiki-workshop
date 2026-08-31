---
type: repo_note
title: How a subagent is spawned and what the parent gets back
description: Traces the agent -> _spawn_child -> _run_attempt call chain to show exactly how a child's deps are narrowed, how its report becomes a truncated section, and how a raise or a bad report is handled.
original_path: github://decodingai-magazine/building-a-coding-agent-from-scratch-course#how-a-subagent-is-spawned-and-what-the-parent-gets-back
repo: "[[wiki/repos/github-decodingai-magazine-building-a-coding-agent-from-scratch-course/ARCHITECTURE]]"
commit_sha: 6ee643fbfeb10d3f9b463bf2a6cdfb64671b8aea
question: in the coding agent repo, how does the agent spawn a subagent, and what does the parent actually get back when it finishes?
spawned_by_question: "[[wiki/questions/2026-08-31-how-a-subagent-is-spawned-and-what-the-parent-gets-back]]"
created: 2026-08-31T14:45:35Z
timestamp: 2026-08-31T14:45:35Z
entities:
  - "[[wiki/entities/pydantic-ai]]"
concepts:
  - "[[wiki/concepts/subagents]]"
  - "[[wiki/concepts/permission-gate]]"
  - "[[wiki/concepts/agent-loop]]"
---

# How a subagent is spawned and what the parent gets back

> Answers [[wiki/questions/2026-08-31-how-a-subagent-is-spawned-and-what-the-parent-gets-back]] against `building-a-coding-agent-from-scratch-course` @ `6ee643f`

`ARCHITECTURE.md`'s "Subagent fan-out" section already covers the shape (width cap, semaphore,
substance guard, byte-budgeted concatenation, no synthesis call). This note answers what it left
at summary level: the mechanics inside `_spawn_child`/`_run_attempt` — how `deps` is narrowed, what
"bypass" and "deny resolvers" concretely are, the truncation boundary, and exception vs. bad-report
handling.

## Answer

`agent()` (the tool the parent model calls) does **not** talk to children directly — it only
validates and fans out. After the empty/width-cap/substance checks it computes a shared byte budget
and hands each prompt to `_spawn_child` under `asyncio.gather`:

```
child_max_bytes = settings.subagent_result_max_bytes // len(prompts)
sections = await asyncio.gather(*(_spawn_child(ctx, prompt, index=i, max_bytes=child_max_bytes) ...))
```
(`src/decode/tools/agent.py:371-378`)

**Spawn is a direct nested `Agent.run()` call**, not a separate entry point. `_run_attempt`
(`agent.py:452-501`) loads the `explore` persona, builds a fresh `AgentDeps`, and re-enters the
*same installed Agent instance* (`_require_main_agent()`, set once by `set_main_agent()` at
`build_agent()` time — so the child shares the parent's model + HTTP client, never a new one):

```python
explore = load_agent(_SUBAGENT_PERSONA)                 # agent.py:469
child_deps = AgentDeps(
    cwd=ctx.deps.cwd, harness_home=ctx.deps.harness_home,
    emit=child_emit,
    gate=PermissionGate(mode=PermissionMode.BYPASS),      # fresh instance, not the parent's gate
    resolve_permission=_deny_permission_resolver,
    resolve_user_question=deny_user_question_resolver,
    active_agent=explore,
    context_window_tokens=ctx.deps.context_window_tokens,
)                                                          # agent.py:474-489
async with _semaphore():
    result = await _require_main_agent().run(
        prompt, deps=child_deps,
        usage_limits=UsageLimits(request_limit=settings.subagent_max_requests),
        event_stream_handler=_make_child_stream_handler(child_emit),
    )                                                      # agent.py:491-499
```

What each narrowing concretely is:
- **Gate bypass** is not a flag on the parent's gate — it's a *brand-new* `PermissionGate(mode=PermissionMode.BYPASS)` object per child (`agent.py:479`). In bypass mode every tool call resolves inline, so a child's `read/glob/grep/lsp` calls never raise `ApprovalRequired` and there is no deferred-approval loop for anyone to answer.
- **"Silent event sink"** is `_make_child_emit(ctx.deps, index)` (`agent.py:278-296`), a closure that checks `parent.verbose.enabled` **at emit time** (not when the child was spawned, so toggling Ctrl+O mid-fan-out takes effect on the very next event). Off → `_silent_emit` just does `logger.debug(...)` (`agent.py:273-275`), nothing reaches the TUI. On → the event is tagged with the child's 1-based `index` and forwarded to the parent's own `emit`. The child's tool-call stream only exists because `event_stream_handler=_make_child_stream_handler(child_emit)` (`agent.py:298-322`) is attached to the nested `run()` on every call — a nested `agent.run()` bypasses decode's own loop, so without this hook a child's tool calls would be invisible even in verbose mode.
- **"Deny resolvers"** are two plain async callables placed on `AgentDeps`: `_deny_permission_resolver` (`agent.py:326-330`) unconditionally returns `PermissionDecision.deny(...)`, and `deny_user_question_resolver` (imported from `decode.tools.askuser`) does the same for `ask_user`. Both are safety nets — bypass mode means neither is normally reached — for an unattended child that has no human to answer an approval or a question.
- `task_store` is *omitted* from `child_deps`; its `default_factory` on `AgentDeps` gives every child a fresh empty list, so nothing a child does touches the parent's task list.

**Bad-report retry.** `_spawn_child` (`agent.py:410-449`) calls `_run_attempt` once; `_usable_report()`
(`agent.py:167-176`) treats a result as BAD if the output is a `DeferredToolRequests`, if the text is
empty/whitespace, or — via `_read_any_code` (`agent.py:153-165`, scanning `result.all_messages()` for
any `ToolCallPart`) — if the child made zero tool calls (answered from memory). A `None` triggers
**exactly one** re-spawn with `prompt + _RETRY_NUDGE` appended (`agent.py:433-438`); if that's *also*
bad, `_spawn_child` gives up and returns `_NO_USABLE_REPORT_NOTE` (`agent.py:444-447`) — never a third
attempt. The nudge is harness text, so it does **not** re-enter `_check_substance` (that word-floor
check runs once, in `agent()`, on the model's *original* prompts before any child spawns —
`agent.py:367`).

**Exceptions do not propagate.** Both attempts live inside one `try/except Exception` in
`_spawn_child` (`agent.py:431-442`) — so if the *first* attempt raises, the retry still runs (the
`except` wraps the whole two-attempt sequence via the `if report is None:` branch being inside the
`try`); if the retry attempt itself raises, that's caught by the same `except` and the child's
section becomes `_CHILD_FAILED_NOTE` ("This subagent failed before producing a report."), never
`_NO_USABLE_REPORT_NOTE` — the two notes are for different failure modes (raised vs. twice-bad).
Because the exception is swallowed inside `_spawn_child`'s own coroutine, `asyncio.gather` in
`agent()` never sees it (no `return_exceptions=True` needed) — one broken child cannot abort its
siblings or the whole `gather`.

**What the parent gets back.** Whichever report wins (fresh or retried) is truncated —
`truncate(report, max_lines=settings.max_output_lines, max_bytes=max_bytes).text` (`agent.py:449`,
`max_bytes` = the per-child share computed once in `agent()`). `truncate()` (`truncate.py:52-63`) caps
at **max_lines OR max_bytes, whichever is hit first, always snapping the cut to a line boundary**
(even the first line is kept whole if it alone exceeds the byte cap); on overflow the full text spills
to a temp file, but `_spawn_child` only takes `.text` — the spill path is dropped at this seam, not
surfaced to the parent model. `agent()` then joins the N section strings into `## Subagent i — "label"`
blocks in prompt order (`agent.py:373-378,386-389`) and returns `fold + SYNTHESIS_FOOTER` as the tool
result string, verbatim — pydantic-ai delivers that string back to the parent model as the `agent` tool
call's result. There is no separate synthesis LLM call inside decode; the "synthesis" the parent
produces next turn is the parent model reading `SYNTHESIS_FOOTER`'s instruction and writing prose
+ a diagram from the raw sections it was just handed.

```
agent(prompts)                              _spawn_child(i)                 _run_attempt(i)
  guards, _check_substance  ───────────►
  child_max_bytes = budget/N
  asyncio.gather ─────────────────────────►  try:
                                                report = _run_attempt() ───►  fresh AgentDeps
                                                if bad: retry +nudge          (gate=BYPASS, silent
                                                except Exception:              emit, deny resolvers)
                                                  -> _CHILD_FAILED_NOTE       under _semaphore():
                                              return truncate(report,          _MAIN_AGENT.run(prompt)
                                                max_bytes).text          ◄──  _usable_report(result)
  fold = "## Subagent i" + section  ◄──────
  return fold + SYNTHESIS_FOOTER  (no synthesis LLM call — this string IS the tool result)
```

## Evidence

- `src/decode/tools/agent.py:371-378` — `agent()`: shared byte budget + `asyncio.gather` fan-out over `_spawn_child` ([permalink](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/6ee643fbfeb10d3f9b463bf2a6cdfb64671b8aea/src/decode/tools/agent.py#L371-L378))
- `src/decode/tools/agent.py:373-389` — labelled fold (`## Subagent i`) built and returned with `SYNTHESIS_FOOTER`, no separate synthesis call ([permalink](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/6ee643fbfeb10d3f9b463bf2a6cdfb64671b8aea/src/decode/tools/agent.py#L373-L389))
- `src/decode/tools/agent.py:410-449` — `_spawn_child`: try/except wraps both attempts, `_CHILD_FAILED_NOTE` on raise, `_NO_USABLE_REPORT_NOTE` on twice-bad, `truncate(...).text` on success ([permalink](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/6ee643fbfeb10d3f9b463bf2a6cdfb64671b8aea/src/decode/tools/agent.py#L410-L449))
- `src/decode/tools/agent.py:452-501` — `_run_attempt`: builds narrowed `AgentDeps` (fresh `PermissionGate(BYPASS)`, deny resolvers, `active_agent=explore`) and calls `_require_main_agent().run(...)` under `_semaphore()` ([permalink](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/6ee643fbfeb10d3f9b463bf2a6cdfb64671b8aea/src/decode/tools/agent.py#L452-L501))
- `src/decode/tools/agent.py:153-176` — `_read_any_code` / `_usable_report`: the BAD-report predicate (deferred output, empty text, or zero `ToolCallPart` in the transcript) ([permalink](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/6ee643fbfeb10d3f9b463bf2a6cdfb64671b8aea/src/decode/tools/agent.py#L153-L176))
- `src/decode/tools/agent.py:278-296` — `_make_child_emit`: verbose-mode check happens at emit time, not spawn time ([permalink](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/6ee643fbfeb10d3f9b463bf2a6cdfb64671b8aea/src/decode/tools/agent.py#L278-L296))
- `src/decode/tools/agent.py:298-322` — `_make_child_stream_handler`: turns the nested run's `FunctionToolCallEvent`s into decode `ToolCallStarted` events ([permalink](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/6ee643fbfeb10d3f9b463bf2a6cdfb64671b8aea/src/decode/tools/agent.py#L298-L322))
- `src/decode/tools/agent.py:326-330` — `_deny_permission_resolver`: unconditional deny, the safety net behind bypass mode ([permalink](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/6ee643fbfeb10d3f9b463bf2a6cdfb64671b8aea/src/decode/tools/agent.py#L326-L330))
- `src/decode/tools/truncate.py:52-63` — `truncate()`: line-OR-byte cap, always snapped to a line boundary, full content spilled to a temp file on overflow ([permalink](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/6ee643fbfeb10d3f9b463bf2a6cdfb64671b8aea/src/decode/tools/truncate.py#L52-L63))

Not read: `decode.agents.loader.load_agent`, the `explore` persona file itself, `AgentDeps`'s full
field list, and `decode.permissions.gate.PermissionGate`'s bypass-mode implementation — this note
only traces the call chain in `tools/agent.py` (+ `truncate.py`) that the question asked about.

## Connections

- **Entities**: [[wiki/entities/pydantic-ai]] — `Agent.run()`, `RunContext`, `ModelRetry`, `DeferredToolRequests`, `UsageLimits`, and the `event_stream_handler`/`FunctionToolCallEvent` seam are all pydantic-ai primitives the spawn mechanism is built directly on top of.
- **Concepts**: [[wiki/concepts/subagents]] — this note is the mechanical detail behind the fan-out pattern the ARCHITECTURE page names. [[wiki/concepts/permission-gate]] — the child's bypass gate is a fresh, separately-scoped instance, not a mode flip on the parent's gate. [[wiki/concepts/agent-loop]] — the child is not a second loop; it's the same installed `Agent` re-entered via a nested `run()`, sharing the parent's model and HTTP client.

> Synthesis: spawning is a direct nested `Agent.run()` on the one installed Agent with narrowed, single-use `AgentDeps`; the parent gets back one harness-built string — N budget-truncated, line-boundary-snapped sections concatenated under `## Subagent i` headings plus a fixed footer — with zero synthesis LLM call and zero exception ever crossing the `_spawn_child` boundary.
