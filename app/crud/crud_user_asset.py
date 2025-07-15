from typing import List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import UserAsset
from app.schemas.schemas import UserAssetCreate, UserAssetResponse

class CRUDUserAsset(CRUDBase[UserAsset, UserAssetCreate, UserAssetResponse]):
    def get_by_user(self, db: Session, *, user_id: int) -> List[UserAsset]:
        """Récupérer tous les assets d'un utilisateur"""
        return db.query(UserAsset).filter(UserAsset.user_id == user_id).all()

    def get_by_type(self, db: Session, *, file_type: str) -> List[UserAsset]:
        """Récupérer les assets par type (image, video, audio, document)"""
        return db.query(UserAsset).filter(UserAsset.file_type == file_type).all()

    def get_user_assets_by_type(self, db: Session, *, user_id: int, file_type: str) -> List[UserAsset]:
        """Récupérer les assets d'un utilisateur par type"""
        return db.query(UserAsset).filter(
            UserAsset.user_id == user_id, 
            UserAsset.file_type == file_type
        ).all()

user_asset = CRUDUserAsset(UserAsset)