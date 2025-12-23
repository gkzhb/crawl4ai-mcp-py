# Agent Skills MCP Server

MCP Server for [Agent Skills](https://agentskills.io/home).

## Features

- **Dynamic Skill Discovery**: Automatically discovers and loads skills from configurable directories
- **Environment-based Configuration**: Configure skill search paths via environment variables
- **Global and Project-level Skills**: Support for both system-wide and project-specific skills
- **YAML Frontmatter Validation**: Validates skill metadata and structure
- **Duplicate Detection**: Prevents duplicate tool names across different skill sources

## Configuration

### Environment Variables

Configure skill discovery paths and tool naming using environment variables:

- `GLOBAL_SKILLS_PATH`: Comma-separated list of global skill directories (default: `~/.skills/`)
- `PROJECT_SKILLS_PATH`: Comma-separated list of project-level skill directories (default: `.skills/`)
- `MCP_SERVER_NAME_PREFIX`: Optional prefix to prepend to tool names in the tool description prompt (e.g., with this mcp server configured as `skills` you may prefix "skills_", the tool will be referenced as "skills_skills" in tool description)

Example:
```bash
export GLOBAL_SKILLS_PATH="~/.skills/,~/.config/opencode/skills"
export PROJECT_SKILLS_PATH=".skills/,./.opencode/skills"
export MCP_SERVER_NAME_PREFIX="<this-mcp-name>_"
```

### Default Paths

If no custom paths are configured, the server will search in these default locations:
- `./.skills` (project-level)
- `~/.skills` (global)

## Usage

1. Create skill directories in your configured paths and add skills
2. [Optional] Set environment variables, e.g. `GLOBAL_SKILLS_PATH`, `MCP_SERVER_NAME_PREFIX`, `MCP_TYPE`, `MCP_PORT`
3. Start the MCP server: `uvx --from agent-skills-mcp-gkzhb agent-skills`

## Skill Format

Skills are defined in `SKILL.md` files with YAML frontmatter:

```yaml
---
name: my-skill
description: Description of what this skill does (minimum 10 characters)
license: MIT
allowed_tools: ["tool1", "tool2"]
metadata:
  category: "utility"
---

# Skill Content

Your skill instructions and documentation go here.
```

## Development

Copy `.env.example` to `.env` and customize the configuration:
```bash
cp .env.example .env
```

Run the development server:
```bash
uv run main.py
```
