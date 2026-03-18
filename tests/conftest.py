import pytest, os, time
from src.api.github_client import GitHubClient

@pytest.fixture(scope='session')
def auth_client():
    token = os.environ.get('GITHUB_TOKEN')
    return GitHubClient(token=token)

@pytest.fixture(scope='session')
def anon_client():
    return GitHubClient()

@pytest.fixture
def perf_timer():
    class Timer:
        def assert_under(self, response_time, sla_ms):
            assert response_time * 1000 < sla_ms, \
                f'Response took {response_time*1000:.0f}ms, SLA is {sla_ms}ms'
    return Timer()