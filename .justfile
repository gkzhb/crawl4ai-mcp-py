# default command
_default:
    @just --list

alias b := build
alias ba := build-all
alias i := install

# install pypi dependencies
install:
    uv sync --all-packages

# build all packages
build-all:
    uv build --all-packages

# build package
build package:
    uv build --package "{{package}}"
