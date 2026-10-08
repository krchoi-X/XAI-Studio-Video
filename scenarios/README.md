# Scenario Collection / 시나리오 모음

이 폴더는 **영상 제작을 위한 이야기와 승인 전 콘티**를 관리한다. 생성 엔진별 프롬프트나 실제 렌더 결과는 여기에 섞지 않는다.

- **원본 우선순위**: Story / Director Intent → Storyboard Spec → Shot Contract → renderer-specific prompt (파생 산출물).
- 시나리오에는 이야기의 인과관계, 인물/장소/소품 원장, 클립·숏 목록, 의도 보존 조건과 실험 평가 기준을 기록한다.
- 클립(편집상의 장면)과 생성 숏은 다르다. 복합 동작은 필요에 따라 여러 생성 숏으로 나눈다.
- 시나리오의 상태는 draft → reviewed → approved → produced로 관리한다. 실제 생성 결과를 검증하기 전에는 성공으로 표기하지 않는다.
- 제작 전 기존 `docs/storyboard-directing.md`, `docs/reference-driven-production-pipeline.md`, `docs/directing-technique-db.md`와 교차 검토한다.

## 목록

| ID | 제목 | 상태 | 내용 |
|---|---|---|---|
| LH-001 | [The Last Light of Day / 하루의 마지막 빛](./LH-001-the-last-light-of-day.md) | draft / experiment | 1905년경 등대지기의 일몰 점등 일상. 14클립, 약 90초. Muse 60초 원안에서 일상물로 전환. |

## 새 작품 추가 규칙

1. `<ID>-<slug>.md`로 파일을 만들고 이 목록에 등록한다.
2. **Story Intent / World Bible / Character & Prop Ledger / Beat & Shot Plan / Hard Locks / Test Plan / Open Issues**를 포함한다.
3. 새로운 AI의 창의적 연출은 허용하되, 승인된 사건 순서·상태·인과관계를 바꾸면 별도 revision으로 기록한다.
4. 이미지를 생성한 결과가 시나리오의 원본 명세를 대체하지 않도록 한다.
