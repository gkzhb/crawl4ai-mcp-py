"""Main entry point for agent-skills-mcp."""
import asyncio
from fastmcp import FastMCP
from common_mcp import run_server
from agent_skills_mcp_gkzhb.register import (
    initialize_skills,
    register_tools,
)

mcp = FastMCP("agent-skills-mcp")


def main():
    """Run the MCP server with skills initialization."""
    # Initialize skills first
    print("Initializing skills...")
    found_skills = asyncio.run(initialize_skills())
    print(f"Loaded {len(found_skills)} skills")

    # Register tools to MCP
    register_tools(mcp, found_skills)

    # Run server
    run_server(mcp, default_port=8001)


if __name__ == "__main__":
    main()