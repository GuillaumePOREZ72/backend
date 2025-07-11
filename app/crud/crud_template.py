from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Template
from app.schemas.schemas import TemplateCreate, TemplateUpdate

class CRUDTemplate(CRUDBase[Template, TemplateCreate, TemplateUpdate]):
    def get_by_category(self, db: Session, *, category_id: int) -> List[Template]:
        """Récupérer tous les templates d'une catégorie"""
        return db.query(Template).filter(Template.category_id == category_id).all()


    def get_active_templates(self, db: Session) -> List[Template]:
        """Récupérer les templates actifs"""
        return db.query(Template).filter(Template.is_active == True).all()

    def search_templates(self, db: Session, *, query: str) -> List[Template]:
        """Rechercher des templates par titre ou description"""
        return db.query(Template).filter(Template.title.ilike(f"%{query}%") | Template.description.ilike(f"%{query}%")).all()

template = CRUDTemplate(Template)