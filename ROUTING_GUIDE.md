# Agent Routing Guide

This guide explains how to test and see which agent routes your input messages.

## Routing Logic

The router in `graph.py` (lines 23-29) checks messages in this order:

1. **TODO AGENT** - Triggers if message contains: `"todo"`
2. **ANALYSIS AGENT** - Triggers if message contains: `"why"`, `"because"`, `"explain"`, or `"analysis"`
3. **ECHO AGENT** (default) - Triggers for all other messages

**Note:** All checks are case-insensitive.

## How to Test Routing

### Method 1: Run the Test Script

```bash
# First install dependencies
pip install -e .

# Then run the test script
python3 tests/test_routing.py

# Or run the interactive test
python3 tests/test_interactive.py -m "Your message here"
python3 tests/test_interactive.py -i  # Interactive mode
```

This will show you:
- The routing rules
- Test cases with expected vs actual agent routing
- Agent responses for each input

### Method 2: Test via MCP Server

1. **Start the MCP server:**
   ```bash
   python main.py
   # or
   mcp-langgraph-server
   ```

2. **Use an MCP client** to call the `agent_chat` tool with different messages:

   **Example 1: Echo Agent**
   ```json
   {
     "message": "Hello, how are you?",
     "thread_id": "test-1"
   }
   ```
   **Expected:** Routes to `echo_agent` → Response: "Echo agent here. You said: 'Hello, how are you?'."

   **Example 2: Todo Agent**
   ```json
   {
     "message": "Add todo: buy groceries, clean house",
     "thread_id": "test-2"
   }
   ```
   **Expected:** Routes to `todo_agent` → Response includes "I captured your tasks" and shows the todo list.

   **Example 3: Analysis Agent**
   ```json
   {
     "message": "Why is Python popular?",
     "thread_id": "test-3"
   }
   ```
   **Expected:** Routes to `analysis_agent` → Response includes "lightweight analysis" and "Main idea".

### Method 3: Direct Python Testing

Create a simple test file:

```python
import sys
sys.path.insert(0, 'src')

from mcp_langgraph_agents.graph import AgentState, build_agent_graph, compile_agent_graph

# Build and compile graph
graph, memory = build_agent_graph()
compiled = compile_agent_graph(graph, memory)

# Test a message
message = "Add todo: test this"
state: AgentState = {
    "messages": [{"role": "user", "content": message}],
    "todos": []
}

result = compiled.invoke(
    state,
    config={"configurable": {"thread_id": "test"}},
)

# Print the result
print("Agent messages:", result["messages"])
print("Todos:", result["todos"])
```

## Identifying Which Agent Responded

You can identify which agent handled your request by the response content:

- **Todo Agent**: Response contains "captured your tasks" or "Current list"
- **Analysis Agent**: Response contains "lightweight analysis" or "Main idea"
- **Echo Agent**: Response starts with "Echo agent here"

## Test Cases

| Input Message | Expected Agent | Key Words |
|--------------|----------------|-----------|
| "Hello world" | echo_agent | (none) |
| "Add todo: buy milk" | todo_agent | "todo" |
| "Why is this?" | analysis_agent | "why" |
| "Can you explain?" | analysis_agent | "explain" |
| "Because I said so" | analysis_agent | "because" |
| "I need analysis" | analysis_agent | "analysis" |
| "Regular message" | echo_agent | (none) |

## Using Thread IDs

The `thread_id` parameter allows you to maintain conversation state:

```python
# First call - adds todos
{"message": "Add todo: task1", "thread_id": "my-thread"}

# Second call - todos persist
{"message": "Add todo: task2", "thread_id": "my-thread"}
# Response will show both task1 and task2

# Different thread - fresh state
{"message": "Add todo: task3", "thread_id": "other-thread"}
# Response will only show task3
```

## Docker Testing

To test in Docker:

```bash
# Build and run
docker-compose up --build

# In another terminal, you can test via MCP client
# Or check logs to see routing behavior
docker-compose logs -f
```

