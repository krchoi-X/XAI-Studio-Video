# Local Environment Status

Checked: **2026-08-22 (Asia/Seoul)**
Scope: read-only inspection only. No package, model, driver, workflow, service, or configuration was installed or changed, and no image generation was run.

## Summary

The PC already has enough system RAM, a CUDA-capable RTX 4070 Laptop GPU, and working local image-generation environments to act as the **low-cost preview and iteration tier** of the wider XAI-Studio production system. ComfyUI has already generated Krea2, FLUX.1 Krea, and Kroma test images, while WanGP has Z-Image Turbo INT8 weights and prior successful image outputs. The 8 GB VRAM limit still makes the official Z-Image BF16 path unsuitable for full GPU loading.

The realistic local role is **quantized model exploration and Character DNA preview**, one image at a time, with low-VRAM/offload behavior. A 5090 Pod should own BF16 baselines, high-resolution or batch production, repeated validation at production speed, and any future training work. Persistent creative state belongs in GitHub/asset storage; the local GPU and ephemeral Pod are replaceable compute tiers.

## Hardware

| Item | Observed state | Character Lab implication |
|---|---|---|
| GPU | NVIDIA GeForce RTX 4070 Laptop GPU, compute capability 8.9 | CUDA inference is available; laptop power limit observed at 80 W, so desktop-4070 timing should not be assumed. |
| VRAM | 8,188 MiB reported by `nvidia-smi` / 8.0 GiB reported by PyTorch | Too small for the official Z-Image BF16 components to remain fully resident; quantization and offload are required. |
| System RAM | 63.07 GiB total; 45.92 GiB available at inspection time | Good headroom for CPU offload, but offload trades VRAM pressure for latency. |
| CPU | AMD64, 24 logical processors | Adequate for orchestration and offload support; exact CPU model was unavailable because CIM access was denied in the sandbox. |
| OS | Windows build `10.0.26200.0`, 64-bit environment | Compatible with the installed portable ComfyUI package. |
| GPU driver | NVIDIA `610.88` | Driver is active and sees the GPU correctly. |
| Driver CUDA compatibility | `nvidia-smi` reports CUDA UMD `13.3` | This is the driver's supported CUDA level, not proof that the standalone CUDA Toolkit is installed. |

## Software

### Git and repository

- Git: `2.54.0.windows.1` at `C:\Program Files\Git\cmd\git.exe`.
- XAI-Studio repository: `main`, clean at inspection time, one local commit ahead of `origin/main` (`9172bb3`).

### Python and CUDA

Two separate Python contexts exist and must not be confused:

| Context | State |
|---|---|
| PATH Python | Python `3.11.14` in the Hermes agent venv. `torch`, `torchvision`, `transformers`, `diffusers`, `accelerate`, `safetensors`, `xformers`, and `triton` were not present. It is not a Character Lab image runtime. |
| ComfyUI embedded Python | Python `3.13.14`; PyTorch `2.13.0+cu130`, torchvision `0.28.0+cu130`, transformers `5.14.1`, safetensors `0.8.0`. |
| ComfyUI CUDA test | `torch.cuda.is_available() == True`; CUDA build `13.0`; RTX 4070 Laptop detected; BF16 support reported true. |
| Standalone CUDA Toolkit | `nvcc` not found, no `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA` directory, and no CUDA environment variables confirmed. |

The standalone Toolkit is not required merely to run the existing PyTorch CUDA wheels, but it may be required later by extensions that compile CUDA code. That need was not tested or addressed here.

### Ollama

- Installed at `C:\Users\krcho\AppData\Local\Programs\Ollama` and running locally.
- Local API reports Ollama `0.32.15`, nine installed models (about 138.9 GB total), and zero loaded models at inspection time.
- `ollama` is not on the sandbox PATH, although the running API at `127.0.0.1:11434` is reachable.
- Ollama is available for text-side assistance but is independent from the already prepared image-rendering runtimes.
- In the wider XAI-Studio design, it is a candidate for repeatable work such as Storyboard Draft 0, prompt compilation, metadata, and evaluation; difficult directing and critique may still be routed to a stronger frontier LLM.

### ComfyUI

- Portable installation: `D:\AI\ComfyUI_windows_portable`.
- Core: clean detached checkout at tag `v0.33.1` (`72865f4`).
- NVIDIA, CPU, and fast-FP16 launchers are present; none was started during this inspection.
- Custom nodes present: `ComfyUI-GGUF` and `krea2-svdquant`.
- Core Z-Image nodes and bundled Z-Image blueprint/templates are present, including Base/Turbo text-to-image and several control workflows.
- `extra_model_paths.yaml` connects `D:\AI\Models\image-generation`, which contains Krea2 Turbo W4A4, FLUX.1 Krea Q4, Kroma INT8/Q4, shared text encoders, and shared VAEs.
- Existing experiment records and output files show successful local generation at 768×1024: Krea2 Turbo W4A4 about 13.38 s, Kroma INT8 about 19.56 s, and FLUX.1 Krea Q4 about 81.57 s under their recorded settings. These are prior observations, not measurements repeated during this inspection.
- The ComfyUI-specific model paths do not currently contain Z-Image weights, but that does not mean the PC lacks them: WanGP has a separate working Z-Image installation.
- No ComfyUI process was running at inspection time.

