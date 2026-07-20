from app.models.inventory import PartMaster
from app.repositories.part_repository import PartRepository
import random
def rand_n_digits(n: int) -> int:
    return random.randint(
        10**(n-1),
        10**n - 1
    )


def test_create_part(db):

    part = PartMaster(
        part_code=f"PART-{rand_n_digits(6)}",
        part_name="Engine Oil",
    )

    repo = PartRepository(db)

    result = repo.create(part)

    assert result is not None
    assert result.part_id is not None
    assert result.part_name == "Engine Oil"


def test_get_part_by_id(db):

    part = PartMaster(
        part_code=f"PART-{rand_n_digits(6)}",
        part_name="Air Filter",
    )

    db.add(part)
    db.commit()
    db.refresh(part)

    repo = PartRepository(db)

    result = repo.get_by_id(
        part.part_id
    )

    assert result is not None
    assert result.part_id == part.part_id


def test_get_all_parts(db):

    db.add(
        PartMaster(
            part_code=f"PART-{rand_n_digits(6)}",
            part_name="Brake Pad",
        )
    )

    db.commit()

    repo = PartRepository(db)

    result = repo.get_all()

    assert result is not None
    assert isinstance(result, list)
    assert len(result) > 0