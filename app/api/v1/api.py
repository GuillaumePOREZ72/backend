from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, categories, templates, projects

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentification"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(templates.router, prefix="/templates", tags=["temlplates"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
