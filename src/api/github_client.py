import os, requests

BASE_URL = 'https://api.github.com'

class GitHubClient:
    def __init__(self, token=None):
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'
        })
        if token:
            self.session.headers['Authorization'] = f'Bearer {token}'

    def get_user(self, username):
        return self.session.get(f'{BASE_URL}/users/{username}')

    def get_repo(self, owner, repo):
        return self.session.get(f'{BASE_URL}/repos/{owner}/{repo}')

    def list_repos(self, username):
        return self.session.get(f'{BASE_URL}/users/{username}/repos')
