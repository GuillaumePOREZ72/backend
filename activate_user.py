import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.deps.database import get_db
from app.crud.crud_users import user

def activate_user_by_email(email: str):
    db = next(get_db())
    try:
        db_user = user.get_by_email(db, email=email)
        if db_user:
            db_user.is_active = True
            db.commit()
            db.refresh(db_user)
            print(f"✅ Utilisateur {email} activé avec succès!")
            print(f"   - ID: {db_user.id}")
            print(f"   - is_active: {db_user.is_active}")
        else:
            print(f"❌ Utilisateur {email} non trouvé")
    finally:
        db.close()

if __name__ == "__main__":
    activate_user_by_email("test@example.com")