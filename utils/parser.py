import json

def safe_parse_json(text: str):
    try:
        return json.loads(text)
    except Exception:
        # fallback: try to extract JSON block
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end != -1:
            try:
                return json.loads(text[start:end])
            except Exception:
                pass
    return {"error": "invalid_json", "raw": text}