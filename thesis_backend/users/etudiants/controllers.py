from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from .presenter import EtudiantPresenter
from .schemas import CreateEtudiantSchema, EtudiantSchema, FiliereSchema, UpdateEtudiantSchema
from .deps import response_data,  get_presenter, \
    get_slug_user, get_updated_data_slug_user, get_limit_offset_user, \
    get_create_data_user

etudiant_controllers = APIRouter(prefix='/etudiants', tags=['etudiants'])



@etudiant_controllers.get(**response_data.get('etudiants'))
async def get_etudiants(
        limit: int | None = 20,
        offset: int | None = 0,
        presenter: EtudiantPresenter = Depends(get_presenter),
):
    data: dict = await get_limit_offset_user(limit, offset)
    return await presenter.get_etudiants(**data)

@etudiant_controllers.post(**response_data.get('create_etudiants'))
async def create_etudiant(
        etudiant_data: CreateEtudiantSchema,
        presenter: EtudiantPresenter = Depends(get_presenter),
):
    data: dict = await get_create_data_user(etudiant_data)
    return await presenter.create_etudiant(**data)

@etudiant_controllers.delete(**response_data.get('delete_etudiants'))
async def delete_etudiant(
        matricule: str,
        presenter: EtudiantPresenter = Depends(get_presenter),
):
    data: dict = await get_slug_user(matricule)
    return await presenter.delete_etudiant(**data)

@etudiant_controllers.patch(**response_data.get('update_etudiant'))
async def update_etudiant(
        matricule: str,
        updated_data: UpdateEtudiantSchema,
        presenter: EtudiantPresenter = Depends(get_presenter),
):
    data: dict = await get_updated_data_slug_user(updated_data, matricule)
    return await presenter.update_etudiant(**data)

@etudiant_controllers.get(**response_data.get('etudiant'))
async def get_etudiant(
        matricule: str,
        presenter: EtudiantPresenter = Depends(get_presenter),
):
    return await presenter.get_etudiant(etudiant_slug=matricule)

@etudiant_controllers.get(**response_data.get('etudiants_by_filiere'))
async def get_etudiants_by_filiere(
        filiere_id: int,
        limit: int | None = 20,
        offset: int | None = 0,
        presenter: EtudiantPresenter = Depends(get_presenter),
):
    data: dict = await get_limit_offset_user(limit, offset)
    data['filiere_id'] = filiere_id
    return await presenter.get_etudiants_by_filiere(**data)


@etudiant_controllers.get('/get_filieres/', response_model=List[FiliereSchema])
async def get_filieres(
    presenter: EtudiantPresenter = Depends(get_presenter),
    limit: int | None = 20,
    offset: int | None = 0,
    ):
    try:
        data: dict = await get_limit_offset_user(limit, offset)
        return await presenter.get_filieres(**data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


