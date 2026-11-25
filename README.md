# SAG Visual Consistency Engine

A local-first visual bible and image-generation workspace for keeping recurring characters, environments, palettes, and scene continuity organized across Gemini and OpenAI image generation.

## Local visual library + direct image generation

The browser app is in `app/`. It adds persistent character and background references using browser IndexedDB, multiple images per asset, automatic reference retrieval, scene prompt compilation, Gemini image generation, OpenAI reference-guided image generation, and local generation history.

### Run on Windows

Requires Python 3.10+; no extra packages are needed.

1. Download or clone this repository.
2. Double-click `run-local.bat`, or open a terminal in the project folder and run `python server.py`.
3. Open `http://127.0.0.1:8765/app/`.
4. In **API settings**, add your Gemini or OpenAI API key.
5. In **Visual library**, save character and background references.
6. In **Generate image**, select their names, describe the scene, and generate.

Keep the terminal running. Press Ctrl+C to stop.

### API keys and billing

This uses provider API keys, not a ChatGPT or Gemini consumer subscription. API usage is billed separately. Create keys at https://aistudio.google.com/app/apikey and https://platform.openai.com/api-keys.

Keys stay in browser session memory and are forwarded through a loopback-only Python server. The server does not persist keys or reference images. Do not expose it to the public internet or use it on a shared computer.

### Local storage

Characters, environments, reference images, and saved generations live in this browser's IndexedDB. They do not sync to other devices. Clearing browser site data can erase them. Keep original images backed up privately. Never commit private artwork or API keys to this public repository.

### Provider notes

- Gemini requests attach the selected approved references as inline image data. This app currently allows up to 3 reference images per Gemini request.
- OpenAI uses the Images edits API with the selected references. It is API image generation, not the ChatGPT website UI.
- Models, image limits, pricing, and account access can change. Check current provider docs.
- Reference images improve consistency but cannot guarantee identical pixels or perfect identity. Review outputs before approving.

## Existing Python CLI

The original provider-neutral visual bible and prompt CLI remain available:

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -e .
sag-vce init --output visual-bible.json
sag-vce validate visual-bible.json
sag-vce prompt examples/scene-001.json --bible visual-bible.json
```

## Privacy

Never commit API keys, private photos, unpublished reference art, or confidential scripts. Keep local assets in browser storage or a private backup. The public repository should contain generic templates and application code only.
