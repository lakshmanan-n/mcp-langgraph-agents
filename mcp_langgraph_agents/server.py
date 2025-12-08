"""A sample MCP server that orchestrates a handful of LangGraph agents."""

from __future__ import annotations

from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCPServer
from mcp.types import TextContent, Tool, ToolOutput
from pydantic import BaseModel, Field

from .graph import AgentState, build_agent_graph, compile_agent_graph


class AgentChatArguments(BaseModel):
    """Schema used when the MCP client calls the chat tool."""

    message: str = Field(..., description="User message to send to the agent graph")
    thread_id: str | None = Field(
        default=None,
        description="Optional thread identifier to keep the conversation memory scoped",
    )


def _render_messages(messages: List[Dict[str, str]]) -> str:
    visible_agent_messages = [msg["content"] for msg in messages if msg["role"] == "agent"]
    return "\n\n".join(visible_agent_messages)


def create_server() -> FastMCPServer:
    """Instantiate the MCP server and wire up the LangGraph-backed tool."""

    graph, memory = build_agent_graph()
    app = FastMCPServer("langgraph-agents")

    @app.list_tools()
    async def list_tools() -> List[Tool]:  # noqa: D401 - MCP spec naming
        """MCP hook used to advertise available tools."""

        return [
            Tool(
                name="agent_chat",
                description=(
                    "Route a message through a small LangGraph of todo, analysis, and echo agents. "
                    "Provide an optional thread_id to reuse conversation memory."
                ),
                inputSchema=AgentChatArguments.model_json_schema(),
            )
        ]

    @app.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[ToolOutput]:  # noqa: D401
        """Execute a tool request from an MCP client."""

        if name != "agent_chat":
            raise ValueError(f"Unknown tool requested: {name}")

        payload = AgentChatArguments.model_validate(arguments)
        state: AgentState = {"messages": [{"role": "user", "content": payload.message}], "todos": []}

        compiled = compile_agent_graph(graph, memory)
        result = compiled.invoke(
            state,
            config={"configurable": {"thread_id": payload.thread_id or "default"}},
        )

        rendered = _render_messages(result["messages"])
        todo_items = result["todos"]
        return [
            ToolOutput(
                tool_name=name,
                content=[
                    TextContent(text=rendered),
                    TextContent(text=f"Tracked todos: {todo_items}"),
                ],
            )
        ]

    return app


def run() -> None:
    """Run the MCP server via stdio entry point."""

    create_server().run()


if __name__ == "__main__":
    run()
