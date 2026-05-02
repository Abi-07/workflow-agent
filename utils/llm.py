import ollama
from app.config import MODEL


def call_llm(prompt: str, system: str = "") -> str:
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        options={
            "temperature": 0.2,  # lower = more deterministic
        },
    )
    return response["message"]["content"]