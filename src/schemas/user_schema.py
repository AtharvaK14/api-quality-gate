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
    name: Optional[str] = None
    company: Optional[str] = None
    blog: Optional[str] = None
    location: Optional[str] = None
    email: Optional[str] = None
    bio: Optional[str] = None
    following: int = 0
    public_gists: int = 0
