# Owning Your Context Layer

### Summary

**Post 17:** Owning the context layer. True freedom. Harnesses are commoditized. The true business value is in the system around it: memory, MCP servers, skills, etc. Using “free” hardware, you are not really free, as what you want to own is the memory. Keeping your memory detached from a harness is true independence. You can do that through MCP servers (e.g., the setup from the book). Like this, you can switch harness, models, etc., and they will instantly remember who you are, your context, and what you have to do.

### Post

[https://www.linkedin.com/posts/pauliusztin_models-are-becoming-commoditized-harnesses-share-7472592740183318528-qNoM/?utm_source=share&utm_medium=member_desktop&rcm=ACoAACQFQWgBqowPZBqBQgSC3ATmuatVfZkf6fE](https://www.linkedin.com/posts/pauliusztin_models-are-becoming-commoditized-harnesses-share-7472592740183318528-qNoM/?utm_source=share&utm_medium=member_desktop&rcm=ACoAACQFQWgBqowPZBqBQgSC3ATmuatVfZkf6fE)

[https://x.com/pauliusztin_/status/2066860844420653299](https://x.com/pauliusztin_/status/2066860844420653299)

---

Models are becoming commoditized.

Harnesses are becoming commoditized.

The only moat that remains is your context layer.

Freedom does NOT come from using open-source models or harnesses.

Because neither the model nor the harness is the thing you care about.

They're just tools.

What you care about is:

- Your research
- Your notes
- Your conversations
- Your tasks
- Your preferences
- Your domain knowledge

Or in short...

- Your data.
- Your memory.
- What the LLM should know about you and your work to get s*** done.

This is why I've become increasingly interested in owning the context layer.

Let's say you switch from:

- Claude Code
- Codex
- Gemini CLI
- Pi
- Hermes

Ideally, nothing should change.

Within 5 minutes, the new system should instantly understand:

- Who you are
- What you're working on
- What you've learned
- What matters to you

Because your memory moved with you.

This is what true independence looks like.

Hence, it's the architecture

[**Maxime Labonne**](https://www.linkedin.com/in/maxime-labonne/)

and I have been converging toward while working on our upcoming book:

𝟭/ 𝗨𝗻𝗶𝗳𝗶𝗲𝗱 𝗺𝗲𝗺𝗼𝗿𝘆

Built using the simplest tool that gets the job done.

For example:

- Filesystems
- BM25
- Semantic Search
- Knowledge Graphs

The goal is to build a memory layer that belongs to you.

So we start simple and add complexity only when your use case demands it

𝟮/ 𝗠𝗖𝗣 𝗦𝗲𝗿𝘃𝗲𝗿

The MCP server becomes the interface to that memory.

It exposes:

- Tools
- Resources
- Prompts
- Skills
- MCP Apps

And wraps all the business logic around how that memory is queried and updated.

The result is a portable context layer that can plug into any harness.

One thing that surprised me while building this was how easy MCP deployment has become...

I recently deployed our memory MCP server using

[**FastMCP**](https://www.linkedin.com/company/fastmcp/)

and

[**Prefect**](https://www.linkedin.com/company/prefect/)

Horizon Cloud.

The workflow was basically:

- Connect GitHub
- Specify the MCP entry point
- Specify the UV environment

And a few minutes later I had:

- Automatic deployments
- Authentication
- Continuous updates on every push
- Serverless infrastructure

[**FastMCP**](https://www.linkedin.com/company/fastmcp/)

has become my default framework for MCP servers, and

[**Prefect**](https://www.linkedin.com/company/prefect/)

Horizon Cloud made deploying them dramatically simpler than I expected.

My biggest takeaway from the last few months:

Your context layer should stay with you because that's where your digital identity lives.

P.S. How much of your knowledge is portable today?

### Sponsor Notes

Prefect FastMCP as THE framework to implement MCP servers

Prefect Horizon Cloud as the easiest way to deploy MCP servers.

For example, I recently deployed my MCP server for the book to Prefect Horizon Cloud, and it was extremely simple. I just hooked my GitHub to Prefect Horizon and connected that GitHub to a new deployment.

I only needed to specify a few things:

1. The entry point to the MCP server
2. The entry point to the UV virtual environment

From there, I got a serverless deployment out of the box. It automatically detects when I push new commits to GitHub and updates with the latest state.

Basically, in five minutes, you get:

1. Scalable deployments
2. A continuous deployment pipeline
3. An automatic authentication layer on top through the browser

It is essentially everything you need. In five minutes, you are good to go to deploy your MCP server to users.

It also provides a generous freemium plan. Where I add all of the above just with the freemium plan.

(more here on [Prefect Horizon](https://gofastmcp.com/deployment/prefect-horizon))

### Media

![[03-llm-wiki-interactive/examples/wiki-ai-engineering/raw/assets/the-context-layer.png]]

---

### Full notes

I want to have a conversation on owning your context layer. I see a lot of discussion regarding closed-source models (such as Claude, Gemini, and OpenAI) versus open-source models (usually Chinese models like Qwen, Minimax, or Kimi). This is the first layer where people think they have true freedom.

The second layer involves being locked into a specific harness. For example, there is the family of harnesses coming from Anthropic (Claude, Claude Code) or OpenAI (Codex). Many people believe they have freedom if they use an open-source harness that allows access to any model, such as Pear or Hermes. They aren't locked into a single subscription or model, but can work with anything.

Many think that using an open-source harness (like Pear) with an open-source model (like Kimi, Qwen, or Gemma) is the path to true freedom. While that is true to some extent, the reality is that these are only means to an end. They are just tools. You are mostly discussing infrastructure here, rather than referring to your own knowledge, context, conversations, and notes.

You aren't referring to what you actually care about: the memory, or the context layer. Owning that layer is the true freedom. You shouldn't just try to hack your way around different tools. For instance, if you own the context layer and use it with Claude Code, you can easily switch the second you find that it doesn't do what it should. Conversely, if your whole ecosystem is built around a specific open-source harness and you stop liking it, the effort to move is much higher.

It is the same with LLMs. If they are open-source, you can run a version on your local machine, but how far can that get you? At some point, you will need the latest versions that keep up with the world.

The context layer, however, is attached to you and your business case. Ultimately, it is your data:

1. Past conversations
2. Notes and research
3. Tasks
4. People you know

This is what makes a system "you" or your business; it is what makes the system actually usable. That is where true independence lies. If you own the context layer and design it properly, you can switch from Claude Code to Codex to Pear to Gemini CLI without issue. The moment you bring your memory with you, these tools will automatically understand who you are and pick up on your whole context. That is the true way to avoid ecosystem lock-in.

There are multiple ways of implementing this, but a popular method is to serve your context layer through an MCP server. This server contains all the business logic around your context layer, which is connected to a unified memory. This memory can be based on:
(a) Knowledge graphs
(b) File systems
(c) Standard hybrid indexes (Semantics + BM25)

The idea is that the context layer is customized to your preferences. What matters is that the unified memory is yours, and you bring it with you whenever you switch harnesses or LLMs.

For example, in the upcoming book I am writing with Maxim, my approach involves:

1. An MCP server that exposes tools to write to and query this memory.
2. An MCP app to visualize, filter, and sort the unified memory so we can understand what is in there visually.

We use an implementation of Knowledge Graph + Semantic Search + BM25. We have a generic ontology that allows you to extract high-signal information from all your data while keeping track of all documents and chunks. It is a more complex solution, but you can also choose to just use Semantic Search + BM25 if you don't want the knowledge graph, or layer the knowledge graph on top for a higher-signal solution.

The idea here isn't that you should just go with a Knowledge Graph, a file system, semantic search, or BM25. The real idea is that you should pick the right tool and the right algorithm for the job.

The most important part is that you need to glue all of this together into a unified memory. This memory is exposed to an MCP server, which is pluggable into any type of harness. That is ultimately the beauty of MCP servers. You should use them because you can write business logic and connect the server to your database, your file system, or private data that is behind an authentication wall. It is secure and portable; it lives in the cloud and essentially has all the properties of a web server.

When it comes to memory, you shouldn't just think about skills or CLIs. While they are useful, their scope is not to build a context layer. An MCP server sits on top of tools and brings with it resources, prompts, and skills that bundle together that server's domain knowledge. For example, it gives context to the harness on how to read and write, what the memory is capable of, and how to interact with that specific server.

To conclude, the context layer is this bundle where MCP servers and unified memory come together. They are highly pluggable, meaning you can own it, move around with it, and easily switch to any other harness or LLM.

This approach offers two major advantages:

1. Ownership and Portability: You are never locked in. Whenever you switch platforms, you bring all your context with you.
2. Data Privacy: You own the data. It doesn't sit on OpenAI, Anthropic, or Google servers.

With the rise of AI, this is becoming increasingly important. As we start using these harnesses, our entire interaction with the computer begins to revolve around them. Essentially, whoever owns this context layer owns your digital identity. This is why it is super important to own your context layer (it represents true freedom).
