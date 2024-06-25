from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult
from sqlalchemy import select, insert, delete, update,  and_
from sqlalchemy.orm import subqueryload, joinedload

from users.auth.models import Departement, Enseignant, Etudiant, Filiere, Grade, Users
from .schemas import CreateEnseignantSchema, EnseignantSchema, UpdateEnseignantSchema
from .exceptions import EnseignantExceptions
from .interfaces.repositories_interface import EnseignantRepositoriesInterface


@dataclass
class EnseignantRepositories(EnseignantRepositoriesInterface):
    session: AsyncSession
    
    async def get_enseignants(self, limit: int, offset: int):
        stmt = (
        select(Enseignant)
        .join(Enseignant.utilisateur)  
        .options(joinedload(Enseignant.utilisateur))
        .filter(Users.is_active == True) 
        .order_by(Enseignant.created.desc())
        .limit(limit)
        .offset(offset)
    )
        result = await self.session.execute(stmt)
        enseignants = result.unique().scalars().all()
        return [EnseignantSchema.from_orm(enseignant) for enseignant in enseignants]

    
    async def create_enseignant(self, enseignant_data: CreateEnseignantSchema):
        values = {
            'matricule': enseignant_data['matricule'],
            'slug': enseignant_data['matricule'],
            'grade_id': enseignant_data['grade_id'],
            'specialite': enseignant_data['specialite'],
            'departement_id': enseignant_data['departement_id'],
            'utilisateur_id': enseignant_data['utilisateur_id']
        }
        stmt = insert(Enseignant).values(**values).returning(Enseignant)
        result = await self.session.execute(statement=stmt)
        await self.session.commit()
        return {'detail': f'Enseignant avec le matricule {enseignant_data["matricule"]} créé avec succès'}
    
    async def delete_enseignant(self, enseignant_slug: str):
        
        enseignant = await self.get_enseignant(enseignant_slug)
        if not enseignant:
            raise EnseignantExceptions().enseignant_not_found
    
        # Récupérer l'utilisateur associé à l'étudiant
        utilisateur_id = enseignant.utilisateur_id
        print(utilisateur_id)
        # Mettre à jour le champ is_active de l'utilisateur à False
        stmt = update(Users).where(Users.id == utilisateur_id).values(is_active=False)
        await self.session.execute(stmt)

        # Supprimer l'étudiant
        # stmt = delete(Enseignant).where(Enseignant.slug == enseignant_slug)
        result = await self.session.execute(statement=stmt)
        await self.session.commit()
        # return result.rowcount
        return {'detail': f'Enseignant avec le matricule {enseignant_slug} supprimé avec succès'}

    async def update_enseignant(self, enseignant_slug: str, updated_data: UpdateEnseignantSchema):
        await self.__check_enseignant(enseignant_slug=enseignant_slug)
        values = {**updated_data.dict(exclude_none=True)}
        if updated_data.matricule:
            values.update({'slug': updated_data.matricule})
            stmt = update(Enseignant).where(Enseignant.slug == enseignant_slug).values(**values).returning(Enseignant)
            result = await self.session.execute(statement=stmt)
        await self.session.commit()
        return {'detail': f'Enseignant avec le matricule {enseignant_slug} mise à jour'}
    
    async def get_enseignant(self, enseignant_slug: str):
        stmt = (
            select(Enseignant)
            .join(Enseignant.utilisateur)  # Join explicite avec la table utilisateur
            .options(joinedload(Enseignant.utilisateur))
            .filter(Users.is_active == True)  # Filtrer sur l'attribut is_active de l'utilisateur
            .order_by(Enseignant.created.desc())
            .where(
                and_(
                    Enseignant.slug == enseignant_slug

                )
            )
        )
        result: AsyncResult = await self.session.execute(stmt)
        return result.scalars().first()


    async def __check_enseignant(self, enseignant_slug: str):
        if not (enseignant := await self.get_enseignant(enseignant_slug=enseignant_slug)):
            raise EnseignantExceptions().enseignant_not_found
        return enseignant

    async def get_enseignants_by_departement(self, departement_id: int, limit: int, offset: int):
        stmt = (
            select(Enseignant)
            .join(Enseignant.utilisateur)
            .options(joinedload(Enseignant.utilisateur))
            .filter(Enseignant.departement_id == departement_id)
            .filter(Users.is_active == True)
            .order_by(Enseignant.created.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        enseignants = result.unique().scalars().all()
        return [EnseignantSchema.from_orm(enseignant) for enseignant in enseignants]
    
    
    async def get_departements(self):
        result = await self.session.execute(select(Departement))
        return result.scalars().all()
    
    async def get_grades(self):
        result = await self.session.execute(select(Grade))
        return result.scalars().all()
    
    async def get_filieres_by_departement(self, departement_id: int):
        stmt = select(Filiere).filter(Filiere.departement_id == departement_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()