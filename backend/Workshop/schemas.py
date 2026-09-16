from pydantic import BaseModel
# BaseModel is the base class provided by pydantic
# Acts as the blueprint
# Creating a class with BaseModel means you are creating a custom data type

# This is a data body for the information that gets sent TO the backend
class PetCreate(BaseModel):
    name: str
    animal: str
    age: int


class Pet(PetCreate):
    id: int
