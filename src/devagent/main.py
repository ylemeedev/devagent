from devagent.agent import Agent
from devagent.tool import UpperTool, GetUserTool, CreateUserTool, Divide
import asyncio
import httpx
from pathlib import Path
import json
import logging
from devagent.logging_config import configure_logging

configure_logging()

logger = logging.getLogger(__name__)

cert_path = Path(__file__).resolve().parents[2] / "certs" / "jsonplaceholder-typicode-com.pem"

async def main():

    users_id = [1, 4, 9]

    async with httpx.AsyncClient(verify=str(cert_path)) as client:

        users = []

        tasks = [
            getUser(client, user_id)
            for user_id in users_id
        ]

        users = await asyncio.gather(*tasks)

        """ for user in users:
            print(user) """

async def getUser(client: httpx.AsyncClient, id: int):
    response = await client.get(
        f"https://jsonplaceholder.typicode.com/users/{id}"
    )

    return response.json()


async def main_test():
    ...

def writeFile(file_path):

    user = {
        "id": 1,
        "name": "Yves Lemée",
        "active": True
    }

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(json.dumps(user, ensure_ascii=False, indent=2))


def loadFile(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
        
        user = json.loads(content)
        print(user)
        return True

    except FileNotFoundError:
        logger.error("Le fichier n'existe pas")
        return False

    except json.JSONDecodeError as error:
        logger.error(f"JSON invalide : {error}")
        return False

def divide():
    divide = Divide()
    print(divide.execute())

if __name__ == "__main__":
    """ asyncio.run(main_test()) """
    """ asyncio.run(main()) """
    """ writeFile("mon_fichier.json")
    loadFile("mon_fichier.json") """
    divide()
