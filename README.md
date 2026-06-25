# SauceDemo Automation

Full-stack test automation suite for [SauceDemo](https://www.saucedemo.com).

## Stack

| Layer | Tool |
|-------|------|
| UI Automation | Playwright + pytest-bdd |
| Reporting | Allure |
| API Mock | FastAPI + uvicorn |
| API Testing | requests + jsonschema |
| CI/CD | GitHub Actions |

## Project structure

```
saucedemo_automation/
├── features/          # BDD feature files
│   ├── login.feature
│   ├── inventory.feature
│   └── checkout.feature
├── pages/             # Page Object Models
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── steps/             # Step definitions + test functions
│   ├── test_login_steps.py
│   ├── test_inventory_steps.py
│   ├── test_checkout_steps.py
│   └── test_api_auth.py
├── api/               # API clients + schemas
│   ├── clients/
│   └── schemas/
├── mock_api/          # FastAPI mock server
│   ├── main.py
│   └── models.py
├── conftest.py
├── pytest.ini
└── requirements.txt
```

## Setup

```bash
pip install -r requirements.txt
playwright install chromium
```

Copy `.env.example` to `.env` and fill in values:
```
BASE_URL=https://www.saucedemo.com
VALID_USERNAME=standard_user
VALID_PASSWORD=secret_sauce
LOCKED_USERNAME=locked_out_user
```

## Run tests

```bash
# Smoke tests only (login + inventory + checkout happy path)
pytest -m smoke

# Checkout flow
pytest -m checkout

# API tests (spins up mock server automatically)
pytest -m api

# Full regression
pytest

# With Allure report
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## Run mock server standalone

```bash
uvicorn mock_api.main:app --reload --port 8000
# Docs: http://localhost:8000/docs
```

## CI pipeline

`api-tests → smoke-tests → regression-tests`

Regression only runs on push to `main`.
