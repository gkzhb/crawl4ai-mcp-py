"""Main entry point for searxng-mcp."""
from fastmcp import FastMCP
from common_mcp import run_server
from searxng_mcp.register import register_tools

mcp = FastMCP("searxng-mcp")

# Register tools
register_tools(mcp)


def main():
    """Run the MCP server."""
    run_server(mcp, default_port=8001)


if __name__ == "__main__":
    main()