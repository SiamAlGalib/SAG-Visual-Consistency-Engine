# Instructions for AI assistants working in this repository

You are helping maintain SAG Visual Consistency Engine (SAG VCE).

## Non-negotiable goals
- Preserve approved character identity, wardrobe, palette, art direction, and environment continuity.
- Treat the visual bible and approved reference images as the source of truth.
- Never invent missing character details. Flag missing information and ask for an approved reference or explicit decision.
- Do not silently modify approved reference files or visual-bible entries.
- Keep provider-specific behavior isolated from the provider-neutral core.
- The local browser library is the user's source of truth for saved assets; never upload its contents to GitHub.

## Image prompt workflow
1. Retrieve the selected saved character and environment records.
2. Include immutable traits and actual approved reference image bytes in every provider request.
3. Treat references as identity anchors, not loose inspiration.
4. Preserve requested shot, action, and composition without redesigning established visual identity.
5. Require explicit instructions for intentional changes to clothing, age, hairstyle, season, or location.

## Color discipline
- Use stored HEX values and named usage from the visual bible.
- Do not casually reinterpret palette descriptions.
- HEX values guide the model but do not guarantee exact rendered pixels.
- For exact color matching, recommend image editing or deterministic post-processing.

## Engineering
- Keep Python dependencies minimal.
- Add tests for core validation and prompt generation.
- Never commit API keys, credentials, or private reference images.
- Keep the local server bound to 127.0.0.1; do not expose it to the public internet.
- Update documentation when behavior changes.
