from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from app.models.user import User

class RefreshToken(SQLModel, table=True):
    __tablename__ = 'refresh_token'
    
    id: str = Field(primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    expiration_at: Optional[datetime] = Field(default=None)
    is_valid: Optional[bool] = Field(default=None)
    
    # Relationship (lazy loading is default in SQLModel)
    user: Optional[User] = Relationship(back_populates="refresh_tokens")
    
    def __repr__(self):
        return f"<RefreshToken(id='{self.id}', user_id={self.user_id}, expiration_at={self.expiration_at}, is_valid={self.is_valid})>"