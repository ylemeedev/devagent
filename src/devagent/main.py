from devagent.agent import Agent
from devagent.tool import HelloTool, GoodbyeTool, UpperTool, ReverseTool, LengthTool, DivideTool

def run() -> None:

    tools = [
        HelloTool(),
        GoodbyeTool(),
        UpperTool(),
        ReverseTool(),
        LengthTool(),
        DivideTool(),
    ]

    agent = Agent(tools)
    
    print(agent.run_tool("hello", "Yves").success)
    print(agent.run_tool("goodbye", "Rémi"))
    print(agent.run_tool("upper", "bob"))
    print(agent.run_tool("reverse", "bonjour"))
    print(agent.run_tool("length", "ceci est un test"))
    print(agent.run_tool("divide", "9"))

    
if __name__ == "__main__":
    run()
