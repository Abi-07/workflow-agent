from agent.intent_parser import parse_intent
from agent.planner import create_plan
from agent.executor import execute_step
from agent.replanner import replan
from agent.response import generate_response
from agent.state import AgentState

MUTATING_TOOLS = [
    "calendar.create_event",
    "calendar.update_event",
]


def requires_confirmation(step: dict) -> bool:
    return step["tool"] in MUTATING_TOOLS


def ask_for_confirmation(step: dict) -> str:
    return f"⚠️ पुष्टि करें: Do you want to execute {step['tool']} with {step['input']}? (yes/no)"


def safe_intent_parse(user_input, state):
    for _ in range(state.max_retries):
        intent = parse_intent(user_input)

        if intent and "intent" in intent:
            return intent

    raise Exception("Intent parsing failed")


def validate_step(step: dict) -> bool:
    return (
        "tool" in step and
        "input" in step
    )

def safe_execute(step, state):
    for attempt in range(state.max_retries):
        result = execute_step(step, state)

        if not result.get("error"):
            return result

    return {"error": "execution_failed_after_retries"}

def is_finished(state):
    return (
        state.status == "failed" or
        state.current_step >= len(state.plan)
    )

def run_agent(user_input: str, state: AgentState = None):
    if state is None:
        state = AgentState(user_input)
    else:
        state.user_input = user_input

    try:
        if state.awaiting_confirmation:
            answer = user_input.strip().lower()
            if answer in ("yes", "y"):
                step = state.pending_action
                state.awaiting_confirmation = False
                state.pending_action = None

                result = safe_execute(step, state)
                state.tool_results.append(result)

                if result.get("error"):
                    state = replan(state, result)
                else:
                    state.current_step += 1
            elif answer in ("no", "n"):
                state.status = "failed"
                return state, "❌ Action canceled."
            else:
                return state, "Please answer yes or no."

        if not state.plan:
            state.intent = safe_intent_parse(user_input, state)
            state.plan = create_plan(state.intent)

        while not is_finished(state):
            if state.current_step >= len(state.plan):
                break

            step = state.plan[state.current_step]

            if not validate_step(step):
                return state, "❌ Invalid plan step detected."

            if requires_confirmation(step) and not state.awaiting_confirmation:
                state.awaiting_confirmation = True
                state.pending_action = step
                return state, ask_for_confirmation(step)

            result = safe_execute(step, state)
            state.tool_results.append(result)

            if result.get("error"):
                state = replan(state, result)
                continue

            state.current_step += 1

        state.status = "completed"
        return state, generate_response(state)

    except Exception as e:
        return state, f"❌ Fatal error: {str(e)}"