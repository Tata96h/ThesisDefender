from dataclasses import dataclass
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult
from sqlalchemy import select, insert, delete, update, and_
from sqlalchemy.orm import subqueryload, joinedload
from database import Base
from users.auth.models import Etudiant, Filiere, Users
from .schemas import CreateEtudiantSchema, EtudiantSchema, UpdateEtudiantSchema
from .exceptions import EtudiantExceptions
from .interfaces.repositories_interface import EtudiantRepositoriesInterface


@dataclass
class EtudiantRepositories(EtudiantRepositoriesInterface):
    session: AsyncSession
     


    async def get_etudiants(self, limit: int, offset: int):
        stmt = (
        select(Etudiant)
        .join(Etudiant.utilisateur)  # Join explicite avec la table utilisateur
        .options(joinedload(Etudiant.utilisateur))
        .filter(Users.is_active == True)  # Filtrer sur l'attribut is_active de l'utilisateur
        .order_by(Etudiant.created.desc())
        .limit(limit)
        .offset(offset)
    )
        result = await self.session.execute(stmt)
        etudiants = result.unique().scalars().all()
        return [EtudiantSchema.from_orm(etudiant) for etudiant in etudiants]

    
    async def create_etudiant(self, etudiant_data: CreateEtudiantSchema):
        values = {
            'matricule': etudiant_data['matricule'],
            'slug': etudiant_data['matricule'],
            'filiere_id': etudiant_data['filiere_id'],
            'utilisateur_id': etudiant_data['utilisateur_id']
        }
        stmt = insert(Etudiant).values(**values).returning(Etudiant)
        result = await self.session.execute(statement=stmt)
        await self.session.commit()
        return {'detail': f'Etudiant avec le matricule {etudiant_data["matricule"]} créé avec succès'}
        
    
    async def delete_etudiant(self, etudiant_slug: str):
        # Récupérer l'étudiant à supprimer
        etudiant = await self.get_etudiant(etudiant_slug)
        if not etudiant:
            raise EtudiantExceptions().etudiant_not_found
    
        # Récupérer l'utilisateur associé à l'étudiant
        utilisateur_id = etudiant.utilisateur_id
        print(utilisateur_id)
        # Mettre à jour le champ is_active de l'utilisateur à False
        stmt = update(Users).where(Users.id == utilisateur_id).values(is_active=False)
        await self.session.execute(stmt)

        # # Supprimer l'étudiant
        # stmt = delete(Etudiant).where(Etudiant.slug == etudiant_slug)
        result = await self.session.execute(statement=stmt)
        await self.session.commit()
        return {'detail': f'Etudiant avec le matricule {etudiant_slug} supprimé avec succès'}
    
    async def update_etudiant(self, etudiant_slug: str, updated_data: UpdateEtudiantSchema):
        await self.__check_etudiant(etudiant_slug=etudiant_slug)
        values = {**updated_data.dict(exclude_none=True)}
        if updated_data.matricule:
            values.update({'slug': updated_data.matricule})
            stmt = update(Etudiant).where(Etudiant.slug == etudiant_slug).values(**values).returning(Etudiant)
            
            result = await self.session.execute(statement=stmt)
        await self.session.commit()
        # return result.scalar_one()
        return {'detail': f'Etudiant avec le matricule {etudiant_slug} mise à jour'}
    
    async def get_etudiant(self, etudiant_slug: str):
        stmt = (
            select(Etudiant)
            .join(Etudiant.utilisateur)  # Join explicite avec la table utilisateur
            .options(joinedload(Etudiant.utilisateur))
            .filter(Users.is_active == True)  # Filtrer sur l'attribut is_active de l'utilisateur
            .order_by(Etudiant.created.desc())
            .where(
                and_(
                    Etudiant.slug == etudiant_slug

                )
            )
        )
        result: AsyncResult = await self.session.execute(stmt)
        return result.scalars().first()

    async def __check_etudiant(self, etudiant_slug: str):
        if not (etudiant := await self.get_etudiant(etudiant_slug=etudiant_slug)):
            raise EtudiantExceptions().etudiant_not_found
        return etudiant

    async def get_etudiants_by_filiere(self, filiere_id: int, limit: int, offset: int):
        stmt = (
            select(Etudiant)
            .join(Etudiant.utilisateur)
            .options(joinedload(Etudiant.utilisateur))
            .filter(Etudiant.filiere_id == filiere_id)
            .filter(Users.is_active == True)
            .order_by(Etudiant.created.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        etudiants = result.unique().scalars().all()
        return [EtudiantSchema.from_orm(etudiant) for etudiant in etudiants]
    
    

    async def get_filieres(self, limit: int, offset: int):
        stmt = select(Filiere) \
            .limit(limit) \
            .offset(offset)
        result = await self.session.execute(stmt)
        return result.scalars().all()

   