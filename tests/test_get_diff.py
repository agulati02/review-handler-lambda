import pytest
from src.utils.dependencies import get_repo_service


def test_get_diff():
    repo_service = get_repo_service()
    pull_request_url = "https://api.github.com/repos/agulati02/sample-service/pulls/4"
    installation_id = 87178034

    diff = repo_service.get_diff(pull_request_url, installation_id)
    
    assert diff is not None
    assert isinstance(diff, str)
    assert "diff --git" in diff  # Basic check to see if it's a diff format
