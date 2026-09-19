# ATLAS

[![Lint & Format](https://github.com/umn-adc/ATLAS/actions/workflows/python-ci.yml/badge.svg?event=push&branch=main&job=lint)](https://github.com/umn-adc/ATLAS/actions/workflows/python-ci.yml)
[![Type Check](https://github.com/umn-adc/ATLAS/actions/workflows/python-ci.yml/badge.svg?event=push&branch=main&job=typecheck)](https://github.com/umn-adc/ATLAS/actions/workflows/python-ci.yml)
[![Tests](https://github.com/umn-adc/ATLAS/actions/workflows/python-ci.yml/badge.svg?event=push&branch=main&job=test)](https://github.com/umn-adc/ATLAS/actions/workflows/python-ci.yml)
[![Migrations](https://github.com/umn-adc/ATLAS/actions/workflows/python-ci.yml/badge.svg?event=push&branch=main&job=migrations)](https://github.com/umn-adc/ATLAS/actions/workflows/python-ci.yml)

**A self-hosted platform for developing, deploying, and monitoring algorithmic trading strategies.**

The platform is designed to run on a local machine or server, with team members accessing the same instance through their browsers.

See [Project Documentation](docs/) for architecture details.

### Prerequisites

For local container-based development:

- Git
- Docker Desktop or Docker Engine with Compose

You do not need to install Python or backend dependencies directly when using Docker.

### 1. Clone the repository

I recommend doing it in your root

```bash
git clone https://github.com/umn-adc/ATLAS.git
cd ATLAS
```
### Backend - Native Python

From the backend directory:

```bash
uv sync
uv run uvicorn app.main:app --reload
```

## Contributing

ATLAS is developed by members of the University of Minnesota App Developers Club.

New contributors are welcome!

### Development Workflow

1. Find or claim an issue on the GitHub project board.
2. Read the relevant module and documentation.
3. Create a branch for your work.
4. Implement the change and add appropriate tests.
5. Open a pull request.
6. Address review feedback before merging.

Keep pull requests focused on a single issue whenever possible.

See the [GitHub Issues](https://github.com/orgs/umn-adc/projects/12/views/1) for current work.

Run these from `backend/` to ensure you pass GitHub Actions:

```bash
uv run ruff format .                              # Auto-format code
uv run ruff check --fix                           # Lint + auto-fix issues
uv run pyright                                    # Type check
uv run pytest                                     # Run tests
uv run alembic upgrade head && uv run alembic check  # Verify migrations in sync
```

## Documentation

Project documentation is maintained with MkDocs.

Documentation covers architecture, development setup, module interfaces, and contributor onboarding as these areas are developed.

## License
GPLv3