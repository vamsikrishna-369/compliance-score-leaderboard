from __future__ import annotations

from pathlib import Path


def load_prompt(prompt_name: str) -> str:
    prompts_dir = Path(__file__).resolve().parents[1] / "prompts"
    prompt_path = (prompts_dir / prompt_name).resolve()

    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt not found: {prompt_path}")

    return prompt_path.read_text(encoding="utf-8")

