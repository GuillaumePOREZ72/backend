from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.deps.database import get_db
from app.deps.auth import get_current_active_user
from app.crud.crud_template import template
from app.crud.crud_category import category
from app.schemas.schemas import TemplateCreate, TemplateUpdate, TemplateResponse
from app.models.models import User

router = APIRouter()

@router.get("/", response_model=List[TemplateResponse])
def get_templates(
    skip: int=0,
    limit: int = 100,
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    db: Session = Depends(get_db)
):
    """
    Récupérer tous les templates avec filtres optionnels
    """
    if search:
        templates = template.search_templates(db, query=search)
    elif category_id:
        templates = template.get_by_category(db, category_id=category_id)
    else:
        templates = template.get_multi(db, skip=skip, limit=limit)
    
    return templates

@router.get("/active", response_model=List[TemplateResponse])
def get_active_templates(db: Session = Depends(get_db)):
    """
    Récupérer uniquement les templates actifs
    """
    templates = template.get_active_templates(db)
    return templates

@router.get("/category/{category_id}", response_model=List[TemplateResponse])
def get_templates_by_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupérer tous les templates d'une catégorie spécifique
    """
    # Vérifier que la catégorie existe
    db_category = category.get(db, id=category_id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    templates = template.get_by_category(db, category_id=category_id)
    return templates

@router.get("/{template_id}", response_model=TemplateResponse)
def get_template_by_id(
    template_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupérer un template par son ID
    """
    db_template = template.get(db, id=template_id)
    if not db_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    return db_template

@router.post("/", response_model=TemplateResponse, status_code=status.HTTP_201_CREATED)
def create_template(
    template_in: TemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Créer un nouveau template
    """
    # Vérifier que la catégorie existe
    db_category = category.get(db, id=template_in.category_id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found"
        )
    return template.create(db, obj_in=template_in)


@router.put("/{template_id}", response_model=TemplateResponse)
def update_template(
    template_id: int,
    template_in: TemplateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Mettre à jour un template
    """
    db_template = template.get(db, id=template_id)
    if not db_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )

    # Vérifier que la nouvelle catégorie existe (si changée)
    if template_in.category_id and template_in.category_id != db_template.category_id:
        db_category = category.get(db, id=template_in.category_id)
        if not db_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category not found"
            )
    return template.update(db, db_obj=db_template, obj_in=template_in)

@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Supprimer un template
    """
    db_template = template.get(db, id=template_id)
    if not db_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    template.remove(db, id=template_id)
    return None

