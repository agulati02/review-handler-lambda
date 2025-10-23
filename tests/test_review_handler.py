import json
from typing import Any

from commons.models.enums import UserAction  # type: ignore

from src.lambda_function import lambda_handler


def get_mock_event() -> dict[str, Any]:
    return {
        "Records": [
            {
                "body": json.dumps(
                    {
                        "action": "synchronize",
                        "number": 4,
                        "pull_request": {
                            "url": "https://api.github.com/repos/agulati02/sample-service/pulls/4",
                            "id": 2853190061,
                        },
                        "installation": {
                            "id": 87178034,
                            "node_id": "MDIzOkludGVncmF0aW9uSW5zdGFsbGF0aW9uODcxNzgwMzQ=",
                        },
                        "trigger": UserAction.REVIEW_REQUESTED,
                    },
                )
            }
        ]
    }


def test_lambda_handler_review_request():
    mock_event = get_mock_event()
    response = lambda_handler(mock_event, None)

    assert response["statusCode"] == 200
    body = response["body"]
    assert "review_comments" in body
