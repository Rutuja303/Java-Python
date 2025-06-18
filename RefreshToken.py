from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from app.models.user import User

class RefreshToken(SQLModel, table=True):
    __tablename__ = 'refresh_token'
    id: str = Field(primary_key=True)
    user: Optional[int] = Field(default=None, foreign_key="user.id")
    expirationAt: Optional[datetime] = Field(default=None)
    isValid: Optional[bool] = Field(default=None, alias="is_valid")

    # Relationship (lazy loading is default in SQLModel)
    user: Optional[User] = Relationship(back_populates="refresh_tokens")
    
    def __repr__(self):
        return f"<RefreshToken(id='{self.id}', user_id={self.user_id}, expiration_at={self.expiration_at}, is_valid={self.is_valid})>"