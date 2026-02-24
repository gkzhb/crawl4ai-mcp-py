"""Tool registration for crawl4ai-mcp."""
import os
from typing import Any, Dict
from fastmcp import FastMCP, Context
from crawl4ai.models import CrawlResultContainer
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    ProxyConfig,
)

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


def filter_link(link: Dict[str, Any]) -> Dict[str, Any]:
    """Filter link to keep only essential fields."""
    return {
        "href": link.get("href", ""),
        "text": link.get("text", ""),
        "title": link.get("title", ""),
        "base_domain": link.get("base_domain", ""),
    }


def filter_links(links: list) -> list:
    """Filter list of links to keep only essential fields."""
    return [filter_link(link) for link in links]


def register_tools(mcp: FastMCP) -> None:
    """Register all crawl4ai tools to the MCP server."""

    @mcp.tool()
    async def web_to_md(url: str, ctx: Context, with_links: bool = False) -> Dict[str, Any]:
        """Convert web page to markdown content. Optionally extract links."""
        async with AsyncWebCrawler(config=config, verbose=False) as crawler:
            result = await crawler.arun(url=url, config=crawler_config)
            if isinstance(result, CrawlResultContainer):
                if ctx:
                    await ctx.info(f"Web crawler result: {result.markdown}")
                response: Dict[str, Any] = {"content": "".join(result.markdown)}
                if with_links and hasattr(result, "links"):
                    response["internal_links"] = filter_links(
                        result.links.get("internal", [])
                    )
                    response["external_links"] = filter_links(
                        result.links.get("external", [])
                    )
                return response
            if ctx:
                await ctx.error(f"Web crawler result error: invalid result type {result}")
            return {
                "content": f"Crawle web failed: {getattr(result, 'error_message', 'Unknown error')}",
                "internal_links": [],
                "external_links": [],
            }

    @mcp.tool()
    async def web_to_html(
        url: str,
        ctx: Context,
        with_links: bool = False,
    ) -> Dict[str, Any]:
        """Convert web page to html content. Optionally extract links."""
        async with AsyncWebCrawler(config=config, verbose=False) as crawler:
            result = await crawler.arun(url=url, config=crawler_config)
            if isinstance(result, CrawlResultContainer):
                if ctx:
                    await ctx.info(f"Web crawler result: {result.cleaned_html}")
                response: Dict[str, Any] = {"content": "".join(result.cleaned_html)}
                if with_links and hasattr(result, "links"):
                    response["internal_links"] = filter_links(
                        result.links.get("internal", [])
                    )
                    response["external_links"] = filter_links(
                        result.links.get("external", [])
                    )
                return response
            if ctx:
                await ctx.error(f"Web crawler result error: invalid result type {result}")
            return {
                "content": f"Crawle web failed: {getattr(result, 'error_message', 'Unknown error')}",
                "internal_links": [],
                "external_links": [],
            }