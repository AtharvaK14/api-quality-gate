import os
import pytest
from src.api.github_client import GitHubClient


@pytest.fixture(scope="session")
def auth_client():
    """
    Authenticated GitHub client. Token loaded from env var GITHUB_TOKEN.
    Session-scoped so the same requests.Session is reused across all tests,
    avoiding per-test TCP handshake overhead and staying under rate limits.
    """
    token = os.environ.get("GITHUB_TOKEN")
    return GitHubClient(token=token)


@pytest.fixture(scope="session")
def anon_client():
    """
    Unauthenticated client. Used for 401/403 contrast tests and to verify
    public endpoints work without credentials.
    """
    return GitHubClient()


@pytest.fixture
def perf_timer():
    """
    Thin SLA assertion helper. Kept as a fixture (not a util function) so
    it appears in Allure's fixture panel and failures include the SLA value.
    """

    class Timer:
        def assert_under(self, response_time: float, sla_ms: int) -> None:
            elapsed_ms = response_time * 1000
            assert elapsed_ms < sla_ms, (
                f"Response took {elapsed_ms:.0f}ms, SLA is {sla_ms}ms"
            )

    return Timer()
