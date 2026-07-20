# app/repositories/driver_repository.py

from sqlalchemy.orm import Session

from app.models.master import DriverMaster
from app.repositories.base_repository import BaseRepository


class DriverRepository(
    BaseRepository[DriverMaster]
):

    def __init__(self, db: Session):

        super().__init__(DriverMaster, db)

    def get_by_dl_number(
        self,
        dl_number: str
    ) -> DriverMaster | None:

        return (
            self.db.query(DriverMaster)
            .filter(
                DriverMaster.dl_number == dl_number
            )
            .first()
        )

    def get_by_mobile(
        self,
        mobile_number: str
    ) -> DriverMaster | None:

        return (
            self.db.query(DriverMaster)
            .filter(
                DriverMaster.mobile_number
                == mobile_number
            )
            .first()
        )

    def update_driver(
        self,
        driver: DriverMaster,
        data: dict
    ):

        for key, value in data.items():

            setattr(
                driver,
                key,
                value
            )

        self.db.commit()
        self.db.refresh(driver)

        return driver
    
    def get_by_id(
    self,
    driver_id: int
    ) -> DriverMaster | None:
    
        return (
            self.db.query(DriverMaster)
            .filter(
                DriverMaster.driver_id == driver_id
            )
            .first()
        )
    
    def exists(
    self,
    driver_id: int
    ) -> bool:
    
        return (
            self.get_by_id(driver_id)
            is not None
        )
