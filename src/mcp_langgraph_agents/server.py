"""A sample MCP server that orchestrates a handful of LangGraph agents."""

from __future__ import annotations

from typing import Dict, List

from fastmcp import FastMCP

from .graph import AgentState, build_agent_graph, compile_agent_graph


def _render_messages(messages: List[Dict[str, str]]) -> str:
    visible_agent_messages = [msg["content"] for msg in messages if msg["role"] == "agent"]
    return "\n\n".join(visible_agent_messages)


# Initialize graph and memory once
_graph, _memory = build_agent_graph()


def create_server() -> FastMCP:
    """Instantiate the MCP server and wire up the LangGraph-backed tool."""

    app = FastMCP("langgraph-agents")

    @app.tool()
    def agent_chat(message: str, thread_id: str | None = None) -> str:
        """
        Route a message through a small LangGraph of todo, analysis, and echo agents.
        Provide an optional thread_id to reuse conversation memory.
        """
        state: AgentState = {"messages": [{"role": "user", "content": message}], "todos": []}

        compiled = compile_agent_graph(_graph, _memory)
        result = compiled.invoke(
            state,
            config={"configurable": {"thread_id": thread_id or "default"}},
        )

        rendered = _render_messages(result["messages"])
        todo_items = result["todos"]
        return f"{rendered}\n\nTracked todos: {todo_items}"

    return app


def run() -> None:
    """Run the MCP server via stdio entry point."""

    create_server().run()


if __name__ == "__main__":
    run()
