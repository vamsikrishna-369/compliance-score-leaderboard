from __future__ import annotations

import json
import re
from typing import Any


_FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE)

def _extract_first_json(cleaned: str) -> str:
    if not cleaned:
        raise ValueError("Empty text")

    # Find first JSON container start.
    start_candidates = [i for i in (cleaned.find("{"), cleaned.find("[")) if i != -1]
    if not start_candidates:
        raise ValueError("No JSON object/array start found")

    start = min(start_candidates)
    opening = cleaned[start]
    closing = "}" if opening == "{" else "]"

    in_string = False
    escape = False
    depth = 0

    for idx in range(start, len(cleaned)):
        ch = cleaned[idx]

        if in_string:
            if escape:
                escape = False
                continue
            if ch == "\\":
                escape = True
                continue
            if ch == "\"":
                in_string = False
            continue

        if ch == "\"":
            in_string = True
            continue

        if ch == opening:
            depth += 1
            continue
        if ch == closing:
            depth -= 1
            if depth == 0:
                return cleaned[start : idx + 1]

        # Handle nested opposite containers too
        if ch in "{[":
            depth += 1
        elif ch in "}]":
            depth -= 1

    raise ValueError("Could not find end of JSON container")

def parse_json_only(text: str) -> Any:
    """
    Extract and parse JSON from an LLM response.

    - Removes optional ```json fences
    - Trims whitespace
    - Parses JSON (object/array/primitive)
    """
    cleaned = (text or "").strip()
    cleaned = _FENCE_RE.sub("", cleaned).strip()

    if cleaned.startswith("{") or cleaned.startswith("["):
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

    return json.loads(_extract_first_json(cleaned))

