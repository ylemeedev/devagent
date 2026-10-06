import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "https://jsonplaceholder.typicode.com")
HTTP_TIMEOUT = int(os.getenv("DEVAGENT_HTTP_TIMEOUT", 10))