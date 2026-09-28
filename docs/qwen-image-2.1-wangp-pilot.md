# Qwen Image 2.1 uncensored GGUF — WanGP pilot

Date: 2026-09-28  
Scope: operator installation, first smoke test, and character-identity A/B. This guide does not make Qwen a production engine.

## Decision

Use Qwen Image 2.1 before expanding the video workflow. The immediate question is not whether it can make an attractive image, but whether it can preserve an approved identity while changing clothing, view angle, and sheet layout more reliably than the current Krea2 path.

Use `qwen-image-2.1-UC-Q4_K_M.gguf` for the first test. It is the publisher's recommended size/quality balance and is a realistic starting point for this machine's RTX 4070 Laptop GPU with 8 GB VRAM. “Uncensored” only means the checkpoint has no built-in safety checker; it does not imply better identity consistency.

## Update the existing WanGP installation

Use the existing `D:/AI/WanGP` checkout. Its `ckpts/`, `finetunes/`, `settings/`, `profiles/`, `outputs/`, and `wgp_config.json` are runtime data excluded from Git, so updating the tracked application code does not remove the models, settings, sessions, or outputs already used for Krea2 and video work. Keeping this checkout also makes the Qwen/Krea comparison use the same operating context.

One tracked source file, `shared/qtypes/int8_convrot.py`, contains a local scalar-scale compatibility fix. Preserve that patch before updating. Do not start with `scripts/update.bat` while this file is dirty: this WanGP version attempts a hard reset if its internal `git pull` fails.

Close WanGP, then run in PowerShell:

```powershell
Set-Location D:\AI\WanGP
git diff --output=D:/AI/WanGP-int8-convrot-local-20260928.patch -- shared/qtypes/int8_convrot.py
git stash push -m "before-qwen21-update-20260928" -- shared/qtypes/int8_convrot.py
```

Now use WanGP's updater:

```powershell
.\scripts\update.bat
```

Choose **1. Update**. It updates the tracked application code and installs current requirements into the existing active `env_uv`; it does not remove the existing runtime-data folders. After it finishes, `git log -1 --oneline` should show a revision from 2026-09-24 or later because Qwen Image 2.1 first appeared in WanGP v13.1315. Start WanGP normally:

```powershell
.\scripts\run.bat
```

The update may download changed Python/CUDA dependencies. Run it yourself when convenient; Codex should not run it as part of the preparation task. A separate `env_qwen21` is optional, not required; create one with `scripts/install.bat` only if you want an environment-level rollback point.

Leave the saved Int8 ConvRot patch in the stash during the Qwen smoke test; Qwen Q4_K_M does not use that local Int8 ConvRot change. If an older Int8 model still needs it afterward, inspect and apply it against the updated file rather than blindly popping the stash:

```powershell
git stash list
git stash show -p 'stash@{0}'
```

## Download the checkpoint

Download only this transformer for the first attempt:

