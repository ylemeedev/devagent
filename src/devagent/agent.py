from devagent.tool import Tool,ToolResult
from pydantic import BaseModel

class Agent:

    def __init__(self, tools: list[Tool]):
        self.tools = {tool.name: tool for tool in tools}

    def run_tool(self, name: str, data) -> ToolResult:
        tool = self.tools.get(name)

        if tool is None:
            raise ValueError(f"Outil inconnu : {name}")

        if issubclass(tool.input_model, BaseModel):
            input = tool.input_model.model_validate(data)
        else:
            input = tool.input_model(data)

        return tool.execute(input)