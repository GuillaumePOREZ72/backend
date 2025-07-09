from typing import List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Category
from app.schemas.category import CategoryCreate, CategoryUpdate

class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Category:
        """Récupérer une catégorie par son nom"""
        return db.query(Category).filter(Category.name == name).first()

    def get_active_categories(self, db: Session) -> List[Category]:
        """Récupérer toutes les catégories actives"""
        return db.query(Category).filter(Category.is_active == True).all()

category = CRUDCategory(Category)
