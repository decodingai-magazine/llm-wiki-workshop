# The Right Way of Building Agents With MCP Servers

Hello Curtis. In this video, I would like to focus on one thing to talk about, which I want to frame as a question because I'm still thinking about the right way to

implement it. I think it will be interesting to talk about the right way of building agents with MCP servers. We can walk people through how we think about this problem,
and there are multiple options on how we could solve it. We can walk people through these options and also let them engage by asking: what options do you prefer, or do
you suggest other options? Is this the right way or not? I think it's a fun way to make this more engaging, and I'm also curious about what they think so I can properly
integrate it in the book.

Before getting into the right way of building agents with MCP servers, I think it will be a lot easier for you to understand a cleaner infrastructure, which is very

related to what we had before. So I would just quickly walk you through what I think is the go-to method, what I chose as the go-to method, and this is the frame around
this question: the right way of building agents with MCP servers. I also have this reflected in a diagram. Let's kick into what I think is the right version. This is

more linear, while the other one has more branches, and that's why I want to start with this.

Basically we have a data pipeline. Step one is to ingest either a full dataset or a URI—for example, an article, a video from YouTube, an image, and so on. We normalize
everything to a document in step two, then save it in a data warehouse as documents. In the memory pipeline, we load everything as documents, transform them into

knowledge graph objects using a knowledge graph extractor, which basically extracts entities and relationships. We have an embedding model which computes the vectors

based on the summary of the document. Then we have other metadata such as the source of the document, author, dates, and whatever other metadata makes sense for the

document. Then we save this into the memory.

We expose interaction with the memory through knowledge graph search and knowledge graph write tools. These are some of the core tools that will be available to the MCP
server—basically ways to search in this memory or to write into the memory. For example, someone chats with this agent and tells particular preferences, such as "I like
more straight-to-the-point articles," "I like more educational posts," "I like to write giveaway posts in this particular way," or "I went in December 2025 to celebrate
New Year's Eve in the mountains." Things like preferences and episodic memories from the user can be automatically detected and written inside the memory. This will be

important to give the special kick when you want to write specific articles or posts.

So basically we have these tools in an MCP server, and we also have prompts, which are predefined procedures. These are specialized prompts that tell the agent how to

use the tools in different combinations. For example, the "update episodic memory" prompt tells the orchestrator how to detect what it needs to update in the episodic

memory and what tools and how to use them. For example, it will use the knowledge graph write to detect when and how to write particular memories to the memory. Episodic
memories are related to what the specific user did at a particular moment—for example, that they celebrated New Year's Eve in the mountains. Semantic memory is similar
but related to preferences, like writing preferences, style preferences, and things like this. The "write technical article" and "write social media post" prompts will

be procedures on how to write these pieces of text—for example, how to use the web search, generate image, and how to combine all of these tools to search the memory.

On the architectural side, we have the MCP server which has these tools and prompts. For this example, let's say it has just these two tools. We expose this as our MCP

server, and then we compose it with other MCP servers—for example, MCP servers that have web search, generate images, and things like these, which are usually prebuilt.
Out there on the internet, there are many MCP servers with default functionality that just work for us. Maybe we could also add things like Google Drive search and

things like this. Basically, when we want to integrate with any other functionality that we don't necessarily want to implement, we can compose with other MCP servers

and expose this set of composed tools and composed prompts.

Now we expose just these composed tools and composed prompts, and then we can hook an MCP client to these composed tools and prompts. Here are two options: you either

build your custom orchestrator using the Fast MCP framework to connect to these tools and prompts exposed by a collection of MCP servers, or you just use a pre-built

orchestrator such as Claude Code where you use all the tools you need but basically leverage all the orchestration logic from Claude Code. The interaction from the user
is pretty much the same because both are MCP clients.

On the tooling side, the data pipeline is orchestrated by Prefect, the memory pipeline is orchestrated again by Prefect, and the retrieval tools will again be

orchestrated by Prefect but on the retrieval side, as these others are more on the ingestion side. The MCP server is implemented with Fast MCP. The custom orchestrator

will also be implemented using Fast MCP, but only their client utility to connect to the server.

So this is the overall logic. Now my question is the following. As you can see, up to here everything is the same. This diagram is pretty similar with the following

particularity: you have two options on how to actually build this MCP server to expose your functionality.

Option one would be to build your tools and prompts and keep them inside the server, not expose them, and actually just expose your custom orchestrator as a tool. This

way, you can then plug in your pre-built MCP servers to your MCP server that has only this custom orchestrator as a tool. Then you can plug in a pre-built orchestrator

such as Claude Code to access your custom orchestrator.

Option two is basically the one I explained before, where you expose all the tools and prompts and you don't care about building an orchestrator at all. But in case you
need planning, you will need to build a custom orchestrator on the client side, on the MCP client side.

The real question here is: where should we put this custom orchestrator? Should we put it on the MCP server side, or should we put it on the client side? If you're in a
scenario where you're fine with the pre-built logic from the Claude Code orchestrator, you don't really care that much about this question. But in many custom

applications, you actually want to build your custom orchestrator—you don't want to use Claude Code. You want to build your own orchestrator with your own planning

logic, your own execution logic, and basically own the solution end to end.

So in that use case, where should you put your orchestrator? On the MCP server side, exposing your whole packaged solution as a tool that can be used by whoever—either

by your own app or by a pre-built orchestrator? Or should you just expose these tools and prompts and build your custom orchestrator on the MCP client side?

Programmatically, both work—I implemented both. But from the architectural system design point of view, which solution is better? I cannot really choose, and I think

it's a very important architectural decision that propagates through the entire application. Because, for example, if the MCP client is not Claude Code, you can build

another Python application that hosts this MCP client and then serves it as a FastAPI server plus some CRUD logic around users, or it can be directly on the frontend,

implemented in TypeScript with React and running on the frontend.

There are multiple options which I think are very interesting to explore with my audience. As before, on the tooling side: data pipeline with Prefect, memory pipeline

with Prefect, retrieval tooling with Prefect, server with Fast MCP. Both servers will be implemented with Fast MCP, and the Claude Code pre-built one is Claude Code,

while the custom orchestrator will be connected to the Fast MCP server through Fast MCP. F stands for Fast MCP, and P stands for Prefect.
