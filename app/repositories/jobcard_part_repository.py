# app/repositories/jobcard_part_repository.py

from typing import Generic
from typing import TypeVar

from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.maintenance import JobCardPart

from sqlalchemy.orm import Session

from app.models.maintenance import (
    JobCardPart,
)

from app.repositories.base_repository import (
    BaseRepository,
)


class JobCardPartRepository(
    BaseRepository[JobCardPart]
):

    def __init__(
        self,
        db: Session,
    ):
        super().__init__(
            JobCardPart,
            db,
        )

    def get_by_id(
        self,
        jobcard_part_id: int,
    ) -> JobCardPart | None:

        return (
            self.db.query(JobCardPart)
            .filter(
                JobCardPart.id
                == jobcard_part_id
            )
            .first()
        )

    def get_by_jobcard(
        self,
        job_card_id: int,
    ) -> list:
        return (
            self.db.query(JobCardPart)
            .filter(
                JobCardPart.job_card_id
                == job_card_id
            )
            .all()
        )

    def get_by_part(
        self,
        part_id: int,
    ) -> list:
        return (
            self.db.query(JobCardPart)
            .filter(
                JobCardPart.part_id
                == part_id
            )
            .all()
        )

    def update_jobcard_part(
        self,
        jobcard_part: JobCardPart,
        data: dict,
    ) -> JobCardPart:

        for key, value in data.items():

            setattr(
                jobcard_part,
                key,
                value,
            )

        self.db.commit()

        self.db.refresh(
            jobcard_part
        )

        return jobcard_part

    def delete_jobcard_part(
        self,
        jobcard_part: JobCardPart,
    ) -> None:

        self.db.delete(
            jobcard_part
        )

        self.db.commit()

    def exists(
    self,
    part_id: int
    ) -> bool:
    
        return (
            self.get_by_id(part_id)
            is not None
        )