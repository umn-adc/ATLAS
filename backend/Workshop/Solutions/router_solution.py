from fastapi import APIRouter, HTTPException, Query

from Workshop.schemas import Pet, PetCreate

router = APIRouter()

pets: dict[int, Pet] = {}
next_id = 1


def reset() -> None:
    global next_id
    pets.clear()
    next_id = 1


# BEGINNER
@router.post("/pets")
def create_pet(data: PetCreate) -> Pet:
    global next_id
    pet = Pet(id=next_id, name=data.name, animal=data.animal, age=data.age)
    pets[next_id] = pet
    next_id += 1
    return pet


@router.get("/pets")
def list_pets() -> list[Pet]:
    return list(pets.values())


# MEDIUM
@router.get("/pets/{pet_id}")
def get_pet(pet_id: int) -> Pet:
    if pet_id not in pets:
        raise HTTPException(status_code=404, detail="Not found")
    return pets[pet_id]


@router.delete("/pets/{pet_id}")
def delete_pet(pet_id: int) -> dict:
    if pet_id not in pets:
        raise HTTPException(status_code=404, detail="Not found")
    del pets[pet_id]
    return {"deleted": pet_id}


# HARD
@router.get("/pets/search/")
def search_pets(
    animal: str | None = Query(default=None),
    min_age: int | None = Query(default=None),
    max_age: int | None = Query(default=None),
) -> list[Pet]:
    result = list(pets.values())
    if animal:
        result = [p for p in result if p.animal == animal]
    if min_age:
        result = [p for p in result if p.age >= min_age]
    if max_age:
        result = [p for p in result if p.age <= max_age]
    return result
