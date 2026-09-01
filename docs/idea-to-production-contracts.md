# Idea-to-Production Contracts

Status: v1 field names and enums are owned by Codex and frozen for Hermes package C3.

The normal durable flow is:

```text
idea-production-request-v1
→ storyboard-candidates-v1
→ explicit user choice
→ renderer-job-request-v1 (sample)
→ review / regenerate
→ renderer-job-request-v1 (final)
→ production-job-result-v1
```

Rules:

1. Reference asset IDs are opaque. Resolve them only through an approved adapter; never infer a filesystem path.
2. Explicit user constraints outrank Stable Character DNA, scene requirements, style enrichment, and optional detail, in that order.
3. `exact` mode cannot creatively rewrite the supplied prompt. It must still create a durable request and Prompt Trace.
4. Stable DNA is read-only during production. A production result cannot silently modify it.
5. Every renderer submission has a durable job ID before execution and preserves failure or interruption state.
6. `result_session_id` is the Gallery handoff key. It is not a local directory path.
7. Missing references and renderer failures are structured errors, not guessed substitutions.

Claude package C3 may add workflow prose, templates, validation instructions, and deterministic fixtures. It must not rename schema fields, widen enums, or edit queue/API/adaptor implementations.

## Durable storyboard worker

`tools/idea_production_worker.py` is the execution boundary used by the private Studio API. The caller creates one request directory containing:

- `request.json` — valid `idea-production-request-v1`;
- `resolved-references.json` — approved adapter results for every character and asset ID;
- `status.json` — initial durable queue state.

Then it starts:

```text
python tools/idea_production_worker.py --job-dir <request-dir> --repo-root <this-repository>
```

The worker writes `storyboards.json` and atomically updates `status.json`. It stops at `needs_user_choice`; it never starts a renderer or changes Character DNA. Missing adapter references fail before the local LLM is called.
