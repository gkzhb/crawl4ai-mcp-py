"""Tool registration for searxng-mcp."""

import os
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from httpx import AsyncClient
from pydantic import BaseModel


class SearchResult(BaseModel):
    url: str
    title: str
    content: str


class InfoboxUrl(BaseModel):
    title: str
    url: str


class Infobox(BaseModel):
    infobox: str
    id: str
    content: str
    urls: list[InfoboxUrl]


class Response(BaseModel):
    query: str
    number_of_results: int
    results: list[SearchResult]
    infoboxes: list[Infobox]


client = AsyncClient(base_url=str(os.getenv("SEARXNG_URL", "http://localhost:8080")))


# reference to https://github.com/SecretiveShell/MCP-searxng for implementation
async def search(query: str, limit: int = 5) -> str:
    params: dict[str, str] = {"q": query, "format": "json"}

    response = await client.get("/search", params=params)
    response.raise_for_status()

    data = Response.model_validate_json(response.text)

    text = ""

    for index, infobox in enumerate(data.infoboxes):
        text += f"Infobox: {infobox.infobox}\n"
        text += f"ID: {infobox.id}\n"
        text += f"Content: <content>\n{infobox.content}\n</content>\n"
        text += "\n\n"

    text += "\n---\n\n"

    if len(data.results) == 0:
        text += "No results found\n"

    for index, result in enumerate(data.results[0:limit]):
        text += f"Title: {result.title}\n"
        text += f"URL: {result.url}\n"
        text += f"Content: <content>\n{result.content}\n</content>\n"
        text += "\n\n"

    return str(text)


def register_tools(mcp: FastMCP) -> None:
    """Register all searxng tools to the MCP server."""

    @mcp.tool()
    async def search_web(query: str, ctx: Context, limit: int = 3) -> str:
        """Search the web using SearXNG and return formatted results."""
        try:
            result = await search(query, limit)
            await ctx.info(f"Search completed for query: {query}")
            return result
        except Exception as e:
            import traceback

            error_detail = f"{type(e).__name__}: {str(e) or '<no message>'}"
            await ctx.error(f"Search failed: {error_detail}")
            await ctx.error(f"Traceback:\n{traceback.format_exc()}")
            raise ToolError(f"Search failed: {error_detail}")
