from fastapi import APIRouter, HTTPException, Query

from Workshop.schemas import Pet, PetCreate

router = APIRouter()

pets: dict[int, Pet] = {}
next_id = 1


def reset() -> None:
    global next_id
    pets.clear()
    next_id = 1


# BEGINNER: Create a pet
@router.post("/pets")
def create_pet(data: PetCreate) -> Pet:
    """
    TODO: Create a pet and return it.

    1. pet = Pet(id=next_id, name=data.name, animal=data.animal, age=data.age)
    2. pets[next_id] = pet
    3. next_id += 1
    4. return pet
    """
    global next_id
    # your code here


@router.get("/pets")
def list_pets() -> list[Pet]:
    return list(pets.values())


# MEDIUM: Get by ID + Delete (must handle 404)
@router.get("/pets/{pet_id}")
def get_pet(pet_id: int) -> Pet:
    """
    TODO: Return pet or 404.

    1. if pet_id not in pets: raise HTTPException(status_code=404, detail="Not found")
    2. return pets[pet_id]
    """
    # your code here


@router.delete("/pets/{pet_id}")
def delete_pet(pet_id: int) -> dict:
    """
    TODO: Delete pet or 404. Return {"deleted": pet_id}

    1. if pet_id not in pets: raise HTTPException(status_code=404, detail="Not found")
    2. del pets[pet_id]
    3. return {"deleted": pet_id}
    """
    # your code here


# HARD: Filter with query params + Pydantic field_validator
# Look up: https://docs.pydantic.dev/latest/concepts/validators/
@router.get("/pets/search/")
def search_pets(
    animal: str | None = Query(default=None),
    min_age: int | None = Query(default=None),
    max_age: int | None = Query(default=None),
) -> list[Pet]:
    """
    TODO: Filter pets by animal type and age range.

    1. Start with all pets: result = list(pets.values())
    2. If animal provided: filter to only that animal
    3. If min_age provided: filter to age >= min_age
    4. If max_age provided: filter to age <= max_age
    5. return result

    Example: /pets/search/?animal=dog&min_age=2
    """
    # your code here
