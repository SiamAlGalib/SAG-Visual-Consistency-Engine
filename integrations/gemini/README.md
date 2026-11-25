# Google Gemini image generation

The local web app creates a fresh request for each scene and attaches selected approved character and environment images as inline image parts. The app, rather than Gemini chat memory, is the persistent source of truth.

- Default model: `gemini-3.1-flash-image`
- Alternate: `gemini-2.5-flash-image`
- App limit: 3 references per request.
- Uses the Gemini Developer API `generateContent` endpoint and requests text + image output.
- API key is provided per request and is not written to disk by the local server.

See [Gemini image generation docs](https://ai.google.dev/gemini-api/docs/image-generation) and [pricing](https://ai.google.dev/gemini-api/docs/pricing). API billing is separate from a Gemini consumer subscription.
