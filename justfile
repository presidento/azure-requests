PYTHON_VERSION := "3.10"

set shell := ["powershell", "-nop", "-c"]

# Set up Python environment with specified Python version
bootstrap:
    If (-not (Test-Path .venv)) { py -{{ PYTHON_VERSION }} -m venv .venv }
    & ".venv\Scripts\python.exe" -m pip install pip mypy setuptools wheel twine black pylint types-requests --quiet --upgrade
    & ".venv\Scripts\python.exe" -m pip install . --upgrade --upgrade-strategy eager

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
    & ".venv\Scripts\python.exe" setup.py sdist bdist_wheel

# Upload the release to PyPi
upload:
    & ".venv\Scripts\python.exe" -m twine upload dist/*
