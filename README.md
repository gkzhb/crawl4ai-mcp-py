# Crawl4AI MCP Python Server

A minimal MCP (Model Context Protocol) server that provides web crawling capabilities using crawl4ai. This server exposes tools to convert web pages to markdown or HTML format.

## Features
- Convert web pages to clean markdown content
- Convert web pages to cleaned HTML content
- Support for multiple transport modes (stdio, SSE, streamable-http)
- Built with FastMCP and crawl4ai

## Installation

### Clone this repo
```bash
git clone https://github.com/gkzhb/crawl4ai-mcp-py.git
cd crawl4ai-mcp-py
```

### Using uv install deps
```bash
uv sync
```

### Check crawl4ai setup

```bash
# Run post-installation setup
crawl4ai-setup

# Or verify your installation
crawl4ai-doctor
```

You need to do this to correctly configure playwright which will be used to launch and control web browsers.

## Usage

### Run with stdio (default)
```bash
uv run main.py
```

### Run with SSE transport
```bash
MCP_TYPE=sse uv run main.py
```

### Run with streamable-http transport
```bash
MCP_TYPE=streamable-http uv run main.py
```

### Custom host configuration
```bash
MCP_HOST=0.0.0.0 MCP_TYPE=sse uv run main.py
```

## Environment Variables
- `MCP_TYPE`: Transport type ( `stdio` , `sse` , `streamable-http` ) - defaults to "stdio"
- `MCP_HOST`: Host address for SSE/HTTP modes - defaults to "127.0.0.1"
- `MCP_PORT`: Listening port for SSE/HTTP modes - defaults to "8000"