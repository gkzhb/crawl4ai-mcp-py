"""Agent Skills MCP Server - A Model Context Protocol server for managing and executing agent skills."""

__version__ = "0.1.0"
__author__ = "gkzhb"
__email__ = "gkzhb98@gmail.com"

from .main import (
    mcp,
    main,
    main_async,
    initialize_skills,
    get_skills,
    Skill,
    SkillFrontmatter,
)

__all__ = [
    "mcp",
    "main",
    "main_async",
    "initialize_skills",
    "get_skills",
    "Skill",
    "SkillFrontmatter",
]
