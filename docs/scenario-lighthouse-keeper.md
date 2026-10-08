# 시나리오: 등대지기 (The Lighthouse Keeper)

- Date: 2026-10-08
- Type: Creative Treatment (frontier 작성)
- 분량: 60초 내외, 5~10초 클립들의 조립
- 인물: 1명 (일단 1명으로)

본 문서는 [Creative Treatment / Production Storyboard 역할 분리
proposal](creative-treatment-production-storyboard-role-split-PROPOSAL.md)에
따른 Creative Treatment다. 샷 수·카메라 경로·타이밍·렌더러 프롬프트는 확정하지
않으며, 아래 "제안 비트 구조"는 Hermes가 재설계할 수 있는 제안일 뿐이다.

---

## 1. Creative Treatment

```yaml
concept: >
  폭풍우 치는 밤, 외딴 섬 등대. 등대지기가 거대한 램프에 불을 밝히는 60초.
  빛을 켜는 것이 곧 누군가를 살리는 일이다.

viewer_should_understand: >
  누군가의 하룻밤 임무. 거대한 자연 앞에서 한 사람이 하는 작고 정확한 일.

viewer_should_feel: >
  고립의 위압 → 묵묵한 의무감 → 점화의 전율 → 안도

story_arc: >
  세계(폭풍) → 등장(계단) → 정체(얼굴 공개) → 임무(점화) →
  페이오프(먼바다 불빛) → 정지(미소)

key_visual_moments:
  - 폭풍우 밤의 등대와 회전하는 광선 (드론 에스타블리싱)
  - 파도가 등대 받침을 때리고 물보라가 렌즈를 덮음
  - 램프 불빛 아래 공개되는 얼굴 — 정체 앵커
  - 하우징 속 불꽃이 커지다 광선 폭발
  - 먼바다에 응답하듯 깜빡이는 작은 불빛들 (구조 장면 없음)
  - 광선이 스치는 얼굴, 2초 정지 (포스터 프레임)

important_objects:
  - 오일 램프 (휴대 → 램프실 거치)
  - 점화봉
  - 철문 (반쯤 열린 상태)
  - 거대 렌즈 하우징

reference_grammar:
  - "#84: 웜/쿨 대비 그레이딩 — 차가운 폭풍 vs 따뜻한 램프빛"
  - "#81: 정지 엔딩 — 끝 2초 홀드, 썸네일용 포스터 프레임"
  - "T-40: 무대-인물 분리 — 프롤로그는 인물 없이, 인물은 컷 뒤에 등장"
  - "T-21: 결과만 보여주기 — 구조는 렌더하지 않고 배 불빛으로 추론"
  - "T-37: 점화 순간(성냥 긋기)은 컷 사이 생략"

known_failure_risks:
  - "P-16: 멀티샷 인물 일관성 — 캐릭터 시트 선행 필수 (특히 뒷모습→정면 전환)"
  - "손가락 미세 동작(성냥 긋기) 렌더 금지 — 비트 분리로 회피"
  - "폭풍우 물 시뮬레이션 과부하 — 프롤로그는 광선+파도 실루엣 위주"

production_risks:
  - "클립 단위 렌더 비용 — 실패 시 해당 비트만 리테이크 (chunked)"
  - "광선 폭발 샷의 노출 튐 — 하이라이트 클리핑 주의"

creative_freedom:
  - "클립 수·카메라 경로·타이밍은 Hermes가 재설계 가능"
  - "아래 비트 구조는 제안이며 확정 아님"
  - "엔딩 미소는 유지 권장 (포스터 프레임), 그 외 표정 연기는 자유"
```

---

## 2. World Bible (consistency bible — 전 씬 주입용)

H3 롱비디오 노트의 "consistency-bible text injected into every scene"에 해당.
모든 클립의 프롬프트에 이 블록이 주입되어야 한다.

```text
WORLD: Early 1900s, a lonely island lighthouse on a stormy night.
GRADE: Cold blue-grey storm vs warm oil-lamp light. High contrast between
the two light sources; the lamp glow is the only warmth in frame.
WARDROBE LANGUAGE: Heavy oilskin coat, hood, thick boots — clothing that
belongs to a storm world. No modern materials, no bright colors.
CHARACTER: The lighthouse keeper, a middle-aged man with a rough beard
and deep wrinkles. Appearance locked by character sheet (P-16).
PROPS: Oil lamp (carried, then set down in the lamp room), lighting rod,
half-open iron door, giant lens housing.
```

---

## 3. 제안 비트 구조 (non-binding — Hermes 재설계 가능)

각 비트는 존재 이유(Necessity Test), entry/exit 상태(P-30),
renderability 판정을 포함한다.

