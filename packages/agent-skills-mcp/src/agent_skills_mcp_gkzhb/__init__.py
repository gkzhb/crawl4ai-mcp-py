"""agent-skills-mcp - MCP server for managing and executing agent skills."""

__version__ = "0.1.0"
__author__ = "gkzhb"
__email__ = "gkzhb98@gmail.com"

from .register import (
    initialize_skills,
    get_skills,
    register_tools,
    Skill,
    SkillFrontmatter,
)

__all__ = [
    "initialize_skills",
    "get_skills",
    "register_tools",
    "Skill",
    "SkillFrontmatter",
]