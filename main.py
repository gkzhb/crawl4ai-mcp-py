import os
from fastmcp import FastMCP, Context
from crawl4ai.models import CrawlResultContainer
from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig

mcp = FastMCP("crawl4ai-mcp")

config = BrowserConfig(
    enable_stealth=True,
)
crawler_config = CrawlerRunConfig(
    cache_mode=CacheMode.BYPASS,
    magic=True,
    simulate_user=True,
    override_navigator=True,
)

@mcp.tool()
async def web_to_md(url: str, ctx: Context) -> str:
    """Convert web page to markdown content."""
    async with AsyncWebCrawler(config=config, verbose=False) as crawler:
        result = await crawler.arun(url=url, config=crawler_config)
        if isinstance(result, CrawlResultContainer):
            await ctx.info(f"Web crawler result: {result.markdown}")
            return ''.join(result.markdown)
        await ctx.error(f"Web crawler result error: invalid result type {result}")
        return "Crawle web failed."


@mcp.tool()
async def web_to_html(url: str, ctx: Context) -> str:
    """Convert web page to html content."""
    async with AsyncWebCrawler(config=config, verbose=False) as crawler:

        result = await crawler.arun(url=url, config=crawler_config)
        if isinstance(result, CrawlResultContainer):
            await ctx.info(f"Web crawler result: {result.cleaned_html}")
            return ''.join(result.cleaned_html)
        await ctx.error(f"Web crawler result error: invalid result type {result}")
        return "Crawle web failed."


if __name__ == "__main__":
    mcp_type = os.getenv("MCP_TYPE", "stdio").lower()
    host = os.getenv("MCP_HOST", "127.0.0.1")
    port_str = os.getenv("MCP_PORT", "8000")
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
