from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass
from typing import Any

import requests

# ✅ ADD THESE 2 LINES
from dotenv import load_dotenv
load_dotenv()


@dataclass(frozen=True)
class GroqResult:
    text: str
    is_fallback: bool


class GroqClient:
    def __init__(self) -> None:
        self._api_key = os.getenv("GROQ_API_KEY", "")
        self._model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self._base_url = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
        self._timeout_s = float(os.getenv("GROQ_TIMEOUT_S", "10"))

        # ✅ OPTIONAL DEBUG (remove later)
        print("Loaded API KEY:", self._api_key[:6] + "..." if self._api_key else "None")

    def generate(self, *, system: str, user: str, temperature: float = 0.3, max_tokens: int = 700) -> GroqResult:
        if not self._api_key:
            return GroqResult(text=self._fallback_text(system=system, user=user), is_fallback=True)

        payload: dict[str, Any] = {
            "model": self._model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json"
        }

        last_err: Exception | None = None
        for attempt in range(1, 4):
            try:
                resp = requests.post(
                    f"{self._base_url}/chat/completions",
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=self._timeout_s,
                )
                resp.raise_for_status()
                data = resp.json()

                content = (
                    (data.get("choices") or [{}])[0]
                    .get("message", {})
                    .get("content", "")
                )

                content = (content or "").strip()
                if not content:
                    raise RuntimeError("Empty Groq response content")

                return GroqResult(text=content, is_fallback=False)

            except Exception as e:
                last_err = e
                time.sleep(0.4 * attempt)

        return GroqResult(
            text=self._fallback_text(system=system, user=user, err=last_err),
            is_fallback=True
        )

    def _fallback_text(self, *, system: str, user: str, err: Exception | None = None) -> str:
        seed = hashlib.sha256((system + "\n" + user).encode("utf-8")).hexdigest()[:10]
        if err:
            return f"[fallback:{seed}] AI unavailable. Please retry. ({type(err).__name__})"
        return f"[fallback:{seed}] AI not configured. Set GROQ_API_KEY in your .env."