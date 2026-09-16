from pydantic import BaseModel


class PetCreate(BaseModel):
    name: str
    animal: str
    age: int


class Pet(PetCreate):
    id: int
