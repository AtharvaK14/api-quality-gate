"""
Functional tests for GET /users/{username}.

Covers: happy path, schema correctness, field semantics,
boundary values, org vs user type distinction, and auth vs anon access.
"""

import re
import pytest
import allure
from src.schemas.user_schema import GitHubUser
from src.data.test_data import Users


@allure.feature("Users API")
class TestGetUser:

    @allure.story("Happy Path")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_get_valid_user_returns_200(self, auth_client):
        response = auth_client.get_user(Users.VALID)
        assert response.status_code == 200

    @allure.story("Schema Validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_user_response_matches_schema(self, auth_client):
        response = auth_client.get_user(Users.VALID)
        # Pydantic v2 raises ValidationError on schema mismatch - no try/except needed
        user = GitHubUser(**response.json())
        assert user.login == Users.VALID

    @allure.story("Schema Validation")
    @allure.severity(allure.severity_level.NORMAL)
    def test_user_html_url_is_valid_github_url(self, auth_client):
        response = auth_client.get_user(Users.VALID)
        user = GitHubUser(**response.json())
        assert str(user.html_url).startswith("https://github.com/")

    @allure.story("Schema Validation")
    @allure.severity(allure.severity_level.NORMAL)
    def test_user_avatar_url_points_to_github_cdn(self, auth_client):
        response = auth_client.get_user(Users.VALID)
        user = GitHubUser(**response.json())
        # Avatars are served from avatars.githubusercontent.com
        assert "githubusercontent.com" in str(user.avatar_url)

    @allure.story("Field Semantics")
    @allure.severity(allure.severity_level.NORMAL)
    def test_user_type_is_user_string(self, auth_client):
        response = auth_client.get_user(Users.VALID)
        user = GitHubUser(**response.json())
        assert user.type == "User"

    @allure.story("Field Semantics")
    @allure.severity(allure.severity_level.NORMAL)
    def test_org_type_is_organization_string(self, auth_client):
        response = auth_client.get_user(Users.ORG)
        user = GitHubUser(**response.json())
        assert user.type == "Organization"

    @allure.story("Field Semantics")
    @allure.severity(allure.severity_level.MINOR)
    def test_user_id_is_positive_integer(self, auth_client):
        response = auth_client.get_user(Users.VALID)
        user = GitHubUser(**response.json())
        assert user.id > 0

    @allure.story("Field Semantics")
    @allure.severity(allure.severity_level.MINOR)
    def test_user_public_repos_is_non_negative(self, auth_client):
        response = auth_client.get_user(Users.VALID)
        user = GitHubUser(**response.json())
        assert user.public_repos >= 0

    @allure.story("Field Semantics")
    @allure.severity(allure.severity_level.MINOR)
    def test_user_followers_is_non_negative(self, auth_client):
        response = auth_client.get_user(Users.VALID)
        user = GitHubUser(**response.json())
        assert user.followers >= 0

    @allure.story("Field Semantics")
    @allure.severity(allure.severity_level.MINOR)
    def test_user_created_at_is_iso8601_format(self, auth_client):
        response = auth_client.get_user(Users.VALID)
        user = GitHubUser(**response.json())
        # GitHub returns ISO 8601: 2011-09-03T15:00:00Z
        iso_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
        assert iso_pattern.match(user.created_at), (
            f"created_at '{user.created_at}' does not match ISO 8601"
        )

    @allure.story("Field Semantics")
    @allure.severity(allure.severity_level.MINOR)
    def test_two_different_users_have_unique_ids(self, auth_client):
        resp1 = auth_client.get_user(Users.VALID)
        resp2 = auth_client.get_user(Users.OCTOCAT)
        id1 = GitHubUser(**resp1.json()).id
        id2 = GitHubUser(**resp2.json()).id
        assert id1 != id2

    @allure.story("Response Headers")
    @allure.severity(allure.severity_level.MINOR)
    def test_response_content_type_is_json(self, auth_client):
        response = auth_client.get_user(Users.VALID)
        assert "application/json" in response.headers.get("Content-Type", "")

    @allure.story("Response Headers")
    @allure.severity(allure.severity_level.MINOR)
    def test_rate_limit_header_present_when_authenticated(self, auth_client):
        response = auth_client.get_user(Users.VALID)
        assert "X-RateLimit-Limit" in response.headers

    @allure.story("Anonymous Access")
    @allure.severity(allure.severity_level.NORMAL)
    def test_anon_client_can_fetch_public_user(self, anon_client):
        response = anon_client.get_user(Users.OCTOCAT)
        assert response.status_code == 200

    @allure.story("Anonymous Access")
    @allure.severity(allure.severity_level.MINOR)
    def test_anon_response_schema_matches(self, anon_client):
        response = anon_client.get_user(Users.OCTOCAT)
        user = GitHubUser(**response.json())
        assert user.login == Users.OCTOCAT

    @allure.story("Field Semantics")
    @allure.severity(allure.severity_level.MINOR)
    def test_guido_user_has_non_zero_public_repos(self, auth_client):
        response = auth_client.get_user(Users.GUIDO)
        user = GitHubUser(**response.json())
        assert user.public_repos > 0

    @allure.story("Field Semantics")
    @allure.severity(allure.severity_level.MINOR)
    def test_html_url_contains_correct_login(self, auth_client):
        response = auth_client.get_user(Users.OCTOCAT)
        user = GitHubUser(**response.json())
        assert Users.OCTOCAT in str(user.html_url)

    @allure.story("Schema Validation")
    @allure.severity(allure.severity_level.NORMAL)
    def test_response_body_is_valid_json(self, auth_client):
        response = auth_client.get_user(Users.VALID)
        # response.json() raises JSONDecodeError if invalid - no assertion needed
        body = response.json()
        assert isinstance(body, dict)
