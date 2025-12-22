# Web Crawl and Search MCP Servers

- [crawl4ai-mcp-py](./packages/crawl4ai-mcp-py/README.md): Convert Web page to md or html
- [searxng-mcp-py](./packages/searxng-mcp-py/README.md): Search Web with Searxng
- [agent-skills-mcp-py](./packages/agent-skills-mcp-py/README.md): [Agent Skills](https://agentskills.io/home) MCP

## Environment Variables
- `MCP_TYPE`: Transport type ( `stdio` , `sse` , `http` ) - defaults to "stdio"
- `MCP_HOST`: Host address for SSE/HTTP modes - defaults to "127.0.0.1"
- `MCP_PORT`: Listening port for SSE/HTTP modes - defaults to "8000" or "8001"(more details in project readme file)

For SSE type, connect to url http://localhost:8000/sse .
For HTTP type, connect to url http://localhost:8000/mcp .
