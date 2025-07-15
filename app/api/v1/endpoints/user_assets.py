from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.deps.database import get_db
from app.crud.crud_user_asset import user_asset
from app.crud.crud_users import user
from app.schemas.schemas import UserAssetCreate, UserAssetResponse

router = APIRouter()

@router.get("/", response_model=List[UserAssetResponse])
def get_user_assets(
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    file_type: Optional[str] = Query(None, description="Filter by file type"),
    db: Session = Depends(get_db)
):
    """
    Récupérer tous les assets avec filtres optionnels
    """
    if user_id and file_type:
        assets = user_asset.get_user_assets_by_type(db, user_id=user_id, file_type=file_type)
    elif user_id:
        assets = user_asset.get_by_user(db, user_id=user_id)
    elif file_type:
        assets = user_asset.get_by_type(db, file_type=file_type)
    else:
        assets = user_asset.get_multi(db, skip=skip, limit=limit)

    return assets

@router.get("/user/{user_id}", response_model=List[UserAssetResponse])
def get_user_assets_by_user(
    user_id: int,
    file_type: Optional[str] = Query(None, description="Filter by file type"),
    db: Session = Depends(get_db)
):
    """
    Récupérer tous les assets d'un utilisateur
    """
    # Vérifier que l'user existe
    db_user = user.get(db, id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if file_type:
        assets = user_asset.get_user_assets_by_type(db, user_id=user_id, file_type=file_type)
    else:
        assets = user_asset.get_by_user(db, user_id=user_id)

    return assets

@router.get("/type/{file_type}", response_model=List[UserAssetResponse])
def get_assets_by_type(
    file_type: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Récupérer tous les assets par type
    """
    assets = user_asset.get_by_type(db, file_type=file_type)
    return assets

@router.get("/{asset_id}", response_model=UserAssetResponse)
def get_user_asset(
    asset_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupérer un asset par son ID
    """
    db_asset = user_asset.get(db, id=asset_id)
    if not db_asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )
    return db_asset

@router.post("/", response_model=UserAssetResponse, status_code=status.HTTP_201_CREATED)
def create_user_asset(
    asset_in: UserAssetCreate,
    db: Session = Depends(get_db)
):
    """
    Créer un nouvel asset
    """
    return user_asset.create(db, obj_in=asset_in)


@router.put("/{asset_id}", response_model=UserAssetResponse)
def update_user_asset(
    asset_id: int,
    asset_in: UserAssetResponse,
    db: Session = Depends(get_db)
):
    """
    Mettre à jour un asset
    """
    db_asset = user_asset.get(db, id=asset_id)
    if not db_asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )
    return user_asset.update(db, db_obj=db_asset, obj_in=asset_in)

@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_asset(
    asset_id: int,
    db: Session = Depends(get_db)
):
    """
    Supprimer un asset
    """
    db_asset = user_asset.get(db, id=asset_id)
    if not db_asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )
    
    user_asset.remove(db, id=asset_id)
    return None