### C1 (8s) 프롤로그 — 폭풍의 바다, 등대 광선
- 존재 이유: 세계 확립. 고립과 임무의 무대
- entry: 검은 파도 → exit: 광선이 화면을 가로지름
- 판정: 인물 0명, 공간 관계 1개 → **DIRECT / easy**. 레퍼런스 불필요 (T-40 phase 1)
- EMOTION: 위압적 고요

### C2 (7s) 프롤로그 — 파도가 받침을 때림
- 존재 이유: 위험의 스케일 확립
- entry: 파도가 밀려옴 → exit: 물보라가 렌즈를 덮음
- 판정: **DIRECT / easy**. 물보라 = 자연 와이프 → 다음 컷으로 (T-33)
- EMOTION: 위협

### C3 (8s) 등장 — 나선 계단 (뒷모습)
- 존재 이유: 인물 도입. 얼굴은 아직 공개하지 않음
- entry: 계단 아래 어둠 → exit: 램프를 든 뒷모습이 위로 사라짐
- 판정: 걷기 + 램프 들기, 공간 관계 2개 → **PARTIAL / medium**.
  뒷모습이라 얼굴 락 불필요 — 정체는 C4에서 확립
- EMOTION: 묵묵한 의무감

### C4 (7s) 클로즈업 — 얼굴 공개
- 존재 이유: "누군지 구분" — 정체 앵커 샷
- entry: 램프 불빛 아래 얼굴 → exit: 정면을 향한 눈빛
- 판정: 정적 1포즈, 공간 관계 1개 → **DIRECT / easy**. 캐릭터 시트로 외모 고정
- EMOTION: 결연함

### C5 (8s) 램프실 — 철문을 밀고 들어감
- 존재 이유: 액션 개시. 임무의 물리적 단계
- entry: 반쯤 열린 철문 → exit: 거대 렌즈 하우징 앞에 섬
- 판정: 밀기는 당기기보다 쉬움 → **PARTIAL / medium**. 문 상태는 소품 원장에 기록
- EMOTION: 집중

### C6 (8s) 점화 — 빛이 켜지는 순간
- 존재 이유: 클라이맥스
- entry: 점화봉을 든 손 → exit: 광선 폭발
- 판정: 성냥 긋기는 손가락 미세 동작이라 **렌더 금지**. 비트로 나눔 —
  얼굴에 번지는 불빛(반응) → 하우징 속 불꽃 → 광선 폭발.
  긋는 순간은 컷 사이에 생략 (T-37)
- EMOTION: 전율

### C7 (8s) 페이오프 — 광선이 폭풍을 가름
- 존재 이유: 임무의 의미. 구조는 보여주지 않음
- entry: 회전하는 광선 → exit: 먼바다에 작은 불빛이 응답하듯 깜빡임
- 판정: 인물 없음 → **DIRECT / easy**. CONSEQUENCE_ONLY (T-21)
- EMOTION: 안도

### C8 (6s) 정지 — 광선이 스치는 얼굴, 미세한 미소
- 존재 이유: 포스터 프레임 (#81 정지 엔딩)
- entry: 광선이 얼굴을 스침 → exit: 2초 홀드
- 판정: **DIRECT / easy**
- EMOTION: 평온한 자부심

---

## 4. 제안 Continuity 전략 (H3 노트 어휘 — Hermes가 최종 결정)

| 경계 | 제안 전략 | 근거 |
|---|---|---|
| C1→C2 | DELIBERATE_MONTAGE | 같은 세계의 몽타주. 시간 연속 불필요 |
| C2→C3 | HARD_CUT | 물보라 와이프가 가림막. 인물 첫 등장 |
| C3→C4 | REFERENCE_ONLY | 동일 인물. 캐릭터 시트로 정체 유지 |
| C4→C5 | HARD_CUT | 장소 이동 (계단→램프실). 소품(램프) 상태 인계 |
| C5→C6 | REFERENCE_ONLY | 동일 공간·인물. 램프 거치 상태 유지 |
| C6→C7 | HARD_CUT | 내→외 전환. 광선이라는 시각 모티프가 다리 |
| C7→C8 | HARD_CUT | 외→내. 미소 엔딩은 독립 샷 |

원칙: "chaining transfers good state; chaining also transfers bad state."
시간 연속이 실제로 가치를 더하는 경계가 없으므로 LAST_FRAME 체이닝은
기본값으로 쓰지 않는다.

---

## 5. 이력

- 2026-10-08: Somni(프론티어)가 사용자 요청으로 Creative Treatment 초안 작성.
  T-40(무대-인물 분리) 아이디어는 사용자의 것 (#84 분석 중 도출).
  CheerSelfAI 라이브러리 리뷰 및 레퍼런스 코퍼스(#1–#84) 반영.
- 다음 단계: Hermes가 Production Storyboard로 전환 (샷 수·카메라·타이밍 확정),
  캐릭터 시트 선행 제작 후 클립 렌더.
