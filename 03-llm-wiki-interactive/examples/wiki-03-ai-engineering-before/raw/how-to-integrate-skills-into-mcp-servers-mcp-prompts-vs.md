# How to integrate Skills into MCP servers: MCP Prompts vs. Skills

# Resources

https://github.com/jlowin/fastmcp/blob/main/examples/skills/server.py

https://gofastmcp.com/python-sdk/fastmcp-server-providers-skills-__init__

# **Agentic Calling in Claude Code**

## **MCP Primitives vs Claude Code Native Skills**

Claude Code treats different MCP primitives differently when it comes to automatic, agentic invocation.

### **MCP Tools**

- **Auto-detected:** Yes
- **Used agentically:** Yes
- Tools registered via `@mcp.tool` are fully agentic — Claude Code will call them autonomously when it determines they are relevant to the task.

### **MCP Resources**

- **Auto-detected:** Yes (listable via `ListMcpResourcesTool`)
- **Used agentically:** No
- Resources (including skills registered via `SkillsDirectoryProvider`) must be explicitly referenced by the user (e.g., `@server:skill://name/SKILL.md`) or read programmatically via `ReadMcpResourceTool`.
- They are passive — available on request, but not part of the agentic loop.

### **MCP Prompts**

- **Auto-detected:** Yes (listable)
- **Used agentically:** No
- Prompts are discoverable by MCP clients, but Claude Code does not automatically invoke them. They must be explicitly triggered by the user.

### **`.claude/skills/` (Claude Code Native Skills)**

- **Auto-detected:** Yes
- **Used agentically:** Yes
- Skills placed in the `.claude/skills/` directory are automatically detected and can be invoked via the `Skill` tool when Claude Code determines they are relevant.

## **Summary Table**

| MCP Primitive | Auto-detected? | Used agentically? |
| --- | --- | --- |
| Tools | Yes | Yes |
| Resources | Yes (listable) | No |
| Prompts | Yes (listable) | No |
| `.claude/skills/` | Yes | Yes |

## **Skills Are NOT Part of the MCP Protocol**

"Skills" do not exist anywhere in the raw MCP specification (revision 2025-11-25). The word doesn't appear in any protocol message, schema type, capability declaration, or method definition.

### **Core MCP Protocol Primitives**

The protocol defines these primitives:

| Primitive | Owner | Description |
| --- | --- | --- |
| **Tools** | Server | Executable functions for AI to invoke |
| **Resources** | Server | Data sources providing context |
| **Prompts** | Server | Reusable message templates |
| **Sampling** | Client | Server-initiated LLM completions |
| **Elicitation** | Client | Server-initiated user input requests |
| **Tasks** | Server | Durable execution wrappers (experimental) |

### **FastMCP's Skill Abstraction**

FastMCP packages skills as MCP **resources** — it's a higher-level packaging convention on top of the protocol. From FastMCP's own docs:

> *"A skill is not a separate concept. It's a prompt, a resource, or a bundle of both. Calling them 'skills' is a packaging decision, not an architectural one."*
> 

Each skill directory is exposed as:

- `skill://name/SKILL.md` — the core instruction content
- `skill://name/_manifest` — a synthetic JSON resource listing all files
- `skill://name/path/to/file` — any supporting files

### **Skills as a Cross-Agent Ecosystem Convention**

Multiple AI coding agents have independently adopted the same convention (a folder with a `SKILL.md` file), but each handles them natively — not through MCP:

| Agent | Skills Directory |
| --- | --- |
| Claude Code | `~/.claude/skills/` |
| GitHub Copilot | `~/.copilot/skills/` |
| Gemini CLI | `~/.gemini/skills/` |
| Cline | `~/.cline/skills/` |
| Codex | `~/.codex/skills/` |

Since skills aren't an MCP primitive, exposing them as MCP resources (via `SkillsDirectoryProvider`) makes them **discoverable** by any MCP client, but **not agentically callable**. Each client decides how to handle resources.

## **Skill Ownership: Developer vs User**

