# Why MCP is Not Dead

**Big picture outline:**

Why “MCP is dead” is not true. Inspired from [this](https://www.linkedin.com/posts/prefect_mcp-is-dead-at-least-thats-what-the-internet-activity-7441955601313812481-514p?utm_source=share&utm_medium=member_desktop&rcm=ACoAACQFQWgBqowPZBqBQgSC3ATmuatVfZkf6fE) post. For example, why building a unified memory on top of your data served through MCP still makes A TON of sense. Easily hooked to:

- Your harness of choice: Claude Code, OpenCode, OpenClaw
- You have full control over your data. Your data still sits in your storage.
- You can easily distribute it to multiple clients at once
- CTA to this event talking about the same topic (same even as in the LinkedIn post above): [https://luma.com/htkxoidx](https://luma.com/htkxoidx) (on April 1 - free in-person event in NYC)
- Also tag Prefect’s CEO: [https://www.linkedin.com/in/jlowin/](https://www.linkedin.com/in/jlowin/)

**Hook:** “MCP is NOT dead.” You were just using it wrong.

---

**My notes from the video and experience:**

- ironically they are “throwing a funeral for the MCP” through the event from the CTA
- the MCP still has a glorious future
- people think “MCP is dead” because they are setting for their personal use cases:
    - CLI to access their database, orchestrator, cloud vectors instead of MCP servers
    - links to llms.txt sitemaps
    - skills to glue stuff together into procedures
- That’s great for personal setup, but when you go into the professional and business world where you have to deploy your business logic at scale to thousands or millions of customers and you tell them: “First thing we have to do is install this CLI on everyones machines then we have to setup a bunch of markdown files on all of these machines…” people will laugh at you
- In this use case, you cannot even talk about governence and security, all essential when doing AI for real at scale, for business use cases, either for internal tools or services, not just for your personal use cases
- We had CLIs for so long and we haven’t found a good way to govern them when distributing them to users
- You need a centralized way to distribute business logic… And we had for such a long time servers to do that exact thing, hence MCP servers will be here to stay when you have to:
    - You have full control over your data. Your data still sits in your storage. You just use MCP to distribute it to multiple users at once.
    - Distribute the data from your service to multiple agents with special consideration to security (e.g., Notion, Linear)
    - Carefully govern and monitor the business logic running on your server, rather than millions of users
    - Easily distribute and scale the business logic from one central place rather than millions of users. The MCP server can do that through skills and prompts (which are similar to skills in many ways)
- Then you can:
    - Choose your harness of choice: Claude Code, OpenCode, OpenClaw
    - Have full control over your data. Your data still sits in your storage.
    - Easily distribute it to multiple clients at once

**Examples from my own setups:**

- Personal Assistant: I am building a unified memory powered by GraphRAG that ingests all your personal data (notes, emails), plus general research (arxiv papers, youtube videos, articles). If loading all of this into simple files, working through SKILLS would have been enough, but as I have extremely specify business logic on how to write and search within my unified memory, plus having the database and infrastructure hosted on cloud, exposing this logic as MCP tools makes A LOT MORE SENSE. Doing this through a CLI would have been a nightmare. 
On the other way around, during development I do access MongoDB and Prefect through their CLI, as there is easier to let the agent have full accesss to everything.
- **My digital twin:** I have a lot of services plugged into my second brain, such as Notion (docs and databases for my business) and Readwise for research. As they are siloed services, the only way to access this information in a secure way is through their MCP servers. 
On the other way around, I use Obsidian to manage my local files, where I let Claude Code directly manage my files or use the new Obsidian CLI to do operations direclty on them.

**Conclusion:** 

“MCP is not dead” . You just need to use it when it makes SENSE, not for everything, along with Claude code skills and CLIs
