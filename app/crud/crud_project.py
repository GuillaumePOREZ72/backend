from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Project
from app.schemas.schemas import ProjectCreate, ProjectUpdate

class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    def get_by_owner(self, db: Session, *, owner_id: int) -> List[Project]:
        """Récupérer tous les projets d'un utilisateur"""
        return db.query(Project).filter(Project.owner_id == owner_id).all()

    def get_public_projects(self, db: Session, *, skip: int=0, limit: int=0) -> List[Project]:
        """Récupérer tous les projets publics"""
        return db.query(Project).filter(Project.is_public == True).offset(skip).limit(limit).all()

    def get_by_format(self, db: Session, *, format_type: str) -> List[Project]:
        """Récupérer les projets par format (A4, A5, custom)"""
        return db.query(Project).filter(Project.format_type == format_type).all()

    def search_projects(self, db: Session, *, query: str) -> List[Project]:
        """Rechercher des projets par titre ou description"""
        return db.query(Project).filter(Project.title.ilike(f"%{query}%")) | Project.description.ilike(f"%{query}%").all().all()

    def get_user_projects(self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
        """Récupérer les projets d'un utilisateur avec pagination"""
        return db.query(Project).filter(Project.owner_id == owner_id).offset(skip).limit(limit).all()

project = CRUDProject(Project)