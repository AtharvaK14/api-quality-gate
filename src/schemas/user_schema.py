from pydantic import BaseModel, HttpUrl
from typing import Optional

class GitHubUser(BaseModel):
    login: str
    id: int
    type: str
    public_repos: int
    followers: int
    html_url: HttpUrl
    avatar_url: HttpUrl
    created_at: str