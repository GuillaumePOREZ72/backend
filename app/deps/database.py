from typing import Generator
from sqlalchemy.orm import Session
from app.core.database import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """
    Dépendance FastAPI pour obtenir une session de base de données.
    Cette fonction sera utilisée dans tous les endpoints pour injecter automatiquement une session DB.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

