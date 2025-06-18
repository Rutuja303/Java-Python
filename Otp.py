from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from app.models.user import User

class Otp(SQLModel, table=True):
    __tablename__ = 'otp'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user: Optional[int] = Field(default=None, foreign_key="user.id")
    value: Optional[str] = Field(default=None)
    validUntil: Optional[datetime] = Field(default=None, alias="valid_until")
    verified: Optional[bool] = Field(default=None)
    verifiedAt: Optional[datetime] = Field(default=None, alias="verified_at")
    
    # Relationship (lazy loading is default in SQLModel)
    user: Optional[User] = Relationship(back_populates="otp")
    
    def __repr__(self):
        return f"<Otp(id={self.id}, user_id={self.user_id}, value='{self.value}', verified={self.verified})>"
