"""Common MCP utilities - Server running and common functionality."""
import os
from fastmcp import FastMCP


def run_server(
    mcp: FastMCP,
    default_port: int = 8000,
    default_host: str = "127.0.0.1",
) -> None:
    """Run the MCP server with configuration from environment variables.

    Args:
        mcp: FastMCP instance to run
        default_port: Default port for SSE/HTTP transports
        default_host: Default host for SSE/HTTP transports
    """
    mcp_type = os.getenv("MCP_TYPE", "stdio").lower()
    host = os.getenv("MCP_HOST", default_host)
    port_str = os.getenv("MCP_PORT", str(default_port))

    try:
        port = int(port_str)
        if not (0 <= port <= 65535):
            raise ValueError(f"Port {port} is out of valid range (0-65535)")
    except ValueError as e:
        raise ValueError(f"Invalid port number: {port_str}") from e

    if mcp_type == "sse":
        mcp.run(transport="sse", host=host, port=port)
    elif mcp_type == "http":
        mcp.run(transport="http", host=host, port=port)
    else:
        mcp.run(transport="stdio")