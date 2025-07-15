from fastapi import APIRouter
from app.api.v1.endpoints import categories, templates, users, projects, user_assets, shared_projects

api_router = APIRouter()

api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(templates.router, prefix="/templates", tags=["templates"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(user_assets.router, prefix="/user-assets", tags=["user-assets"])
api_router.include_router(shared_projects.router, prefix="/shared-projects", tags=["shared-projects"])
