---
name: screenplay-to-storyboard
description: Load the shared screenplay-to-storyboard definition for converting a versioned external scenario into a separately versioned Hermes production storyboard.
---
<!-- shared-resource-adapter: 1 -->

This is a project entrypoint. From the configured XAI execution checkout run:

```text
python tools/shared_resources.py --skill screenplay-to-storyboard
```

Read the returned source and the references it routes before doing the task. The shared source owns the skill; scenario files, storyboard files, runtime templates, schemas and validators remain in this execution checkout. Missing or inactive shared configuration is an error.

