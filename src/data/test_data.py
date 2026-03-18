"""
Centralized test data factory.

All test inputs are defined here so changes propagate everywhere.
Using well-known stable GitHub accounts ensures tests are not brittle.
"""


class Users:
    # Linus Torvalds - stable, high-follower individual account
    VALID = "torvalds"
    # Python org - validates Organization type response
    ORG = "python"
    # GitHub's own mascot account - used by GitHub internally for examples
    OCTOCAT = "octocat"
    # Guido van Rossum - stable individual with known public repos
    GUIDO = "gvanrossum"
    # Deliberately non-existent - suffix chosen to avoid accidental real accounts
    NOT_FOUND = "this-user-cannot-exist-xk39z99"
    # Username with only valid chars but zero chance of existing
    NOT_FOUND_ALT = "zzz-no-such-user-abc123xyz"


class Repos:
    # linux kernel - most starred repo by a known user; very stable
    OWNER = "torvalds"
    NAME = "linux"
    FULL_NAME = "torvalds/linux"

    # CPython - stable, well-known, good for schema tests
    CPython_OWNER = "python"
    CPython_NAME = "cpython"

    # Non-existent repo under a real owner
    NOT_FOUND_OWNER = "torvalds"
    NOT_FOUND_NAME = "this-repo-does-not-exist-xk39z99"


class SLAs:
    """Response time SLAs in milliseconds."""
    GET_USER = 800
    GET_REPO = 800
    LIST_REPOS = 1200
    AUTHENTICATED_USER = 800
