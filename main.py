import os
from fastmcp import FastMCP, Context
from crawl4ai.models import CrawlResultContainer
from crawl4ai import AsyncWebCrawler

mcp = FastMCP("crawl4ai-mcp")


@mcp.tool()
async def web_to_md(url: str, ctx: Context) -> str:
    """Convert web page to markdown content."""
    async with AsyncWebCrawler(verbose=False) as crawler:
        result = await crawler.arun(url=url)
        if isinstance(result, CrawlResultContainer):
            await ctx.info(f"Web crawler result: {result.markdown}")
            return ''.join(result.markdown)
        await ctx.error(f"Web crawler result error: invalid result type {result}")
        return "Crawle web failed."


@mcp.tool()
async def web_to_html(url: str, ctx: Context) -> str:
    """Convert web page to html content."""
    async with AsyncWebCrawler(verbose=False) as crawler:
        result = await crawler.arun(url=url)
        if isinstance(result, CrawlResultContainer):
            await ctx.info(f"Web crawler result: {result.cleaned_html}")
            return ''.join(result.cleaned_html)
        await ctx.error(f"Web crawler result error: invalid result type {result}")
        return "Crawle web failed."


if __name__ == "__main__":
    mcp_type = os.getenv("MCP_TYPE", "stdio").lower()
    host = os.getenv("MCP_HOST", "127.0.0.1").lower()

    if mcp_type == "sse":
        mcp.run(transport="sse", host=host)
    elif mcp_type == "streamable-http":
        mcp.run(transport="streamable-http", host=host)
    else:
        mcp.run(transport="stdio")
