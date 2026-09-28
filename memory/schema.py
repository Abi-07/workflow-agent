from pydantic import BaseModel
from typing import Optional, Dict


class UserPreferences(BaseModel):
    default_meeting_duration: Optional[int] = 60  # minutes
    preferred_morning_time: Optional[str] = "9:00"
    timezone: Optional[str] = "UTC"


class MemoryData(BaseModel):
    preferences: UserPreferences = UserPreferences()
    last_events: Dict[str, str] = {}  # title → event_id