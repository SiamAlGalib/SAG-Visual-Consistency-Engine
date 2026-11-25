# OpenAI image generation

The local web app uses the OpenAI Images API `/v1/images/edits` endpoint and supplies selected approved character and environment images as image inputs alongside the compiled scene prompt.

- Default model: `gpt-image-2.6-flare`
- Other models are selectable in API settings.
- API key is supplied per request and is not written to disk by the local server.
- This is OpenAI API image generation, not the ChatGPT website UI or a ChatGPT subscription. API billing is separate.

See the [image generation guide](https://developers.openai.com/api/docs/guides/image-generation) and [image edit API reference](https://developers.openai.com/api/reference/resources/images/methods/edit).
