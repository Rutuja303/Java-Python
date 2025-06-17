from typing import Optional
from app.models.email_request import EmailRequest
from app.models.enums.event_type import EventType

class OTPRequest(EmailRequest):
    def __init__(self, event: Optional[EventType] = None, email_to: Optional[str] = None, 
                 name: Optional[str] = None, otp: Optional[str] = None):
        super().__init__(event, email_to)
        self.name = name
        self.otp = otp
    
    @property
    def name(self) -> Optional[str]:
        return self._name
    
    @name.setter
    def name(self, value: Optional[str]):
        self._name = value
    
    @property
    def otp(self) -> Optional[str]:
        return self._otp
    
    @otp.setter
    def otp(self, value: Optional[str]):
        self._otp = value
    
    def __repr__(self):
        return f"<OTPRequest(event={self.event}, email_to='{self.email_to}', name='{self.name}', otp='{self.otp}')>"