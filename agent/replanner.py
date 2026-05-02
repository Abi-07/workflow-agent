from utils.llm import call_llm
from utils.parser import safe_parse_json
from utils.prompt_loader import load_prompt


def replan(state, error):
    template = load_prompt("prompts/replanner_prompt.txt")

    prompt = template \
        .replace("__PLAN__", str(state.plan)) \
        .replace("__FAILED_STEP__", str(state.plan[state.current_step])) \
        .replace("__ERROR__", str(error))

    raw = call_llm(prompt)

    parsed = safe_parse_json(raw)

    if "steps" in parsed:
        state.plan = parsed["steps"]
        state.current_step = 0
        return state

    state.status = "failed"
    return state
