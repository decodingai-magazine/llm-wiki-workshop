# Explaining the Architecture

## The Core Concept: Brainstorming the Architecture

I’m still brainstorming the optimal way to build this second brain agent, so I want the post to be engaging. It should feel like: *"Hey, I’m building this, here are my thoughts so far—what do you think?"*

The foundation of this system is **GraphRAG**. Everything starts with a GraphRAG ingestion pipeline where we process all the documents from your second brain—whether they are written notes, videos, or other media.

### 1. The GraphRAG Ingestion Pipeline

The ingestion side is what populates our "memory." Here is the workflow:

- **Cleaning & Extraction:** We take the raw documents and use an open-source knowledge graph model to extract entities and relationships.
- **Embedding & Summarization:** We use an open-source embedding model to create a summary of the document. We embed that summary along with other metadata.
- **The Knowledge Graph Object:** This creates a structured object that allows for three types of retrieval: **semantic search** (via vectors), **text search** (via metadata), and **knowledge graph search** (via the structured relationships).

We use **Prefect** to orchestrate this entire pipeline. It handles scheduling, monitoring, and retries, making the process durable and production-ready. This can run on a schedule (e.g., every 24 hours) or on-demand whenever a new document is added.

---

## 2. The Agentic Retrieval Layer

Once the memory is populated, we have the agent itself. This agent uses the knowledge graph to interact with your second brain. My personal goal is to use this to generate articles and social media content.

The agent has access to several specialized tools:

- **Knowledge Graph Search:** To query the memory we built during ingestion.
- **Memory Management:** The agent can update its own memory relative to the user. This includes **episodic memory** (personal experiences anchored in time), **semantic memory** (user preferences and styles), and **procedural memory** (how the user specifically likes to structure a post).
- **External Tools:** Access to web search for real-time info and image generation (like Google’s Nano Banana) for post visuals.
- **The LLM Twin:** This is an open-source model fine-tuned to sound like my specific voice. Interestingly, smaller models often perform better at mimicking a specific writing style than larger reasoning models.

All of this orchestration—the complex back-and-forth between the agent and these tools during retrieval—is again handled by **Prefect**. It serves as the "durable workflow" engine that ensures the agentic process is robust.

---

## 3. Serving via FastMCP

The final piece of the puzzle is how we serve this agent. We are building this as an **MCP server** using the **FastMCP** framework by Prefect. It’s currently the most popular tool for building MCP servers, and for good reason—it’s excellent to work with.

This allows us to connect to **MCP clients** like **Claude** or **Cursor**. The user can interact with the agent conversationally. It’s not a rigid process where you just wait for an output; you can refine the ideas agentically until you're ready to hit "enter" and generate the final article.
