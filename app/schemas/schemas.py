from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any, List

# === USER SCHEMAS ===
class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    avatar_url: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    google_id: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# === CATEGORY SCHEMAS ===
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    color: Optional[str] = Field(None, pattern=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    icon: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None
    color: Optional[str] = Field(None, pattern=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    icon: Optional[str] = None
    is_active: Optional[bool] = None

class CategoryResponse(CategoryBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# === TEMPLATE SCHEMAS ===
class TemplateBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    canvas_data: Dict[str, Any]
    thumbnail_url: str

class TemplateCreate(TemplateBase): 
    category_id: int

class TemplateUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    canvas_data: Optional[Dict[str, Any]] = None
    thumbnail_url: Optional[str] = None
    category_id: Optional[int] = None
    is_active: Optional[bool] = None

class TemplateResponse(TemplateBase):
    id: int
    category_id: int
    is_active: bool
    created_at: datetime
    category: CategoryResponse

    model_config = ConfigDict(from_attributes=True)

# === PROJECT SCHEMAS ===
class ProjectBase(BaseModel): 
    title: str = Field(..., min_length=1, max_length=100) 
    description: Optional[str] = None 
    canvas_data: Dict[str, Any] 
    is_public: bool = False 
    format_type: str = Field(default="A4", pattern=r'^(A4|A5|custom)$') 
    width: Optional[float] = Field(None, gt=0) 
    height: Optional[float] = Field(None, gt=0)

class ProjectCreate(ProjectBase): 
    pass

class ProjectUpdate(BaseModel): 
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None 
    canvas_data: Optional[Dict[str, Any]] = None 
    thumbnail_url: Optional[str] = None 
    is_public: Optional[bool] = None 
    format_type: Optional[str] = Field(None, pattern=r'^(A4|A5|custom)$') 
    width: Optional[float] = Field(None, gt=0) 
    height: Optional[float] = Field(None, gt=0)

class ProjectResponse(ProjectBase): 
    id: int 
    owner_id: int 
    thumbnail_url: Optional[str] = None 
    created_at: datetime 
    updated_at: datetime 
    owner: UserResponse

    model_config = ConfigDict(from_attributes=True)

# === USER ASSET SCHEMAS ===
class UserAssetBase(BaseModel): 
    filename: str 
    original_filename: str 
    cloudinary_url: str 
    file_type: str 
    file_size: int = Field(..., gt=0)

class UserAssetCreate(UserAssetBase): 
    pass

class UserAssetResponse(UserAssetBase): 
    id: int 
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# === SHARED PROJECT SCHEMAS ===
class SharedProjectBase(BaseModel): 
    permission: str = Field(default="view", pattern=r'^(view|edit|copy)$')

class SharedProjectCreate(SharedProjectBase): 
    project_id: int 
    shared_with_id: int

class SharedProjectResponse(SharedProjectBase): 
    id: int 
    project_id: int 
    shared_with_id: int 
    shared_at: datetime 
    project: ProjectResponse 
    shared_with: UserResponse

    model_config = ConfigDict(from_attributes=True)

# === AUTH SCHEMAS ===
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None

class UserLogin(BaseModel):
    email: str = Field(..., description="Email address")
    password: str = Field(..., min_length=6, description="Password")

class UserRegister(BaseModel):
    email: str = Field(..., description="Email address")
    password: str = Field(..., min_length=6, description="Password")
    full_name: str = Field(..., min_length=2, max_length=100, description="Full name")

class PasswordReset(BaseModel):
    email: str = Field(..., description="Email address")

class PasswordResetConfirm(BaseModel):
    token: str = Field(..., description="Reset token")
    new_password: str = Field(..., min_length=6, description="New password")

class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., description="Refresh token")