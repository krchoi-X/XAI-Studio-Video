# Scenario Collection / 시나리오 모음

이 폴더는 **영상 제작을 위한 작가 시나리오와 그 개정본**을 관리한다. Hermes가 시나리오에서 파생한 프로덕션 콘티는 형제 폴더 `storyboards/`에 별도 보관하며, 생성 엔진별 프롬프트나 실제 렌더 결과는 어느 폴더에도 섞지 않는다.

기존 실험 문서에는 시나리오와 작가 측 숏 제안이 함께 들어 있을 수 있다. 그것은 역사적 원본으로 그대로 보존하되, 앞으로 Hermes가 작성하거나 수정하는 콘티는 `storyboards/`에 분리한다.

- **원본 우선순위**: Story / Director Intent → Storyboard Spec → Shot Contract → renderer-specific prompt (파생 산출물).
- 시나리오에는 이야기의 인과관계, 인물/장소/소품 원장, 장면·행동·대사, 의도 보존 조건과 필요시 작가의 연출 제안을 기록한다.
- 클립(편집상의 장면)과 생성 숏은 다르다. 복합 동작은 필요에 따라 여러 생성 숏으로 나눈다.
- 시나리오의 상태는 draft → reviewed → approved → produced로 관리한다. 실제 생성 결과를 검증하기 전에는 성공으로 표기하지 않는다.
- 제작 전 기존 `docs/storyboard-directing.md`, `docs/reference-driven-production-pipeline.md`, `docs/directing-technique-db.md`와 교차 검토한다.

## 목록

| ID | 제목 | 상태 | 내용 |
|---|---|---|---|
| LH-001 | [The Last Light of Day / 하루의 마지막 빛](./LH-001-the-last-light-of-day.md) | draft / experiment | 1905년경 등대지기의 일몰 점등 일상. 14클립, 약 90초. Muse 60초 원안에서 일상물로 전환. |
| VW-001 | [The Weaver's Day / 베 짜는 여인의 하루](./VW-001-the-weavers-day.md) | draft | 중세 마을 젊은 여인의 평범한 하루. 12클립, 약 81초. 물 긷기·빨래·베틀. |
| GH-001 | [The Greenhouse Ladybug / 온실의 무당벌레](./GH-001-the-greenhouse-ladybug.md) | draft | 22세기 밀폐 온실의 젊은 여성 식물학자와 미등록 무당벌레. 도입부 6클립, 약 55초. Ladybug Productions E05. |

## 새 작품 추가 규칙

1. `<ID>-<slug>.md`로 파일을 만들고 이 목록에 등록한다.
2. **Story Intent / World Bible / Character & Prop Ledger / Beat & Shot Plan / Hard Locks / Test Plan / Open Issues**를 포함한다.
3. 기존 무접미 파일은 revision 1로 취급한다. 작가가 시나리오를 수정하면 기존 파일을 덮어쓰지 않고 `<ID>-<slug>.r002.md`, `.r003.md`처럼 새 파일로 저장한다.
4. Hermes의 카메라·프레이밍·숏 분할 수정은 시나리오에 쓰지 않고 `storyboards/<ID>/storyboard-rNNN.md`에 기록한다.
5. 새로운 AI의 창의적 연출은 허용하되, 승인된 사건 순서·상태·인과관계를 바꾸는 제안은 시나리오 새 revision과 사용자 승인이 필요하다.
6. 이미지나 영상을 생성한 결과가 시나리오 원본 또는 콘티 명세를 대체하지 않도록 한다.

외부 작가에게 권장 형식을 전달할 때는 [`templates/external-writer-scenario.md`](../templates/external-writer-scenario.md)를 사용한다. 작가의 일반 문장이 권위이며 기법 코드는 선택 제안이다.
