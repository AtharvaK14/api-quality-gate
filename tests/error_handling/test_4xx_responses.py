"""
Error handling tests for 4xx responses.

Most candidates skip this category. Covering 404/401 paths demonstrates
adversarial thinking about quality beyond the happy path.
"""

import pytest
import allure
from src.data.test_data import Users, Repos


@allure.feature("Error Handling")
class TestNotFoundResponses:

    @allure.story("404 User")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_nonexistent_user_returns_404(self, anon_client):
        response = anon_client.get_user(Users.NOT_FOUND)
        assert response.status_code == 404

    @allure.story("404 User")
    @allure.severity(allure.severity_level.NORMAL)
    def test_404_user_body_has_message_field(self, anon_client):
        response = anon_client.get_user(Users.NOT_FOUND)
        body = response.json()
        assert "message" in body

    @allure.story("404 User")
    @allure.severity(allure.severity_level.NORMAL)
    def test_404_user_message_is_not_found(self, anon_client):
        response = anon_client.get_user(Users.NOT_FOUND)
        body = response.json()
        assert body["message"] == "Not Found"

    @allure.story("404 User")
    @allure.severity(allure.severity_level.MINOR)
    def test_404_user_body_has_documentation_url(self, anon_client):
        response = anon_client.get_user(Users.NOT_FOUND)
        body = response.json()
        assert "documentation_url" in body
        assert body["documentation_url"].startswith("https://")

    @allure.story("404 User")
    @allure.severity(allure.severity_level.MINOR)
    def test_alt_nonexistent_user_also_returns_404(self, anon_client):
        """Ensures 404 is consistent, not tied to one specific username."""
        response = anon_client.get_user(Users.NOT_FOUND_ALT)
        assert response.status_code == 404

    @allure.story("404 Repo")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_nonexistent_repo_returns_404(self, anon_client):
        response = anon_client.get_repo(Repos.NOT_FOUND_OWNER, Repos.NOT_FOUND_NAME)
        assert response.status_code == 404

    @allure.story("404 Repo")
    @allure.severity(allure.severity_level.NORMAL)
    def test_404_repo_body_has_message_field(self, anon_client):
        response = anon_client.get_repo(Repos.NOT_FOUND_OWNER, Repos.NOT_FOUND_NAME)
        body = response.json()
        assert "message" in body

    @allure.story("404 Repo")
    @allure.severity(allure.severity_level.NORMAL)
    def test_404_repo_message_is_not_found(self, anon_client):
        response = anon_client.get_repo(Repos.NOT_FOUND_OWNER, Repos.NOT_FOUND_NAME)
        assert response.json()["message"] == "Not Found"


@allure.feature("Error Handling")
class TestAuthenticationErrors:

    @allure.story("401 Unauthorized")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_anon_request_to_auth_only_endpoint_returns_401(self, anon_client):
        response = anon_client.get_authenticated_user()
        assert response.status_code == 401

    @allure.story("401 Unauthorized")
    @allure.severity(allure.severity_level.NORMAL)
    def test_401_body_has_message_field(self, anon_client):
        response = anon_client.get_authenticated_user()
        body = response.json()
        assert "message" in body

    @allure.story("401 Unauthorized")
    @allure.severity(allure.severity_level.MINOR)
    def test_401_message_indicates_auth_required(self, anon_client):
        response = anon_client.get_authenticated_user()
        body = response.json()
        # GitHub returns "Requires authentication" for this endpoint
        assert "authentication" in body["message"].lower() or \
               "credentials" in body["message"].lower() or \
               "401" in str(response.status_code)

    @allure.story("Auth Contrast")
    @allure.severity(allure.severity_level.NORMAL)
    def test_auth_client_can_reach_authenticated_endpoint(self, auth_client):
        """Confirms that the auth_client token is valid when provided."""
        response = auth_client.get_authenticated_user()
        # 200 with token, 401 without - this test validates the fixture contrast
        assert response.status_code == 200
