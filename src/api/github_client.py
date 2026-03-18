import requests

BASE_URL = "https://api.github.com"


class GitHubClient:
    def __init__(self, token=None):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            }
        )
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def get_user(self, username: str) -> requests.Response:
        return self.session.get(f"{BASE_URL}/users/{username}")

    def get_repo(self, owner: str, repo: str) -> requests.Response:
        return self.session.get(f"{BASE_URL}/repos/{owner}/{repo}")

    def list_repos(self, username: str) -> requests.Response:
        return self.session.get(f"{BASE_URL}/users/{username}/repos")

    def get_authenticated_user(self) -> requests.Response:
        """Requires an authenticated session. Used for 401 contrast testing."""
        return self.session.get(f"{BASE_URL}/user")
