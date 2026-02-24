"""Configuration management for gkzhb-mcp."""
import os
from typing import Optional


class ServerConfig:
    """MCP Server configuration."""

    def __init__(self):
        self.mcp_type: str = os.getenv("MCP_TYPE", "stdio").lower()
        self.host: str = os.getenv("MCP_HOST", "127.0.0.1")
        self.port: int = int(os.getenv("MCP_PORT", "8000"))

    @property
    def transport(self) -> str:
        """Map MCP_TYPE to transport name."""
        if self.mcp_type == "sse":
            return "sse"
        elif self.mcp_type == "http":
            return "http"
        else:
            return "stdio"

    def validate(self) -> None:
        """Validate configuration values."""
        if not (0 <= self.port <= 65535):
            raise ValueError(f"Port {self.port} is out of valid range (0-65535)")

        if self.mcp_type not in ("stdio", "sse", "http"):
            raise ValueError(f"Invalid MCP_TYPE: {self.mcp_type}. Must be stdio, sse, or http")


def get_config() -> ServerConfig:
    """Get server configuration from environment variables."""
    config = ServerConfig()
    config.validate()
    return config