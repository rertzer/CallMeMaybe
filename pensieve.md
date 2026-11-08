# Summary

Maybe is a function calling tool that translates natural language prompts into structured function calls.

It uses constrained decoding to guarantee 100% valid JSON output.

# Concepts

## Function Calling

Translates natural language requests into precise function calls with typed arguments. Instead of answering directly the question in natural language, it provides tools to solve it.

Function calls enables LLM to

- Interact with external systems (Call APIs, query databases, control devices)
- Execute code
- Chain operations: Break complex tasks into executable steps
- Provide structured output: Generate, JSON, XML
- Extract structured data from unstructured text

## Generation Pipeline:

1. Prompt -> Tokenization -> Input IDs -> LLM -> Logits -> Next Token Selection
2. Add next token and repeat

## Constrained Decoding

A technique that guides the model output token-by-token to guarantee valid structure.
Constrained decoding modify the logits before token selection:

1. The model produces logits for all possible tokens
2. You identify which tokens would maintain both a valid JSON structure and compliance with the expected schema
3. You set logits for invalid tokens to negative infinity
4. You sample only from the remaining valid tokens

# Small Language Models

- Qwen/Qwen3-0.6B

# LLM SDK

## wrapper class `Small_LLM_Model`

- `get_logits_from_input_ids(input_ids: List[int]) -> list[float]`
- `get_path_to_vocab_file() -> str`
- `encode(text: str) -> Tensor`
- `decode(token_ids: list[int]) -> str (optional)`

# Python

## General Instructions

- Python 3.10 or later
- flake8 coding standard
- `try-except` blocks
- context managers for files and connections
- No file / connections leaks
- type hints for function parameters, return types and variables: use `typing` module
- use `mypy` for static type checking
- include docstrings in functions and classes (PEP 257) Google or NumPy style
- Document purpose, parameters and returns
- Add tests using `unittest` or `pytest`
- Include a `.gitignore`
- Use a virtual env (`venv` or `conda`)
- All classes must use `pydantic` for validation
- `numpy` and `json` packages are allowed
- ! the reviewer will run `uv sync`

## Packages

### `typing`

### `mypy`

### `pytest`

### `pydantic`

### `uv`

`uv` is an extremely fast Python package and project manager written in Rust. It acts like a single tool to replace several common Python tools, and it can manage dependencies, virtual environments, and Python versions.

- Install with `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Initialize projects with `uv init myproj` and add dependencies with uv add package
- Run scripts with `uv run script.py` — no manual virtual environment activation needed
- UV replaces pip, virtualenv, pyenv, and pip-tools in a single tool
- Lock files (`uv.lock`) ensure reproducible environments across machines
- Use uvx to run CLI tools like black and ruff without permanent installation
- Updating UV: `uv self update`

the command `uv init myproject` create a new directory `myproject` containing:

```
.gitignore
 .python-version
 README.md
 hello.py
 pyproject.toml
```

add packages with:

```sh
uv add scikit-learn
```

To remove a dependency:

```sh
uv remove scikit-learn
```

Install a python version:

```sh
uv python install 3.12
```

Python installations are stored in `~/.local/share/uv/python/`

Pin a project to a specific version:

```sh
uv python pin 3.12
```

Changing version for the current project:

```sh
requires-python = ">=3.12"
```

List installed versions:

```sh
uv python list --only-installed
```

#### `uv sync`

The command first checks against existing Python installations. If the requested version isn't found, UV downloads and installs it.

The command creates a new virtual environment inside the project directory, replacing the old one. It reinstalls all dependencies from `pyproject.toml` and `uv.lock` files.

### `numpy`

### `json`

# Makefile

- use `-strict`
- Rules:
  - install
  - run
  - debug
  - clean
  - lint
  - lint-strict (optional)

## install

- install dependencies using uv

## run

- execute the main script

## debug

- run the main script in debug mode using python's built-in debugger (`pdb`)

## clean

- remove temporary files or caches:
- `__pycache__`
- `.mypy_cache`

## lint

execute the commands:

- `flake8 .`
- `mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs`

## lint-strict

execute the commands:

- `flake8 . `
- `mypy . --strict`

# Usage

```sh
uv run python -m src [--function_definition <functions_definition_file>] [--input <input_file>] [--output <output_file>]
```

By default, the program will read input from `data/input/` and write output to `data/output/`

- `data/input/functions_definition.json`
- `data/input/function_calling_tests.json`
- `data/output/function_calls.json`

## Input files

### `function_calling_tests.json`

```json
[
  {
    "prompt": "What is the sum of 2 and 3?"
  },
  {
    "prompt": "What is the sum of 265 and 345?"
  },
  {
    "prompt": "Greet shrek"
  },
  {
    "prompt": "Greet john"
  },
  {
    "prompt": "Reverse the string 'hello'"
  }
]
```

### `functions_definition.json`

```json
[
  {
    "name": "fn_add_numbers",
    "description": "Add two numbers together and return their sum.",
    "parameters": {
      "a": {
        "type": "number"
      },
      "b": {
        "type": "number"
      }
    },
    "returns": {
      "type": "number"
    }
  },
  {
    "name": "fn_greet",
    "description": "Generate a greeting message for a person by name.",
    "parameters": {
      "name": {
        "type": "string"
      }
    },
    "returns": {
      "type": "string"
    }
  },
  {
    "name": "fn_reverse_string",
    "description": "Reverse a string and return the reversed result.",
    "parameters": {
      "s": {
        "type": "string"
      }
    },
    "returns": {
      "type": "string"
    }
  }
]
```

## Output File: `data/output/function_calling_results.json`

```json
[
  {
    "prompt": "What is the sum of 2 and 3?",
    "name": "fn_add_numbers",
    "parameters": { "a": 2.0, "b": 3.0 }
  },
  {
    "prompt": "Reverse the string 'hello'",
    "name": "fn_reverse_string",
    "parameters": { "s": "hello" }
  }
]
```

### Validation Rules

- valid JSON (no trailing commas, no comments)
- Keys and types must match the schema in `functions_definition.json`
- All required arguments must be present
- Argument types must match the function definition

# Content

- `src/`
- `pyproject.toml`
- `uv.lock`
- `llm_sdk/`
- `data/input`
- `README.md`

# Performances

- > 90% correct function selection and arguement extraction
- 100% valid JSON
- Process all tests prompts in under 5 minutes
- Robust error handling
  - malformed inputs
  - missing files
  - edge cases

# README

- `README.md` at the Git repo root
- First line: **_This project has been created as part of the 42 curiculum by rertzer_**
- Content:
  - Description
  - Instructions
  - Resources
  - Algorithm explanation
  - Design Decisions
  - Performance analysis
  - Challenges faced
  - Testing strategy
  - Example usage

# Bonus

- Support for multiple LLM models
- Recoding the tokenizer: do not use `encode` and `decode` functions
- Advanced error recovery mechanisms
- Performance optimizations (caching, batching)
- Comprehensive test suite
- Visualization of the generation process
- Support for complex nested function arguments
- Public implementation of encode and decode ?
- Demonstration of how encoding and decoding integrate with constrained methods
