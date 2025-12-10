# Testing MCP Server in Docker

After running `docker-compose up --build`, here are several ways to test your messages:

## Method 1: Execute Test Scripts Inside Container

Run the test scripts directly in the running container:

```bash
# Run routing tests
docker exec -it mcp_langgraph_agents python3 tests/test_routing.py

# Run interactive test with a message
docker exec -it mcp_langgraph_agents python3 tests/test_interactive.py -m "Add todo: test this"

# Run in interactive mode
docker exec -it mcp_langgraph_agents python3 tests/test_interactive.py -i
```

## Method 2: Use Python REPL in Container

```bash
# Enter Python REPL in the container
docker exec -it mcp_langgraph_agents python3

# Then in Python:
>>> import sys
>>> sys.path.insert(0, '/app/src')
>>> from mcp_langgraph_agents.graph import AgentState, build_agent_graph, compile_agent_graph
>>> 
>>> graph, memory = build_agent_graph()
>>> compiled = compile_agent_graph(graph, memory)
>>> 
>>> state = {"messages": [{"role": "user", "content": "Add todo: buy groceries"}], "todos": []}
>>> result = compiled.invoke(state, config={"configurable": {"thread_id": "test"}})
>>> print(result["messages"])
>>> print(result["todos"])
```

## Method 3: Check Container Logs

View what's happening in the container:

```bash
# View logs
docker-compose logs -f

# View last 50 lines
docker-compose logs --tail=50
```

## Method 4: Use MCP Inspector (External Tool)

If you have MCP Inspector installed:

```bash
# Install MCP Inspector (if not installed)
npm install -g @modelcontextprotocol/inspector

# Connect to the container's stdio
docker exec -it mcp_langgraph_agents mcp-langgraph-server | mcp-inspector
```

## Method 5: Direct Container Execution

Run commands directly in the container:

```bash
# Get a shell in the container
docker exec -it mcp_langgraph_agents /bin/bash

# Then you can run Python scripts or interact with the server
```

## Quick Test Commands

```bash
# Test echo agent
docker exec -it mcp_langgraph_agents python3 tests/test_interactive.py -m "Hello world"

# Test todo agent
docker exec -it mcp_langgraph_agents python3 tests/test_interactive.py -m "Add todo: buy groceries"

# Test analysis agent
docker exec -it mcp_langgraph_agents python3 tests/test_interactive.py -m "Why is Python popular?"
```

