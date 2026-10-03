# Phase 0 compatibility report — face-first character master

Author: Claude Code · Date: 2026-10-01 · Scope: read-only inspection; no weights downloaded, no WanGP change, no GPU.
Parent task: [face-first-character-master-workflow-TASK.md](face-first-character-master-workflow-TASK.md).
Evidence levels: **observed** = read from a file/URL today; **inferred** = reasoning from observed facts;
**unverified** = needs the authorized pilot.

## 1. Xpade Face Liquify

- The tool is a web app at `https://xpade.dothome.co.kr/` (single `index.html`, `sw.js` v1.9.5, manifest). The
  Google Drive link behind `bit.ly/4d22JEk` needs a Google sign-in and was not used. (observed)
- `index.html` hides its ~90 KB application script as base64 chunks XOR-ed with a key stored in the same file, then
  runs it with `Function()`. The key is public, so it was decoded statically without executing anything. (observed)
- Decoded code contains no `fetch`, `XMLHttpRequest`, `sendBeacon`, `WebSocket`, analytics or cookies. Images are read
  with `FileReader`, processed on a canvas and saved as `liquify-result.png` via a data URL. The only browser storage
  is the language preference. (observed)
- External loads: `human.js` 3.3.6 (cdnjs), face models from `cdn.jsdelivr.net/npm/@vladmandic/human/models/`
  (unpinned path; detector, mesh, iris, attention enabled), Google Fonts. `sw.js` caches only the app shell and those
  CDN hosts. (observed)
- Models actually available: `blazeface`, `facemesh`, `iris`; `facemesh-attention` is not published in 3.3.6 (404),
  so Human falls back. This does not affect privacy. (observed)
- Residual risk: the operator can change the served code at any time (obfuscation prevents casual audit), and the
  model path is unpinned. Mitigation: use copies only, record the hashes below, and re-check the `index.html` hash
  before each session. Static analysis only; a live network capture is still to be done at first use. (inferred)
