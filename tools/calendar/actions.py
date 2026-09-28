from tools.calendar.client import get_calendar_service
from tools.calendar.schema import (
    SearchEventInput,
    CreateEventInput,
    UpdateEventInput,
    CheckAvailabilityInput,
    EventOutput,
    AvailabilityOutput,
)
from utils.time import parse_time
from datetime import timedelta


# 🔍 SEARCH EVENT
def search_event(params):
    data = SearchEventInput(**params)

    service = get_calendar_service()

    events_result = service.events().list(
        calendarId="primary",
        q=data.query,
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    events = events_result.get("items", [])

    if events:
        return EventOutput(
            event_id=events[0]["id"],
            title=events[0]["summary"],
            start=events[0]["start"]["dateTime"],
            end=events[0]["end"]["dateTime"],
        ).dict()
    else:
        return {"message": "No events found"}


# ➕ CREATE EVENT
def create_event(params):
    data = CreateEventInput(**params)

    service = get_calendar_service()

    start_time = parse_time(data.datetime)
    end_time = start_time + timedelta(minutes=data.duration)

    event_body = {
        "summary": data.title,
        "start": {"dateTime": start_time.isoformat()},
        "end": {"dateTime": end_time.isoformat()},
    }

    event = service.events().insert(
        calendarId="primary",
        body=event_body
    ).execute()

    return EventOutput(
        event_id=event["id"],
        title=data.title,
        start=start_time.isoformat(),
        end=end_time.isoformat()
    ).model_dump()


# ✏️ UPDATE EVENT
def update_event(params):
    import re
    data = UpdateEventInput(**params)

    service = get_calendar_service()

    # If the new datetime is only a time (without a relative date or explicit date),
    # keep the original event date and replace only the time portion.
    has_date_context = re.search(
        r'\b(day after tomorrow|tomorrow|today|yesterday|\d{1,2}[-/]\d{1,2}|january|february|march|april|may|june|july|august|september|october|november|december)\b',
        data.new_datetime,
        re.I,
    )

    if data.original_datetime and not has_date_context:
        original_dt = parse_time(data.original_datetime)
        new_time_dt = parse_time(data.new_datetime)
        new_time = original_dt.replace(
            hour=new_time_dt.hour,
            minute=new_time_dt.minute,
            second=0,
            microsecond=0,
        )
    else:
        new_time = parse_time(data.new_datetime)

    event = service.events().get(
        calendarId="primary",
        eventId=data.event_id
    ).execute()

    event["start"]["dateTime"] = new_time.isoformat()
    event["end"]["dateTime"] = new_time.isoformat()

    updated = service.events().update(
        calendarId="primary",
        eventId=data.event_id,
        body=event
    ).execute()

    return {
        "status": "updated",
        "event_id": updated["id"]
    }


# 📅 CHECK AVAILABILITY
def check_availability(params):
    data = CheckAvailabilityInput(**params)

    service = get_calendar_service()

    time = parse_time(data.datetime)

    events_result = service.events().list(
        calendarId="primary",
        timeMin=time.isoformat(),
        timeMax=time.isoformat(),
        maxResults=1,
        singleEvents=True,
    ).execute()

    events = events_result.get("items", [])

    return AvailabilityOutput(
        available=len(events) == 0
    ).model_dump()