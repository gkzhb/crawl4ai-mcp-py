"""Main entry point for agent-skills-mcp."""

import asyncio
from fastmcp import FastMCP
from common_mcp import load_dotenv_file, run_server, create_auth_verifier_from_env
from agent_skills_mcp_gkzhb.register import (
    initialize_skills,
    register_tools,
)

# Load environment variables from dotenv file at startup
load_dotenv_file()

# Create auth verifier from MCP_AUTH environment variable
auth_verifier = create_auth_verifier_from_env()

# Create MCP server with auth if available
mcp = FastMCP("agent-skills-mcp", auth=auth_verifier)


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
