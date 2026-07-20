from app.schemas.vehicle import VehicleCreate


def test_vehicle_schema():

    payload = VehicleCreate(
        rc_number="KA01AB1234",
        engine_no="en-asdf23",
        chassis_no="CH-1232"
    )

    assert payload.rc_number == "KA01AB1234"