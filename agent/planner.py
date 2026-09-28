import json
import re
from utils.llm import call_llm
from utils.parser import safe_parse_json
from utils.prompt_loader import load_prompt


def clean_title(raw_text: str) -> str:
    text = raw_text.strip()
    text = re.sub(r'^(please\s+)?(add|schedule|create|set up|book|make)\s+', '', text, flags=re.I)
    text = re.sub(r'\b(today|tomorrow)\b', '', text, flags=re.I).strip()
    text = re.sub(r'\bat\s*\d{1,2}(:\d{2})?\s*(am|pm)?\b', '', text, flags=re.I).strip()
    return text or "Meeting"


def normalize_entities(entities: dict) -> dict:
    normalized = dict(entities or {})

    if "event_name" in normalized and "title" not in normalized:
        normalized["title"] = normalized["event_name"]
    if "event_type" in normalized and "title" not in normalized:
        normalized["title"] = normalized["event_type"]
    if "meeting_with" in normalized and "title" not in normalized:
        normalized["title"] = f"{normalized.get('event_type', 'Meeting')} with {normalized['meeting_with']}"
    if "event_time" in normalized and "time" not in normalized:
        normalized["time"] = normalized["event_time"]
    if "event_date" in normalized and "date" not in normalized:
        normalized["date"] = normalized["event_date"]

    # Extract duration from title or other fields
    if "duration" not in normalized:
        duration_match = None
        text_to_check = normalized.get("title", "") + " " + normalized.get("raw_input", "")
        
        # Look for patterns like "30 minute", "2 hour", "1.5 hr", etc.
        import re
        duration_patterns = [
            r'(\d+(?:\.\d+)?)\s*(?:hour|hr)s?\b',  # hours
            r'(\d+(?:\.\d+)?)\s*(?:minute|min)s?\b',  # minutes
        ]
        
        for pattern in duration_patterns:
            match = re.search(pattern, text_to_check, re.I)
            if match:
                value = float(match.group(1))
                if 'hour' in pattern or 'hr' in pattern:
                    normalized["duration"] = int(value * 60)  # convert hours to minutes
                else:
                    normalized["duration"] = int(value)  # minutes
                break

    if "datetime" not in normalized:
        if normalized.get("date") and normalized.get("time"):
            normalized["datetime"] = f"{normalized['date']} {normalized['time']}"
        elif normalized.get("time"):
            normalized["datetime"] = normalized["time"]
    return normalized


def validate_step(step: dict) -> bool:
    return (
        isinstance(step, dict)
        and "id" in step
        and "tool" in step
        and "input" in step
    )


def fallback_plan(intent: dict) -> list[dict]:
    intent_name = intent.get("intent")
    entities = normalize_entities(intent.get("entities", {}) or {})
    raw_input = intent.get("raw_input", "")

    if intent_name == "create_event":
        title = entities.get("title") or clean_title(raw_input)
        datetime_value = entities.get("datetime") or f"{entities.get('date', 'today')} {entities.get('time', '4pm')}"
        duration = entities.get("duration", 60)  # default 1 hour
        return [
            {
                "id": 1,
                "tool": "calendar.create_event",
                "input": {
                    "title": title,
                    "datetime": datetime_value,
                    "duration": duration,
                },
            }
        ]

    if intent_name == "update_event":
        query = entities.get("target_event") or entities.get("title") or "meeting"
        new_datetime = entities.get("datetime") or f"{entities.get('date', 'today')} {entities.get('time', '4pm')}"
        return [
            {
                "id": 1,
                "tool": "calendar.search_event",
                "input": {"query": query},
            },
            {
                "id": 2,
                "tool": "calendar.update_event",
                "input": {
                    "event_id": "$step_1.event_id",
                    "new_datetime": new_datetime,
                    "original_datetime": "$step_1.start",
                },
            },
        ]

    if intent_name == "search_event":
        query = entities.get("query") or entities.get("title") or "meeting"
        return [
            {
                "id": 1,
                "tool": "calendar.search_event",
                "input": {"query": query},
            }
        ]

    if intent_name == "check_availability":
        datetime_value = entities.get("datetime") or f"{entities.get('date', 'today')} {entities.get('time', 'now')}"
        return [
            {
                "id": 1,
                "tool": "calendar.check_availability",
                "input": {"datetime": datetime_value},
            }
        ]

    return []

def create_plan(intent: dict, state):
    # For now, always use fallback planning to avoid LLM timeouts
    return fallback_plan(intent)