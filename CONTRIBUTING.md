TODO: 現状はダミーのため、プロジェクトの実態に合わせて内容を修正する必要がある。

# CONTRIBUTING

Thank you for considering a contribution!

## Planned Contribution Flow
We are currently planning the following contribution workflow, but it is not yet operational:

## Pull Request Flow

1. Fork this repository and create a feature branch from `main`.
2. Make your changes with clear commit messages.
3. Ensure code style and tests pass locally.
4. Open a Pull Request against `main` and fill in a concise summary of your changes.

## Code Style

This project uses [Black](https://github.com/psf/black) and [Ruff](https://github.com/astral-sh/ruff). Run the following before committing:

```bash
uv pip install -e .  # ensure the project and dev tools are installed
black .
ruff .
```

## Testing

Tests are executed with `pytest`.
After setting up the environment via `uv sync`, run:

```bash
pytest
```

Please make sure all tests pass before submitting your Pull Request.
