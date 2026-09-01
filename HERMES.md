# Hermes project instructions

For character creation or revision, load `skills/character-manager/SKILL.md` and use `tools/character_manager.py`. The repository schema and validator are authoritative.

Always inspect existing characters first. Keep Stable DNA separate from Scene Delta. Write validated artifacts into this repository. Do not silently overwrite identity, approve references, infer biography from appearance, or turn a scene request into a DNA change.

When the user describes a new piece of content to make and wants alternatives before rendering, load `skills/idea-to-production/SKILL.md`. Use its versioned Idea → Storyboard → Sample → Final contracts, stop for the two director decisions it defines, and keep reference asset IDs opaque. Do not use it for Character DNA edits or simple re-submission of an already approved prompt.

For renderer work, follow the repository `SKILL.md` and keep the Character DNA version/hash in generation metadata.

When the user asks for a night batch or begins with `야간 배치:`, load the Character Manager skill and use `tools/hermes_night_batch.py`. Preserve the request in the plan, enforce its review-image budget, and let the durable queue run local image jobs sequentially. Do not improvise shell chains with `&&`, and do not start parallel WanGP jobs.
