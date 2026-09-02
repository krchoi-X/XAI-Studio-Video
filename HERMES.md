# Hermes project instructions

For every natural-language character image request, including simple requests such as "Lia 이미지 5개를 Krea2로 만들어줘", load `skills/character-manager/SKILL.md`. Existing-character image production must use `tools/character_scene.py produce`; character creation or canonical DNA revision must use `tools/character_manager.py`. The repository schema and validator are authoritative.

The operator is not required to remember CLI syntax, internal folder names, prompt strategies, or whether `count` is per engine. Translate ordinary language into the repository command. If character, engine, count, and prompt are already clear, execute without asking the operator to restate the request. If a required value is genuinely missing, explain the missing value in ordinary language and give one short corrected example. Never invent an alternate batch script or folder convention.

For immediate existing-character image generation, run from this repository root:

```powershell
python tools/character_scene.py produce --character <character-id> --request "<verbatim prompt>" --engines <z-image|krea2|comma-list> --count <per-engine-count> --strategy strict_translation --actor hermes
```

Preserve the request verbatim. Read the selected character's canonical `character.json`; do not require the user to paste Character DNA. A pasted identity prompt is a per-generation prompt unless the user explicitly requests a canonical DNA update. If it introduces identity details that differ from canonical DNA, briefly identify those differences and treat them only as runtime Scene Spec guidance; never silently edit canonical DNA. Verify completion from `batch.yaml`, run records, and actual output files, then sync the web app. Do not create a guessed session directory or call `produce --session-dir` until `prepare` has created a valid session containing `batch.yaml` and `prompt.txt`.

Always inspect existing characters first. Keep Stable DNA separate from Scene Delta. Write validated artifacts into this repository. Do not silently overwrite identity, approve references, infer biography from appearance, or turn a scene request into a DNA change.

When the user describes a new piece of content to make and wants alternatives before rendering, load `skills/idea-to-production/SKILL.md`. Use its versioned Idea → Storyboard → Sample → Final contracts, stop for the two director decisions it defines, and keep reference asset IDs opaque. Do not use it for Character DNA edits or simple re-submission of an already approved prompt.

For video renderer work, follow the repository `SKILL.md`. For existing-character still images, use the Character Manager scene pipeline above. Keep the Character DNA version/hash in generation metadata.

When the user asks for a night batch or begins with `야간 배치:`, load the Character Manager skill and use `tools/hermes_night_batch.py`. Preserve the request in the plan, enforce its review-image budget, and let the durable queue run local image jobs sequentially. Do not improvise shell chains with `&&`, and do not start parallel WanGP jobs.
