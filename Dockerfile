FROM python:3.11-slim

WORKDIR /app

# Copy project files
COPY pyproject.toml README.md LICENSE ./
COPY src/ ./src/

# Install the package in editable mode
RUN pip install --no-cache-dir -e .

# Run the MCP server via stdio
CMD ["mcp-langgraph-server"]

