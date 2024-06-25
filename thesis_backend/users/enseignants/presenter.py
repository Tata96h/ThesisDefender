from dataclasses import dataclass
from typing import List

from database import AsyncSessionLocal
from users.auth.exceptions import AuthExceptions
from users.auth.interfaces.password_service_interface import PasswordServiceInterface
from users.auth.interfaces.repositories_interface import UserRepositoriesInterface
from users.auth.service_email import send_email
from users.etudiants.exceptions import EtudiantExceptions
from users.etudiants.schemas import FiliereSchema
from .schemas import DepartementSchema, EnseignantSchema, GradeSchema, UpdateEnseignantSchema, CreateEnseignantSchema
from .interfaces.repositories_interface import EnseignantRepositoriesInterface
from .exceptions import EnseignantExceptions
from sqlalchemy.exc import SQLAlchemyError


@dataclass
class EnseignantPresenter:
    repository: EnseignantRepositoriesInterface
    user_repository: UserRepositoriesInterface
    password_service: PasswordServiceInterface

    async def get_enseignants(self,  limit: int, offset: int):
        data = { 'limit': limit, 'offset': offset}
        return await self.repository.get_enseignants(**data)

   
    async def create_enseignant(self, enseignant_data: CreateEnseignantSchema):
        async with AsyncSessionLocal() as session:
            utilisateur_id = None  # Initialiser utilisateur_id à None
            try:
                async with session.begin_nested():
                    # Vérifier si l'utilisateur existe déjà
                    if await self.user_repository.receive_user_by_username(username=enseignant_data.username):
                        raise AuthExceptions().username_exists
                    
                    # Vérifier si le matricule existe déjà
                    existing_etudiant = await self.repository.get_enseignant(enseignant_slug=enseignant_data.matricule)
                    if existing_etudiant:
                        raise EnseignantExceptions().enseignant_exists
                    
                    # Hacher le mot de passe
                    hashed_password = await self.password_service.hashed_password(password=enseignant_data.password)

                    # Enregistrer l'utilisateur et récupérer l'utilisateur_id
                    utilisateur_id = await self.user_repository.save_user(
                        username=enseignant_data.username,
                        email=enseignant_data.email,
                        password=hashed_password,
                        nom=enseignant_data.nom,
                        prenoms=enseignant_data.prenoms,
                        role_id=2  # Role ID pour étudiant
                    )
                    print(f"Utilisateur {enseignant_data.username} enregistré avec succès. ID Utilisateur: {utilisateur_id}")

                    # Créer l'enseignant avec l'ID de l'utilisateur
                    enseignant_creation_data = {
                        'matricule': enseignant_data.matricule,
                        'grade_id': enseignant_data.grade_id,
                        'specialite': enseignant_data.specialite,
                        'departement_id': enseignant_data.departement_id,
                        'utilisateur_id': utilisateur_id
                    }
                    await self.repository.create_enseignant(enseignant_creation_data)
                    print(f"Enseignant créé avec succès pour l'utilisateur {enseignant_data.username}.")

                # Si tout s'est bien passé, committer la transaction
                await session.commit()
            
                # Envoyer l'e-mail de bienvenue après la création réussie de l'étudiant
                app_name = "SoutenanceManager"
                subject = "Invitation à SoutenanceManager"
                subject_with_app = f"[{app_name}] {subject}"
                login_url = "http://localhost:3000/login"  # Remplacez par l'URL réelle de votre système de gestion
                body = f"""
                    <html>
                        <head>
                            <title>Invitation</title>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    background-color: #f5f5f5;
                                }}
                                .container {{
                                    max-width: 600px;
                                    margin: 0 auto;
                                    padding: 20px;
                                    background-color: #fff;
                                    border: 1px solid #ccc;
                                    border-radius: 5px;
                                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                                }}
                                .header {{
                                    background-color: #007bff;
                                    color: white;
                                    padding: 10px;
                                    text-align: center;
                                    font-weight: bold;
                                    border-top-left-radius: 5px;
                                    border-top-right-radius: 5px;
                                }}
                                .button-container {{
                                    text-align: center;
                                }} 
                                .button {{
                                    display: inline-block;
                                    background-color: #007bff;
                                    color: white;
                                    padding: 10px 20px;
                                    text-decoration: none;
                                    border-radius: 5px;
                                    transition: background-color 0.3s ease;
                                }}
                                .button:hover {{
                                    background-color: #0116b3;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="container">
                                <div class="header">{app_name}</div>
                                <h2>Bienvenue dans le Système de Gestion des Soutenances</h2>
                                <p>Bonjour {enseignant_data.username},</p>
                                <p>Vous avez été ajouté au Système de Gestion des Soutenances. Vous pouvez maintenant vous connecter pour préparer votre soutenance.</p>
                                <p>Pour commencer, veuillez cliquer sur le bouton ci-dessous :</p>
                                <div class="button-container">
                                    <a href="{login_url}" class="button">Se connecter</a>
                                </div>
                                <p>Cordialement,<br>L'équipe administrative de {app_name}</p>
                            </div>
                        </body>
                    </html>
                """
                await send_email(enseignant_data.email, subject_with_app, body, app_name)
                raise EnseignantExceptions().enseignant_create
            except SQLAlchemyError as e:
                print("Il y a eu une erreur:", e)
                # Annuler la transaction en cas d'erreur
                await session.rollback()
                raise e
            
    async def delete_enseignant(self, enseignant_slug: str):
        data = { 'enseignant_slug': enseignant_slug}
        if not await self.repository.delete_enseignant(**data):
            raise EnseignantExceptions().enseignant_not_found

    async def update_enseignant(self, enseignant_slug: str, updated_data: UpdateEnseignantSchema):
        if updated_data.is_empty:
            raise EnseignantExceptions().empty_data
        return await self.repository.update_enseignant(
             enseignant_slug=enseignant_slug, updated_data=updated_data
        )

    async def get_enseignant(self, enseignant_slug: str):
        data = {'enseignant_slug': enseignant_slug}
        if (result := await self.repository.get_enseignant(**data)) is None:
            raise EnseignantExceptions().enseignant_not_found
        return result

    async def get_enseignants_by_departement(self, departement_id: int, limit: int, offset: int) -> List[EnseignantSchema]:
        return await self.repository.get_enseignants_by_departement(departement_id, limit, offset)
    

    async def get_departements(self) -> List[DepartementSchema]:
        departements = await self.repository.get_departements()
        return [DepartementSchema.from_orm(departement) for departement in departements]
    
    async def get_grades(self) -> List[GradeSchema]:
        grades = await self.repository.get_grades()
        return [DepartementSchema.from_orm(grade) for grade in grades]
    
    async def get_filieres_by_departement(self, departement_id: int):
        try:
            filieres = await self.repository.get_filieres_by_departement(departement_id)
            return [FiliereSchema.from_orm(filiere) for filiere in filieres]
        except Exception as e:
            # Gérer les exceptions appropriées ici
            raise e