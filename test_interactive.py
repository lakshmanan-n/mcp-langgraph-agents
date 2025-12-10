#!/usr/bin/env python3
"""Interactive test script to test the agent routing."""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_langgraph_agents.graph import AgentState, build_agent_graph, compile_agent_graph


def test_single_message(message: str, thread_id: str = "test"):
    """Test a single message and show the result."""
    graph, memory = build_agent_graph()
    compiled = compile_agent_graph(graph, memory)
    
    state: AgentState = {
        "messages": [{"role": "user", "content": message}],
        "todos": []
    }
    
    result = compiled.invoke(
        state,
        config={"configurable": {"thread_id": thread_id}},
    )
    
    # Extract agent response
    agent_messages = [msg["content"] for msg in result["messages"] if msg["role"] == "agent"]
    todos = result["todos"]
    
    print("\n" + "=" * 60)
    print(f"Input: '{message}'")
    print("-" * 60)
    
    if agent_messages:
        response = agent_messages[0]
        # Determine which agent responded
        if "captured your tasks" in response.lower() or "current list" in response.lower():
            agent = "📝 TODO AGENT"
        elif "lightweight analysis" in response.lower() or "main idea" in response.lower():
            agent = "🔍 ANALYSIS AGENT"
        elif "echo agent" in response.lower():
            agent = "📢 ECHO AGENT"
        else:
            agent = "❓ UNKNOWN"
        
        print(f"Agent: {agent}")
        print(f"\nResponse:\n{response}")
        if todos:
            print(f"\nTodos: {todos}")
    else:
        print("No agent response found")
    
    print("=" * 60 + "\n")
    
    return result


def interactive_mode():
    """Run in interactive mode."""
    print("\n" + "=" * 60)
    print("Interactive Agent Routing Test")
    print("=" * 60)
    print("\nEnter messages to test routing. Type 'quit' or 'exit' to stop.\n")
    
    thread_id = "interactive-test"
    
    while True:
        try:
            message = input("Enter message: ").strip()
            
            if message.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break
            
            if not message:
                continue
            
            test_single_message(message, thread_id)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test agent routing")
    parser.add_argument(
        "-m", "--message",
        help="Test a single message",
        type=str
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    
    args = parser.parse_args()
    
    if args.message:
        test_single_message(args.message)
    elif args.interactive:
        interactive_mode()
    else:
        # Show examples
        print("\n" + "=" * 60)
        print("Quick Test Examples")
        print("=" * 60)
        print("\nTesting different routing scenarios...\n")
        
        examples = [
            "Hello, how are you?",
            "Add todo: buy groceries",
            "Why is Python popular?",
        ]
        
        for example in examples:
            test_single_message(example)
        
        print("\n" + "=" * 60)
        print("Usage:")
        print("  python3 test_interactive.py -m 'Your message here'")
        print("  python3 test_interactive.py -i  (interactive mode)")
        print("=" * 60 + "\n")

