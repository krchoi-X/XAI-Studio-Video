---
name: idea-to-production
description: Load the shared idea-to-production definition and adjacent references for this workflow.
---
<!-- shared-resource-adapter: 1 -->

This is a project entrypoint. From the configured XAI execution checkout run:

```text
python tools/shared_resources.py --skill idea-to-production
```

Read the returned file and its adjacent references before doing the task. That shared source owns this skill; edit it there. Runtime tools and schemas remain in this execution checkout. Missing or inactive shared configuration is an error; do not treat retained project reference copies as current authority. Existing routing and human approval rules still apply.
