#from app.models.inventory import PartMaster
from app.models.inventory import PartMaster
from app.schemas.part import PartCreate,PartUpdate,PartResponse
from app.services.exceptions import NotFoundException
from app.repositories.part_repository import PartRepository
#from app.repositories.complaint_repository import ComplaintRepository
#from app.repositories.vehicle_repository import VehicleRepository
#from app.repositories.inspection_repository import InspectionRepository

class PartService:
    def __init__(
        self,
        repository: PartRepository,
    ):
        self.repo = repository

    def create_part(
            self,
            payload: PartCreate,
            ) -> PartMaster:
        part = PartMaster(
            part_code=payload.part_code,
            part_name=payload.part_name,
        )
        return (
            self.repo.create(
                part
            )
        )
    
    def get_all_parts(self):
        return (
            self.repo.get_all()
        )

    def get_part_by_id(
        self,
        part_id: int,
    ) :
        part = (
            self.repo.get_by_id(
                part_id
            )
        )
        if not part:
            raise NotFoundException(
                f"Part "
                f"{part_id} "
                f"not found"
            )
        return part

    def update_part(
        self,
        part_id: int,
        payload: PartUpdate,
        user_id: int| None = None,
    ):

        update = (
            self.get_part_by_id(
                part_id
            )
        )

        update_data = (
            payload.model_dump(
                exclude_unset=True
            )
        )
        update_data["modified_by"] = user_id
        
        return (
            self.repo.update_part(
                update,
                update_data
            )
        )

    def delete_part(
        self,
        part_id: int,
    ) -> None:

        part = (
            self.get_part_by_id(
                part_id
            )
        )
        assert part is not None, (
            f"Part "
            f"{part_id} "
            f"not found"
        )
#        self.repo.delete_part(
#            part
#        )