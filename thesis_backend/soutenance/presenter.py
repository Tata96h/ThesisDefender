from dataclasses import dataclass
from typing import List
from .schemas import CreateThesisSchema, UpdateThesisSchema
from .interfaces.repositories_interface import \
     ThesisRepositoriesInterface
    
from .exceptions import ThesisExceptions
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class ThesisPresenter:
    repository: ThesisRepositoriesInterface
    
    # async def create_thesis(self, thesis_data: CreateThesisSchema, db: AsyncSession):
    #     thesis_id = await self.repository.create_thesis(thesis_data, db)
    #     return {'thesis_id': thesis_id}

    async def get_all_thesis(self, annee_id: int, limit: int, offset: int):
        data = {'annee_id': annee_id, 'limit': limit, 'offset': offset}
        return await self.repository.get_all_thesis(**data)

    async def get_thesis(self, utilisateur_id: int, years_id: int):
        data = {'utilisateur_id': utilisateur_id, 'years_id': years_id}
        return await self.repository.get_thesis(**data)
    
    async def create_thesis(self, utilisateur_id: int, thesis_data: CreateThesisSchema, matricules: list, db: AsyncSession):
        thesis_id = await self.repository.create_thesis(utilisateur_id, thesis_data, matricules, db)
        return thesis_id

    async def get_all_thesis_with_students(self, annee_id: int, limit: int, offset: int, db: AsyncSession):
        print(f"Presenter: Entering function with annee_id={annee_id}, limit={limit}, offset={offset}")
        print(f"Presenter: Repository instance: {self.repository}")
        
        try:
            print("Presenter: Calling repository.get_all_thesis_with_students")
            result = await self.repository.get_all_thesis_with_students(annee_id, limit, offset, db)
            print(f"Presenter: Received result from repository: {result}")
            return result
        except Exception as e:
            print(f"Presenter: Error occurred: {str(e)}")
            raise
    
    async def update_thesis(
            self, utilisateur_id: int, thesis_slug: str,
            updated_data: UpdateThesisSchema
    ):
        if updated_data.is_empty:
            raise ThesisExceptions().empty_data
        return await self.repository \
            .update_thesis(utilisateur_id=utilisateur_id, thesis_slug=thesis_slug,
                            updated_data=updated_data)
    
    async def get_thesisa(self, thesis_slug: str):
        data = {'thesis_slug': thesis_slug}
        if (result := await self.repository.get_thesisa(**data)) is None:
            raise ThesisExceptions().thesis_not_found
        return result
    

    async def assign_choices(self):
        # Implémentation pour récupérer les choix depuis la base de données
        pass  # À implémenter