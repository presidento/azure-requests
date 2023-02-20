PYTHON_VERSION := "3.10"

set shell := ["powershell", "-nop", "-c"]

# Set up Python environment with specified Python version
bootstrap:
    If (-not (Test-Path .venv)) { py -{{ PYTHON_VERSION }} -m venv .venv }
    & ".venv\Scripts\python.exe" -m pip install pip --quiet --upgrade
    & ".venv\Scripts\python.exe" -m pip install ".[dev]" --upgrade --upgrade-strategy eager

# Check static typing
mypy:
    just clean
    & ".venv\Scripts\mypy.exe" azure_requests

# Remove compiled assets
clean:
    -Remove-Item -Recurse -Force -ErrorAction Ignore build
    -Remove-Item -Recurse -Force -ErrorAction Ignore dist

# Build the whole project, create a release
build: clean bootstrap
    & ".venv\Scripts\python.exe" -m build

# Upload the release to PyPi
upload:
    & ".venv\Scripts\python.exe" -m twine upload dist/*
