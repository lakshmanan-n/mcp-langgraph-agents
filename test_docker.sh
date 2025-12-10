#!/bin/bash
# Quick test script for Docker container

CONTAINER_NAME="mcp_langgraph_agents"

echo "=========================================="
echo "Testing MCP LangGraph Agents in Docker"
echo "=========================================="
echo ""

# Check if container is running
if ! docker ps | grep -q "$CONTAINER_NAME"; then
    echo "❌ Container '$CONTAINER_NAME' is not running!"
    echo "   Start it with: docker-compose up -d"
    exit 1
fi

echo "✅ Container is running"
echo ""

# Test 1: Echo Agent
echo "Test 1: Echo Agent"
echo "-------------------"
docker exec -it "$CONTAINER_NAME" python3 tests/test_interactive.py -m "Hello, how are you?"
echo ""

# Test 2: Todo Agent
echo "Test 2: Todo Agent"
echo "-------------------"
docker exec -it "$CONTAINER_NAME" python3 tests/test_interactive.py -m "Add todo: buy groceries, clean house"
echo ""

# Test 3: Analysis Agent
echo "Test 3: Analysis Agent"
echo "-------------------"
docker exec -it "$CONTAINER_NAME" python3 tests/test_interactive.py -m "Why is Python popular?"
echo ""

echo "=========================================="
echo "All tests completed!"
echo ""
echo "To run interactive mode:"
echo "  docker exec -it $CONTAINER_NAME python3 tests/test_interactive.py -i"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo "=========================================="

