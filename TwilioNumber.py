from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, Set, TYPE_CHECKING
from app.models.base import AuditableBaseModel
from app.models.dto.twilio_number_dto import TwilioNumberDto
from app.models.dto.twilio_forward_dto import TwilioForwardDto
from app.models.dto.actor import Actor
from app.models.dto.conference_dto import ConferenceDto
from app.models.dto.user_dto import UserDto
from app.models.dto.support_line_dto import SupportLineDto
from app.models.enums.active_association import ActiveAssociation
from app.utils.twilio_utility import is_phone_number
from app.exceptions.validation_exception import ValidationException

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.twilio_number_usage import TwilioNumberUsage
    from app.models.conference.room import Room
    from app.models.call_redirect import CallRedirect
    from app.models.call_level import CallLevel

class TwilioNumber(AuditableBaseModel, table=True):
    __tablename__ = 'twilio_number'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    phone_number: Optional[str] = Field(default=None, max_length=13, unique=True)
    forwarded_number: Optional[str] = Field(default=None, max_length=13)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    is_deleted: bool = Field(default=False)
    is_forwarded: bool = Field(default=False)
    is_room_associated: bool = Field(default=False)
    is_support_number: bool = Field(default=False)
    voicemail_s3_key: Optional[str] = Field(default=None)
    is_voice_mail_enabled: bool = Field(default=False)
    
    # Relationships
    user: Optional["User"] = Relationship(back_populates="twilio_numbers")
    twilio_number_usage: Optional["TwilioNumberUsage"] = Relationship(back_populates="twilio_number")
    room: Optional["Room"] = Relationship(back_populates="moderator")
    redirect: Optional["CallRedirect"] = Relationship(back_populates="call_to")
    call_level_set: Set["CallLevel"] = Relationship(back_populates="twilio_numbers", link_table="call_level_twilio_number")
    
    def disable_voice_mail(self) -> None:
        """Disable voicemail and clear S3 key"""
        self.is_voice_mail_enabled = False
        self.voicemail_s3_key = None
    
    def enable_voice_mail(self, s3_key: str) -> None:
        """Enable voicemail with S3 key"""
        self.is_voice_mail_enabled = True
        self.voicemail_s3_key = s3_key
    
    def update_forwarding(self, forward_dto: TwilioForwardDto) -> None:
        """Update forwarding settings based on DTO"""
        if forward_dto.forward_to and is_phone_number(forward_dto.forward_to):
            self.forwarded_number = forward_dto.forward_to
            self.is_forwarded = forward_dto.is_enabled
        else:
            self.forwarded_number = None
            self.is_forwarded = False
    
    def to_dto(self, exclude_actor_data: bool = False) -> TwilioNumberDto:
        """Convert to DTO"""
        return TwilioNumberDto(
            id=self.id,
            phone_number=self.phone_number,
            forwarded_number=self.forwarded_number,
            is_forwarded=self.is_forwarded,
            active_association=self._get_active_association(),
            actor=self._get_actor(exclude_actor_data),
            last_usage_report=self.twilio_number_usage.to_dto() if self.twilio_number_usage else None,
            is_voice_mail_enabled=self.is_voice_mail_enabled
        )
    
    def _get_active_association(self) -> ActiveAssociation:
        """Get the active association type"""
        if not self._is_assigned():
            return ActiveAssociation.NONE
        
        if self.is_room_associated:
            return ActiveAssociation.CONFERENCE
        elif self.is_support_number:
            return ActiveAssociation.SUPPORT
        else:
            return ActiveAssociation.USER
    
    def _get_actor(self, exclude_actor_data: bool = False) -> Optional[Actor]:
        """Get the actor based on active association"""
        association = self._get_active_association()
        
        if association == ActiveAssociation.CONFERENCE:
            if self.room:
                return ConferenceDto(
                    id=self.room.id,
                    title=self.room.room_name
                )
        elif association == ActiveAssociation.USER:
            if self.user and not exclude_actor_data:
                return UserDto(
                    id=self.user.id,
                    first_name=self.user.first_name,
                    last_name=self.user.last_name
                )
        elif association == ActiveAssociation.SUPPORT:
            if self.redirect:
                return SupportLineDto(
                    id=self.redirect.id,
                    title=self.redirect.name
                )
        
        return None
    
    def _is_assigned(self) -> bool:
        """Check if the number is assigned"""
        return (self.user is not None or 
                self.is_support_number or 
                self.is_room_associated)
    
    def un_assign(self) -> None:
        """Unassign the number"""
        self.user = None
        self.user_id = None
        self.is_forwarded = False
        self.forwarded_number = None
    
    def assign_user(self, user: "User") -> None:
        """Assign number to a user"""
        self.user = user
        self.user_id = user.id
    
    def is_redirect_assignable(self) -> bool:
        """Check if number can be assigned for redirect"""
        return (not self.is_room_associated and 
                self.user is None)
    
    def mark_redirected(self) -> None:
        """Mark number as redirected/support number"""
        if self.is_redirect_assignable():
            self.is_support_number = True
        else:
            raise ValidationException("Number is not assignable.")
    
    def mark_deleted(self) -> None:
        """Mark number as deleted and unassign"""
        self.is_deleted = True
        self.un_assign()
    
    def __repr__(self):
        return f"<TwilioNumber(id={self.id}, phone_number='{self.phone_number}', is_deleted={self.is_deleted})>"