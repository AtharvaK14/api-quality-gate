"""
Functional tests for GET /repos/{owner}/{repo} and GET /users/{username}/repos.

Covers: schema correctness, field semantics, list endpoint behavior,
ownership assertions, and public repo invariants.
"""

import pytest
import allure
from src.schemas.repo_schema import GitHubRepo
from src.data.test_data import Repos, Users


@allure.feature("Repos API")
class TestGetRepo:

    @allure.story("Happy Path")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_get_valid_repo_returns_200(self, auth_client):
        response = auth_client.get_repo(Repos.OWNER, Repos.NAME)
        assert response.status_code == 200

    @allure.story("Schema Validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_repo_response_matches_schema(self, auth_client):
        response = auth_client.get_repo(Repos.OWNER, Repos.NAME)
        repo = GitHubRepo(**response.json())
        assert repo.name == Repos.NAME

    @allure.story("Schema Validation")
    @allure.severity(allure.severity_level.NORMAL)
    def test_repo_html_url_starts_with_https_github(self, auth_client):
        response = auth_client.get_repo(Repos.OWNER, Repos.NAME)
        repo = GitHubRepo(**response.json())
        assert str(repo.html_url).startswith("https://github.com/")

    @allure.story("Field Semantics")
    @allure.severity(allure.severity_level.NORMAL)
    def test_repo_full_name_matches_owner_slash_name(self, auth_client):
        response = auth_client.get_repo(Repos.OWNER, Repos.NAME)
        repo = GitHubRepo(**response.json())
        assert repo.full_name == Repos.FULL_NAME

    @allure.story("Field Semantics")
    @allure.severity(allure.severity_level.NORMAL)
    def test_public_repo_private_flag_is_false(self, auth_client):
        response = auth_client.get_repo(Repos.OWNER, Repos.NAME)
        repo = GitHubRepo(**response.json())
        assert repo.private is False

    @allure.story("Field Semantics")
    @allure.severity(allure.severity_level.MINOR)
    def test_repo_stargazers_count_is_non_negative(self, auth_client):
        response = auth_client.get_repo(Repos.OWNER, Repos.NAME)
        repo = GitHubRepo(**response.json())
        assert repo.stargazers_count >= 0

    @allure.story("Field Semantics")
    @allure.severity(allure.severity_level.MINOR)
    def test_repo_forks_count_is_non_negative(self, auth_client):
        response = auth_client.get_repo(Repos.OWNER, Repos.NAME)
        repo = GitHubRepo(**response.json())
        assert repo.forks_count >= 0

    @allure.story("Field Semantics")
    @allure.severity(allure.severity_level.NORMAL)
    def test_repo_has_non_empty_default_branch(self, auth_client):
        response = auth_client.get_repo(Repos.OWNER, Repos.NAME)
        repo = GitHubRepo(**response.json())
        assert repo.default_branch and len(repo.default_branch) > 0

    @allure.story("Field Semantics")
    @allure.severity(allure.severity_level.NORMAL)
    def test_repo_owner_login_matches_requested_owner(self, auth_client):
        response = auth_client.get_repo(Repos.OWNER, Repos.NAME)
        repo = GitHubRepo(**response.json())
        assert repo.owner.login == Repos.OWNER

    @allure.story("Field Semantics")
    @allure.severity(allure.severity_level.MINOR)
    def test_repo_id_is_positive_integer(self, auth_client):
        response = auth_client.get_repo(Repos.OWNER, Repos.NAME)
        repo = GitHubRepo(**response.json())
        assert repo.id > 0

    @allure.story("Field Semantics")
    @allure.severity(allure.severity_level.MINOR)
    def test_linux_repo_language_is_c(self, auth_client):
        response = auth_client.get_repo(Repos.OWNER, Repos.NAME)
        repo = GitHubRepo(**response.json())
        assert repo.language == "C"

    @allure.story("Field Semantics")
    @allure.severity(allure.severity_level.MINOR)
    def test_cpython_repo_language_is_python(self, auth_client):
        response = auth_client.get_repo(Repos.CPython_OWNER, Repos.CPython_NAME)
        repo = GitHubRepo(**response.json())
        assert repo.language == "Python"


@allure.feature("Repos API")
class TestListRepos:

    @allure.story("List Repos")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_list_repos_returns_200(self, auth_client):
        response = auth_client.list_repos(Users.OCTOCAT)
        assert response.status_code == 200

    @allure.story("List Repos")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_list_repos_returns_a_list(self, auth_client):
        response = auth_client.list_repos(Users.OCTOCAT)
        assert isinstance(response.json(), list)

    @allure.story("List Repos")
    @allure.severity(allure.severity_level.NORMAL)
    def test_list_repos_items_each_have_a_name_field(self, auth_client):
        response = auth_client.list_repos(Users.OCTOCAT)
        repos = response.json()
        assert len(repos) > 0
        for repo in repos:
            assert "name" in repo, f"Repo entry missing 'name' field: {repo}"

    @allure.story("List Repos")
    @allure.severity(allure.severity_level.NORMAL)
    def test_list_repos_count_does_not_exceed_default_page_size(self, auth_client):
        # Default per_page is 30; without pagination params, max is 30
        response = auth_client.list_repos(Users.OCTOCAT)
        assert len(response.json()) <= 30
