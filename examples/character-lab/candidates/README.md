# Cross-batch Candidates

Only copy survivors here after an engine-level selection. For every copied image, add a sidecar `<filename>.yaml` containing:

```yaml
character_id: ch-jung-haewon
source_batch: BATCH-001
source_engine: z-image
source_file: ../experiments/BATCH-001-master-portrait-neutral/outputs/z-image/example.png
prompt_file: ../experiments/BATCH-001-master-portrait-neutral/engine-prompts/z-image.md
settings_file: ../experiments/BATCH-001-master-portrait-neutral/batch.yaml
selection_reason: null
```
