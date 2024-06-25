from dataclasses import dataclass
from typing import Dict, List, Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult
from sqlalchemy import select, insert, delete, update, and_
from sqlalchemy.orm import subqueryload
from sqlalchemy.orm.exc import NoResultFound

from users.auth.models import Etudiant, Users
from users.etudiants.schemas import CreateEtudiantSchema
from .schemas import CreateThesisSchema, CreateThesisSchema, UpdateThesisSchema
from users.auth.models import  Appartenir, Thesis
from .exceptions import ThesisExceptions
from .interfaces.repositories_interface import \
    ThesisRepositoriesInterface
from sqlalchemy import exists

@dataclass
class ThesisRepositories(ThesisRepositoriesInterface):
    session: AsyncSession

    async def get_all_thesis(self, annee_id: int, limit: int, offset: int):
        stmt = (
            select(Thesis)
            .where(Thesis.annee_id == annee_id)
            .limit(limit)
            .offset(offset)
            .order_by(Thesis.created.desc())
        )
        print(annee_id)
        result = await self.session.execute(statement=stmt)
        theses = result.scalars().all()
        print(f"Fetched theses: {theses}")  
        return theses

    async def get_thesis(self, utilisateur_id: int, years_id: int):
        print(utilisateur_id)
        print(years_id)
        try:
            # Récupérer l'ID de l'étudiant associé à l'utilisateur
            stmt = select(Etudiant.id).join(Users, Users.id == Etudiant.utilisateur_id).where(
                Users.id == utilisateur_id
            )
            etudiant_id_result = await self.session.execute(stmt)
            etudiant_id = etudiant_id_result.scalar_one()
            print(f"Etudiant ID associé à l'utilisateur {utilisateur_id}: {etudiant_id}")

            # Récupérer les IDs des soutenances associées à cet étudiant
            soutenance_ids_stmt = select(Appartenir.soutenance_id).where(Appartenir.etudiant_id == etudiant_id)
            soutenance_ids_result = await self.session.execute(soutenance_ids_stmt)
            soutenance_ids = [row[0] for row in soutenance_ids_result.fetchall()]
            print(soutenance_ids)

            if not soutenance_ids:
                print("Aucune soutenance trouvée pour l'étudiant spécifié.")
                return []

            print(f"Soutenance IDs associés à l'étudiant {etudiant_id}: {soutenance_ids}")

            # Récupérer les thèses correspondantes
            thesis_stmt = select(Thesis).where(
                and_(
                    Thesis.id.in_(soutenance_ids),
                    Thesis.annee_id == years_id
                )
            ).order_by(Thesis.created.desc())

            thesis_result = await self.session.execute(thesis_stmt)
            theses = thesis_result.scalars().all()
            print(theses)

            if not theses:
                print("Aucune thèse trouvée pour les critères spécifiés.")

            return theses

        except NoResultFound:
            print(f"Aucun étudiant trouvé pour l'utilisateur {utilisateur_id}.")
            raise HTTPException(status_code=404, detail=f"Aucun étudiant trouvé pour l'utilisateur {utilisateur_id}.")

        except Exception as e:
            print(f"Erreur lors de l'exécution de la requête : {e}")
            raise HTTPException(status_code=500, detail="Erreur interne du serveur")



    async def create_thesis(self, utilisateur_id: int, thesis_data: CreateThesisSchema, matricules: list, session: AsyncSession):
        try:
            values = {
                'owner_id': utilisateur_id,
                'slug': thesis_data.numero, 
                **thesis_data.dict(exclude_unset=True)
            }
            print(values)
            thesis_stmt = insert(Thesis).values(**values).returning(Thesis.id)
            result = await session.execute(thesis_stmt)
            thesis_id = result.scalar()
            print(f"Soutenance créée avec succès, ID: {thesis_id}")

            etudiant_ids = await self.get_etudiant_ids(session, matricules)
            print(etudiant_ids)

            if any(etudiant_id is None for etudiant_id in etudiant_ids.values()):
                raise ThesisExceptions("Un ou plusieurs matricules sont invalides.")

            for matricule, etudiant_id in etudiant_ids.items():
                thesis_annee_id_stmt = select(Thesis.annee_id).where(Thesis.id == thesis_id)
                thesis_annee_id_result = await session.execute(thesis_annee_id_stmt)
                thesis_annee_id = thesis_annee_id_result.scalar()

                appartenir_exist_stmt = select(exists().where(
                    Appartenir.etudiant_id == etudiant_id
                ).where(
                    Thesis.id == Appartenir.soutenance_id
                ).where(
                    Thesis.annee_id == thesis_annee_id
                ))
                appartenir_exist_result = await session.execute(appartenir_exist_stmt)

                if appartenir_exist_result.scalar():
                    raise ThesisExceptions(f"L'étudiant avec le matricule {matricule} est déjà associé à une autre thèse pour la même année académique.")

                appartenir_stmt = insert(Appartenir).values(etudiant_id=etudiant_id, soutenance_id=thesis_id)
                await session.execute(appartenir_stmt)

            await session.commit()
            print("La thèse et les associations ont été créées avec succès.")
            return thesis_id

        except Exception as e:
            print(f"Une erreur s'est produite : {str(e)}")
            await session.rollback()
            raise e



    async def get_etudiant_ids(self, session, matricules: list[str]):
        stmt = (
            select(Etudiant.id, Etudiant.matricule)
            .where(Etudiant.matricule.in_(matricules))
            .order_by(Etudiant.matricule)
        )
        result = await session.execute(stmt)
        etudiant_ids = {row.matricule: row.id for row in result}
        return etudiant_ids
    
    async def update_thesis(
            self, utilisateur_id: int, thesis_slug: str,
            updated_data: UpdateThesisSchema
    ):
        await self.__check_thesis(thesis_slug=thesis_slug)
        values = {**updated_data.dict(exclude_none=True)}
        if updated_data.numero:
            values.update({'slug': updated_data.numero})
        cond = (Thesis.slug == thesis_slug, Thesis.owner_id == utilisateur_id)
        stmt = update(Thesis).where(*cond).values(**values)
        await self.session.execute(statement=stmt)
        await self.session.commit()
    
    async def get_thesisa(self, thesis_slug: str):
        stmt = select(Thesis).where(Thesis.slug == thesis_slug)
        result: AsyncResult = await self.session.execute(statement=stmt)
        return result.scalars().first()
    
    async def __check_thesis(self, thesis_slug: str):
        if not (thesis := await self.get_thesisa(thesis_slug=thesis_slug)):
            raise ThesisExceptions().thesis_not_found
        return thesis

    async def get_all_thesis_with_students(self, annee_id: int, limit: int, offset: int, db: AsyncSession):
        print("Entering get_all_thesis_with_students function")
        print(f"Received annee_id: {annee_id}")
        
        if not isinstance(annee_id, int):
            raise ValueError(f"annee_id must be an integer, received: {type(annee_id)}")

        try:
            stmt = (
                select(Thesis.id, Thesis.theme, Thesis.annee_id, Appartenir.etudiant_id)
                .join(Appartenir, Thesis.id == Appartenir.soutenance_id)
                .where(Thesis.annee_id == annee_id)
                .limit(limit)
                .offset(offset)
            )
            result = await db.execute(stmt)
            print(f"SQL Query executed. Result: {result}")
            
            if result is None:
                raise Exception("Database execution returned None")

            # Aggregating results
            thesis_dict = {}
            all_results = result.all()
            print(f"Number of results: {len(all_results)}")
            
            if not all_results:
                raise Exception(f"No results found for annee_id: {annee_id}")

            for thesis_id, theme, annee_id, etudiant_id in all_results:
                if thesis_id not in thesis_dict:
                    thesis_dict[thesis_id] = {
                        'thesis_id': thesis_id,
                        'theme': theme,
                        'annee_id': annee_id,
                        'etudiant_ids': []
                    }
                thesis_dict[thesis_id]['etudiant_ids'].append(etudiant_id)

            if not thesis_dict:
                raise Exception(f"No theses found after processing for annee_id: {annee_id}")

            return list(thesis_dict.values())

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            raise
    async def assign_choices(self):
        # Implémentation pour récupérer les choix depuis la base de données
        pass  # À implémenter

