---
title: "From a Raw Shell to a Sandboxed Coding Agent"
subtitle: "The guide to isolating your harness and safely executing its commands, locally or remotely."
authors: ["Paul Iusztin"]
published_date: "2026-08-18T11:02:59+00:00"
source_url: https://www.decodingai.com/p/run-coding-agents-safely
origin: article
fetched: 2026-08-29T17:01:06Z
---

# From a Raw Shell to a Sandboxed Coding Agent

*The guide to isolating your harness and safely executing its commands, locally or remotely.*
# From a Raw Shell to a Sandboxed Coding Agent

### The guide to isolating your harness and safely executing its commands, locally or remotely.

[![Paul Iusztin's avatar](https://substackcdn.com/image/fetch/$s_!pQz0!,w_36,h_36,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0714d360-396c-4b41-a676-1b58dc1dc5f3_1470x1470.jpeg)](https://substack.com/@pauliusztin)

[Paul Iusztin](https://substack.com/@pauliusztin)

Aug 18, 2026

In LangChain’s Terminal-Bench experiment, changing only the harness (with the same model) moved a coding agent from ~30th place into the top 5: the harness, not the model, is what makes a coding agent good.

In the **open-source course** **[Building a Coding Agent From Scratch](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course)**, you’ll build that harness from scratch in Python: **Decode**, a complete coding agent that grows lesson by lesson from a bare agent loop into a swarm of remote agents running in parallel in the cloud.

**Why?** You’ll be able to engineer custom harnesses for your own AI products (the skill behind that leaderboard jump), and you’ll understand what Claude Code and Codex actually do under the hood, turning you into a power user.

[![](https://substackcdn.com/image/fetch/$s_!ge05!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F27ba7d81-6547-41ad-9370-e9df2dd960e1_1200x630.gif)](https://substackcdn.com/image/fetch/$s_!ge05!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F27ba7d81-6547-41ad-9370-e9df2dd960e1_1200x630.gif)

**Lessons:**

1. [Building a Coding Agent From Scratch](https://www.decodingai.com/p/building-a-coding-agent-from-scratch-system-design)
2. [The Bare-Bones Coding Agent Loop](https://www.decodingai.com/p/the-coding-agent-loop)
3. **From a Raw Shell to a Sandboxed Coding Agent** **←** ***you are here***
4. [Context Engineering for Coding Agents](https://www.decodingai.com/p/context-engineering-for-coding-agents)
5. [Subagents Are Context Engineering](https://www.decodingai.com/p/subagents-are-context-engineering)
6. Remote Headless Mode & Durability
7. AI Evals Foundations: Benchmarks, Regression and Online
8. AI Evals on Steroids via Replays

[Full open-source course](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course)

# Lesson 3: From Raw Shell to a Sandboxed Coding Agent*.*

[![The agent keeps all of its power. The room is what changes.](https://substackcdn.com/image/fetch/$s_!k1Xr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F97e3b938-fb2a-462c-923f-fbd591667a65_1376x768.png "The agent keeps all of its power. The room is what changes.")](https://substackcdn.com/image/fetch/$s_!k1Xr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F97e3b938-fb2a-462c-923f-fbd591667a65_1376x768.png)

Mid-session, Claude Code was running inside my Obsidian Second Brain when it fired off a cleanup command that deleted half my notes. If I hadn’t been backing them up with Obsidian Sync, two years of work would have been gone.

Even if you carefully isolate your agent, it can still reach the internet and go off the rails. In July 2026, [OpenAI’s agents](https://www.scientificamerican.com/article/openai-admits-its-agent-went-rogue-and-hacked-ai-startup-hugging-face/) hacked Hugging Face. A week later, Anthropic [disclosed](https://www.anthropic.com/news/investigating-incidents-cybersecurity-evals) that, after analyzing 141,006 eval runs from an isolated harness, their Claude models had gained unauthorized access to production infrastructure across 3 real organizations.

Still, for normal people who care about protecting their data, sandboxing is THE containment solution.

In Lesson 2, we saw how to implement an agent loop that controls your computer through 4 core tools: `read`, `write`, `edit`, and `bash`. In this article, we will learn how to isolate every computer-use tool from the rest of your system inside a **sandbox**.

We will hook it to two types of sandbox backends — local Docker and remote Modal — plus explore the other options and their trade-offs.

The cherry on top? GPU compute and scaling out of the box, plugged straight into your harness as a control center.

By the end, you will run:

```
SANDBOX_MODE=modal decode --repo https://github.com/<your-repo>.git "Swap from Gemini to Kimi K3."
```

Which will spin up a remote Modal sandbox hooked to Decode — the educational harness we are building throughout this course — set up the given repo, implement the requested feature, and end with a PR for review as the final artifact.

[Try it yourself](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course)

## The tools you love already use a sandbox

Locally, every `bash` command Claude Code or [Codex CLI](https://github.com/openai/codex) runs is wrapped in an OS-level jail — Seatbelt on macOS, bubblewrap on Linux (kernel features that block a process’s filesystem reach and syscalls).

In the cloud, Codex isolates [every task in its own environment (aka sandbox) preloaded with your repo](https://blog.bytebytego.com/p/how-openai-codex-works).

**In that case, what’s a sandbox?** It’s an execution boundary: the agent runs every tool that can alter the host inside a “jail”, so a wrong command runs inside a container, not your host.

Ok… That’s abstract. So how does a harness actually run its tools in this “jail”?

## How do sandboxes actually work?

In [Lesson 2](https://www.decodingai.com/p/the-coding-agent-loop), we learned that the core tools the agent uses to interact with your computer are `read`, `write`, `edit`, and `bash`. The rest (`web_fetch`, `todo_write`, `ask_user`, plan mode) never touch the filesystem — they are meta tools for fetching context and planning. That’s why, following Pi’s philosophy, they are optional.

Thus, our problem reduces to isolating the execution of the core tools from the rest of the harness. There are two main approaches.

In **option 1,** we run the whole harness in a Docker container or a remote Modal sandbox. It is straightforward and gives complete isolation, but it forces you to work in an environment different from your machine, with little flexibility to isolate specific tasks.

[![The one decision that defines the architecture — put the whole harness in the box, or keep it home and send only its tools across.](https://substackcdn.com/image/fetch/$s_!7A90!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0a626466-af9c-4245-a046-b7b1c11819cf_1200x498.png "The one decision that defines the architecture — put the whole harness in the box, or keep it home and send only its tools across.")](https://substackcdn.com/image/fetch/$s_!7A90!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0a626466-af9c-4245-a046-b7b1c11819cf_1200x498.png)

*The one decision that defines the architecture: Put the whole harness in the sandbox, or keep it local and only execute tools inside the sandbox.*

In **option 2**, we run the computer-use tools in a sandbox while the harness and the rest of the tools stay on the host. You keep your harness as your control center while executing tools inside the sandbox.

Option 1 is as simple as SSH-ing into a remote machine and running `claude`. Option 2 is where the real harness engineering happens.

The second dimension we have to think about is where the sandbox runs: locally in Docker or remotely on Modal.

[![Where a bash tool call actually runs — remote on Modal, locally in Docker, or raw on the host.](https://substackcdn.com/image/fetch/$s_!7aEX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde23dee8-a770-4dd1-9d50-4ea4dfb6a1e9_1200x484.png "Where a bash tool call actually runs — remote on Modal, locally in Docker, or raw on the host.")](https://substackcdn.com/image/fetch/$s_!7aEX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde23dee8-a770-4dd1-9d50-4ea4dfb6a1e9_1200x484.png)

*The core idea behind sandboxing computer-use tools such as bash.*

Regardless of where the sandbox runs, every computer-use tool call gets wrapped in an `inSandbox(command)` call. In our educational coding harness, Decode, we defined a `CommandExecutor` interface with 2 implementations (`LocalExecutor` for the host, `SandboxExecutor` for a backend), powered by 2 **sandbox backends**: `DockerBackend` or `ModalBackend`.

*From [src/decode/sandbox/\_\_init\_\_.py](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/main/src/decode/sandbox/__init__.py):*

```
def select_executor(mode: str) -> CommandExecutor:
    if mode == "docker":
        return SandboxExecutor(DockerBackend())
    if mode == "modal":
        return SandboxExecutor(ModalBackend())
    from decode.tools.exec import LocalExecutor

    return LocalExecutor()
```

The tool never knows where the command runs. The LLM emits the command, while the harness takes care of executing it in the selected environment. Once we build the right executor, we just call `executor.run(command)`, completely abstracted away from the sandbox — which means we can extend it with sandboxes beyond Docker or Modal.

*From [src/decode/tools/bash.py](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/main/src/decode/tools/bash.py):*

```
async def bash(
    ctx: RunContext[AgentDeps],
    command: str,
    timeout: float | None = None,
) -> str:
    if needs_approval(ctx):
        raise ApprovalRequired  # Permission gate — before anything runs

    if not command.strip():
        raise ModelRetry("command is empty; provide a shell command to run.")
    timeout_s = _resolve_timeout(timeout)

    executor = await _get_executor() # sandbox (powered by Docker or Modal) or local
    result = await executor.run(command, cwd=ctx.deps.cwd, timeout_s=timeout_s)

    return _render(result, timeout_s=timeout_s)
```

We adopt a similar strategy for the `read`, `write`, and `edit` tools, plus optional ones such as `glob` and `ls`. That way the agent sees a single filesystem: when `write` creates a file, `bash` sees it immediately.

[![The executor seam in motion — the agent loop keeps emitting bash calls on your machine, and each one runs as a command inside the sandbox.](https://substackcdn.com/image/fetch/$s_!uAaO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1215db45-22b7-45ea-a80d-ce91ae11cda2_1200x592.png "The executor seam in motion — the agent loop keeps emitting bash calls on your machine, and each one runs as a command inside the sandbox.")](https://substackcdn.com/image/fetch/$s_!uAaO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1215db45-22b7-45ea-a80d-ce91ae11cda2_1200x592.png)

*The executor logic: The agent loop keeps emitting bash calls on your machine, and each one runs as a command inside the sandbox.*

Now, let’s zoom in on how local sandboxes work via Docker.

## Local sandboxes via Docker

Run “`SANDBOX_MODE=docker decode --repo git@github.com:you/project.git"` to start a new Decode session inside a Docker sandbox, which contains 5 main steps:

1. `DockerBackend` launches one long-lived **keeper container** running `sleep infinity`.
2. Injects all the environment variables from `.env` into the container.
3. Attaches a local volume at `.decode/sandbox`.
4. Prepares **the Workspace** by cloning `--repo` into `.decode/sandbox` at HEAD.
5. Installs the dependencies by running `uv sync` on the given `--repo`.

[![Session start in Docker mode is a straight line — create the container, inject the env vars, bind the Workspace volume, download the repo, install dependencies.](https://substackcdn.com/image/fetch/$s_!gae9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbd37a1cb-ef55-4cf9-b5e4-8d823e392358_1200x309.png "Session start in Docker mode is a straight line — create the container, inject the env vars, bind the Workspace volume, download the repo, install dependencies.")](https://substackcdn.com/image/fetch/$s_!gae9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbd37a1cb-ef55-4cf9-b5e4-8d823e392358_1200x309.png)

*Docker sandbox lifecycle: Create the container, inject the env vars, bind the Workspace volume, download the repo, install dependencies.*

Within the `DockerBackend` class, plugged into `SandboxExecutor`, we have 2 functions to implement: `create` and `exec`. `create` mostly goes through the 5 steps outlined above. In `exec`, each `bash` call translates to a `docker exec <command>` against its associated container.

*From [src/decode/sandbox/docker\_backend.py](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/main/src/decode/sandbox/docker_backend.py):*

```
_WORKSPACE = "/workspace"  # container-side path of the Workspace

class DockerBackend:
    async def create(self, workspace: Path) -> None:
        # once, at session start
        # `workspace` is the host-side clone of your
        # --repo at .decode/sandbox

        args = ["run", "-d", "--rm", "-v", f"{workspace}:{_WORKSPACE}", "-w", _WORKSPACE]
        if sandbox_git_token():
            args += ["-e", GIT_TOKEN_ENV]
        args += ["ghcr.io/astral-sh/uv:python3.12-bookworm-slim", "sleep", "infinity"]
        proc = await asyncio.create_subprocess_exec(
            "docker", *args,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
            env=_run_env(), 
        )
        stdout, _ = await proc.communicate()
        container_id = stdout.decode().strip()  # `docker run -d` prints the container id

    async def exec(self, *args: str, timeout_s: float) -> ExecResult:
        # for every bash tool call — a fresh exec
        proc = await asyncio.create_subprocess_exec(
            "docker", "exec", "-w", _WORKSPACE, container_id, *args,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
            start_new_session=True,  # own process group → kill as a unit on timeout
        )
        ...  # gather stdout/stderr → ExecResult
```

Docker is easy to set up, works out of the box with container tooling, and the same containers can later be hosted remotely via Kubernetes or other orchestrators. As good as that sounds, it isn’t truly secure. Container processes are [native processes on your kernel](https://www.youtube.com/watch?v=wsFd22SL1s8). As Abhishek Bhardwaj, on OpenAI’s RL and agent-infrastructure team, puts it, a container process can exploit that boundary and take the host — a kernel exploit is [“a New York Times article waiting to happen”](https://www.youtube.com/watch?v=OqM67QG_Ikk).

Docker sits on a spectrum:

1. **fork/exec** — straightforward to implement, no boundary. The command talks straight to your kernel.
2. **Containers** ← **we are here.** A namespace-and-cgroup boundary. Shared kernel. Another option is Podman, which doesn’t use a daemon, saving latency.
3. **gVisor** — a user-space “sentry” kernel answers the syscalls, turning a direct kernel exploit into a two-hop chain (sentry → host kernel). Costs little: near-container performance. It’s what [Modal runs underneath its sandboxes](https://modal.com/docs/guide/security?source=decodingai&campaign=harnesseng). Not perfect. If the agent gets past the sentry, you’re back on the shared kernel.
4. **microVMs** — [Firecracker](https://github.com/firecracker-microvm/firecracker) or [Cloud Hypervisor](https://www.cloudhypervisor.org/) on KVM, the Linux kernel’s own hypervisor (Linux hosts only). The guest kernel runs in a separate CPU execution context from the host, so even if the agent fully compromises it, it can’t reach yours. Cheaper than it sounds: [Arrakis](https://github.com/abshkbh/arrakis) boots one in under 7s, against ~40s for a traditional VM.

**Seatbelt and bubblewrap sit on the same layer as containers.** They are OS jails. They wrap one command instead of the whole machine, deriving the filesystem profile from the permission rules the agent already uses. No image, no daemon. Still sharing your host’s kernel. That’s what Claude Code and Codex CLI run locally. Cheaper than Docker, not stronger.

So which one? If you trust the code and just want your own files safe, go with **containers** (as we did in Decode). Otherwise, for full isolation, go with **microVMs**. Bhardwaj’s verdict, after building OpenAI’s sandbox cloud: [“in the end, everyone always wants a VM… let me save you the story and two years of grief, just please use microVMs from the start”](https://www.youtube.com/watch?v=OqM67QG_Ikk).

To run it on your own machine, follow the [“Running the Code” setup steps](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course#-running-the-code) in the course repo, then launch:

```
SANDBOX_MODE=docker decode --repo https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course.git
```

This clones the repo into the isolated Workspace (`/workspace` ≡ host `.decode/sandbox`) and opens a new TUI session wired to the Docker container. To test it out, pick any feature, plan it, ask for a PR, and let Decode do the rest.

For a quick test, we prepared a demo wrapped as the `/demo-5-sandbox-feature-pr` skill. It uses Decode to spin up a new sandboxed Decode session and instructs it to implement a small feature from a pool of available ones (e.g. a `decode --version` CLI command), then open a PR with it. Creating feature PRs is essential when working in sandboxes, as you have no direct access to where the code actually runs.

The real win, though, is when the box isn’t on your machine at all.

## Remote sandboxes via Modal

[Modal](https://modal.com/?source=decodingai&campaign=harnesseng)‘s core primitive is [the sandbox](https://modal.com/docs/guide/sandboxes?source=decodingai&campaign=harnesseng) — an isolated, serverless runtime that starts in under half a second.

Run “`SANDBOX_MODE=modal decode --repo git@github.com:you/project.git"` and here is what happens through Modal’s 5-event lifecycle:

1. **Created**: `ModalBackend` requests a sandbox under `decode-sandbox-<env>`.
2. **Scheduled**: Modal finds capacity on its infra.
3. **Started**: the container is live and can execute commands (but the app is not ready yet).
4. **Ready**: the tar containing the app files is uploaded into `/workspace` (making the app env ready).
5. **In use**: `bash` and the other computer-use tools exec successfully against the remote.

Modal’s sandbox infra boots fast. Preparing the app dependencies is what takes a while.

That’s why, as you can see in the image below, we mount a volume that already contains the app dependencies, so they are ready when the container starts. On top of that, to avoid the cold start problem — you want the sandbox ready as soon as the harness starts — we prepare a sandbox pool modeled as a queue. We populate it with application-agnostic sandboxes and turn them into application-specific ones by attaching a volume. This combination of sandbox pool plus volume mounting gives us application-ready sandboxes on demand. More on this [here](https://modal.com/blog/unpacking-sandbox-startup-latency?source=decodingai&campaign=harnesseng).

> Check [this blog post](https://modal.com/blog/scaling-to-1-million-concurrent-sandboxes-in-seconds?source=decodingai&campaign=harnesseng) if you want to learn more about how Modal dropped Kubernetes and built its sandbox architecture from scratch to start 1 million concurrent sandboxes in under a minute.

[![The Modal backend — the harness stays local, every tool call crosses into a remote sandbox that mounts its repository volume, and sandboxes come pre-provisioned from a pool.](https://substackcdn.com/image/fetch/$s_!Uvba!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6fbbf5d8-c0e6-45ff-95c3-5c9555da65a2_1200x618.png "The Modal backend — the harness stays local, every tool call crosses into a remote sandbox that mounts its repository volume, and sandboxes come pre-provisioned from a pool.")](https://substackcdn.com/image/fetch/$s_!Uvba!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6fbbf5d8-c0e6-45ff-95c3-5c9555da65a2_1200x618.png)

*The Modal backend: The harness stays local, every tool call crosses into a remote sandbox that mounts its repository volume, and sandboxes come pre-provisioned from a pool.*

The `ModalBackend` class looks similar to the `DockerBackend` one. Inside `create`, we create the sandbox from a pre-built `uv` Docker image. We inject a git token to get access to our private repositories. Finally, we launch it with the `sleep infinity` command to keep it running — now on Modal’s infrastructure, which takes care of our security concerns.

**Modal puts zero risk on your host.** It’s remote, and it runs gVisor to intercept syscalls before they reach the kernel. Even when OpenAI’s agents hacked Hugging Face, as reported [here](https://www.aljazeera.com/news/2026/7/29/openais-rogue-agent-hacked-an-account-at-a-second-technology-firm-report), their code was running on one of Modal’s sandboxes — the agent exploited Hugging Face’s code running there, not the Modal infrastructure itself.

Within the `exec` method, we execute the command that comes from the LLM and return the output and exit code.

*From [src/decode/sandbox/modal\_backend.py](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/main/src/decode/sandbox/modal_backend.py):*

```
class ModalBackend:
    async def create(self, workspace: Path) -> None:
        app = await modal.App.lookup.aio(_app_name(), create_if_missing=True)
        image = modal.Image.from_registry(
            "ghcr.io/astral-sh/uv:python3.12-bookworm-slim"
        ).apt_install("git", "curl", "ca-certificates")
        secrets = []
        if token := sandbox_git_token():
            image = image.run_commands(GIT_CREDENTIAL_HELPER)
            secrets = [modal.Secret.from_dict({GIT_TOKEN_ENV: token})]
        sandbox = await modal.Sandbox.create.aio(
            "sleep", "infinity", app=app, image=image,

        ...  # tar-upload the Workspace into /workspace — the "Ready" step

    async def exec(self, *args: str, timeout_s: float) -> ExecResult:
        proc = await sandbox.exec.aio(*args, workdir=workdir, timeout=timeout, text=False)
        stdout, stderr = await asyncio.gather(proc.stdout.read.aio(), proc.stderr.read.aio())
        exit_code = await proc.wait.aio()

        ...  # → ExecResult
```

From [Modal’s pricing page](https://modal.com/pricing?source=decodingai&campaign=harnesseng) at the time of writing: a CPU sandbox at 2 cores + 4 GiB runs ≈ 0.38/*hr*, *a* *B*200 *GPU* *bills* ≈6.25/hr, and an H200 ≈ $4.54/hr. For pure agentic work, the CPU sandbox gets the job done, while the GPU ones let you run inference or fine-tuning jobs directly from your harness.

The default is using the CPU sandbox. To configure it with x4 H200 we would do:

```
sandbox = await modal.Sandbox.create.aio(
    ...,              # Same parameters as the CPU sandbox
    gpu="H200:4",     # 4× H200 attached to this sandbox
)
```

As discussed in [Lesson 2](https://www.decodingai.com/i/208432780/the-llm-providers) on pay-per-token vs. serverless, for ad-hoc data processing serverless can come out ~80-90% cheaper.

The trade-offs of a remote sandbox over a local one: network latency, sandbox management, and extra costs.

You can run the same test as for the Docker sandbox by following the [“Running the Code” Modal extra setup steps](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course#-running-the-code) and swapping `SANDBOX_MODE=docker` for `modal`:

```
SANDBOX_MODE=modal decode --repo https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course.git
```

After running it, Modal’s dashboard shows how many sandboxes are live (5 in our case):

[![Number of running sandboxes in Modal](https://substackcdn.com/image/fetch/$s_!5yvV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdb61bc42-9973-4655-8108-40308b5a9a8c_3288x978.png "Number of running sandboxes in Modal")](https://substackcdn.com/image/fetch/$s_!5yvV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdb61bc42-9973-4655-8108-40308b5a9a8c_3288x978.png)

And if you open the sandbox app and click “Sandboxes”, you get the full list:

[![The list of running sandboxes inside the Modal sandbox app](https://substackcdn.com/image/fetch/$s_!0AC-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fccdaad8d-8c2a-4918-9513-5cd9abb6c812_3088x1086.png "The list of running sandboxes inside the Modal sandbox app")](https://substackcdn.com/image/fetch/$s_!0AC-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fccdaad8d-8c2a-4918-9513-5cd9abb6c812_3088x1086.png)

These sandboxes are created when you enter a new Decode session and automatically cleaned up when you exit via the `/quit` command.

## The wanted side effects of remote sandboxes

Remote sandboxes give you 2 powerful side effects beyond safety.

**The first is compute.** Modal sandboxes accept a [GPU spec like](https://modal.com/blog/how-to-price-serverless?source=decodingai&campaign=harnesseng) `gpu="B200:8"` [at creation](https://modal.com/blog/how-to-price-serverless?source=decodingai&campaign=harnesseng), letting you agentically fine-tune models or process large datasets (eg extracting knowledge graphs from 1000+ documents) with open-weight LLMs such as Qwen3.6, Gemma 4, K3, or GLM5.2.

**The second is scale.** An orchestrator agent running directly on the host (no sandbox) can hand work to background agents running on Modal remote sandboxes. Put them on a CPU if you just need a bunch of parallel agents hitting an LLM API to pull tickets from your Linear backlog, or on a GPU if you need to squeeze out more juice.

In [this case study](https://modal.com/blog/how-ramp-built-a-full-context-background-coding-agent-on-modal?source=decodingai&campaign=harnesseng), Ramp, a fintech company, runs every agent session in its own Modal sandbox with a full dev environment inside. Modal’s own conclusion from the case study is that with cheap isolation, the bottleneck shifts from “can the agent write correct code” to “how many agents can you run in parallel”.

[![The scaling shape the seam makes possible — an unsandboxed orchestrator on your machine fans work out to N background agents, each contained in its own sandbox.](https://substackcdn.com/image/fetch/$s_!Vi-q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4e446570-e1bb-4559-a85a-e95d6bcb4795_1200x551.png "The scaling shape the seam makes possible — an unsandboxed orchestrator on your machine fans work out to N background agents, each contained in its own sandbox.")](https://substackcdn.com/image/fetch/$s_!Vi-q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4e446570-e1bb-4559-a85a-e95d6bcb4795_1200x551.png)

*Scaling: An unsandboxed orchestrator on your machine fans work out to N background agents, each contained in its own sandbox.*

## Next steps

Should you sandbox all the time? No. As a Claude Code power user, to keep it simple, I still run directly on my machine in folders versioned by git or Obsidian Sync.

Sandboxes are non-negotiable for:

* 24/7 personal assistants that control your whole computer like [OpenClaw](https://openclaw.ai/) or Hermes;
* non-engineers using tools like [Claude Cowork](https://www.anthropic.com/product/claude-cowork);
* unmonitored remote jobs like [Codex](https://openai.com/research/codex);
* or when chasing GPUs and parallel scale.

Is this the only way to add sandboxes to your harness? As we are just getting started, surely not. For another perspective, [here is Abhishek Bhardwaj’s talk](https://www.youtube.com/watch?v=OqM67QG_Ikk), explaining how OpenAI runs agent workloads in a cloud of microVM sandboxes instead of containers.

🧑‍💻 We encourage you to **clone our [course repo](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course)**, open your terminal, type **”decode”**,and test out the coding agent.

In the next lesson, we will explore the key context-engineering techniques that coding harnesses use: memory, compaction, skills, and LSP servers.

Here is the **course roadmap,** lesson by lesson *([see all in GitHub](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course#-course-outline)*):

1. [Building a Coding Agent From Scratch](https://www.decodingai.com/p/building-a-coding-agent-from-scratch-system-design)
2. [The Bare-Bones Coding Agent Loop](https://www.decodingai.com/p/the-coding-agent-loop)
3. **From a Raw Shell to a Sandboxed Coding Agent** **←** ***you are here***
4. [Context Engineering for Coding Agents](https://www.decodingai.com/p/context-engineering-for-coding-agents)
5. [Subagents Are Context Engineering](https://www.decodingai.com/p/subagents-are-context-engineering)
6. Remote Headless Mode & Durability
7. AI Evals Foundations: Benchmarks, Regression and Online
8. AI Evals on Steroids via Replays

*But here is what I’m wondering:*

> ***Do you run your coding agent raw on your machine, or sandboxed?***

*Click the button below and tell me. I read every response.*

[Leave a comment](https://www.decodingai.com/p/run-coding-agents-safely/comments)

---

*Enjoyed the article? The most sincere compliment is to restack this for your readers.*

[Share](https://www.decodingai.com/p/run-coding-agents-safely?utm_source=substack&utm_medium=email&utm_content=share&action=share)

---

*Special thanks to **[Modal](https://modal.com?source=decodingai&campaign=harnesseng)**, **[Opik (by Comet)](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul&utm_content=coding_agent_course)**, and **[Kitaru (by ZenML)](https://www.zenml.io/product/kitaru?utm_source=decodingai&utm_medium=referral&utm_campaign=coding-agent-course&utm_content=brand)** for sponsoring this open-source course and keeping it free!*

[![](https://substackcdn.com/image/fetch/$s_!Uq-1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F98999460-8389-40b0-9dda-73f934bbf55a_1200x400.png)](https://substackcdn.com/image/fetch/$s_!Uq-1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F98999460-8389-40b0-9dda-73f934bbf55a_1200x400.png)

---

#### Whenever you’re ready, here is how I can help you

*Go from agent user to agent builder.* Master the foundations of AI agents and turn fragile demo code into reliable, production-ready systems with my course, **[Agent Engineering: Building Multi-Agent Systems](https://academy.towardsai.net/courses/agent-engineering?ref=b3ab31&utm_source=decodingai&utm_medium=partner&utm_campaign=agent_engineering)** (made with Towards AI).

35 lessons. Pure foundations from scratch. 4 mini-projects. 2 production systems. A certificate and direct access to me & industry experts in our Discord.

Built for software and data professionals transitioning into AI engineering. *Rated 5/5 with 300+ students. The first 7 lessons are free:*

[Start here](https://academy.towardsai.net/courses/agent-engineering?ref=b3ab31&utm_source=decodingai&utm_medium=partner&utm_campaign=agent_engineering)

*Not ready to commit?* Start with our **[free Agent AI Engineering Guide](https://email-course.towardsai.net/?ref=b3ab31&utm_source=decodingai&utm_medium=partner&utm_campaign=agent_engineering)**, a 6-day email course on the mistakes that silently break AI agents in production.

---

## Images & videos

If not otherwise stated, all images are created by the author.
