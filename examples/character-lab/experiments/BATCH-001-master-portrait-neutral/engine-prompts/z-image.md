# Z-Image Runtime Prompt

- variant: common-prompt
- submitted at: 2026-08-26T21:09:19+09:00
- renderer: WanGP v12.53
- model: Z-Image Turbo 6B INT8
- checkpoint: `ZImageTurbo_quanto_bf16_int8.safetensors`
- source canonical revision: v1
- batch size: 5
- seed: 5109044
- resolution: 1024x1024
- inference steps: 8
- LoRA: none
- refine: false
- upscale: false
- generation time: 114 seconds
- output: JPEG quality 95

## Exact submitted prompt

The user submitted canonical prompt v1. WanGP preserved the exact runtime prompt inside every JPEG's EXIF `UserComment` metadata. Its serialized runtime string has the same SHA-256 as the Krea2 WanGP run, confirming that both local engines received the same WanGP-normalized prompt.

- canonical source: `../canonical-prompt.md`
- embedded runtime prompt SHA-256: `379fb4a93e6e3b776a5df9caf6db8959e1d7bb8f7e3377fec583d68f03c5ffee`
- canonical source prompt SHA-256: `ff2a5cf714472cb83b5c4ff618b03884b02b89e79fbbd48336f493ec4cff783d`
- runtime prompt location: each `../outputs/z-image/z-image-*.jpg` EXIF `UserComment` JSON field `prompt`
