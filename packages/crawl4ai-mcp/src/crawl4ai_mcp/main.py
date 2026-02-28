"""Main entry point for crawl4ai-mcp."""

from fastmcp import FastMCP
from common_mcp import load_dotenv_file, run_server
from crawl4ai_mcp.register import register_tools

# Load environment variables from dotenv file at startup
load_dotenv_file()

mcp = FastMCP("crawl4ai-mcp")

# Register tools
register_tools(mcp)


def main():
    """Run the MCP server."""
    run_server(mcp, default_port=8000)


if __name__ == "__main__":
    main()
