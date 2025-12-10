"""Utilities for building a small LangGraph-powered agent team."""

from __future__ import annotations

from typing import Literal, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict):
    """Shared state flowing between the agents in the graph."""

    messages: list[dict[str, str]]
    todos: list[str]


def _append_agent_message(state: AgentState, content: str) -> AgentState:
    updated_messages = state["messages"] + [{"role": "agent", "content": content}]
    return {**state, "messages": updated_messages}


def _router_node(state: AgentState) -> AgentState:
    """Router node that passes state through without modification."""
    return state


def _route(state: AgentState) -> Literal["todo_agent", "analysis_agent", "echo_agent"]:
    """Routing function that determines which agent to call next."""
    user_message = state["messages"][-1]["content"].lower()
    if "todo" in user_message:
        return "todo_agent"
    if any(keyword in user_message for keyword in ("why", "because", "explain", "analysis")):
        return "analysis_agent"
    return "echo_agent"


def _todo_agent(state: AgentState) -> AgentState:
    message = state["messages"][-1]["content"]
    additions = [item.strip() for item in message.split("todo")[-1].split(",") if item.strip()]
    next_todos = state["todos"] + additions if additions else state["todos"]
    todo_summary = "\n".join(f"- {item}" for item in next_todos) or "(no items yet)"
    content = (
        "I captured your tasks. Current list:\n"
        f"{todo_summary}\n"
        "Use 'todo' again to add more items."
    )
    return _append_agent_message({**state, "todos": next_todos}, content)


def _analysis_agent(state: AgentState) -> AgentState:
    prompt = state["messages"][-1]["content"]
    content = (
        "Here is a lightweight analysis of your request:\n"
        f"- Main idea: {prompt}\n"
        "- Signal: I am a deterministic reasoning helper, not an LLM.\n"
        "- Next step: ask the todo agent to track follow-ups or simply continue chatting."
    )
    return _append_agent_message(state, content)


def _echo_agent(state: AgentState) -> AgentState:
    user_message = state["messages"][-1]["content"]
    content = f"Echo agent here. You said: '{user_message}'."
    return _append_agent_message(state, content)


def build_agent_graph() -> tuple[StateGraph[AgentState], MemorySaver]:
    """Create the multi-agent LangGraph and in-memory checkpointer."""

    graph = StateGraph(AgentState)

    graph.add_node("router", _router_node)
    graph.add_node("todo_agent", _todo_agent)
    graph.add_node("analysis_agent", _analysis_agent)
    graph.add_node("echo_agent", _echo_agent)

    graph.set_entry_point("router")
    graph.add_conditional_edges(
        "router",
        _route,
        {
            "todo_agent": "todo_agent",
            "analysis_agent": "analysis_agent",
            "echo_agent": "echo_agent",
        },
    )

    graph.add_edge("todo_agent", END)
    graph.add_edge("analysis_agent", END)
    graph.add_edge("echo_agent", END)

    memory = MemorySaver()
    return graph, memory


def compile_agent_graph(graph: StateGraph[AgentState], memory: MemorySaver):
    """Return the executable graph with memory enabled."""

    return graph.compile(checkpointer=memory)
