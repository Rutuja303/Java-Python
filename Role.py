from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum

class RoleName(str, Enum):
    EMPLOYEE = "EMPLOYEE"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"

class Role(SQLModel, table=True):
    __tablename__ = 'role'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    role: Optional[RoleName] = Field(default=None)
    
    def __repr__(self):
        return f"<Role(id={self.id}, role={self.role})>"