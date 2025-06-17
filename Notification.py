from sqlmodel import SQLModel, Field
from typing import Optional
from app.models.base import AuditableBaseModel

class Notification(AuditableBaseModel, table=True):
    __tablename__ = 'notification'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    actor: Optional[str] = Field(default=None)
    notifier: Optional[str] = Field(default=None)
    entity: Optional[str] = Field(default=None)
    entity_type: Optional[str] = Field(default=None)
    is_read: Optional[bool] = Field(default=None)
    
    def __repr__(self):
        return f"<Notification(id={self.id}, actor='{self.actor}', notifier='{self.notifier}', entity='{self.entity}', entity_type='{self.entity_type}', is_read={self.is_read})>"