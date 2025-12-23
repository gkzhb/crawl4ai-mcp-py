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

Configure skill discovery paths using environment variables:

- `GLOBAL_SKILLS_PATH`: Comma-separated list of global skill directories (default: `~/.skills/`)
- `PROJECT_SKILLS_PATH`: Comma-separated list of project-level skill directories (default: `.skills/`)

Example:
```bash
export GLOBAL_SKILLS_PATH="~/.skills/,~/.config/opencode/skills"
export PROJECT_SKILLS_PATH=".skills/,./.opencode/skills"
```

### Default Paths

If no custom paths are configured, the server will search in these default locations:
- `./.skills` (project-level)
- `~/.skills` (global)

## Usage

1. Create skill directories in your configured paths
2. Add `SKILL.md` files with YAML frontmatter to define your skills
3. Start the MCP server: `uv run main.py`

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
