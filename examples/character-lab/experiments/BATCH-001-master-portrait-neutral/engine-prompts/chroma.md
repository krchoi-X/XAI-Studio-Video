# Chroma Runtime Prompt

- variant: common-prompt
- provider: Venice.ai
- model: Chroma
- source canonical revision: v1
- generated images: 5
- resolution: 1272x1896
- steps: 10
- CFG: 5
- LoRA strength: 0
- seeds: 46141571, 73178285, 72069576, 10714853, 9211667
- EXIF datetime range: `2026:08:26 13:17:52–13:19:19` (timezone not embedded)

## Exact submitted prompt

Venice.ai preserved the exact runtime prompt in every PNG's EXIF `UserComment` JSON field `generationParams.prompt` and in `ImageDescription`.

- canonical source: `../canonical-prompt.md`
- embedded Venice runtime prompt SHA-256: `33766dab84c9ae2091d6854c63edf8178685303c215b8bb975cb1c65b3323aad`
- runtime prompt location: each `../outputs/chroma/chroma-*.png`

The hash matches the Krea v2 Large and Qwen Image 3 Pro Venice runs. Venice normalised `café` to `cafe` and the curved apostrophe in `Hae-won’s` to ASCII; the embedded value is authoritative for byte-exact provenance.
