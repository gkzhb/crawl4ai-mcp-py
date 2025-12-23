# SearXNG MCP Python Server

A minimal MCP (Model Context Protocol) server that provides web search capabilities using SearXNG. This server exposes tools to search the web and return formatted results.

## Features
- Search the web using SearXNG meta-search engine
- Return formatted search results with titles, URLs, and content snippets
- Support for multiple transport modes (stdio, SSE, HTTP)
- Built with FastMCP and httpx

## Installation

### Clone this repo
```bash
git clone https://github.com/gkzhb/crawl4ai-mcp-py.git
cd crawl4ai-mcp-py/packages/searxng-mcp-py
```

### Using uv install deps
```bash
uv sync
```

### Setup SearXNG
You need to have a SearXNG instance running. You can:
- Run your own SearXNG instance locally (recommended)
- Use a public SearXNG instance

To run SearXNG locally with Docker:
```bash
docker run --rm -d -p 8080:8080 searxng/searxng
```

## Usage

### Environment Variables
- `SEARXNG_URL`: SearXNG instance URL (defaults to "http://localhost:8080")
- `MCP_TYPE`: Transport type (`stdio`, `sse`, `http`) - defaults to "stdio"
- `MCP_HOST`: Host address for SSE/HTTP modes - defaults to "127.0.0.1"
- `MCP_PORT`: Listening port for SSE/HTTP modes - defaults to "8001"

### Run with stdio (default)
```bash
uv run main.py
```

### Run with SSE transport
```bash
MCP_TYPE=sse uv run main.py
```

### Run with HTTP transport
```bash
MCP_TYPE=http uv run main.py
```

### Custom host configuration
```bash
MCP_HOST=0.0.0.0 MCP_TYPE=sse uv run main.py
```

### Custom SearXNG URL
```bash
SEARXNG_URL=https://searx.example.com uv run main.py
```

## Available Tools

### search_web
Search the web using SearXNG and return formatted results.

**Parameters:**
- `query` (string): The search query
- `limit` (integer, optional): Maximum number of results to return (default: 5)

**Returns:**
Formatted string containing search results with titles, URLs, and content snippets, plus any infoboxes if available.
