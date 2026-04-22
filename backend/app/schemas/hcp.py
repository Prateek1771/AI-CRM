from pydantic import BaseModel
from datetime import datetime


class HCPBase(BaseModel):
    name: str
    specialty: str | None = None
    territory: str | None = None
    email: str | None = None
    phone: str | None = None


class HCPCreate(HCPBase):
    pass


class HCPRead(HCPBase):
    id: str
    created_at: datetime

    model_config = {"from_attributes": True}
