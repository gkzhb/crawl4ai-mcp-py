"""Main entry point for gkzhb-mcp unified MCP server."""

import asyncio
import os
from fastmcp import FastMCP
from common_mcp import load_dotenv_file, run_server

# Load environment variables from dotenv file at startup
load_dotenv_file()

# Configure logging level based on environment
log_level = os.getenv(
    "LOG_LEVEL",
    "INFO" if os.getenv("ENV", "development").lower() == "production" else "DEBUG",
)

# Create the unified MCP server with production settings
is_production = os.getenv("ENV", "development").lower() == "production"
mcp = FastMCP(
    "gkzhb-mcp",
    debug=not is_production,  # 生产环境关闭 debug
    log_level=log_level.lower(),
)


def get_enabled_tools():
    """Parse MCP_TOOL_LIST environment variable to determine which tools to enable."""
    tool_list_env = os.environ.get("MCP_TOOL_LIST", "")
    if not tool_list_env:
        # Default: enable all tools
        return {"skills", "crawl4ai", "searxng"}

    # Parse comma-separated list
    enabled = {
        tool.strip().lower() for tool in tool_list_env.split(",") if tool.strip()
    }
    valid_tools = {"skills", "crawl4ai", "searxng"}
    invalid_tools = enabled - valid_tools

    if invalid_tools:
        print(
            f"Warning: Invalid tools in MCP_TOOL_LIST: {invalid_tools}. Valid options: {valid_tools}"
        )

    return enabled & valid_tools  # Only keep valid tools


def main():
    """Main function to run the unified MCP server."""
    # Determine which tools to enable based on environment variable
    enabled_tools = get_enabled_tools()
    print(f"Enabled tools: {enabled_tools}")

    # Import and register tools from each subpackage based on enabled tools
    if "crawl4ai" in enabled_tools:
        from crawl4ai_mcp.register import register_tools as crawl4ai_register_tools

    if "searxng" in enabled_tools:
        from searxng_mcp.register import register_tools as searxng_register_tools

    if "skills" in enabled_tools:
        from agent_skills_mcp_gkzhb.register import (
            initialize_skills,
            register_tools as skills_register_tools,
        )

    # Initialize and register enabled tools
    found_skills = []
    if "skills" in enabled_tools:
        print("Initializing agent skills...")
        found_skills = asyncio.run(initialize_skills())
        print(f"Loaded {len(found_skills)} skills")
        skills_register_tools(mcp, found_skills)

    if "crawl4ai" in enabled_tools:
        crawl4ai_register_tools(mcp)

    if "searxng" in enabled_tools:
        searxng_register_tools(mcp)

    # Run server
    run_server(mcp, default_port=8000)


if __name__ == "__main__":
    main()
