import json
from .utils.dependencies import get_llm_service, get_repo_service, get_secrets_manager


def lambda_handler(event, context):
    try:
        message_payload = json.loads(event["Records"][0]["body"])
        return {"statusCode": 200, "body": json.dumps("Hello from Lambda!")}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps(f"Error: {str(e)}")}
