"""
AI Test Generator
PageSnapshot'ı Claude'a gönderir, BDD feature + step definitions üretir.
"""
import os
import json
import re
import httpx
from ai_generator.page_inspector import PageSnapshot


SYSTEM_PROMPT = """You are a senior QA automation engineer expert in Playwright, pytest-bdd, and Python.

Given a page snapshot (URL, title, interactive elements with selectors), generate:
1. A BDD feature file
2. pytest-bdd step definitions using Playwright

Respond ONLY with a JSON object in this exact format:
{
  "feature_file": "full content of the .feature file",
  "steps_file": "full content of the pytest step definitions Python file"
}

Rules for feature file:
- Use realistic, business-meaningful scenarios
- Include @smoke tag on the happy path scenario
- Include at least one negative/edge case scenario
- Use Background for login if needed
- Scenario names should describe user intent, not technical actions

Rules for steps file:
- Import from pages module (assume POM classes exist)
- Use allure.step() wrappers
- Use parsers.parse() for parameterized steps
- Follow existing project patterns with page and base_url fixtures
- Selectors must match exactly what was provided in the snapshot
- No hardcoded waits — use Playwright's auto-waiting

No markdown, no preamble, pure JSON only.
"""


class TestGenerator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = "claude-sonnet-4-6"
        self.api_url = "https://api.anthropic.com/v1/messages"

    def generate(self, snapshot: PageSnapshot, page_name: str) -> dict:
        """Send page snapshot to Claude, get feature + steps back."""
        prompt = self._build_prompt(snapshot, page_name)

        response = httpx.post(
            self.api_url,
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": self.model,
                "max_tokens": 4096,
                "system": SYSTEM_PROMPT,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=60,
        )
        response.raise_for_status()

        raw = response.json()["content"][0]["text"].strip()

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            match = re.search(r'\{.*\}', raw, re.DOTALL)
            parsed = json.loads(match.group()) if match else {}

        return parsed

    def _build_prompt(self, snapshot: PageSnapshot, page_name: str) -> str:
        return f"""Generate tests for the '{page_name}' page.

{snapshot.to_prompt_text()}

Page name to use for POM class: {page_name}Page
Feature file name: {page_name.lower()}.feature
Steps file name: test_{page_name.lower()}_steps.py
"""
