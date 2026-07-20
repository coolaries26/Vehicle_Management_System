from app.models.inventory import PartMaster


def test_part_model_creation():

    part = PartMaster(
        part_code="P-001",
        part_name="Oil Filter",
        active_flag=True,
    )

    assert part.part_code == "P-001"
    assert part.part_name == "Oil Filter"
    assert part.active_flag is True