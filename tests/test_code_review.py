from typing import Any
from unittest.mock import Mock

from commons.models.enums import UserAction  # type: ignore

import src.utils.dependencies as dependencies


def test_get_code_review_with_mock(monkeypatch: Any):
    fake_reviewer = Mock()
    expected_response = {"summary": "Fibonacci recursion; consider memoization"}
    fake_reviewer.get_code_review.return_value = expected_response

    monkeypatch.setattr(dependencies, "get_llm_service", lambda: fake_reviewer)

    # Example diff input: suboptimal Fibonacci function
    diff_example = "diff --git a/file_2.py b/file_2.py\nindex 00b98e2..ae1255d 100644\n--- a/file_2.py\n+++ b/file_2.py\n@@ -1 +1,5 @@\n-print('This is file #2')\n\\ No newline at end of file\n+def fibonacci(n):\n+    '''Calculates the n-th Fibonacci number'''\n+    if n <= 1:\n+        return n\n+    return fibonacci(n - 1) + fibonacci(n - 2)"

    reviewer = dependencies.get_llm_service()
    response = reviewer.get_code_review(
        user_action=UserAction.REVIEW_REQUESTED, diff=diff_example
    )

    assert response == expected_response
    fake_reviewer.get_code_review.assert_called_once_with(
        user_action=UserAction.REVIEW_REQUESTED, diff=diff_example
    )
