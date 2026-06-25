"""
pytest plugin — hooks into test failures and triggers AI analysis automatically.
Activated via conftest.py when ANTHROPIC_API_KEY is set.
"""
import pytest
import traceback as tb
from ai_analyst.analyzer import TestFailureAnalyzer, FailureContext
from ai_analyst.report import AnalysisReport


class AIAnalystPlugin:
    def __init__(self):
        self.analyzer = TestFailureAnalyzer()
        self.report = AnalysisReport()
        self.enabled = bool(self.analyzer.api_key)

        if self.enabled:
            print("\n🤖 AI Test Analyst: active")
        else:
            print("\n⚠️  AI Test Analyst: disabled (set ANTHROPIC_API_KEY to enable)")

    def pytest_runtest_logreport(self, report):
        """Hook called after each test phase (setup/call/teardown)."""
        if not self.enabled:
            return
        if report.when != "call" or not report.failed:
            return

        self._analyze_failure(report)

    def _analyze_failure(self, report):
        try:
            # Extract test info
            test_name = report.nodeid.split("::")[-1]
            test_file = report.nodeid.split("::")[0]
            error_text = str(report.longrepr) if report.longrepr else "No error details"

            # Split traceback from error message
            lines = error_text.split("\n")
            error_message = lines[-1] if lines else error_text
            traceback_text = "\n".join(lines[:-1]) if len(lines) > 1 else ""

            # Extract BDD feature/scenario if available
            feature = None
            scenario = None
            for line in lines:
                if "Feature:" in line:
                    feature = line.strip()
                if "Scenario:" in line:
                    scenario = line.strip()

            context = FailureContext(
                test_name=test_name,
                test_file=test_file,
                error_message=error_message,
                traceback=traceback_text[:3000],  # cap at 3k chars
                feature=feature,
                scenario=scenario,
            )

            print(f"\n🔍 Analyzing failure: {test_name}...")
            result = self.analyzer.analyze(context)
            self.report.add(result)

            # Print inline summary
            from ai_analyst.report import CONFIDENCE_EMOJI
            emoji = CONFIDENCE_EMOJI.get(result.confidence, "⚪")
            print(f"\n{'─'*60}")
            print(f"🤖 AI Analysis — {test_name}")
            print(f"   {emoji} Root cause: {result.root_cause}")
            print(f"   💡 Fix: {result.fix_suggestion}")
            print(f"{'─'*60}")

        except Exception as e:
            print(f"\n⚠️  AI analysis failed for {report.nodeid}: {e}")

    def pytest_sessionfinish(self, session, exitstatus):
        """Save full report at end of session."""
        if self.enabled and self.report.results:
            self.report.save()
