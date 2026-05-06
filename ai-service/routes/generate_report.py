from flask import Blueprint, request, jsonify
from services.groq_client import GroqClient

generate_report_bp = Blueprint("generate_report", __name__)

client = GroqClient()


@generate_report_bp.route("/generate-report", methods=["POST"])
def generate_report():
    data = request.get_json()

    if not data or "input" not in data:
        return jsonify({"error": "input is required"}), 400

    user_input = data["input"]

    system_prompt = """
You are a compliance report generator.

Generate:
- title
- summary
- overview
- recommendations

Return valid JSON only.
"""

    result = client.generate(
        system=system_prompt,
        user=user_input,
        temperature=0.3,
        max_tokens=500,
    )

    return jsonify({
        "report": result.text,
        "is_fallback": result.is_fallback
    })