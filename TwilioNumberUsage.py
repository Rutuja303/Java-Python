from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timedelta
from app.models.dto.twilio_number_usage_dto import TwilioNumberUsageDto

if TYPE_CHECKING:
    from app.models.twilio_number import TwilioNumber

class TwilioNumberUsage(SQLModel, table=True):
    __tablename__ = 'twilio_number_usage'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_name: Optional[str] = Field(default=None)
    twilio_number_id: Optional[int] = Field(default=None, foreign_key="twilio_number.id")
    last_incoming_call_date: Optional[datetime] = Field(default=None)
    last_outgoing_call_date: Optional[datetime] = Field(default=None)
    last_incoming_sms_date: Optional[datetime] = Field(default=None)
    last_outgoing_sms_date: Optional[datetime] = Field(default=None)
    last_used_more_than_15_days: Optional[bool] = Field(default=None)
    last_used_more_than_30_days: Optional[bool] = Field(default=None)
    last_used_more_than_60_days: Optional[bool] = Field(default=None)
    
    # Relationship
    twilio_number: Optional["TwilioNumber"] = Relationship(back_populates="twilio_number_usage")
    
    def to_dto(self) -> TwilioNumberUsageDto:
        """Convert to DTO"""
        owner_softphone = "~~No User Assigned~~"
        if self.twilio_number and self.twilio_number.user:
            owner_softphone = self.twilio_number.user.get_full_name()
        
        return TwilioNumberUsageDto(
            last_incoming_call_date=self.last_incoming_call_date,
            last_incoming_sms_date=self.last_incoming_sms_date,
            last_outgoing_call_date=self.last_outgoing_call_date,
            last_outgoing_sms_date=self.last_outgoing_sms_date,
            last_used_more_than_15_days=self.last_used_more_than_15_days,
            last_used_more_than_30_days=self.last_used_more_than_30_days,
            last_used_more_than_60_days=self.last_used_more_than_60_days,
            twilio_number=self.twilio_number.phone_number if self.twilio_number else None,
            owner_twilio=self.owner_name,
            owner_softphone=owner_softphone
        )
    
    def set_last_incoming_call_date(self, last_incoming_call_date: datetime) -> None:
        """Set last incoming call date only if it's newer"""
        if (self.last_incoming_call_date is None or 
            self.last_incoming_call_date < last_incoming_call_date):
            self.last_incoming_call_date = last_incoming_call_date
    
    def set_last_outgoing_call_date(self, last_outgoing_call_date: datetime) -> None:
        """Set last outgoing call date only if it's newer"""
        if (self.last_outgoing_call_date is None or 
            self.last_outgoing_call_date < last_outgoing_call_date):
            self.last_outgoing_call_date = last_outgoing_call_date
        else:
            self.last_outgoing_call_date = self.last_outgoing_call_date
    
    def set_last_incoming_sms_date(self, last_incoming_sms_date: datetime) -> None:
        """Set last incoming SMS date only if it's newer"""
        if (self.last_incoming_sms_date is None or 
            self.last_incoming_sms_date < last_incoming_sms_date):
            self.last_incoming_sms_date = last_incoming_sms_date
        else:
            self.last_incoming_sms_date = self.last_incoming_sms_date
    
    def set_last_outgoing_sms_date(self, last_outgoing_sms_date: datetime) -> None:
        """Set last outgoing SMS date only if it's newer"""
        if (self.last_outgoing_sms_date is None or 
            self.last_outgoing_sms_date < last_outgoing_sms_date):
            self.last_outgoing_sms_date = last_outgoing_sms_date
        else:
            self.last_outgoing_sms_date = self.last_outgoing_sms_date
    
    def set_last_used_more_than_15_days(self) -> None:
        """Check if last used more than 15 days ago"""
        last_15_date = datetime.now() - timedelta(days=15)
        self.last_used_more_than_15_days = self._compare_with_datetime(last_15_date)
    
    def set_last_used_more_than_30_days(self) -> None:
        """Check if last used more than 30 days ago"""
        last_month = datetime.now() - timedelta(days=30)
        self.last_used_more_than_30_days = self._compare_with_datetime(last_month)
    
    def set_last_used_more_than_60_days(self) -> None:
        """Check if last used more than 60 days ago"""
        last_2_months = datetime.now() - timedelta(days=60)
        self.last_used_more_than_60_days = self._compare_with_datetime(last_2_months)
    
    def _compare_with_datetime(self, dt: datetime) -> bool:
        """Compare all usage dates with given datetime"""
        return ((self.last_incoming_call_date is None or self.last_incoming_call_date < dt) and
                (self.last_incoming_sms_date is None or self.last_incoming_sms_date < dt) and
                (self.last_outgoing_call_date is None or self.last_outgoing_call_date < dt) and
                (self.last_outgoing_sms_date is None or self.last_outgoing_sms_date < dt))
    
    def __repr__(self):
        return f"<TwilioNumberUsage(id={self.id}, owner_name='{self.owner_name}', twilio_number_id={self.twilio_number_id})>"