---
name: continuity-check
description: Load the shared continuity-check definition for this workflow.
---
<!-- shared-resource-adapter: 1 -->

This is a project entrypoint. From the configured XAI execution checkout run:

```text
python tools/shared_resources.py --skill continuity-check
```

Read the returned shared source before reviewing or repairing shot handoffs. The shared source owns the skill; runtime schemas and validators remain in this execution checkout. Missing or inactive shared configuration is an error.
