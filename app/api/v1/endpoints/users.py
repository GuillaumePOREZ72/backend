from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps.database import get_db
from app.crud.crud_users import user
from app.schemas.schemas import UserCreate, UserUpdate, UserResponse

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Récupérer tous les utilisateurs avec pagination
    """
    users = user.get_multi(db, skip=skip, limit=limit)
    return users

@router.get("/active", response_model=List[UserResponse])
def get_active_users(db: Session = Depends(get_db)):
    """
    Récupérer uniquement les utilisateurs actifs
    """
    users = user.get_active_users(db)
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupérer un utilisateur par son ID
    """
    db_user = user.get(db, id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Créer un nouvel utilisateur
    """
    # Vérifier si l'email existe déjà
    existing_user = user.get_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return user.create(db, obj_in=user_in)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Supprimer un utilisateur
    """
    db_user = user.get(db, id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user.remove(db, id=user_id)


