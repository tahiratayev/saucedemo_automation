#!/usr/bin/env python3
"""
AI Test Generator — CLI
Kullanım:
    python generate_tests.py --url https://www.saucedemo.com --name Login
    python generate_tests.py --url https://www.saucedemo.com/inventory.html --name Inventory
    python generate_tests.py --url https://www.saucedemo.com/cart.html --name Cart
"""
import argparse
import os
import sys
from dotenv import load_dotenv

load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="Generate BDD tests from a page URL using Claude AI")
    parser.add_argument("--url",  required=True, help="Page URL to inspect")
    parser.add_argument("--name", required=True, help="Page name (e.g. Login, Inventory, Cart)")
    parser.add_argument("--preview", action="store_true", help="Preview generated files without saving")
    args = parser.parse_args()

    # Check API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not set in .env")
        sys.exit(1)

    from ai_generator.page_inspector import PageInspector
    from ai_generator.test_generator import TestGenerator
    from ai_generator.file_writer import FileWriter

    # Step 1: Inspect page
    print(f"\n🔍 Inspecting page: {args.url}")
    inspector = PageInspector()
    snapshot = inspector.inspect(args.url)
    print(f"   ✅ Found {len(snapshot.elements)} interactive elements")
    print(f"   Title: {snapshot.title}")

    # Step 2: Generate tests
    print(f"\n🤖 Generating tests with Claude...")
    generator = TestGenerator(api_key=api_key)
    result = generator.generate(snapshot, args.name)

    if not result.get("feature_file") or not result.get("steps_file"):
        print("❌ Claude returned incomplete response")
        sys.exit(1)

    feature_content = result["feature_file"]
    steps_content = result["steps_file"]

    # Step 3: Preview or save
    writer = FileWriter()

    if args.preview:
        writer.preview(feature_content, steps_content)
        print("\n✅ Preview only — no files written (remove --preview to save)")
    else:
        writer.preview(feature_content, steps_content)
        paths = writer.write(args.name, feature_content, steps_content)
        print(f"\n✅ Files saved:")
        print(f"   Feature: {paths['feature']}")
        print(f"   Steps:   {paths['steps']}")
        print(f"\n💡 Review the files in ai_generated/ before moving to features/ and steps/")


if __name__ == "__main__":
    main()
