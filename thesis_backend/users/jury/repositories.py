from dataclasses import dataclass
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult
from sqlalchemy import select, insert, delete, update, and_
from sqlalchemy.orm import subqueryload
from database import Base
from users.auth.models import Jury
from .schemas import CreateJurySchema, JurySchema, UpdateJurySchema
from .exceptions import JuryExceptions
from .interfaces.repositories_interface import JuryRepositoriesInterface


@dataclass
class JuryRepositories(JuryRepositoriesInterface):
    session: AsyncSession
    
    async def get_jurys(self, limit: int, offset: int):
        stmt = select(Jury) \
            .limit(limit) \
            .offset(offset)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    
    async def create_jury(self, jury_data: CreateJurySchema):
        president_id = jury_data.president_id
        examinateur_id = jury_data.examinateur_id
        rapporteur_id = jury_data.rapporteur_id

        # Normaliser les ids pour comparaison
        ids_to_check = sorted([president_id, examinateur_id, rapporteur_id])

        # Vérifier si un jury avec les mêmes membres existe déjà
        stmt = select(Jury).filter(
            and_(
                Jury.president_id.in_(ids_to_check),
                Jury.examinateur_id.in_(ids_to_check),
                Jury.rapporteur_id.in_(ids_to_check)
            )
        )
        result = await self.session.execute(stmt)
        existing_jurys = result.scalars().all()

        for jury in existing_jurys:
            existing_ids = sorted([
                jury.president_id,
                jury.examinateur_id,
                jury.rapporteur_id
            ])
            if existing_ids == ids_to_check:
                raise ValueError(f"Un jury avec la composition {ids_to_check} existe déjà sous le numéro {jury.numero}")

        # Si aucun jury existant avec la même composition, insérer le nouveau jury
        values = {
            'numero': jury_data.numero,
            'president_id': president_id,
            'examinateur_id': examinateur_id,
            'rapporteur_id': rapporteur_id
        }
        stmt = insert(Jury).values(**values).returning(Jury)
        result = await self.session.execute(statement=stmt)
        await self.session.commit()
        return {'detail': f'Jury numéro {jury_data.numero} créé avec succès'}
    
    
    async def delete_jury(self, numero: str):
        # Récupérer le jury à supprimer
        jury = await self.get_jury(numero)
        if not jury:
            raise JuryExceptions().jury_not_found

        # Supprimer le jury
        stmt = delete(Jury).where(Jury.numero == numero)
        result = await self.session.execute(statement=stmt)
        await self.session.commit()
        return {'detail': f'Jury numéro {numero} supprimé avec succès'}
    
    async def update_jury(self, numero: str, updated_data: UpdateJurySchema):
        await self.__check_jury(numero=numero)
        values = {**updated_data.dict(exclude_none=True)}
        if updated_data.numero:
            values.update({'numero': updated_data.numero})
            stmt = update(Jury).where(Jury.numero == numero).values(**values).returning(Jury)
            result = await self.session.execute(statement=stmt)
        await self.session.commit()
        # return result.scalar_one()
        return {'detail': f'Jury numéro {numero} mise à jour'}
    
    async def get_jury(self, numero: str):
        stmt = select(Jury).where(Jury.numero == numero)
        result: AsyncResult = await self.session.execute(statement=stmt)
        return result.scalars().first()

    async def __check_jury(self, numero: str):
        if not (jury := await self.get_jury(numero=numero)):
            raise JuryExceptions().jury_not_found
        return jury
