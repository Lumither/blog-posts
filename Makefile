MAKEFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
MAKEFILE_DIR := $(dir $(MAKEFILE_PATH))

.PHONY: all
all: build_dist

.PHONY: setup
setup:
	uv sync --project workflow

.PHONY: build-dist
build_dist: setup
	uv run --project workflow -- python workflow/main.py

.PHONY: clean
clean:
	rm -rf dist