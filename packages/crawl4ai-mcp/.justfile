# default command
_default:
    @just --list

set dotenv-filename := ".env.http"
set dotenv-load := true

dev-http:
    uv run src/crawl4ai_mcp/main.py


