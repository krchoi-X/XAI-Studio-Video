# Z-Image execution record

- renderer: WanGP shared API
- model: Z-Image Turbo INT8
- model type: `z_image`
- count: 10
- resolution: 768x1024
- steps: 8
- seed: 830202601
- LoRA: none
- prompt: `../prompt.txt`
- run: `../runs/run-20260830-200507-5a90fc0e`

WanGP embedded the effective settings and prompt in each JPEG EXIF `UserComment`. The run recorder hashed every output. Its current ffprobe-based metadata reader does not decode JPEG EXIF, so it conservatively labeled the artifacts `needs_review`; this is a recorder limitation rather than a generation failure.
