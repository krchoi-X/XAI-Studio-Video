# Grok Bot 시작 지시문 — 외부 생성 결과 가져오기와 배치 제작

Updated: 2026-09-07
Status: A 구현은 scoped TASK에 완료 기록됨 — 실제 데스크톱/태블릿 재생 검증은 대기. B 생성 시험은 별도 사용자 요청 필요.
Owner: Grok Bot (가져오기 패키지와 아래에 명시한 영상 Gallery 통합 범위)
Integration owner: Codex

## 사용자 결정과 목표

사용자는 Grok Bot에도 일부 개발과 이미지·영상 배치 운영을 맡기기로 했다.
Hermes보다 우수하다는 결론은 아직 없다. 작은 실제 과제로 작업 완결성과 복구 능력을 검증한다.
첫 과제는 **GPT·Grok·Krea·Z-Image 등에서 만든 이미지와 영상을 기존 Studio Gallery에 가져와 열람·재생하는 도구와 통합**이다.
사용자의 후속 요청으로 이미지 전용 제한을 폐기하고 영상 지원을 첫 버전의 필수 완료 조건으로 포함한다.
새 갤러리나 생성 플랫폼을 만들지 않는다.

## 처음 받은 메시지처럼 읽고 실행할 것

1. `GROK.md` → `AGENTS.md`, `external_media_import/TASK.md`와 Git 상태를 읽는다. 공통 연계는 `docs/shared-agent-workflow.md`, 저장·Gallery 계약은 `docs/artifact-and-review-contract.md`를 따른다. 영상 프롬프트를 실제 설계할 때만 루트 `SKILL.md`와 창작 아키텍처를 추가로 읽는다.
2. `docs/agent-development-production-roles.md`와 이 문서를 읽는다. 과거 TODO보다 이 과제의 범위가 우선한다.
3. Git 상태와 실제 파일을 확인한다. 다른 에이전트의 수정 파일을 덮어쓰거나 함께 커밋하지 않는다.
4. 아래 경로에 접근 가능한지 확인하고, 가능한 개발부터 진행한다. 이 문서의 Windows 경로는 운영 PC 기준이며 클라우드 VM의 경로가 아니다.
5. `external_media_import/TASK.md`에 Goal, Constraints, Must NOT Do, Plan, Progress, Next, Blockers, Contract impact를 기록한 뒤 구현한다. 루트의 다른 과제 기록은 교체하지 않는다.

## 프로젝트 구조와 실제 사례

| 위치 | 용도 |
|---|---|
| `D:\codex\XAI-studio` | 캐릭터 레코드, 생성 기록, 로컬 생성 CLI, Control Tower |
| `D:\codex\personal-prompt-studio\personal-prompt-studio` | 사설 웹앱 프런트엔드와 백엔드 |
| `D:\codex\XAI-Studio-Private` | 비공개 백업 및 캐릭터 설정; 주 구현 저장소가 아님 |
| `D:\AI_Studio\library` | 실제 이미지·영상 파일; Git에 넣지 않음 |

현재 레이카 사례: GPT 기본 후보 10장, GPT 표정 비교 12장, Krea2 5장, Z-Image 5장.
Codex가 GPT 결과를 수동 등록했고 웹앱 이미지 API 및 32개 미리보기 GET 응답을 확인했다.
이 수작업을 재사용 가능한 가져오기 도구로 바꾸는 것이 첫 개발 과제다.

운영 PC에 있으면 다음을 조사한다. 원격 checkout에 없으면 누락이라고 정확하게 기록하고 합성 fixture로 개발을 계속한다.

- `output/register-reika-gpt-gallery.py`: 일회성 등록의 참고 자료. 그대로 범용 도구라고 취급하지 않는다.
- `output/reika-gallery-registration.md`: 완료 기록.
- `output/reika-gpt-expression-study-20260906/manifest.json`: 이미지별 프롬프트와 참조 기록.
- `characters/ch-mizuki-reika/02_generations/GPT-20260906-*/batch.yaml`
- Studio의 `backend/app/importer.py`: `import_batch`, `sync_character_repo`, `import_external_candidates`.
- Studio의 `backend/app/main.py`: `POST /api/sync`, 캐릭터 이미지 및 미리보기 API.

## A. 첫 개발 과제: 외부 이미지·영상 가져오기와 Gallery 통합

**편집 허용 범위:** `external_media_import/**` 안의 코드, README, TASK, 테스트 및 작은 합성 fixture.
추가로 영상 지원에 필요한 다음 Studio 파일과 직접 관련 테스트를 편집할 수 있다. Studio 루트는 `D:\codex\personal-prompt-studio\personal-prompt-studio`다.

