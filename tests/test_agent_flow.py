from datetime import datetime, timedelta

from agent.loop import run_agent
from agent.state import AgentState
from utils.time import parse_time


def test_basic_flow():
    result = run_agent("Move my 3pm meeting to tomorrow")
    assert result is not None


def test_hour_only_time_is_exact():
    value = parse_time("8am tomorrow")
    assert value.hour == 8
    assert value.minute == 0
    assert value.second == 0


def test_day_after_tomorrow_is_parsed():
    value = parse_time("4pm day after tomorrow")
    assert value.hour == 16
    assert value.minute == 0
    assert value.second == 0
    assert value.date() == (datetime.now() + timedelta(days=2)).date()


def test_a_day_after_day_after_tomorrow_is_parsed():
    value = parse_time("a day after day after tomorrow")
    assert value.date() == (datetime.now() + timedelta(days=3)).date()
    assert value.hour == 22
    assert value.minute == 0
    assert value.second == 0


def test_update_without_match_falls_back_to_create(monkeypatch):
    state = AgentState("move gym to 8am tomorrow")
    state.intent = {
        "intent": "update_event",
        "entities": {
            "target_event": "gym",
            "datetime": "8am tomorrow",
            "duration": 60,
        },
    }
    state.plan = [{
        "id": 1,
        "tool": "calendar.create_event",
        "input": {"title": "gym", "datetime": "8am tomorrow", "duration": 60},
    }]
    state.awaiting_confirmation = True
    state.pending_action = state.plan[0]

    calls = []

    def fake_safe_execute(step, current_state):
        calls.append(step)
        return {"result": {"id": "abc123", "summary": "gym", "status": "created"}}

    monkeypatch.setattr("agent.loop.safe_execute", fake_safe_execute)

    new_state, response = run_agent("yes", state)

    assert new_state.status == "completed"
    assert calls and calls[0]["tool"] == "calendar.create_event"
    assert "gym" in response.lower()