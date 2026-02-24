"""searxng-mcp - MCP server for web search using SearXNG."""

__version__ = "0.1.0"
__author__ = "gkzhb"
__email__ = "gkzhb98@gmail.com"

from .register import register_tools

__all__ = ["register_tools"]