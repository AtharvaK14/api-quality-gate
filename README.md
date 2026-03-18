# api-quality-gate

[![API Quality Gate](https://github.com/AtharvaK14/api-quality-gate/actions/workflows/test.yml/badge.svg)](https://github.com/AtharvaK14/api-quality-gate/actions/workflows/test.yml)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

**[Live Allure Report](https://AtharvaK14.github.io/api-quality-gate/)**

Production-grade API test automation framework targeting the GitHub REST API. Covers functional correctness, schema validation, error path coverage, and per-endpoint performance SLAs. Tests run on every push and on a nightly schedule, with results published to a live Allure report via GitHub Pages.

---

## Prerequisites

| Requirement | Notes |
|---|---|
| Python 3.11+ | `python --version` to verify |
| GitHub PAT | Settings > Developer Settings > Personal Access Tokens > Fine-grained tokens. Needs `repo` read scope. |
| Allure CLI | Required only for local report generation. Install via [the official docs](https://allurereport.org/docs/install/). |

---

## What This Tests

| Endpoint | Test Type | Count | SLA |
|---|---|---|---|
| `GET /users/{username}` | Functional, Schema, Headers | 18 | 800ms |
| `GET /repos/{owner}/{repo}` | Functional, Schema | 12 | 800ms |
| `GET /users/{username}/repos` | Functional, List validation | 4 | 1200ms |
| `GET /users/{username}` (404) | Error handling | 5 | - |
| `GET /repos/{owner}/{repo}` (404) | Error handling | 3 | - |
| `GET /user` (401) | Auth contrast | 4 | 800ms |
| Performance (all endpoints) | SLA assertions | 7 | per above |

**Total: 53 test cases**

---

## Framework Architecture

**Why session-scoped fixtures:** `auth_client` and `anon_client` are scoped to `session` in `conftest.py`. This reuses a single `requests.Session` (and its underlying TCP connection pool) across all tests, avoiding per-test handshake overhead and significantly reducing the risk of hitting GitHub's rate limit during the full parallel run.

**Why Pydantic over jsonschema:** Pydantic v2 gives typed field access after validation, catches type coercion issues that jsonschema misses (e.g., an integer field returning a string), and integrates naturally with the rest of the Python ecosystem. The `GitHubUser` and `GitHubRepo` models also serve as living documentation of the expected contract.

**Why pytest-xdist:** The full suite runs with `-n auto`, distributing tests across all available CPU cores. Tests are written to be fully independent (no shared mutable state) so parallel execution is safe. This cuts total wall-clock time roughly in half on a 4-core runner.

**Why two CI stages:** A fast smoke gate (10 tests, serial) runs first on every push. The full suite only runs if smoke passes, preventing wasted runner minutes on a broken build. The smoke set covers one test per endpoint class, enough to catch regressions quickly.

**Centralized test data:** `src/data/test_data.py` is the single source of truth for all usernames, repo names, and SLA values. Changing a target username or tightening an SLA requires editing one file, not hunting through test files.

---

## How to Run Locally

```bash
# Set up environment
python -m venv venv

source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

pip install -r requirements.txt

# Export your GitHub PAT (optional, but increases rate limits and enables auth tests)
export GITHUB_TOKEN=ghp_your_token_here   # Mac/Linux
set GITHUB_TOKEN=ghp_your_token_here      # Windows CMD
$env:GITHUB_TOKEN="ghp_your_token_here"  # Windows PowerShell

# Run smoke tests only (fast, serial)
pytest -m smoke -p no:xdist -v

# Run full suite (parallel)
pytest -v

# Run only performance tests
pytest -m performance -v

# Lint
ruff check src/ tests/

# Generate and open Allure report locally (requires Allure CLI)
allure serve allure-results
```

---

## CI/CD Pipeline

Two-stage GitHub Actions pipeline defined in `.github/workflows/`:

**Stage 1 (test.yml):** On every push to `main`, a smoke gate runs 10 targeted tests serially. If the gate passes, the full 53-test regression suite runs in parallel with `pytest-xdist`. Allure result artifacts are uploaded regardless of outcome so failures are always diagnosable.

**Stage 2 (pages.yml):** Triggered on successful completion of the test workflow. Downloads the Allure artifact, generates the HTML report with trend history, and deploys to the `gh-pages` branch. The live report URL updates automatically within ~60 seconds of a passing run.

Nightly schedule (`0 6 * * *` UTC) runs the full suite unconditionally, catching regressions introduced by upstream API changes rather than code changes.

---

## Project Structure

```
api-quality-gate/
├── .github/workflows/
│   ├── test.yml          # Two-stage CI: smoke gate + full regression
│   └── pages.yml         # Allure report deployment to GitHub Pages
├── src/
│   ├── api/
│   │   └── github_client.py   # Thin HTTP wrapper; no test logic
│   ├── schemas/
│   │   ├── user_schema.py     # Pydantic model for /users response
│   │   └── repo_schema.py     # Pydantic model for /repos response
│   └── data/
│       └── test_data.py       # Centralized test inputs and SLA values
├── tests/
│   ├── conftest.py            # Session-scoped fixtures
│   ├── functional/
│   │   ├── test_users.py      # 18 user endpoint tests
│   │   └── test_repos.py      # 16 repo endpoint tests
│   ├── error_handling/
│   │   └── test_4xx_responses.py  # 12 error path tests
│   └── performance/
│       └── test_response_times.py # 7 SLA assertion tests
├── pytest.ini
└── requirements.txt
```