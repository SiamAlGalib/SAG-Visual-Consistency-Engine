# Instructions for AI assistants working in this repository

You are helping maintain SAG Visual Consistency Engine (SAG VCE).

## Non-negotiable goals
- Preserve approved character identity, wardrobe, palette, art direction, and environment continuity.
- Treat the visual bible and approved reference images as the source of truth.
- Never invent missing character details. Flag missing information and ask for an approved reference or explicit decision.
- Do not silently modify approved reference files or visual-bible entries.
- Keep provider-specific behavior isolated from the provider-neutral core.

## Image prompt workflow
1. Read the project's visual bible.
2. Read the scene manifest.
3. Identify every referenced character and environment.
4. Include their immutable traits and approved reference image paths in the prompt.
5. Tell the user to attach the actual reference images in the target image-generation interface. A local path in text is not an uploaded image.
6. Preserve the requested shot, action, and composition without redesigning the established visual identity.
7. If a scene intentionally changes clothing, age, hairstyle, season, or location, require that change to be explicit in the scene manifest.

## Color discipline
- Use stored HEX values and named usage from the visual bible.
- Do not casually reinterpret palette descriptions.
- Explain that prompt-level HEX instructions are guidance, not a guarantee of exact rendered pixels.
- For exact color matching, recommend image editing or deterministic post-processing.

## Engineering
- Keep Python dependencies minimal.
- Add tests for core validation and prompt generation.
- Never commit API keys, credentials, or private reference images.
- Update documentation when behavior changes.
