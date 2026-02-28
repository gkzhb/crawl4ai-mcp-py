# Web Crawl and Search MCP Servers

- [crawl4ai-mcp](./packages/crawl4ai-mcp/README.md): Convert Web page to md or html
- [searxng-mcp](./packages/searxng-mcp/README.md): Search Web with Searxng
- [agent-skills-mcp](./packages/agent-skills-mcp/README.md): [Agent Skills](https://agentskills.io/home) MCP
- [gkzhb-mcp](./packages/gkzhb-mcp/README.md): Unified MCP server combining crawl4ai, searxng, and agent-skills

## Common Environment Variables

All MCP servers support the following common environment variables (configured via common-mcp):

- `MCP_TYPE`: Transport type ( `stdio` , `sse` , `http` ) - defaults to "stdio"
- `MCP_HOST`: Host address for SSE/HTTP modes - defaults to "127.0.0.1"
- `MCP_PORT`: Listening port for SSE/HTTP modes - defaults to "8000" or "8001"(more details in project readme file)
- `ENV`: Environment mode (`development` or `production`) - defaults to "development"
- `LOG_LEVEL`: Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) - defaults to "DEBUG" in development, "INFO" in production
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

For SSE type, connect to url http://localhost:8000/sse .
For HTTP type, connect to url http://localhost:8000/mcp .

## gkzhb-mcp Features

The gkzhb-mcp server provides a unified MCP server that combines multiple tools:

- **crawl4ai**: Web crawling and content extraction (convert pages to markdown/HTML)
- **searxng**: Web search capabilities using Searxng
- **skills**: Agent Skills integration for enhanced AI capabilities

You can selectively enable tools using the `MCP_TOOL_LIST` environment variable:

```bash
# Enable only crawl4ai and searxng
MCP_TOOL_LIST=crawl4ai,searxng uv run gkzhb-mcp

# Enable only skills
MCP_TOOL_LIST=skills uv run gkzhb-mcp
```
