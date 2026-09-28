import re
from datetime import datetime, timedelta
from dateutil import parser, tz


def parse_time(text: str):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Invalid datetime string")

    normalized = text.strip().lower().replace(" at ", " ")
    now = datetime.now(tz=tz.tzlocal())

    def is_hour_only(dt_text: str) -> bool:
        if not dt_text:
            return False
        return bool(re.fullmatch(r"\d{1,2}\s*(?:am|pm)", dt_text))

    def coerce_time(dt):
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=tz.tzlocal())

        if is_hour_only(re.sub(r"\b(?:today|tomorrow|day after tomorrow|day after)", "", normalized).strip()):
            dt = dt.replace(minute=0, second=0, microsecond=0)
        return dt

    if "day after" in normalized:
        normalized = normalized.replace("a ", " ", 1)
        repeated = re.findall(r"day after", normalized)
        if repeated and "tomorrow" in normalized:
            day_offset = len(repeated) + 1
            normalized = re.sub(r"(?:day after\s+)+tomorrow", "", normalized).strip()
            dt = parser.parse(normalized or "10pm", default=now.replace(minute=0, second=0, microsecond=0))
            dt = coerce_time(dt)
            return dt + timedelta(days=day_offset)

    if "day after tomorrow" in normalized:
        normalized = normalized.replace("day after tomorrow", "").strip()
        day_offset = 2
        dt = parser.parse(normalized or "10pm", default=now.replace(minute=0, second=0, microsecond=0))
        dt = coerce_time(dt)
        if dt.date() <= (now.date() + timedelta(days=1)):
            dt += timedelta(days=day_offset)
        return dt

    if "tomorrow" in normalized:
        normalized = normalized.replace("tomorrow", "").strip()
        dt = parser.parse(normalized or "10pm", default=now.replace(minute=0, second=0, microsecond=0))
        dt = coerce_time(dt)
        if dt.date() <= now.date():
            dt += timedelta(days=1)
        return dt

    if "today" in normalized:
        normalized = normalized.replace("today", "").strip()
        dt = parser.parse(normalized or "10pm", default=now.replace(minute=0, second=0, microsecond=0))
        return coerce_time(dt)

    dt = parser.parse(normalized, default=now.replace(minute=0, second=0, microsecond=0))
    return coerce_time(dt)