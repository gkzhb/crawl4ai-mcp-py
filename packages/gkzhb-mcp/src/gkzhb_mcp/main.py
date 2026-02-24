"""Main entry point for gkzhb-mcp unified MCP server."""
import asyncio
from fastmcp import FastMCP
from common_mcp import run_server

# Create the unified MCP server
mcp = FastMCP("gkzhb-mcp")


def main():
    """Main function to run the unified MCP server."""
    # Import and register tools from each subpackage
    from crawl4ai_mcp.register import register_tools as crawl4ai_register_tools
    from searxng_mcp.register import register_tools as searxng_register_tools
    from agent_skills_mcp_gkzhb.register import (
        initialize_skills,
        register_tools as skills_register_tools,
    )

    # Initialize agent-skills first (requires async initialization)
    print("Initializing agent skills...")
    found_skills = asyncio.run(initialize_skills())
    print(f"Loaded {len(found_skills)} skills")

    # Register all tools from subpackages
    crawl4ai_register_tools(mcp)
    searxng_register_tools(mcp)
    skills_register_tools(mcp, found_skills)

    # Run server
    run_server(mcp, default_port=8000)


if __name__ == "__main__":
    main()