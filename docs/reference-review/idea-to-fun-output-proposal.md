# 제안 — 레퍼런스 자료를 "재미있는 결과물"로 바꾸는 구조

> 작성: Claude Code (claude-opus-5-5), 2026-09-26. **의견 문서**다. 결정은 사용자가, 구현은 담당 에이전트가 한다.
> 전제 자료: [evidence.md](2026-09-26-grok-muse/evidence.md), [claude-opinion.md](2026-09-26-grok-muse/claude-opinion.md).
> 다른 에이전트의 반론·보완은 맨 아래 §9에 append.

## 0. 한 줄 요약

**레퍼런스는 "패턴 카드" 라이브러리로 만든다. LLM은 카드를 골라 구조화된 Shot Plan만 쓴다. 렌더러별 프롬프트는 코드(어댑터)가 컴파일한다.**
이렇게 하면 어떤 LLM(Claude, Codex, Grok, Muse, Hermes의 로컬 Qwen)이 기획해도 같은 형식이 나온다. 그 결과를 H3, LTX, 외부 엔진이 각자 이해하는 언어로 바꾸는 일은 한 곳(어댑터)에서만 일어난다.

## 1. 지금 이미 있는 것 (새로 만들 필요 없음)

| 층 | 이미 있는 것 | 위치 |
|---|---|---|
| 기획 흐름 | 아이디어 → 2~3개 연출 후보 → 샘플 → 최종 | `skills/idea-to-production`, `skills/storyboard-director` |
| 스킬 선택 | 후보마다 스킬 2~4개를 고르는 라우터 (현재 스킬 11개) | `docs/director-memory/skill-router.json`, `tools/director_skill_router.py` |
| 구조화 계획 | Shot Production Plan 스키마 + 검증 + `compile_h3` | `schemas/shot-production-plan-v1.schema.json`, `tools/shot_production_plan.py` |
| 컴파일 원칙 | 기획 언어 ≠ 렌더러 언어, 최종 프롬프트는 컴파일 산출물 | `docs/director-memory/prompt-compiler-principles.md` |
| 정책 분리 | 창작·기술·호스팅 정책 제약 3분리, 거절되면 스토리 대신 렌더러를 바꿈 | `docs/renderer-policy-separation.md` |
| H3 실측 지식 | 오디오·대사 `<d>`, 크롭으로 프레이밍, 프롬프트 예산, FL2VA 이음 | `docs/claude-findability-and-h3-knowhow.md` |
| 로컬 LLM | Hermes → Ollama Qwen (abliterated 포함) | `docs/prompt-strategy-TASK.md` 등 |

**판단:** 뼈대는 이미 맞다. 빠진 것은 ① 레퍼런스가 이 뼈대에 연결돼 있지 않다는 점(Grok·Muse 합쳐 약 125건이 원자료 상태, 라우터 스킬은 11개), ② 어댑터가 H3 하나이고 그것도 실행 요약 수준이라는 점, ③ "재미"를 명시적으로 다루는 층이 없다는 점, ④ 패턴이 실제로 효과가 있었는지 측정하는 순환이 없다는 점이다.

## 2. 제안 구조 — 5개 층

```text
L0 Evidence      Grok 아카이브 + Muse 분석집 (원자료, append-only, 레퍼런스 ID 통일)
      │  추출(사람+LLM, 근거 링크 필수)
L1 Pattern Cards 모듈 라이브러리: 카드 1장 = 패턴 1개 (YAML/JSON, 렌더러 중립)
      │  라우터가 후보별 2~4장 선택
L2 Skills/지침    storyboard-director · idea-to-production · Fun Check
      │  LLM 출력 = Shot Plan(JSON, 카드 ID 인용)  ← 어느 LLM이든 동일 형식
L3 Adapters      코드: Shot Plan → H3 / LTX-2 / 외부 멀티샷 / 스틸·만화 패널
      │
L4 Render+Eval   렌더 → 실측(컷 검출·identity·플랜 대비) → 사용자 평가 → 카드 상태 갱신
```

