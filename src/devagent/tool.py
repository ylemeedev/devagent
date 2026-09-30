from typing import Protocol, TypeVar
from dataclasses import dataclass
from pydantic import BaseModel, Field, ValidationError
import requests
import httpx

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
    b: int = Field(ne=0)

class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    test: int

class CreateUserTool:
    name = "create_user"
    input_model = CreateUserInput

    def execute(self, input: CreateUserInput) -> ToolResult:

        json = {
            "name": input.name,
            "age": input.age
        }

        try:
            response = requests.post(
                "https://jsonplaceholder.typicode.com/users",
                json = json
            )
            
            if (response.status_code == 201):
                user = UserResponse.model_validate(response.json())
                return ToolResult.ok(f"{user.name} est ajouté - Age: {user.age} - Id: {user.id}")

            return ToolResult.error(
                f"Erreur HTTP : {response.status_code}"
            )
        except ValidationError:
            return ToolResult.error("Données reçues non valide")
        except requests.RequestException:
            return ToolResult.error("Une erreur s'est produite lors de l'ajout de l'utilisateur")

class HelloTool:

    name = "hello"
    input_model  = HelloInput

    def execute(self, input: HelloInput) -> ToolResult:
        return ToolResult.ok(f"Bonjour {input.name} - Status : {input.active} - Description : {input.description}")

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

        print(input.model_json_schema())

        try:
            result = input.a / input.b
            return ToolResult.ok(str(result))
        except ZeroDivisionError:
            return ToolResult.error("Division impossible")