- [qwen-image-2.1-UC-Q4_K_M.gguf (4.60 GB)](https://huggingface.co/abenzerps/Qwen-Image-2.1-Uncensored-GGUF/resolve/main/qwen-image-2.1-UC-Q4_K_M.gguf?download=true)

Save it as:

```text
D:\AI\Models\image-generation\qwen\qwen-image-2.1-UC-Q4_K_M.gguf
```

Do not download BF16, Q5/Q6/Q8, ComfyUI's separate VAE, or its text encoder for the first WanGP test. WanGP supplies its own compatible Qwen 2.1 VAE, processor, Qwen3-VL encoder, and vision files when the custom model is first loaded. Those companion downloads are additional to the 4.60 GB transformer and can require substantial disk/system RAM.

## Register it in WanGP

1. In the model selector, choose **Qwen Image 2.1 TextImage2Image 7B**. Do not generate with the base model first; that could download its default transformer.
2. Open the **Finetune Creator** from the `+`/finetune tool in the model toolbar.
3. Choose **Using Current Model**.
4. Enter:

   - Id: `qwen_image_21_uncensored_q4_k_m`
   - Name: `Qwen Image 2.1 Uncensored Q4_K_M`
   - Description: `Local 4.60 GB GGUF pilot; no automatic canonical promotion`

5. In **URLs**, use the folder picker and select:

```text
D:\AI\Models\image-generation\qwen\qwen-image-2.1-UC-Q4_K_M.gguf
```

6. Save, select the newly created finetune, and use these first-run settings:

   - 1024 × 1024
   - 40 steps
   - guidance 4.0
   - batch 1
   - Qwen 2.1 KV cache: Disabled
   - prompt enhancer: Disabled
   - no LoRA, TeaCache, recompilation, or extra accelerator

WanGP's current Qwen 2.1 handler recognizes a `.gguf` transformer and loads the remaining architecture files separately. This makes the route plausible, not guaranteed: the community checkpoint is not a built-in WanGP preset, so the first load is the compatibility gate.

## First smoke test

Use a non-canonical duplicate of one approved face-master image as reference 1. Run one edit at 768 × 768 first if 1024 fails for memory; otherwise keep 1024. Prompt:

```text
Reconstruct the same person from <image1> as a neutral studio head-and-shoulders portrait. Preserve facial proportions, eye shape and spacing, nose structure, jawline, skin tone, apparent age, and hairstyle. Neutral expression, mouth closed, even soft light, plain gray background. Do not beautify, stylize, change ethnicity, or redesign the face.
```

Record:

- WanGP commit and finetune id
- seed, size, steps, guidance
- peak VRAM and system RAM if visible
- total generation time
- console error text, if any
- input hash and output path

If it fails twice for the same reason, stop. Do not try random package upgrades or download another quantization; return the console output for diagnosis.

## Fixed identity gate

After the smoke test succeeds, run two fixed seeds for each row. Reuse the exact same approved master, resolution, and base identity wording.

| Gate | Requested change | Pass signal | Common failure |
|---|---|---|---|
| Reconstruction | No semantic change | Face remains recognizably identical without beautification | eye spacing, jaw, age, skin or hairstyle drifts |
| Clothing only | Replace top/outerwear | Face and hair remain stable; only clothing changes | face is regenerated or body proportions drift |
| 45-degree view | Turn head/body to three-quarter view | plausible same identity and stable distinctive features | generic new face or asymmetric collapse |
| 90-degree profile | Produce a clean side profile | internally plausible profile that agrees across both seeds | invented nose/jaw geometry changes between seeds |

The profile gate cannot prove ground-truth side geometry from a frontal master alone. It measures whether Qwen invents a stable, user-acceptable profile. If accepted, that profile becomes a separately reviewed angle master; it does not silently replace the original face master.

Compare against the already existing Krea2 Turbo/RAW evidence on:

- same-angle identity preservation
- isolation of the requested edit
- cross-seed consistency of invented profile geometry
- hands/body/clothing geometry
- speed, VRAM/RAM, and operational reliability

## Project adoption gate

Do not alter the production engine list on a successful single image. Adoption requires:

1. all four gates completed with manifests;
2. explicit user selection of any new angle master;
3. at least one reusable character-sheet layout built from individually approved views;
4. deterministic adapter tests showing existing `z-image` and `krea2` paths are unchanged.

If it passes, the project change is small but not zero: add a Qwen engine/architecture option to `tools/character_scene.py`, relax the Krea-only identity-reference guard in an engine-aware way, add Qwen reference/settings provenance, and expose the model through the maintained WanGP catalog. Until then, Qwen remains an isolated pilot.

## Sources checked

- [Qwen/Qwen-Image-2.1 model card](https://huggingface.co/Qwen/Qwen-Image-2.1)
- [Qwen Image 2.1 Diffusers pipeline](https://huggingface.co/docs/diffusers/main/api/pipelines/qwenimage21)
- [WanGP repository](https://github.com/deepbeepmeep/Wan2GP)
- [WanGP model documentation](https://github.com/deepbeepmeep/Wan2GP/blob/main/docs/MODELS.md)
- [WanGP finetune documentation](https://github.com/deepbeepmeep/Wan2GP/blob/main/docs/FINETUNES.md)
- [Uncensored GGUF model card and files](https://huggingface.co/abenzerps/Qwen-Image-2.1-Uncensored-GGUF)
