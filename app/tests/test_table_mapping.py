from app.db.base import Base

def test_table_mapping():
    for name in Base.metadata.tables:
        print(name)

    assert "master.vehicle_master" in Base.metadata.tables
    assert "master.driver_master" in Base.metadata.tables
    assert "maintenance.vehicle_complaint" in Base.metadata.tables