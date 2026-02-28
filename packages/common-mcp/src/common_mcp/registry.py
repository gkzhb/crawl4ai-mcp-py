"""Common MCP utilities - Server running and common functionality."""

import os
from typing import Any
from fastmcp import FastMCP
from dotenv import load_dotenv
from fastmcp.server.middleware.logging import StructuredLoggingMiddleware

try:
    from fastmcp.server.auth.providers.jwt import StaticTokenVerifier

    HAS_AUTH = True
except ImportError:
    HAS_AUTH = False


def create_auth_verifier_from_env(
    env_var: str = "MCP_AUTH",
    default_scopes: list[str] | None = None,
) -> Any | None:
    """Create auth verifier from environment variable.

    Args:
        env_var: Environment variable name containing comma-separated tokens.
                 Default is "MCP_AUTH".
        default_scopes: Default scopes to assign to each token.
                        Default is ["read:data", "write:data"].

    Returns:
        StaticTokenVerifier instance if tokens are found, None otherwise.

    Example:
        MCP_AUTH="token1,token2,token3"
    """
    if not HAS_AUTH:
        return None

    auth_env = os.getenv(env_var)
    if not auth_env:
        return None

    # Split by comma and strip whitespace
    tokens = [token.strip() for token in auth_env.split(",") if token.strip()]

    if not tokens:
        return None

    # Default scopes
    if default_scopes is None:
        default_scopes = ["read:data", "write:data"]

    # Create token dictionary with default claims
    token_dict: dict[str, dict[str, Any]] = {
        token: {
            "client_id": f"token-{idx}",
            "scopes": default_scopes,
        }
        for idx, token in enumerate(tokens)
    }

    return StaticTokenVerifier(
        tokens=token_dict,
        required_scopes=["read:data"],
    )


def load_dotenv_file() -> None:
    """Load environment variables from dotenv file.

    This function should be called at the beginning of main.py files
    to ensure environment variables are loaded before any other code runs.
    """
    dotenv_file = os.getenv("DOTENV_FILE")
    if dotenv_file:
        load_dotenv(dotenv_file, override=True)


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

    # Detect environment
    env = os.getenv("ENV", "development").lower()
    is_production = env == "production"

    # Add production middleware for structured logging
    if is_production:
        mcp.add_middleware(StructuredLoggingMiddleware())

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
