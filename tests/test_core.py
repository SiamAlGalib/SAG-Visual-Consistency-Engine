import json

from sag_vce.core import build_scene_prompt, validate_bible


def sample_bible():
    return {
        "project": {"name": "Test story", "aspect_ratio": "16:9"},
        "art_direction": {
            "style_name": "Hand-drawn 2D",
            "linework": "Dark clean outlines",
            "shading": "Two-tone cel shading",
            "texture": "Subtle",
            "global_negative_rules": ["Do not redesign characters"],
        },
        "palette": {"colors": [{"name": "outline", "hex": "#1A1512", "usage": "Outlines"}]},
        "characters": [{
            "id": "leo",
            "name": "Leo",
            "identity_lock": "Oval face, brown hair, blue eyes",
            "wardrobe_lock": "Navy jacket",
            "reference_images": ["references/leo-turnaround.png"],
        }],
        "environments": [{
            "id": "garden",
            "name": "Back garden",
            "description": "Old tree beside a wooden fence",
            "reference_images": ["references/garden.png"],
        }],
        "continuity_rules": ["Keep character proportions stable"],
    }


def test_valid_bible_has_no_issues():
    assert validate_bible(sample_bible()) == []


def test_invalid_palette_is_reported():
    bible = sample_bible()
    bible["palette"]["colors"] = []
    assert any("Palette" in issue for issue in validate_bible(bible))


def test_prompt_includes_character_palette_and_environment():
    scene = {
        "scene_id": "scene-001",
        "story_beat": "Leo walks into the garden",
        "characters": ["leo"],
        "environment_id": "garden",
        "shot": {"framing": "wide shot", "camera_angle": "eye level"},
    }
    prompt = build_scene_prompt(sample_bible(), scene)
    assert "Leo" in prompt
    assert "#1A1512" in prompt
    assert "references/leo-turnaround.png" in prompt
    assert "Back garden" in prompt
    assert "references/garden.png" in prompt


def test_unknown_character_is_flagged_in_prompt():
    scene = {"characters": ["unknown-character"]}
    prompt = build_scene_prompt(sample_bible(), scene)
    assert "WARNING: Unknown character ID" in prompt
