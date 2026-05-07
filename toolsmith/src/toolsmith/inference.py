"""Inference wrapper. Loads the base model + LoRA adapter and produces a tool call."""

from __future__ import annotations

import json
import re
from typing import Any

from toolsmith.data.tools import system_prompt

_JSON_RE = re.compile(r"\{[\s\S]*\}")


class ToolSmithModel:
    """Thin wrapper that handles loading + prompt assembly + JSON extraction."""

    def __init__(self, model: Any, tokenizer: Any) -> None:
        self.model = model
        self.tokenizer = tokenizer

    @classmethod
    def from_pretrained(cls, adapter_path_or_hub_id: str) -> "ToolSmithModel":
        """Load the LoRA adapter from a local path or the HuggingFace Hub."""
        from peft import PeftModel
        from transformers import AutoModelForCausalLM, AutoTokenizer

        from toolsmith.config import settings

        tokenizer = AutoTokenizer.from_pretrained(adapter_path_or_hub_id)
        base = AutoModelForCausalLM.from_pretrained(
            settings.base_model, torch_dtype="auto", device_map="auto"
        )
        model = PeftModel.from_pretrained(base, adapter_path_or_hub_id)
        model.eval()
        return cls(model=model, tokenizer=tokenizer)

    def call(self, user_prompt: str, max_new_tokens: int = 256) -> dict[str, Any]:
        """Return the parsed tool-call JSON.

        Robust to small model wandering: falls back to the first JSON-like
        substring found in the output.
        """
        messages = [
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": user_prompt},
        ]
        inputs = self.tokenizer.apply_chat_template(
            messages, return_tensors="pt", add_generation_prompt=True
        ).to(self.model.device)

        outputs = self.model.generate(
            inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        text = self.tokenizer.decode(outputs[0][inputs.shape[1] :], skip_special_tokens=True)

        match = _JSON_RE.search(text)
        if not match:
            return {"tool": None, "reason": "model produced no JSON", "_raw": text}
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError as exc:
            return {"tool": None, "reason": f"invalid JSON: {exc}", "_raw": text}
