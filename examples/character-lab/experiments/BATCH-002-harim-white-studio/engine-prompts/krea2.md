# Krea2 execution record

- renderer: WanGP shared API
- model: Moody Krea 2 V7 INT8
- model type: `krea2_turbo_moody_krea`
- count: 10
- resolution: 768x1024
- steps: 8
- seed: 830202602
- LoRA: none
- prompt: `../prompt.txt`
- run: `../runs/run-20260830-201111-5be4805b`

WanGP embedded the effective settings and prompt in each JPEG EXIF `UserComment`. The run recorder hashed every output. Its current ffprobe-based metadata reader does not decode JPEG EXIF, so it conservatively labeled the artifacts `needs_review`; this is a recorder limitation rather than a generation failure.
