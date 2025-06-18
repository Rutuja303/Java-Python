from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, Set, List, Collection, TYPE_CHECKING
from app.models.base import AuditableBaseModel
from app.models.dto.user_dto import UserDto
from app.models.enums.job_type import JobType

if TYPE_CHECKING:
    from app.models.twilio_number import TwilioNumber
    from app.models.role import Role
    from app.models.directory.contact import Contact
    from app.models.company import Company

class User(AuditableBaseModel, table=True):
    __tablename__ = 'users'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    firstName: Optional[str] = Field(default=None, alias="first_name")
    lastName: Optional[str] = Field(default=None, alias="last_name")
    email: Optional[str] = Field(default=None, unique=True)
    password: Optional[str] = Field(default=None)
    jobType: Optional[JobType] = Field(default=None, alias="job_type")
    company: Optional[str] = Field(default=None)
    role: Optional[int] = Field(default=None, foreign_key="role.id", alias="role_id")
    profilePic: Optional[str] = Field(default=None, alias="profile_pic")
    isEnabled: bool = Field(default=True, alias="is_enabled")
    voicemailS3Key: Optional[str] = Field(default=None, alias="voicemail_s3_key")
    isVoiceMailEnabled: Optional[bool] = Field(default=None, alias="is_voice_mail_enabled")
    
    # Relationships
    twilioNumbers: Set["TwilioNumber"] = Relationship(back_populates="user", cascade_delete=True)
    role: Optional["Role"] = Relationship(back_populates="users")
    contacts: Set["Contact"] = Relationship(back_populates="user", cascade_delete=True)
    companies: Set["Company"] = Relationship(
        back_populates="users", 
        link_table="user_company"
    )

    def disableVoiceMail(self) -> None:
        """Disable voicemail and clear S3 key"""
        self.isVoiceMailEnabled = False
        self.voicemailS3Key = None

    def enableVoiceMail(self, s3_key: str) -> None:
        """Enable voicemail with S3 key"""
        self.isVoiceMailEnabled = True
        self.voicemailS3Key = s3_key

    def to_dto(self) -> UserDto:
        """Convert to DTO"""
        return UserDto(
            id=self.id,
            email=self.email,
            firstName=self.firstName,
            lastName=self.lastName,
            company=self.company,
            jobType=self.jobType,
            isVoiceMailEnabled=self.isVoiceMailEnabled,
            companies=[company.to_dto() for company in self.companies] if self.companies else [],
            twilioNumbers={
                twilio_number.to_dto(exclude_actor_data=True) 
                for twilio_number in self.twilioNumbers
            } if self.twilioNumbers else set(),
            roleName=self.role.role if self.role else None,
            isEnabled=self.isEnabled
        )
    
    def set_twilio_numbers(self, twilio_numbers: Optional[Set["TwilioNumber"]]) -> None:
        """Set twilio numbers with proper cleanup"""
        if hasattr(self, 'twilioNumbers') and self.twilioNumbers:
            self.twilioNumbers.clear()

        if twilio_numbers:
            if not hasattr(self, 'twilioNumbers'):
                self.twilioNumbers = set()
            self.twilioNumbers.update(twilio_numbers)

    def get_full_name(self) -> str:
        """Get full name by combining first and last name"""
        return f"{self.firstName or ''} {self.lastName or ''}".strip()

    def disable_account(self) -> None:
        """Disable account and unassign all twilio numbers"""
        self.isEnabled = False
        if self.twilioNumbers:
            for twilio_number in self.twilioNumbers:
                twilio_number.un_assign()
    
    def set_companies(self, companies: Optional[Collection["Company"]]) -> None:
        """Set companies with proper bidirectional relationship management"""
        if companies is not None:
            # Remove this user from existing companies
            if hasattr(self, 'companies') and self.companies:
                for company in self.companies:
                    if hasattr(company, 'users') and company.users and self in company.users:
                        company.users.remove(self)
                self.companies.clear()
            
            # Add to new companies
            if not hasattr(self, 'companies'):
                self.companies = set()
            
            self.companies.update(companies)
            
            # Add this user to the new companies
            for company in self.companies:
                if not hasattr(company, 'users'):
                    company.users = set()
                company.users.add(self)
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', full_name='{self.get_full_name()}')>"