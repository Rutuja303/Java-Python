from sqlmodel import SQLModel, Field
from typing import Optional
from app.models.base import AuditableBaseModel
from app.models.dto.NumberDTO import NumberDTO

class Number(AuditableBaseModel, table=True):
    __tablename__ = 'number'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    label: Optional[str] = Field(default=None)
    phoneNumber: Optional[str] = Field(default=None, alias="phone_number")
    
    def to_dto(self) -> NumberDTO:
        return NumberDTO(
            id=self.id,
            label=self.label,
            phoneNumber=self.phoneNumber
        )
    
    def __repr__(self):
        return f"<Number(id={self.id}, label='{self.label}', phoneNumber='{self.phoneNumber}')>"