# WanGP model types on this workstation

**Generated file — do not edit by hand.** Refresh with `python tools/wangp_models.py --write`.

Generated: 2026-09-09T19:05:07+09:00  ·  WanGP: `D:\AI\WanGP`  ·  definitions: 217  ·  usable: 10

`model_type` is the file name of a definition in `<wangp>/defaults` or `<wangp>/finetunes`. Passing anything
else fails in WanGP validation before any GPU work starts. Check one id before submitting:

```bash
python tools/wangp_models.py --check minimax_h3_ref2va_pruned
```

## Usable now

Weights, modules and LoRAs are all present. `steps` and `guidance` are the definition's own defaults.

| model_type | steps | guidance | model |
|---|---|---|---|
| `flux_chroma` | 20 | 3.0 | Flux 1 Chroma 1 HD 8.9B |
| `krea2_raw` | 52 | 3.5 | Krea 2 RAW |
| `krea2_raw_edit` | 20 | 2 | Krea 2 RAW Identity Edit v1.2 |
| `krea2_turbo` | 8 | 0 | Krea 2 Turbo |
| `krea2_turbo_edit` | 8 | 0 | Krea 2 Turbo Identity Edit v1.2 |
| `krea2_turbo_moody_krea` | 8 | 0 | Moody Krea 2 V7 INT8 |
| `ltx2_25_22B_distilled` | 8 |  | LTX-2 2.5 Distilled 22B |
| `minimax_h3_fl2va_pruned` |  |  | MiniMax H3 FL2VA Pruned 20B |
| `minimax_h3_ref2va_pruned` |  |  | MiniMax H3 Ref2VA Pruned 20B |
| `z_image` | 8 | 0 | Z-Image Turbo 6B |

## Variants of the same models that are not usable

The definition exists, so the name looks plausible, but something it needs is not on disk.

| model_type | steps | guidance | model | missing |
|---|---|---|---|---|
| `flux` |  |  | Flux 1 Dev 12B | weights |
| `flux_chroma_radiance` | 20 | 3.0 | Flux 1 Chroma Radiance 8.9B | weights |
| `ltx2_25_22B` | 8 | 1.0 | LTX-2 2.5 Dev 22B | weights |
| `ltx2_25_22B_distilled_nvfp4` | 8 |  | LTX-2 2.5 Distilled NVFP4 22B | weights |
| `minimax_h3_fl2va` |  |  | MiniMax H3 FL2VA 33B | weights |
| `minimax_h3_ref2va` |  |  | MiniMax H3 Ref2VA 33B | weights |
| `z_image_base` | 30 |  | Z-Image Base 6B | weights |
| `z_image_control` | 9 | 0 | Z-Image Turbo Fun ControlNet v1 6B | module:Z-Image-Turbo-Fun-Controlnet-Union_bf16.safetensors |
| `z_image_control2` | 9 | 0 | Z-Image Turbo Fun ControlNet v2 6B | module:Z-Image-Turbo-Fun-Controlnet-Union2_bf16.safetensors |
| `z_image_control2_1` | 9 | 0 | Z-Image Turbo Fun ControlNet v2.1 6B | module:Z-Image-Turbo-Fun-Controlnet-Union2.1_bf16.safetensors |
| `z_image_control2_1_8s` | 8 | 0 | Z-Image Turbo Fun ControlNet v2.1 8 Steps YYY 6B | module:Z-Image-Turbo-Fun-Controlnet-Tile-2.1-2601-8_steps_bf16.safetensors |
| `z_image_nunchaku_r128_fp4` | 8 | 0 | Z-Image Turbo Nunchaku FP4 (r128) 6B | weights |
| `z_image_nunchaku_r256_int4` | 8 | 0 | Z-Image Turbo Nunchaku INT4 (r256) 6B | weights |
| `z_image_twinflow_turbo` | 2 | 0 | TwinFlow Z-Image Turbo 6B | weights |

A further 193 definitions for models not installed here are omitted; `python tools/wangp_models.py --all` lists everything.

## Notes

- A definition may borrow another model's weights (`URLs` naming another id), so two ids can share one file.
- Which ids have actually produced output here is visible in the Control Tower job history, not in this file.
