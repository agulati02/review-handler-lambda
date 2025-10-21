import os
from dotenv import load_dotenv


ENV = os.getenv("ENV", "local")
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'resources', f'.env.{ENV}'))

LLM_API_KEY_PATH = os.getenv("LLM_API_KEY_PATH")
GITHUB_PRIVATE_KEY_PATH = os.getenv("GITHUB_PRIVATE_KEY_PATH")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME", "ap-southeast-2")

CLIENT_ID = 'Iv23liHKhbBXLoJvAoC7'
JWT_ALGORITHM = 'RS256'

LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")
LLM_MAX_RESPONSE_TOKENS = int(os.getenv("LLM_MAX_RESPONSE_TOKENS", "2048"))
