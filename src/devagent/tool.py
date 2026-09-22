from typing import Protocol
from dataclasses import dataclass

@dataclass
class ToolResult:
    success: bool
    content: str

    @classmethod
    def ok(cls, content: str) -> "ToolResult":
        return cls(
            success=True,
            content=content
        )

    @classmethod
    def error(cls, content: str) -> "ToolResult":
        return cls(
            success=False,
            content=content
        )

class Tool(Protocol):

    name: str

    def execute(self, input: str) -> ToolResult:
        ...

class HelloTool:

    name = "hello"

    def execute(self, input: str) -> ToolResult:
        return ToolResult.ok(f"Bonjour {input}")

class GoodbyeTool:

    name = "goodbye"

    def execute(self, input: str) -> ToolResult:
        return ToolResult.ok(f"Au revoir {input}")

class UpperTool:

    name = "upper"

    def execute(self, input: str) -> ToolResult:
        return ToolResult.ok(content=input.upper())

class ReverseTool:

    name = "reverse"

    def execute(self, input: str) -> ToolResult:
        return ToolResult.ok(input[::-1])

class LengthTool:

    name = "length"

    def execute(self, input: str) -> ToolResult:
        return ToolResult.ok(str(len(input)))

