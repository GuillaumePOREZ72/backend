from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps.database import get_db
from app.deps.auth import get_current_active_user
from app.crud.crud_category import category
from app.schemas.schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from app.models.models import User

router = APIRouter()

# ======== ENDPOINTS PUBLICS (pour la landing page) ========

@router.get("/", response_model=List[CategoryResponse])
def get_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Récupérer toutes les catégories avec pagination
    """
    categories = category.get_multi(db, skip=skip, limit=limit)
    return categories

@router.get("/active", response_model=List[CategoryResponse])
def get_active_categories(db: Session = Depends(get_db)):
    """
    Récupérer uniquement les catégories actives
    """
    categories = category.get_active_categories(db)
    return categories

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """
    Récupérer une catégorie par son ID
    """
    db_category = category.get(db, id=category_id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return db_category

# ======== ENDPOINTS PROTÉGÉS (authentification) ========

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_in: CategoryCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Créer une nouvelle catégorie (PROTEGE par auth)
    """
    # Vérifier si le nom existe déjà
    existing_category = category.get_by_name(db, name=category_in.name)
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists"
        )
    return category.create(db, obj_in=category_in)

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int, 
    category_in: CategoryUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Mettre à jour une catégorie
    """
    db_category = category.get(db, id=category_id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Vérifier si le nouveau nom existe (si on change le nom)
    if category_in.name and category_in.name != db_category.name:
        existing_category = category.get_by_name(db, name=category_in.name)
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists"
            )
            
    return category.update(db, db_obj=db_category, obj_in=category_in)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Supprimer une catégorie
    """
    db_category = category.get(db, id=category_id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    category.remove(db, id=category_id)
    return None