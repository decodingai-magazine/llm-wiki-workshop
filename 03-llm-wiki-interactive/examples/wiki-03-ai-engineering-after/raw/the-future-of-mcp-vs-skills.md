# The Future of MCP vs. Skills

# **MCP**

Fri, 10 Apr 26

### **MCP Ecosystem Growth & Milestones**

- 110M monthly downloads milestone achieved in just 18 months
    - Comparison to React’s adoption trajectory: “React. One of the most successful open source projects over the last decade took roughly double the amount of time for which the download will be”
    - Downloads represent broad ecosystem adoption across major AI infrastructure:
        - OpenAI agents SDK integration
        - Google ADK implementation
        - LangChain framework adoption
        - “Thousands of frameworks and tools that you might have never heard of it, putting it as a dependency”
    - Creates interoperability: “Which means there’s one common standard that all of us have at our disposal to speak to each other”
- Evolution from minimal viable protocol to comprehensive ecosystem
    - Original state 18 months ago: “There was just a little spec document, a few SDKs, mostly written by Claude, local only with little more than just tools”
    - Community development: “you guys have been absolutely crazy building stuff, building servers, building and crazy ecosystem around this”
    - Anthropic’s parallel development added remote capabilities, centralized authorization, elicitation tasks, and experimental MCP applications
- Server development spans experimentation to enterprise production
    - Experimental projects: “little toy projects of WhatsApp servers and Blender servers”
    - Production SaaS integrations: “building SaaS integrations like linear Slack and Notion that are really powering what everyone does every day when they use mcp”
    - Enterprise adoption: “But most importantly, the vast majority of MCP server most of all of us have built are behind closed doors connecting companies systems to agents in AI applications”

### **Opening Demo Context: MCP Applications Revolutionary Concept**

- Revolutionary interface serving capability: “This is an entity application that’s an agent shipping its own interface. Not like a plugin, not an SDK, not rendered on the fly by the model, by the client side, or hard coded to the product. That is something that’s served over an NCP server”
- Deployment flexibility: “And you can take the server, put it into cloud, you can put it into ChatGPT, you can put it into VS code cursor, just function”
- Protocol requirements for bidirectional understanding: “You need semantics. You need to have both sides, the client and the server, to understand what each side is talking, to understand how you render this, understand the UI coming. And for that you need a protocol”
- Dual interaction capability: “And the best part about this, an MTP server doesn’t just ship an app or can ship an app, it can also ship tools with it. And so you can interact with it, with the application as a human and you can have the model interact with it through tools”

### **2026 Agent Development Paradigm Shift**

- Historical progression through distinct phases
    - 2024: “we just built a bunch of demos and showed cool stuff to people and there was a little bit of a buzz there”
    - 2025: “was really all about coding agents”
    - Coding agents as optimal initial use case: “But coding agents, if you really think about it, are the most ideal scenario for an agent. It’s local, it’s verifiable, you can call a compiler like you have a developer who can fix shit if it goes wrong in front of the computer and it can display a two year interface and the user’s quite happy”
- 2026 transition to general knowledge work
    - “But I think now with the capabilities of the model increasing, we are going into a new era which I think this year we will see the start where we’re not just doing coding agents, we’re going to have general agents that will do real knowledge worker stuff, like things a financial analysis analysts want to do, a marketing person want to do”
    - Critical infrastructure requirement: “And they need one thing in particular, they don’t need a local agent that calls a compiler. What they need is something that can connect to like five SaaS applications and a shared drive. Because the most important part for them for an agent is connectivity”
- Connectivity complexity requires nuanced approach
    - Warning against oversimplification: “And in my mind connectivity is not one. If one if someone tells you there’s one solution for all your connectivity problems, be it computing, dsc, Life, plmtp, they are probably pretty rough because the right thing of course is that it always means it depends and there is a really a big connectivity stack and there’s the right tool for the right job”
    - Three-layer connectivity architecture: skills, CLI, and MCP with distinct use cases

### **Skills Layer**

