# Pull Requests

## Pull requests should be

1. Made against the `devel` branch.
2. Made from a git feature branch.

## Pull requests will not be accepted that

1. Are not made against the `devel` branch
2. Are submitted from a branch named `devel`
3. Do not pass `ruff` linting and `pytest` test suite
4. Do not work with Python 3.8+
5. Add python modules not included with the Python standard library (optional UI dependencies like `rich` are exceptions)
6. Are made by editing files via the GitHub website

# Coding Guidelines

We follow standard Python PEP8 formatting, enforced by `ruff`.

## Some other points

1. Do not use `\` for line continuations, long strings should be wrapped in `()`. Imports should start a brand new line.
2. String quoting should be done with single quotes `'`, except for situations where you would otherwise have to escape an internal single quote.
3. Docstrings should use three double quotes `"""`.
4. All functions, classes and modules should have docstrings following PEP257 and PEP8 standards.
5. Inline comments should only be used on code where it is not immediately obvious what the code achieves.

# Supported Python Versions

All code needs to support Python 3.8 and above.

# Permitted Python Modules

Core functionality must rely only on the standard library. Optional dependencies for UI improvements (like `rich`) are allowed but must gracefully fallback when unavailable.

# Testing

Please ensure all existing and new tests pass by running:

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
ruff check speedtest.py
```
