"""Main entry point for crawl4ai-mcp."""
from fastmcp import FastMCP
from common_mcp import run_server
from crawl4ai_mcp.register import register_tools

mcp = FastMCP("crawl4ai-mcp")

# Register tools
register_tools(mcp)


def main():
    """Run the MCP server."""
    run_server(mcp, default_port=8000)


if __name__ == "__main__":
    main()