from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import SharedProject
from app.schemas.schemas import SharedProjectCreate, SharedProjectResponse

class CRUDSharedProject(CRUDBase[SharedProject, SharedProjectCreate, SharedProjectResponse]):
    def get_by_user(self, db: Session, *, user_id: int) -> List[SharedProject]:
        """Récupérer tous les projets partagés avec un utilisateur"""
        return db.query(SharedProject).filter(SharedProject.shared_with_user_id == user_id).all()

    def get_by_project(self, db: Session, *, project_id: int) -> List[SharedProject]:
        """Récupérer tous les partages d'un projet"""
        return db.query(SharedProject).filter(SharedProject.project_id == project_id).all()

    def get_by_permission(self, db: Session, *, permission: str) -> List[SharedProject]:
        """Récupérer les partages par permission (view, edit, copy)"""
        return db.query(SharedProject).filter(SharedProject.permission == permission).all()

    def get_user_project_permission(self, db: Session, *, user_id: int, project_id: int) -> Optional[SharedProject]:
        """Récupérer la permission d'un utilisateur sur un projet"""
        return db.query(SharedProject).filter(
            SharedProject.shared_with_user_id == user_id, 
            SharedProject.project_id == project_id
        ).first()

shared_project = CRUDSharedProject(SharedProject)