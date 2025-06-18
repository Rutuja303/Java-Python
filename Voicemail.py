from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from app.schemas.voicemail import VoicemailDTO
from app.utils.date_utility import convert_ms


class Voicemail(SQLModel, table=True):
    __tablename__ = "voicemail"

    id: str = Field(primary_key=True, index=True)
    date_created: Optional[datetime] = None
    media_url: Optional[str] = None
    from_number: Optional[str] = None
    to_number: Optional[str] = None
    duration: Optional[str] = None
    status: Optional[str] = None
    call_sid: Optional[str] = None
    transcription_sid: Optional[str] = None

    should_post_on_slack: bool = Field(default=False)
    has_posted_on_slack: bool = Field(default=False)

    def to_dto(self) -> VoicemailDTO:
        return VoicemailDTO(
            id=self.id,
            media_url=self.media_url,
            is_transcript_available=bool(self.transcription_sid),
            date_created=self.date_created,
            from_number=self.from_number,
            duration=convert_ms(int(self.duration)) if self.duration else None,
        )

    def to_slack_message_dict(self) -> dict:
        return {
            "voicemail_url": self.media_url,
            "caller": self.from_number,
            "callee": self.to_number,
        }
