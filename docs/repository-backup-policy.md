# Repository and Backup Policy

Updated: 2026-08-31

## Purpose

Keep creative source-of-truth records recoverable without putting large media, local credentials, or private character-production history into a public repository.

## Repository roles

### `krchoi-X/XAI-Studio-Video` — public upstream

Use for generally reusable architecture, renderer adapters, sanitized documentation, schemas, templates, and examples that are safe to publish.

Do not push private character prompts, sensitive generation history, private review comments, local paths containing personal data, credentials, or unpublished media. The local checkout may temporarily be ahead of this public upstream; do not push it without reviewing the complete outgoing diff.

### Local `XAI-Studio` repository — tablet application source

Path: `C:\Users\krcho\Documents\ChatGPT\XAI-Studio`

Track the tablet web application, backend/frontend source, tests, documentation, reusable agent skills, and non-secret model configuration. Exclude databases, `.env`, virtual environments, build products, application logs, downloaded installers, and the nested consolidated-backup checkout.

### `krchoi-X/XAI-Studio-Private` — private consolidated backup

This is the off-machine source and metadata backup. It contains committed snapshots under:

- `XAI-Studio-Video/`
- `XAI-Studio/`

It may contain private Character DNA, prompt lineage, Scene Specs, Prompt Trace, generation manifests, Hermes workflows, and tablet application source. It must remain private. Verify repository visibility before every first push from a newly configured machine.

## Canonical storage by data class

| Data | Canonical location | Git policy |
|---|---|---|
| Character DNA and bounded identity states | `XAI-Studio-Video/characters/<id>/` | Private backup required |
| Scene Spec, prompts, Prompt Trace, run manifests | character generation session folders | Private backup required |
| Character Manager/Hermes tools and tests | `XAI-Studio-Video/tools`, `skills`, `schemas`, `tests` | Private backup; publish only after sanitization |
| Tablet application source | local `XAI-Studio/personal-prompt-studio` | Private backup required |
| Review database, favorites, comments, work queues | `personal-prompt-studio/data` and `D:\AI_Studio\workspace` | Never Git; separate data backup required |
| Generated images and videos | `D:\AI_Studio\library` | Never ordinary Git; separate media backup required |
| Models/checkpoints/LoRAs | local model directories and `D:\AI_Studio` | Never Git; preserve download source and checksum instead |
| Credentials/API tokens | OS keyring or local ignored `.env` | Never commit or copy into backup snapshots |
| Temporary downloads/research extraction | `inbox`, `tmp`, caches | Never Git unless deliberately promoted into a small sanitized reference |

## Backup cadence

Create a private consolidated snapshot:

- after a meaningful application or pipeline milestone;
- before migrations, schema changes, or bulk generation refactors;
- after approved Character DNA changes;
- at the end of a long production day;
- before reinstalling or moving the workstation.

Do not commit after every generated image. Commit stable code, decisions, schemas, prompts, and compact provenance together at useful checkpoints.

## Snapshot procedure

1. Stop or finish active writers when practical; never snapshot half-written queue files.
2. Run repository and application tests.
3. Check `git status` in both source repositories.
4. Confirm ignore rules exclude media, databases, models, logs, `.env`, and credentials.
5. Scan staged content for secrets and files larger than 20 MB.
6. Commit each source repository locally with a descriptive message.
7. Merge/fetch upstream only after preserving the local commit.
8. Export committed trees, not dirty working directories, into the private consolidated repository.
9. Commit and push the private consolidated repository.
10. Verify GitHub visibility is `PRIVATE` and local/remote divergence is `0 0`.
11. Record any media/data backup that remains outstanding.

## Media and operational-data backup

GitHub does not back up the actual generated library or tablet review database. Back up these separately:

- `D:\AI_Studio\library`
- `D:\AI_Studio\workspace`
- `personal-prompt-studio\data`

Use a second physical disk or encrypted cloud storage. Preserve relative paths and use checksums or a verified copy report. A GitHub push is not a complete workstation backup until these locations also exist elsewhere.

## Restore order

1. Clone `XAI-Studio-Private`.
2. Restore `XAI-Studio-Video` and `XAI-Studio` source trees.
3. Recreate Python/Node environments from committed manifests; do not restore virtual environments.
4. Restore the media library and operational data to their canonical paths.
5. Reinstall or redownload models and verify checksums.
6. Configure local `.env` and credentials from secure storage.
7. Run validation/tests, start the tablet app, sync the Library, and verify a known character session.

## Safety rules

- Never change the private backup repository to public without a full history audit.
- Never push the private local video checkout to the public upstream merely because it is ahead.
- Never treat Git-ignored data as backed up.
- Never store a sole copy of an accepted image, video, review database, or model only on an ephemeral GPU instance.
- For Vast/RunPod, download and verify durable outputs before deleting compute.

