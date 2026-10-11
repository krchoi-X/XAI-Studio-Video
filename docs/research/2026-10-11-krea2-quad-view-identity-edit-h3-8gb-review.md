# Krea 2 Quad View / Identity Edit + MiniMax H3 8GB — Review

Date: 2026-10-11
Status: Research candidate, not integrated or benchmarked.
Priority: Do not replace active P0 in docs/current-priorities.md.

## Context
The main production problem is maintaining an approved character's face across camera angles, outfits and scenes. Secondary issues are H3 iteration time on RTX 4070 8GB and loss of storyboard meaning during prompt conversion.

## Findings and recommendations
1. **Krea 2 Identity Edit**: test reference-based edits with one approved face master. Preserve original face geometry, compare profile and 3/4 views and clothing/background changes. The independent node is not proven to be included in the Quad View workflow.
2. **Krea 2 Quad View**: independently inspect RunningHub workflow JSON and compare view-to-view identity. Do not automatically promote generated views to canonical DNA.
3. **MiniMax H3 4/8-step Turbo**: compare creator workflow against already installed Turbo LoRA; verify weight hashes to avoid duplicate downloads. 8GB compatibility does not guarantee usable speed. Measure end-to-end elapsed time, VRAM/RAM, motion, face consistency and fidelity to storyboard.
4. **UniBlockSwap and SageAttention**: potential memory efficiency and speed improvements; verify CPU/GPU swapping overhead and Python/PyTorch/CUDA compatibility.
5. **Official H3 prompt skill**: review adapter conventions while preserving approved storyboard, explicit camera/subject motion, direction, duration and start/end state.
6. **All-in-one ComfyUI bundle/Node.js**: no default installation; retain functioning Krea2/H3 environment and isolate any trial.

## Test gates
- Inspect source workflow graphs, dependency and version requirements before installation.
- Compare baseline Krea2, Identity Edit and Quad View using the SAME approved face master. Generate 3x3 review sheet for geometry, age impression, skin, pose and identity.
- Compare existing H3 and creator's 4/8-step setup using matching 864x480 / 124f inputs when available; log total time, peak GPU/system memory, quality and motion intent.
- Promote changes only when repeatable advantages are demonstrated; record hashes, workflow JSON, versions, and outputs.
- Keep references derived from the canonical master, not recursively from each other (see docs/reference-driven-production-pipeline.md).

## Links
- Video: https://youtu.be/2jv1I9-JULo
- Creator's comment: https://youtube.com/watch?v=2jv1I9-JULo&lc=UgxMhZCwVHoZjDNPaAp4AaABAg
- Krea Quad View: https://www.runninghub.ai/post/2088925222431309826/
- H3 4/8-step: https://www.runninghub.ai/post/2088925178326958082/
- Identity Edit node: https://github.com/lbouaraba/comfyui-krea2edit
- H3 official: https://huggingface.co/MiniMaxAI/MiniMax-H3
- H3 official prompt skill: https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/h3-prompt-writing
- Used video prompts (not verified): https://docs.google.com/document/d/1NtLVaqkT6tNwbxEXPsPysiX1JSb1r0z3lZmmtlhPOZA/edit
- Comfy-Org weights: https://huggingface.co/Comfy-Org/MiniMax-H3/tree/main/diffusion_models
- LightX2V Turbo: https://huggingface.co/lightx2v/Minimax-h3-Turbo/tree/main
- Unified package: https://huggingface.co/noname1992/ComfyAllInOnePackage/tree/main
- Installation: https://youtu.be/vXgKgevpPIk
- KJNodes: https://github.com/kijai/ComfyUI-KJNodes
- VideoHelperSuite: https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite
- UniBlockSwap: https://github.com/smthemex/ComfyUI_UniBlockSwap
- SageAttention: https://github.com/woct0rdho/SageAttention
- Node.js: https://nodejs.org/en/download

## Decision
Recommended order: Identity Edit -> Quad View comparison -> H3 speed/quality A/B -> official prompt adapter comparison. These are research follow-ups, not implementation authorizations.
