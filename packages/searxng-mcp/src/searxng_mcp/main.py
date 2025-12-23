import os
from fastmcp import FastMCP, Context
from httpx import AsyncClient
from pydantic import BaseModel

mcp = FastMCP("searxng-mcp")


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
    # img_src: Optional[str] = None
    urls: list[InfoboxUrl]
    # attributes: list[str]
    # engine: str
    # engines: list[str]


class Response(BaseModel):
    query: str
    number_of_results: int
    results: list[SearchResult]
    # answers: list[str]
    # corrections: list[str]
    infoboxes: list[Infobox]
    # suggestions: list[str]
    # unresponsive_engines: list[str]


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


@mcp.tool()
async def search_web(query: str, ctx: Context, limit: int = 3) -> str:
    """Search the web using SearXNG and return formatted results."""
    try:
        result = await search(query, limit)
        await ctx.info(f"Search completed for query: {query}")
        return result
    except Exception as e:
        await ctx.error(f"Search failed: {str(e)}")
        return f"Search failed: {str(e)}"


def main():
    mcp_type = os.getenv("MCP_TYPE", "stdio").lower()
    host = os.getenv("MCP_HOST", "127.0.0.1")
    port_str = os.getenv("MCP_PORT", "8001")
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


if __name__ == "__main__":
    main()
