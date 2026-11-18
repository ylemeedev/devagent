import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "https://jsonplaceholder.typicode.com")

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("La variable API_KEY est obligatoire")

try:
    HTTP_TIMEOUT = int(os.getenv("HTTP_TIMEOUT", 10))
except ValueError:
    raise ValueError("DEVAGENT_HTTP_TIMEOUT doit être un nombre entier")

if HTTP_TIMEOUT <= 0:
    raise ValueError("DEVAGENT_HTTP_TIMEOUT doit être supérieur à zéro")

