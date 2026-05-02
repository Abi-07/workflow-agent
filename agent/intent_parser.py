from utils.llm import call_llm
from utils.parser import safe_parse_json

SYSTEM_PROMPT = """
You are an intent parser for a task automation agent.

Return ONLY valid JSON.
"""

def load_prompt(file_path: str) -> str:
    with open(file_path, 'r') as f:
        return f.read()

USER_PROMPT = load_prompt("prompts/intent_prompt.txt")


def parse_intent(user_input: str) -> dict:
    prompt = USER_PROMPT.replace("{input}", user_input)

    raw = call_llm(prompt, SYSTEM_PROMPT)

    parsed = safe_parse_json(raw)
    if isinstance(parsed, dict):
        parsed["raw_input"] = user_input

    return parsed