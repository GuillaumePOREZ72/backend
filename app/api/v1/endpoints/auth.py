from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.deps.database import get_db
from app.deps.auth import get_current_active_user
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.crud.crud_users import user
from app.schemas.schemas import (
    UserLogin,
    UserRegister,
    UserResponse,
    Token,
    RefreshToken,
    UserCreate
)

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserRegister,
    db: Session(get_db)
):
    """
    Inscription d'un nouvel utilisateur
    """
    # Vérifier si l'email existe déjà
    existing_user = user.get_by_email(db, email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hacher le mot de passe
    hashed_password = get_password_hash(user_data.password)

    # Créer l'utilisateur
    user_create = UserCreate(
        email=user_data.email,
        full_name=user_data.full_name,
        password_hash=hashed_password,
        is_active=True
    )

    db_user = user.create(db, obj_in=user_create)
    return db_user


@router.post("/login", response_model=Token)
def login(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Connexion d'un utilisateur
    """
    # Récupérer l'utilisateur par email
    db_user = user.get_by_email(db, email=user_credentials.email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Vérifier le mot de passe
    if not verify_password(user_credentials.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Vérifier que l'utilisateur est actif
    if not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    # Créer les tokens
    access_token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(
        data={"sub": str(db_user.id)}
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/refresh", response_model=Token)
def refresh_token(
    refresh_data: RefreshToken,
    db: Session = Depends(get_db)
):
    """
    Rafraîchir le token d'accès
    """
    # Vérifier le refresh token
    payload = verify_token(refresh_data.refresh_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Extraire l'ID utilisateur
    user_id = payload.get("sub")
    if user_id is Noe:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    # Vérifier que l'utilisateur existe toujours
    db_user = user.get(db, id=int(user_id))
    if db_user is None or not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    # Créer de nouveaux tokens
    access_token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(
        data={"sub": str(db_user.id)}
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )
