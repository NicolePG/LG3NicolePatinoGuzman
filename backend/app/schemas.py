from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class GroupBase(BaseModel):
    group: str = Field(min_length=2, max_length=120)
    is_active: bool = True


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    pass


class GroupOut(GroupBase):
    code: str
    people_count: int = 0
    model_config = ConfigDict(from_attributes=True)


class PersonBase(BaseModel):
    names: str = Field(min_length=2, max_length=120)
    last_names: str = Field(min_length=2, max_length=120)
    email: EmailStr
    cell_number: str = Field(min_length=5, max_length=30)
    address: str = Field(min_length=5, max_length=250)
    observations: Optional[str] = None
    photo_base64: Optional[str] = None
    is_active: bool = True
    group_code: str


class PersonCreate(PersonBase):
    pass


class PersonUpdate(PersonBase):
    pass


class PersonOut(PersonBase):
    code: str
    group_name: str
    model_config = ConfigDict(from_attributes=True)