- `backend/app/importer.py`: 이미지·영상 구분, 영상 probe, 썸네일, 기존 sync 가져오기 경로.
- `backend/app/main.py`: 기존 자산 상세 및 미리보기와 연결되는 영상 재생 응답.
- `backend/app/schemas.py`, `frontend/src/shared/types.ts`, `frontend/src/shared/api.ts`: 영상 길이·해상도·재생 URL 등 선택적 필드 전달.
- `frontend/src/apps/gallery/**`: 영상 표시, 플레이어, 썸네일, 메타데이터와 해당 테스트.
- `backend/tests/**`, shared types/API 관련 테스트 및 이 과제의 계약 문서.

작업 전에 Studio의 `AGENTS.md`, `TASK.md`, `DESIGN.md`, `docs/architecture/private-studio-public-app-boundaries.md`를 읽는다. Studio TASK에 기존 작업을 보존하며 담당·범위·Contract impact를 기록한다. 다른 Active editor가 작업 중이면 소유 파일을 덮어쓰지 말고 독립 브랜치/patch로 진행한다.
기존 `tools/`, `control_tower/`, 루트 실행 스크립트, 패키지 설정과 DB 마이그레이션은 이번 범위에 포함하지 않는다. 기존 metadata JSON과 선택적 필드 확장을 우선한다. 범위 밖 변경이 필요하면 최소 변경안을 인계한다.
위 파일의 영상 통합은 명시적으로 배정된 작업이다. 단순히 통합 파일이라는 이유로 구현을 중단하지 않는다. Codex는 최종 호환성 검토를 담당한다.

제안 실행 인터페이스는 `python -m external_media_import --help`다. 이 신규 패키지의 CLI는 Grok이 설계·구현한다.
README에 실제 실행 가능한 dry-run, apply, resume 예시를 제공한다.

### 입력과 처리

- 입력: 명시적인 입력 manifest, 원본 폴더, 캐릭터 ID, 배치 ID/제목, 출력 라이브러리 루트, 생성 기록 루트.
- 항목마다 원본 상대경로, engine/provider/model(알려진 경우), 원문 프롬프트, 참조 파일/ID, 사용자 요청, 알려진 생성시각을 받는다.
- 모델 버전·seed·시각을 모르면 미상으로 둔다. GPT로 만들었다는 이유로 세부 모델 버전을 추측하지 않는다.
- 입력 manifest의 경로가 허용 원본 루트를 벗어나지 않도록 검사한다. 절대경로와 `..`, symlink 탈출도 검사한다.
- 기본은 dry-run: 누락 파일, 유효하지 않은 이미지·영상, 중복, 계획된 복사와 기록 경로를 보고하고 파일을 쓰지 않는다.
- apply는 원본을 복사하며 원본 삭제·덮어쓰기 금지. 동일 배치·동일 파일·동일 hash 재실행은 no-op.
- 같은 목적지 파일명이 다른 내용이면 충돌을 명시한다. 조용히 덮어쓰거나 새 이름으로 중복 수입하지 않는다.
- SHA-256, 실제 해상도, 원본 위치, 프롬프트, 참조 관계를 보존한다. 이미지·영상 원본 내용을 변경하지 않는다. 영상 썸네일은 별도 파생 파일로 저장한다.
- 기본 승인 상태는 needs_review. 사용자 선택이나 별표, 기준 얼굴 승인을 만들어내지 않는다.
- visibility는 입력에서 명시적으로 받고 기존 값은 보존한다. 생성 엔진 이름으로 기존 제한 상태를 해제하지 않는다.

### 기존 Gallery와 맞물리는 출력 계약

기존 batch 구조와 sync 진입점을 재사용한다. 가져오기 패키지는 DB를 직접 쓰지 않는다. Studio에는 필요한 영상 읽기·재생 경로를 추가하되 기존 이미지 응답과 ID를 유지한다.

```text
<record-root>/<session-id>/
  batch.yaml
  prompt.txt
  import-provenance.json

<library-root>/<character-id>/generations/<session-id>/outputs/
  <engine>/image-or-video-files
```

