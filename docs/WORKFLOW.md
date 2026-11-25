# ChatGPT + Gemini workflow

The repository is the shared source of truth; the model chat is the generation workspace.

## For every new story

1. Create a project-specific copy of `visual-bible.example.json`.
2. Add characters with stable IDs, immutable identity descriptions, wardrobe rules, and approved reference image paths.
3. Add environments with stable IDs, layout descriptions, and approved reference image paths.
4. Add a scene manifest for each scene.
5. Run the prompt builder and copy the output into ChatGPT or Gemini.
6. Attach the actual approved reference images in the image-generation interface. A path written in a prompt is not itself an uploaded image.
7. Inspect the generated result against the reference sheet and palette.
8. Mark accepted images as approved; do not silently replace the master references.

## Character record guidance

Use fields such as:

- `id`: stable machine-readable identifier, e.g. `leo`.
- `name`: display name.
- `identity_lock`: face shape, age appearance, skin tone, eye shape, hair, build, and other stable visible traits.
- `wardrobe_lock`: default clothing; specify scene exceptions explicitly.
- `reference_images`: paths to approved turnaround, expression, and color reference images.
- `do_not_change`: explicit invariants.

Avoid vague rules such as "same character". Describe visible traits and always attach reference images when the platform supports them.

## Color consistency

Sample colors from approved art rather than guessing. Store HEX values with named usage (hair, jacket, shirt, outline, background). HEX values guide the model but do not guarantee exact pixel colors; use image editing or post-processing if exact color matching is mandatory.

## Platform notes

ChatGPT and Gemini interfaces and APIs have different image-reference capabilities. Use the same visual bible, but follow each platform's current instructions for attaching reference images and selecting image models. Never put API keys in scene manifests or prompts.
