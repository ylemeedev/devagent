from devagent.agent import Agent
from devagent.tool import HelloTool, GoodbyeTool, UpperTool, ReverseTool, LengthTool, ToolResult

def run() -> None:

    tools = [
        HelloTool(),
        GoodbyeTool(),
        UpperTool(),
        ReverseTool(),
        LengthTool()
    ]

    agent = Agent(tools)
    
    print(agent.run_tool("hello", "Yves").success)
    print(agent.run_tool("goodbye", "Rémi"))
    print(agent.run_tool("upper", "bob"))
    print(agent.run_tool("reverse", "bonjour"))
    print(agent.run_tool("length", "ceci est un test"))

    
if __name__ == "__main__":
    run()
