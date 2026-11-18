from typing import Protocol, TypeVar
from dataclasses import dataclass
from pydantic import BaseModel, Field, ValidationError, field_validator
from devagent.config import API_URL, HTTP_TIMEOUT
import httpx
import logging
from pathlib import Path


cert_path = Path(__file__).resolve().parents[2] / "certs" / "jsonplaceholder-typicode-com.pem"

logger = logging.getLogger(__name__)

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

    async def execute(self, input: T) -> ToolResult:
        ...

class CreateUserInput(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(gt=0)

class HelloInput(BaseModel):
    name: str = Field(min_length=2)
    active: bool = True
    description: str | None = None

class GoodbyeInput(BaseModel):
    name: str = Field(min_length=2)

class UpperInput(BaseModel):
    text: str = Field(min_length=2)

class ReverseInput(BaseModel):
    text: str = Field(min_length=2)

class LengthInput(BaseModel):
    text: str = Field(min_length=2)

class DivideInput(BaseModel):
    a: int
    b: int = Field(json_schema_extra={"ne": 2})

    @field_validator("b")
    @classmethod
    def b_must_not_be_zero(cls, value: int) -> int:
        if value == 0:
            raise ValueError("b ne doit pas être égal à zéro")

        return value

class UserResponse(BaseModel):
    id: int
    name: str
    age: int

class GetUserInput(BaseModel):
    id: int = Field(gt=0)

class GetUserTool:
    name = "get_user"
    input_model = GetUserInput

    async def execute(self, input: GetUserInput) -> ToolResult:
        try:
            async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, verify=str(cert_path)) as client:
                response = await client.get(f"{API_URL}/users/{input.id}")

            if (response.status_code == 200):
                logger.info("Utilisateur récupéré")
                return ToolResult.ok(response.json())

            logger.error("User introuvable")
            return ToolResult.error("User introuvable")
        except httpx.RequestError as error:
            logger.error(f"Erreur HTTPX : {error}")
            return ToolResult.error("Une erreur s'est produite")
        except httpx.TimeoutException as error:
            logger.error(f"Une erreur s'est produite - {error}")


class CreateUserTool:
    name = "create_user"
    input_model = CreateUserInput

    async def execute(self, input: CreateUserInput) -> ToolResult:

        json = {
            "name": "Rémi",
            "age": input.age
        }

        try:
            async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, verify=str(cert_path)) as client:
                response = await client.post(
                    f"{API_URL}/users",
                    json = json
                )
            
            if (response.status_code == 201):
                user = UserResponse.model_validate(response.json())
                logger.info(f"Utilisateur {user.name} sauvegardé")
                return ToolResult.ok(f"{user.name} est ajouté - Age: {user.age} - Id: {user.id}")

            logger.error("Une erreur s'est produite lors de la sauvegarde")
            return ToolResult.error(
                f"Erreur HTTP : {response.status_code}"
            )
        except ValidationError as error:
            logger.error(f"Erreur de données - {error}")
            return ToolResult.error("Données reçues non valide")
        except httpx.RequestError as error:
            logger.error(f"Erreur de requête - {error}")
            return ToolResult.error("Une erreur s'est produite lors de l'ajout de l'utilisateur")
        except httpx.TimeoutException as error:
            logger.error(f"Requête expiré - {error}")
            return ToolResult.error("La requête a expiré")

class HelloTool:

    name = "hello"
    input_model  = HelloInput

    async def execute(self, input: HelloInput) -> ToolResult:
        return ToolResult.ok(f"Bonjour {input.name} - Status : {input.active} - Description : {input.description}")

class GoodbyeTool:

    name = "goodbye"
    input_model  = GoodbyeInput

    async def execute(self, input: GoodbyeInput) -> ToolResult:
        return ToolResult.ok(f"Au revoir {input.name}")

class UpperTool:

    name = "upper"
    input_model  = UpperInput

    async def execute(self, input: UpperInput) -> ToolResult:
        return ToolResult.ok(content=input.text.upper())

class ReverseTool:

    name = "reverse"
    input_model  = ReverseInput

    async def execute(self, input: ReverseInput) -> ToolResult:
        return ToolResult.ok(input.text[::-1])

class LengthTool:

    name = "length"
    input_model  = LengthInput

    async def execute(self, input: LengthInput) -> ToolResult:
        return ToolResult.ok(str(len(input.text)))

class DivideTool:

    name = "divide"
    input_model  = DivideInput

    async def execute(self, input: DivideInput) -> ToolResult:
        try:
            result = input.a / input.b
            return ToolResult.ok(str(result))
        except ZeroDivisionError:
            return ToolResult.error("Division impossible")


class Divide:

    def execute(self):
        try:
            return 10 / 0;
        except ZeroDivisionError:
            return "Division par zéro impossible"




