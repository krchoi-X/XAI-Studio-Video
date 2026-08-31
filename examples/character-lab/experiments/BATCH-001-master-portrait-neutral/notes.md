# BATCH-001 Notes

## Question

Which engine and image best establishes Jung Hae-won's neutral master portrait identity?

## Before generation

- Expected strengths by engine: GPT Image should be strong at prompt adherence, natural portrait composition, and coherent facial anatomy.
- Known risks: generic AI beauty face, overly polished skin, insufficient midsummer contrast, identity variation across independent generations.
- Variables intentionally held constant: canonical prompt v1 and five independent candidates per engine.
- GPT Image generation note: candidates 2–6 form the five-image canonical v1 verbatim comparison set. Candidate 1 used a semantically equivalent structured normalization and is retained only as an exploratory result.
- Krea2 generation note: five-image WanGP batch completed with Moody Krea 2 V7 INT8 at 1024x1024, 8 steps, seed 242498957, no LoRA, in 178 seconds. WanGP embedded the full runtime configuration and prompt in each JPEG. Its serialization normalised whitespace/non-ASCII punctuation, which is recorded in `engine-prompts/krea2.md`.
- Z-Image generation note: five-image WanGP batch completed with Z-Image Turbo 6B INT8 at 1024x1024, 8 steps, seed 5109044, no LoRA, in 114 seconds. Its embedded runtime prompt hash exactly matches the Krea2 WanGP run, making these two local batches a direct prompt comparison.
- Paid single candidates: one Krea v2 Large image and one Qwen Image 3 Pro image were generated through Venice.ai. Both contain the same Venice-normalized runtime prompt hash. Treat them as qualitative single candidates, not five-sample consistency evidence.
- Chroma generation note: five Venice.ai candidates were generated at 1272x1896, 10 steps, CFG 5, LoRA strength 0, with a separate recorded seed for every image. The embedded runtime prompt hash matches the other Venice runs.
- Grok Image generation note: four candidates were generated at 1152x1728. The files expose signed provenance UUIDs but not prompt, seed, settings, or internal model version. Canonical v1 prompt usage is recorded from the user's report rather than claimed as file-verified.

## First pass — within each engine

| Engine | Best files | Why they survived | Repeated failures |
|---|---|---|---|
| Z-Image | | | |
| Krea2 | | | |
| GPT Image | | | |
| Nano Banana | | | |
| Grok Image | | | |
| Meta Image | | | |

## Second pass — survivors across engines

- preferred image:
- preferred engine/model:
- identity reason:
- realism reason:
- concerns:
- user decision:

## What to keep for the next batch

- prompt traits:
- model/settings:
- reference image:
- single variable to change next:
