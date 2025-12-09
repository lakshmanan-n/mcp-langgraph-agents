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

## Running with Docker

1. Build the image from the repository root:

   ```bash
   docker build -t mcp-langgraph-agents .
   ```

2. Run the MCP server over stdio inside the container. Attach with `-it` so your
   MCP client can stream input/output through the terminal. If your client or
   downstream tools require API keys (for example, `GROQ_API_KEY` for Groq's
   client), pass them through with `-e`:

   ```bash
   docker run --rm -it \
     -e GROQ_API_KEY="<your_api_key_if_needed>" \
     mcp-langgraph-agents
   ```

   The entrypoint executes `mcp-langgraph-server`, so the container will behave
   the same as running the CLI locally. Connect your MCP-compatible client to
   the container's stdio or adapt the command to your client's launch method
   (e.g., `docker run --rm -i` when piping input).

## Running in PyCharm

1. Open the repository folder (`mcp-langgraph-agents`) in PyCharm.
2. Create a Python interpreter for the project (Python 3.11+). If prompted, let
   PyCharm create a virtual environment and set it as the project interpreter.
3. Install dependencies inside that interpreter:

   ```bash
   pip install -e .
   ```

4. Create a **Run Configuration**:
   - Type: **Python**.
   - Name: `mcp-langgraph-server` (or similar).
   - Module name: `mcp_langgraph_agents.server` (PyCharm will run `python -m mcp_langgraph_agents.server`).
   - Working directory: project root (folder containing `pyproject.toml`).

   Alternatively, set **Script path** to the `mcp-langgraph-server` console
   script installed by the project and keep the working directory at the project
   root.

5. Run the configuration. The MCP server will start over stdio; connect to it
   from your MCP-compatible client and invoke the `agent_chat` tool as shown
   above. Reuse a `thread_id` to keep conversation context and todo items
   between calls.

### Docker commands to use from PyCharm

If you prefer to build and run the container from PyCharm's built-in terminal,
use these commands from the project root:

```bash
# Build the image
docker build -t mcp-langgraph-agents .

# Run the MCP server in the container over stdio
docker run --rm -it mcp-langgraph-agents
```

For a **Docker** run configuration instead of Python:

1. Add a new **Docker** configuration.
2. Set **Image tag** to `mcp-langgraph-agents` (PyCharm can build it using the
   Dockerfile in the project root).
3. Set **Container name** to something like `mcp-langgraph-agents-dev` and add
   `--rm -it` to **Run options** so stdio is interactive.
4. Leave the command at the image's default (`mcp-langgraph-server`) or specify
   `/usr/local/bin/mcp-langgraph-server` explicitly.
5. Start the configuration and connect your MCP client to the container's
   stdio stream.

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
