from devagent.tool import Tool,ToolResult

class Agent:

    def __init__(self, tools: list[Tool]):
        self.tools = {tool.name: tool for tool in tools}

    def run_tool(self, name: str, value: str) -> ToolResult:
        tool = self.tools.get(name)

        if tool is None:
            raise ValueError(f"Outil inconnu : {name}")

        return tool.execute(value)