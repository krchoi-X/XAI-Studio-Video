# Production incident — <short title>

Status: OPEN
Date: YYYY-MM-DD
Recorded by: <user|grok|hermes|codex|claude>
Requested reviewer: <Codex|Claude|both|unassigned>
Review authority: <review-only|bounded edit; describe exact scope>
Evidence level: <candidate|repeated|verified>

## Summary

<Two or three sentences: expected result, observed failure and why review is needed.>

## Production identity

| Field | Value |
|---|---|
| session ID | `<id>` |
| session path | `<absolute path>` |
| user request | `<verbatim request or link to provenance>` |
| GO / approval state | `<approved, held, remake not approved, etc.>` |
| requester | `<supported recorded value>` |
| orchestration / relay note | `<known fact or unknown; do not relabel requester/executor>` |
| executor | `<worker/host>` |
| engine | `<engine/provider>` |
| model | `<exact model ID/version>` |
| prompt mode / skill | `<mode and catalog source/hash when available>` |
| final renderer prompt | `<path; confirm literal Stable DNA included: yes/no/unknown>` |
| exact transform source | `<asset ID/path/role/SHA-256, or not an exact-source transform>` |

## Character and reference contract

| Character | DNA source + version/hash | Mandatory anchors | Selected references + roles | Known conflicts |
|---|---|---|---|---|
| `<ch-id>` | `<path/version/hash>` | `<observable anchors>` | `<path/hash: face/body/pose/etc.>` | `<none or conflict>` |

Record anatomical left/right explicitly when relevant. Note whether reference composition is native landscape, portrait, padded or cropped.

## Expected acceptance criteria

- <Observable condition 1>
- <Observable condition 2>
- <Observable condition 3>

## Observed result

| Pack/shot/run | Timestamp/frame | Observation | Severity |
|---|---|---|---|
| `<id>` | `<time>` | `<fact>` | `<HARD/Soft>` |

## Direct evidence

- Final prompt: `<absolute path and relevant line>`
- Settings: `<absolute path>`
- References: `<absolute paths and hashes>`
- Run record: `<absolute path/run ID>`
- Output: `<absolute path>`
- Review/result: `<absolute path>`
- Relevant code/config revision: `<commit or dirty diff path>`

## Facts

- <Directly observed or deterministically verified fact>

## Hypotheses

- <Inference, why it is plausible, and how to test it cheaply>

## Attempts already made

| Attempt | What changed | Result | Evidence |
|---|---|---|---|
| 1 | `<one variable or bounded change>` | `<improved/unchanged/regressed>` | `<path>` |

## Decision and current hold

- Current decision: `<preserve / reject / accept / wait>`
- Rerender authority: `<not granted / exact approved scope>`
- Must preserve: `<successful behavior and historical evidence>`
- Must not do: `<DNA edit, automatic retry, publication, etc.>`

## Questions for Codex/Claude

1. <Specific diagnostic or design question>
2. <Which layer should own the fix?>
3. <What is the smallest deterministic or one-sample verification?>

## Proposed smallest correction

<Proposal only; identify whether it belongs to the session packet, character workflow, engine adapter, shared skill or implementation contract.>

## Verification plan

1. <No-generation validation first>
2. <Optional single controlled sample, only with authority>
3. <Acceptance comparison and reviewer>

## Resolution

Final status: <leave OPEN until resolved>
Owner: <unassigned>
Changed files/commits: <none>
Checks: <not run>
Later production evidence: <none>
Remaining uncertainty: <state explicitly>
