from app.models.master import DriverMaster

from app.repositories.driver_repository import (
    DriverRepository,
)

from app.schemas.driver import (
    DriverCreate,
    DriverUpdate,
)

from app.services.exceptions import (
    DuplicateRecordException,
    NotFoundException,
)


class DriverService:

    def __init__(
        self,
        driver_repository: DriverRepository
    ):

        self.driver_repo = (
            driver_repository
        )

    def create_driver(
        self,
        payload: DriverCreate,
        user_id: int| None = None,
    ) -> DriverMaster:

        if payload.dl_number:

            existing_driver = (
                self.driver_repo
                .get_by_dl_number(
                    payload.dl_number
                )
            )

            if existing_driver:

                raise (
                    DuplicateRecordException(
                        "Driver already exists"
                    )
                )

        driver = DriverMaster(
            driver_name=payload.driver_name,
            mobile_number=payload.mobile_number,
            dl_number=payload.dl_number,
            dl_expiry_date=payload.dl_expiry_date,
            modified_by = user_id
        )

        return (
            self.driver_repo.create(
                driver
            )
        )

    def get_driver(
        self,
        driver_id: int
    ):

        driver = (
            self.driver_repo
            .get_by_id(driver_id)
        )

        if not driver:

            raise NotFoundException(
                f"Driver "
                f"{driver_id}"
                f" not found"
            )

        return driver

    def get_all_drivers(self):

        return (
            self.driver_repo.get_all()
        )

    def update_driver(
        self,
        driver_id: int,
        payload: DriverUpdate,
        user_id: int| None = None,
    ):

        driver = (
            self.get_driver(
                driver_id
            )
        )

        update_data = (
            payload.model_dump(
                exclude_unset=True
            )
        )
        update_data["modified_by"] = user_id
        
        return (
            self.driver_repo
            .update_driver(
                driver,
                update_data
            )
        )

    def delete_driver(
        self,
        driver_id: int
    ):

        driver = (
            self.get_driver(
                driver_id
            )
        )

        self.driver_repo.delete(
            driver
        )