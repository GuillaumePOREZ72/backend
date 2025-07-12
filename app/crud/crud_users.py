from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import User
from app.schemas.schemas import UserCreate, UserUpdate

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """Récupérer un utilisateur par email"""
        return db.query(User).filter(User.email == email).first()

    def get_by_google_id(self, db: Session, *, google_id: str) -> Optional[User]:
        """Récupérer un utilisateur par son Google ID"""
        return db.query(User).filter(User.google_id == google_id).first()

    def get_active_users(self, db: Session) -> list[User]:
        """Récupérer tous les utilisateurs actifs"""
        return db.query(User).filter(User.is_active == True).all()

user = CRUDUser(User)