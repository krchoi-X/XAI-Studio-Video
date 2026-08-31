# Krea2 Runtime Prompt

- variant: common-prompt
- submitted at: 2026-08-26T21:00:26+09:00
- renderer: WanGP v12.53
- model: Moody Krea 2 V7 INT8
- base model: Krea2 Turbo
- checkpoint: `D:/AI/Models/image-generation/krea2/moodyKrea2Mix_v70_INT8.safetensors`
- source canonical revision: v1
- batch size: 5
- seed: 242498957
- resolution: 1024x1024
- inference steps: 8
- LoRA: none
- refine: false
- upscale: false
- generation time: 178 seconds
- output: JPEG quality 95

## Exact submitted prompt

The user submitted canonical prompt v1. WanGP preserved the exact runtime prompt inside every JPEG's EXIF `UserComment` metadata. It normalised blank-line spacing and at least some non-ASCII punctuation during serialization, so the embedded runtime string is authoritative for byte-exact provenance rather than claiming it is byte-identical to the Markdown source.

- canonical source: `../canonical-prompt.md`
- embedded runtime prompt SHA-256: `379fb4a93e6e3b776a5df9caf6db8959e1d7bb8f7e3377fec583d68f03c5ffee`
- canonical source prompt SHA-256: `ff2a5cf714472cb83b5c4ff618b03884b02b89e79fbbd48336f493ec4cff783d`
- runtime prompt location: each `../outputs/krea2/krea2-*.jpg` EXIF `UserComment` JSON field `prompt`
