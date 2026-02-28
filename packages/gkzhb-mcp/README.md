# gkzhb-mcp

Unified MCP server for web tools - combines crawl4ai-mcp, searxng-mcp, and agent-skills-mcp into a single server.

## Features

This unified server provides the following capabilities:

- **crawl4ai**: Web crawling and content extraction
  - Convert web pages to markdown format
  - Convert web pages to cleaned HTML format
  - Extract internal and external links
  - Support for remote Chrome CDP endpoint
  - Proxy support

- **searxng**: Web search capabilities
  - Search the web using Searxng
  - Retrieve search results with content
  - Display infoboxes and structured data

- **skills**: Agent Skills integration
  - Access to [Agent Skills](https://agentskills.io/home) for enhanced AI capabilities
  - Dynamic skill loading and registration

## Installation

```bash
uv sync --all-packages
```

## Usage

```bash
# Run as stdio (default) with all tools enabled
uv run gkzhb-mcp

# Run with SSE transport
MCP_TYPE=sse uv run gkzhb-mcp

# Run with HTTP transport
MCP_TYPE=http uv run gkzhb-mcp

# Enable only specific tools
MCP_TOOL_LIST=crawl4ai,searxng uv run gkzhb-mcp
MCP_TOOL_LIST=skills uv run gkzhb-mcp
```

## Environment Variables

### Common Configuration
- `MCP_TYPE`: Transport type (stdio|sse|http), defaults to "stdio"
- `MCP_HOST`: Host address for SSE/HTTP modes, defaults to "127.0.0.1"
- `MCP_PORT`: Port for SSE/HTTP modes, defaults to "8000"
- `ENV`: Environment mode (development|production), defaults to "development"
- `LOG_LEVEL`: Logging level (DEBUG|INFO|WARNING|ERROR), defaults to "DEBUG" in development, "INFO" in production
- `MCP_AUTH`: Comma-separated auth tokens for authentication (optional)
- `DOTENV_FILE`: Path to dotenv file to load environment variables from (optional)

### Authentication

When `MCP_AUTH` is set, you need to include the auth token in the request header when connecting to the MCP server:

```bash
Authorization: Bearer <your-token>
```

Example:
```bash
curl -H "Authorization: Bearer my-secret-token" http://localhost:8000/mcp
```

### Tool Selection
- `MCP_TOOL_LIST`: Comma-separated list of tools to enable (crawl4ai,searxng,skills), defaults to all tools

### Crawl4AI Configuration
- `CHROME_CDP_ENDPOINT`: Chrome DevTools Protocol WebSocket URL for remote Chrome instance (optional)
- `CRAWL4AI_PROXY_SERVER`: Proxy server URL (optional)
- `CRAWL4AI_PROXY_USERNAME`: Proxy username (optional)
- `CRAWL4AI_PROXY_PASSWORD`: Proxy password (optional)

### Searxng Configuration
- `SEARXNG_URL`: Searxng instance URL, defaults to "http://localhost:8080"

## Examples

### Production deployment with SSE
```bash
ENV=production \
LOG_LEVEL=INFO \
MCP_TYPE=sse \
MCP_HOST=0.0.0.0 \
MCP_PORT=8000 \
MCP_AUTH=your-secret-token \
uv run gkzhb-mcp
```

### Using remote Chrome for crawling
```bash
CHROME_CDP_ENDPOINT=ws://chrome-browser:9222 \
uv run gkzhb-mcp
```

### Enable only web crawling and search
```bash
MCP_TOOL_LIST=crawl4ai,searxng \
uv run gkzhb-mcp
```