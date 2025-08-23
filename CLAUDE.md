# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is a Python MCP (Model Context Protocol) server that provides web crawling capabilities using the crawl4ai library. It exposes two main tools for converting web pages to markdown or HTML format.

## Architecture
- **FastMCP**: Uses fastmcp>=2.11.3 as the MCP server framework
- **crawl4ai**: Uses crawl4ai>=0.7.4 for web crawling and content extraction
- **Transport**: Supports stdio, SSE, and streamable-http transports via environment variables

## Key Files
- `main.py`: Main MCP server implementation with web crawling tools
- `pyproject.toml`: Project configuration with dependencies

## Development Commands
- **Install dependencies**: `pip install -e .` or `uv sync`
- **Run server**: `python main.py` (stdio mode by default)
- **Run with SSE**: `MCP_TYPE=sse python main.py`
- **Run with HTTP**: `MCP_TYPE=http python main.py`
- **Custom host**: `MCP_HOST=0.0.0.0 MCP_TYPE=sse python main.py`

## Environment Variables
- `MCP_TYPE`: Transport type (stdio|sse|http), defaults to "stdio"
- `MCP_HOST`: Host address for SSE/HTTP modes, defaults to "127.0.0.1"