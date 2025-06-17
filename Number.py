from sqlmodel import SQLModel, Field
from typing import Optional
from app.models.base import AuditableBaseModel
from app.models.dto.number_dto import NumberDTO

class Number(AuditableBaseModel, table=True):
    __tablename__ = 'number'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    label: Optional[str] = Field(default=None)
    phone_number: Optional[str] = Field(default=None)
    
    def to_dto(self) -> NumberDTO:
        return NumberDTO(
            id=self.id,
            label=self.label,
            phone_number=self.phone_number
        )
    
    def __repr__(self):
        return f"<Number(id={self.id}, label='{self.label}', phone_number='{self.phone_number}')>"