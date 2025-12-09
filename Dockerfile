FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Only system deps needed for pure-Python stack
RUN groupadd --system app && useradd --system --gid app app

COPY pyproject.toml README.md ./
COPY mcp_langgraph_agents ./mcp_langgraph_agents

RUN pip install --no-cache-dir .

USER app
ENTRYPOINT ["mcp-langgraph-server"]
