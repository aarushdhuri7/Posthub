# PostHub — Automated Testing with pytest

A small Django API that fetches posts from JSONPlaceholder and demonstrates unit tests, API tests, fixtures, mocks, error handling, and code coverage.

## Features

- `GET /api/posts/` — fetch a list of posts.
- `GET /api/posts/<id>/` — fetch a single post.
- Normalized handling of upstream errors, 404s, timeouts, invalid JSON, and unexpected response shapes.
- pytest + pytest-django + pytest-mock tests.
- pytest-cov terminal and HTML coverage reports.

## Requirements

Python 3.10+ recommended. Use a virtual environment.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the test suite

```bash
pytest -v
```

All external HTTP requests are mocked in the tests, so tests do not depend on JSONPlaceholder or the internet.

## Generate coverage

```bash
pytest --cov=posts --cov-report=term-missing --cov-report=html
```

Open `htmlcov/index.html` in a browser to inspect line-by-line coverage.

## Run the application

```bash
python manage.py runserver
```

Then visit `http://127.0.0.1:8000/api/posts/1/` or `http://127.0.0.1:8000/api/posts/`.

The live endpoints require internet access to JSONPlaceholder.

## API behavior

- Successful responses return JSON with HTTP 200.
- An upstream post 404 becomes HTTP 404.
- Upstream network/service/response errors become HTTP 502.
- A non-positive post ID becomes HTTP 400.
- Unsupported HTTP methods are rejected with HTTP 405.

## Testing concepts

- **Unit tests:** test the service layer with HTTP calls mocked.
- **API tests:** use Django's test client to exercise URL routing, views, and JSON responses.
- **Fixtures:** provide reusable sample data and mock responses.
- **Mocks:** replace `requests.get` to simulate external responses and failures.
- **Coverage:** reports executed code, not correctness or completeness of assertions.

## Project structure

```text
posthub/
├── manage.py
├── pytest.ini
├── requirements.txt
├── posthub/
│   ├── settings.py
│   └── urls.py
└── posts/
    ├── services.py
    ├── views.py
    ├── urls.py
    └── tests/
        ├── conftest.py
        ├── test_services.py
        └── test_api.py
```

## Important note

The included Django settings are for local coursework/demo use. Do not deploy with `DEBUG=True` or the development-only secret key.
