from typing import Text
from sqlalchemy import func, Column, Integer, String, DateTime,text, Time, Boolean, \
    ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import UniqueConstraint
from sqlalchemy import UniqueConstraint, CheckConstraint
from sqlalchemy.orm import validates


class Users(Base):
    __tablename__ = 'utilisateur'

    __mapper_args__ = {"eager_defaults": True}


    id = Column(Integer, primary_key=True)
    username = Column(String(length=200), nullable=False, unique=True)
    password = Column(String, nullable=True)
    nom = Column(String(length=200), nullable=False)
    prenoms = Column(String(length=200), nullable=False)
    bio = Column(String(length=255))
    role_id = Column(
        Integer,
        ForeignKey('role.id', ondelete='CASCADE')
    )
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created = Column(DateTime, server_default=func.now())
    reset_token = Column(String, nullable=True)  
    token_expires = Column(DateTime, nullable=True)  

    role_rel = relationship('Role', backref='utilisateur')
    images = relationship(
        'UserImage',
        backref='utilisateur',
        passive_deletes=True,
        lazy='joined'
    )

    __table_args__ = (
        UniqueConstraint('id', 'role_id', name='unique_user_role'),
    )
    
    def __repr__(self) -> str:
        return f'User(username={self.username}, token_expires={self.token_expires})'
    

class UserImage(Base):
    __tablename__ = 'utilisateur_image'

    id = Column(Integer, primary_key=True)
    photo = Column(String)
    utilisateur_id = Column(Integer, ForeignKey('utilisateur.id', ondelete='CASCADE'))

    def __repr__(self) -> str:
        return f'User image: {self.photo} : {self.utilisateur_id}'
    

class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    libelle = Column(String(length=200), nullable=False)

    def __repr__(self) -> str:
        return f'Role : {self.libelle}'
    

class Etudiant(Base):
    __tablename__ = 'etudiant'
    __mapper_args__ = {'eager_defaults': True}

    id = Column(Integer, primary_key=True)
    matricule = Column(String(length=200), nullable=False, unique=True)
    slug = Column(String)
    utilisateur_id = Column(Integer, ForeignKey('utilisateur.id', ondelete='CASCADE'), unique=True)
    filiere_id = Column(Integer, ForeignKey('filiere.id', ondelete='CASCADE'))
    
    
    utilisateur = relationship('Users', backref='etudiant')
    filiere_rel = relationship('Filiere', backref='etudiant')
    created = Column(DateTime, server_default=func.now())
    

    def __repr__(self) -> str:
        return f'Etudiant: {self.slug}'
    
    
class Filiere(Base):
    __tablename__ = 'filiere'

    id = Column(Integer, primary_key=True)
    nom = Column(String(length=200), nullable=False)
    departement_id = Column(Integer, ForeignKey('departement.id', ondelete='CASCADE'))
    
    chef_departemnt_rel = relationship('Departement', backref='filiere')
    def __repr__(self) -> str:
        return f'Filiere : {self.nom}'
    

class Annee(Base):
    __tablename__ = 'annee'

    id = Column(Integer, primary_key=True)
    libelle = Column(String(length=200), nullable=False)

    def __repr__(self) -> str:
        return f'Annee : {self.libelle}'
    

class Salle(Base):
    __tablename__ = 'salle'

    id = Column(Integer, primary_key=True)
    libelle = Column(String(length=200), nullable=False)

    def __repr__(self) -> str:
        return f'Salle : {self.libelle}'



class Enseignant(Base):
    __tablename__ = 'enseignant'
    __mapper_args__ = {'eager_defaults': True}

    id = Column(Integer, primary_key=True)
    matricule = Column(String(length=200), nullable=False, unique=True)
    slug = Column(String)
    grade_id = Column(Integer,  ForeignKey('grade.id', ondelete='CASCADE'), nullable=False)
    specialite = Column(String(length=200), nullable=False) 
    utilisateur_id = Column(Integer,  ForeignKey('utilisateur.id', ondelete='CASCADE'), unique=True)
    departement_id = Column(ForeignKey('departement.id', ondelete='CASCADE'))
    is_chef = Column(Boolean, default=False)

    utilisateur = relationship('Users', backref='etudiants')
    grade_rel = relationship('Grade', backref='enseignant')
    departement_rel = relationship('Departement', backref='enseignant')
    created = Column(DateTime, server_default=func.now())
    
    def __repr__(self) -> str:
        return f'Enseignant: {self.slug}'
    
    
class Departement(Base):
    __tablename__ = 'departement'
    __mapper_args__ = {'eager_defaults': True}

    id = Column(Integer, primary_key=True)
    nom = Column(String(150), nullable=False)
    
    def __repr__(self) -> str:
        return f'Departement: {self.nom}'
    
