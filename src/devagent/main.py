from devagent.agent import Agent
from devagent.tool import HelloTool, GoodbyeTool, UpperTool, ReverseTool, LengthTool, DivideTool, DivideInput

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
    
    print(agent.run_tool("hello", {"name": "Yves"}))
    print(agent.run_tool("goodbye", {"name": "Rémi"}))
    print(agent.run_tool("upper", {"text": "bob"}))
    print(agent.run_tool("reverse", {"text": "bonjour"}))
    print(agent.run_tool("length", {"text": "ceci est un test"}))
    print(agent.run_tool("divide", {"a": 9, "b": 4}))
    
if __name__ == "__main__":
    run()
