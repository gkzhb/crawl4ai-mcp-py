"""Main entry point for searxng-mcp."""

from fastmcp import FastMCP
from common_mcp import load_dotenv_file, run_server
from searxng_mcp.register import register_tools

# Load environment variables from dotenv file at startup
load_dotenv_file()

mcp = FastMCP("searxng-mcp")

# Register tools
register_tools(mcp)


def main():
    """Run the MCP server."""
    run_server(mcp, default_port=8001)


if __name__ == "__main__":
    main()
