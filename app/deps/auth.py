from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.security import verify_token
from app.deps.database import get_db
from app.crud.crud_users import user
from app.models.models import User


# Configuration du schéma de sécurité Bearer
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dépendance pour obtenir l'utilisateur actuel depuis le token JWT
    """
    # Extraire le token
    token = credentials.credentials

    # Vérifier le token
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extraire l'ID utilisateur du payload
    user_id: int = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Récupérer l'utilisateur depuis la base de données
    db_user = user.get(db, id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return db_user

def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dépendance pour s'assurer que l'utilisateur est actif
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Dépendance optionnelle - utilisateur peut être None
    Utile pour les endpoints qui fonctionnent avec ou sans auth
    """
    if not credentials:
        return None
    
    try:
        return get_current_user(credentials, db)
    except HTTPException:
        return None

