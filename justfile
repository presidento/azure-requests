PYTHON_VERSION := "3.10"

set shell := ["nu", "-c"]

# Set up Python environment with specified Python version
bootstrap:
    if not (".venv" | path exists) { py -{{ PYTHON_VERSION }} -m venv .venv }
    ^".venv/Scripts/python.exe" -m pip install pip --quiet --upgrade
    ^".venv/Scripts/python.exe" -m pip install ".[dev]" --upgrade --upgrade-strategy eager

# Check static typing
mypy:
    ^".venv/Scripts/mypy.exe" azure_requests

# Remove compiled assets
clean:
    rm --force --recursive --verbose build dist azure_requests.egg-info

# Build the whole project, create a release
build: clean bootstrap
    ^".venv/Scripts/python.exe" -m build

# Upload the release to PyPi
upload:
    ^".venv/Scripts/python.exe" -m twine upload dist/*
