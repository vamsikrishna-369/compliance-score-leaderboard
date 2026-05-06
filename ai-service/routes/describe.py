from __future__ import annotations

import time

from flask import Blueprint, jsonify, request

from services.groq_client import GroqClient
from services.json_only import parse_json_only
from services.prompt_loader import load_prompt


describe_bp = Blueprint("describe", __name__)


@describe_bp.post("/describe")
def describe():
    start = time.time()
    data = request.get_json(silent=True) or {}
    input_text = (data.get("input") or "").strip()

    if not input_text:
        return jsonify({"error": "input is required"}), 400
    if len(input_text) > 5000:
        return jsonify({"error": "input is too long (max 5000 chars)"}), 400

    prompt = load_prompt("describe_prompt.txt")
    system = "You are a compliance assistant. Return only valid JSON."
    user = prompt.replace("{{INPUT}}", input_text)

    groq = GroqClient()
    result = groq.generate(system=system, user=user, temperature=0.3, max_tokens=600)

    elapsed_ms = int((time.time() - start) * 1000)
    is_fallback = result.is_fallback
    try:
        parsed = parse_json_only(result.text)
    except Exception:  # noqa: BLE001
        parsed = {
            "title": "AI output unavailable",
            "summary": "The AI response could not be generated right now. Please retry.",
            "key_risks": ["Unknown", "Unknown", "Unknown"],
        }
        is_fallback = True

    return jsonify(
        {
            "generated_at": int(time.time()),
            "elapsed_ms": elapsed_ms,
            "is_fallback": is_fallback,
            "description": parsed,
        }
    )

