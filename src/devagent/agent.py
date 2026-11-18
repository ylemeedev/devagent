from devagent.tool import Tool,ToolResult
from pydantic import BaseModel
from devagent.exceptions import ToolNotFoundError

class Agent:

    total = 0

    def __init__(self, tools: list[Tool]):
        self.tools = {tool.name: tool for tool in tools}

    async def run_tool(self, name: str, data) -> ToolResult:
        tool = self.tools.get(name)

        if tool is None:
            raise ToolNotFoundError(f"Outil inconnu : {name}")

        if issubclass(tool.input_model, BaseModel):
            input = tool.input_model.model_validate(data)
        else:
            input = tool.input_model(data)

        return await tool.execute(input)
