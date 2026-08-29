---
type: source
title: Prefect is the only orchestrator that survives agentic coding
description: Why an orchestrator's fitness for AI-assisted development is decided by one question — can the agent restart the execution environment in seconds after a code change?
origin: local
original_path: data_input_examples/notes/03-hard/How Smooth Is to Use Prefect for Agentic Coding.md
source_url: null
authors: []
published_date: null
raw_file: raw/how-smooth-is-to-use-prefect-for-agentic-coding.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities:
  - "[[wiki/entities/prefect]]"
  - "[[wiki/entities/claude-code]]"
concepts:
  - "[[wiki/concepts/agentic-coding-loop]]"
  - "[[wiki/concepts/durable-execution]]"
  - "[[wiki/concepts/infrastructure-over-frameworks]]"
  - "[[wiki/concepts/agent-skills]]"
---

# Prefect is the only orchestrator that survives agentic coding

> [[raw/how-smooth-is-to-use-prefect-for-agentic-coding|Raw]] · local

## Summary

A build report with a general lesson inside it. Four pipelines, Dockerized, with a
documented scaling path, built in roughly two hours of agentic coding with no
human intervention — and the surprise was not the speed but that "the agent never
got stuck on infrastructure."

The diagnosis: an AI coding agent works by looping edit → run → read → fix, and
most orchestrators insert a step the agent cannot perform. The note tables it —
Airflow needs a scheduler restart and DAG re-parse (30–60s, fragile), Dagster a
code-location reload (15–30s), Kubernetes a rebuild-and-push (2–5 min, "no"),
against Prefect's `serve()` where the worker *is* the Python process and
restarting means `kill %1 && make serve-workflows &` in about two seconds.

The architecture that makes this work is layered: pure Python business logic with
zero framework awareness; thin `@task`/`@flow` wrappers of 30–50 lines; a
19-line orchestrator that is one `serve()` call with four deployments; trigger
scripts that stream every Prefect log to stdout **and exit non-zero on failure**;
a Makefile so the agent need not remember deployment names; and a Docker Compose
that runs the identical command. Zero code changes between dev and production.

The second enabler deserves its own note: the trigger scripts exist so the agent
gets structured feedback in the same terminal — no UI, no log files. And the
runbook lives in `CLAUDE.md`, which is only writable because the loop is "kill a
process, start a process, run a make command, read the output."

## Key claims

- The agentic loop breaks wherever the agent cannot restart the execution environment itself. [[raw/how-smooth-is-to-use-prefect-for-agentic-coding#The core insight: why Prefect survives the agentic loop and other orchestrators don't|cite]]
- `serve()` puts no infrastructure between a code change and its execution — the worker is the Python process. [[raw/how-smooth-is-to-use-prefect-for-agentic-coding#The core insight: why Prefect survives the agentic loop and other orchestrators don't|cite]]
- Streaming logs to stdout and exiting non-zero is what gives the agent an unambiguous signal without a UI. [[raw/how-smooth-is-to-use-prefect-for-agentic-coding#The architecture Claude Code built|cite]]
- Business logic must stay framework-unaware so it can be tested and debugged outside the orchestrator. [[raw/how-smooth-is-to-use-prefect-for-agentic-coding#The architecture Claude Code built|cite]]
- The four questions to ask of any tool for AI-assisted development: can the agent restart it in seconds, does it surface errors in the agent's terminal, does it need external systems the agent cannot control, is it configured in the same language as the code. [[raw/how-smooth-is-to-use-prefect-for-agentic-coding#The broader lesson|cite]]
- "Works well with AI agents" was never a design goal — it falls out of code-first, infrastructure-last. [[raw/how-smooth-is-to-use-prefect-for-agentic-coding#The broader lesson|cite]]

## Connections

- **Entities**: [[wiki/entities/prefect]], [[wiki/entities/claude-code]]
- **Concepts**: [[wiki/concepts/agentic-coding-loop]], [[wiki/concepts/durable-execution]], [[wiki/concepts/infrastructure-over-frameworks]], [[wiki/concepts/agent-skills]]

> Synthesis: The four questions at the end generalize far past orchestrators — they are a usable test for whether *any* tool belongs in an agent-built system, and no other source in the wiki offers one.
