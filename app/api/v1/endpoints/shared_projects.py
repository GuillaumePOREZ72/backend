from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.deps.database import get_db
from app.crud.crud_shared_project import shared_project
from app.crud.crud_users import user
from app.crud.crud_project import project
from app.schemas.schemas import SharedProjectCreate, SharedProjectResponse

router = APIRouter()

@router.get("/", response_model=List[SharedProjectResponse])
def get_shared_projects(
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    permission: Optional[str] = Query(None, description="Filter by permission"),
    db: Session = Depends(get_db)
):
    """
    Récupérer tous les projets partagés avec filtres optionnels
    """
    if user_id:
        shares = shared_project.get_by_user(db, user_id=user_id)
    elif project_id:
        shares = shared_project.get_by_project(db, project_id=project_id)
    elif permission:
        shares = shared_project.get_by_permission(db, permission=permission)
    else:
        shares = shared_project.get_multi(db, skip=skip, limit=limit)
    
    return shares

@router.get("/user/{user_id}", response_model=List[SharedProjectResponse])
def get_user_shared_projects(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupérer tous les projets partagés avec un utilisateur
    """
    # Vérifier que l'utilisateur existe
    db_user = user.get(db, id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    shares = shared_project.get_by_user(db, user_id=user_id)
    return shares

@router.get("/project/{project_id}", response_model=List[SharedProjectResponse])
def get_project_shares(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupérer tous les partages d'un projet
    """
    # Vérifier que le projet existe
    db_project = project.get(db, id=project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    shares = shared_project.get_by_project(db, project_id=project_id)
    return shares

@router.get("/permission/{user_id}/{project_id}", response_model=SharedProjectResponse)
def get_user_project_permission(
    user_id: int,
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupérer la permission d'un utilisateur sur un projet
    """
    permission = shared_project.get_user_project_permission(db, user_id=user_id, project_id=project_id)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )
    return permission

@router.get("/{share_id}", response_model=SharedProjectResponse)
def get_shared_project(
    share_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupérer un partage par son ID
    """
    db_share = shared_project.get(db, id=share_id)
    if not db_share:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shared project not found"
        )
    return db_share

@router.post("/", response_model=SharedProjectResponse, status_code=status.HTTP_201_CREATED)
def create_shared_project(
    share_in: SharedProjectCreate,
    db: Session = Depends(get_db)
):
    """
    Créer un nouveau partage de projet
    """
    # Vérifier que l'utilisateur existe
    db_user = user.get(db, id=share_in.shared_with_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
        )
    
    # Vérifier que le projet existe
    db_project = project.get(db, id=share_in.project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project not found"
        )
    
    # Vérifier qu'il n'existe pas déjà un partage
    existing_share = shared_project.get_user_project_permission(
        db, user_id=share_in.shared_with_id, project_id=share_in.project_id
    )
    if existing_share:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project already shared with this user"
        )
    
    return shared_project.create(db, obj_in=share_in)

@router.put("/{share_id}", response_model=SharedProjectResponse)
def update_shared_project(
    share_id: int,
    share_in: SharedProjectResponse,
    db: Session = Depends(get_db)
):
    """
    Mettre à jour un partage de projet
    """
    db_share = shared_project.get(db, id=share_id)
    if not db_share:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shared project not found"
        )
    
    return shared_project.update(db, db_obj=db_share, obj_in=share_in)

@router.delete("/{share_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shared_project(
    share_id: int,
    db: Session = Depends(get_db)
):
    """
    Supprimer un partage de projet
    """
    db_share = shared_project.get(db, id=share_id)
    if not db_share:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shared project not found"
        )
    
    shared_project.remove(db, id=share_id)
    return None
