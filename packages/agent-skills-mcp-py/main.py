import os
import glob
import yaml
from pathlib import Path
from typing import Optional, List, Dict, Any
from fastmcp import FastMCP, Context
from pydantic import BaseModel, field_validator

mcp = FastMCP("agent-skills-mcp")

# global path to search skills, comma separated path list
global_skills_path = os.getenv("GLOBAL_SKILLS_PATH", "~/.skills/")
# project-level path to search skills, comma separated path list
project_skills_path = os.getenv("PROJECT_SKILLS_PATH", ".skills/")


def parse_skills_paths(env_var: str, default_path: str) -> List[str]:
    """Parse comma-separated paths from environment variable"""
    paths_str = os.getenv(env_var, default_path)
    if not paths_str:
        return []

    # Split by comma and expand user paths
    paths = []
    for path in paths_str.split(","):
        path = path.strip()
        if path:
            # Expand ~ to home directory
            expanded_path = os.path.expanduser(path)
            # Convert to absolute path if relative
            if not os.path.isabs(expanded_path):
                expanded_path = os.path.join(os.getcwd(), expanded_path)
            paths.append(expanded_path)

    return paths


class SkillFrontmatter(BaseModel):
    name: str
    description: str
    license: Optional[str] = None
    allowed_tools: Optional[List[str]] = None
    metadata: Optional[Dict[str, str]] = None

    @field_validator("name")
    def validate_name(cls, v):
        if not v or not v.replace("-", "").isalnum() or not v.islower():
            raise ValueError("Name must be lowercase alphanumeric with hyphens")
        return v

    @field_validator("description")
    def validate_description(cls, v):
        if len(v) < 10:
            raise ValueError(
                "Description must be at least 10 characters for discoverability"
            )
        return v


class Skill(BaseModel):
    name: str
    full_path: str
    tool_name: str
    description: str
    allowed_tools: Optional[List[str]] = None
    metadata: Optional[Dict[str, str]] = None
    license: Optional[str] = None
    content: str
    path: str
    location: str


def generate_tool_name(skill_path: str, base_dir: str) -> str:
    """Generate tool name from skill path"""
    rel_path = os.path.relpath(skill_path, base_dir)
    dir_path = os.path.dirname(rel_path)
    components = [comp for comp in dir_path.split(os.sep) if comp != "."]
    return "skills_" + "_".join(components).replace("-", "_")


async def parse_skill(skill_path: str, base_dir: str, cwd: str) -> Optional[Skill]:
    """Parse a SKILL.md file and return structured skill data"""
    try:
        # Read file
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Split frontmatter and content
        if not content.startswith("---"):
            print(f"❌ Invalid frontmatter in {skill_path}: Missing YAML frontmatter")
            return None

        parts = content.split("---", 2)
        if len(parts) < 3:
            print(
                f"❌ Invalid frontmatter in {skill_path}: Incomplete YAML frontmatter"
            )
            return None

        frontmatter_str = parts[1].strip()
        markdown_content = parts[2].strip()

        # Parse YAML frontmatter
        try:
            frontmatter_data = yaml.safe_load(frontmatter_str)
            frontmatter = SkillFrontmatter(**frontmatter_data)
        except yaml.YAMLError as e:
            print(f"❌ Invalid YAML in {skill_path}: {e}")
            return None
        except ValueError as e:
            print(f"❌ Invalid frontmatter in {skill_path}: {e}")
            return None

        # Validate name matches directory
        skill_dir = os.path.basename(os.path.dirname(skill_path))
        if frontmatter.name != skill_dir:
            print(f"❌ Name mismatch in {skill_path}:")
            print(f'   Frontmatter name: "{frontmatter.name}"')
            print(f'   Directory name: "{skill_dir}"')
            print(
                f"   Fix: Update the 'name' field in SKILL.md to match the directory name"
            )
            return None

        # Generate tool name from path
        tool_name = generate_tool_name(skill_path, base_dir)

        return Skill(
            name=frontmatter.name,
            full_path=os.path.dirname(skill_path),
            tool_name=tool_name,
            description=frontmatter.description,
            allowed_tools=frontmatter.allowed_tools,
            metadata=frontmatter.metadata,
            license=frontmatter.license,
            content=markdown_content,
            path=skill_path,
            location="project" if skill_path.startswith(cwd) else "global",
        )
    except Exception as e:
        print(f"❌ Error parsing skill {skill_path}: {e}")
        return None


