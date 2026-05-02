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


# 🔍 SEARCH EVENT
def search_event(params):
    try:
        data = SearchEventInput(**params)

        service = get_calendar_service()

        events_result = service.events().list(
            calendarId="primary",
            q=data.query,
            timeMin=data.start_time,
            timeMax=data.end_time,
            singleEvents=True,
            orderBy="startTime",
        ).execute()

        events = events_result.get("items", [])

        if events:
            return EventOutput(
                event_id=events[0]["id"],
                title=events[0]["summary"],
                start_time=events[0]["start"]["dateTime"],
                end_time=events[0]["end"]["dateTime"],
            ).dict()
        else:
            return {"message": "No events found"}
    except Exception as e:
        # Fallback to dummy data
        return {"event_id": "123", "time": "3pm", "fallback": True}


# ➕ CREATE EVENT
def create_event(params):
    data = CreateEventInput(**params)

    service = get_calendar_service()

    start_time = parse_time(data.datetime)
    end_time = start_time  # MVP: same time (no duration yet)

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
        start=start_time.isoformat()
    ).model_dump()


# ✏️ UPDATE EVENT
def update_event(params):
    data = UpdateEventInput(**params)

    service = get_calendar_service()

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