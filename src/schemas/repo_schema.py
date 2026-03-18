from pydantic import BaseModel, HttpUrl
from typing import Optional


class RepoOwner(BaseModel):
    login: str
    id: int
    type: str
    html_url: HttpUrl
    avatar_url: HttpUrl


class GitHubRepo(BaseModel):
    id: int
    name: str
    full_name: str
    private: bool
    owner: RepoOwner
    html_url: HttpUrl
    description: Optional[str] = None
    language: Optional[str] = None
    stargazers_count: int
    forks_count: int
    default_branch: str
    fork: bool = False
    size: int = 0
    open_issues_count: int = 0
    watchers_count: int = 0
