from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship, DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True) # Null pour OAuth
    full_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=False) # Validation email
    is_verified = Column(Boolean, default=False)
    google_id = Column(String, nullable=True) # OAuth Google
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    
    projects = relationship("Project", back_populates="owner")
    user_assets = relationship("UserAsset", back_populates="user")
    shared_projects = relationship("SharedProject", back_populates="shared_with")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    color = Column(String, nullable=True) # HEX color pour l'UI
    icon = Column(String, nullable=True) # Nom de l'icône
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)

    templates = relationship("Template", back_populates="category")

class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    canvas_data = Column(JSON, nullable=False)
    thumbnail_url = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="templates")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    canvas_data = Column(JSON, nullable=False)
    thumbnail_url = Column(String, nullable=True)
    is_public = Column(Boolean, default=False)
    format_type = Column(String, default="A4")  # A4, A5, custom
    width = Column(Float, nullable=True)        # Pour formats custom
    height = Column(Float, nullable=True)       # Pour formats custom
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="projects")
    shared_projects = relationship("SharedProject", back_populates="project")

class UserAsset(Base):
    __tablename__ = "user_assets"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    cloudinary_url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # image, icon, etc.
    file_size = Column(Integer, nullable=False)  # en bytes
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="user_assets")

class SharedProject(Base):
    __tablename__ = "shared_projects"
    
    id = Column(Integer, primary_key=True, index=True)
    permission = Column(String, default="view")  # view, edit, copy
    shared_at = Column(DateTime, default=datetime.utcnow)
    
    project_id = Column(Integer, ForeignKey("projects.id"))
    shared_with_user_id = Column(Integer, ForeignKey("users.id"))
    
    project = relationship("Project", back_populates="shared_projects")
    shared_with = relationship("User", back_populates="shared_projects")