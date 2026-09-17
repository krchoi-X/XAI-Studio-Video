---
name: storyboard-cutboard
description: Load the shared storyboard-cutboard definition for this workflow.
---
<!-- shared-resource-adapter: 1 -->

This is a project entrypoint. From the configured XAI execution checkout run:

```text
python tools/shared_resources.py --skill storyboard-cutboard
```

Read the returned shared source before planning editorial shots. The shared source owns the skill; runtime schemas and validators remain in this execution checkout. Missing or inactive shared configuration is an error.
