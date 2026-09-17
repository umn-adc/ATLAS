from pydantic import BaseModel, field_validator
# BaseModel is the base class provided by pydantic
# Acts as the blueprint
# Creating a class with BaseModel means you are creating a custom data type

# This is a data body for the information that gets sent TO the backend
class PetCreate(BaseModel):
    name: str
    animal: str
    age: int

    @field_validator('age')
    @classmethod
    def age_must_be_positive(cls, v: int) -> int:
        if v < 0:
            raise ValueError("age must be positive")
        return v



class Pet(PetCreate):
    id: int