- Local pin: `D:\codex\XAI-studio\.tmp\xpade-inspect\` holds the site files, decoded script, `human.js` 3.3.6 and the
  three models with `SHA256SUMS.txt`. `index.html` SHA-256
  `6eaa281a361c73dbb1bfaf328f5a29d4f16ecdcaa8f8a96a9788e58db316a4f4`. This folder is untracked scratch; it does not
  run the app.
- Correction to the idea note: the app is not a 13 KB wrapper; it is ~90 KB and only the models are external.

## 2. BFS Krea 2 head swap

Source: Hugging Face `Alissonerdx/BFS-Best-Face-Swap`, license MIT, not gated, revision
`0ca3913ade4b4ada458d60c232354e8586c4c181` (last modified 2026-09-27). (observed)

| Item | Value |
|---|---|
| File | `bfs_head_swap_v1.1_krea2.safetensors` |
| Size | 914,159,816 bytes |
| SHA-256 (LFS oid) | `abc6c468c578b36e6bd960106ad5886afd3f5321e4fe2de26c05bb5c6585b836` |
| Format | LoRA, rank 128, 512 F16 tensors, keys `diffusion_model.blocks.N.attn.*`, `mlp.*`, `txtfusion.*` |
| Inputs | Image 1 = base/body target; Image 2 = reference head |
| Prompt | `head_swap: replace the head with the reference head.` |
| Strength | 1.0 (workflow); repo says start at 1.0 and adjust |
| Workflow | `Head Swap Krea 2 - V1 Simple Workflow.json`: turbo model, 10 steps (note says 8 = stronger instruction adherence, 12 = more face detail), euler/simple, cfg 1; RAW 40 steps, cfg 3-4. The saved KSampler widget itself shows 8 steps. |
| Resolution | latent 848x1280; note says 1 MP is the sweet spot |
| Extra dial | `ref_boost` 4.0 recommended in the workflow note (reference fidelity); 1.0 = classic v1.1 |

The ComfyUI workflow depends on custom nodes `Krea2EditModelPatch` and `Krea2EditGroundedEncode`, with the
`qwen3vl_4b_fp8_scaled` text encoder and `qwen_image_vae`. (observed)

## 3. WanGP loader compatibility (static)

- Installed model `krea2_turbo_edit` ("Identity Edit v1.2") already loads one LoRA of the same family:
  `loras/krea2/krea2_identity_edit_v1_2.safetensors`, 512 F16 tensors. The BFS key set is **identical** (512 of 512
  key names, none differing) with the same tensor dimensionality; only the rank differs (128 vs 256). (observed)
- WanGP applies model-definition LoRAs and the user's `activated_loras` as separate lists and merges their schedules
  (`wgp.py` `get_transformer_loras` and `parse_loras_multipliers(..., merge_slist=...)`), so stacking BFS on top of
  Identity Edit is supported by design. (observed)
- `models/krea2/krea2_main.py` encodes each ordered reference image as extra tokens with frame index 1, 2, ..., so
  `image_refs = [body, head]` preserves "Image 1 / Image 2" order. Mode `KI` makes the first image the scene; the
  handler allows at most two refs. (observed)
- The local base checkpoint is `Krea2Turbo_quanto_bf16_int8.safetensors` (quanto INT8, 13.49 GB). **The task text
  says "Krea 2 Turbo int8 ConvRot"; no Krea ConvRot file exists locally** (ConvRot files are LTX, MiniMax and
  Qwen3-VL). The workflow's `krea2_turbo_int8_convrot` is a ComfyUI-side checkpoint. (observed)
- Verdict: **key-level and ordering compatibility is strongly indicated; actual loadability and quality are
  unverified.** Open questions only the pilot can settle:
  1. Whether the BFS LoRA expects the Identity Edit LoRA active, absent or replaced (ComfyUI's patch node is not the
     same as WanGP's built-in LoRA).
  2. WanGP has no equivalent of `ref_boost`; the recommended 4.0 may not be reproducible.
  3. Image fit/crop and text-encoder grounding sizes differ between the two stacks.
  4. LoRA merge quality at strength 1.0 on a quantized checkpoint.
- Contract gap: `tools/local_wangp.py` `REFERENCE_MODELS` accepts `krea2_turbo_edit` with 1-2 refs, but the
  validated reference path records no LoRA name, hash or strength. A BFS run through it would hide evidence the task
  requires. A writer must add that evidence first (additive, with an old-record fixture).

## 4. Proposed first test (not executed; needs operator approval)

- Download only `bfs_head_swap_v1.1_krea2.safetensors`, pinned to revision `0ca3913a...`; verify the size and
  SHA-256 above; place it in `D:\AI\WanGP\loras\krea2\`. No whole-repository download.
- Run one image: model `krea2_turbo_edit`, `video_prompt_type` `KI`, `image_refs` [body target, reference head],
  the prompt above, 10 steps, guidance 0 (cfg 1 equivalent for turbo), `activated_loras` [BFS file], multiplier 1,
  resolution about 848x1280, fixed recorded seed, Identity Edit v1.2 left as the model default. No retry. The output
  enters Gallery as restricted `needs_review`.
- The GPU must not be shared with a resident Ollama model (see the VRAM-contention memory).

## 5. Proposed Phase 1 file scope (additive, smallest first)

1. Deterministic, no GPU: a lineage/recipe record writer with schema and old-record fixture, as new files
   `tools/face_master_lineage.py` and `tests/test_face_master_lineage.py` (roles `concept_dna`, `face_candidate`,
   `sculpted_face_candidate`, `body_target`, `composite_candidate`; hashes, provider/model, exact prompt, LoRA
   name/hash/strength, ordered inputs).
2. Only after the first pilot: record LoRA evidence in the WanGP reference path. That touches `tools/local_wangp.py`,
   which has uncommitted Qwen-integration edits, so it needs that scope's editor or must wait for those edits to be
   committed.
3. No Studio UI, no database, no change to Qwen/Krea identity-edit behavior.

## 6. Decisions for the operator

- Approve the 914 MB LoRA download and one GPU test, and name the existing fictional adult character, the face and
  the body target; or ask for further static checks first.
- Confirm the lineage module (item 1 above) may be built before the pilot.