- Core function: “main knowledge” that “capture specific capabilities put into a very simple file”
- Reusability characteristics: “And it’s mostly reusable. There’s some minor differences between the different files, of course”

### **CLI Layer**

- Popularity in coding contexts: “CLI is very popular with local coding agents”
- Accessibility advantage: “It’s an amazing tool to get simply started to have something that you can compose in a bash that you get automatically discovered when the model can automatically discover what the CLI is capable of”
- Training data leverage: “And most importantly, if you have things that are like CLIs, like GitHub, Git and other things that are in free training, CLI is an amazing solution for your productivity part”
- Optimal environment requirements: “And they’re particularly good when you have a local agent where you can assume a sandbox where you can assume a good execution environment”

### **MCP Layer**

- Rich semantics requirement: “But if you don’t have this, if you need rich semantics and you need a UI that can display long running time, when you need things like resources”
- Platform independence: “when you need to build something that is fully decoupled and needs platform independence, or you don’t have a sandbox”
- Enterprise requirements: “when you need things like authorization, governance policies, or short to say boring end up boring but important enterprise stuff”
- Experimental capabilities: “or if you want to have experiments like MCP applications or what consume skills or brands are key”
- Positioning: “that then I think MCP is this like additional connective tissue that is just yet another tool in the toolbox for you to build an amazing agent”
- Unified multi-tool approach as 2026 prediction
    - “And so this is all to say that I think in 2026 we’re going to start building agents that use all of them. They don’t use one thing, they use all of it. And they use it quite seamlessly together”
    - Current limitations: “And I don’t think we’re quite there just yet because we need to build a lot of stuff. Firstly because our agents kind of still suck and partially because I think we just haven’t talked enough about some of the techniques you can do to really put this connective tissue together”

### **Technical Implementation Improvements**

- Progressive discovery as fundamental paradigm shift
    - Current problematic pattern: “And what everybody so far has done, because we’re in this very early experimentation phase is to simply put all the tools into the context window and then be quite surprised that maybe the context window gets large”
    - Better approach: “But what you can do instead, and what you should do instead, you should start using this progressive discovery pattern, which is to say do something like tool search to defer the loading of the tools and start loading the tools when the model needs it”
    - Implementation options: “And we have this in the anthropic product. The API people can use this type on competitors APIs as well. But also you can just build this in yourself where you just don’t load the tool directly. And the moment you get the model, a tool loading tool basically”
    - Real-world impact: demonstrated massive reduction in Claude Code before/after comparison
- Programmatic tool calling (code mode) addresses orchestration inefficiencies
    - Problem with sequential pattern: “This is the idea that one thing that you really want to do is you want to compose things together. You don’t want the model to go, call a tool, take the result and go and talk, call another tool, take the result, call another. Because what you’re effectively doing is you’re letting the model orchestrate things together. And in that orchestration you will use a inference. You will, it’s latency sensitive and all of its stuff could be done way more effective if you would instead write a script”
    - Implementation approach: “So what you want, instead of having one tool at another, you want to give the model a repo provide like execution environment like a V8 isolate or a Monty or something like that, or LUA interpreter and just have the model write the code for you and the model just executes that code and then composes them together”
    - MCP advantage through structured output: “And there’s a neat daily feature in MCP called structured output that tells you what the return value of the output will be. And the model can use this information to figure out type information which then mean it can really nicely compose these things together”
    - Fallback for non-structured output: “Of course, if you don’t have a structured output, you can always just ask the model to get you structured output by just extracting it and saying, hey, call us cheap model and say I want this expected type, give it back to me and bam, you have a type”

### **Server Design Philosophy Revolution**

- Strong criticism of naive REST API conversion approaches
    - “And that means we all need to stop taking rest APIs and put them one to one into an MTP server. Every time I see someone building another rest apart MTP server conversion tool, it’s a bit cringe because I think it just results in horrible things”
