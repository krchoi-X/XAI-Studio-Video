# Pre-migration video methodology backup

Status: immutable recovery manifest; not current production guidance.

This record preserves the methodology and shared-skill baseline immediately before the intent-preserving migration. The backup uses Git objects rather than copied guidance files so archived text cannot be mistaken for a second authority.

## Recovery points

- Runtime repository: `D:/codex/XAI-studio`
  - commit: `b666e28`
  - local annotated tag: `backup/pre-intent-methodology-20261003`
- Shared-skill authority: `D:/codex/XAI-Studio-Private`
  - commit: `8275a30`
  - local annotated tag: `backup/pre-intent-shared-skills-20261003`

The tags are local recovery references until an authorized push includes them. Git commits remain the underlying immutable evidence.

## File hashes at backup time

| Repository | File | SHA-256 |
|---|---|---|
| runtime | `SKILL.md` | `6621ab64950c492fbdc2fdf616d51977e348013e8673e80620985c1979df96a4` |
| runtime | `docs/architecture.md` | `ddb783d2d48206fca06c09640b67f1fbe9678a38f2bc1a43032b1201595b6411` |
| runtime | `docs/storyboard-directing.md` | `fadb9b5bc6d81854e2b13627919e5005a606be8a667b3f348497ad185ebbd021` |
| runtime | `docs/storyboard-rendering.md` | `910c3b80bffd15798943b67ff17f8b3173529af93e05acc01dcfab8798adff25` |
| runtime | `docs/director-memory/autonomous-video-quality-guide.md` | `bc88daa0748a6fdb691cd9fddc780d51fe3f04d8bf6809a58dd4e8073324ba6a` |
| shared | `shared-skills/storyboard-director/SKILL.md` | `f90898d621abd7a4e6b3234fe3b183a57b25fcc5f265cd0a27dd6c560b51448c` |
| shared | `shared-skills/storyboard-cutboard/SKILL.md` | `f59a161ea9f7a344760c9cd2e6ed2d1849fbf733debaba5d0f8bfb2eab37a0cf` |
| shared | `shared-skills/continuity-check/SKILL.md` | `4febe402030d069e923b0101efb433d094b6ad9b5796615a0041282f951843a7` |
| shared | `shared-skills/adaptive-video-production/SKILL.md` | `abf4534cf464d8dbf43f42b5745544c5f2c8855e94ea6bccd6e083a55f856b35` |
| shared | `shared-skills/adaptive-video-production/references/artifact-gates.md` | `72e086740405e15c2c58a4ad633d41191ed471eae8f8ff81481353a133858489` |

## Inspection and restoration

Inspect an old file without changing the working tree:

```powershell
git show backup/pre-intent-methodology-20261003:docs/architecture.md
git -C D:/codex/XAI-Studio-Private show backup/pre-intent-shared-skills-20261003:shared-skills/storyboard-director/SKILL.md
```

Restoration is a deliberate migration decision. Do not reset a working tree or replace current guidance automatically. Compare the required file, restore only the intended content through a reviewed change, and preserve newer production evidence.

