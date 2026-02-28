# default command
_default:
    @just --list

set dotenv-filename := ".env.http"
set dotenv-load := true

dev-http:
    uv run src/gkzhb_mcp/main.py

# start production server
start:
    DOTENV_FILE=.env.prod uv run src/gkzhb_mcp/main.py