핵심 원칙:
1. **LLM은 최종 프롬프트를 직접 쓰지 않는다.** Shot Plan의 칸을 채우고 카드 ID를 인용할 뿐이다. 그래서 LLM을 바꿔도 품질의 바닥이 무너지지 않는다.
2. **렌더러 차이는 어댑터에만 있다.** H3가 오디오 태그를 원하고 LTX가 긴 서술 문단을 원하는 차이는 코드가 처리한다.
3. **카드는 문법을 저장하지, 남의 프롬프트 원문을 저장하지 않는다.** 저작권 문제를 피하고, 복붙 대신 재조합을 유도한다.

## 3. L1 패턴 카드 — 라이브러리의 단위

Grok 카드(제작 문법, 실측)와 Muse 항목(프롬프트 기법, 증거 태그)을 **레퍼런스 ID 하나 아래** 합치고, 거기서 재사용 가능한 패턴을 뽑아 카드로 만든다. 카드 예시 (warehouse #33에서 추출):

```yaml
id: action.causal-impact-chain
family: action            # hook | camera | action | gaze | cut | audio | physics | look | gag | structure
viewer_effect: "타격이 '세다'는 말 대신 눈에 보이는 결과로 체감된다 (타격감)"
use_when: [1v1 physical contact, sports hit, drum/instrument strike]
avoid_when: [intimate slow scene, dialogue-led scene]
beats:                    # 슬롯 템플릿. 수치 대신 순서
  - setup: "{attacker} plants lead foot, weight shifts forward"
  - contact: "{limb} meets {target_part}"
  - reaction: "{target} displaced + {attacker} recoils"   # 양쪽 반응
  - evidence: "{secondary}: dust / fabric snap / debris, only after contact"
  - camera: "brief directional jolt on contact, then settles"
locks:
  hard: ["no camera shake before contact", "counter only after previous motion completes"]
  soft: ["exact punch order"]
renderers:
  h3:       {support: likely, note: "한 [Shot] 안에서 체인 1회. 10s 넘기면 FL2VA로 분할", verified: false}
  ltx2:     {support: likely, note: "한 문단 안에서 시간순 서술", verified: false}
  seedance: {support: yes, note: "원 레퍼런스 엔진", verified: "reference-only"}
evidence:
  refs: [muse#33, grok:PAT-20260925-warehouse-hitfeel-lt, muse#34, muse#38]
  independent_authors: 2  # jeong_do_ryeong, chase90re
status: candidate         # candidate → piloted → proven (우리 렌더러 A/B 후)
```

카드 설계 규칙:
- **viewer_effect 필수.** "무엇을 잠그나"보다 "관객이 무엇을 느끼나"가 먼저다. 지금 두 수집물 모두 통제(lock)에 치우쳐 있고 재미의 기능은 약하다.
- **renderers 칸에 검증 여부를 적는다.** 레퍼런스 엔진(Seedance, Dola)에서 된 것이 H3나 LTX에서도 되는지는 별개다.
- **evidence.independent_authors**로 신뢰도를 센다 (같은 저자 반복은 1).
- 크기: 카드 1장은 약 40줄. 작은 로컬 LLM에 3~4장을 넣어도 컨텍스트가 버틴다.

첫 배치는 **15~20장**으로 제한할 것을 권한다. 후보: 인과 타격 체인, 속도의 출처(컷 vs 모션), 컷 크기 사다리(CU↔MW↔ECU↔LS, 실사 만화), 시선 할당·시선의 호, Self-POV 락, 컷리스 모프 / 컷 트리거 변신, 스톨릭 대비 개그(cafeteria mute-stoic hinge), 첫 1초 훅(Necessity: 도입 가지치기), 헤드카운트·소품 락, 관계형 부정문, 상태 구별화(부력/무중력), boundary lock, 컷별 오디오 켜기/끄기, 연속성 토큰(라이트 트레일→로고).

## 4. "재미" 층 — Fun Check

통제만 잘하면 "틀리지 않은 영상"이 나오지, 재미있는 영상이 나오지는 않는다. Shot Plan에 다음 필드를 추가하고, 기획 LLM이 반드시 채우게 한다:

| 필드 | 질문 | 레퍼런스 근거 예 |
|---|---|---|
| `hook` | 첫 1~2초에 무엇이 시선을 잡나? | #37 즉시 절정, #38 "첫 초에 직접 전투 진입" |
| `engine_of_excitement` | 박진감의 출처는 컷 리듬인가, 샷 안의 모션인가? (하나를 고른다) | #27 컷 사다리 vs #33 원테이크 |
| `turn` | 기대를 한 번 뒤집는 지점 | cafeteria mute-stoic hinge, #36 변신 |
| `payoff` | 끝에서 무엇이 해소되나? | #37 로고 수렴, #39 시선 단절 |
| `contrast` | 무엇과 무엇의 대비를 쓰나? (크기, 속도, 감정, 소리) | 컷 크기 점프, 오디오 부정문 |
| `restraint` | 무엇을 **안** 넣나? 효과 상한 | Motion budget, "Match Cut 1회" |

여기에 **사용자 취향 기록**을 추가한다. 예: "만화 그림이 아니라 실사 + 다양한 컷 분할의 박진감"(#27에 대한 사용자 코멘트), Necessity Test에 대한 사용자 정정(2001 오디세이 사례). 이것은 `director-memory`에 선호 레코드로 쌓고, 라우터 가중치에 반영한다. 이 부분이 "사용자의 아이디어를 사용자 취향대로" 만드는 핵심이다.

## 5. L3 어댑터 — 렌더러마다 다른 언어

같은 Shot Plan이 렌더러별로 이렇게 달라진다 (방향 예시이며 문구는 확정이 아니다):

| | MiniMax H3 (로컬, 검증 多) | LTX-2 (WanGP에 존재, **로컬 미검증**) | 외부 멀티샷 (Seedance·Grok Imagine 등) | 스틸 / 실사 만화 |
|---|---|---|---|---|
| 형식 | `[Shot N]` 블록, 대사는 `<d>[lang] …</d>`, `overall_soundscape:`, `non_diegetic_music:` | 시간순 단일 서술 문단 (동작→카메라→빛→소리) | 섹션형 마스터 스펙 + 타임드 샷 + POSITIVE LOCKS | 패널별 이미지 프롬프트 + 레이아웃 |
| 프레이밍 | 샷 크기 단어 대신 "무엇이 프레임을 채우나/어디서 잘리나" | 공식 가이드 기준, 로컬 실측 필요 | 샷 크기 + FOV 수치 | 패널 크기 = 샷 크기 |
| 연속성 | 이전 클립 마지막 프레임 → FL2VA (검증됨) | 키프레임 조건 (검증 필요) | 레퍼런스 이미지 역할 분리 | 캐릭터 레퍼런스 + 같은 조명 레시피 |
| 예산 | 신원 블록을 짧게. 약 90단어 신원 블록이 행동을 밀어낸 실측이 있음 | 미측정 | 긴 프롬프트 허용 | 패널당 짧게 |
| 컷 | `[Shot 2+]`로 렌더 안 컷 (**로컬 미검증**) → 검증 1순위 | 클립 단위로 분할 | 모델이 컷 처리. 시각은 실측으로 확인(E4) | 컷 = 패널 |

**정정 (제 이전 의견):** claude-opinion.md에서 컷·비트표 문법(#13~#16)을 "우리 흐름에는 해당 없음, 보류"라고 했다. 하지만 H3 포맷은 한 렌더 안에 여러 `[Shot]`을 둘 수 있다 (로컬 미검증). 그래서 **"H3 멀티샷 검증 후 판단"** 으로 바꾸는 게 맞다. 이것이 검증되면 실사 만화식 컷 사다리를 한 번의 렌더로 만들 수 있다.

**실사 만화**는 같은 Shot Plan에서 두 산출물을 뽑는 방식을 권한다:
1. 패널 페이지: 컷 사다리를 스틸(Krea 2 등)로 → 패널 레이아웃 (`storyboard-director`에 이미 graphic-novel 분기가 있음)
2. 모션 코믹 / 영상: 같은 패널을 키프레임으로 → H3 FL2VA 또는 LTX로 사이를 움직임

## 6. LLM 이식성과 Hermes

목표는 "어떤 LLM이 기획해도 쓸 만하다"이다. 이를 위해:

1. **작은 단계로 쪼갠 기획 파이프라인.** 긴 문서를 통째로 읽히지 않는다. 단계마다 짧은 지시 + JSON 스키마:
   1. 아이디어 → Intent Brief (누가, 무엇을, 느낌, 길이, 매체)
   2. 라우터(코드)가 카드 후보를 좁힘 → LLM이 2~4장 선택하고 이유를 한 줄로
   3. 카드 슬롯 채우기 → Shot Plan 초안 (+ Fun Check 필드)
   4. 체크리스트 자기검증 → 코드 검증기(스키마 + 의미 규칙)가 반려하면 재시도
2. **각 단계의 지시문은 카드와 함께 약 2k 토큰 이내.** 로컬 Qwen 27~35B급이 따라올 수 있는 크기다. Claude나 Codex는 같은 단계를 더 잘할 뿐, 형식은 같다.
3. **역할 분담:**
   - Claude, Codex: 카드 추출, 어댑터 코드, 검증기, 리뷰
   - Grok: 레퍼런스 수집과 파일 실측 (강점)
   - Muse: 프롬프트 기법 분석 (강점)
   - Hermes → 로컬 Qwen: 호스티드 모델이 거절하는 내용의 기획 단계
4. **검열 관련 원칙 (기존 `renderer-policy-separation.md` 유지):** 창작 결정은 로컬 경로에서 왜곡 없이 유지한다. 호스티드 LLM이나 엔진이 거절하면 **내용을 우회해서 통과시키려 하지 말고, 그 단계를 로컬 LLM과 로컬 렌더러로 라우팅**한다. 호스티드 어댑터는 해당 서비스 정책을 지킨다. 스토리와 정책 판단을 섞지 않는 것이 결과 품질에도 유리하다.
5. **기획자 기록:** Shot Plan에 `planned_by` (실제 LLM·모델)를 남긴다. 같은 아이디어를 Claude와 Qwen으로 기획해 비교할 수 있어야 로컬 경로의 품질을 판단할 수 있다.

## 7. L4 평가 순환 — 패턴이 실제로 효과가 있었나

- **자동 실측:** 렌더 결과의 컷 시각을 Plan과 비교(E4에서 쓴 scene detect), identity 점수(얼굴 크기 보정 포함), 길이·화면비.
- **사용자 평가:** 후보 A/B 중 선택 + "재미 1~5" 한 줄 (`tools/pairwise_preference.py`가 이미 있음).
- **카드 상태 갱신:** 우리 렌더러에서 A/B 1회 이상 이긴 카드만 `proven`. 레퍼런스에서 많이 봤다는 것만으로는 승격하지 않는다.

## 8. 진행 순서 제안 (한 번에 다 만들지 말 것)

| 단계 | 내용 | 완료 기준 |
|---|---|---|
| P0 | 레퍼런스 ID 통일 (Grok 카드 ↔ Muse 번호), 카드 스키마 확정, 카드 15~20장 | 스키마 검증 통과, 카드마다 evidence 링크 |
| P1 | **H3 멀티샷 `[Shot 2]` 검증** + LTX-2 로컬 1회 실측 (8GB에서 불가하면 5090/클라우드) | 렌더러 칸의 `verified` 채우기 |
| P2 | Shot Plan에 `pattern_refs`, Fun Check, `planned_by` 추가 (하위 호환) + H3 텍스트 어댑터 완성 + LTX 어댑터 | 기존 플랜 fixture 통과 |
| P3 | Hermes 단계형 기획 파이프라인 + 검증기. 같은 아이디어 1건을 Claude와 로컬 Qwen으로 기획해 비교 | 두 플랜 모두 검증 통과 |
| P4 | 파일럿: 사용자 아이디어 1건 → 후보 2개 → 렌더 → 평가 → 카드 상태 갱신. 실사 만화 1페이지 포함 | 사용자 "재미" 평가 기록 |

P0~P1은 저비용이고, 이후 모든 판단의 전제다. 특히 P1의 H3 멀티샷 검증 결과에 따라 어댑터 설계가 크게 바뀐다.

**하지 말 것:**
- 125건 전부를 카드로 만드는 것 (평균화되어 재미가 사라짐)
- LLM에게 긴 지침서를 통째로 읽히는 것
- 레퍼런스 프롬프트 원문 복붙
- 실존 개인(예: 드럼 직캠)을 신원 참고로 쓰는 것
- 파일럿 전에 대규모 스키마 개편

## 9. 다른 에이전트의 검토 (append only)

형식: `### <날짜> <에이전트/모델> — 동의|반론|보완: <§번호>` + 근거

<!-- 여기부터 추가 -->
