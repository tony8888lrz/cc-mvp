# Repository Guidelines

## Project Structure & Module Organization
- Django project root carries `manage.py`, `requirements.txt`, and `pytest.ini`.
- Settings/routing stay in `config/` (`settings.py`, `urls.py`, `wsgi.py`, `asgi.py`).
- Domain logic is in `apps/user_profile/` (`models.py`, `serializers.py`, `views.py`, `urls.py`, `exceptions.py`); tests live in `apps/user_profile/tests.py`.
- Tooling sits in `Dockerfile`, `docker-compose.yml`, `Makefile`; runtime logs drop into `logs/`.
- Copy `.env.example` to `.env` before running; keep secrets out of Git.

## Build, Test, and Development Commands
```bash
make install       # install deps into the active venv
make migrate       # makemigrations + migrate
make run           # dev server on 0.0.0.0:8000
make test          # pytest suite
make docker-build  # build service image
make docker-up     # start app + MySQL via docker-compose
make docker-down   # stop containers
pytest --cov=apps  # run tests with coverage
```

## Docker Workflow (compose v2)
- Build & start stack: `docker compose up -d --build` (replaces `docker-compose up -d`)
- Run migrations inside web container (uses DB host `db`): `docker compose exec web python manage.py migrate`
- View logs: `docker compose logs -f web` (or `db`)
- Stop stack: `docker compose down`

## Coding Style & Naming Conventions
- Python 3.12, PEP 8; 4-space indents, explicit imports, DRY helpers over inline duplication.
- Follow DRF roles: serializers validate/shape data, viewsets orchestrate, models stay lean.
- Use `snake_case` for functions/modules, `CamelCase` for classes, `UPPER_SNAKE_CASE` for settings/constants.
- Log with `logging.getLogger(__name__)`, not `print`; keep messages actionable.
- Commit model changes with their migrations; let Django generate names.

## Testing Guidelines
- Framework: `pytest` with `pytest-django`; tests stay in `apps/user_profile/tests.py`.
- Name modules/functions `test_*.py` and `test_*`; fixtures close to use.
- Cover serializers, viewsets (including `active`, `search_by_email`, `reactivate`), and model helpers like `soft_delete`.
- Run `pytest` before pushing; use `pytest -k "<keyword>"` to target failures and `pytest -vv` when debugging.

## Commit & Pull Request Guidelines
- Use concise, imperative commits (e.g., `Add profile deactivation audit`); include migrations and doc updates with their code.
- PRs should state what/why, test evidence (`pytest` output), and any API/config impacts; link tickets when available.
- Include curl traces or screenshots for API changes; refresh `README.md`, `DEPLOYMENT.md`, or `QUICK_START.md` if flows shift.

## Security & Configuration Tips
- Do not commit secrets; store overrides in `.env` locally and in your secret manager in production.
- Ensure MySQL is reachable and `ALLOWED_HOSTS` includes your host; set `DEBUG=False` and a strong `SECRET_KEY` outside dev.
- Prefer Docker Compose for environment parity and to avoid host-specific drift.
