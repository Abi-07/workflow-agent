from pydantic import BaseModel, Field
from typing import Optional


# -------- INPUT SCHEMAS -------- #

class SearchEventInput(BaseModel):
    query: str


class CreateEventInput(BaseModel):
    title: str
    datetime: str
    duration: Optional[int] = 60  # minutes, default 1 hour


class UpdateEventInput(BaseModel):
    event_id: str
    new_datetime: str
    original_datetime: Optional[str] = None  # original event's datetime for preserving date


class CheckAvailabilityInput(BaseModel):
    datetime: str


# -------- OUTPUT SCHEMA -------- #

class EventOutput(BaseModel):
    event_id: str
    title: str
    start: str
    end: Optional[str] = None


class AvailabilityOutput(BaseModel):
    available: bool