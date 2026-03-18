"""
Performance SLA tests.

Response time thresholds enforced per endpoint. These run with the
'performance' marker and are included in the nightly full suite.
SLA values are defined in test_data.py as a single source of truth.
"""

import time
import pytest
import allure
from src.data.test_data import Users, Repos, SLAs


@allure.feature("Performance")
class TestResponseTimeSLAs:

    @allure.story("GET /users/{username}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.performance
    def test_get_user_response_time(self, auth_client, perf_timer):
        start = time.perf_counter()
        auth_client.get_user(Users.VALID)
        elapsed = time.perf_counter() - start
        perf_timer.assert_under(elapsed, SLAs.GET_USER)

    @allure.story("GET /users/{username}")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.performance
    def test_get_octocat_user_response_time(self, auth_client, perf_timer):
        start = time.perf_counter()
        auth_client.get_user(Users.OCTOCAT)
        elapsed = time.perf_counter() - start
        perf_timer.assert_under(elapsed, SLAs.GET_USER)

    @allure.story("GET /repos/{owner}/{repo}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.performance
    def test_get_repo_response_time(self, auth_client, perf_timer):
        start = time.perf_counter()
        auth_client.get_repo(Repos.OWNER, Repos.NAME)
        elapsed = time.perf_counter() - start
        perf_timer.assert_under(elapsed, SLAs.GET_REPO)

    @allure.story("GET /repos/{owner}/{repo}")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.performance
    def test_get_cpython_repo_response_time(self, auth_client, perf_timer):
        start = time.perf_counter()
        auth_client.get_repo(Repos.CPython_OWNER, Repos.CPython_NAME)
        elapsed = time.perf_counter() - start
        perf_timer.assert_under(elapsed, SLAs.GET_REPO)

    @allure.story("GET /users/{username}/repos")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.performance
    def test_list_repos_response_time(self, auth_client, perf_timer):
        start = time.perf_counter()
        auth_client.list_repos(Users.OCTOCAT)
        elapsed = time.perf_counter() - start
        # List calls get a larger budget; more data to serialize
        perf_timer.assert_under(elapsed, SLAs.LIST_REPOS)

    @allure.story("GET /user (authenticated)")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.performance
    def test_authenticated_user_endpoint_response_time(self, auth_client, perf_timer):
        start = time.perf_counter()
        auth_client.get_authenticated_user()
        elapsed = time.perf_counter() - start
        perf_timer.assert_under(elapsed, SLAs.AUTHENTICATED_USER)

    @allure.story("Consistency")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.performance
    def test_user_endpoint_three_consecutive_calls_all_within_sla(
        self, auth_client, perf_timer
    ):
        """
        Validates consistency, not just best-case latency.
        A single fast call can mask intermittent slowness.
        """
        for i in range(3):
            start = time.perf_counter()
            auth_client.get_user(Users.OCTOCAT)
            elapsed = time.perf_counter() - start
            perf_timer.assert_under(elapsed, SLAs.GET_USER)
