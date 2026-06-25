"""
AI Test Failure Analyzer
Sends failed test context to Claude API and returns root cause + fix suggestion.
"""
import os
import json
import httpx
from dataclasses import dataclass
from typing import Optional


@dataclass
class FailureContext:
    test_name: str
    test_file: str
    error_message: str
    traceback: str
    feature: Optional[str] = None
    scenario: Optional[str] = None


@dataclass
class AnalysisResult:
    test_name: str
    root_cause: str
    fix_suggestion: str
    confidence: str  # high / medium / low
    raw_response: str


SYSTEM_PROMPT = """You are a senior QA automation engineer specializing in Playwright, pytest-bdd, and Python test automation.

When given a test failure, you analyze it and respond ONLY with a JSON object in this exact format:
{
  "root_cause": "concise explanation of why the test failed",
  "fix_suggestion": "specific code or config change to fix it",
  "confidence": "high|medium|low"
}

Rules:
- root_cause: 1-2 sentences max, technical and specific
- fix_suggestion: actionable, include code snippet if relevant
- confidence: high if error is clear, medium if uncertain, low if needs more context
- No markdown, no preamble, pure JSON only
"""


class TestFailureAnalyzer:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = "claude-sonnet-4-6"
        self.api_url = "https://api.anthropic.com/v1/messages"

    def analyze(self, context: FailureContext) -> AnalysisResult:
        """Send failure context to Claude and get analysis back."""
        prompt = self._build_prompt(context)

        response = httpx.post(
            self.api_url,
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": self.model,
                "max_tokens": 1024,
                "system": SYSTEM_PROMPT,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=30,
        )
        response.raise_for_status()

        raw = response.json()["content"][0]["text"].strip()

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            # Fallback if model adds extra text
            import re
            match = re.search(r'\{.*\}', raw, re.DOTALL)
            parsed = json.loads(match.group()) if match else {
                "root_cause": "Could not parse AI response",
                "fix_suggestion": raw,
                "confidence": "low"
            }

        return AnalysisResult(
            test_name=context.test_name,
            root_cause=parsed.get("root_cause", ""),
            fix_suggestion=parsed.get("fix_suggestion", ""),
            confidence=parsed.get("confidence", "low"),
            raw_response=raw,
        )

    def _build_prompt(self, ctx: FailureContext) -> str:
        parts = [
            f"Test file: {ctx.test_file}",
            f"Test name: {ctx.test_name}",
        ]
        if ctx.feature:
            parts.append(f"Feature: {ctx.feature}")
        if ctx.scenario:
            parts.append(f"Scenario: {ctx.scenario}")
        parts += [
            f"\nError message:\n{ctx.error_message}",
            f"\nTraceback:\n{ctx.traceback}",
        ]
        return "\n".join(parts)
