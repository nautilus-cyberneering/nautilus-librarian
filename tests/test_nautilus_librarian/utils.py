import json


def compact_json(json_string: str) -> str:
    return json.dumps(json_string, separators=(",", ":"))
