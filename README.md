# mcp-langgraph-agents

Multi-agent orchestration with MCP and LangGraph for modular AI workflows.

## What this sample includes

This repository contains a minimal Model Context Protocol (MCP) server wired to a
LangGraph that coordinates three deterministic agents:

- **Router node** – examines the latest user message and chooses the next agent.
- **Todo agent** – captures tasks when the message includes the word "todo" and
  keeps a running list scoped to a conversation thread.
- **Analysis agent** – provides a structured, deterministic analysis for "why" or
  "because"-style prompts.
- **Echo agent** – mirrors the latest user message for quick feedback.

The LangGraph is backed by an in-memory checkpointer so threads can reuse prior
state (messages and todos) when a caller supplies a `thread_id`. The MCP server
exposes a single `agent_chat` tool that forwards requests into the compiled
graph and returns the collected agent responses and the current todo list.

### File-by-file breakdown

- `mcp_langgraph_agents/graph.py`: Defines the graph state (`messages`, `todos`),
  router logic, individual agent behaviors, and the `build_agent_graph` helper
  that wires nodes together with LangGraph's `StateGraph`. The module also
  exports `compile_agent_graph` to enable checkpointing via LangGraph's
  `MemorySaver`.
- `mcp_langgraph_agents/server.py`: Implements an MCP stdio server with FastMCP
  that publishes the `agent_chat` tool, validates user input with a Pydantic
  model, routes each call through the compiled graph, and renders agent replies
  plus tracked todos.
- `pyproject.toml`: Declares package metadata, dependencies (`mcp`, `langgraph`,
  `pydantic`), and the console entry point `mcp-langgraph-server` for running
  the server over stdio.
- `README.md` (this file): Documents setup steps, tool contract, and the
  architecture summary above.

## Getting started

1. Install dependencies (Python 3.11+):

   ```bash
   pip install -e .
   ```

2. Launch the MCP server over stdio:

   ```bash
   mcp-langgraph-server
   ```

3. From an MCP-compatible client, call the `agent_chat` tool with a message and an
   optional `thread_id` to retain memory across calls.

### Tool contract

The `agent_chat` tool accepts the following JSON payload:

```json
{
  "message": "Summarize why we need tests and add todo: stabilize CI",
  "thread_id": "demo-thread"
}
```

The response includes the combined agent messages and the tracked todo list for the
provided thread.
