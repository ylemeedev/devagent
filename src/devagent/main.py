from devagent.agent import Agent
from devagent.tool import UpperTool, GetUserTool, CreateUserTool
import asyncio
import httpx

async def main():
    users_id = [1, 4, 9]

    async with httpx.AsyncClient() as client:

        users = []

        tasks = [
            getUser(client, user_id)
            for user_id in users_id
        ]

        users = await asyncio.gather(*tasks)

        for user in users:
            print(user)

async def getUser(client: httpx.AsyncClient, id: int):
    response = await client.get(
        f"https://jsonplaceholder.typicode.com/users/{id}"
    )

    return response.json()


async def main_test():

    tools = [
        UpperTool(),
        GetUserTool(),
        CreateUserTool()
    ]

    agent = Agent(tools)

    results = await asyncio.gather(
        agent.run_tool("get_user", {"id": 1}),
        agent.run_tool("create_user", {
            "name": "Yves",
            "age": 25,
        }),
        agent.run_tool("upper", {"text": "ceci est un test"})
    )

    """ print(results) """

if __name__ == "__main__":
    asyncio.run(main_test())
    """ asyncio.run(main()) """