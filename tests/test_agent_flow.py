from agent.loop import run_agent

def test_basic_flow():
    result = run_agent("Move my 3pm meeting to tomorrow")
    assert result is not None