# default command
_default:
    @just --list

set dotenv-filename := ".env.http"
set dotenv-load := true

dev-http:
    uv run src/agent_skills_mcp_gkzhb/main.py