### WanGP and shared model storage

- WanGP is installed at `D:\AI\WanGP` with separate image and video model support.
- Filesystem verification found `ZImageTurbo_quanto_bf16_int8.safetensors` (about 6.414 GiB), its VAE, Qwen3 INT8 text encoder, Z-Image presets/settings, and prior image outputs.
- The personal knowledge record reports successful Krea2 and Z-Image generation in WanGP on this RTX 4070, with the user preferring the existing ComfyUI Krea2 W4A4 result in that comparison.
- WanGP also contains MiniMax H3 and LTX assets used by the separate local-preview → 5090-final video strategy. Their presence does not make them the center of Character Lab.

## Z-Image feasibility

Z-Image is a 6B-parameter family. The official model card and ComfyUI guide say Z-Image-Turbo fits within **16 GB VRAM** consumer devices and identify three required ComfyUI components: a diffusion model, `qwen_3_4b` text encoder, and `ae.safetensors` VAE. The official ComfyUI repack also publishes lower-precision diffusion and text-encoder alternatives. Sources: [Tongyi-MAI model card](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo), [ComfyUI Z-Image guide](https://docs.comfy.org/tutorials/image/z-image/z-image-turbo), [Comfy-Org model files](https://huggingface.co/Comfy-Org/z_image_turbo).

### Realistic on this RTX 4070 Laptop (8 GB)

- Quantized **Z-Image-Turbo** through the already prepared WanGP INT8 path, not the full BF16 path.
- One image at a time for prompt checks and early Character DNA comparison; basic Z-Image execution is no longer hypothetical because prior outputs exist.
- Low-VRAM/offload operation, with system RAM absorbing components that cannot remain in VRAM.
- Conservative initial resolution (for example 512–768 px) before attempting 1024 px.
- Expect slower load/generation cycles and more sensitivity to quantization, node version, and memory fragmentation.
- Treat success as a feasibility result, not a production-speed or BF16-quality baseline.

The hardware boundary is an engineering inference from the observed 8 GB VRAM, available 63 GB system RAM, existing quantized runtimes, and the official 16 GB guidance. Prior local generations are historical evidence from `personal-ai-knowledge` and output files; no model was downloaded and no workflow was executed during this inspection.

### Send to a 5090 Pod (32 GB)

- Official BF16 Z-Image-Turbo baseline and comparisons against quantized local output.
- Z-Image-Base work where diversity, controllability, or fine-tuning behavior matters.
- 1024 px and larger production candidates, batches, parallel candidates, and repeated eight-slot Character DNA validation where turnaround matters.
- ControlNet or other multi-model graphs that increase simultaneous VRAM demand.
- Any future LoRA training or other training pipeline after it is separately approved and designed.
- Final repeatability/performance measurements for a production adapter.

NVIDIA specifies 32 GB GDDR7 for the RTX 5090, giving substantially more room for full-precision components and multi-model graphs: [official RTX 5090 specifications](https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5090/).

## Already prepared vs missing

### Already prepared

- RTX 4070 Laptop GPU with working NVIDIA driver and CUDA-visible PyTorch.
- 63 GB system RAM for low-VRAM offload experiments.
- Functional ComfyUI portable runtime with Z-Image core support and workflow templates.
- `ComfyUI-GGUF`, which is relevant to a future 8 GB quantized test.
- External Krea2, FLUX.1 Krea, Kroma, text-encoder, and VAE assets already connected to ComfyUI.
- Successful ComfyUI image smoke tests and lightweight upscale comparisons already recorded.
- WanGP Z-Image Turbo INT8 runtime, required weights, and prior successful outputs.
- XAI-Studio Character Lab documents and eight-slot validation plan.
- A pre-existing, model-neutral Jung Haewon character record in `personal-ai-knowledge`, including `ch-jung-haewon`, base appearance profile, recognition anchors, and the preserved source appearance prompt.

### Missing before Character Lab production validation

- Reconciliation of the XAI-Studio placeholder with the existing `ch-jung-haewon` source record; the earlier Character DNA must not be overwritten or duplicated blindly.
- A chosen first comparison path: the user-preferred ComfyUI Krea2 W4A4 baseline, WanGP Z-Image INT8, or a deliberate A/B of both.
- A Character Lab test protocol defining prompt module, resolution, seed policy, one-image concurrency, timing, peak VRAM, and identity-review fields.
- Eight-slot results using one approved candidate identity/reference baseline. General model smoke tests do not yet prove Character DNA consistency.
- Renderer-specific run records and an adapter maturity decision based on repeatable identity results rather than one successful image.

## Recommended boundary

Use the 4070 laptop for cheap, sequential Character Lab exploration and quantized feasibility checks. Promote only accepted Character DNA and prompt/spec decisions. Use a 5090 Pod for full-quality reference baselines, throughput-heavy validation, complex graphs, and future training. Keep both runtimes behind renderer-specific execution notes so local constraints do not alter the canonical Character DNA.
