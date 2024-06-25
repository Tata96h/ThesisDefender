from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime

from users.auth.schemas import UsersSchema
from users.profile.schemas import UserSchema


class CreateEtudiantSchema(BaseModel):
    username: str
    password: Optional[str] = Field(None)
    nom: str
    prenoms: str
    matricule: str
    filiere_id: int
    
    

class UpdateEtudiantSchema(BaseModel):
    matricule: str 
    filiere_id: int | None
    # nom: str  = Field(None, max_length=200)
    # prenoms: str = Field(None, max_length=200)
   

    @property
    def is_empty(self): return not self.dict(exclude_none=True)


class EtudiantSchema(BaseModel):
    id: int
    matricule: str
    slug: Optional[str]
    utilisateur_id: int
    filiere_id: int
    created: datetime
    utilisateur: UsersSchema

    class Config:
        from_attributes = True


        
class FiliereSchema(BaseModel):
    id: int
    nom: str
    departement_id: int

    class Config:
        from_attributes = True


class EmailSchema(BaseModel):
    username: List[EmailStr]

    class Config:
        from_attributes = True
    