| Who owns it | Mechanism | Example |
| --- | --- | --- |
| **Developer** | MCP tool descriptions, MCP prompts | "This tool expects ISO dates", "Call X before Y" |
| **User** | `.claude/skills/` (or equivalent) | "When recalling memories, always render to markdown" |

**Developer-owned instructions** should ship with the MCP server:

- How to correctly use a specific tool or API
- Recommended workflows for the server's capabilities
- Best expressed as MCP **prompts** or **tool descriptions**

**User-owned skills** live in the user's environment:

- Personal workflows and preferences
- Project-specific conventions
- Portable across projects and tools

FastMCP's `SkillsDirectoryProvider` blurs this line by letting developers package user-level instructions inside the server. But since MCP resources aren't agentically consumed by Claude Code, they end up in a dead zone — not quite developer instructions (which should be prompts or tool descriptions), and not quite user skills (which should be in `.claude/skills/`).

## **Recommendations**

- **For user defined agentic workflows in Claude Code:** Use MCP tools or `.claude/skills/`.
- **For developer-owned multi-step workflows:** Express them as MCP **tools** (server-side execution) or MCP **prompts** (client-side templates).
- **For user-owned workflows:** Place them in `.claude/skills/` so Claude Code can invoke them automatically.
- **For cross-client compatibility:** Use `SkillsDirectoryProvider` to expose skills as MCP resources for any MCP client, and optionally duplicate them in `.claude/skills/` for Claude Code's native skill system.

# **An In-Depth Guide on the MCP Protocol vs Claude’s Skills**

## Table of Contents

