from datetime import datetime, timedelta
from dateutil import parser, tz

def parse_time(text: str):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Invalid datetime string")

    normalized = text.strip().lower().replace(" at ", " ")
    now = datetime.now(tz=tz.tzlocal())

    if "tomorrow" in normalized:
        normalized = normalized.replace("tomorrow", "").strip()
        dt = parser.parse(normalized or "10pm", default=now)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=tz.tzlocal())
        if dt.date() <= now.date():
            dt += timedelta(days=1)
        return dt

    if "today" in normalized:
        normalized = normalized.replace("today", "").strip()
        dt = parser.parse(normalized or "10pm", default=now)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=tz.tzlocal())
        return dt

    dt = parser.parse(normalized, default=now)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tz.tzlocal())
    return dt