class Grade(Base):
    __tablename__ = 'grade'
    __mapper_args__ = {'eager_defaults': True}

    id = Column(Integer, primary_key=True)
    nom = Column(String(150), nullable=False)
    
    def __repr__(self) -> str:
        return f'Grade: {self.nom}'
    
class Chefdepartement(Base):
    __tablename__ = 'chef_departement'

    id = Column(Integer, primary_key=True)
    enseignant_id = Column(Integer, ForeignKey('enseignant.id', ondelete='CASCADE'))
    annee_id = Column(Integer, ForeignKey('annee.id', ondelete='CASCADE'))
    
    enseignant_rel = relationship('Enseignant', backref='chef_departement')
    annee_rel = relationship('Annee', backref='chef_departement')

    def __repr__(self) -> str:
        return f'Chefdepartement : {self.id}'

class Jury(Base):
    __tablename__ = 'jury'
    __table_args__ = (
        UniqueConstraint('president_id', 'examinateur_id', 'rapporteur_id', name='uq_jury_composition'),
        {'schema': 'public'}
    )

    id = Column(Integer, primary_key=True)
    numero = Column(String(length=200), nullable=False, unique=True)
    president_id = Column(Integer, ForeignKey('enseignant.id', ondelete='CASCADE'))
    examinateur_id = Column(Integer, ForeignKey('enseignant.id', ondelete='CASCADE'))
    rapporteur_id = Column(Integer, ForeignKey('enseignant.id', ondelete='CASCADE'), nullable=True)

    president = relationship('Enseignant', foreign_keys=[president_id], backref='membre_jury1')
    examinateur = relationship('Enseignant', foreign_keys=[examinateur_id], backref='membre_jury2')
    rapporteur = relationship('Enseignant', foreign_keys=[rapporteur_id], backref='membre_jury3')

    def __repr__(self) -> str:
        return f'Jury : {self.numero}'
    
    @validates('president_id', 'examinateur_id', 'rapporteur_id')
    def validate_unique_enseignant(self, key, value):
        ids = [self.president_id, self.examinateur_id, self.rapporteur_id]
        ids.remove(value)
        if value in ids:
            raise ValueError("Un enseignant ne peut pas occuper plusieurs rôles dans le même jury.")
        return value

class Thesis(Base):
    __tablename__ = 'soutenance'
    __mapper_args__ = {'eager_defaults': True}

    id = Column(Integer, primary_key=True)
    numero = Column(String(length=200), unique=True, nullable=False)
    slug = Column(String)
    owner_id = Column(Integer, ForeignKey('utilisateur.id', ondelete='CASCADE'))
    theme = Column(String(length=200), nullable=True)
    lieu_stage = Column(String(length=200), nullable=True)
    responsable = Column(String(length=200), nullable=True)
    cahier_charge = Column(String(length=200), nullable=True)
    is_theme_valide = Column(Boolean, default=False)
    is_binome_valide = Column(Boolean, default=False)
    choix1_id = Column(Integer, ForeignKey('enseignant.id', ondelete='CASCADE'), nullable=True)
    choix2_id = Column(Integer, ForeignKey('enseignant.id', ondelete='CASCADE'), nullable=True)
    maitre_memoire_id = Column(Integer, ForeignKey('enseignant.id', ondelete='CASCADE'), nullable=True)
    annee_id = Column(Integer, ForeignKey('annee.id', ondelete='CASCADE'), nullable=True)
    
    maitre_memoire = relationship('Enseignant', foreign_keys=[maitre_memoire_id], backref='soutenances_maitre_memoire')
    annee =  relationship('Annee', foreign_keys=[annee_id], backref='annee_id')
    choix1 = relationship('Enseignant', foreign_keys=[choix1_id], backref='soutenances_choix1')
    choix2 = relationship('Enseignant', foreign_keys=[choix2_id], backref='soutenances_choix2')
    utilisateur = relationship('Users', backref='soutenance')
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f'Thesis: {self.slug}'


class Appartenir(Base):
    __tablename__ = 'appartenir'
    __mapper_args__ = {'eager_defaults': True}

    id = Column(Integer, primary_key=True)
    etudiant_id = Column(Integer, ForeignKey('etudiant.id', ondelete='CASCADE'))
    soutenance_id = Column(Integer, ForeignKey('soutenance.id', ondelete='CASCADE'))

    etudiant_rel = relationship('users.auth.models.Etudiant', backref='appartenir')
    soutenance_rel = relationship('Thesis', backref='appartenir')

    def __repr__(self) -> str:
        return f'Appartenir: {self.id}'