1. [MCP Protocol Fundamentals](https://www.notion.so/MCP-Architecture-Skills-Implementation-Guide-2fd449159be280058f55c79ed144fafe#mcp-protocol-fundamentals)
2. [Prompts vs. Skills: The Critical Distinction](https://www.notion.so/MCP-Architecture-Skills-Implementation-Guide-2fd449159be280058f55c79ed144fafe#prompts-vs-skills)
3. [Tool Execution Architecture](https://www.notion.so/MCP-Architecture-Skills-Implementation-Guide-2fd449159be280058f55c79ed144fafe#tool-execution-architecture)
4. [Implementing Skills in FastMCP](https://www.notion.so/MCP-Architecture-Skills-Implementation-Guide-2fd449159be280058f55c79ed144fafe#implementing-skills-in-fastmcp)
5. [Recommended Architecture for AI Twin](https://www.notion.so/MCP-Architecture-Skills-Implementation-Guide-2fd449159be280058f55c79ed144fafe#recommended-architecture)
6. [Code Examples](https://www.notion.so/MCP-Architecture-Skills-Implementation-Guide-2fd449159be280058f55c79ed144fafe#code-examples)

---

## MCP Protocol Fundamentals

### Core Primitives

MCP defines **three core primitives** that servers expose:

| Primitive | Purpose | Control Model | When to Use |
| --- | --- | --- | --- |
| **Tools** | Executable functions the AI can invoke | AI-controlled (the model decides when to call them) | Actions, operations, API calls, database queries |
| **Resources** | Passive data sources for context | Application-controlled (client reads them) | File contents, configs, documentation, schemas |
| **Prompts** | Reusable message templates | User-controlled (explicitly invoked by user) | Workflow templates, structured interactions |

### Key Concepts

**Client-Server Architecture:**

`┌─────────────────────────────────────┐
│   MCP Host (AI Application)        │
│   - Claude Desktop, VS Code, etc.  │
│                                     │
│   ┌───────────┐  ┌───────────┐    │
│   │MCP Client1│  │MCP Client2│    │
│   └─────┬─────┘  └─────┬─────┘    │
└─────────┼──────────────┼───────────┘
          │              │
          ▼              ▼
    ┌─────────┐    ┌─────────┐
    │ Server1 │    │ Server2 │
    │ (Local) │    │(Remote) │
    └─────────┘    └─────────┘`

**Execution Flow:**

1. Client sends JSON-RPC request: `tools/call`
2. **Server executes the tool code** (on the server)
3. Server returns result to client
4. AI uses result in conversation

---

## Prompts vs. Skills: The Critical Distinction

### The Confusion

Your original design had:

- **Prompts** = Predefined procedures
- **Skills** = User-defined procedures

### The Reality

**MCP has NO native "Skills" primitive.** Here's what actually exists:

| MCP Primitive | Actual Behavior | Control |
| --- | --- | --- |
| **Prompts** | User-controlled templates that must be explicitly invoked (like slash commands) | User decides when to run them |
| **Tools** | AI-controlled functions that the model autonomously decides to call | AI decides when to run them |
| **Resources** | Passive data that clients read for context | Application reads them |

### Skills Don't Exist in MCP

**There is no `/skills/list` or `/skills/execute` in the MCP protocol.**

To implement "skills," you must use one of the existing primitives:

- **Option A:** Skills as Prompts (user-invoked workflow templates)
- **Option B:** Skills as composite Tools (server-side orchestration)
- **Option C:** Skills as Resources (FastMCP 3.0 Skills Provider)

---

## Tool Execution Architecture

### Where Code Runs

**Critical Point:** Tool code ALWAYS executes on the MCP server.

python

`# This code is in your MCP server
@mcp.tool
def echo(message: str) -> str:
    # ⚠️ THIS FUNCTION RUNS ON YOUR SERVER
    # NOT on the client (Claude Desktop/VS Code)
    return f"Echo: {message}"`

### Client-Side vs. Server-Side Orchestration

### Server-Side Orchestration (Recommended for Deterministic Pipelines)

python

`@mcp.tool
def training_pipeline(dataset_id: str, config: dict) -> dict:
    # ALL of this runs on YOUR server in ONE request
    preprocessed = preprocess_data(dataset_id)      # Step 1
    configured = configure_model(config)            # Step 2
    trained = train_model(preprocessed, configured) # Step 3
    validated = validate_model(trained)             # Step 4
    
    return {"status": "complete", "result": validated}`

**Advantages:**

- ✅ Single network round-trip
- ✅ Guaranteed execution order
- ✅ State persists across steps
- ✅ Full control flow (if/else, loops, error handling)
- ✅ AI can't skip or reorder steps

### Client-Side Orchestration (AI-Driven)

python

`# Register individual tools
@mcp.tool
def preprocess_data(dataset_id: str) -> dict: ...

@mcp.tool
def train_model(data: dict) -> dict: ...

# Use a prompt to guide the AI
@mcp.prompt
def training_guide(dataset_id: str) -> str:
    return """
    1. Call preprocess_data
    2. Call train_model with the result
    3. Call validate_model
    """
```

**What happens:**
```
Client → Server: preprocess_data(...)
Server → Client: {result1}
# AI analyzes, decides next step
Client → Server: train_model(result1)
Server → Client: {result2}
# AI analyzes again
Client → Server: validate_model(result2)`

**Disadvantages:**

- ❌ Multiple network round-trips
- ❌ AI might skip/reorder steps
- ❌ More token consumption (AI reasoning between steps)

---

## Implementing Skills in FastMCP

### Pattern 1: Direct Function Calls (Simplest)

python

`from fastmcp import FastMCP

mcp = FastMCP("AI Twin Server")

def preprocess_data(dataset_id: str) -> dict:
    """Helper function"""
    return {"cleaned": dataset_id}

def train_model(data: dict) -> dict:
    """Helper function"""
    return {"model_id": "123", "accuracy": 0.95}

@mcp.tool
def execute_training_pipeline(dataset_id: str) -> dict:
    """
    Composite skill: orchestrates multiple steps
    """
    preprocessed = preprocess_data(dataset_id)
    trained = train_model(preprocessed)
    return {"result": trained}

if __name__ == "__main__":
    mcp.run()`

### Pattern 2: Hybrid (Atomic + Composite)

python

`from fastmcp import FastMCP

mcp = FastMCP("Hybrid Server")

# Expose as individual tools (for AI flexibility)
@mcp.tool
def preprocess_data(dataset_id: str) -> dict:
    return {"cleaned": dataset_id}

@mcp.tool
def train_model(data: dict) -> dict:
    return {"model_id": "123"}

# Also expose as composite tool (for efficiency)
@mcp.tool
def full_training_workflow(dataset_id: str) -> dict:
    """One-shot pipeline"""
    # Call the decorated functions directly
    preprocessed = preprocess_data(dataset_id)
    trained = train_model(preprocessed)
    return {"result": trained}`

### Pattern 3: Skills Provider (User-Defined Workflows)

python

`from pathlib import Path
from fastmcp import FastMCP
from fastmcp.server.providers.skills import SkillsDirectoryProvider

mcp = FastMCP("Skills Server")

# Expose user-defined skill directories as MCP resources
mcp.add_provider(
    SkillsDirectoryProvider(
        roots=Path.home() / ".claude" / "skills"
    )
)`

**User creates:** `~/.claude/skills/train_model/SKILL.md`

markdown

- `--description: ML training pipeline--# Train Model SkillExecute these steps:
1. Call preprocess_data with dataset_id
2. Call train_model with preprocessed data
3. Call validate_model`

### Pattern 4: Prompts for AI-Driven Composition

python

`@mcp.tool
def step1() -> dict: ...

@mcp.tool
def step2() -> dict: ...

@mcp.prompt
def workflow_guide() -> str:
    """Guide AI to orchestrate tools"""
    return """
    Execute workflow:
    1. Call step1
    2. Call step2 with step1's result
    """
```

---

## Recommended Architecture for AI Twin

### Current Design Issues

Your whiteboard shows:
```
Prompts (Predefined procedures)    Skills (User-defined procedures)
- Update MCP Memory                - Execute Write Article Script
- Update KG                        - Execute Write Article Vision
```

**Problem:** This doesn't align with MCP's actual architecture.

### Corrected Architecture
```
┌──────────────────────────────────────────────────────┐
│              MCP Server Architecture                 │
├──────────────────────────────────────────────────────┤
│                                                      │
│  TOOLS (AI-Invoked, Server-Side Execution)          │
│  ├─ Atomic Tools (Building Blocks)                  │
│  │  ├─ preprocess_data()                           │
│  │  ├─ configure_model()                           │
│  │  ├─ train_model()                               │
│  │  ├─ validate_model()                            │
│  │  ├─ kg_search()                                 │
│  │  └─ kg_write()                                  │
│  │                                                  │
│  └─ Composite Tools (Skills/Workflows)              │
│     ├─ execute_training_pipeline()                  │
│     │   → orchestrates: preprocess → config →      │
│     │     train → validate                         │
│     └─ execute_inference_pipeline()                 │
│         → orchestrates: load_model → predict →     │
│           post_process                             │
│                                                      │
│  RESOURCES (Context/Data Access)                    │
│  ├─ Pipeline Configurations                         │
│  ├─ Model Metadata                                  │
│  ├─ Knowledge Graph Schema                          │
│  └─ Training History                                │
│                                                      │
│  PROMPTS (User-Invoked Workflows) - Optional        │
│  └─ training_workflow_template()                    │
│     (only if you want user-triggered workflows)     │
│                                                      │
└──────────────────────────────────────────────────────┘`

---

## Code Examples

### Complete AI Twin Server Implementation

python

`from fastmcp import FastMCP
from typing import Dict, Any

mcp = FastMCP(
    name="AI Twin Server",
    instructions="""
    This server provides ML training and inference pipelines.
    Use execute_training_pipeline for end-to-end training.
    Use atomic tools for custom workflows.
    """
)

# ═══════════════════════════════════════════════════════
# ATOMIC TOOLS (Building Blocks)
# ═══════════════════════════════════════════════════════

@mcp.tool
def preprocess_data(dataset_id: str) -> Dict[str, Any]:
    """
    Load and preprocess dataset.
    
    Args:
        dataset_id: Unique identifier for the dataset
        
    Returns:
        Preprocessed data ready for training
    """
    # Your preprocessing logic
    return {
        "dataset_id": dataset_id,
        "cleaned_data": "...",
        "feature_count": 10,
        "sample_count": 1000
    }

@mcp.tool
def configure_model(
    model_type: str, 
    hyperparams: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Configure model architecture and hyperparameters.
    
    Args:
        model_type: Type of model (e.g., "neural_network", "random_forest")
        hyperparams: Model hyperparameters
        
    Returns:
        Model configuration
    """
    return {
        "model_type": model_type,
        "config": hyperparams,
        "architecture": "..."
    }

@mcp.tool
def train_model(
    data: Dict[str, Any], 
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Train model with given data and configuration.
    
    Args:
        data: Preprocessed training data
        config: Model configuration
        
    Returns:
        Trained model metadata
    """
    # Your training logic
    return {
        "model_id": "model_abc123",
        "training_loss": 0.05,
        "training_time": "120s",
        "status": "trained"
    }

@mcp.tool
def validate_model(
    model: Dict[str, Any], 
    test_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Validate model performance on test data.
    
    Args:
        model: Trained model metadata
        test_data: Validation dataset
        
    Returns:
        Validation metrics
    """
    return {
        "model_id": model["model_id"],
        "accuracy": 0.95,
        "precision": 0.93,
        "recall": 0.94,
        "validated": True
    }

@mcp.tool
def kg_search(query: str, filters: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Search the knowledge graph.
    
    Args:
        query: Search query
        filters: Optional filters
        
    Returns:
        Search results
    """
    return {
        "results": [...],
        "count": 42
    }

@mcp.tool
def kg_write(entity: str, properties: Dict[str, Any]) -> Dict[str, Any]:
    """
    Write entity to knowledge graph.
    
    Args:
        entity: Entity identifier
        properties: Entity properties
        
    Returns:
        Write confirmation
    """
    return {
        "entity_id": entity,
        "status": "written",
        "timestamp": "2026-02-02T18:00:00Z"
    }

# ═══════════════════════════════════════════════════════
# COMPOSITE TOOLS (Skills/Orchestrated Workflows)
# ═══════════════════════════════════════════════════════

@mcp.tool
def execute_training_pipeline(
    dataset_id: str,
    model_type: str,
    hyperparams: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Complete end-to-end training pipeline.
    
    Orchestrates:
    1. Data preprocessing
    2. Model configuration
    3. Model training
    4. Model validation
    
    Args:
        dataset_id: Dataset to train on
        model_type: Type of model to train
        hyperparams: Model hyperparameters
        
    Returns:
        Complete pipeline results
    """
    # Server-side orchestration - all steps run in one request
    
    # Step 1: Preprocess
    preprocessed = preprocess_data(dataset_id)
    
    # Step 2: Configure
    config = configure_model(model_type, hyperparams)
    
    # Step 3: Train
    trained = train_model(preprocessed, config)
    
    # Step 4: Validate
    validated = validate_model(trained, preprocessed)
    
    return {
        "pipeline": "training",
        "status": "complete",
        "dataset_id": dataset_id,
        "model_id": trained["model_id"],
        "validation_results": validated,
        "overall_status": "success"
    }

@mcp.tool
def execute_inference_pipeline(
    model_id: str,
    input_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Complete inference pipeline.
    
    Orchestrates:
    1. Load model
    2. Run prediction
    3. Post-process results
    
    Args:
        model_id: Model to use for inference
        input_data: Input data for prediction
        
    Returns:
        Inference results
    """
    # Your inference orchestration logic
    return {
        "model_id": model_id,
        "predictions": [...],
        "confidence": 0.92
    }

# ═══════════════════════════════════════════════════════
# RESOURCES (Context/Data)
# ═══════════════════════════════════════════════════════

@mcp.resource("config://training-pipeline")
def get_pipeline_config() -> str:
    """Training pipeline configuration"""
    return """
    {
        "default_model_type": "neural_network",
        "default_hyperparams": {
            "learning_rate": 0.001,
            "epochs": 100
        }
    }
    """

@mcp.resource("schema://knowledge-graph")
def get_kg_schema() -> str:
    """Knowledge graph schema"""
    return """
    {
        "entities": ["Person", "Organization", "Event"],
        "relationships": ["works_at", "attended", "located_in"]
    }
    """

# ═══════════════════════════════════════════════════════
# PROMPTS (Optional - User-Invoked Workflows)
# ═══════════════════════════════════════════════════════

@mcp.prompt
def training_workflow_template(
    dataset_id: str,
    model_type: str = "neural_network"
) -> str:
    """
    Template for guided training workflow.
    Only use if you want user to explicitly invoke workflows.
    """
    return f"""
    Execute training pipeline for dataset '{dataset_id}':
    
    Recommended approach:
    - Use execute_training_pipeline for one-shot execution
    - Or manually call: preprocess_data → configure_model → 
      train_model → validate_model
    
    Model type: {model_type}
    """

# ═══════════════════════════════════════════════════════
# RUN SERVER
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    # For local stdio transport (Claude Desktop)
    mcp.run()
    
    # For HTTP transport (remote access)
    # mcp.run(transport="http", host="0.0.0.0", port=8000)`

---

## Key Takeaways

### 1. MCP Primitives Reality Check

| What You Thought | What Actually Exists |
| --- | --- |
| Prompts = Server-defined procedures | Prompts = User-invoked templates |
| Skills = User-defined procedures | Skills = NOT an MCP primitive |

### 2. How to Implement Skills

✅ **Use composite Tools** for server-side orchestration

✅ **Call Python functions directly** inside tools

✅ **Hybrid approach:** Expose both atomic and composite tools

⚠️ **Prompts are optional** - only if you want user-triggered workflows

❌ **Don't rely on AI to orchestrate** deterministic pipelines

### 3. Where Code Runs

- **All tool code runs on the MCP server**
- **Client-server communication is JSON-RPC**
- **Server-side orchestration = one request, multiple operations**
- **Client-side orchestration = multiple round-trips**

### 4. Recommended Pattern

python

`# Pattern: Hybrid Atomic + Composite Tools

# Expose atomic tools for flexibility
@mcp.tool
def step1(): ...

@mcp.tool
def step2(): ...

# Expose composite tools for efficiency
@mcp.tool
def full_workflow():
    result1 = step1()
    result2 = step2(result1)
    return result2`

### 5. Answer to Paul's Question

**"Do we even need prompts within the MCP protocol?"**

**For your AI Twin use case: NO**

- Your pipelines are **deterministic** (fixed steps)
- You need **guaranteed execution order**
- You want **server-side control**
- **Use composite Tools instead of Prompts**

Prompts are useful for:

- User-triggered workflow templates (slash commands)
- Flexible, AI-driven compositions
- When you want the AI to adapt the sequence

But for your Training/Inference pipelines → **composite Tools are the right choice**.

---

## Quick Reference

### Tool Composition in FastMCP

python

`# ✅ Direct function calls (simplest)
@mcp.tool
def skill():
    result1 = helper_func1()
    result2 = helper_func2(result1)
    return result2

# ✅ Hybrid (atomic + composite)
@mcp.tool
def atomic_tool1(): ...

@mcp.tool
def composite_skill():
    return atomic_tool1()  # Call decorated functions directly

# ✅ With context
@mcp.tool
def skill(data: str, ctx: Context):
    result = atomic_tool(data, ctx)
    return result

# ⚠️ AI-driven (use prompts to guide)
@mcp.prompt
def workflow_guide():
    return "1. Call tool1\\n2. Call tool2"`

---

**End of Guide**

This document provides the complete architectural foundation for implementing your AI Twin MCP server with proper skill orchestration using FastMCP.
