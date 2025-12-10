#!/usr/bin/env python3
"""Test script to demonstrate agent routing based on input messages."""

import sys
import os

# Add src to path for imports (go up one directory from tests/)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mcp_langgraph_agents.graph import AgentState, build_agent_graph, compile_agent_graph


def test_routing_directly():
    """Test routing by directly invoking the graph to see which agent is called."""
    print("=" * 60)
    print("Testing Agent Routing Logic")
    print("=" * 60)
    print()
    
    graph, memory = build_agent_graph()
    compiled = compile_agent_graph(graph, memory)
    
    # Test cases to demonstrate routing
    test_cases = [
        ("Hello, how are you?", "echo_agent"),
        ("Add todo: buy groceries, clean house", "todo_agent"),
        ("Why is the sky blue?", "analysis_agent"),
        ("Can you explain quantum physics?", "analysis_agent"),
        ("I need to todo: finish project", "todo_agent"),
        ("What is the weather?", "echo_agent"),
        ("Because I said so", "analysis_agent"),
        ("Please add todo: call mom", "todo_agent"),
        ("Just a regular message", "echo_agent"),
    ]
    
    for message, expected_agent in test_cases:
        print(f"Input: '{message}'")
        print(f"Expected Agent: {expected_agent}")
        
        # Create initial state
        state: AgentState = {
            "messages": [{"role": "user", "content": message}],
            "todos": []
        }
        
        # Invoke the graph
        result = compiled.invoke(
            state,
            config={"configurable": {"thread_id": "test"}},
        )
        
        # Extract agent response
        agent_messages = [msg["content"] for msg in result["messages"] if msg["role"] == "agent"]
        if agent_messages:
            response = agent_messages[0]
            # Determine which agent responded based on response content
            if "captured your tasks" in response.lower() or "current list" in response.lower():
                actual_agent = "todo_agent"
            elif "lightweight analysis" in response.lower() or "main idea" in response.lower():
                actual_agent = "analysis_agent"
            elif "echo agent" in response.lower():
                actual_agent = "echo_agent"
            else:
                actual_agent = "unknown"
            
            print(f"Actual Agent: {actual_agent}")
            print(f"Response: {response[:100]}..." if len(response) > 100 else f"Response: {response}")
        else:
            print("No agent response found")
        
        print("-" * 60)
        print()


def show_routing_rules():
    """Display the routing rules clearly."""
    print("=" * 60)
    print("Agent Routing Rules")
    print("=" * 60)
    print()
    print("The router checks the user message (case-insensitive) in this order:")
    print()
    print("1. TODO AGENT:")
    print("   → Triggers if message contains: 'todo'")
    print("   → Example: 'Add todo: buy milk'")
    print("   → Example: 'I need to todo: finish homework'")
    print()
    print("2. ANALYSIS AGENT:")
    print("   → Triggers if message contains: 'why', 'because', 'explain', or 'analysis'")
    print("   → Example: 'Why is Python popular?'")
    print("   → Example: 'Can you explain this?'")
    print("   → Example: 'Because I need it'")
    print()
    print("3. ECHO AGENT (default):")
    print("   → Triggers for all other messages")
    print("   → Example: 'Hello, how are you?'")
    print("   → Example: 'What is the weather?'")
    print()
    print("=" * 60)
    print()


if __name__ == "__main__":
    show_routing_rules()
    test_routing_directly()
    
    print("\n" + "=" * 60)
    print("To test with the actual MCP server:")
    print("1. Install dependencies: pip install -e .")
    print("2. Run: python main.py (or mcp-langgraph-server)")
    print("3. Use an MCP client to call the 'agent_chat' tool")
    print("4. Or use the MCP Inspector tool")
    print("=" * 60)

