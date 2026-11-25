"""Command line interface for SAG VCE."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import BibleError, build_scene_prompt, load_json, validate_bible


def main() -> None:
    parser = argparse.ArgumentParser(prog="sag-vce", description="SAG Visual Consistency Engine")
    sub = parser.add_subparsers(dest="command", required=True)
    init_cmd = sub.add_parser("init", help="Copy the example visual bible")
    init_cmd.add_argument("--output", default="visual-bible.json")
    validate_cmd = sub.add_parser("validate", help="Validate a visual bible")
    validate_cmd.add_argument("bible")
    prompt_cmd = sub.add_parser("prompt", help="Build a scene prompt")
    prompt_cmd.add_argument("scene")
    prompt_cmd.add_argument("--bible", default="visual-bible.json")
    args = parser.parse_args()

    try:
        if args.command == "init":
            source = Path("visual-bible.example.json")
            if not source.exists():
                raise BibleError("Run this command from the repository root.")
            target = Path(args.output)
            if target.exists():
                raise BibleError(f"Refusing to overwrite existing file: {target}")
            target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"Created {target}")
        elif args.command == "validate":
            issues = validate_bible(load_json(args.bible))
            if issues:
                print("Visual bible needs attention:")
                for issue in issues:
                    print(f"- {issue}")
                raise SystemExit(1)
            print("Visual bible looks structurally valid.")
        elif args.command == "prompt":
            bible = load_json(args.bible)
            scene = load_json(args.scene)
            print(build_scene_prompt(bible, scene))
    except BibleError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
