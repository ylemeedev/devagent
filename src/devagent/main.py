from devagent.agent import Agent
from devagent.tool import HelloTool, GoodbyeTool, UpperTool, ReverseTool, LengthTool, DivideTool, CreateUserTool
import httpx
import asyncio

async def getUser(id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://jsonplaceholder.typicode.com/users/{id}")
        return response.json()


async def main():
    users_id = [1, 4, 9]
    tasks = [
        getUser(user_id)
        for user_id in users_id
    ]
    user = await asyncio.gather(*tasks)
    print(user)


def run() -> None:

    tools = [
        HelloTool(),
        GoodbyeTool(),
        UpperTool(),
        ReverseTool(),
        LengthTool(),
        DivideTool(),
        CreateUserTool()
    ]

    agent = Agent(tools)
    
    """ print(agent.run_tool("hello", {"name": "Yves"}))
    print(agent.run_tool("goodbye", {"name": "Rémi"}))
    print(agent.run_tool("upper", {"text": "bob"}))
    print(agent.run_tool("reverse", {"text": "bonjour"}))
    print(agent.run_tool("length", {"text": "ceci est un test"}))
    print(agent.run_tool("divide", {"a": 9, "b": 4})) """

    """print(agent.run_tool("create_user", {"name": "Rémi", "age": 25}))"""

    print("TEST")
    
if __name__ == "__main__":
    asyncio.run(main())
    run()
