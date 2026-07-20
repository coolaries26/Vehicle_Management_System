from app.schemas.part import (
    PartCreate,
)

from app.services.part_service import (
    PartService,
)

from app.repositories.part_repository import (
    PartRepository,
)

import random
def rand_n_digits(n: int) -> int:
    return random.randint(
        10**(n-1),
        10**n - 1
    )

def test_create_part_service(db):
    repo = PartRepository(db)
    service = PartService(repo)
    payload = PartCreate(
        part_code=f"PART-{rand_n_digits(6)}",
        part_name="Engine Oil",
    )
    result = service.create_part(
        payload
    )
    assert result is not None
    assert result.part_name == "Engine Oil"


def test_get_all_parts_service(db):
    repo = PartRepository(db)
    service = PartService(repo)
    result = service.get_all_parts()
    assert result is not None
    assert isinstance(result, list)

def test_get_part_by_id_service(db):
    repo = PartRepository(db)
    service = PartService(repo)
    result = service.get_part_by_id(part_id=1)
    assert result is not None
#    assert isinstance(result, dict)

def test_update_part_service(db):
    repo = PartRepository(db)
    service = PartService(repo)
    payload = PartCreate(
        part_code=f"PART-{rand_n_digits(6)}",
        part_name="Updated Engine Oil",
    )
    result = service.update_part(
        part_id=1,
        payload=payload
    )
    assert result is not None
    assert result.part_name == "Updated Engine Oil"

def test_delete_part_service(db):
    repo = PartRepository(db)
    service = PartService(repo)
    payload=PartCreate(
            part_code=f"PART-{rand_n_digits(6)}",
            part_name="Deleted Part",
            active_flag=True,
        )

    result = service.update_part(
        part_id=1,
        payload=payload
        )
    assert result is not None