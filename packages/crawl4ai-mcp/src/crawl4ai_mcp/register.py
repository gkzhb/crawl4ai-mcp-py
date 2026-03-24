"""Tool registration for crawl4ai-mcp."""

import os
from typing import Any, Dict
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
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

# Chrome CDP endpoint 配置
chrome_cdp_endpoint = os.getenv("CHROME_CDP_ENDPOINT")

# 构建BrowserConfig
config_kwargs: Dict[str, Any] = {"enable_stealth": False}

# 如果设置了 Chrome CDP WebSocket endpoint，添加到配置中
if chrome_cdp_endpoint:
    config_kwargs["cdp_url"] = chrome_cdp_endpoint
    config_kwargs["cdp_cleanup_on_close"] = True

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


def _safe_join_content(content: Any, field_name: str) -> str:
    """Safely join content, handling None and non-iterable values."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if hasattr(content, "__iter__"):
        try:
            return "".join(content)
        except Exception as e:
            raise ToolError(f"Failed to join {field_name}: {str(e)}")
    raise ToolError(
        f"Invalid {field_name} type: {type(content).__name__}, expected str or iterable"
    )


def register_tools(mcp: FastMCP) -> None:
    """Register all crawl4ai tools to the MCP server."""

    @mcp.tool()
    async def web_to_md(
        url: str, ctx: Context, with_links: bool = False
    ) -> Dict[str, Any]:
        """Convert web page to markdown content. Optionally extract links."""
        try:
            async with AsyncWebCrawler(config=config, verbose=False) as crawler:
                result = await crawler.arun(url=url, config=crawler_config)
                if isinstance(result, CrawlResultContainer):
                    await ctx.info(f"Web crawler result for URL: {url}")
                    markdown_content = getattr(result, "markdown", None)
                    await ctx.debug(
                        f"markdown_content fit content: {str(markdown_content.fit_markdown)[:500]}, raw content: {repr(markdown_content.raw_markdown)[:500]} str:{str(markdown_content)}"
                    )
                    response: Dict[str, Any] = {
                        "content": str(
                            markdown_content.fit_markdown
                            or markdown_content.raw_markdown
                        )
                    }
                    if with_links and hasattr(result, "links"):
                        response["internal_links"] = filter_links(
                            result.links.get("internal", [])
                        )
                        response["external_links"] = filter_links(
                            result.links.get("external", [])
                        )
                    return response
                error_msg = f"Invalid result type: {type(result)}"
                await ctx.error(
                    f"Web crawler result error for URL '{url}': {error_msg}"
                )
                raise ToolError(f"Web crawler result error: {error_msg}")
        except ToolError:
            raise
        except Exception as e:
            await ctx.error(f"Web crawler failed for URL '{url}': {str(e)}")
            raise ToolError(f"Web crawler failed: {str(e)}")

    @mcp.tool()
    async def web_to_html(
        url: str,
        ctx: Context,
        with_links: bool = False,
    ) -> Dict[str, Any]:
        """Convert web page to html content. Optionally extract links."""
        try:
            async with AsyncWebCrawler(config=config, verbose=False) as crawler:
                result = await crawler.arun(url=url, config=crawler_config)
                if isinstance(result, CrawlResultContainer):
                    await ctx.info(f"Web crawler result for URL: {url}")
                    html_content = getattr(result, "cleaned_html", None)
                    await ctx.debug(
                        f"cleaned_html type: {type(html_content)}, value: {repr(html_content)[:500]}"
                    )
                    response: Dict[str, Any] = {
                        "content": _safe_join_content(html_content, "cleaned_html")
                    }
                    if with_links and hasattr(result, "links"):
                        response["internal_links"] = filter_links(
                            result.links.get("internal", [])
                        )
                        response["external_links"] = filter_links(
                            result.links.get("external", [])
                        )
                    return response
                error_msg = f"Invalid result type: {type(result)}"
                await ctx.error(
                    f"Web crawler result error for URL '{url}': {error_msg}"
                )
                raise ToolError(f"Web crawler result error: {error_msg}")
        except ToolError:
            raise
        except Exception as e:
            await ctx.error(f"Web crawler failed for URL '{url}': {str(e)}")
            raise ToolError(f"Web crawler failed: {str(e)}")
