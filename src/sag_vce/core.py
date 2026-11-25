"""Core validation and provider-neutral scene prompt construction."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class BibleError(ValueError):
    """Raised when a visual bible or scene manifest is invalid."""


def load_json(path: str | Path) -> dict[str, Any]:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise BibleError(f"File not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise BibleError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise BibleError(f"Expected a JSON object in {path}")
    return data


def validate_bible(bible: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    for key in ("project", "art_direction", "palette"):
        if not isinstance(bible.get(key), dict):
            issues.append(f"Missing or invalid '{key}' object")
    palette = bible.get("palette", {}).get("colors", [])
    if not isinstance(palette, list) or not palette:
        issues.append("Palette must contain at least one color")
    else:
        for index, color in enumerate(palette):
            if not isinstance(color, dict) or not color.get("name") or not color.get("hex"):
                issues.append(f"Palette color at index {index} needs name and hex")
            elif not isinstance(color["hex"], str) or not color["hex"].startswith("#"):
                issues.append(f"Palette color at index {index} must use a hex color")
    for collection in ("characters", "environments", "continuity_rules"):
        if collection not in bible:
            issues.append(f"Missing '{collection}' collection")
    return issues


def build_scene_prompt(bible: dict[str, Any], scene: dict[str, Any]) -> str:
    issues = validate_bible(bible)
    if issues:
        raise BibleError("Visual bible is incomplete: " + "; ".join(issues))

    art = bible["art_direction"]
    project = bible["project"]
    palette = bible["palette"].get("colors", [])
    chars = {c.get("id"): c for c in bible.get("characters", []) if isinstance(c, dict)}
    envs = {e.get("id"): e for e in bible.get("environments", []) if isinstance(e, dict)}

    lines = [
        f"PROJECT: {project.get('name', 'Untitled Story')}",
        f"FORMAT: {project.get('aspect_ratio', '16:9')} widescreen",
        "ART DIRECTION:",
        f"- Style: {art.get('style_name', '')}",
        f"- Linework: {art.get('linework', '')}",
        f"- Shading: {art.get('shading', '')}",
        f"- Texture: {art.get('texture', '')}",
        "APPROVED PALETTE (preserve these color identities):",
    ]
    lines.extend(f"- {c.get('name')}: {c.get('hex')} — {c.get('usage', '')}" for c in palette)

    lines.append("CHARACTER REFERENCES:")
    selected = scene.get("characters", [])
    if not selected:
        lines.append("- No named characters specified. Do not invent recurring character designs.")
    for character_id in selected:
        character = chars.get(character_id)
        if not character:
            lines.append(f"- WARNING: Unknown character ID '{character_id}'. Add it to the visual bible.")
            continue
        lines.append(f"- {character.get('name', character_id)} ({character_id}): {character.get('identity_lock', '')}")
        if character.get("wardrobe_lock"):
            lines.append(f"  Wardrobe: {character['wardrobe_lock']}")
        if character.get("reference_images"):
            lines.append("  Attach these approved references: " + ", ".join(character["reference_images"]))

    environment_id = scene.get("environment_id")
    if environment_id:
        env = envs.get(environment_id)
        lines.append("ENVIRONMENT:")
        if env:
            lines.append(f"- {env.get('name', environment_id)}: {env.get('description', '')}")
            if env.get("reference_images"):
                lines.append("- Attach environment references: " + ", ".join(env["reference_images"]))
        else:
            lines.append(f"- WARNING: Unknown environment ID '{environment_id}'.")

    shot = scene.get("shot", {})
    lines.extend([
        "SCENE:",
        f"- Scene ID: {scene.get('scene_id', 'unspecified')}",
        f"- Story beat: {scene.get('story_beat', '')}",
        f"- Framing: {shot.get('framing', '')}",
        f"- Camera angle: {shot.get('camera_angle', '')}",
        f"- Composition: {shot.get('composition', '')}",
        f"- Time and lighting: {scene.get('time_and_lighting', '')}",
        f"- Continuity from previous scene: {scene.get('continuity_from_previous', '')}",
        "MUST NOT CHANGE:",
    ])
    lines.extend(f"- {rule}" for rule in scene.get("must_not_change", []))
    lines.extend(f"- {rule}" for rule in bible.get("continuity_rules", []))
    lines.append("GLOBAL NEGATIVE RULES:")
    lines.extend(f"- {rule}" for rule in art.get("global_negative_rules", []))
    if scene.get("additional_prompt"):
        lines.extend(["ADDITIONAL SCENE DETAILS:", scene["additional_prompt"]])
    lines.append("Use the attached approved reference images as visual anchors. Do not treat written descriptions as permission to redesign them.")
    return "\n".join(lines)
