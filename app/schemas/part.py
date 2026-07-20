from pydantic import BaseModel  #type: ignore
from pydantic import ConfigDict #type: ignore


class PartCreate(BaseModel):

    part_code: str | None = None

    part_name: str


class PartUpdate(BaseModel):

    part_code: str | None = None

    part_name: str | None = None

    active_flag: bool | None = None


class PartResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    part_id: int

    part_code: str | None = None

    part_name: str | None = None

    active_flag: bool | None = True