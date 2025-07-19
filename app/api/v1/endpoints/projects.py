from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.deps.database import get_db
from app.deps.auth import get_current_active_user
from app.crud.crud_project import project
from app.crud.crud_users import user
from app.schemas.schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from app.models.models import User

router = APIRouter()

@router.get("/", response_model=List[ProjectResponse])
def get_projects(
    skip: int = 0,
    limit: int = 100,
    owner_id: Optional[int] = Query(None, description="Filter by owner ID"),
    format_type: Optional[str] = Query(None, description="Filter by format (A4, A5, custom)"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    public_only: bool = Query(False, description="Show only public projects"),
    db: Session = Depends(get_db)
):
    """
    Récupérer tous les projets avec filtres optionnels
    """
    if search:
        projects = project.search_projects(db, query=search)
    elif owner_id:
        projects = project.get_user_projects(db, owner_id=owner_id, skip=skip, limit=limit)
    elif format_type:
        projects = project.get_by_format(db, format_type=format_type)
    elif public_only:
        projects = project.get_public_projects(db, skip=skip, limit=limit)
    else:
        projects = project.get_multi(db, skip=skip, limit=limit)

    return projects

@router.get("/public", response_model=List[ProjectResponse])
def get_public_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Récupérer uniquement les projets publics
    """
    projects = project.get_public_projects(db, skip=skip, limit=limit)
    return projects

@router.get("/user/{user_id}", response_model=List[ProjectResponse])
def get_user_projects(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Récupérer tous les projets d'un utilisateur
    """
    # Vérifier que l'utilisateur existe
    db_user = user.get(db, id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    projects = project.get_user_projects(db, owner_id=user_id, skip=skip, limit=limit)
    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupérer un projet par son ID
    """
    db_project = project.get(db, id=project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return db_project

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Créer un nouveau projet
    """
    # Forcer l'owner_id à l'utilisateur connecté (sécurité)
    project_data = project_in.model_dump()
    project_data["owner_id"] = current_user.id
    
    return project.create(db, obj_in=ProjectCreate(**project_data))

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_in: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Mettre à jour un projet
    """
    db_project = project.get(db, id=project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Plus tard, avec l'authentification, on vérifiera que l'utilisateur
    # connecté est bien le propriétaire du projet
    
    return project.update(db, db_obj=db_project, obj_in=project_in)

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Supprimer un projet
    """
    db_project = project.get(db, id=project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    project.remove(db, id=project_id)
    return None