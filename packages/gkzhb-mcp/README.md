# gkzhb-mcp

Unified MCP server for web tools - combines crawl4ai-mcp, searxng-mcp, and agent-skills-mcp.

## Installation

```bash
uv sync --all-packages
```

## Usage

```bash
# Run as stdio (default)
uv run gkzhb-mcp

# Run with SSE transport
MCP_TYPE=sse uv run gkzhb-mcp

# Run with HTTP transport
MCP_TYPE=http uv run gkzhb-mcp
```

## Environment Variables

- `MCP_TYPE`: Transport type (stdio|sse|http), defaults to "stdio"
- `MCP_HOST`: Host address for SSE/HTTP modes, defaults to "127.0.0.1"
- `MCP_PORT`: Port for SSE/HTTP modes, defaults to "8000"