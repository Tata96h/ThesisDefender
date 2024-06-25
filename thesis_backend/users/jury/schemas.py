from pydantic import BaseModel, Field
from datetime import datetime

from users.profile.schemas import UserSchema


class CreateJurySchema(BaseModel):
    numero: str
    president_id: int
    examinateur_id: int
    rapporteur_id: int | None

class UpdateJurySchema(BaseModel):
    numero: str
    president_id: int | None
    examinateur_id: int | None
    rapporteur_id: int | None

    @property
    def is_empty(self): return not self.dict(exclude_none=True)


class JurySchema(BaseModel):
    id: int
    numero: str
    presiend_id: int
    examinateur_id: int
    rapporteur_id: int | None

    class Config:
        orm_mode = True

