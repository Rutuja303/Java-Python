from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from app.schemas.voicemail import VoicemailDTO
from app.utils.date_utility import convert_ms


class Voicemail(SQLModel, table=True):
    __tablename__ = "voicemail"

    id: str = Field(primary_key=True, index=True)
    dateCreated: Optional[datetime] = None
    mediaUrl: Optional[str] = Field(default=None, alias="media_url")
    fromNumber: Optional[str] = Field(default=None, alias="from_number")
    toNumber: Optional[str] = Field(default=None, alias="to_number")
    duration: Optional[str] = Field(default=None, alias="duration")
    status: Optional[str] = Field(default=None, alias="status")
    callSid: Optional[str] = Field(default=None, alias="call_sid")
    transcriptionSid: Optional[str] = Field(default=None, alias="transcription_sid")

    shouldPostOnSlack: bool = Field(default=False, alias="should_post_on_slack")
    hasPostedOnSlack: bool = Field(default=False, alias="has_posted_on_slack")

    def to_dto(self) -> VoicemailDTO:
        return VoicemailDTO(
            id=self.id,
            media_url=self.mediaUrl,
            is_transcript_available=bool(self.transcriptionSid),
            date_created=self.dateCreated,
            from_number=self.fromNumber,
            duration=convert_ms(int(self.duration)) if self.duration else None,
        )

    def to_slack_message_dict(self) -> dict:
        return {
            "voicemail_url": self.mediaUrl,
            "caller": self.fromNumber,
            "callee": self.toNumber,
        }
