from devagent.tool import ToolResult, UpperTool, UpperInput, DivideInput
import pytest
from pydantic import ValidationError

def test_tool_ok():
    result = ToolResult.ok("Bonjour")

    assert result.success is True
    assert result.content == "Bonjour"

def test_tool_error():
    result = ToolResult.error("Une erreur est survenue")

    assert result.success is False
    assert result.content == "Une erreur est survenue"

@pytest.mark.asyncio
async def test_upper_tool():
    tool = UpperTool()

    value = "un test"

    result = await tool.execute(
        UpperInput(text=value)
    )

    assert result.success is True
    assert result.content ==  value.upper()

def test_upper_input_invalid():
    with pytest.raises(ValidationError):
        UpperInput(text="A")

def test_divide_input_invalid():
    with pytest.raises(ValidationError):
        DivideInput(a=5, b=0)