- `batch.yaml`의 `session`: id, character_id, title, asset_root(실제 outputs 절대경로), visibility, status, prompt_file.
- jobs 또는 engines에는 provider/model과 output_dir를 실제 파일의 첫 번째 하위 폴더 이름과 맞춘다.
- `import_batch`는 outputs 아래 첫 경로 요소를 engine으로 표시한다. 예: `gpt`, `krea2`, `z-image`.
- 기존 importer의 prompt_text는 세션 공통 프롬프트다. 항목별 정확한 프롬프트를 상세 화면에서도 읽게 하려면 **항목별 세션**으로 나누는 기존 계약 내 방식을 지원한다. 다른 프롬프트를 하나로 뭉쳐 정확한 항목 프롬프트인 것처럼 표시하지 않는다.
- 원본별 프롬프트와 참조 hash는 provenance에 별도로 남긴다. 추가 정보를 UI가 읽는다고 확인 없이 주장하지 않는다.
- 모든 검증·복사가 끝난 뒤 discoverable `batch.yaml`을 마지막에 원자적으로 게시한다. 중단된 반쪽 배치를 완료 상태로 노출하지 않는다.
- 선택적 sync URL을 입력받아 `POST /api/sync`를 호출할 수 있다. sync 실패와 미디어 복사 실패를 구분하고 다시 생성하지 않고 sync만 재시도할 수 있어야 한다.

### 범위와 완료 조건

첫 버전은 PNG/JPEG/WebP 이미지와 MP4/WebM 영상을 지원한다. 최소한 MP4(H.264/AAC 또는 무음)와 WebM(VP9/Opus 또는 무음)을 실제 브라우저로 검증한다. 그 외 컨테이너·코덱은 지원 여부를 명시한다.

- 현재 이미지 전용 importer가 영상을 PIL로 열지 않도록 분기하고, batch 및 external candidate 경로에 일관되게 적용한다.
- `ffprobe` 등으로 duration_seconds, width/height, 실제 MIME, codec, frame rate와 오디오 유무를 확인한다. 확장자만 믿거나 길이를 추정하지 않는다. 도구가 없으면 필요한 설치/경로를 보고하고 완료로 처리하지 않는다.
- 원본은 `<library-root>/<character-id>/generations/<session-id>/outputs/<engine>/`에 저장한다. 운영 기본 library-root는 `D:\AI_Studio\library\characters`, record-root는 `D:\codex\XAI-studio\characters\<character-id>\02_generations`다. 경로를 README에도 그대로 명시한다.
- 영상 포스터는 Studio의 기존 preview cache에 저장해 원본 자산으로 중복 수입되지 않게 한다. 짧은 영상도 추출 가능한 시점을 사용하고 원본 hash는 보존한다.
- Gallery 목록에 영상 표시와 길이를, 상세에 길이·해상도와 `<video controls playsinline preload="metadata">` 재생을 제공한다. 자동 음성 재생은 하지 않는다.
- 재생 경로는 자산 ID로 등록된 원본을 찾고 기존 경로/접근 정책을 보존한다. 임의 파일 경로 입력을 허용하지 않는다. HTTP Range/206 및 탐색을 검증한다.
- 브라우저가 지원하지 않는 코덱은 원본을 보존하고 재생 불가 사유를 표시한다. 무단 원본 변환·덮어쓰기 없이 다운로드/별도 호환 사본 정책을 문서화한다.
- 이미지 전용 참조/변형 액션에 영상이 잘못 전달되지 않게 한다. 기존 이미지 확대·리뷰·favorite 동작은 보존한다.

### Contract impact — 영상 확장

Producer: external_media_import 및 Studio importer. Consumers: sync, assets/detail/preview/playback API, Gallery 카드·상세 플레이어, 기존 이미지 참조/변형 액션.
기존 이미지 batch.yaml과 asset ID를 보존하고 선택적 영상 메타데이터를 추가한다. 이미지 응답의 필수 필드를 제거하지 않는다. 구버전 이미지 fixture와 영상 fixture를 함께 검증한다.
영상 원본을 제거하는 마이그레이션은 하지 않는다. 롤백 시 신규 영상 수입/표시만 비활성화하고 원본과 provenance를 보존하며 기존 이미지 읽기는 계속 가능해야 한다.
패키지 TASK와 Studio TASK에 실제 변경 필드·경로·테스트를 기록하고 계약/호환성 checkpoint를 먼저 남긴다.

필수 검증:

