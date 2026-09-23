from typing import Protocol, TypeVar
from dataclasses import dataclass
from pydantic import BaseModel

T = TypeVar("T")

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

class Tool(Protocol[T]):

    name: str
    input_model: type[T]

    def execute(self, input: T) -> ToolResult:
        ...

class HelloInput(BaseModel):
    name: str

class GoodbyeInput(BaseModel):
    name: str

class UpperInput(BaseModel):
    text: str

class ReverseInput(BaseModel):
    text: str

class LengthInput(BaseModel):
    text: str

class DivideInput(BaseModel):
    a: int
    b: int

class HelloTool:

    name = "hello"
    input_model  = HelloInput

    def execute(self, input: HelloInput) -> ToolResult:
        return ToolResult.ok(f"Bonjour {input.name}")

class GoodbyeTool:

    name = "goodbye"
    input_model  = GoodbyeInput

    def execute(self, input: GoodbyeInput) -> ToolResult:
        return ToolResult.ok(f"Au revoir {input.name}")

class UpperTool:

    name = "upper"
    input_model  = UpperInput

    def execute(self, input: UpperInput) -> ToolResult:
        return ToolResult.ok(content=input.text.upper())

class ReverseTool:

    name = "reverse"
    input_model  = ReverseInput

    def execute(self, input: ReverseInput) -> ToolResult:
        return ToolResult.ok(input.text[::-1])

class LengthTool:

    name = "length"
    input_model  = LengthInput

    def execute(self, input: LengthInput) -> ToolResult:
        return ToolResult.ok(str(len(input.text)))

class DivideTool:

    name = "divide"
    input_model  = DivideInput

    def execute(self, input: DivideInput) -> ToolResult:
        try:
            result = input.a / input.b
            return ToolResult.ok(str(result))
        except ZeroDivisionError:
            return ToolResult.error("Division impossible")

