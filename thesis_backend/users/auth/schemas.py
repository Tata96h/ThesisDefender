from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class BaseUserAccountSchema(BaseModel):
    username: str = Field(max_length=200)


class CreateUserSchema(BaseUserAccountSchema):
    password: Optional[str] = Field(None)
    nom: str
    prenoms: str
    role_id: int
    reset_token: datetime
    token_expires: str


class CreateLoginSchema(BaseModel):
    username: str = Field(max_length=200)
    password: str

class ResetPasswordSchema(BaseModel):
    token: str
    new_password: str

    class Config:
        from_attributes = True
        
class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    user_info: dict

    class Config:
        from_attributes = True

# Exemple de schéma pour les informations utilisateur
class UserInfoSchema(BaseModel):
    utilisateur_id: int
    nom: str
    prenoms: str
    role_id: int
    is_admin: str

    class Config:
        from_attributes = True

class UsersSchema(BaseModel):
    id: int
    username: str
    nom: str
    prenoms: str
    bio: Optional[str]
    role_id: int
    is_active: bool
    is_admin: bool
    # created: str

    class Config:
        from_attributes = True

