import pytest
from devagent.agent import Agent
from devagent.tool import UpperTool, DivideTool
from pydantic import ValidationError

@pytest.mark.asyncio
async def test_agent_run_known_tool():
    agent = Agent(tools=[UpperTool()])

    result = await agent.run_tool("upper", {"text": "ceci est un test"})

    assert result.success is True
    assert result.content == "CECI EST UN TEST"

@pytest.mark.asyncio
async def test_data_invalid():
    agent = Agent(tools=[DivideTool()])

    with pytest.raises(ValidationError):
        await agent.run_tool(
            "divide", 
            {
                "a": 10, 
                "b": 0
            }
        )

@pytest.mark.asyncio
async def test_agent_invalid_data():

    agent = Agent(tools=[UpperTool()])

    with pytest.raises(ValidationError):
        await agent.run_tool("upper", {})

@pytest.mark.asyncio
async def test_agent_unknown():

    agent = Agent(tools=[UpperTool()])

    with pytest.raises(ValueError, match="Outil inconnu"):
        await agent.run_tool("test", {})


