# SAG Visual Consistency Engine

A provider-neutral toolkit for keeping characters, palettes, art direction, environments, and scene continuity organized across ChatGPT and Google Gemini image workflows.

## What this first version does

- Stores a reusable visual bible in JSON and Markdown.
- Builds scene prompts from approved character and style references.
- Checks scene manifests for missing or conflicting visual rules.
- Keeps provider integrations modular: this repository does not assume that connecting GitHub automatically grants image-generation access.
- Keeps API keys out of source control.

## Quick start

Requires Python 3.10+.

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -e .
```

Create a visual bible from the example:

```bash
sag-vce init --output visual-bible.json
```

Validate it:

```bash
sag-vce validate visual-bible.json
```

Build a prompt for a scene manifest:

```bash
sag-vce prompt examples/scene-001.json --bible visual-bible.json
```

## Suggested workflow

1. Create one approved character record per recurring character.
2. Add reference image paths and describe immutable identity traits.
3. Define the master art direction and exact palette.
4. Describe recurring locations in the environment library.
5. Write each scene as a small JSON manifest that references character and location IDs.
6. Generate images in ChatGPT or Gemini using the resulting prompt and attach the relevant reference images in that platform.
7. Review the output, approve it, and update the bible only deliberately.

## Important limitation

Text prompts and metadata alone cannot guarantee identical pixels or perfect character identity. Stronger consistency comes from supplying the same approved reference images to the image model, using its supported reference/image-editing controls, and reviewing results. Model capabilities and API availability differ by provider and may change.

## Provider strategy

- **ChatGPT:** use the prompt and reference bundle in ChatGPT image generation. A future API adapter can be added when the chosen OpenAI image endpoint and account access are confirmed.
- **Gemini:** use the same prompt and reference bundle with a Gemini image-capable model. A future adapter can be added using the currently supported Google API.
- The core visual bible and prompt builder remain provider-neutral.

## Privacy and safety

- Never commit API keys, private photos, unpublished reference art, or confidential scripts to a public repository.
- Store secrets in local environment variables or a secret manager.
- If this repository is public, keep only generic templates and code here; store private project assets elsewhere or change repository visibility before uploading them.

## Project status

Initial scaffold. Provider API calls, image similarity scoring, a web dashboard, and automated reference-image packaging are planned follow-up milestones.
