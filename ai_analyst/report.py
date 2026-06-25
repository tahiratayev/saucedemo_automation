"""
AI Analysis Report Generator
Saves analysis results to JSON + human-readable Markdown.
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List
from ai_analyst.analyzer import AnalysisResult


CONFIDENCE_EMOJI = {"high": "🟢", "medium": "🟡", "low": "🔴"}


class AnalysisReport:
    def __init__(self, output_dir: str = "reports/ai_analysis"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results: List[AnalysisResult] = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def add(self, result: AnalysisResult):
        self.results.append(result)

    def save(self):
        if not self.results:
            return
        self._save_json()
        self._save_markdown()

    def _save_json(self):
        path = self.output_dir / f"analysis_{self.timestamp}.json"
        data = [
            {
                "test_name": r.test_name,
                "root_cause": r.root_cause,
                "fix_suggestion": r.fix_suggestion,
                "confidence": r.confidence,
            }
            for r in self.results
        ]
        path.write_text(json.dumps(data, indent=2))
        print(f"\n📄 AI analysis saved: {path}")

    def _save_markdown(self):
        path = self.output_dir / f"analysis_{self.timestamp}.md"
        lines = [
            f"# AI Test Failure Analysis",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Failed tests analyzed: {len(self.results)}",
            "",
        ]
        for r in self.results:
            emoji = CONFIDENCE_EMOJI.get(r.confidence, "⚪")
            lines += [
                f"---",
                f"## {r.test_name}",
                f"**Confidence:** {emoji} {r.confidence.upper()}",
                f"",
                f"**Root cause:**",
                f"{r.root_cause}",
                f"",
                f"**Fix suggestion:**",
                f"```",
                f"{r.fix_suggestion}",
                f"```",
                f"",
            ]
        path.write_text("\n".join(lines))
        print(f"📋 Markdown report: {path}")