1. 합성 이미지 3개, MP4 1개, WebM 1개와 서로 다른 프롬프트·참조 정보를 넣어 dry-run이 쓰기 없이 계획을 반환한다.
2. apply 후 파일 hash와 원본 hash가 같고 필요한 기록이 모두 존재한다.
3. 같은 배치 재실행 시 중복이 없고 기존 사용자 review/favorite를 건드리지 않는다.
4. 누락·손상 이미지·영상, 경로 탈출, 동일 이름/다른 hash, 중간 실패와 재개를 검증한다.
5. 동기화 실패 후 재시도 시 파일 복사·생성을 반복하지 않는다.
6. 가능하면 임시 DB와 합성 fixture로 기존 Studio `import_batch`가 출력을 읽는 통합 검증을 한다. Studio 코드 접근이 없으면 미검증으로 표시한다.
7. 이미지·영상 혼합 배치의 등록 개수, engine 표시, 모든 포스터 GET 200, 재동기화 중복 0을 확인한다.
8. 영상 원본 MIME과 Range/206, 재생·탐색, 실제 길이·해상도 표시, 무음 영상과 짧은 영상, 손상 파일·지원하지 않는 코덱을 검증한다.
9. 데스크톱과 태블릿 크기에서 영상 플레이어와 기존 이미지 확대·리뷰·favorite를 회귀 검증한다.
10. 로컬에 이미 있는 사용자 지정 영상이 있으면 새로 생성하지 않고 실제 가져오기·재생까지 확인한다. 대상이 명확하지 않으면 무관한 영상 전체를 수입하지 말고 합성 fixture 검증 후 대상만 확인한다. 운영 웹앱에 접근하지 못했다면 실제 재생은 미검증으로 보고하고 전체 통합 완료라고 하지 않는다.

개발 결과는 독립 브랜치의 커밋/PR 또는 적용 가능한 patch로 전달한다. 승인된 원격에만 push하고 운영 main에 자동 병합하지 않는다.
보고에는 변경 파일, 실행 명령, 테스트 결과, 실제로 확인한 환경, 아직 못 확인한 부분을 적는다.

## B. 다음 운영 시험: 레이카 이미지 배치 6장

A 구현에 실제 이미지 생성은 필요하지 않다. **이 문서는 신규 유료 생성이나 영상 실행 요청 자체가 아니다.**
사용자가 이 시험을 실행하라고 하면 다음 계획을 사용한다. 이미 지정된 엔진·수량·사용 조건은 다시 묻지 않는다.

- 얼굴 참조: 사용자 후보 GPT 06 또는 09. 두 얼굴을 혼합하거나 최종 승인됐다고 취급하지 않는다.
- 한 얼굴당 검은 재킷의 차분한 화보 표정 1장, 환한 일상 미소 1장, 합계 4장.
- 두 얼굴 각각 동일 조건 추가 1장씩, 합계 6장으로 재현성을 확인한다.
- 참조 파일이 없으면 파일 확보가 선행 조건이다. 텍스트만으로 대체하고 identity-preserving 결과라고 주장하지 않는다.
- 요청된 생성 서비스/모델을 사용한다. Grok Bot은 작업자이며 이미지 엔진과 같은 개념이 아니다.
- requested_by, executor=Grok Bot, 실제 provider/model을 분리 기록한다.
- 항목별 상태 queued/running/completed/failed와 결과 파일을 기록한다. 완료 파일이 검증된 항목은 재실행하지 않는다.
- 서비스가 제공하는 진행률만 표시한다. 없으면 활동/상태와 완료 항목 수를 표시한다.
- 합의된 수량을 넘겨 재생성하지 않는다. 실패·한도·로그인 문제를 정확하게 남긴다.
- 원본, 정확한 프롬프트, 참조 관계를 내려받고 A의 도구로 가져와 Gallery에서 검수한다.

평가: 요청 6개 대비 수집된 유효 파일 수, 누락 프롬프트/참조 수, 중복 수, 중단 후 재개 여부, 사용자 개입 횟수, 실제 소요 시간과 확인 가능한 사용량.
Hermes보다 낫다는 판단은 이 결과를 비교한 뒤 한다.

## 네트워크와 작업 환경

사용자 PC에는 Grok Bot 앱이 설치되어 있고 로컬 폴더를 읽고 있다. 먼저 위 Windows 경로와 로컬 Studio 접근을 실제 확인한다. 실행 도구가 별도 클라우드 VM에 있다면 그 VM의 `127.0.0.1:8787`은 사용자 PC가 아니므로 둘을 구분한다.
로컬 서비스 접근이 없으면 테스트 가능한 importer와 전송 가능한 결과 묶음을 만든 뒤 PC 반영 절차를 제공한다.
Tailscale 등 접속 설정이 이미 제공된 경우 그 주소를 사용한다. 임의 공개 터널이나 새 공개 배포를 만들지 않는다.
비공개 캐릭터 DNA, 원본, 로그인 정보는 공개 Git에 넣지 않는다. 테스트에는 작은 합성 이미지와 가짜 캐릭터 ID를 사용한다.

## Grok에 보낼 짧은 재개 메시지

> GROK.md와 external_media_import/TASK.md를 읽고 실제 Git diff부터 확인해줘. A에서 이미 구현된 부분을 반복하지 말고 남은 검증과 호환성 문제를 배정된 범위에서 처리해. 공통 저장·Gallery 계약을 유지하고, 확인한 환경과 미검증 부분을 scoped TASK에 기록해. B의 신규 생성 시험은 아직 실행하지 마.
