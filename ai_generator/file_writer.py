"""
File Writer
Üretilen feature ve step dosyalarını projeye yazar.
"""
from pathlib import Path


class FileWriter:
    def __init__(self, project_root: str = "."):
        self.root = Path(project_root)
        self.features_dir = self.root / "features"
        self.steps_dir = self.root / "steps"
        self.generated_dir = self.root / "ai_generated"

        # Generated files go to ai_generated/ — don't pollute main dirs
        self.generated_dir.mkdir(exist_ok=True)
        (self.generated_dir / "features").mkdir(exist_ok=True)
        (self.generated_dir / "steps").mkdir(exist_ok=True)

    def write(self, page_name: str, feature_content: str, steps_content: str) -> dict:
        """Write generated files and return their paths."""
        name = page_name.lower()

        feature_path = self.generated_dir / "features" / f"{name}.feature"
        steps_path = self.generated_dir / "steps" / f"test_{name}_steps.py"

        feature_path.write_text(feature_content)
        steps_path.write_text(steps_content)

        return {
            "feature": str(feature_path),
            "steps": str(steps_path),
        }

    def preview(self, feature_content: str, steps_content: str):
        """Print generated content to terminal for review."""
        print("\n" + "═" * 60)
        print("📄 GENERATED FEATURE FILE")
        print("═" * 60)
        print(feature_content)

        print("\n" + "═" * 60)
        print("🐍 GENERATED STEPS FILE")
        print("═" * 60)
        print(steps_content)
        print("═" * 60)
