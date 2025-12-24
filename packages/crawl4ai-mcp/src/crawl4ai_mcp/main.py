import os
from typing import Any, Dict, Optional, Union
from fastmcp import FastMCP, Context
from crawl4ai.models import CrawlResultContainer
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    ProxyConfig,
)

mcp = FastMCP("crawl4ai-mcp")

# 代理配置
proxy_server = os.getenv("CRAWL4AI_PROXY_SERVER")
proxy_username = os.getenv("CRAWL4AI_PROXY_USERNAME")
proxy_password = os.getenv("CRAWL4AI_PROXY_PASSWORD")

# 构建BrowserConfig
config_kwargs: Dict[str, Any] = {"enable_stealth": False}

# 如果设置了代理服务器，添加到配置中
if proxy_server:
    proxy_config = ProxyConfig(server=proxy_server)
    if proxy_username and proxy_password:
        proxy_config.username = proxy_username
        proxy_config.password = proxy_password
    config_kwargs["proxy_config"] = proxy_config

config = BrowserConfig(**config_kwargs)

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
            return "".join(result.markdown)
        await ctx.error(f"Web crawler result error: invalid result type {result}")
        return f"Crawle web failed: {getattr(result, 'error_message', 'Unknown error')}"


@mcp.tool()
async def web_to_html(url: str, ctx: Context) -> str:
    """Convert web page to html content."""
    async with AsyncWebCrawler(config=config, verbose=False) as crawler:
        result = await crawler.arun(url=url, config=crawler_config)
        if isinstance(result, CrawlResultContainer):
            await ctx.info(f"Web crawler result: {result.cleaned_html}")
            return "".join(result.cleaned_html)
        await ctx.error(f"Web crawler result error: invalid result type {result}")
        return f"Crawle web failed: {getattr(result, 'error_message', 'Unknown error')}"


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
