from __future__ import annotations
import os
import json
from typing import Dict, Any, Optional

try:
    from anthropic import Anthropic
except Exception:
    Anthropic = None # allow import without anthropic installed

class ClaudeClient:
    """
    Client for fetching data from Claude(Anthropic).
    Reads API key from ANTHROPIC_API_KEY environment variable.
    Defaults to Claude 3.7 Sonnet model.
    """
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        # 1) assign key FIRST
        key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.api_key = key

        # 2) assign model
        self.model = model or os.getenv("CLAUDE_MODEL", "claude-3-7-sonnet-20250219")

        # 3) create client LAST (after self.api_key exists)
        if Anthropic and self.api_key:
            self.client = Anthropic(api_key=self.api_key)
        else:
            self.client = None
    
    def _ensure(self) -> None:
        if not self.client:
            raise RuntimeError("Anthropic client not initialized. Please provide an API key in your .env file")

    def _query_claude(self, prompt: str, system:Optional [str] = None, max_tokens: int = 1000) -> str:
        """Returns response from Claude model"""
        self._ensure()
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=0,
            system=system or (
                "You are an expert real estate analyst. You provide factual, structured information about the US real estate market."
            ),
            messages=[{"role": "user", "content": prompt}],
        )
        #Extract first text block
        try:
            for block in response.content:
                if getattr(block, "type", "") == "text":
                    return block.text
        except Exception:
            pass
        return ""
    def _query_json(self, prompt: str, max_tokens: int = 1200) -> Dict[str, Any]:
        """Ask Claude to return strict JSON; parse defensively."""
        raw = self._query_claude (
            "Return STRICT JSON only. No prose outside JSON. /n/n" + prompt,
            system="Return strict JSON only.",
            max_tokens=max_tokens, 
        )
        try:
            return json.loads(raw)
        except Exception:
            #best-effort salvage if the moel wrapped JSON
            start, end = raw.find("{"), raw.rfind("}")
            if start != -1 and end!= -1 and end > start:
                try:
                    return json.loads(raw[start:end +1])
                except Exception:
                 pass
        return {}
        

        
