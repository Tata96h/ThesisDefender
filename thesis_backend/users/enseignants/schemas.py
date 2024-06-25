from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from users.auth.schemas import UsersSchema
from users.profile.schemas import UserSchema


class CreateEnseignantSchema(BaseModel):
    username: str
    email: str
    password: str
    nom: str
    prenoms: str
    matricule: str
    grade_id: int
    specialite: str
    departement_id: int 
    
    


class UpdateEnseignantSchema(BaseModel):
    matricule: str | None = Field(None, max_length=200)
    grade: str | None = Field(None, max_length=255)
    specialite: str | None = Field(None, max_length=255)

    @property
    def is_empty(self): return not self.dict(exclude_none=True)


# class EnseignantSchema(BaseModel):
#     id: int
#     slug: str | None
#     matricule: str
#     grade_id: int
#     specialite: str
#     departement_id: int
#     created: datetime


#     class Config:
#         from_attributes = True

class EnseignantSchema(BaseModel):
    id: int
    matricule: str
    slug: Optional[str]
    utilisateur_id: int
    grade_id: int
    specialite: str
    departement_id: int
    created: datetime
    utilisateur: UsersSchema

    class Config:
        from_attributes = True

class DepartementSchema(BaseModel):
    id: int
    nom: str 
    
    class Config:
        from_attributes = True

class GradeSchema(BaseModel):
    id: int
    nom: str 
    
    class Config:
        from_attributes = True

        