- Agent-first design methodology: “And what you should do instead is to design for an agent. Basically you can start designing for you as a human how you would want to interact with this because that’s actually a very, very good start for an agent”
- Server-side programmatic orchestration: “If you want to orchestrate things together, you should reach, of course, for programmatic tool calling, you can do this on the client side, as I said before, but you can also do this on the server side. The cloudflare, MCP server and others like that are great examples how you can have, instead of providing tools, provide an execution environment through the model and then just have them orchestrate things together, which again have some token usage as cuts on latency and is way more powerful in its composition”
- Rich semantics utilization as MCP differentiator: “And then last but not least, you should have started, or we should start as server authors to use this rich semantics that MCP offers over alternatives. This means shipping MCP applications. It means shipping skills over mcp. It means using things like tasks and other aspects that the protocol offers that we’re currently slightly under. Things like elicitations, things that only MCP can do for you”

### **Technical Roadmap & Core Infrastructure Improvements**

- Stateless transport protocol addressing enterprise scalability
    - Current limitation: “There’s a few things that as we have developed the protocol over the last year that are just not in good shape. Number one is that the current stream relation to key is very hard to scale if you’re a large paper scale”
    - Solution: “And so we have a proposal from our friends at Google who are working with something called a stateless transport protocol which make it significantly easier to just trade MCP servers like you know, another stateless REST server or something like that. We used to know how to deploy to cloud runs or kubernetes and so on”
    - Timeline: “So that’s coming down in June and hopefully lining the SDKs very soon”
- Agent-to-agent communication enhancement: “In addition, we need to improve our HP asynchronous task primitive which basically is a very fancy way to say we just want to have agent to agent communication. We have a very experimental version of the protocol that very few clients support. So we’re going to start building more clients out like that”
- SDK modernization: “And most importantly we are improving some of the semantics that we need to. We’re going to ship a TypeScript version SDK version 2 and Python SDK version 2 based on a lot of the lessons learned over the last year. There’s a SDK called FastMCP who’s using FastMCP. It’s just way probably better than Python distribution, right? And that’s on me because I wrote the Python SDK and so I have a bunch of people way better Python developers than me help me out write it better”

### **Enterprise Integration & Advanced Features**

- Cross-app access solving enterprise authentication friction: “The second part is we need to start integrating. Everywhere we’re going to ship for particular enterprise is something called cross app Access. It’s a new thing that we’re working closely together with identity providers which just allows you. It’s a very fancy way to say once you log in once with your local company identity provider via Google, via Google be able to just use FTP servers without having to re log in. So it’s a bit more smoothness”
- Server discovery mechanism: “In addition, we’re going to add something called a server discovery like specifying how you can discover servers on well known URLs automatically. So crawlers, browsers, agents and just go to a website and say oh and instead of just parsing the website, is there also entities that I can use? And we’ll be able to automatically discover this. This is a really cool thing that will come down also in June when we launch the next specification, it will be supported there”
- Extension mechanisms and platform-specific adaptations: “And then last but not least, we are starting to use our extension mechanisms in which means that some clients like for example MCP applications will only be supported by web based interfaces. Because if you’re a cli, you just have a hard time Rendering hdr. Right. I’m going to do more of these extensions”
- Skills over MCP as major capability extension: “One of the most exciting extensions that I think is cool. You’re just going to shift skills over mcp because it’s very obvious that if you have a large MCP server with tons and tons of tools, you just want to ship the main knowledge with and say, oh, this is how you’re supposed to use this. This is how you’re supposed to do this. And it allows you as a server author to continuously ship updated skills without having to rely on plugin mechanism to register as a person”

### **Vision & Community Direction**

- 2026 connectivity prediction: “Okay, that’s for me, along winded way. I think to say that I think MCP is actually in a really good shape and I think in this year we’re going to push agents to full connectivity. MTP will continue to play a major, major, major role”
- Community values and feedback mechanisms: “We want of course to feel that we are a very open community. We just have created a foundation where most programming as an open source community, as a discord with issues just come to us and tell us where the fuck are we wrong, what are we getting right so that we can improve this on a continuous basis”
- Multi-tool agent architecture as ultimate vision: “So 2026, I think it’s all about connectivity and the best agents use every available network. They will use computer use, they will use clis, they will use mcps, we’ll use scripts because they want to have a wide variety of things they can do”

---
