# default command
_default:
    @just --list

# load UV_PUBLISH_TOKEN env to publish package
set dotenv-filename := ".env"
set dotenv-load := true

alias b := build
alias ba := build-all
alias i := install
alias p := publish

# install pypi dependencies
install:
    uv sync --all-packages

# build all packages
build-all:
    uv build --all-packages

# build package
build package:
    uv build --package "{{package}}"

# build package
publish package:
    uv publish --package "{{package}}"
