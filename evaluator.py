"""
Research quality evaluator.

Uses an LLM to score research across multiple dimensions:
- Completeness: Are all key aspects of the topic covered?
- Depth: Does the research go beyond surface-level information?
- Novelty: Does each iteration add genuinely new information?
- Sources: Are claims backed by specific sources/URLs?

Returns a composite score 0-100.
"""

from __future__ import annotations

import json
import logging

import httpx

logger = logging.getLogger(__name__)

EVALUATION_PROMPT = """You are a research quality evaluator. Score the following research document on a scale of 0-100 across these dimensions:

1. **Completeness** (0-25): Are all key aspects of the topic covered? Are there obvious gaps?
2. **Depth** (0-25): Does it go beyond surface-level? Are there specific details, data points, examples?
3. **Novelty** (0-25): Is the information substantive and non-obvious? Would an expert find this useful?
4. **Sources** (0-25): Are claims supported by specific sources, URLs, or references?

TOPIC: {topic}

RESEARCH DOCUMENT:
{research}

Respond with ONLY a JSON object (no markdown, no explanation):
{{
  "completeness": <0-25>,
  "depth": <0-25>,
  "novelty": <0-25>,
  "sources": <0-25>,
  "total": <0-100>,
  "gaps": ["gap1", "gap2", ...],
  "strengths": ["strength1", "strength2", ...]
}}
"""


def score(
    research_text: str,
    topic: str,
    *,
    api_key: str | None = None,
    model: str = "anthropic/claude-sonnet-4-6",
    base_url: str = "https://openrouter.ai/api/v1",
) -> dict:
    """
    Score research quality using an LLM.

    Returns dict with keys: completeness, depth, novelty, sources, total, gaps, strengths
    """
    import os
    api_key = api_key or os.environ.get("OPENROUTER_API_KEY", "")

    if not research_text.strip():
        return {
            "completeness": 0, "depth": 0, "novelty": 0, "sources": 0,
            "total": 0, "gaps": ["No research content yet"], "strengths": [],
        }

    prompt = EVALUATION_PROMPT.format(topic=topic, research=research_text[:12000])

    try:
        with httpx.Client(timeout=60.0) as client:
            resp = client.post(
                f"{base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1,
                    "max_tokens": 500,
                },
            )
            resp.raise_for_status()
            data = resp.json()

        content = data["choices"][0]["message"]["content"].strip()
        # Strip markdown code fences if present
        if content.startswith("```"):
            content = content.split("\n", 1)[1]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

        result = json.loads(content)
        # Ensure total is calculated correctly
        result["total"] = (
            result.get("completeness", 0)
            + result.get("depth", 0)
            + result.get("novelty", 0)
            + result.get("sources", 0)
        )
        return result

    except Exception as e:
        logger.error("Evaluation failed: %s", e)
        # Return a minimal score so the loop continues
        return {
            "completeness": 5, "depth": 5, "novelty": 5, "sources": 5,
            "total": 20,
            "gaps": [f"Evaluation error: {e}"],
            "strengths": [],
        }
