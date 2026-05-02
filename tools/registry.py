from tools.calendar.actions import (
    search_event,
    create_event,
    update_event,
    check_availability,
)

TOOLS = {
    "calendar.search_event": search_event,
    "calendar.create_event": create_event,
    "calendar.update_event": update_event,
    "calendar.check_availability": check_availability,
}