async def discover_skills(base_paths: List[str]) -> List[Skill]:
    """Discover all SKILL.md files in the specified base paths"""
    skills = []
    cwd = base_paths[0] if base_paths else ""

    for base_path in base_paths:
        try:
            # Check if directory exists
            if not os.path.exists(base_path):
                continue

            # Find all SKILL.md files recursively
            skill_count = 0
            for skill_path in glob.glob(
                os.path.join(base_path, "**/SKILL.md"), recursive=True
            ):
                skill = await parse_skill(skill_path, base_path, cwd)
                if skill:
                    skills.append(skill)
                    skill_count += 1

            print(f"Found {skill_count} skills in {base_path}")
        except Exception as e:
            print(f"⚠️  Could not scan skills directory: {base_path}")
            print(f"   Error: {e}")

    # Detect duplicate tool names
    tool_names = set()
    duplicates = []

    for skill in skills:
        if skill.tool_name in tool_names:
            duplicates.append(skill.tool_name)
        tool_names.add(skill.tool_name)

    if duplicates:
        print(f"⚠️  Duplicate tool names detected: {duplicates}")

    return skills


def get_skill_xml(skill: Skill) -> str:
    """Generate XML representation of a skill"""
    return f"""<skill>
<name>
{skill.name}
</name>
<description>
{skill.description}
</description>
<location>
{skill.location}
</location>
</skill>"""


def construct_tool_desc(skills: List[Skill]) -> str:
    """Construct tool description with available skills"""
    return f"""Execute a skill within the main conversation

<skills_instructions>
When users ask you to perform tasks, check if any of the available skills below can help complete the task more effectively. Skills provide specialized capabilities and domain knowledge.

How to use skills:
- **Invoke skills using this tool `skills` with the skill name only (no arguments)**
- When you invoke a skill, you will see <command-message>The "{{name}}" skill is loading</command-message>
- The skill's prompt will expand and provide detailed instructions on how to complete the task
- Examples:
  - `command: "pdf"` - invoke the pdf skill
  - `command: "xlsx"` - invoke the xlsx skill
  - `command: "ms-office-suite:pdf"` - invoke using fully qualified name

Important:
- Only use skills listed in <available_skills> below
- Do not invoke a skill that is already running
- Do not use this tool for built-in CLI commands (like /help, /clear, etc.)
</skills_instructions>

<available_skills>
{chr(10).join(get_skill_xml(skill) for skill in skills)}
</available_skills>"""


# Global skills cache
_skills_cache: Optional[List[Skill]] = None


async def initialize_skills() -> List[Skill]:
    """Initialize skills cache during MCP startup"""
    global _skills_cache

    # Parse global and project skills paths from environment variables
    global_paths = parse_skills_paths("GLOBAL_SKILLS_PATH", "~/.skills/")
    project_paths = parse_skills_paths("PROJECT_SKILLS_PATH", ".skills/")

    # Combine all paths, with project paths taking precedence for location detection
    all_paths = global_paths + project_paths

    _skills_cache = await discover_skills(all_paths)
    return _skills_cache


def get_skills() -> List[Skill]:
    """Get cached skills (must be initialized first)"""
    if _skills_cache is None:
        raise RuntimeError("Skills not initialized. Call initialize_skills() first.")
    return _skills_cache


@mcp.tool()
async def skills(command: str, ctx: Context) -> str:
    """Execute a skill within the main conversation"""
    skills_list = get_skills()
    skill = next((s for s in skills_list if s.name == command), None)

    if not skill:
        available_names = [s.name for s in skills_list]
        return f'Skill "{command}" not found. Available skills: {", ".join(available_names)}'

    await ctx.info(f"Skill '{command}' executed")

    return f"""<command-message>The "{command}" skill is running</command-message>
<command-name>{command}</command-name>

# {command} Skill information

Base directory for this skill: {skill.full_path}

Skill Content:

{skill.content}"""


async def main_async():
    """Async main function to initialize skills"""
    # Initialize skills cache during startup
    print("Initializing skills...")
    skills = await initialize_skills()
    print(f"✅ Loaded {len(skills)} skills")


def main():
    """Main function to run the MCP server"""
    # Initialize skills cache during startup
    import asyncio

    asyncio.run(main_async())

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
