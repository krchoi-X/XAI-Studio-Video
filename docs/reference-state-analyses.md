# Reference State 분석집 — Evidence-First

> XAI-Studio-Video 레퍼런스 추출 양식(`docs/reference-extraction.md`)에 맞춘 분석집.
> 작성: 2026-09-24, 최종 정리: 2026-09-25. 분석: Somni (Muse).
> 원문 규칙: **Visible evidence first. Unsupported inference stays out of the production spec.**

> ⚠️ **정정 요약 (Claude, 2026-09-26)** — Grok 레퍼런스 카드와 교차 검증하면서 파일 실측으로 확인한 사항이다. Somni의 원문은 수정하지 않았고, 해당 항목에 `⚠️ 정정` 주석만 붙였다.
> 근거와 재현 방법: `docs/reference-review/2026-09-26-grok-muse/evidence.md` (E1~E6).
> - #26: 파일은 1920×1080 가로 (9:16이 아님) — E5
> - #34: 게시물 캐러셀의 영상2(10.11s)는 분석되지 않음 — E1
> - #37: 엠블럼은 원형이 아니라 "S"자 / 농구 컷은 3.71–4.54s에 존재 / 뒤쪽 두 컷은 ±0.06s로 프롬프트 시각을 지킴 — E2~E4
> - #40: 거울벽은 프레임에서 확인되지 않음 (2초 간격 샘플 기준) — E6

## 증거 기반 표기

총 40건. 증거의 출처는 항목별로 밝힌다: 프롬프트에서 읽은 것은
`prompt-derived`, 영상 설명·작성자 댓글에서 읽은 것은 `author-described`,
실제 영상 프레임에서 본 것은 `frame-derived`, 내가 추론한 것은 `inference`.
추론은 프로덕션 스펙에 넣지 않는다 — 각 항목의 "관찰 vs 추론" 섹션에만 둔다.

- 프레임 분석 항목: 18·19·21·22·23·24·25·26·30·31·32·33·34·35·36(임베드
  스크린샷)·37·38(임베드 스크린샷)·39(직접 다운로드)·40(직접 다운로드).
  24번은 실패 사례.
- 기사 기반: 20·29. 프롬프트 표본(영상 미확인): 27·28.
- 39번(@AIwithzayn)은 프롬프트가 X 로그인 월 뒤에 있어 frame-derived로만
  기록. 프롬프트 확보 시 보강 예정.
- 양식 변천: 1–9번은 구 양식(Subject state / Composition / Camera evidence…),
  10–40번은 신 양식(기본 정보 / 관찰 / 관찰 vs 추론 / Control Levels /
  기여 패턴). 원문은 그대로 두고, 양식 차이만 여기서 명시한다.

## 패턴 → 프레임워크 매핑

분석 과정에서 뽑은 마스터 패턴과 XAI-Studio-Video 컴포넌트의 대응.
(2026-09-25 정리 시점에 8개 → 20개로 확장.)

| 마스터 패턴 | 대응 컴포넌트 | 출처 |
|---|---|---|
| 1. 앵커 락 (신원·의상·소품·장면 분리 고정) | Character DNA + Control Levels (Hard Lock) | 3·9·16·17 |
| 2. 상대 좌표 (인물 기준 위치·시선) | Spatial blocking + Shot Graph | 2·12·13 |
| 3. 자국 서술 (힘 대신 시각적 증거) | Reaction Evidence + Physics Lock | 5·8·26·33·34 |
| 4. 상태 전이 체인 (anticipation→contact→consequence) | Action Skeleton + Action Grammar | 8·26·33·35·36 |
| 5. 실패 기반 네거티브 | Constraints | 4·19·24·25·35 |
| 6. 절제 (효과 횟수 제한) | Motion Budget | 4·32·33·37 |
| 7. 오디오를 프레임 단위 권위로 | Audio DNA | 5·14·32·37 |
| 8. 복잡한 액션은 보여주기 (블렌더 블로커트) | Storyboard-first (저비용 프리비즈) | 7 |
| 9. 시선 할당 테이블 (공동/분리/상호 시선) | Shot Graph 확장 | 12·21·23·31 |
| 10. 배타적 립싱크 할당 | Audio DNA 하위 규칙 | 5 |
| 11. 레퍼런스 역할 분리 (기능별 1역할) | Character DNA 입력 규격 | 4·9·16 |
| 12. 모션 버짓 수치화 (횟수 상한 + 트리거) | Motion Budget | 4·33 |
| 13. 비트표는 순서만 신뢰 (절대 시간 불신) | Storyboard-first / Adapter 주의 | 31·37 |
| 14. POSITIVE LOCKS (금지보다 고정) | Control Levels (Hard Lock) | 33·37 |
| 15. capability-calibrated 언어 (모델 능력에 맞춘 서술) | Adapter 설계 원칙 | 33 |
| 16. boundary lock (물체 경계 유지) | Physics Lock | 34 |
| 17. 상태 구별화 (오류명에 ID 부여) | Constraints 어휘 | 8·35 |
| 18. 컷리스-모프 vs 컷-트리거 (변신 문법 2종) | Action Grammar | 1·36 |
| 19. Necessity Test (근거의 두 출처: 실측/authored) | Master Spec 근거 태그 | 37 |
| 20. 음악→LLM 시나리오→프롬프트 파이프라인 | 파이프라인 아키텍처 | 32·37 |

---

## 1. @codewithhajra — "THE LAST TRAIN" (15초 패션 필름)

**기본 정보**
- 출처: X (Twitter) @codewithhajra, 프롬프트가 트윗에 공개됨
- 길이: 15초 / 모델: 미상 (prompt-derived)
- 증거 기반: prompt-derived (프롬프트 전문) + author-described (영상 설명)

**Subject state** (prompt-derived)
- pose: 기차에 탑승하는 여성, 시간 전이에 따라 의상·헤어가 변함
- gaze: 프롬프트에 명시적 시선 지시 없음 — 카메라는 인물을 추적하고 인물은 환경을 응시
- wardrobe: CUT을 경계로 변신 (동일 인물의 다른 시대 의상)

**Composition** (prompt-derived)
- 단일 인물 + 단일 기차 앵커. 장면 전환은 "She reaches the carriage. CUT. The train doors open again." 같은
  명시적 CUT 문장으로 트리거됨 — "seamless time-transition" 지정

**Camera evidence** (prompt-derived)
- 움직임 3분할: (1) 주인공 추적, (2) 배경 슬로모션, (3) 카메라 자체 움직임이 따로 기술됨.
  관찰 가능한 기하가 아니라 프롬프트 지시지만, "누가 움직이는가"를 주체별로 분리 서술한 점이 핵심

**Lighting / Materials** (prompt-derived)
- 스타일 블록 + 네거티브로 톤 고정. 구체적 수치는 프롬프트에 없음

**Spatial blocking** (prompt-derived)
- 인물-기차 상대 위치 고정. 시간 전이가 일어나도 공간 관계는 유지

**Movable elements** (prompt-derived)
- 미세 디테일: 미소, 바람에 날리는 요소 — "살아있는" 질감의 근거

**관찰 vs 추론**
- 관찰(프롬프트): CUT이 변신 트리거로 쓰임. 움직임이 주체별로 분리 기술됨.
- 추론: 동일 인물 유지가 15초 패션 필름에서 가장 깨지기 쉬운 지점이라 앵커를 강하게 잡은 것으로 보임.
  → 프로덕션 스펙에 넣지 않음.

**Production description → Control Levels**
- Hard Lock: 동일 인물 identity, 기차라는 공간 앵커
- Soft Guidance: 시간 전이의 의상 방향 (시대별 무드 범위)
- Creative Freedom: 바람·미소 같은 마이크로 디테일

**기여 패턴**: 1 (앵커 락), 6 (변신은 CUT 1회로 절제)

```yaml
reference_state:
  source: "@codewithhajra / X — THE LAST TRAIN (15s)"
  evidence_basis: prompt-derived
  subject:
    gaze: not_directed # 프롬프트에 시선 지시 없음
    wardrobe: transforms_at_explicit_CUT
  camera:
    motion_split: [subject_tracking, background_slowmo, camera_move] # 주체별 분리 기술
  continuity:
    anchors: [same_identity, same_train]
    transition_trigger: "explicit CUT sentence"
  control_levels:
    hard_lock: [identity, location_anchor]
    soft_guidance: [era_wardrobe_direction]
    creative_freedom: [micro_details_wind_smile]
```

---

## 2. @Flkrstudio (Issei) — 메이지 시대 로닌 액션 (31초)

**기본 정보**
- 출처: X @Flkrstudio, PixVerse + Seedance 2.5, 중국어 프롬프트
- 길이: 31초 (액션물로는 김)
- 증거 기반: prompt-derived (중국어 프롬프트) + author-described

**Subject state** (prompt-derived)
- pose: 주인공 로닌 vs 포위하는 3인. 시선을 직접 지시하는 문장이 없음
- gaze: 인물 기준 상대 위치로 간접 해결 — A는 정면, B는 우측, C는 후방에 배치.
  "고개를 숙였다 들기" 같은 액션 비트가 시선 이동을 대신함

**Composition** (prompt-derived)
- 동시 포위 (줄서기 금지). 적이 한 명씩 돌아가며 덤비지 않고 동시에 압박

**Camera evidence** (prompt-derived)
- 액션물 특유의 추적·충격 컷. 물리: anticipation → contact → consequence 순서가
  프롬프트에 인과 사슬로 명문화됨

**Spatial blocking** (prompt-derived)
- 전부 주인공 기준 상대 좌표. 절대 방향(화면 좌/우)이 아니라 "주인공의 정면/우측/후방".
  이것이 시선 붕괴(대치하는데 같은 방향 보기)를 프롬프트 단에서 예방한 핵심 장치

**Movable elements** (prompt-derived)
- 의상·먼지 등 2차 모션은 타격 인과의 결과로 기술

**관찰 vs 추론**
- 관찰(프롬프트): 시선 직접 지시 없이 상대 위치 + 액션 비트로 해결. 막판 역전 금지(클리셰 차단).
- 추론: 다수 대 다수 액션에서 캐릭터 오염이 일어나기 쉬워 적의 행동을 "동시"로 묶은 듯.
  → 프로덕션 스펙에 넣지 않음.

**Production description → Control Levels**
- Hard Lock: 3인의 상대 위치 (정면/우측/후방), 동시 포위
- Soft Guidance: 각 타격의 구체적 안무
- Creative Freedom: 먼지·잔상 같은 임팩트 장식

**기여 패턴**: 2 (상대 좌표 — 시선 문제의 간접 해결), 4 (인과 사슬)

```yaml
reference_state:
  source: "@Flkrstudio (Issei) / X — Meiji ronin action (31s)"
  evidence_basis: prompt-derived
  subject:
    gaze: indirect_via_relative_position # 직접 지시 없음
    blocking: {A: front_of_hero, B: right_of_hero, C: behind_hero}
  action:
    chain: [anticipation, contact, consequence]
    rule: simultaneous_pressure_no_turn_taking
  control_levels:
    hard_lock: [relative_positions, simultaneity]
    soft_guidance: [choreography_details]
    creative_freedom: [impact_decor_dust]
```

---

## 3. @newtake_korea — "World Camera" 누아르 (14초)

**기본 정보**
- 출처: Threads @newtake_korea (World Camera 홍보 영상)
- 길이: 14초, 25컷
- 증거 기반: author-described (프롬프트 미공개)

**Subject state** (author-described)
- 단일 이미지 앵커에서 25컷을 뽑아낸 일관성 데모

**Composition** (author-described)
- 친밀한 클로즈업 → 광활한 와이드의 샷 설계. 컷 수 대비 인물 identity 유지가 주제

**Camera evidence** (author-described)
- World Camera(가상 카메라 이동) 특성상 카메라 기하가 가변. 관찰 가능한 것은
  "한 앵커에서 뽑아낸 컷들이 서로 같은 세계에 속해 보인다"는 점

**Lighting** (author-described)
- 전 컷 공통 컬러그레이드 — 시간·공간이 바뀌어도 톤이 묶여 있음

**관찰 vs 추론**
- 관찰: 프롬프트 없이도 앵커 이미지 + 공통 그레이드로 일관성 확보 가능.
- 추론: 25컷이면 컷당 0.5초 내외 — identity보다 "분위기 연속성"이 체감 품질을 결정했을 가능.
  → 프로덕션 스펙에 넣지 않음.

**Production description → Control Levels**
- Hard Lock: 앵커 이미지의 identity, 전 컷 공통 LUT
- Soft Guidance: 컷별 구도 (친밀→광활의 리듬)
- Creative Freedom: 컷 내 소품·배경 디테일

**기여 패턴**: 1 (단일 앵커 → 다컷 일관성)

```yaml
reference_state:
  source: "@newtake_korea / Threads — World Camera noir (14s, 25 cuts)"
  evidence_basis: author-described
  continuity:
    anchors: [single_image_anchor, shared_color_grade]
    shot_design: intimate_closeup_to_vast_wide
  control_levels:
    hard_lock: [anchor_identity, common_LUT]
    soft_guidance: [per_cut_framing_rhythm]
    creative_freedom: [in_cut_prop_details]
```

---

## 4. @fashablelab — 아테나 vs 아프로디테 (15초 원테이크)

**기본 정보**
- 출처: Threads @fashablelab, 영어 프롬프트 공개
- 길이: 15초, 원테이크(컷 없음)
- 증거 기반: prompt-derived (프롬프트 전문)

**Subject state** (prompt-derived)
- pose: 두 여신의 대치. 캐릭터별 모션 아이덴티티가 분리 기술됨
  (아테나: 절제된 전투 자세 / 아프로디테: 유려한 움직임 — prompt-derived)
- gaze: 대치 구도. 프롬프트에 "Exactly two goddesses" 인원 고정

**Composition** (prompt-derived)
- 원테이크이므로 구도 변화는 카메라 움직임으로만 해결

**Camera evidence** (prompt-derived)
- 불릿타임 1초 × 2회로 횟수 제한. 절제의 정량화 사례

**Lighting / Materials** (prompt-derived)
- 레퍼런스 분리: Image1은 "화풍만" 가져오고 "색감·조명·구도는 가져오지 마" —
  레퍼런스 이미지의 역할을 기능별로 자르는 패턴의 원형

**Spatial blocking** (prompt-derived)
- 두 인물의 대치 거리·자세가 프롬프트에 고정. 원테이크라 블로킹 변경 불가

**관찰 vs 추론**
- 관찰(프롬프트): 네거티브가 매우 구체적 — "창이 칼로 변형 금지" 같은 실패 기반 문장.
  엔딩은 긴장에서 정지 (해결하지 않고 멈춤).
- 추론: 원테이크는 컷으로 숨을 곳이 없어서 네거티브가 길어진 듯. → 스펙 제외.

**Production description → Control Levels**
- Hard Lock: 인원수 2, 각 캐릭터의 모션 아이덴티티, 무기 형태 고정
- Soft Guidance: 불릿타임 타이밍 (2회 중 언제 쓸지 범위)
- Creative Freedom: 배경 신전의 장식 디테일

**기여 패턴**: 1 (레퍼런스 기능 분리), 5 (구체적 네거티브), 6 (불릿타임 횟수 제한)

```yaml
reference_state:
  source: "@fashablelab / Threads — Athena vs Aphrodite one-take (15s)"
  evidence_basis: prompt-derived
  subject:
    headcount: exactly_two
    motion_identity_per_character: true
    gaze: confrontation_held # 대치 유지, 엔딩은 긴장에서 정지
  camera:
    bullet_time: 2x1s_capped
  references:
    image1_role: art_style_only # 색감·조명·구도는 가져오지 않음
  control_levels:
    hard_lock: [headcount, motion_identity, weapon_shape]
    soft_guidance: [bullet_time_timing]
    creative_freedom: [background_ornament]
```

---

## 5. @cheese__ai — 급식실 식판 개그 (20초)

**기본 정보**
- 출처: Threads @cheese__ai, 영어 프롬프트 공개, Facebook 380만 조회
- 길이: 20초
- 증거 기반: prompt-derived (프롬프트 전문) + 간접 지표 (380만 조회 = 대중성 검증)

**Subject state** (prompt-derived)
- pose: 급식실에서 식판을 든 학생들. 소품 연속성 락이 핵심 —
  "왼손 젓가락 never disappear / never fall / never switch hands"
- gaze: 개그 연기의 리액션 시선. 타임스탬프별 샷(11개)에 명시

**Composition** (prompt-derived)
- 11개 타임스탬프 샷으로 분할. 각 샷의 시작·종료 상태가 정의됨

**Camera evidence** (prompt-derived)
- PHYSICS LOCK: "수직 이동만" — 카메라·인물의 이동 축을 하나로 제한해
  물리 붕괴를 원천 차단

**Lighting / Materials** (prompt-derived)
- 캐릭터 시트 위 의상 오버라이드 (시트와 다른 의상을 명시적으로 덮어쓰기)

**Spatial blocking** (prompt-derived)
- 실패 기반 네거티브의 보고: "테이블 없는 의자", "서서 발 걸기" 등
  실제 실패 렌더에서 수집한 금지 목록

**Movable elements** (prompt-derived)
- 식판·젓가락·음식물의 연속성이 샷마다 체크됨

**관찰 vs 추론**
- 관찰(프롬프트): 대사 IPA 병기 — "밥 먹고 보자" [pap̚ mʌk̚.ko po.dʑa].
  립싱크를 음성학 기호로 고정한 사례.
- 관찰(간접 지표): 380만 조회 — 기법이 대중적으로 통했다는 증거.
- 추론: 개그는 타이밍 예술이라 샷을 11개로 잘게 쪼갠 듯. → 스펙 제외.

**Production description → Control Levels**
- Hard Lock: 소품 연속성 (젓가락의 손·위치), PHYSICS LOCK (수직 이동)
- Soft Guidance: 개그 타이밍의 강약
- Creative Freedom: 급식 메뉴·배경 학생들

**기여 패턴**: 5 (실패 기반 네거티브의 정점), 7 (IPA 립싱크 — Audio DNA의 극단형)

```yaml
reference_state:
  source: "@cheese__ai / Threads — cafeteria gag (20s, 3.8M views)"
  evidence_basis: prompt-derived
  subject:
    prop_continuity: chopsticks_left_hand_locked # never disappear/fall/switch
    dialogue: IPA_annotated # "[pap̚ mʌk̚.ko po.dʑa]"
  camera:
    physics_lock: vertical_movement_only
  shots: 11_timestamped
  negatives_source: collected_from_real_failed_renders
  control_levels:
    hard_lock: [prop_continuity, physics_lock]
    soft_guidance: [comic_timing_intensity]
    creative_freedom: [menu_items, background_students]
```

---

## 6. @aanggaamc — K-댄스 (30초)

**기본 정보**
- 출처: Threads @aanggaamc, Seedance 2.5 on Pollo.ai, 프롬프트 5개 공개
- 길이: 30초 (5개 프롬프트로 분할 생성 추정)
- 증거 기반: prompt-derived (프롬프트 5개)

**Subject state** (prompt-derived)
- 주인공 댄서 앵커 락: "댄서 바꿔치기 금지" — 30초 댄스에서 identity 유지가 최대 난제
- 2인 이상 군무. "같은 춤 vs 따로"의 할당은 프롬프트 분할(5개)로 해결한 것으로 보임

**Camera evidence** (prompt-derived)
- 카메라를 "6번째 댄서"로 취급 — 카메라 움직임이 안무의 일부
- 와이프 트랜지션 디바이스: 프롬프트 간 연결을 화면 전환 기법으로 매꿈
- 132 BPM 고정: 음악 템포를 프롬프트에 수치로 박음

**Spatial blocking** (prompt-derived)
- 대형(formation) 유지가 프롬프트마다 반복 확인됨

**관찰 vs 추론**
- 관찰(프롬프트): "NO STATIC END POSE" — 정지 포즈로 끝나지 않게 금지.
  30초를 5개 프롬프트로 나눈 구조.
- 추론: 단일 프롬프트로 30초 댄스의 일관성을 못 잡으니 분할 + 와이프 디바이스를 쓴 듯.
  → 스펙 제외.

**Production description → Control Levels**
- Hard Lock: 주인공 identity, 132 BPM
- Soft Guidance: 카메라=댄서로서의 움직임 범위
- Creative Freedom: 배경 조명 효과

**기여 패턴**: 1 (주인공 앵커), 6 (와이프 디바이스), 7 (BPM 수치 고정 — Audio DNA)

```yaml
reference_state:
  source: "@aanggaamc / Threads — K-dance (30s, Seedance 2.5)"
  evidence_basis: prompt-derived
  subject:
    lead_anchor: no_dancer_swap
    ending: NO_STATIC_END_POSE
  camera:
    role: sixth_dancer # 카메라가 안무의 일부
    transitions: wipe_devices_between_prompts
  audio:
    bpm_locked: 132
  structure: 5_prompts_for_30s
  control_levels:
    hard_lock: [lead_identity, bpm]
    soft_guidance: [camera_as_dancer_range]
    creative_freedom: [background_light_fx]
```

---

## 7. @apple_tea_richard — 옹박 오마주 (Seedance 2.5 + 블렌더 블로커트)

**기본 정보**
- 출처: Threads @apple_tea_richard
- 파이프라인: 블렌더 crude 프리뷰 → Seedance 최종 렌더
- 증거 기반: author-described (작업 과정 설명)

**Subject state** (author-described)
- 다수 적 설정 시 캐릭터 오염 발생 → 적 1명으로 축소. 인원수 자체가 변수

**Camera / Action** (author-described)
- 복잡한 액션은 프롬프트 문장으로 때우지 않고 블렌더에서 블로킹을 먼저 잡음.
  "크레딧 왕창 날리고 블렌더에 눈뜸", "보여주는 게 제일 빠르다"

**관찰 vs 추론**
- 관찰: 다수 캐릭터 액션에서 오염이 발생한다는 실패 보고. 블로커트가 해결책.
- 추론: 텍스트의 해상도로는 다체 액션의 동시성을 못 잡는다는 한계 선언으로 읽힘.
  → 스펙 제외 (단, 파이프라인 단계로는 채택 — 아래 "기여 패턴" 참조).

**Production description → Control Levels**
- Hard Lock: 블로커트에서 확정된 블로킹
- Soft Guidance: 타격의 디테일
- Creative Freedom: Seedance가 채우는 질감

**기여 패턴**: 8 (복잡한 액션은 보여주기 — Storyboard-first의 실전형)

```yaml
reference_state:
  source: "@apple_tea_richard / Threads — Ong-Bak homage"
  evidence_basis: author-described
  pipeline: [blender_crude_blockout, seedance_final]
  failure_report: multi_enemy_causes_character_contamination # → 적 1명으로 축소
  control_levels:
    hard_lock: [blockout_blocking]
    soft_guidance: [hit_details]
    creative_freedom: [rendered_texture]
```

---

## 8. @jeong_do_ryeong — 중력 프롬프트 엔지니어링 가이드 (텍스트)

**기본 정보**
- 출처: Threads @jeong_do_ryeong, 11시간 전 게시, 조회 942
- 형식: 영상 아님. 프롬프트 엔지니어링 가이드 스레드
- 증거 기반: text-guide (가이드 본문). 영상 관찰 없음 — 기법 제안으로만 취급

**핵심 주장** (text-guide)
- "중력 자체를 쓰지 말고, 중력이 남기는 자국(Traces)을 서술하라."
  근거: 모델은 물리 엔진을 돌리지 않고 다음 픽셀을 확률 예측하므로,
  "heavy gravity" 같은 추상어는 토큰 낭비

**제안 프레임워크** (text-guide)
- 5대 시각적 증거: Trajectory(궤적), Momentum(운동량·모션블러),
  Resistance(공기저항에 의한 머리·옷자락 들뜸), Impact(지면 변형·파편),
  Weight Transfer(하중 이동·무릎 흡수)
- GSTREC: G(중력 상태 10종 선언) - T(궤적) - R(저항 2차 모션) - E(환경 상호작용) - C(카메라)
- 중력 상태 전이 트리거 체인:
  SUPPORTED → JUMP → ASCENT → APEX(미세 정지) → DESCENT(가속) → IMPACT(흡수) → SUPPORTED
- 관계형 부정 → 긍정형 제어: "no floating" 대신 "firmly grounded, weight distributed naturally"

**Before/After 예시** (text-guide)
- Before: "A person jumps high in the air and lands on the rocky ground smoothly."
  → APEX·흡수 인과사슬 생략 → 고무공처럼 튐
- After: 4페이즈 분할. 상승 시 옷자락 아래로 / 하강 시 옷이 위로 부풀어 오름 (방향 반전)

**관찰 vs 추론**
- 가이드의 주장은 제안이지 검증된 프로덕션 결과가 아님. 이 항목 전체를 inference로 취급.
- 단, Before/After의 "옷자락 방향 반전" 같은 구체적 디테일은 자국 서술의 유효한 예시로
  Soft Guidance에 둘 수 있음.

**Production description → Control Levels**
- Hard Lock: (제안 단계이므로 없음 — 검증 후 승격)
- Soft Guidance: 자국 서술 원칙, 상태 전이 체인
- Creative Freedom: —

**기여 패턴**: 3 (자국 서술의 이론적 근거), 4 (상태 전이 체인)

```yaml
reference_state:
  source: "@jeong_do_ryeong / Threads — gravity prompt guide (text)"
  evidence_basis: text-guide # 영상 아님, 기법 제안
  core_claim: describe_traces_not_forces
  framework: GSTREC # Gravity state / Trajectory / Resistance / Environment / Camera
  state_chain: [SUPPORTED, JUMP, ASCENT, APEX, DESCENT, IMPACT, SUPPORTED]
  negative_style: positive_state_over_ban # "firmly grounded" > "no floating"
  control_levels:
    hard_lock: [] # 미검증 — 승격 보류
    soft_guidance: [trace_rule, state_chain]
    creative_freedom: []
```

---

## 9. OpenArt 공유 — "PUNCH BEER COMMERCIAL — ACT 4: SORA TAKES OVER" (15초)

**기본 정보**
- 출처: OpenArt suite share (작성자 표기 없음, 영상 파일은 CDN에서 삭제됨 — 404)
- 길이: 15초, 프롬프트 전문 공개 (605줄)
- 증거 기반: prompt-derived (프롬프트 전문). 영상 본체는 확인 불가 — 렌더 결과에 대한
  판단은 하지 않음

**Subject state** (prompt-derived)
- 2인: SORA(은발 단발, 랩 담당) / KARINA(흑발 롱헤어, 서포트)
- 립싱크 배타적 할당: SORA만 풀 립싱크, "KARINA MUST NEVER LIP-SYNC" / "NEVER mouths or silently copies the rap"
- KARINA 행동 규정: 술 마시기, 그루브, 리액션 — "얼어붙은 엑스트라가 되지 말 것"

**Composition** (prompt-derived)
- 11개 타임스탬프 샷 (00:00–00:01.40 RAP ENTRY … 00:13.55–00:15.00 FINAL RAP BUTTON).
  각 샷: 렌즈 → 블로킹 → 시선 → 액션/가사 → 카메라 → 자국 디테일 순서로 기술

**Camera evidence** (prompt-derived)
- CAMERA RHYTHM RULE: "Camera aggression must be intentional, not random."
  구간별 에너지 맵 (오프닝 미디엄 핸드헬드 → 파이널 최강).
  "Do NOT shake every frame equally. Rap cadence controls camera behavior."

**Lighting** (prompt-derived)
- MASTER LIGHTING HIERARCHY: 모든 광원은 로케이션 마스터 시트에서만.
  주광 2600–2900K 앰버 / 보조 4300–5200K 도시광 / 액센트 더스티 바이올렛.
  "DO NOT light either character independently from the room."

**Materials** (prompt-derived)
- WET CONTINUITY: "Wetness NEVER resets." 젖은 머리·의상의 상태가 샷 전체에 고정

**Spatial blocking** (prompt-derived)
- 로케이션 나침반 고정 (North=글래스 파사드 … East=소파 라운지).
  냉장고 위치를 동쪽 미디어월로 못 박음. "Never redesign, mirror, expand, compress, relocate or mutate"

**관찰 vs 추론**
- 관찰(프롬프트): 레퍼런스 4장의 역할 분리 (캐릭터 시트 2 + 제품 시트 1 + 로케이션 마스터 1).
  제품(PUNCH 캔)을 "병으로 바꾸지 마라"는 실패 기반 네거티브.
- 추론: 상업 광고급이라 네거티브가 40줄에 달함 — 클라이언트 작업의 방어적 프롬프팅으로 보임.
  → 스펙 제외.

**Production description → Control Levels**
- Hard Lock: 립싱크 배타 할당, 2인 고정, 로케이션 나침반, 조명 위계, 젖음 상태
- Soft Guidance: 샷별 카메라 에너지 (구간 맵 범위 내)
- Creative Freedom: 배경 서울 야경의 디테일

**기여 패턴**: 1, 2, 5, 6, 7 전부. 이 문서의 `prompt-template.md`의 구조적 원형.

```yaml
reference_state:
  source: "OpenArt share — PUNCH BEER COMMERCIAL ACT 4 (15s)"
  evidence_basis: prompt-derived # 영상 파일 삭제됨(404), 렌더 미확인
  subject:
    headcount: exactly_two
    lip_sync: {SORA: exclusive, KARINA: never}
    supporting_behavior: drink_groove_react # frozen extra 금지
  camera:
    rhythm_rule: beat_driven_intentional_aggression
    shots: 11_timestamped
  lighting:
    hierarchy_locked_to_master_sheet: true
    independent_character_lighting: banned
  continuity:
    location_compass_locked: true
    wetness: never_resets
  references:
    separated_authority: [character_x2, product, location_master]
  control_levels:
    hard_lock: [lip_sync_assignment, headcount, location_compass, lighting_hierarchy, wetness]
    soft_guidance: [per_shot_camera_energy]
    creative_freedom: [city_view_details]
```

---

## 10. @aiprompts_adda (anime threads) — Reika vs Vorn 슬리퍼 전투 (10초)

**기본 정보**
- 출처: Threads @aiprompts_adda, 프롬프트 전문 공개 (본문 + 작성자 댓글 13개).
  본문은 "Full Prompt On Profile Bio" 한 줄, 실제 프롬프트는 작성자 댓글 13개에
  조각나 있음. 댓글 14조각(본문 1 + 댓글 13)을 순서대로 합치면 완전한 10초 프롬프트
  1개가 됨 (2026-09-24 재확인).
- 각 작성자 댓글 아래 "Comment 1" 카운터가 있으나 로그인 월 뒤라 내용 미확인.
  14조각 프롬프트 자체가 완결되므로 관객 댓글이거나 추가 조각 — 불명. → 추론 제외.
- 작성자 고정 댓글: "Full Prompt" → Telegram 채널 t.me/AiPrompts Adda로 유도.
  실제 프롬프트 전문은 댓글에 그대로 있음.
- 길이: 10초, 16:9, 24fps, 원 컨티뉴어스 샷 (하드컷 없음)
- 게시 9시간, 조회 3.3K (2026-09-24 재확인)
- 증거 기반: prompt-derived (프롬프트 전문 + 비트 타임라인)

**Subject state** (prompt-derived)
- pose: REIKA MASTER (긴 흑발, 오버사이즈 흰 티, 다크 카고 쇼츠, 슬리퍼, 목걸이) — 첫 비트에서
  오른쪽 슬리퍼를 벗어 손에 들고 맨발로 전진. 10초 내내 "닿지 않음" 상태 유지
- gaze: 직접 지시 없음. 대신 타겟팅 규칙이 시선을 대신함 — "촉수는 항상 Reika의 실제
  신체 위치로 수렴" (TARGETED EXCLUSIONS)
- VORN MASTER: 뿔, 백발, 뼈 꼬리, 뼈 갑옷, 뼈 오라 촉수 3개로 연속 공격만 수행
- dialogue: 전편 대사 1개 — Reika의 "Baka" (일본어 バカ가 에너지 타이포그래피로 공기 중에
  차원적으로 형성, "화면 텍스트처럼 보이지 않음")

**Composition** (prompt-derived)
- 4비트 × 2.5초 타임라인:
  - [00:00–00:02.5] BEAT 1 EFFORTLESS EVASION — 회피, 0.2s 슬로모 1회
  - [00:02.5–00:05.0] BEAT 2 ESCALATING SPEED GAP — 잔해 연막으로 위치 이동, Vorn 옆에 착지
  - [00:05–00:07.5] BEAT 3 CRIMSON-SILVER FIRE — 에너지 축적, 0.2s 슬로모 1회
  - [00:07.5–00:10.0] BEAT 4 ONE-HIT FINISH — 슬리퍼 안면 타격, 충격파, Vorn 분해

**Camera evidence** (prompt-derived)
- 원테이크 연속 모멘텀: "카메라는 연속 모멘텀을 따르고 리셋·하드컷 없음"
- 비트별 카메라: 어깨 뒤 시작 → 궤도 회전 / 측면 추적 가속 → 휩 / 에너지 발현을 감싸는
  커브 → 접점 푸시 → 충격파와 함께 리코일
- 각 미스가 환경을 파괴하고 그 파괴가 카메라 전환을 정당화 ("each missed attack ...
  motivates the camera transitions") — 인과 기반 카메라 전환

**Lighting** (prompt-derived)
- 딥 시안-틸 섀도우 + 절제된 앰버-오렌지 하이라이트, 다크 노추널 콘트라스트.
  Reika의 시그니처 에너지: 다크 메탈릭 실버 + 블랙-크림슨 불꽃

**Materials** (prompt-derived)
- 젖은 반사 표면 (비에 젖은 아스팔트), 촉각적 재질, 자연스러운 모션블러, 필름 그레인

**Spatial blocking** (prompt-derived)
- Beat 2에서 잔해 연막을 이용한 위치 재배치: 카메라 시야가 막힌 틈에 God Speed 이동으로
  Vorn 옆에 나타남. 오컬루전(가림)을 공간 이동의 정당화로 쓴 사례
- 최종 타격점: 슬리퍼-안면 접점에서 충격파가 원점으로 확산 (인과 원점 고정)

**Movable elements** (prompt-derived)
- 빗물, 유리 파편, 차량 잔해, 아스팔트 파편, 군중. 각 미스가 환경을 점진적으로 파괴

**관찰 vs 추론**
- 관찰(프롬프트): 소품 락이 극도로 구체적 — "벗은 슬리퍼는 절대 발로 돌아가지 않음",
  "맨발은 끝까지 맨발". 슬로모는 0.2초 × 2회로 정량 상한. BGM 없음(환경음만).
- 관찰(프롬프트): 장비 명칭 선언 — ARRI ALEXA 65 / RED V-RAPTOR XL, 35mm anamorphic,
  Kodak Vision3 500T. 이는 관측된 사실이 아니라 작성자가 명시한 스타일 토큰.
  레포 규칙(보이지 않는 카메라 바디·렌즈 추측 금지)에 따르면, 선언된 경우는
  "style token"으로 취급하고 관측 장비로 오인하지 않아야 함. → 스펙에 넣을 때는
  "선언된 룩"으로 표기.
- 추론: "대사는 1개" — 멀티 캐릭터 대사 충돌을 원천 차단한 설계로 보임. → 스펙 제외.

**Production description → Control Levels**
- Hard Lock: 소품 상태 (슬리퍼 in hand / 맨발), 타겟팅 수렴 규칙, 원테이크 연속성,
  대사 1회 배타 (Reika만)
- Soft Guidance: 비트별 카메라 궤적 (구간 에너지 맵 범위 내), 파괴 디테일
- Creative Freedom: 잔해 파편의 구체적 형태, 군중 반응 디테일

**기여 패턴**: 1 (소품 락 — 지금까지 중 가장 구체적), 3 (미스의 자국: 파괴된 환경이
  공격의 증거), 4 (회피→축적→일격의 상태 전이), 5 (TARGETED EXCLUSIONS),
  6 (0.2s × 2회 슬로모 상한), 7 (BGM 없이 환경음만 — Audio DNA의 절제형)

```yaml
reference_state:
  source: "@aiprompts_adda / Threads — Reika vs Vorn flip-flop battle (10s)"
  evidence_basis: prompt-derived
  subject:
    gaze: indirect_via_convergence_rule # "촉수는 항상 실제 신체 위치로 수렴"
    prop_state: flipflop_in_hand_barefoot_locked # 절대 복귀 금지
    dialogue: single_line_exclusive # Reika "Baka" 1회만, 차원 타이포
    reika_never_touched_beats_1_2: true
  camera:
    one_continuous_shot: no_reset_no_hard_cut
    slow_mo_cap: 2x0.2s
    transition_logic: missed_attack_damage_motivates_camera_move
  audio:
    bgm: none
    design: environmental_only_with_compression_at_energy_manifest
  equipment_declared: ARRI_ALEXA_65_RED_VRAPTOR_XL_35mm_anamorphic_Kodak500T
    # declared style token, not observed hardware
  control_levels:
    hard_lock: [prop_state, convergence_rule, one_shot_continuity, single_dialogue]
    soft_guidance: [per_beat_camera_path, destruction_details]
    creative_freedom: [debris_shapes, crowd_reactions]
```

---

## 11. @seoa.superverse (세아) — Seedance 2.5 무언 감정연기 (싱글테이크)

**기본 정보**
- 출처: Threads @seoa.superverse, 프롬프트 전문이 작성자 댓글로 공개 (`<<<image_1>>>` 참조 이미지)
- 모델: Seedance 2.5, 게시 08/31/26, 조회 3.1K
- 증거 기반: prompt-derived (프롬프트 전문)
- 캡션: "울다가 웃다가 책상까지 쾅. 시댄스 2.5의 무언 연기 차력쇼."

**Subject state** (prompt-derived)
- pose: 나무 식탁에 앉은 여성. 대사 없이 5단계 감정을 빠른 리듬으로 통과
  1. (Fast) 억누른 쓰라림 — 시선 아래, 눈물 고임, 아랫입술 떨림, 턱 주름, 숨 가쁨
  2. (Fast) 눈물 — 눈물 흐름, 갑자기 고개 들기, 손등으로 눈 닦기
  3. (Fast) 폭소 — 눈물 속 히스테릭한 무성 웃음, 고개 흔들기
  4. (Climax) 책상 쾅 + 해소 — 손바닥으로 책상을 내리침, 의자에 기대어 팔짱, 짧은 한숨
  5. (Ending) 촛불 빛에서 마무리
- gaze: "감정은 오로지 표정과 eye contact으로만 전달". 구체적 시선 지시는
  Stage 1 "시선 아래"와 Stage 2 "갑자기 위를 봄"뿐. **시선의 대상(누구를 보는가)은
  프롬프트에 명시되지 않음** — 감정 연기의 눈맞춤이 카메라를 향하는지는 불명
- audio: 무음 대사. 호흡, 흐느낌, 코 훌쩍임, 무성 웃음, 책상 타격음, 의자 삐걱임,
  미세한 타닥거림만. BGM 없음, 대사 없음

**Composition** (prompt-derived)
- 단일 컨티뉴어스 롱테이크. 컷·트랜지션·카메라 변경 없음 — 처음부터 끝까지 같은 카메라

**Camera evidence** (prompt-derived)
- 카메라는 고정 위치지만 핸드헬드 질감: "vivid handheld tremors, slight shaking and
  vibrations, lens drifting almost imperceptibly left and right, breathing with the scene"
- 얼굴 클로즈업에 계속 포커스. 떨림 자체가 긴장을 만드는 장치
- 조명은 카메라 주변을 원을 그리며 이동 (invisible beam smoothly circling)

**Lighting** (prompt-derived)
- 프레임 안에 광원 없음 — "빛 자체와 얼굴에 떨어지는 방식만 보이고 광원은 전부 프레임 밖"
- 5단계 조명 안무:
  1. 정면 부드러운 균등광 (얼굴 전체)
  2. 우측광 — 오른쪽 절반만, 왼쪽은 그림자
  3. 백라이트 실루엣 — 얼굴은 어둡고 귀·광대·머리카락에 밝은 엣지
  4. 책상 타격 순간 강렬한 플래시 — 전신 과다노출, 그림자 소멸 (유일한 급격한 변화)
  5. 촛불광 — 따뜻하게 깜빡임, 눈동자에 빛점
- 조명 변화는 항상 부드럽게, 단계마다 강도가 층층이 증가

**Spatial blocking** (prompt-derived)
- 인물은 식탁 앞에 고정. 움직이는 것은 빛과 카메라의 미세 떨림뿐.
  감정의 고조를 "인물의 이동"이 아니라 "조명의 이동"으로 처리한 사례

**Movable elements** (prompt-derived)
- 눈물 (흐름), 머리카락 (백라이트 엣지), 손 (눈 닦기·책상 타격), 의자

**관찰 vs 추론**
- 관찰(프롬프트): 시선 대상 미지정. eye contact이 있다고만 하고 누구를 보는지는 안 씀.
  멀티 인물 영상에 이 프롬프트를 이식하면 시선 붕괴가 날 수 있는 지점.
  → gaze assignment table (후보 1)이 필요한 근거 사례.
- 관찰(관련 스레드): @re_cognizee_ai (08/25/26) — Seedance 2.0 vs 2.5 눈물 비교.
  2.0은 "눈물이 볼 한가운데서 툭 생김(출발점 없음)". 2.5는 순서가 있음:
  눈가에 고임 → 속눈썹에 걸림 → 무거워지면 떨어짐 → 지나간 자리에 젖은 흔적.
  "2.0은 눈물이 어떻게 보이는지를 알았고 2.5는 눈물이 어디서 오는지를 알아요."
  → 자국 서술(패턴 3)의 실제 렌더 증거. 눈물의 source-to-flow 인과.
- 추론: 5단계 감정을 "인물 이동 없이 조명 이동으로" 처리한 것은 싱글테이크의
  제약을 역이용한 설계로 보임. → 스펙 제외.

**Production description → Control Levels**
- Hard Lock: 싱글테이크 (노컷), 프레임 내 광원 없음, 5단계 감정 순서, BGM·대사 없음
- Soft Guidance: 조명 순환의 타이밍과 강도 곡선, 핸드헬드 떨림의 정도
- Creative Freedom: 배경 부엌 소품, 촛불 깜빡임의 디테일

**기여 패턴**: 2 (시선 대상 미지정의 위험 사례 — gaze table 필요), 3 (눈물
  source-to-flow가 자국 서술의 렌더 증거), 6 (감정 전환은 빠르게, 조명 변화는
  부드럽게 — 속도의 대비), 7 (SFX만, BGM 없음)

```yaml
reference_state:
  source: "@seoa.superverse / Threads — Seedance 2.5 silent acting (single take)"
  evidence_basis: prompt-derived
  subject:
    gaze: stages_defined_target_unspecified # Stage1 아래 / Stage2 위 — 대상 미지정 (위험)
    dialogue: none_silent
    emotion_stages: 5_fast_rhythm
  camera:
    single_continuous_take: no_cuts
    position: fixed_with_handheld_texture # 떨림이 긴장 장치
  lighting:
    no_visible_sources_in_frame: true
    choreography: circular_light_5_stages # 정면→우측→백라이트→플래시→촛불
    intensity_curve: layer_by_layer_increase
  audio:
    bgm: none
    dialogue: none
    sfx_only: [breathing, sobbing, sniffing, nervous_laugh, table_slam, chair_creak]
  control_levels:
    hard_lock: [single_take, no_visible_light_sources, emotion_order, no_bgm_no_dialogue]
    soft_guidance: [light_timing_curve, handheld_tremor_degree]
    creative_freedom: [kitchen_props, candle_flicker_detail]
```

---

## 12. @luffyndaaa (AI Threads) — 순간이동 히어로 액션 (15초)

**기본 정보**
- 출처: Threads @luffyndaaa, 프롬프트 전문이 고정 댓글로 공개
- 형식: 16:9, 15초, 약 7개 연결 신
- 생성 플랫폼: Syntx로 추정 (프로모 코드 LUF15, @syntx_global 태그). 모델명 미기재
- 증거 기반: prompt-derived (프롬프트 전문)

**Subject state** (prompt-derived)
- pose: Hero (Image 1 기준, identity 완전 보존 — "Do not redesign or alter").
  Scene 1에서 스마트폰 보며 걷다가 Scene 2에서 어리둥절하게 고개 듦 →
  Scene 3–5에서 순간이동 전투 → Scene 7에서 폰을 주머니에 넣고 걸어감
- gaze: "The Hero never poses for the camera. Characters never look directly into
  the camera unless naturally motivated by the action."
  → 카메라 응시 금지 원칙 명시. Scene 7 "looks back at the confused agents" —
  시선 대상이 명명됨 (confused agents). 시선 실패 방지의 긍정 사례
- dialogue: 영어 대사 4개 (ENEMY 1 + HERO 3). 자막은 인도네시아어 싱크

**Composition** (prompt-derived)
- 7개 신 연결: 평온(1) → 함정(2) → 첫 순간이동(3) → 근접전(4) → 혼전(5) → 군중 패닉(6) → 탈출(7)

**Camera evidence** (prompt-derived)
- CAMERA DNA 명명: "Extremely dynamic Hollywood action cinematography.
  The camera must feel like a real cinematographer physically reacting to the action,
  never like a video game camera."
- 기법: 핸드헬드, 휩팬, 급추적, 푸시인, 로우/하이앵글, 랙포커스, 모션블러,
  "realistic camera inertia and physical camera response to impacts"
- 신별 카메라: 뒤+옆 핸드헬드 관찰 → 순간이동 따라가는 급 휩팬 → 임팩트 리코일 →
  넓은 혼란 시점 → 파이널 와이드

**Lighting** (prompt-derived)
- 한낮 강한 자연광, 하드 섀도우, 유리·차량 반사, 물리적으로 믿을 만한 노출

**Materials** (prompt-derived)
- 현실 피부 질감, 의상 물리, 환경 상호작용. "Grounded supernatural effects"

**Spatial blocking** (prompt-derived)
- Scene 3: 잡히기 직전 몇 미터 뒤로 순간이동 → 요원이 빈 공기를 잡음 → Hero는 그 뒤에 나타남.
  "공격의 빗나감"을 공간 전이로 설계
- Scene 5: 차 보닛을 밟고 밀어내며 순간이동 — 환경(차)을 발판으로 쓰는 2차 상호작용
- Scene 6: 군중 패닉으로 전투를 "믿을 만한 공공 환경" 안에 배치

**관찰 vs 추론**
- 관찰(프롬프트): 카메라 DNA가 "느낌"으로 정의됨 (실제 촬영감독처럼 반응하는 카메라).
  "No artificial slow motion except extremely brief cinematic impact emphasis" —
  슬로모 상한을 절제 원칙으로 명문화.
- 관찰(프롬프트): 시선 규칙이 "카메라 응시 금지 + 대상 명명"의 이중 구조.
  gaze assignment table (후보 1)의 실전형.
- 추론: 15초에 7개 신은 신당 2초 내외 — 각 신이 한 비트씩만 담당하는 극단적 분할로 보임.
  → 스펙 제외.

**Production description → Control Levels**
- Hard Lock: Hero identity 완전 보존, 카메라 응시 금지, 순간이동 자국 세트
  (공간 왜곡 + 공기 변위 + 미세 파티클 + 날카로운 효과음)
- Soft Guidance: 신별 카메라 기법 (DNA 범위 내), 전투 안무
- Creative Freedom: 군중 반응 디테일, 거리 소품

**기여 패턴**: 1 (identity 보존 선언), 2 (시선 대상 명명 — "confused agents"),
  3 (순간이동의 자국: 공간 왜곡·공기 변위·파티클 — 힘 대신 증거), 6 (인위적 슬로모 금지),
  7 (대사+자막 싱크, 효과음 설계)

```yaml
reference_state:
  source: "@luffyndaaa / Threads — teleportation hero action (15s, 7 scenes)"
  evidence_basis: prompt-derived
  subject:
    gaze: camera_look_banned_unless_motivated # Scene 7은 "confused agents" 명명
    dialogue: 4_lines_EN_with_ID_subtitles
    identity: fully_preserved_from_image1
  camera:
    dna: real_cinematographer_reacting # never like a video game camera
    techniques: [handheld, whip_pan, push_in, rack_focus, impact_recoil]
    slow_mo: banned_except_brief_impact_emphasis
  power_traces: [spatial_warp, air_displacement, particle_displacement, sharp_sfx]
  structure: 7_scenes_15s # 신당 약 2초
  control_levels:
    hard_lock: [identity, camera_look_ban, power_trace_set]
    soft_guidance: [per_scene_camera, choreography]
    creative_freedom: [crowd_reactions, street_props]
```

---

## 13. @aanggaamc (AI Threads) — 30초 2씬 누아르 에디토리얼

**기본 정보**
- 출처: Threads @aanggaamc (K-댄스 영상과 동일 작성자), 프롬프트 전문이 작성자 댓글로 공개
- 생성: Wavespeed AI, 30초 × 2씬
- 게시 1일 전, 조회 777
- 증거 기반: prompt-derived (프롬프트 전문)
- 캡션: "Terlalu tampan ~" (너무 잘생겼어~)

**두 편의 구조** (prompt-derived)
- Sc 1 "SILENT AUTHORITY / NOIR EDITORIAL": 턱시도 남성의 권위적 서사.
  무도회장 문 열기 → 군중 속 제스처 → 연회장 테이블 도약 → 크리스털 잔 받기 →
  흙 (무덤 암시) → 빗속 계단 → 빈티지 세단에서 봉투 → 서재에서 편지 →
  사진 접어 넣기 → 문 앞에서 마지막 돌아봄
- Sc 2 "BETWEEN US": 파트너의 부재에 대한 조용한 실망. 10개 로케이션.
  호텔 무도회장(미사용 초대장) → 루프탑(빈 자리) → 꽃시장(두 송이 중 하나 반납) →
  철도 플랫폼(놓친 도착) → 대계단(중단된 메시지) → 빈 극장(옆자리 꽃) →
  해안 테라스(날아가는 사진) → 당구장(두 공이 반대 방향) → 빗속 주차장(빈 조수석에
  우산을 향함) → 아파트(빈 고리)

**Subject state** (prompt-derived)
- pose: identity @image1 고정. 턱시도·새틴 피크 라펠·나비넥타이 전편 동일
- gaze: 시선이 서사의 핵심 장치. Sc 1 — "eyes scanning the room"(방 스캔),
  "already looking toward the courtyard"(이미 안뜰을 봄). Sc 2 — "eyes dropping"
  (눈이 떨어짐), "eyes follow only one ball"(한 공만 따라감), "unfinished glance
  toward the empty room"(빈 방을 향한 미완의 시선).
  **파트너는 전편 오프스크린** — 부재하는 인물을 시선과 빈 공간으로 표현
- dialogue: 없음. 오디오: "No SFX. No added foley... All editorial accents and
  lens flares remain purely visual." — 완전 무음. 감정은 시각만으로

**Camera evidence** (prompt-derived)
- 신마다 초점거리 지정: 28mm 후퇴, 50mm 측면 트랙, 24mm 바닥 트랙, 100mm 매크로,
  85mm 인물, 135mm 압축, 40mm, 32mm 크레인, 75mm.
  → 선언된 스타일 토큰. 관측된 광학이 아니므로 스펙에는 "선언된 렌즈 언어"로 표기
- LENS LANGUAGE: 광원은 샹들리에·낮은 태양·차 헤드라이트에서 유래한 motivated flare.
  anamorphic streak, veiling flare, halation. "preserve facial visibility"
- CAMERA CHOREOGRAPHY: 로케이션당 하나의 주 카메라 움직임. "No repeated full orbits"

**Editing evidence** (prompt-derived)
- EDITORIAL RULES: "Each cut follows a completed physical gesture." —
  컷은 물리적 제스처가 완료된 뒤에만. 제스처 매치, 전경 와이프, 매치컷
- 매치컷 체인: 여는 손가락 → 같은 손에서 떨어지는 흙 / 주머니 제스처 → 빈 의자를
  향한 손 / 꽃 포장 → 같은 손의 접힌 티켓 / 우산 손잡이 → 아파트의 빈 고리
- 모노크롬 전환은 감정 제스처에 종속: "the complete image becomes monochrome on the
  moment the second flower touches the counter", "Color gradually drains into
  black-and-white". **격리된 컬러 오브젝트 금지** ("No isolated colored objects")

**Lighting** (prompt-derived)
- muted amber ↔ rich black-and-white 에디토리얼 교대. 딥 블랙이지만 디테일 유지

**관찰 vs 추론**
- 관찰(프롬프트): 시선으로 부재를 표현 — 파트너를 보여주지 않고 "빈 곳을 보는 눈"으로
  관계 서사를 전달. gaze assignment table에서 "오프스크린 대상" 항목의 근거 사례.
- 관찰(프롬프트): 오디오 완전 제거. 30초 감정 서사를 무음으로 — Audio DNA의
  "침묵도 설계" 사례.
- 관찰(프롬프트): K-댄스 영상의 와이프 디바이스와 같은 작성자 — 이 작성자의
  일관된 기법은 "프롬프트 분할 + 화면 전환 디바이스로 연결".
- 추론: 3초 × 10세그먼트 구조는 각 세그먼트가 독립 렌더 후 조립된 것으로 보임.
  → 스펙 제외.

**Production description → Control Levels**
- Hard Lock: identity, 턱시도 연속성, "컷은 제스처 완료 후" 규칙, 완전 무음,
  격리 컬러 오브젝트 금지
- Soft Guidance: 모노크롬 전환 타이밍 (감정 제스처 종속), 매크로 인서트 선택
- Creative Freedom: 로케이션 디테일, 전경 레이어

**기여 패턴**: 2 (오프스크린 대상 시선 — 시선으로 부재 표현), 4 (제스처 완료 →
  컷의 인과 사슬), 5 (No isolated colored objects 같은 구체적 금지),
  6 (로케이션당 카메라 움직임 1개), 7 (완전 무음 — 침묵의 설계), 8 (작성자 일관 기법:
  분할 렌더 + 전환 디바이스)

```yaml
reference_state:
  source: "@aanggaamc / Threads — 30s x2 noir editorial (Wavespeed AI)"
  evidence_basis: prompt-derived
  subject:
    gaze: offscreen_absence_as_story # 파트너 오프스크린, 빈 공간을 보는 시선
    gaze_beats: [scanning_room, eyes_dropping, follows_one_ball, unfinished_glance]
    wardrobe: tuxedo_continuous
    dialogue: none
  camera:
    declared_lens_language: [28mm, 50mm, 24mm, 100mm_macro, 85mm, 135mm] # style tokens
    flare: motivated_only_visible_or_plausible_source
    choreography: one_primary_move_per_location
  editing:
    cut_rule: only_after_completed_gesture
    match_cut_chains: [fingers_to_soil, pocket_to_chair, flower_to_ticket, umbrella_to_hook]
    monochrome: triggered_by_emotional_gesture # no isolated colored objects
  audio:
    everything: none # 무음. 모든 악센트는 시각
  control_levels:
    hard_lock: [identity, wardrobe, cut_after_gesture, total_silence, no_isolated_color]
    soft_guidance: [monochrome_timing, macro_insert_choice]
    creative_freedom: [location_details, foreground_layers]
```

---

## 14. @aanggaamc (AI Threads) — AGILE WATER DANCE (30초)

**기본 정보**
- 출처: Threads @aanggaamc (K-댄스, 누아르 에디토리얼과 동일 작성자)
- 생성: 모델명 미기재. 레퍼런스 3종 분리: @image1(identity) / @image2(wardrobe) / @video1(리듬 마스터)
- 게시 2일 전, 조회 1.3K
- 증거 기반: prompt-derived (프롬프트 전문)
- 캡션: "Tag orangnya 🫵 ... Prompt bisa tanpa video taging cek stabilo kuning."

**글자와 인물의 조화 — 핵심 발견**
- 프롬프트에 **글자·타이포그래피에 대한 서술이 전혀 없음**. 네가 보라고 한 "글자 움직임"은
  프롬프트에서 설명되지 않는다.
- 네 개의 동기화 레이어로 명시된 것은: (1) 인물 움직임, (2) 물 궤적, (3) RGB 조명,
  (4) 카메라 모션. 텍스트는 레이어에 없음.
- 반면 영상 커버 프레임에는 댄서 뒤에 큰 블록 레터 "TEM..."이 보임 (browser task 관찰).
  → **프롬프트에 없는 요소가 렌더에 등장한 사례**. 출처는 불명 (@image1의 배경일 수도,
  @video1의 잔재일 수도, 모델의 창발일 수도 있음). 추론이므로 스펙에 넣지 않음.
- 교훈: 레퍼런스 분리(@image1/2, @video1)를 해도, 레퍼런스 안의 원치 않는 요소가
  새어 들어올 수 있다. 레퍼런스의 "역할"뿐 아니라 "배제 요소"도 명시해야 하는 근거.
  → 실패 기반 네거티브(패턴 5)의 확장: "레퍼런스에서 가져오지 말 것" 목록.

**MASTER BEAT SYSTEM** (prompt-derived)
- "@video1을 절대적인 리듬·템포·악센트·움직임·조명 동기화 소스로 사용.
  모든 빠른 스텝, 바운스, 손목 플릭, 물 분출, 카메라 반응, RGB 조명 변화는
  @video1의 실제 리듬에서 자연스럽게 파생되어야 함."
- 레퍼런스 영상이 오디오를 대신해 프레임 단위 권위가 된 사례. Audio DNA의 확장형 —
  "리듬 마스터"라는 새 후보 규칙

**Subject state** (prompt-derived)
- pose: 5초 × 6세그먼트의 고밀도 안무. "No standing and posing between moves",
  "The body never freezes between gestures", "Finish still dancing, not frozen in
  a hero pose" — 정지 금지의 삼중 명시
- 손에 양손 멀티젯 물 분사기. 물줄기가 "춤의 능동적 확장"으로 정의됨
- gaze: 명시적 시선 지시 없음. "playful head turn, natural smile" — 표정은 있으나
  대상은 없음

**Camera evidence** (prompt-derived)
- "Camera acceleration follows @video1's rhythmic accents, but the performer always
  remains readable." — 카메라 가속은 리듬을 따르되 가독성은 유지 (제약 조건)
- 프레이밍 규칙: "Large water movements receive wider framing; smaller hand/face
  moments receive medium-full framing." — 움직임의 크기에 따른 프레이밍 할당

**Spatial blocking** (prompt-derived)
- "Keep the protagonist inside a tight dance radius throughout. No walking toward
  the camera." — 댄스 반경 락. 카메라가 다가가는 것이 아니라 인물이 반경 안에 머묾

**관찰 vs 추론**
- 관찰(프롬프트): 네 레이어 동기화 + 리듬 마스터. 정지 금지 3회 반복.
- 관찰(커버 프레임): 프롬프트에 없는 대형 텍스트 "TEM...".
- 추론: 텍스트의 출처는 불명. 레퍼런스 오염 가능성을 시사하지만 단정 불가.
  → 스펙 제외. 단, "레퍼런스 배제 목록"은 네거티브 후보로 기록.

**Production description → Control Levels**
- Hard Lock: identity(@image1), wardrobe(@image2), 리듬 마스터(@video1),
  타이트 댄스 반경, 정지 금지
- Soft Guidance: 6세그먼트의 안무 디테일, 물 궤적의 기하학
- Creative Freedom: 물방울 디테일, 미스트

**기여 패턴**: 1 (레퍼런스 3종 기능 분리 — 가장 정교한 형태), 6 (정지 금지 =
  움직임 버짓의 하한), 7 (리듬 마스터 — Audio DNA 확장 후보), 5 (레퍼런스 배제
  목록 — 네거티브 확장 후보)

```yaml
reference_state:
  source: "@aanggaamc / Threads — AGILE WATER DANCE (30s)"
  evidence_basis: prompt-derived
  typography_finding:
    in_prompt: none # 글자 서술 없음
    in_frame: large_block_letters_TEM_behind_dancer # 커버 프레임 관찰
    verdict: unprompted_element_source_unknown # 추론 — 스펙 제외
  beat_authority:
    master: "@video1" # 절대 리듬·템포·조명 동기화 소스
    synced_layers: [performer_movement, water_trajectories, rgb_lighting, camera_motion]
  subject:
    gaze: unspecified
    freeze_ban: triple_stated # never freezes / no posing / finish dancing
    prop: dual_handheld_water_sprayers_as_dance_extension
  camera:
    acceleration: follows_rhythm_accents_but_performer_readable
    framing_rule: wide_for_large_water_moves_medium_full_for_hand_face
  blocking:
    dance_radius: tight_locked # no walking toward camera
  control_levels:
    hard_lock: [identity, wardrobe, beat_master, dance_radius, freeze_ban]
    soft_guidance: [choreography_details, water_geometry]
    creative_freedom: [droplet_details, mist]
```

---

## 15. @chase90re (CHAse) — 장미정원 로맨틱 액션 (30초)

**기본 정보**
- 출처: Threads @chase90re (인증 계정), 프롬프트 전문이 본문에 공개 (한국어)
- 생성: @zcre.co.kr, 30초 연속 단일 씬, 16:9, 24fps
- 게시 4일 전 (2026-09-19), 조회 719
- 증거 기반: prompt-derived (프롬프트 전문)
- 캡션: "누군가 프롬프트를 원하여 공유"

**스토리 (5막)** (prompt-derived)
- 제1막 [0–8.5s] 알콩달콩 달리기 → chase가 자갈에 헛디뎌 철퍼덕 → 남성이 웃음 폭발 →
  chase 각성, 파스텔 핑크 에너지로 공중부양
- 제2막 [8.5–16.5s] 공중 플라즈마 맹공 vs 시안 헥사 쉴드 고속 체술
- 제3막 [16.5–24.5s] 에너지 탄 크레이터 폭발 → 클린치, 마운트 잡고 주먹 치켜듦
- 제4막 [24.5–27.5s] **정확히 25.0초** 남성이 볼에 기습 뽀뽀 + "사랑해" 속삭임
- 제5막 [27.5–30s] 포옹, 토스카나 노을 피날레

**Subject state** (prompt-derived)
- pose: 여성 주인공 "chase"(@Image2: 긴 흑발, 브라운 오프숄더 니트, 플리츠 미니스커트,
  가죽 롱부츠) / 남성(@Image3: 네이비 워크재킷, 데님, 스니커즈). 임의 환복 금지
- gaze: 제4막 "눈을 맞추며 진심 어린 목소리로 속삭인다" — **상호 시선 명시**.
  제1막 "카메라를 향해 웃으며" — 초반에는 카메라 응시 허용 (자연스러운 상황)
- dialogue: 한국어 4개, 시간·감정·발화 자세까지 지정:
  - 3.5–5.0s chase: 얼굴을 흙에 파묻은 채 웅얼거리며 작고 낮게 {재밌냐..?}
  - 5.0–6.5s 남성: 웃음을 삼키며 능청스럽게 {어? 뭐라고?}
  - 7.0–8.5s chase: 부양하며 서늘하게 {재밌냐고...}
  - 25.0–26.5s 남성: 볼 뽀뽀 후 눈을 맞추며 {사랑해}

**Camera evidence** (prompt-derived)
- 35mm 미디엄 트래킹 → 지면 밀착 로우앵글 → 35mm 푸시인 → 초저각 + 1200°/s 휩팬 →
  35mm 측면 트래킹 → 24mm 다이내믹 와이드 → 지면 밀착 핸드헬드 →
  초밀착 핸드헬드 + 랙포커스 → 24mm 스테디 와이드 풀아웃(0.5m/s)
- 선언된 렌즈 언어 (관측 아님)

**Lighting** (prompt-derived)
- 황금빛 노을 역광 + 앰버톤. 액션 시 파스텔 핑크 플라즈마 ↔ 시안 림라이트 교차.
  25.0초 이후 모든 파티클이 벚꽃빛 온기 톤으로 점진 전환

**Action / Physics** (prompt-derived)
- 슬랩스틱: "실제 중력과 관성에 의한 현실적 넘어짐 및 모래먼지 마찰"
- 타격 제한: "1초당 주요 타격 3개 제한" — 모션 버짓의 정량화
- 임팩트 등급: 1~3급 임팩트 프레임, 충격파 링
- 무술 디테일: 골반 회전(转髋), 공중 낙법, 메다치기
- 무혈 원칙(ZeroBlood): 에너지 충격파 + 꽃잎 비산으로 위력 표현

**Spatial blocking** (prompt-derived)
- **피해 영구 보존**: "자갈길의 미끄러진 흔적, 크레이터, 흩어진 장미 꽃잎은 마지막
  포옹 장면까지 배경에 영구 유지" — 환경 피해의 연속성 락
- 공간 상속 규칙: 배경 참조는 "공간 구조와 자연광만 상속하며 빈 공간 상태 유지"

**Audio** (prompt-derived)
- BGM 3단 전환: 어쿠스틱 기타(0–7.5s) → 정적(7.5s) → 서브 베이스 드롭(8.5s~) →
  피아노·스트링(25.0s~)
- 폴리: 발소리, 마찰음, 억눌린 웃음, 에너지 충전음, 스파크음, 뽀뽀 입맞춤 소리

**관찰 vs 추론**
- 관찰(프롬프트): 25.0초라는 전환 시점이 소수점 단위로 고정. 감정선 전환의
  트리거가 시간 코드.
- 관찰(프롬프트): 한국어 프롬프트 최초 사례. 대사의 감정·자세·음량까지 지정.
- 관찰(프롬프트): "화면 상 텍스트, 자막, 워터마크, UI, 타임코드 일체 생성 금지" —
  14번의 무단 글자 등장(TEM...)에 대한 방어적 네거티브로 읽힘.
- 추론: 5막 구조는 각 막이 다른 장르(로코→SF→로맨스)라 톤 전환이 핵심 난제였을 듯.
  → 스펙 제외.

**Production description → Control Levels**
- Hard Lock: identity 2인, 의상 고정, 25.0s 전환 시점, 피해 영구 보존,
  화면 텍스트 일체 금지, ZeroBlood
- Soft Guidance: 막별 카메라 (선언된 렌즈 범위), BGM 전환 타이밍
- Creative Freedom: 꽃잎 비산 디테일, 노을 구름

**기여 패턴**: 2 (상호 시선 명시 — "눈을 맞추며"), 3 (넘어짐의 자국: 흙먼지·미끄러진
  흔적), 4 (넘어짐→각성→맹공→뽀뽀→포옹의 상태 전이), 5 (화면 텍스트 금지 —
  14번의 교훈이 반영된 네거티브), 6 (1초당 타격 3개 제한), 7 (BGM 3단 전환 +
  대사 4개의 시간·감정 지정)

```yaml
reference_state:
  source: "@chase90re / Threads — rose garden romantic action (30s, Korean prompt)"
  evidence_basis: prompt-derived
  subject:
    gaze: mutual_at_25s_kiss # "눈을 맞추며" — 상호 시선 명시
    gaze_opening: toward_camera_while_running # 자연스러운 상황의 카메라 응시
    dialogue: 4_lines_Korean_with_time_emotion_posture
    wardrobe_locked: true
  camera:
    declared_lenses: [35mm, 24mm] # style tokens
    techniques: [tracking, low_angle, whip_pan_1200dps, rack_focus, pullout_0.5mps]
  action:
    hits_per_second_cap: 3
    impact_grades: [1, 2, 3]
    zero_blood: true
  continuity:
    damage_persists_to_end: [skid_marks, crater, scattered_petals]
    transition_trigger: "25.0s"
  audio:
    bgm_3stage: [acoustic_guitar, sub_bass_drop, piano_strings]
    sfx: [footsteps, friction, suppressed_laugh, energy_charge, kiss]
  negatives: [no_text_subtitles_watermark_UI, no_2D_effects, no_blood]
  control_levels:
    hard_lock: [identity_x2, wardrobe, transition_25s, damage_persistence, no_text, zeroblood]
    soft_guidance: [per_act_camera, bgm_timing]
    creative_freedom: [petal_details, sunset_clouds]
```

---

## 16. @chase90re (CHAse) — 얼굴 없는 캐릭터 시트 (이미지 레퍼런스 기법)

**기본 정보**
- 출처: Threads @chase90re (인증 계정), 21.1K 조회, 240 좋아요 — 현재까지 최고 반응
- 게시 5일 전 (2026-09-19)
- 형식: **영상이 아님**. GPT Image 2 Flare로 만든 캐릭터 시트 이미지 4패널
- 증거 기반: prompt-derived (프롬프트 전문) + author-described (댓글 Q&A)

**핵심 주장** (author-described)
- "얼굴 없는 캐릭터 시트를 만드는 이유: 4K로 만들어도 전신샷을 만들 경우
  얼굴 참조가 뭉게지기 때문"
- 해법: 얼굴과 몸을 분리. 전신 3뷰(정면/측면/후면)는 **머리 없이**,
  얼굴은 별도 클로즈업 패널로

**프롬프트** (prompt-derived)
- "character design sheet four panels side by side on pure light gray background,
  no text, no watermark, highly detailed realistic fabric and leather texture,
  photorealistic skin, cinematic studio lighting, 8k, clean composition"
- left: full body front view, headless / second: side view, headless /
  third: back view, headless / right: face close-up portrait only
- [얼굴참조] @Image1의 얼굴과 헤어스타일을 100% 승계, 임의 변경 금지,
  프롬프트에 없는 내용 절대 추가 금지
- [의상] @Image2의 의상을 100% 승계, **단 악세사리·오브젝트·배경은 승계하지 않는다**
- [신체사이즈] 템플릿 자리 (사용자가 채우는 변수)

**댓글 Q&A** (author-described)
- Q: 패널 사이 구분선이 있는 게 나을까? → A: 인물 참조라 라인은 무관.
  거슬리면 "인물의 얼굴과 의상만을 참조하며 그 외 모든 것을 승계하지 않는다" 추가
- Q: 헤어 디테일을 AI가 못 알아들으면? → A: 바이트댄스 공식 가이드대로
  참조 이미지가 있어도 헤어스타일·의상·악세사리는 텍스트로 간소하게 병기 권장
- Q: 뒷통수는? (mylady_haneulbit) → 답글 4개 (내용 미확인)

**관찰 vs 추론**
- 관찰: 참조 역할 분리의 이미지 버전. 얼굴↔몸, 의상↔악세사리·배경을 자름.
  "승계하지 않는다"는 배제 목록이 명시적.
- 관찰: 참조 이미지가 있어도 텍스트 병기를 권장 — 이미지+텍스트 이중 앵커.
- 추론: 21.1K 조회는 이 기법이 실전痛点(전신샷 얼굴 뭉개짐)을 정확히 찔렀기 때문으로 보임.
  → 스펙 제외.

**Production description → Control Levels**
- Hard Lock: 얼굴 100% 승계, 의상 100% 승계, 전신뷰는 무두(無頭)
- Soft Guidance: 신체사이즈 템플릿 변수
- Creative Freedom: —

**기여 패턴**: 1 (참조 역할 분리의 원형 — 얼굴/몸/의상/배경 4분할),
  5 (배제 목록 명시: "악세사리·오브젝트·배경은 승계하지 않는다")

```yaml
reference_state:
  source: "@chase90re / Threads — faceless character sheet (GPT Image 2 Flare)"
  evidence_basis: prompt-derived + author-described
  format: image_not_video # 영상 아님 — 캐릭터 시트 기법
  problem: face_reference_blurs_in_fullbody_even_4K
  solution:
    panels: [front_headless, side_headless, back_headless, face_closeup_only]
    face: "@Image1 100%"
    outfit: "@Image2 100%"
    excluded: [accessories, objects, background] # 명시적 배제 목록
  rule: text_annotation_alongside_reference # 참조 있어도 텍스트 병기
  control_levels:
    hard_lock: [face_100, outfit_100, headless_body_views]
    soft_guidance: [body_size_template]
    creative_freedom: []
```

---

## 17. @bmx_ai13 (BMX) — "A 2026 Vlog from Troy" (30초)

**기본 정보**
- 출처: X @bmx_ai13 (인증 계정, bio: SocialSight)
- 생성: Seedance 2.5 on @dreamina_ai (작성자가 "Seednace 2.5"로 표기 — 오타로 보임)
- 30초, 프롬프트 전문 공개 (영어)
- 게시 2026-09-24 01:02, 조회 1,135, #DreaminaCPP 태그
- 증거 기반: prompt-derived (프롬프트 전문)

**컨셉** (prompt-derived)
- 2026년 Gen Z 여행자(일본인 여성, 25세)가 트로이 전쟁 한복판에서 휴대폰으로
  찍는 핸드헬드 브이로그. "목격자가 될 수 있는 것만" 원칙

**Subject state** (prompt-derived)
- CHARACTER LOCK — VLOGGER: 25세 일본인 여성, 곧은 흑발 로우포니테일, 작은 실버
  스터드 귀걸이, 챠콜 후드티, 루즈 카고 팬츠, 캔버스 백팩. **전 샷 내내 휴대폰을 듦**
- "Same face, hair, voice, and clothing in every shot" — 얼굴·헤어·목소리·의상 4종
  캐릭터 락. 목소리까지 앵커에 포함된 점이 특이
- 감정선: curious → shaken → sincere (호기심→충격→진심)
- gaze: 셀피 모드라 카메라(자신의 폰)를 봄 — 브이로그 컨벤션이라 시선 금지가 없음
- dialogue: 영어 5개, 일본어 억양. 립싱크 정밀 지정: "Dialogue must be clearly
  audible and precisely lip-synchronized"

**Composition** (prompt-derived)
- 5비트 × 6초:
  - [00:00–00:05] THE ARRIVAL — 빛 글리치로 도착, 셀피: "Okay… I was in 2026
    five seconds ago." 성벽 뒤로 트로이, 연기가 밝은 하늘로
  - [00:05–00:11] OUTSIDE THE WALLS — 돌 뒤에 숨어 와이드: 청동 갑옷 병사들,
    근처에 화살 박힘. "That's Troy. This is the war."
  - [00:11–00:17] INSIDE THE GATE — 문을 통한 민간인들: 문 잡는 손, 도공, 아이를
    카트에 올리는 부모. 폰이 리포커싱에 고생. "Everyone talks about the heroes…"
    → (조용히) "…but people live here."
  - [00:17–00:24] THE WALL — 성벽 위에서 전장 와이드. 폰을 내리자 화면이
    먼지 쌓인 신발에 머뭄. "I thought I wanted to see history. I don't think I
    understood what that meant."
  - [00:24–00:30] THE RETURN — 도시 레인: 빨랫감, 지붕 너머 연기, 물동이 나르는
    사람들. 빛이 깜빡이며 복귀. "I'm going home. I'll remember them." → 빛으로
    깨지며 CUT TO BLACK

**Camera evidence** (prompt-derived)
- 핸드헬드 폰 푸티지 + 오토포커스 헌팅(초점 사냥) + 렌즈 먼지 + 자연 노출 변화
- "excessive camera shake"는 금지 — 흔들림의 상한 명시
- Keep combat mostly distant — 전투는 원경으로 (목격 가능성 규칙)

**Audio** (prompt-derived)
- Diegetic audio only; no music. 바람, 돌 위 샌들, 카트, 뿔나팔, 함성, 화살, 호흡
- "Dialogue must be clearly audible and precisely lip-synchronized" — 립싱크 정밀

**관찰 vs 추론**
- 관찰(프롬프트): AVOID 목록이 시대고증 필터 — "브이로거의 의상·백팩·폰 외의
  현대 물건 금지, 중세 갑옷·성 금지, 마법 생물 금지, 맥락 없는 유명 영웅 금지,
  과장된 억양 금지, 코믹 반응 금지, 전투의 승리적 묘사 금지"
- 관찰(프롬프트): 시점 제한 — "목격자가 될 수 있는 것만"에 초점. 전투는 원경.
- 추론: 5비트 × 6초 균등 분할은 Seedance 2.5의 샷 계획과 맞아떨어지는 듯.
  → 스펙 제외.

**Production description → Control Levels**
- Hard Lock: 캐릭터 4종(얼굴·헤어·목소리·의상), 전 샷 폰 소지, 시대고증 네거티브,
  LAST FRAME (화이트 플리커 → 블랙, 텍스트 없음)
- Soft Guidance: 비트별 구도 (셀피/와이드/게이트/성벽/레인)
- Creative Freedom: 먼지·초점 사냥 디테일

**기여 패턴**: 1 (CHARACTER LOCK — 목소리까지 포함한 4종 앵커),
  3 (렌즈 먼지·초점 사냥 — 폰 푸티지의 자국), 4 (호기심→충격→진심의 감정 전이),
  5 (시대고증 AVOID 목록), 7 (diegetic only + 정밀 립싱크)

```yaml
reference_state:
  source: "@bmx_ai13 / X — 2026 Vlog from Troy (30s, Seedance 2.5)"
  evidence_basis: prompt-derived
  subject:
    character_lock: [face, hair, voice, clothing] # 목소리까지 앵커
    gaze: camera_selfie # 브이로그 컨벤션
    dialogue: 5_lines_English_Japanese_accent_lipsync_precise
    emotion_arc: [curious, shaken, sincere]
    prop: modern_phone_held_every_shot
  camera:
    language: handheld_phone_footage
    artifacts_allowed: [autofocus_hunting, lens_dust, exposure_changes]
    shake_cap: not_excessive
    combat_distance: mostly_distant # 목격 가능성 규칙
  audio:
    diegetic_only: true
    bgm: none
  negatives: [modern_objects_except_gear, medieval_armor, magical_creatures,
    contextless_named_heroes, graphic_injuries, exaggerated_accents,
    comedic_reactions, triumphant_battle_portrayal]
  control_levels:
    hard_lock: [character_4way, phone_prop, period_negatives, last_frame]
    soft_guidance: [per_beat_composition]
    creative_freedom: [dust_focus_details]
```

---

## 18. @IqrasaifiAI (Iqra Saifi) — 사극풍 인테리어 여성 (30초)

**기본 정보**
- 출처: X @IqrasaifiAI (인증 계정, AI Filmmaker & Educator, Adobe Firefly 앰배서더)
- 본문: "Honestly felt like watching a scene straight out of a period drama" + "Prompt Below⤵️"
- **프롬프트는 댓글에 있는데 X 로그인 월 뒤라 미확인** — 텍스트 증거 없음
- 30초, 1280×720, 조회 6.7K (2026-09-24)
- 증거 기반: **frame-derived** (영상에서 5프레임 추출 분석) + post-described

**영상 흐름 (프레임 기준)** (frame-derived)
- f1 (~0s): 침대 위, 붉은 시스루 로브를 어깨에 걸친 채 앉아 아래를 봄
- f2 (~5s): 클로즈업, 몸을 앞으로 숙임
- f3 (~10s): 일어나 촛대 있는 화장대로 걸어감 (뒷모습, 맨등)
- f4 (~15s): 거울 — 뒤통수 + 거울 속 반영. 반영은 붉은 스트랩리스 드레스의 정면 얼굴
- f6 (~25s): 침대 옆에 서서 시스루 천을 들고 아래를 봄. 붉은 스트랩리스 드레스, 긴 머리
- f7 (~29s): 페이드 (파일 크기상 암전으로 추정)

**Subject state** (frame-derived)
- pose: 1인 여성, 긴 흑발. 침대에 앉기 → 숙이기 → 일어서기 → 거울 보기 → 서 있기.
  움직임은 느리고 절제됨
- gaze: 전편 아래를 보거나 거울 속 자신을 봄. **카메라를 직접 본 프레임 없음**.
  f4는 자기 자신과의 상호 시선 (거울)
- wardrobe: 붉은 시스루 로브 ↔ 붉은 스트랩리스 드레스. f1~f3은 로브, f4 반영과
  f6은 스트랩리스 드레스

**관찰된 불일치** (frame-derived — 관찰, 단정 아님)
- f4 거울 장면: 뒤통수의 머리는 올려 묶인 것처럼 보이고, 거울 속 반영은 긴 머리가
  내려와 있음. 거울 반영과 실제 뒷모습의 헤어 불일치로 보임. AI 거울 렌더의
  전형적 실패 패턴과 일치하나, 프레임 1장 기준이므로 "관찰된 차이"로만 기록

**Composition** (frame-derived)
- 침대 → 화장대 → 거울의 3공간 이동. 카메라는 인물을 따라가되 급격한 컷 없이
  부드럽게 전환되는 것으로 보임 (프레임 간 연속성 유지)
- 얕은 심도, 필름 스틸 미학

**Lighting** (frame-derived)
- 촛불 기반 따뜻한 황금-적색 조명. 격자창, 붉은 드레이프, 화려한 침구
- 전편 일관된 야간 실내 촛불 톤

**관찰 vs 추론**
- 관찰(프레임): 1인, 느린 움직임, 아래 시선, 카메라 응시 없음, 촛불 실내
- 관찰(프레임): f4의 거울 반영-뒷모습 헤어 차이
- 추론: 프롬프트 미확인이므로 의도된 연출인지 모델 실패인지 판단 불가. → 스펙 제외.
  단, "거울 장면의 반영 일관성"은 체크리스트 후보로 기록할 만함

**Production description → Control Levels**
- Hard Lock: (프롬프트 미확인 — 프레임에서 역추론하지 않음)
- 관찰 기록: 1인 여성, 촛불 실내, 아래 시선 유지, 거울 자기응시

**기여 패턴**: 2 (시선 — 전편 카메라 회피 + 거울 자기응시), 1 (거울 반영 일관성 —
  체크리스트 후보)

```yaml
reference_state:
  source: "@IqrasaifiAI / X — period drama interior (30s)"
  evidence_basis: frame-derived # 프롬프트는 로그인 월 뒤라 미확인
  subject:
    gaze: down_or_mirror_self # 카메라 직접 응시 없음
    movement: slow_restrained
    wardrobe: [red_sheer_robe, red_strapless_dress]
  observed_issue:
    mirror_hair_mismatch_f4: reflection_long_hair_down_vs_back_hair_up
    # 관찰된 차이. 의도/실패 판단 불가 — 체크리스트 후보
  lighting: candlelit_golden_red_interior
  camera: smooth_continuous_no_hard_cuts_observed
```

---

## 19. @iamahmedfaraz66 (Ahmad Faraz) — 빗방울 침실 MiniDV (15초)

**기본 정보**
- 출처: X @iamahmedfaraz66 (인증 계정)
- 생성: Seedance 2.5, 15초, 1280×720, 5샷 × 3초
- 프롬프트 전문 공개 (영어), 조회 811
- 게시 2026-09-24 12:50 (약 5시간 전)
- 증거 기반: prompt-derived (프롬프트 전문) + **frame-derived** (6프레임 추출 분석)

**컨셉** (prompt-derived)
- 비 오는 날, 젖은 머리로 방에 들어온 여성의 15초. 2000년대 초 Sony MiniDV
  홈비디오 룩. "완전히 솔직하고 연출되지 않은" — 다른 사람이 캠코더를 든 설정
- MOTION RULE: "부드럽고 연속적인 실시간 모션. 떨림·저더·프레임 스킵·슬로모 금지.
  빈티지함은 프레임 저하가 아닌 MiniDV 이미지 특성에서"

**벽·창문 검증 (사용자 지정 확인 항목)** (frame-derived)
- 프롬프트에 명시: "The rainy window remains a physical window throughout;
  walls must never turn into windows, doors or openings"
  → 벽이 창으로 변하는 실패를 직접 겨냥한 네거티브
- f1 (Shot 1): 나무 패널 문 + 복도. 벽은 벽, 문은 문
- f2 (Shot 2): 창문 클로즈업 — 창틀, 손잡이/잠금쇠 하드웨어, 유리에 빗방울.
  물리적 창문으로 읽힘. 바깥은 청회색 지붕들
- f3 (Shot 3): 와이드 — 같은 벽의 3연창 + 시스루 커튼. 벽은 베이지 민벽 유지.
  침대(왼쪽), 책상(오른쪽), 의자 위 흰 수건
- f4 (Shot 4): f3과 같은 구도. 창문·벽 동일
- f5·f6 (Shot 5): 창문 클로즈업 + 어깨너머 빗방울 유리. 창틀 하드웨어 재확인
- 판정: 6프레임에서 벽→창 변형 없음. f2의 단창 클로즈업과 f3의 3연창 와이드는
  같은 창문의 다른 거리로 읽힘 (모순 없음). 바깥 풍경(비 오는 지붕)도 일관

**시선 검증 (사용자 지정 확인 항목)** (frame-derived)
- f1: 방 안으로 들어오며 정면 (카메라 든 사람을 향한 자연스러운 방향)
- f2: 젖은 머리카락 → 소매 위 물방울을 내려다봄 (프롬프트와 일치)
- f3: 집으려는 수건을 내려다봄
- f4: 수건에 얼굴 가림, 머리를 문지름
- f5: 빗방울 창문을 바라보며 젖은 머리카락을 넘김
- f6: 창밖 비를 보며 작은 미소
- **6프레임 모두 카메라 렌즈를 직접 본 적 없음**. 시선 대상은 전부 명명된
  오브젝트 (머리카락·물방울·수건·창문). 컷을 넘어 시선 연속성 유지

**Subject state** (prompt + frame)
- pose: maroon 후드티, 긴 젖은 흑발. 들어오기 → 머리카락 만지기 → 수건 집기 →
  머리 말리기 → 창밖 보기
- performance: "아무도 안 보는 것처럼 자연스럽게. 과장된 연기·포즈·극적 표정 금지"
- 프레임에서 확인: 표정은 졸린 듯 무덤덤, 프롬프트의 "tiny sleepy smile"이 f6에
  관찰됨

**Camera evidence** (prompt + frame)
- MiniDV: 핸드헬드, 미세한 흔들림, 불완전한 프레이밍(f1의 문틀 기울기),
  오토포커스 헌팅, 노출 변화, DV 압축감, 저조도 노이즈
- 카메라 오퍼레이터가 존재하는 설정 — "The camera operator gently follows her"

**Audio** (prompt-derived)
- 로케이션 사운드만: 창문에 부딪히는 비, 먼 교통, 바람, 발소리, 문 소리,
  수건·옷감 소리. 음악·내레이션·효과음 금지

**관찰 vs 추론**
- 관찰(프레임): 벽·창문·문의 물리적 일관성 유지. 시선 대상 명명 + 카메라 응시
  제로. 프롬프트의 네거티브가 렌더에서 지켜짐
- 관찰(프롬프트): "walls must never turn into windows" — 실패 모드를 직접
  이름 붙인 네거티브의 가장 명확한 사례
- 추론: 없음

**Production description → Control Levels**
- Hard Lock: 5샷 × 3초 구조, 동일 인물·의상·아파트 레이아웃, 창문 물리적 고정,
  실시간 모션 (슬로모 금지)
- Soft Guidance: 샷별 구도, MiniDV 질감
- Creative Freedom: 빗방울 디테일, 바깥 풍경

**기여 패턴**: 2 (시선 — 전편 카메라 회피 + 명명된 대상),
  5 (벽→창 변형 금지 — 실패 출처 명시 네거티브의 대표 사례),
  6 (모션 버짓 — 실시간 모션 강제, 슬로모 금지),
  7 (로케이션 사운드만)

```yaml
reference_state:
  source: "@iamahmedfaraz66 / X — rainy bedroom MiniDV (15s, Seedance 2.5)"
  evidence_basis: prompt-derived + frame-derived
  subject:
    gaze: never_at_camera # 6프레임 모두 렌즈 응시 없음
    gaze_targets: [wet_hair, droplets_on_sleeve, towel, rainy_window] # 전부 명명
    performance: natural_unstaged_tiny_sleepy_smile_f6
  spatial:
    window: physical_throughout # 창틀·손잡이·빗방울로 확인
    walls: never_become_windows # 프롬프트 네거티브가 렌더에서 지켜짐
    layout_consistent: [bed, desk, chair, 3pane_window]
  camera:
    style: MiniDV_handheld
    motion_rule: realtime_only_no_slowmo
  audio:
    location_sound_only: [rain, traffic, wind, footsteps, door, towel_fabric]
  control_levels:
    hard_lock: [5x3s_structure, identity_layout, window_physical, realtime_motion]
    soft_guidance: [per_shot_framing, minidv_texture]
    creative_freedom: [raindrop_details, outside_view]
```

---

## 20. Higgsfield "Passport Rush" 메이킹 (METAL 기사, 2026-09-24)

**기본 정보**
- 출처: metallab.ai — Higgsfield가 9월 23일 유튜브에 공개한 28분 메이킹 영상 정리
- 대상: 5분짜리 액션 코미디 단편 "Passport Rush"의 택시 추격 시퀀스 (18씬, 3일 작업)
- 애니메이터 Amina가 전 과정 설명. Higgsfield Animation 채널 첫 에피소드
- 증거 기반: article-described (메이킹 영상에 대한 기사)

**파이프라인 구조** (article-described)
- 전통 파이프라인을 닮음. 전담 프롬프트 엔지니어 없음 — 캐릭터·환경·애니메이션
  담당 아티스트가 각자 파트의 프롬프트를 씀
- 스토리보드 패널에 주황색 표시 = Blender 프리비즈를 거치는 숏. 빈 패널은 바로
  영상 생성으로. 규칙: "특정 움직임·카메라 앵글이 있거나, 말로 설명하기엔
  너무 긴 숏은 Blender로"

**Asset-first 원칙** (article-described)
- "The quality of the image inputs dictates the quality of the overall film."
  (이미지 입력의 품질이 전체 영화의 품질을 결정)
- 캐릭터 시트·소품 시트·배경을 준비하는 역할을 "manager"라 부름 — 아트 디렉터급
- 캐릭터: Claude로 캐릭터 시트 프롬프트 작성 → Higgsfield 자체 이미지 모델
  Soul 2.0으로 4장씩 배치 생성 → 1장 선택 → Photoshop에서 채도·밝기 올리고
  실루엣 주변에 페인트 스트로크 추가. 히로인: 생강색 머리 + 파란 후드티.
  택시 기사: 모자 + 큰 콧수염

**배경의 해법** (article-described)
- 순수 수채화 배경은 테스트에서 "sloppy and lifeless". 한때 수채화를 버리고
  3D로 가자고 논의할 정도
- 해법은 조명: 한낮 → 늦은 오후로 시간대를 옮기고 프롬프트에 "따뜻한 저녁 빛 +
  강한 그림자"를 추가 → 볼륨과 깊이가 생김. "수채화 배경 위에 골든아워 조명"이
  작품의 비주얼 공식이 됨

**택시는 반대로** (article-described)
- 처음엔 차에도 수채화 텍스처가 강했는데, 움직이자 "3D 지오메트리 위에 이미지를
  늘려놓은 것처럼" 싸구려로 보임
- Amina의 분석: "무거운 수채화 텍스처는 모델이 움직임 속에서 유지하기엔 정보가
  너무 많다. 수채화 소품이 수채화 배경 위에 있으면 매 프레임 싸우는 빽빽한
  텍스처가 두 배가 된다." → 차는 클린 3D로. 지붕 날아간 버전은 Seedream 5.0 Pro로
  기존 이미지 편집

**프롬프트 구조** (article-described)
- 4초짜리 숏에도 에세이급 프롬프트: "우리가 쓰지 않은 모든 디테일은 모델이
  결정하는데, 모델은 형편없는 추측가다."
- **프롬프트의 앞 20%가 가장 중요** — 모델은 위에서 아래로 읽고, 뒤로 갈수록
  텍스트를 덜 엄격하게 따름
- 5개 블록: (1) 씬 컨텍스트와 스타일, (2) 활성 레퍼런스, (3) 숏 구조,
  (4) 락과 제약, (5) 애니메이션의 12원칙
- 이 구조는 Claude에 스킬로 한 번 작성해 팀 전체가 공유

**Blender 프리비즈** (article-described)
- 대표 숏: 택시가 두 바퀴로 기울어 트럭 사이를 빠져나감. Blender에서는
  회색 지오메트리 + 카메라만으로 언제 기울고 언제 착지하는지 프리뷰
  (색·재질 없음) → 그 프리뷰를 영상 입력으로, 택시·트럭·캐릭터·도로·조명
  이미지를 레퍼런스로 붙여 생성. 영상 생성은 Seedance 2.5

**실패 사례들** (article-described)
- 트럭 문 옆 숏: Blender 카메라가 너무 가까워서 모델이 회색 도형을 해석 못 함.
  카메라를 뒤로 빼니 해결
- 안전벨트 씬: 카메라 앵글 고정을 위해 붙인 스크린샷에 소녀의 헤드폰이 빠져
  있었는데, 그 뒤 모든 테이크에서 헤드폰이 사라짐. Photoshop으로 스크린샷에
  헤드폰을 손으로 그려 넣어 해결
- **못 푼 숏**: 천장 손잡이를 잡았다가 뜯어지고, 당황해서 다른 걸 잡았다가 또
  뜯어지는 개그. 첫 손잡이가 고장났다는 걸 깨닫는 "짧은 멈칫"이 개그의 핵심인데,
  회색 캐릭터로는 표정·손 움직임을 전달 못 함. 디테일을 추가하자 모델이 캐릭터
  시트 대신 Blender 지오메트리를 복사해버림. 팀은 이를 "performance gap"이라 부름
- "큰 액션 씬이 더 어려울 줄 알았는데, AI가 어려워하는 건 미묘한 캐릭터
  연기였다."

**METAL의 해석** (article-described)
- 도구가 노동을 대체한 게 아니라 노동이 이동함: 손그림 → 에셋 선택·수정과
  프롬프트 작성. 애니메이터들이 가장 오래 붙잡은 건 캐릭터가 "머뭇거리는
  반 박자"

**관찰 vs 추론**
- 관찰(기사): 스토리보드-퍼스트, 에셋-퍼스트, 5블록 프롬프트, 앞 20% 규칙,
  회색 지오메트리 프리비즈, 실패 3건, performance gap
- 추론: 이 파이프라인은 네 XAI-Studio-Video의 개념들과 거의 1:1로 대응됨
  (아래 매핑). → 네 시스템 이야기는 스펙이 아니라 참고 매핑으로만 기록

**네 시스템과의 매핑** (참고용, 스펙 아님)
- 주황 패널 = Blender 프리비즈 → 블로커트 프리비즈
- 5블록 프롬프트 → Master Creative Spec의 블록 구조
- (4) 락과 제약 → Hard Lock / Soft Guidance
- (2) 활성 레퍼런스 → 레퍼런스 역할 분리 (패턴 1)
- 에셋-퍼스트 → Character/Visual DNA
- 헤드폰 사건 → 레퍼런스 위생 (락용 스크린샷의 완전성)
- 앞 20% 규칙 → 프롬프트 순서 가중치 (신규 후보)
- performance gap → 미묘한 연기가 액션보다 어려움. MV 감정연기의 난이도 근거

```yaml
reference_state:
  source: "Higgsfield Passport Rush making-of via METAL (2026-09-24)"
  evidence_basis: article-described
  pipeline:
    storyboard_first: orange_panels_blender_previs
    no_prompt_engineer: artists_write_own_prompts
    asset_first: "image input quality dictates film quality"
    prompt_5_blocks: [scene_context_style, active_references, shot_structure,
      locks_constraints, twelve_principles_of_animation]
    prompt_front_weight: first_20_percent_matters_most
    previs: gray_geometry_plus_camera_only # 색·재질 없음
    video_model: Seedance_2_5
  key_fixes:
    background: golden_hour_lighting_over_watercolor
    taxi: clean_3D_because_heavy_texture_too_much_info_in_motion
    headphone: hand_drawn_back_into_lock_screenshot
  unsolved:
    performance_gap: subtle_acting_harder_than_action
    ceiling_handle_gag: brief_pause_of_realization_unconveyable
```

---

## 21. @diyah04_ (Mamah Yaya) — 부채 트랜스포메이션 선협 코스프레 (12.7초)

**기본 정보**
- 출처: Threads @diyah04_ (AI Threads 배지), 게시 2026-09-22
- 프롬프트 전문 공개 (영어) + 인도네시아어 한 줄: "Seperti biasa, cukup referensi
  wajah saja ya seng" (늘 그렇듯 얼굴 레퍼런스만이면 돼)
- 조회 6.6K, 좋아요 97, 댓글 58
- 증거 기반: prompt-derived + **frame-derived** (7프레임 추출 분석)
- 실제 영상 12.7초 (프롬프트는 10초라 했으나 렌더는 더 김)

**컨셉** (prompt-derived)
- 9:16 세로. Douyin 스타일 메이크업 트랜스포메이션 × 선협 코스프레 에디토리얼
- 0–3.5초: 민낯 부채 안무 → 3.5초에 부채가 렌즈를 가득 채우며 HARD CUT →
  3.5–10초: 풀 코스프레 리빌
- "donghua vibe"는 캐릭터 스타일링에만 해당. 얼굴은 100% 실사 인간 유지.
  NO anime face / NO illustrated skin / NO CGI-looking face / NO plastic skin
- "She must NEVER simply stand and wait for the transition" — 전환 전 대기 금지

**전환 디바이스** (prompt + frame)
- 부채가 화면을 가득 채우는 와이프 = 하드컷 (f3에서 확인: 부채가 프레임 전체를
  가림)
- 컷 전후 신체 위치·부채 위치·카메라 앵글·움직임이 정확히 이어져야 함
  (f3→f4: 부채 위치 연속 확인)
- **#1의 CUT 트리거와 같은 전환 디바이스 계열**. 이 작성자의 일관 기법
  (14번 aanggaamc와 마찬가지로 분할 렌더 + 전환 디바이스로 추정)

**시선** (prompt + frame)
- f1·f2: 민낯 상태에서도 카메라를 강렬하게 응시 ("looks intensely into the camera")
- f4: 부채를 내리며 변신한 얼굴 공개, 직접적인 아이컨택
- f6: 얼굴을 렌즈 쪽으로 기울임
- f7: 턱을 살짝 내리고 카메라에 시선 고정 ("eyes locked onto camera")
- **전편 카메라 응시가 의도된 장르** (Douyin 트랜스포메이션 관습).
  15번·19번의 "카메라 응시 금지"와 정반대 — 장르에 따라 카메라 응시 규칙이
  뒤집히는 사례

**프롬프트에 없는데 렌더에 새어든 것** (frame-derived)
- 프롬프트: NO text / NO logo / NO watermark
- 실제 영상: 우하단에 **"Dola AI" 워터마크**가 전 프레임에 박혀 있음
  (생성 툴의 번인 워터마크 — 프롬프트로 막을 수 없는 레이어)
- 부채 위에 **"diyah04__"** 텍스트가 렌더됨 (f2·f3·f4에서 확인. 작성자 핸들을
  모델이 부채 장식으로 해석했거나, 작성자가 후처리로 넣었거나 — 단정 불가)
- **#14의 "TEM..." 글자 새어듦과 같은 실패 계열**: 네거티브에 텍스트 금지를
  써도 막히지 않는 경우가 있음. 출처 불명 요소는 스펙에서 제외

**세트 연속성** (frame-derived)
- 문게이트(원형 문), 랜턴, 화병, 조각 스크린, 향로 연기가 7프레임 내내 유지
- 변신 후 의상: 상아·펄화이트·실버·딥크림슨 한푸, 은 왕관, 옥 장식, 진주 체인,
  이마 장식, 그라데이션 레드 립 — 프롬프트의 액세서리 목록과 일치
- f5: 뒤돌아선 뒷모습 — 헤어스타일 뒷면의 비녀·장식이 유지됨 (뒷모습 일관성)

**관찰 vs 추론**
- 관찰(프레임): 부채 와이프 전환, 전편 카메라 응시, 세트·의상 일관성,
  프롬프트에 없는 텍스트 2종 (Dola AI 워터마크, 부채 위 diyah04__)
- 관찰(프롬프트): "얼굴 레퍼런스만" 한 줄 — 얼굴은 이미지 앵커, 나머지는 텍스트
- 추론: 분할 렌더로 추정되나 증거 없음 → 스펙 제외

**Production description → Control Levels**
- Hard Lock: 3.5초 하드컷 타이밍, 부채 와이프 전환, 실사 인간 얼굴 (애니메 금지),
  카메라 응시 유지
- Soft Guidance: 부채 안무 시퀀스, 카메라 래터럴 오빗·푸시인
- Creative Freedom: 세트 디테일, 연기 강도

**기여 패턴**: 2 (시선 — 장르별 카메라 응시 규칙의 뒤집힘),
  4 (전환 디바이스), 5 (텍스트 금지 네거티브가 막지 못한 새어듦)

```yaml
reference_state:
  source: "@diyah04_ / Threads — fan-sweep xianxia transformation (12.7s)"
  evidence_basis: prompt-derived + frame-derived
  transition_device: fan_fills_frame_hard_cut_at_3_5s
  subject:
    gaze: intense_direct_eye_contact_throughout # 장르 관습상 의도적
    face: photorealistic_human_locked # NO anime/CGI/plastic
    identity: face_reference_only # 작성자: "얼굴 레퍼런스만"
  leak_observed:
    - "Dola AI watermark baked in (tool layer, prompt cannot block)"
    - "'diyah04__' text rendered on fan (source undetermined, excluded from spec)"
  set_continuity: [moon_gate, lanterns, vases, carved_screens, incense_smoke]
  control_levels:
    hard_lock: [cut_timing_3_5s, fan_wipe_transition, photoreal_face, camera_gaze]
    soft_guidance: [fan_choreography, lateral_orbit, push_in]
    creative_freedom: [set_details, performance_intensity]
```

---

## 22. @QAiStudio (Tensor) — CHASE 헬스장 브이로그 (15초)

**기본 정보**
- 출처: X @QAiStudio (골드 인증), 게시 2026-09-24 14:22 (약 7시간 전)
- 생성: Seedance 2.5 on Flova AI, 15초, 1280×720, 8샷
- 프롬프트 전문 공개 (영어), 조회 4,914, 좋아요 110
- 댓글: "DV 캠코더 핸들링이 거친 리얼함을 준다" (첫 댓글)
- 증거 기반: prompt-derived + **frame-derived** (8프레임 추출 분석)

**컨셉** (prompt-derived)
- 한국 아이돌 CHASE(20대)의 운동 후 셀프 브이로그. DV 16mm 테이프 캠코더
  핸드헬드 질감
- **POV: CHASE 본인이 카메라를 듦.** 가끔 랙·벤치에 올려놓음. "캠코더는 화면에
  절대 등장하지 않음"
- 스타일: 장난스럽고 자기비하적인 짐 브이로그 톤. 과장된 투덜거림, 진짜 웃음,
  지쳤지만 즐거운 에너지

**카메라 = 등장인물** (prompt + frame)
- 카메라가 다이제틱 캐릭터 (시청자). 시선의 문법 전체가 카메라 응시
- f1: 스쿼트랙에 올린 카메라, 미디엄샷, 숨 고르기. 카메라 응시
- f2: 핸드헬드 얼굴 클로즈업, 일그러진 웃음. 카메라 응시
- f3: 레그프레스 미디엄샷, 웃음. 카메라 응시
- f4: 머신 손잡이 쥔 손 매크로 인서트 (대사 없음, 체육관 앰비언트만)
- f5: 비틀거리며 랙을 잡음, 거울 벽에 **등진 모습이 반사로 일관되게** 찍힘.
  얼굴이 프레임 위로 잘림 — "occasional face cut-off framing"이 실제 렌더됨
- f6: 정수기 쪽으로 비틀걸음, 카메라가 걸음에 맞춰 흔들림. 카메라 응시하며 웃음
- f7: 정수기에서 물 마시기. 시선은 정수기 (명명된 대상)
- f8: 벽에 기대어 암즈렝스 셀카 피니시, 지친 미소. 렌즈 응시
- **시선 규칙**: 21번과 같은 계열 — 브이로그 장르에서는 카메라 응시가 문법.
  f7의 정수기 시선만 명명된 오브젝트로 분리

**캐릭터 DNA** (prompt + frame)
- 긴 흑발 하이포니테일, 운동 후 땀 광택, 큰 표정 풍부한 눈
- 모 modest 긴팔 애슬레틱 탑 (팔·몸통 완전 커버), 루즈 조거, 스니커즈,
  목에 수건, 주얼리 없음
- 프레임 확인: 포니테일·의상·땀 광택 전편 일관. **목의 수건은 추출된 8프레임에서
  확인되지 않음** (프롬프트와 렌더의 차이로 관찰만 기록)
- 주얼리 없음 — 일관

**세트** (prompt + frame)
- 저녁 체육관: 스쿼트랙, 레그프레스, 정수기(자판기형), 거울 벽, 라커, 부드러운
  천장 조명. 8프레임에서 레이아웃 일관

**대사** (prompt-derived)
- 영어 대사 8개, 샷별 지정 ("Okay... leg day is not it today." 등)
- 스틸 프레임으로는 립싱크 검증 불가 → 검증 불가로 기록

**관찰 vs 추론**
- 관찰(프레임): 셀프 POV + 전편 카메라 응시, 거울 반사 일관성, 얼굴 잘림
  프레이밍의 실제 렌더, 수건 미확인, 땀 광택·의상 일관
- 관찰(프롬프트): "캠코더는 화면에 절대 등장하지 않음" — 셀프 POV의 물리 규칙
- 추론: 없음

**Production description → Control Levels**
- Hard Lock: 8샷 스토리보드, CHASE 캐릭터 DNA, 셀프 POV (캠코더 비등장),
  실시간 모션
- Soft Guidance: DV 질감, 핸드헬드 흔들림, 불완전 프레이밍
- Creative Freedom: 웃음의 강도, 땀 디테일

**기여 패턴**: 1 (앵커 락 — 캐릭터 DNA 명세),
  2 (시선 — 카메라가 등장인물인 경우의 응시 문법),
  5 (거울 반사 일관성 — 18번의 거울 관찰과 연결),
  6 (불완전 프레이밍을 의도적 디바이스로)

```yaml
reference_state:
  source: "@QAiStudio / X — CHASE gym vlog (15s, Seedance 2.5)"
  evidence_basis: prompt-derived + frame-derived
  camera:
    pov: CHASE_holds_camera_herself # 카메라는 다이제틱 캐릭터
    rule: camcorder_never_appears_on_screen
    texture: DV_16mm_tape_handheld
    imperfect_framing_rendered: face_cutoff_f5
  subject:
    gaze: at_camera_throughout # 브이로그 문법
    gaze_exception: water_fountain_f7 # 명명된 대상
    character_dna: [high_ponytail, postworkout_sheen, modest_athletic_wear, no_jewelry]
    towel_around_neck: not_visible_in_sampled_frames # 관찰된 차이
  spatial:
    mirror_reflection: consistent_back_view_f5
    layout: [squat_rack, leg_press, water_fountain, mirror_wall, lockers]
  dialogue: 8_english_lines # 립싱크는 스틸로 검증 불가
  control_levels:
    hard_lock: [8_shot_storyboard, character_dna, self_pov, camcorder_never_shown]
    soft_guidance: [dv_texture, handheld_shake, imperfect_framing]
    creative_freedom: [laughter_intensity, sweat_detail]
```

---

## 23. @ChillaiKalan__ (K) — 옥상 라디오 석양 (30초)

**기본 정보**
- 출처: X @ChillaiKalan__ (인증), 게시 2026-09-24 14:45 (약 7시간 전)
- 생성: Seedance 2.5 on Higgsfield, 30초, 16:9, 1080p
- 프롬프트 전문 공개 (영어), 조회 1,392, X "Made with AI" 라벨
- 증거 기반: prompt-derived + **frame-derived** (6프레임 추출 분석)

**컨셉** (prompt-derived)
- 모로코 카사블랑카 아파트 옥상, 일몰 전. 20대 초반 모로코 여성 (곱슬머리·
  패브릭 밴드, 머스타드 스웨트셔츠, 다크진, 흰 캔버스 스니커즈, 얇은 은 목걸이)
- 오래된 배터리 라디오를 고쳐보다 일몰 전에 음악이 터지는 30초
- "The entire story happens in one location. No shopping, no café, no market,
  no journey, and no walking-home sequence." — 단일 로케이션 선언

**소품 물리** (prompt + frame)
- 라디오: f1에서 테이블 위 먼지 쌓인 라디오 → 노브 돌리기 → f2 배터리함 열기 →
  f3 안테나 뽑기·회전. 6프레임에서 같은 라디오 (그릴·노브·손잡이·안테나 일관)
- "The radio must behave like a real old battery-powered device."
  다이얼은 물리적으로 회전, 안테나는 현실적으로 확장, 회전에 따라 스태틱 변화
- NEGATIVE: "impossible radio mechanics, fake static, unrealistic antenna
  movement" — 소품별 실패 모드를 직접 이름 붙인 네거티브 (패턴 5)

**시선 문법** (prompt + frame)
- f1·f2·f3: 라디오를 봄 (명명된 대상)
- 카메라 응시는 대사 순간에만 2회: "Come on…" (0–5초), "There." (15–21초)
- f4: 음악이 터지자 라디오를 보며 진짜 미소
- f5·f6: 의자에 앉아 일몰을 봄 (명명된 대상)
- **세 번째 시선 문법**: 15·19번은 전편 회피, 21·22번은 전편 응시,
  이건 대사 결합형 — 말이 있을 때만 카메라를 봄

**로케이션 연속성** (frame-derived)
- 6프레임 모두 같은 옥상: 콘크리트 벽, 빨랫줄, 위성 안테나, 화분, 플라스틱 의자,
  나무 테이블, 이웃 건물. "ordinary rooftop clutter" 유지
- 햇빛이 점진적으로 따뜻해짐 — f1은 옅고 f4–f6은 골든. "gradually changes"
  렌더됨
- 자막·워터마크·로고 없음 (프레임에서 확인)

**절제** (prompt-derived)
- "Don't force emotion. Don't make the sunset overly dramatic."
- "Keep the imperfect camera movement, ordinary rooftop clutter, realistic wind,
  slight autofocus mistakes, and natural pauses."
- 오디오: 옥상 앰비언스만. "NO ADDED BACKGROUND MUSIC. The radio melody must
  be original" — 오디오 권위 (패턴 7)

**관찰 vs 추론**
- 관찰(프레임): 단일 로케이션 유지, 라디오 동일 오브젝트, 안테나 확장,
  햇빛 점진 변화, 캐릭터 DNA 일관 (목걸이 f1·f2에서 확인)
- 관찰(프롬프트): 대사 결합형 카메라 응시, 소품별 네거티브
- 추론: 없음

**Production description → Control Levels**
- Hard Lock: 30초 단일 로케이션, 6샷 브레이크다운, 라디오 물리, 동일 인물·의상
- Soft Guidance: 핸드헬드 컨슈머 캠코더 질감, 햇빛 점진 변화
- Creative Freedom: 바람·빨래 디테일, 미소의 타이밍

**기여 패턴**: 2 (시선 — 대사 결합형 세 번째 문법),
  3 (자국 서술 — 라디오 물리), 5 (소품별 실패 네거티브),
  6 (절제 — "감정을 강제하지 마라"), 7 (앰비언스만)

```yaml
reference_state:
  source: "@ChillaiKalan__ / X — rooftop radio sunset (30s, Seedance 2.5)"
  evidence_basis: prompt-derived + frame-derived
  location: single_rooftop_casablanca # No shopping/cafe/market/journey
  prop_physics:
    radio: same_object_6_frames
    antenna: extends_realistically_f3
    dial: physically_rotates
    negative: [impossible_radio_mechanics, fake_static, unrealistic_antenna]
  subject:
    gaze: dialogue_coupled_camera_looks # "Come on…" / "There." 때만 카메라
    gaze_default: radio_then_sunset # 명명된 대상
    character_dna: [curly_hair_fabric_band, mustard_sweatshirt, dark_jeans,
      white_sneakers, thin_silver_necklace]
  light: gradually_warmer_f1_to_f6
  restraint: [dont_force_emotion, dont_overdramatize_sunset]
  audio: rooftop_ambience_only_no_music_original_melody
  control_levels:
    hard_lock: [single_location, 6_shot_breakdown, radio_physics, identity]
    soft_guidance: [consumer_camcorder_texture, gradual_light_change]
    creative_freedom: [wind_laundry_detail, smile_timing]
```

---

## 24. @AIwithSynthia (Synthia) — 화장실 좀비 어택 (30초) [실패 사례]

**기본 정보**
- 출처: X @AIwithSynthia (인증), 게시 2026-09-24 20:57 (약 1.5시간 전)
- 생성: Seedance 2.5, 30초, 1280×720, X "Made with AI" 라벨
- 프롬프트 전문 공개 (영어), 조회 1,632
- 증거 기반: prompt-derived + **frame-derived** (8프레임 추출 분석)
- **사용자가 직접 실패를 지적한 케이스**: 좀비 수, 추리닝 여자의 감염 여부,
  화장실 안 좀비 수 불일치

**프롬프트의 의도** (prompt-derived)
- 좀비 1명 (이미지 레퍼런스 `<<< image>>>`, 얼굴·머리·체형·의상 고정) +
  피해자 1명 → 피해자 감염 → "The two infected women"이 새로 들어온 사람을
  향해 돌진 → 마지막에 2명이 형광등 아래 카메라를 응시
- 네거티브에 "no duplicate characters" 명시

**프레임별 인원 추적** (frame-derived)
- f1 (~2.5초): 피해자(그레이 후드·긴 갈발)가 손 씻음. 거울에 2명 (본인 반사 +
  뒤에 선 좀비). 실제 공간에도 2명. **이 시점 좀비 1명** (흰 탱크톱·카키 카고·
  흑단발). 거울 반사 일관 — #18과 달리 거울은 정상
- f2 (~7.5초): 좀비가 피해자에게 돌진. 2명
- f3 (~12.5초): 좀비가 세면대 너머로 공격 (모션 블러). 2명
- f4 (~17.5초): 피해자가 타일 벽에 눌림. 목·얼굴에 검은 혈관, 눈이 하얗게
  뒤집힘. 좀비의 창백한 손이 목을 잡음. 감염 진행 중
- f5 (~22.5초): 피해자가 네 발로 쓰러짐. 손이 창백해지고 혈관이 보임.
  뒤에 좀비 (카고 바지·흰 스니커즈)가 서 있음. 2명
- f6 (~27.5초): **공격자 3명** — 왼쪽 흰 탱크톱·카고 (원본 좀비) + 가운데
  그레이 후드 (일어난 피해자) + 오른쪽 흰 탱크톱·카고 (**복제된 좀비**).
  문 쪽의 세 번째 인물에게 돌진
- f7 (~26초): 돌아서는 2명 — 그레이 후드 (검은 눈) + 흰 탱크톱 1명
- f8 (~29초): 최종 — 형광등 아래 가만히 서서 카메라를 응시하는 2명.
  프롬프트의 엔딩과 일치

**사용자 지적 3건에 대한 판정**
1. **좀비 수**: 프롬프트는 좀비 1명 → 감염 후 2명. 렌더는 f1–f5·f7·f8에서 2명
   유지, **f6 돌진 구간에서만 흰 탱크톱 좀비가 2명으로 복제되어 3명**.
   복제 좀비는 f6에만 존재하는 일시적 duplicate
2. **추리닝(그레이 후드) 여자**: 피해자이며 **감염됨이 맞음**.
   f4 (혈관·흰 눈) → f5 (쓰러짐·창백한 손) → f6 (일어나 함께 돌진) →
   f7·f8 (검은 눈으로 카메라 응시). 감염 서사는 렌더됐으나, f6의 복제로
   "누가 감염자인지" 헷갈리게 됨
3. **화장실 안 좀비 수**: f1 시점 좀비 1명. f6에서 일시적 3명, f8에서 2명.
   **"no duplicate characters" 네거티브 + 이미지 레퍼런스 지정에도 불구하고
   복제 발생**

**실패의 교훈**
- 네거티브에 "복제 금지"를 써도 돌진 같은 고에너지 구간에서 복제가 새어듦
- 이미지 레퍼런스로 좀비를 고정해도 마찬가지 — 레퍼런스는 외형 고정에만
  작용하고 인원 수 보장에는 작용하지 않음
- 관객 댓글은 복제를 못 알아챔 ("infection spread and that final stare" 극찬) —
  실패가 눈에 띄지 않아도 스펙 위반은 위반
- 후보 규칙 연결: **샷별 인원수 명시** (각 샷에 "화면에 정확히 N명"을 Hard Lock으로).
  이름 붙은 캐릭터 + 샷별 헤드카운트는 레포 승격 후보에 추가할 만한 사례

**추가 분석 — 감염 위치의 공간 연속성 붕괴** (사용자 관찰 + frame-derived)
- 사용자 지적: "사로 안에 들어갔는데 감염되는 건 밖이야"
- 프레임 확인 (~8초): 좀비가 변기 칸 문 앞에서 피해자를 잡음 — 공격 시작점은
  STALL DOORS
- 프레임 확인 (~14초): 좀비(흰 탱크톱)가 세면대 위에 엎드려 있고, 피해자
  (그레이 후드)는 오히려 변기 칸 문 쪽에 서 있음 — **공수·위치가 뒤바뀜**.
  누가 누구를 공격하는지 프레임만으로 판독 불가
- 프레임 확인 (~17초): 피해자가 밋밋한 타일 벽에 눌려 감염 진행 (목의 손,
  흰 눈). 공격 지점(변기 칸)과 다른 장소
- 프롬프트의 원인: 변기 칸이라는 장소가 프롬프트에 **한 번도 등장하지 않음**.
  "pins her against the tiled wall" — 어느 벽인지, 감염이 어디서 일어나는지,
  각 비트의 WHERE가 없음. 동작 목록만 있고 블로킹이 없음
- 모델이 변기 칸을 스스로 발명해놓고, 감염 비트에서는 그 장소를 잃어버림
- 대응 후보: **비트별 장소 앵커** — 각 비트에 명명된 장소 노드
  (SINK AREA / STALL DOORS / TILED WALL / EXIT)를 찍고, 상태 전이
  (물림 → 감염)는 장소를 명시 ("물린 그 변기 칸 안에서 감염이 진행된다").
  #2의 상대 좌표 블로킹과 Shot Graph의 네거티브 증명 — 없으면 공간이
  뒤섞인다는 실증

**관찰 vs 추론** (추가분)
- 관찰(프레임): 공격 시작점=변기 칸 문 (~8초), 공수 뒤바뀜 (~14초),
  감염 지점=별개의 타일 벽 (~17초)
- 관찰(프롬프트): 장소 명칭 전무, "the tiled wall"만 1회
- 추론: 없음

**관찰 vs 추론**
- 관찰(프레임): f6의 일시적 3명, f8의 2명 복귀, 감염 서사 4단계 (f4→f5→f6→f7),
  거울 반사 일관
- 관찰(프롬프트): 좀비 이미지 레퍼런스 + no duplicate characters 네거티브
- 추론: 복제가 돌진 구간에서 발생한 이유는 단정 불가 → 스펙 제외

**Production description → Control Levels**
- Hard Lock (의도됐으나 지켜지지 않음): 좀비 1명 + 피해자 1명, no duplicates
- Soft Guidance: 핸드헬드, 형광등 조명
- Creative Freedom: 감염 디테일, 연기

**기여 패턴**: 1 (앵커 락의 한계 — 레퍼런스로도 막지 못한 복제),
  5 (네거티브의 한계 — "no duplicate characters"가 막지 못함),
  8 (신규 후보 — 샷별 헤드카운트 명시)

```yaml
reference_state:
  source: "@AIwithSynthia / X — washroom zombie attack (30s, Seedance 2.5)"
  evidence_basis: prompt-derived + frame-derived
  failure_case: true
  intended: [1_zombie_image_referenced, 1_victim, 2_infected_final]
  observed_headcount:
    f1_to_f5: 2
    f6_charge: 3 # duplicate white-tank zombie, transient
    f7_to_f8: 2
  victim_grey_hoodie: infected_confirmed # f4 veins/white eyes → f5 collapse →
    # f6 rises → f7/f8 black eyes camera stare
  negative_failed: no_duplicate_characters # 명시됐으나 f6에서 복제
  mirror: consistent # f1 거울 반사 정상
  spatial_failure: attack_at_stall_doors_infection_at_plain_wall
    # ~14초 공수 뒤바뀜, 프롬프트에 장소 명칭 전무
  lesson: [shot_level_headcount_as_hard_lock, location_anchored_beats] # 후보 규칙
```

---

## 25. @SadiaMalik182 (Sadia) — 마지막 열차, 한 명 너무 많은 승객 (30초)

**기본 정보**
- 출처: X @SadiaMalik182 (인증), 게시 2026-09-24 19:20 (약 3시간 전)
- 생성: Seedance 2.5 on WaveSpeedAI, 30초, 세로 1088×1920, X "Made with AI" 라벨
- 프롬프트 전문 공개 (영어, 샷별 30초 브레이크다운), 조회 541
- 증거 기반: prompt-derived + **frame-derived** (8프레임 추출 분석)
- 사용자 질문: "일관성이 없는데 그래서 괴이를 표현한 것 같아. 제작자의 의도일까"

**프롬프트의 설계** (prompt-derived)
- 제목 자체가 카운팅 이상: "The last train arrived with one passenger too many"
- 불가능성의 카탈로그: 존재하지 않는 역명, 터널 속 수백 명의 가만히 선 사람들,
  문 밖에 있는 똑같은 열차, 그 안에 앉아 있는 또 다른 자신, 사라지는 승객들,
  없어진 반사상
- 모든 "불일치"가 비트별로 명시됨 — 즉 **괴이는 스펙**

**프레임별 확인** (frame-derived)
- t1 (~2초): 플랫폼을 달리는 여성 (베이지 블라우스·어두운 스커트)
- t2 (~6초): 차내 — 여성 + 승객 3명 (정장 남성·노년 여성·헤드폰 청년).
  "only three passengers" 일치
- t3 (~10초): 같은 4명, 조명 어두워짐. "동시에 고개를 돌린다"는 스틸로 확인 불가
- t4 (~14초): 행선 표시기 보임. "존재하지 않는 역" 비트
- t5 (~18초): 문이 열리고 정장 남성이 서 있음. 문 너머 어둠 속에 가만히 선
  군중 — **프롬프트는 이 군중을 10–16초 "창밖 터널"에 배치**. 렌더는 열린 문
  앞으로 비트를 옮김 (beat displacement)
- t6·t7 (~22–26초): 문 너머 **똑같은 열차**, 파란 좌석에 또 다른 자신이 앉아
  있음. 도플갱어 비트 렌더됨. 의상(블라우스·스커트) 일관
- t8 (~28.5초): 여성 클로즈업, 승객 0명. "The other passengers disappear" 렌더됨

**의도 vs 모델 아티팩트 판정**
- 의도 (프롬프트에 명시): 도플갱어, 똑같은 열차, 사라지는 승객, 존재하지
  않는 역, 없어진 반사상 — 전부 스펙대로 렌더됨
- 모델 아티팩트이나 장르가 흡수: t5의 군중 비트 이동 (창밖→문 앞).
  공포 장르에서는 하나의 악몽으로 읽혀서 의도로 보임
- 실패가 피처가 된 경우: 행선 표시기의 난독 텍스트 ("Karoi Suta" 등).
  네거티브에 "no random text"가 있으나, "존재하지 않는 역" 비트에는 오히려
  난독이 필요했음 — 모델의 텍스트 렌더 실패가 컨셉에 봉사
- 명백한 비의도 아티팩트: 우상단 "Wavespeed SEEDANCE 2.5" 워터마크 번인.
  네거티브에 "no watermark" 명시됐으나 툴 레이어에서 새어듦 (#21 Dola AI
  케이스와 동일 계열)

**핵심 통찰 — 장르 흡수 불일치**
- 초자연 호러에서는 모델의 고유 실패 모드(불가능한 기하학, 사라지는 인물,
  정체 이상)가 서사 안에서 읽힘 — 장르 계약("이 세계는 일부러 틀렸다")이
  버그를 피처로 전환
- #24(좀비)의 정반대: 같은 연속성 붕괴라도 물리 리얼리즘 장르에서는 실패,
  호러 장르에서는 의도로 읽힘
- 제작 시사점: 모델의 약점과 장르의 계약을 맞춰라. 불가능성을 스펙으로
  명시하면(비트별 샷 브레이크다운) 관객은 글리치를 디자인으로 읽는다
- 단, 제작자가 어떤 글리치를 환영하고 어떤 걸 용인했는지는 외부에서 단정
  불가 — 워터마크만이 명백한 비의도 증거

**관찰 vs 추론**
- 관찰(프레임): 승객 3명→0명, 도플갱어, 문 앞 군중, 워터마크 번인, 여성 의상 일관
- 관찰(프롬프트): 불가능성 6종 전부 비트별 명시, no watermark 네거티브
- 추론: t5 비트 이동이 의도적 재배치인지 모델 압축인지는 단정 불가 → 스펙 제외

**Production description → Control Levels**
- Hard Lock: 불가능성 6종의 비트별 배치, 승객 3명→소멸, 도플갱어
- Soft Guidance: 핸드헬드, 형광등 플리커, diegetic 사운드만
- Creative Freedom: 군중의 정확한 위치 (모델이 문 앞으로 옮김 — 장르가 흡수)

**기여 패턴**: 6 (절제 — "subtle supernatural effects", 고어 없이 조용한 틀어짐),
  8 (신규 — 장르 흡수 불일치: 호러에서는 글리치가 의도로 읽힌다),
  14 (프롬프트에 없는 것 — 워터마크 번인)

```yaml
reference_state:
  source: "@SadiaMalik182 / X — last train doppelganger (30s, Seedance 2.5)"
  evidence_basis: prompt-derived + frame-derived
  format: portrait_1088x1920
  designed_impossibilities: # 전부 프롬프트에 비트별 명시 — 의도
    [nonexistent_station, tunnel_crowd, identical_train_outside_doors,
     doppelganger_seated, passengers_disappear, reflection_gone]
  model_artifacts_absorbed:
    crowd_beat_displaced: window_tunnel_to_open_doors # t5, 장르가 흡수
    display_gibberish: failure_became_feature # "존재하지 않는 역"에 봉사
  unintended_artifact: wavespeed_seedance_watermark_burnin # no watermark 무력화
  character_dna: [beige_blouse, dark_skirt] # t1→t8 일관
  insight: genre_absorbent_inconsistency # 호러에선 글리치가 의도로 읽힘
  control_levels:
    hard_lock: [6_impossibility_beats, passenger_3_to_0, doppelganger]
    soft_guidance: [handheld, fluorescent_flicker, diegetic_sound_only]
    creative_freedom: [crowd_exact_placement]
```

---

## 26. @pyona_ai (Pyona) — ORANGE SODA INCIDENT (30초)

**기본 정보**
- 출처: X @pyona_ai (인증), 게시 2026-09-23 01:55 (약 2일 전)
- 생성: Seedance 2.5, 30초, 9:16 세로, 24fps, X "Made with AI" 라벨
  > ⚠️ 정정 (Claude, 2026-09-26): 같은 게시물의 파일(Grok `videos/PAT-20260925-cafeteria-soda-1v2-ladder.mp4`)은 **1920×1080 16:9**, 30.93s다. 9:16은 프롬프트 값으로 보인다. evidence E5.
- 프롬프트 전문 공개 (**중국어**), 조회 3,079
- 증거 기반: prompt-derived + **frame-derived** (9프레임 추출 분석)
- 댓글: "Prompt in chinese would be more accurate for seedance" —
  Seedance에는 중국어 프롬프트가 더 잘 먹는다는 커뮤니티 지식

**컨셉** (prompt-derived)
- 한국 대학 캠퍼스 식당. PYONA(연분홍-파랑 머리)에게 A(흑단발·막대사탕)가
  오렌지 소다를 밥에 붓고, 식판을 엎음. PYONA가 A를 무에타이 클린치→니킥→
  트립으로, B(흑장발)를 유도 한팔업어치기로 제압. 30초

**REFERENCE BINDING — 5 에셋** (prompt + frame)
- image1=PYONA, image2=B(흑장발·사탕 없음), image3=A(흑단발·사탕),
  image4=식판, image5=오렌지 소다병
- "不得交换A与B身份" — A/B 정체 교환 금지. #24 복제·정체 붕괴의 정면 대응
- 프레임 확인: pyo_02에서 5요소(얼굴·식판·A·소다병·B) 동시 식별 가능.
  A의 막대사탕 흰 막대가 pyo_04까지 유지됨

**ACTION DIFFERENCE LOCK** (prompt-derived)
- A = 무에타이 (클린치→보디 니→턴→아웃사이드 트립)
- B = 유도 (한팔업어치기, over-the-shoulder)
- "A和B的技术绝对不能看起来一样" — 캐릭터별 기술 배타 할당
- pyo_07: A에게 클린치 거는 PYONA 렌더됨. pyo_08: B가 측면에서 어깨를 잡는
  진입 렌더됨

**IMPACT & EXPRESSION RULE — 반응 증거 메뉴** (prompt-derived)
- 모든 접촉은 13개 항목 중 2–3개를 써서 반응: 어깨 압축·관성 이동·빠른 눈깜빡임·
  호흡 중단·빠른 흡기·짧은 호기·0.5–1초 RECOVERY DELAY 등
- "A和B落地后不能下一帧马上正常站起来" — 다음 프레임에 멀쩡히 일어나기 금지
  (AI 티 정면 저격)
- PYONA도 무적 캐릭터처럼 무반응이면 안 됨 — 맞으면 먼저 영향받고 회복

**CONTINUITY — Hard Lock** (prompt + frame)
- 00:11 이후 PYONA 옷·머리의 음식 얼룩은 마지막 프레임까지 유지.
  "绝对不能突然变干净" (갑자기 깨끗해지면 안 됨)
- pyo_05 (식판 엎은 직후) → pyo_08·pyo_09 (종반)까지 얼룩 지속 확인
- 최종 배치 고정: PYONA 서 있음, A·B 각각 바닥. pyo_09 로우앵글 미디엄
  와이드에서 3인 동시 확인 — 스펙 그대로
- 오렌지 소다는 A만 조작, 식판은 A만 한 손으로 엎음 — 소품 조작권 배타 할당

**마이크로 디렉션** (prompt + frame)
- "不是头先抬。PYONA的眼睛先慢慢向上抬起。然后头部才跟着抬起"
  (고개가 먼저 아님. 눈이 먼저 올라가고 그 다음 고개) — pyo_06에서 렌더됨
- "嘴里的棒棒糖棒也停止晃动" (입속 사탕 막대의 흔들림도 멈춤) — 반응의 증거로
  소품의 미세 움직임을 씀
- 최종 시선 안무: "PYONA先低头看一眼A。然后转头看向B。最后缓慢抬起视线"
  (먼저 A를 내려다보고, B를 돌아보고, 마지막에 천천히 시선을 들어올림) —
  명명된 대상의 시선 시퀀스

**카메라 안티-치트** (prompt-derived)
- "不要用大量快速剪辑隐藏技术。不要用夸张手持摇晃隐藏身体关系"
  (빠른 컷으로 기술을 숨기지 마라. 과장된 핸드헬드로 신체 관계를 숨기지 마라) —
  모델의 치팅 경향을 직접 겨냥한 메타 디렉션

**어댑터 시사점**
- 중국 모델(Seedance)에 중국어 프롬프트 — 같은 크리에이티브 스펙을 모델별
  언어로 컴파일한다는 Adapter 개념의 실전 사례
- 댓글도 이를 확인 ("중국어로 쓰면 Seedance에 더 정확해")

**관찰 vs 추론**
- 관찰(프레임): 5에셋 동시 식별, 사탕 막대 유지, 눈-먼저 리프트, 얼룩 지속,
  최종 3인 배치, A 클린치·B 진입 렌더
- 관찰(프롬프트): 기술 배타 할당, 13개 반응 메뉴, 안티-치트 카메라, 중국어 작성
- 추론: B의 한팔업어치기 전체 궤적(발이탈·어깨 넘김)은 스틸로 확인 불가 →
  스펙 제외

**Production description → Control Levels**
- Hard Lock: 5에셋 바인딩, A/B 정체·기술 배타, 얼룩 지속, 최종 배치,
  30초 비트표, RECOVERY DELAY
- Soft Guidance: 50–70mm 중근경, 한국 청춘영화 질감
- Creative Freedom: 배경 학생들의 반응 디테일

**기여 패턴**: 1 (5에셋 바인딩 + 정체 교환 금지),
  2 (눈-먼저 리프트, 최종 시선 안무 A→B→들어올림),
  3 (ACTION DIFFERENCE LOCK — 캐릭터별 기술 배타 할당),
  5 (안티-치트 네거티브: "갑자기 깨끗해지지 마라", "다음 프레임에 일어나지 마라",
  "컷으로 기술을 숨기지 마라"),
  7 (diegetic 사운드 리스트, NO BGM),
  8 (신규 후보 — 13개 반응 증거 메뉴, 모델별 프롬프트 언어=어댑터)

```yaml
reference_state:
  source: "@pyona_ai / X — ORANGE SODA INCIDENT (30s, Seedance 2.5)"
  evidence_basis: prompt-derived + frame-derived
  format: vertical_9x16_24fps
  prompt_language: chinese_for_seedance # 어댑터 실전 사례
  reference_binding:
    assets: [image1_PYONA, image2_B, image3_A, image4_tray, image5_soda]
    identity_lock: no_A_B_swap
    prop_operation_rights: {soda: A_only, tray_flip: A_single_hand_only}
    lollipop: A_white_stick_throughout # pyo_04 확인
  action_difference_lock:
    A: muay_thai_clinch_knee_turn_trip
    B: judo_ippon_seoi_nage
    rule: techniques_must_not_look_alike
  impact_expression_rule:
    reaction_menu_13_items: [shoulder_compression, inertia, blink, breath_cut,
      quick_inhale, short_exhale, recovery_delay_0.5_1s]
    min_items_per_contact: 2_to_3
    no_instant_getup: true
    pyona_not_invincible: brief_impact_then_recover
  continuity:
    food_stains_persist_from_00:11_to_last_frame: true # pyo_05→pyo_09 확인
    final_positions: {PYONA: standing_center, A: floor_side, B: floor_side}
    final_framing: low_angle_medium_wide_three_shot # pyo_09 확인
  micro_direction:
    eyes_lift_before_head: true # pyo_06 확인
    lollipop_stick_stops_shaking: reaction_evidence
    final_gaze_choreography: [look_down_at_A, turn_to_B, slowly_lift_gaze]
  camera_anti_cheat: [no_fast_cut_hiding_technique, no_shaky_cam_hiding_body_relation]
  dialogue: {A: "맛있게 먹어.", B: "…뭐야?", PYONA: silent_throughout}
  control_levels:
    hard_lock: [5_asset_binding, AB_exclusive_tech, stain_persistence,
      final_positions, 30s_beats, recovery_delay]
    soft_guidance: [50_70mm_closeups, k_youth_film_texture]
    creative_freedom: [background_students_reaction_detail]
```

---

## 27. @darkjl81 (堂島の龍) — 흰색 포니 한밤 다운힐 (프롬프트 표본)

**기본 정보**
- 출처: Threads @darkjl81, 게시 2026-09-24 22:32 (약 7시간 전)
- 형식: **정지 이미지 1장 + 프롬프트 전문** (영상 없음 — 첨부 이미지도 CDN 만료로
  미확인). 댓글에 프롬프트 전문이 한국어로 공개됨
- 모델명 미표기. "Prompt by SENIORBEAR · 공유/사용 시 출처 표기"
- 증거 기반: prompt-derived (author-described). 프레임 분석 불가
- 사용자 코멘트: "내가 원하는 만화스타일. 실사 스타일이고 컷 나누기가 다양해서
  박진감" — 실제 스타일은 **만화 문법을 100% 실사로 재현**하는 것.
  "만화 그림으로 만들지 않는다. 만화의 컷 분할과 카메라 연출만 실사 영화로
  재현한다"

**핵심 — 만화식 컷 문법의 실사 컴파일** (prompt-derived)
- CUT 1–9 명시적 스토리보드:
  1. 흰 포니가 헤어핀에 접근 (와이드)
  2. 운전자 얼굴 극클로즈업 (냉정)
  3. 눈만 보이는 초극단 클로즈업 (apex 응시)
  4. 기어 레버 조작 손 클로즈업
  5. 페달 조작 발 클로즈업
  6. 스티어링 휠 돌리는 손
  7. 헤드램프 켠 포니, 헤어핀 진입하며 롤링 (와이드)
  8. 다시 얼굴 클로즈업 (가로등 빛이 스침)
  9. 뒤 미끄러지며 헤어핀 탈출 (외부 와이드)
- 박진감의 원천: 샷 내부 모션이 아니라 **컷의 리듬** —
  와이드(상황) ↔ 극클로즈업(신체 부위)의 교대. 만화의 "긴박한 순간 얼굴
  클로즈업 삽입" 문법을 그대로 가져옴
- Storyboard-first의 실전 표본: 프롬프트 자체가 스토리보드

**시선** (prompt-derived)
- "눈동자는 카메라를 보지 않는다. 다음 헤어핀의 apex와 진입점을 정확하게
  계산하듯 전방을 응시한다" — 카메라 응시 금지 + 명명된 대상(apex·진입점)에
  고정. 계산하는 눈빛이라는 정서 지정까지
- 동공·홍채에 도로 조명과 계기판 불빛이 작게 반사 — 시선 대상의 증거를
  눈 안에 심음

**정체성 + 미화** (prompt-derived)
- "첨부 사진 속 바로 그 사람이 영화 주연배우급으로 가장 잘생겨 보이는 모습"
  — 정체 유지와 미화의 결합 스펙. 그대로 복사가 아니라
  "그 사람의 베스트 버전"
- "다른 AI 미남으로 교체하지 않는다" — 정체 드리프트 방지
- 피부색은 원본 사진을 복사하지 않고 야간 조명 환경에 맞춰 "자연스럽게
  재계산" — 레퍼런스 붙여넣기 방지

**조명 안무** (prompt-derived)
- 스튜디오 조명 금지. 야간 차량 실내의 실제 광원만: 계기판의 따뜻한 빛
  (아래에서), 달빛·가로등 (측면)
- 가로등을 통과하는 찰나 빛의 띠가 눈→콧날→광대→입술→턱 위로 스침 —
  얼굴을 가로지르는 빛의 타이밍을 안무로 지정
- 얼굴 반대쪽 절반은 깊은 그림자 — 강한 명암 대비가 골격과 긴장감 동시 강조

**관찰 vs 추론**
- 관찰(프롬프트): CUT 1–9, 시선 금지·고정, 미화 스펙, 조명 안무, 실사 100% 선언
- 미확인: 첨부 이미지 만료로 렌더 결과 확인 불가, 영상 없음
- 추론: 없음

**Production description → Control Levels**
- Hard Lock: CUT 1–9 순서, 얼굴이 화면 65–80%, 실사 100% (애니메이션 금지),
  정체 유지
- Soft Guidance: 야간 실내 광원만, 눈→턱 빛 스윕
- Creative Freedom: 가로등 간격·밝기 디테일

**기여 패턴**: 2 (시선 — 카메라 금지 + apex 고정 + 눈 속 반사),
  3 (컷 문법 — 만화식 삽입 클로즈업의 실사 컴파일, CUT 1–9 스토리보드),
  5 (네거티브 — "애니메이션 얼굴 금지", "다른 AI 미남으로 교체 금지",
  "스튜디오 조명 금지"),
  8 (신규 후보 — "그 사람의 베스트 버전" 정체+미화 결합 스펙,
  피부톤 재계산)

```yaml
reference_state:
  source: "@darkjl81 / Threads — white Pony midnight downhill (prompt specimen)"
  evidence_basis: prompt-derived # 영상 없음, 첨부 이미지 만료
  style: manga_shot_grammar_compiled_to_photoreal
    # 만화 그림이 아니라 만화의 컷 분할+카메라 연출을 실사로
  storyboard: CUT_1_to_9
    rhythm: wide_action_alternating_extreme_closeups
    closeup_subjects: [face, eyes_only, gear_hand, pedal_feet, steering_hands]
  subject:
    gaze: never_at_camera_locked_on_apex # 다음 헤어핀 apex·진입점 계산
    gaze_evidence: road_and_dashboard_light_reflected_in_iris
    identity: attached_photo_recognizable
    beautification: best_version_of_that_person # AI 미남 교체 금지
    skin_tone: recalculated_for_night_lighting # 원본 복사 금지
  light_choreography:
    sources: [dashboard_warm_from_below, moonlight_and_streetlamps_side]
    sweep: streetlight_band_across_eyes_nose_cheek_lips_chin
    contrast: half_face_in_deep_shadow
  control_levels:
    hard_lock: [cut_1_to_9_order, face_65_80_percent, photoreal_100, identity]
    soft_guidance: [diegetic_night_sources_only, light_sweep]
    creative_freedom: [streetlamp_interval_detail]
```

---

## 28. @woko_0o0 — WEKA2 vs YAYUK 해상 대결투 (30초)

**기본 정보**
- 출처: Threads @woko_0o0, 게시 2026-09-25 (약 3시간 전)
- 프롬프트: 구글독스 공개 문서 "SEEDANCE 2.5 30s" (**인도네시아어**)
- 생성: Seedance 2.5, 30초, 16:9, 3D 중국 애니메이션 시네마 스타일
- 증거 기반: prompt-derived (Google Doc 전문 확보)
- **영상은 로그인 월 뒤라 미확인** — 프레임 분석 불가. 사용자 질문
  ("시선이나 캐릭터들의 방향이 조금 이상해")에 대한 프롬프트 차원의 분석만 수행

**컨셉** (prompt-derived)
- WEKA2 (25세 남성 검객, 청금색 검기, 400m Divine Sword Avatar 소환) vs
  YAYUK (여성 수계 cultivator, 900m Mystic Water Dragon)
- 새벽의 거대 해협, 수천 미터 석교. 구름→해면→부서진 석교→상공으로
  이어지는 전투 회로

**데미지 연속성 — 상태 전이 체인** (prompt-derived)
- 아바타 왼팔의 데미지 아크: 멀쩡 → 용에게 물림 (09.50–10.25, 아머가 안으로
  휘어짐) → 어깨가 뒤로 밀림 (10.25–11) → 심하게 금감 (21.25–22.25) →
  **왼팔이 분리되어 바다에 추락** → 최종 (28–30) "왼팔이 없는 채로 손상된
  아바타"
- "Kerusakan pada lengan kiri dan armor harus tetap terlihat pada shot
  berikutnya" (왼팔과 아머의 손상은 다음 샷에서도 보여야 함)
- "No unexplained reset of damage" — #8의 상태 전이 체인을 데미지에 적용

**스케일 락** (prompt-derived)
- 아바타 400m, 용 900m 명시. "No shrinking or enlarging of the giant entities"
- WEKA2는 화면 좌하단 모서리에 "tiny"하게 — 스케일 대비를 연출로 씀

**싱크로나이즈 락** (prompt-derived)
- "The avatar synchronizes perfectly with WEKA2's movement"
- "The giant sword follows exactly the same diagonal trajectory" —
  조종사-아바타 동기화. 작은 검의 궤적 = 거대 검의 궤적

**속도 규율** (prompt-derived)
- 0.25초 슬로모션은 임팩트 순간에만 허용, "Immediately return to normal speed"
- 충돌점에 2프레임 흑백 붓터치식 임팩트 플래시 — 만화식 충격 연출 (#27 계열)
- #19의 "슬로모 금지"와 대비: 여기는 0.25초 윈도우로 허용

**사용자 질문에 대한 분석 — 시선·방향**
- 프롬프트는 **이동 방향을 샷마다 지정**함 (WEKA2는 좌후방에서 대각선으로,
  YAYUK는 우후방에서 추격 등). CONTINUITY RULE에도 "direction of movement"
  명시
- 그러나 **마스터 스크린 방향 축이 없음**: "WEKA2는 항상 화면 좌측" 같은
  전역 기준 없이 샷별 방향만 나열 → 각 샷은 локально 맞추면서 전체 방향이
  깨질 수 있음. 30초에 약 40샷(평균 0.75초/샷)이라 방향 연속성이 가장
  깨지기 쉬운 구조
- **시선 타겟 지정 전무**: 누가 누구를 보는지 한 번도 안 나옴. 고속 공중전이라
  이동 방향이 시선을 대신한다고 가정한 듯 — "시선이 이상해"라는 느낌의
  유력한 원인. #12·#23·#26식 명명 시선이 있었다면 달랐을 것
- 처방 후보: 마스터 축 선언 (WEKA2=화면 좌, YAYUK=화면 우, 용은 시계방향
  회전) + 주요 비트의 시선 타겟 명명

**모델 특화 네거티브** (prompt-derived)
- "No artificial or strange Seedance-generated vocal sounds" —
  Seedance가 이상한 보컬음을 만들어내는 known artifact를 직접 겨냥
- NO DIALOGUE / NO MUSIC / NO TEXT / NO LOGO / NO WATERMARK

**환경 회로** (prompt-derived)
- 구름 → 해면 → 부서진 석교 → 상공. 명명된 장소 노드의 이동 회로 —
  #24 교훈(비트별 장소 앵커)의 긍정 사례
- 최종 프레임: "산 붕괴·해양 충격·구름 파열이 동시에 일어나는 절대 정점" —
  해결이 아니라 정점에서 끝내기

**관찰 vs 추론**
- 관찰(프롬프트): 데미지 아크 5단계, 스케일·싱크 락, 0.25초 슬로모 윈도우,
  시선 타겟 전무, 마스터 축 전무, 약 40샷
- 미확인: 영상 미확인으로 실제 렌더의 방향 붕괴 여부 확인 불가
- 추론: "시선이 이상해"의 원인이 프롬프트의 시선 미지정 때문이라는 단정 불가 →
  스펙 제외 (영상 확인 후 판정)

**Production description → Control Levels**
- Hard Lock: 데미지 아크, 스케일, 싱크로나이즈, 40샷 비트표, 노 다이얼로그
- Soft Guidance: 새벽 해협, 청금 vs 심청 에너지 대비
- Creative Freedom: 물보라·파편 디테일

**기여 패턴**: 1 (캐릭터 락 + 데미지 상태 전이),
  3 (싱크로나이즈 락 — 조종사와 아바타의 궤적 일치),
  5 (모델 특화 네거티브 — Seedance 보컬음),
  8 (신규 후보 — 마스터 스크린 방향 축: 샷별 방향만으로는 부족하다)

```yaml
reference_state:
  source: "@woko_0o0 / Threads — WEKA2 vs YAYUK sea battle (30s, Seedance 2.5)"
  evidence_basis: prompt-derived # 영상은 로그인 월 뒤 — 미확인
  prompt_language: indonesian_in_google_doc
  style: 3D_chinese_animation_cinema
  characters:
    WEKA2: [male_25_swordsman, blue_gold_energy, 400m_divine_sword_avatar]
    YAYUK: [female_water_cultivator, dark_blue_energy, 900m_water_dragon]
  damage_arc: # Hard Lock — 상태 전이 체인
    [intact, bitten_left_forearm, shoulder_pushed_back,
     heavily_cracked, arm_severed_falls_to_ocean, missing_in_final]
  scale_lock: [avatar_400m, dragon_900m, no_rescaling]
  sync_lock: avatar_mirrors_weka2_trajectory_exactly
  speed_discipline:
    slow_motion: 0.25s_only_at_impact_then_normal
    impact_flash: 2_frames_bw_brush_stroke
  direction_design:
    per_shot_directions: specified # 매 샷 이동 방향 지정
    master_screen_axis: absent # 전역 기준 없음 — 붕괴 가능 지점
    gaze_targets: absent # 시선 지정 전무 — 사용자 지적의 유력 원인
  environment_circuit: [clouds, sea_surface, broken_arch, back_to_sky]
  final_frame: peak_of_simultaneous_collapse # 해결이 아닌 정점
  model_specific_negative: no_seedance_generated_vocal_sounds
  control_levels:
---

## 29. AI Shot Studio — 42 Camera Movements (카메라 움직임 프롬프트 모음)

**기본 정보**
- 출처: aishotstudio.com "42 Camera Movements for AI Video Prompts: The Ultimate List"
- 게시: 2026-09-14
- 증거 기반: article-described (기사 전문 확보). 각 무브마다 1~2줄 영어 프롬프트 문구 제공

**전체 구조** (article-derived)
42개를 계열별로 분류하면: 돌리계 (Slow Dolly In/Out, Fast Dolly In, Vertigo Effect),
줌계 (Extreme Macro Zoom, Cosmic Hyper Zoom, Smooth Optical Zoom In/Out, Snap Zoom),
포커스계 (Rack Focus, Reveal from Blur), 수평계 (Truck Left/Right, Tilt Up/Down),
오르빗계 (Orbit 180/360, True Orbit 180/360 [Seedance 1.5 Pro], Slow Cinematic Arc),
수직계 (Pedestal Up/Down, Crane Up/Down), 드론계 (Drone Fly Over, Epic Drone Reveal,
Large Scale Drone Orbit, Top Down, FPV Drone Dive), 트래킹계 (Leading/Backward,
Following/Forward, Side Tracking, POV Walk, Hyperlapse), 특수계 (Barrel Roll,
Bullet Time, Worm's Eye Tracking), 렌즈·프레이밍 (Fisheye, OTS, Reveal from Behind,
Through Shot, Handheld Documentary, Whip Pan, Dutch Angle)

**관찰 — 좋은 점** (article-derived)
- Dolly vs Optical Zoom 분리: "Slow dolly in (카메라가 앞으로)" vs
  "Smooth optical zoom in (렌즈만 확대, 카메라는 정지)". 돌리는 패럴랙스,
  줌은 압축 — 물리적으로 다른 연출이 정확히 구분됨
- True Orbit 180/360에 Seedance 1.5 Pro 태그 — 특정 무브가 특정 모델에서
  테스트됐다는 표시
- FPV Drone Dive, Barrel Roll, Bullet Time 같은 난이도 높은 무브 포함

**관찰 — 문제점** (inference가 아니라 기사 텍스트와의 비교 분석)
- 명칭 오류: "Tilt Up, camera pans vertically" — 틸트인데 팬이라 부름.
  "Reveal from Behind — Wipe movement" — 와이프는 트랜지션(컷)이고
  이건 lateral reveal. "Rack Focus — start completely out of focus" —
  시작 프레임이 완전 블러인 건 focus pull이지 랙 포커스(피사체 간 포커스 이동)가 아님
- 움직임이 아닌 항목: Fisheye or Peephole Lens (렌즈), Over the Shoulder (프레이밍),
  Worm's Eye Tracking (앵글+트래킹)
- 중복: "Orbit 180 (Spin)"과 "True Orbit 180 [Seedance 1.5 Pro]"가 같은 무브를
  두 번 기재. Smooth Optical Zoom In/Out도 dolly 항목과 문구만 다르고 유사
- 문구가 1줄 수준: 대부분 "Slow dolly in, camera moves slowly forward toward the subject"
  — 시작 프레임→끝 프레임, 속도(초당 비율), 앵커(누구를 따라가며) 미지정

**관찰 vs 추론**
- 관찰(기사): 42개 항목, 각 1~2줄 문구, Seedance 1.5 Pro 태그 2개,
  dolly/zoom 분리, 명칭 오류 3건, 비-움직임 항목 4건, 중복 3건
- 추론: 이 문구 그대로 생성하면 모델이 무브를 약하게 해석할 가능성 → 스펙 제외
- 미확인: 실제 렌더 예시 영상 없음 — 각 무브의 실제 작동 여부 검증 불가

**Production description → Control Levels**
- Hard Lock: start_frame, end_frame, speed_percent_of_clip,
  anchor_subject (돌리가 누구를 향해/오르빗이 누구를 중심에)
- Soft Guidance: 무브의 드라마틱 목적 (urgent/reveal/disorienting)
- Creative Freedom: 이 기사 문구 자체의 1줄 버전

**기여 패턴**: 6 (절제 — 무브도 Motion Budget 대상), 2 (상대 좌표 —
  오르빗/트래킹의 앵커는 인물 기준), 8 (신규 후보 — Camera DNA:
  돌리/줌/포커스/오르빗/드론/트래킹 6계열 무브 어휘표. 단, 각 문구는
  start→end+속도+앵커의 확장 문법이 필요)

```yaml
reference_state:
  source: "AI Shot Studio — 42 Camera Movements for AI Video Prompts (2026-09-14)"
  evidence_basis: article-derived # 기사 전문, 예시 영상 없음
  move_families: [dolly, zoom, focus, lateral, orbit, vertical, drone,
                  tracking, special, lens_framing]
  strengths: [dolly_vs_optical_zoom_separated, seedance_tested_tag_on_orbits,
              aggressive_moves_included]
  defects:
    naming_errors: [tilt_called_pan, wipe_misnamed_lateral_reveal,
                    rack_focus_misdefined_as_blur_to_sharp]
    not_movements: [fisheye_lens, ots_framing, worms_eye_angle]
    duplicates: [orbit_180_twice, zoom_in_repeated_as_dolly]
    under_specified: all_42 # start/end/속도/앵커 없음
  needs: [start_frame, end_frame, speed_percent_of_clip, anchor_subject]
  control_levels:
    hard_lock: [start_end_frames, speed, anchor]
    soft_guidance: [dramatic_purpose]
    creative_freedom: [one_line_phrase_variant]
```

---

## 30. X @Diplomeme — "A day with all new iPhone 18 Pro Max" (30초, Seedance 2.5 on OpenArt)

**기본 정보**
- 출처: X @Diplomeme, 게시 2026-09-25. 트윗에 프롬프트 전문 공개
- 생성: Seedance 2.5 on @openart_ai, 30초, 16:9 (1280x720, 24fps)
- 증거 기반: prompt-derived (프롬프트 전문) + **frame-derived (12프레임 분석)**
- 장르: 가상 제품(iPhone 18 Pro Max, 버건디) 상업 광고 — 제품 자체는 존재하지 않음

**구조 — 마스터 스펙에 가장 가까운 케이스** (prompt-derived)
- 12비트 비트표, 2.5초 간격 (00:00–02.5 CLOSE-UP HOOK ... 27.5–30 FINAL REVEAL)
- 각 비트마다 렌즈 명시: 85mm (훅·클로즈업), 24mm (랜드스케이프·무브먼트),
  35/50mm (휴먼 모먼트)
- 독립 섹션: CAMERA / VISUAL-COLOR / MOTION / LIGHTING / AUDIO /
  REALISM / BRAND CONTROL / EDITING / CONTINUITY / FINAL QUALITY TARGET

**관찰 — 12프레임 전부 비트표와 1:1 매칭** (frame-derived)
- f1(01s)=훅 (창가 버건디 아이폰 클로즈업, 손이 프레임으로 들어옴),
  f3.75=아침 촬영, f6.25=무브먼트 (교차로 추적), f8.75=스트리트 라이프
  (증기 전경), f11.25=휴먼 모먼트 (카페 초상), f13.75=랜드스케이프 리빌
  (돌계단→계곡), f16.25=프로덕트 모먼트 (골든아워 실루엣),
  f18.75=액션 캡처 (폰 화면 속 모션블러 열차), f21.25=나이트 전환 (등불 거리),
  f23.75=로우라이트 (강변 스카이라인), f26.25=시티 에너지 (화면 빛 받는 얼굴),
  f29=파이널 리빌 (강변 뒷모습+야경)
- 캐릭터 일관성 12프레임 유지: 브라운 웨이브 헤어, 차콜 오버셔츠, 크로스백,
  버건디 폰. 의상·헤어·소품 불일치 없음
- 시간대 아크 확인: 아침 햇살 → 낮 → 골든아워 → 블루아워 → 밤
  ("daylight → golden hour → blue hour → night" 지시 렌더됨)

**관찰 — 폰 화면 = 인월드 카메라 장치** (frame-derived)
- f3.75·f11.25·f18.75에서 폰 디스플레이가 화면 안의 화면으로 등장.
  "Cut briefly to the phone display showing the same scene being framed"
  지시가 그대로 렌더됨
- 디스플레이는 프레이밍 장치이자 일관성 치트: 모델이 같은 장면을 두 번 그림
- f18.75 열차 샷에서 디스플레이 속 창문에 모션블러 — 화면 안 화면에도
  블러가 전파됨

**관찰 — 실패 2건** (frame-derived)
- (1) UI 난독 텍스트: f3.75 폰 UI에 "VERDO, PRMTTT, PSTENHES" 같은
  무의미 텍스트. BRAND CONTROL에 "Do not add ... random UI"가 있었으나
  Seedance가 그대로 렌더. **네거티브가 실패를 예측했으나 막지 못한 케이스**
  (#14·#25의 난독 텍스트 계열)
- (2) 카페 씬 디스플레이 불일치: f11.25 폰 속 초상은 수염 없는 문신 남자인데
  옆의 실제 인물은 수염 남. 화면 안 초상의 정체가 주변 인물과 안 맞을 가능성
  — 디스플레이 콘텐츠의 정체 검증 필요 지점

**시선 (eye-line)**
- 12프레임 전체에서 카메라 직시 0회. 문법: 뒷모습 추적(f6.25·f13.75·f21.25·f29)
  + 옆모습(f16.25·f23.75) + 폰 응시(f8.75·f26.25)
- **화면을 시선 타겟으로 쓰는 구조**: "traveler → 폰 화면 → 장면"의 삼각형.
  #26의 명명 시선과 달리, 여기서는 오브젝트(폰)가 시선의 목적지
- 유일한 인물 간 시선: 카페 휴먼 모먼트 — traveler가 현지인을 찍고
  상대가 자연스럽게 웃음 (양방향, 카메라 개입 없음)

**관찰 vs 추론**
- 관찰(프롬프트+프레임): 12비트 1:1 렌더, 렌즈별 비트 설계, 캐릭터 일관성,
  시간대 아크, 폰 화면 장치 3회, UI 난독 2프레임, 카페 정체 불일치 가능
- 미확인: 음악 동기화 ("Cut precisely with the music") — 무음 프레임 분석이라
  검증 불가
- 추론: 폰 화면 장치가 비트표를 지키게 도운 건지는 단정 불가 → 스펙 제외

**Production description → Control Levels**
- Hard Lock: 2.5초 비트표, 비트별 렌즈(mm), 캐릭터 의상·소품 명세,
  시간대 아크, "camera slowly moves backward rather than flying upward"
- Soft Guidance: 비트별 장소 노드, 컬러그레이드, 불완전 프레이밍
- Creative Freedom: 군중·벤더 디테일

**기여 패턴**: 1 (캐릭터+소품+시간대 3중 락),
  2 (신규 — 렌즈 mm를 카메라 설계 언어로: 비트별 85/24/35/50 선언),
  5 (실패 기반 네거티브: "no warped phone geometry, no changing camera system,
  no random UI" — UI는 막지 못함, 한계 데이터),
  6 (불완전성 지시: imperfect framing, autofocus adjustment, exposure
  adaptation — 리얼리즘의 신호로 불완전성을 씀),
  8 (신규 후보 — 인월드 모니터: 폰 화면을 화면 안 카메라로 쓰는 장치.
  anti-cheat 지시 "flying upward 금지·backward dolly 명시"는 #26 계열)
```

---

## 31. Threads @mylady_haneulbit (하늘빛) — 도서관 unresolved chemistry (Seedance 2.5 via Pollo AI)

**기본 정보**
- 출처: Threads @mylady_haneulbit (하늘빛 🩵, "AI Threads"), 게시 2026-09-24 17:00
- 포스트: "30 seconds of unresolved chemistry in a library. Created with Pollo AI × Seedance 2.5 × 480FPS"
- 프롬프트: 고정 댓글에 전문 공개 (영어)
- 생성: Pollo AI × Seedance 2.5. **실제 영상 길이 37초** (캡션은 30초) —
  Pollo AI가 비트표를 늘려 렌더
- 증거 기반: prompt-derived (프롬프트 전문) + author-described (캡션) +
  **frame-derived (5개 타임스탬프 스크린샷: 3s·8s·13s·18s·23s)**

**컨셉** (prompt-derived)
- Surya (남, 이미지2 얼굴 참조, 은발 투톤, 브라운 틴트 선글라스,
  회색 수트, 목·팔 문신) × My Lady (여, 이미지1 얼굴 참조,
  적갈색 웨이브 헤어, 블랙 오프숄더, 샴페인 새틴 스커트)
- 헤어진 연인의 재회: 같은 책 → 책을 위로 듦 → 대치 → 책을 건넴 →
  카베돈 → almost kiss (키스는 안 함)

**관찰 — 시선 사다리 (gaze ladder)** (frame-derived + prompt-derived)
- 5프레임 전체에서 카메라 직시 0회. 시선은 오직 두 인물 사이와 책을 오감
- 3s: 둘이 같은 책을 봄 (공동 시선 — 명명 대상은 "the SAME book")
- 8s: 여자가 올려다보고 남자가 내려다봄 (상호 시선, 카베돈)
- 13s·18s: 얼굴이 가까워진 상태의 상호 응시
- 23s: 몇 인치 거리의 face-to-face eye contact
- 프롬프트의 종결: 여자가 천천히 눈을 감음 → **시선 강도로 감정을
  고조시키고 눈 감기로 종결**. 비트 자체가 시선 에스컬레이션으로 설계됨
  ("follows the book with her eyes" → "looks directly up" →
  "maintains eye contact" → "closes her eyes")

**관찰 — 프레이밍 케이지** (prompt-derived + frame-derived)
- "ALL SHOTS MUST BE HALF-BODY / MEDIUM CLOSE-UP OR CLOSE-UP.
  NO FULL BODY. NO WIDE SHOTS. NO ESTABLISHING SHOTS."
- 5프레임 전부 하프바디~클로즈업. 전신 0회
- **전신 해부학 실패를 카메라 구도로 회피** — 모델의 약점을
  프레이밍 하드락으로 우회 (#12 카메라 응시 규칙의 프레이밍 버전)

**관찰 — 전이 체인 (romance blocking)** (prompt-derived)
- 카메라 규칙에 물리적 전이 13단계 명시:
  reach → touch book → lift book → turn body → lower book →
  hand book over → step backward → bookshelf contact →
  Surya steps forward → lean downward → eye contact → approach →
  eyes close → almost kiss
- "No teleporting. No instant pose changes. No floating hands.
  No unnatural weight transfer." — #24의 공간 붕괴를 겨냥한
  인터랙션 전용 네거티브
- "He places one hand against the bookshelf beside her head,
  NOT touching her body" — 비트 안에 박힌 네거티브

**관찰 — 책 = 연속성 토큰** (prompt-derived + frame-derived)
- "the SAME book" 반복, 네거티브에 "disappearing book, changing book,
  floating book". 5프레임 중 4프레임에서 책이 손에/위에 있음
- 단일 소품을 서사의 척추로 — #10의 소품 락을 내러티브로 승격

**관찰 — 이상 2건** (frame-derived)
- (1) 길이 불일치: 캡션 30초, 실제 37초. 프롬프트 비트표(0–6–11–16–21–25–30)
  대비 실제 전개가 빠름 — 8s 프레임에 이미 카베돈 (프롬프트상 21–25s 비트).
  **모델이 비트 순서는 지켰으나 타임스탬프는 압축**. 비트표의 절대 시간은
  보장되지 않는다는 데이터
- (2) Pollo.ai 워터마크 좌상단 번인 — 네거티브에 "watermark"가 있었으나
  무력화 (#21 Dola AI, #25 Wavespeed와 동계열. 플랫폼 워터마크는
  프롬프트로 못 지운다)

**관찰 vs 추론**
- 관찰(프롬프트+5프레임): 시선 사다리 5단계, 프레이밍 케이지 유지,
  전이 체인 13단계, 책 연속성, 37초 실측, 워터마크 번인
- 미확인: 28s 프레임 (캡처 실패) — almost kiss 종결 프레임 미확인.
  대사 립싱크 (인도네시아어) — 정지 프레임이라 검증 불가
- 추론: Pollo AI의 480FPS 표기가 실제 렌더에 미친 영향 → 스펙 제외

**Production description → Control Levels**
- Hard Lock: 하프바디 이상 프레이밍 금지, 전이 체인 13단계,
  시선 사다리 (공동→상호→eye contact→눈 감음), "같은 책" 토큰,
  no kiss / no lip contact
- Soft Guidance: K-드라마 핸드헬드, 웜 골든아워 도서관, 이미지 참조 3종 분리
- Creative Freedom: 서가 디테일, 호흡·눈깜빡임

**기여 패턴**: 1 (이미지 참조 3종 역할 분리 — 얼굴2·얼굴1·환경),
  2 (신규 — 시선 사다리: 감정 고조를 시선 강도 단계로 설계하고
  눈 감기로 종결),
  3 (전이 체인 13단계 — 로맨스 블로킹의 물리적 전이 명시),
  5 (인터랙션 전용 네거티브 — teleporting/floating hands/weight transfer),
  6 (신규 — 프레이밍 케이지: 전신 해부학 실패를 구도 하드락으로 회피),
  8 (신규 후보 — 비트표 절대 시간 불신: 모델이 순서는 지키나
  타임스탬프는 압축한다)

---

## 32. Threads @aiwack_de_gorry (IM-RAHADI ⁰³) — RALLY TANTE DOLA JUNGLE RUN (Dola.com)

**기본 정보**
- 출처: Threads @aiwack_de_gorry (표시명 "AI Threads"/"𝐈𝐌-𝐑𝐀𝐇𝐀𝐃𝐈𝐀𝐍 ⁰³"),
  게시 2026-09-24 23:01
- 포스트 (인도네시아어, 의역): "RALLY TANTE DOLA. 어제 @poncosunarko77가
  Dola용 1분 프롬프트를 줬는데, 궁금해서 그 프롬프트를 Qwen에 넣고
  바꿔봤어. 방금 Dola.com에서 그 1분 프롬프트로 생성해봤는데 꽤 괜찮네"
- 고정 댓글에 프롬프트 전문 공개 (영어)
- 생성: Dola.com (모델명 미표기). 실제 영상 60.3초
- 증거 기반: prompt-derived (전문) + author-described (캡션) +
  **frame-derived (7개 타임스탬프 스크린샷: 4·12·20·30·40·49·56s)**

**관찰 — 프롬프트 파이프라인** (author-described)
- 원본 프롬프트를 **Qwen(LLM)에 넣어 확장** → Dola.com에서 60초 생성.
  LLM이 짧은 프롬프트를 60초 비트 시트로 확장하는 실전 워크플로.
  소맨님 목표 파이프라인(기획→프롬프트)의 축소판이 이미 현장에 있음

**관찰 — 비트표 × 렌즈 문법** (prompt-derived + frame-derived)
- 7비트: 0–8 출발·침투 / 8–16 첫 추월 / 16–25 공중 점프 / 25–35
  박스인 탈출 / 35–45 4대 혼전 / 45–53 강 건너기·거짓 선두 / 53–60 피니시
- 비트마다 렌즈 지시: MACRO (타이어 트레드) / TELEPHOTO (압축 추격) /
  WIDE (정글 스케일). #14의 MASTER BEAT SYSTEM을 60초로 확장한 형태
- 프레임 매핑: 4s 타이어 매크로 → 12s 정글 도로(차 없음) →
  20s 먼지 구름 속 BMW → 30s 캐노피 햇살(차 없음) →
  40s 바위 옆 틈새 주행 → 49s 로우앵글 트래킹 (범퍼 "Tante Dola" 식별) →
  56s 대나무 게이트 (차량 접근 중)

**관찰 — 이상 4건** (frame-derived)
- (1) 차 없는 프레임 2개 (12s 정글 도로, 30s 캐노피 빛). 프롬프트의
  모든 비트에 차가 등장하는데 모델이 환경 B-roll을 삽입. #31의
  타이밍 압축과 함께 "모델이 비트 사이에 숨을 넣는다"는 데이터
- (2) 텍스트 새어듦: 앞유리 문구가 "Tante Donina"로 렌더 (프롬프트는
  도어 "Tante Dola"). 같은 영상에서 범퍼 "Tante Dola"는 정확 —
  텍스트 충실도는 균일하지 않고 인스턴스마다 확률적 (#14 "TEM..." 계열)
- (3) 더블 워터마크: 좌상단 "Arshaka Studio" 로고 + 우하단 "Dola AI".
  프롬프트에 워터마크 네거티브 없음 (#21·#25·#31 동계열, 플랫폼
  워터마크는 막을 수 없다)
- (4) 56s: 대나무 게이트만 보이고 통과 장면은 미포착 — 캡처 시점
  (55.15s)이 피니시 비트(53–60) 초반이라 모델 실패가 아니라 캡처 한계.
  점프 비트(16–25)도 20s 프레임엔 착지 먼지만 — 공중 장면 미확인

**관찰 — 차량 연속성** (frame-derived)
- 20s·40s·49s 프레임에서 연한 파란 BMW E30 실루엣, 펜더 플레어,
  루프 라이트 포드, 머드 얼룩 유지. CONTINUITY LOCK의 시각적 성립 확인.
  네거티브의 "clean cars" 금지 → 전 프레임 머드 유지

**관찰 — 모션 버짓 (역방향)** (prompt-derived)
- "NO SLOW MOTION" 3회 반복 (FORMAT·MASTER·NO 섹션),
  "The camera NEVER stops moving". 전편 하이퍼키네틱 = 모션 버짓의
  역방향 명시. 소맨님이 원하는 만화식 박진감 컷 문법과 가장 가까운
  속도 철학 — 다만 이 영상은 단일 60초 연속 생성이라 컷이 없음
- 시선: 차량 외부 샷만이라 인간 시선 문법 해당 없음 (eye-line N/A)

**관찰 vs 추론**
- 관찰(프롬프트+7프레임): Qwen 확장 워크플로, 7비트×렌즈 문법,
  차 없는 프레임 2개, 텍스트 새어듦 1건, 더블 워터마크, 차량 연속성 유지
- 미확인: 점프 비트 실제 렌더 여부, 피니시 통과 장면 (캡처 한계),
  21:9 아나모픽 실제 출력 비율 (스크린샷으론 미확인)
- 추론: 없음

**Production description → Control Levels**
- Hard Lock: NO SLOW MOTION, 카메라 상시 이동, CONTINUITY LOCK
  (동일 BMW·동일 문구·동일 수트·동일 정글 아침·머드 누적),
  라이벌 차량 근접 추격, 물리적 임팩트 무게감
- Soft Guidance: BBC Earth식 매크로/울트라와이드/텔레포토 렌즈 문법,
  웜 골든아워 + 콜드 그린 정글 컬러그레이드, 아나모픽 플레어
- Creative Freedom: 구체적 추격 배치, 먼지·물보라 양상, 라이벌 차량 디자인

**기여 패턴**: 2 (7비트 렌즈 문법 — 비트마다 MACRO/TELEPHOTO/WIDE를
  명시하는 #14 MASTER BEAT SYSTEM의 60초 확장형),
  3 (차량 CONTINUITY LOCK + 머드 누적 = 데미지 아크의 차량 버전, #28 연계),
  5 (NO SLOW MOTION 3회 반복 — 모션 버짓의 역방향 명시),
  6 (신규 후보 — 모델의 "숨" 삽입: 비트 사이에 차 없는 환경 B-roll을
  끼워넣는다. 타이밍 압축(#31)과 쌍을 이루는 모델 거동 데이터),
  7 (신규 — LLM 프롬프트 확장 워크플로: Qwen으로 짧은 프롬프트를
  60초 비트 시트로 확장한 뒤 생성. 소맨님 파이프라인 목표의 현장 구현)

---

## 33. Threads @jeong_do_ryeong — 타격감 극대화 프롬프트 가이드 + 웨어하우스 격투 (Dola AI)

**기본 정보**
- 출처: Threads @jeong_do_ryeong, 게시 2026-09-25 13:52 KST
  (#8 중력 가이드와 동일 저자 — 한국어 프롬프트 엔지니어링 가이드 연작)
- 포스트 본문: "[프롬프트 엔지니어링 가이드] AI 비디오 타격감 극대화
  액션 씬 연출 및 프롬프트 가이드" (한국어 전문, 영어 예시 문구 포함)
- 댓글 2: 실전 프롬프트 전문 (SCENE CONTEXT ~ POSITIVE LOCKS)
- 생성: Dola AI (프레임 우하단 워터마크로 확인). 실제 영상 10초
- 증거 기반: prompt-derived (가이드 전문 + 실전 프롬프트) +
  **frame-derived (6개 타임스탬프 스크린샷: 1.5·3·5·6.5·8·9.5s)**

**관찰 — 가이드의 핵심 장치** (prompt-derived)
- Universal Action Grammar 10단계:
  SETUP → ACCELERATION → CONTACT → IMPACT PEAK →
  FORCE TRANSFER → REACTION → SECONDARY EVIDENCE →
  CAMERA RESPONSE → AFTERMATH → RECOVERY/SETTLING.
  소맨님 시스템의 Action Grammar·전이 체인(#8)과 독립적으로 수렴한 동일 형식
- Concept Lowering: "강하게 때린다"를 지시하지 말고 관찰 가능한
  시각적 결과로 낮춘다. "추상적 의도 → 충돌 사건 → 운동 변화 →
  피격 반응 → 2차 시각 증거 → 카메라 반응 → 잔여 운동 → 안정화".
  레포의 "Visible evidence first" 원칙과 정확히 일치
- 인과적 카메라 반응: BEFORE IMPACT 안정 → IMPACT 짧은 방향성 jolt →
  AFTER 빠른 감쇠 → SETTLING. "constant camera shake" 금지 —
  카메라 흔들림을 사건에 종속 (Camera DNA의 event-coupled 모션)
- Relational Negative Constraints: "no camera shake" 대신
  "no camera shake **before physical contact**". 조건·관계를 포함한
  네거티브 (#4의 실패 출처 명시 네거티브 후보의 정식화)
- Weight Transfer: 발·하체·중심 이동 명시 ("lead foot remains planted",
  "loses balance as the center of mass shifts backward")
- Optional Impact Hold: 충돌 순간 짧은 visual hold 후 즉시 재개.
  단 "at the exact microsecond" 같은 표현 금지 — 모델의 시간 정밀도
  한계를 아는 **capability-calibrated 언어** (신규 패턴)
- 7원칙: 강함을 직접 말하지 않는다 / 충돌은 시간적 순서를 가진다 /
  원인보다 결과를 보여준다 / 충돌 양쪽의 반응을 고려한다 /
  카메라 반응도 사건에 종속시킨다 / 2차 효과는 증거로만 /
  선택적 연출과 필수 물리 결과를 분리한다

**관찰 — 실전 프롬프트의 장치** (prompt-derived)
- POSITIVE LOCKS 섹션: 네거티브가 아니라 긍정 불변식으로 잠금
  ("Rapid counterattacks occur only after the preceding movement
  has visibly completed" — 반격은 이전 동작 완료 후에만)
- FORMAT MODE: "One continuous shot, the camera does not cut on its own"
  — 모델이 임의로 컷을 넣는 것을 막는 anti-cheat
- OPTICS: "47° field of view" — 구체 수치 하드락
- LOCATION MAP (Foreground/Midground/Background 3층) + FIRST FRAME/BLOCKING —
  #2의 상대 좌표 블로킹과 동계열

**관찰 — 영상 대조** (frame-derived)
- 1.5s: 두 파이터 로우 스탠스 대치 — FIRST FRAME/BLOCKING과 일치
- 3s: 근접 인게이지, 한 명이 숙임 — 접촉 체인 진행
- 5s: 모션 블러 타격 교환, 기둥 근처 — "steel support column" 방향으로
  전개 중
- 6.5s: 한 파이터가 기둥 옆에서 몸을 접음 — "folds slightly around
  the contact" 반응의 시각적 성립
- 8s: 바디샷 교환, 한 명이 리코일 — 반격 타이밍의 인과성 유지처럼 보임
- 9.5s: 기둥 앞 클린치 레인지
- 전 프레임 해부학 파탄 없음 (스틸 해상도 한계 내). Dola AI 워터마크
  우하단 번인 (#21·#25·#31·#32 동계열)

**관찰 — 시선** (frame-derived)
- 전 프레임 두 파이터의 시선은 서로에게 고정 (전투 상호 시선).
  카메라 직시 0회. 격투 장르의 시선 문법 = 상대방 락.
  시선 원칙 "공동 시선은 이름 붙은 동일 목표점"의 전투 버전:
  목표점은 명명된 상대

**관찰 vs 추론**
- 관찰(가이드+프롬프트+6프레임): 10단계 액션 문법, Concept Lowering,
  인과적 카메라 반응, 조건부 네거티브, POSITIVE LOCKS, 반격 인과성,
  웨어하우스·기둥·조명(5600K) 일치, Dola AI 워터마크
- 미확인: Impact Hold 실제 렌더 여부 (스틸로는 불가), 해부학 파탄의
  완전한 부재 (동영상 검증 필요), 가이드 주장의 재현성
- 추론: 없음

**Production description → Control Levels**
- Hard Lock: 10단계 액션 문법 순서, 양쪽 반응(attacker recoil +
  target displacement), 접촉점 명시, 조건부 네거티브,
  continuous shot (no auto-cut), 47° FOV
- Soft Guidance: 5600K 인더스트리얼 조명, muted neutrals 그레이드,
  lateral tracking 카메라, 2차 증거(먼지·의상·파편)
- Creative Freedom: 구체적 타격 조합, 기둥 활용 타이밍, 표정 디테일

**기여 패턴**: 1 (POSITIVE LOCKS — 네거티브가 아닌 긍정 불변식 섹션.
  레퍼런스 역할 분리 다음의 "잠금 표현" 신규 어휘),
  2 (Universal Action Grammar 10단계 — #8·소맨님 시스템과 독립 수렴.
  컨택스트 체인의 정식 명명),
  3 (Concept Lowering — "Visible evidence first"의 가이드급 정식화),
  4 (Relational Negative Constraints — 조건부 네거티브의 정식 문법),
  5 (인과적 카메라 반응 — event-coupled jolt + rapid decay),
  6 (신규 — capability-calibrated 언어: "at the exact microsecond" 금지처럼
  모델의 정밀도 한계를 아는 표현 선택),
  7 (신규 후보 — "the camera does not cut on its own": 모델의 임의 컷 삽입
  방지 anti-cheat)

---

## 34. Threads @jeong_do_ryeong — "드럼을 치라고 시켜봤다" (Dola AI)

**기본 정보**
- 출처: Threads @jeong_do_ryeong, 게시 2026-09-25 01:39 KST
- 포스트 본문: "드럼을 치라고 시켜봤다"
- 댓글에 프롬프트 전문 공개 (영어, 3-Phase 구조)
  > ⚠️ 정정 (Claude, 2026-09-26): 게시물 확인 결과 캐러셀은 10.215s + 10.111s (둘 다 1280×720)이고, 이 항목은 영상1만 분석했다. 참고로 Grok 카드 `practice-drumcam-lt`가 분석한 3.34s 9:16 직캠은 "관련 스레드"에 있는 다른 사용자(@drum_minjeong)의 영상이다. 이 항목의 분석 대상이 맞다. evidence E1.
- 캐러셀 2개 영상 (각 10초, 24fps, 1280×720). 영상1 직접 다운로드 성공 —
  이번엔 CDN 서명이 살아 있었음
- 증거 기반: prompt-derived (전문) + author-described (캡션) +
  **frame-derived (영상1에서 6프레임 추출: 1.5·3·5·6.5·8·9.5s)**

**관찰 — 임팩트 문법을 비전투 도메인에 이식** (prompt-derived + frame-derived)
- 프롬프트는 #33의 타격 문법을 드럼 연주에 적용한 3-Phase:
  Phase 1 타격 시퀀스 개시 (전신 체중 이동, 스틱 가속) →
  Phase 2 접촉 순간 impact peak (심벌 진동, 카메라 jolt) →
  Phase 3 탄성 리바운드 (손목이 반동 흡수, 머리카락·의상 반응)
- 6.5s 프레임: 양쪽 크래시 심벌이 눈에 띄게 기울어 진동 중
  (왼쪽은 아래로, 오른쪽은 위로) — "immediate, violent physical
  oscillation across the metal surface"의 시각적 성립
- 8s 프레임: 스틱을 높이 든 채 머리카락이 위로 흩날림 —
  "hair reacts elastically to momentum and body rotation" 성립
- 9.5s: 오른 스틱이 머리 위로, 왼 스틱은 중간 동작 —
  "rapid alternating strikes"
- **#33의 Universal Action Grammar가 도메인 템플릿으로 작동한다는
  증거**: 접촉→반응→2차 증거 체인이 격투가 아닌 연주에도 그대로 이식됨

**관찰 — 경계 유지 (boundary lock)** (prompt-derived)
- "Preserve distinct physical boundaries between the hands, drumsticks,
  drumheads, and cymbals at all times."
- #33 가이드의 "주먹과 얼굴이 융합됨"을 사물 버전으로 확장: 손·스틱·
  드럼헤드·심벌의 물리적 경계 유지. 6프레임 모두 손과 스틱 분리 유지
- 손가락 해부학 하드락: "Both hands maintain five anatomically correct,
  clearly separated fingers in a firm grip throughout the shot."
  (스틸 해상도로 5개 손가락 개수 검증은 불가 — 미확인으로 기록)

**관찰 — 반(反)로봇 불규칙성** (prompt-derived)
- "Avoid perfectly smooth, identical, or robotically synchronized motion.
  ...subtle irregular timing." — 불완전함을 리얼리즘으로 (#30 계열)

**관찰 — 시선** (frame-derived)
- 전 프레임 드러머 얼굴이 머리카락·그림자에 가림. 시선 검증 불가 (N/A)

**관찰 vs 추론**
- 관찰(프롬프트+6프레임): 3-Phase 이식, 심벌 진동·머리카락 반응 성립,
  손-스틱 경계 유지, Dola AI 워터마크 우하단, 35mm·얕은 심도·
  고대비 콘서트 스포트라이트 조명 일치
- 미확인: 손가락 5개 개수 (스틸 한계), 영상2 (캐러셀 두 번째) 내용,
  카메라 jolt의 실제 렌더 (스틸 불가)
- 추론: 없음

**Production description → Control Levels**
- Hard Lock: 3-Phase 순서, 손가락 해부학, 손·스틱·드럼·심벌 경계 유지,
  single continuous shot, 반로봇 불규칙성
- Soft Guidance: 60fps·35mm·얕은 심도, 고대비 콘서트 스포트라이트,
  impact 순간 directional camera jolt
- Creative Freedom: 연주 패턴, 머리카락·의상 반응 양상

**기여 패턴**: 1 (신규 — boundary lock: 손/도구/타격 대상의 물리적 경계
  유지를 명시. 해부학 파탄 방지의 사물 버전),
  2 (#33 문법의 도메인 이식 증거 — 임팩트 문법이 격투→연주로 이식됨),
  3 (반로봇 불규칙성 — subtle irregular timing을 명시하는
  imperfection-as-realism)

---

## 35. Threads @jeong_do_ryeong — "AI 비디오 유체 역학: 부력 구현 및 제어 명세" (Dola AI)

**기본 정보**
- 출처: Threads @jeong_do_ryeong, 게시 2026-09-21 07:13 KST
- 포스트 본문: 한국어 프롬프트 엔지니어링 가이드 (부력 Buoyancy)
- 작성자 댓글에 가이드 전문: 물리적 정의 → AI 오류 분류 →
  4대 원칙 → Before/After 예시 2개
- 영상: ~10초 수중 다이버 클립 (24fps, 1280×720). 직접 다운로드 성공,
  6프레임 추출 (1.5·3·5·6.5·8·9.5s)
- 증거 기반: author-described (가이드 전문) + **frame-derived (6프레임)**

**관찰 — 상태 구별화 (State Differentiation)** (author-described)
- 가이드의 핵심 개념: AI가 부력을 "무중력"이나 "자유낙하"와 혼동하는
  현상을 상태 충돌(state_conflict)로 명명:
  `buoyancy_zerogravity_confusion`, `state_conflict_underwater_free_fall`
- 세 상태의 시각적 증거 차이를 명시: 부력 = 유체 저항·상승 기포·
  코스틱스·중성 부력 표류 / 무중력 = 매질 부재·회전 표류·기포 없음 /
  자유낙하 = 공기 저항·수직 가속·모션 블러
- #8 중력 가이드(GSTREC)의 형제 편: 물리 상태 제어 시리즈
  (중력→타격→부력)

**관찰 — 4대 유체 환경 앵커링** (author-described + frame-derived)
- 유체 저항, 상승 기포, 코스틱스 광학 굴절, 체적광/빛내림
- 프레임 검증: 1.5s 수면에서 기포 상승 + 상부 빛내림, 3s 레귤레이터
  기포 스트림 + god rays, 9.5s 바닥 부근에서도 기포 지속 상승 —
  "Streams of small rising bubbles continuously ascend" 성립
- 코스틱스 무늬는 다이버가 실루엣 규모라 스틸에서 검증 불가 (미확인)

**관찰 — 관계형 부정문** (author-described)
- ❌ "no zero gravity, no free fall" (단순 금지)
- ⭕ "no weightless rotational drift without fluid drag,
  no free-fall acceleration underwater,
  no instant direction changes without fluid displacement." (관계형 금지)
- #33의 "no camera shake before physical contact"와 같은 조건부 네거티브

**관찰 — Before/After 교육법** (author-described)
- 실패 프롬프트 + 문제점 진단 + 수정 프롬프트의 3단 구성
- 예시 1 (다이버 중성 부력): "floating underwater nicely in zero gravity
  style" → 유체 증거 앵커링 버전
- 예시 2 (상자 입수): "falls into water and floats instantly" → 입수 충격·
  항력·역전 상승의 3단계 인과 서술
- 가이드 자체가 프롬프트 설계 패턴의 재사용 가능한 템플릿

**관찰 — 시선** (frame-derived)
- 다이버가 헤드다운 실루엣. 얼굴 미식별, 시선 N/A

**관찰 vs 추론**
- 관찰(6프레임): 기포 지속 상승, 체적광, 완만한 하강 표류, Dola AI
  워터마크 우하단, 모래 바닥+심해 그라데이션
- 미확인: 코스틱스 무늬, 유체 저항의 모션상 표현 (스틸 한계)
- 추론: 영상은 예시 1(다이버 중성 부력)의 수정 프롬프트 계열로 추정 —
  포스트 본문에 예시 프롬프트가 직접 붙어 있지 않아 추론으로 기록

**Production description → Control Levels**
- Hard Lock: 세 상태의 시각 증거 차이 (기포 유무, 저항 유무, 표류 방식),
  관계형 네거티브 3종
- Soft Guidance: 4대 환경 앵커 (기포·코스틱스·체적광·저항), 3단계
  시간축 인과 (입수→중성 부력→표류)
- Creative Freedom: 장면 구성, 다이버 동작

**기여 패턴**: 1 (신규 — 상태 구별화: 유사 물리 상태를 시각 증거 차이로
  명명·분리하는 기법. `buoyancy_zerogravity_confusion` 같은 오류명 부여는
  네거티브 설계의 재사용 가능한 어휘), 2 (관계형 네거티브 #33 동계열),
  3 (Before/After 교육법 — 실패 프롬프트 진단+수정의 3단 템플릿)

---

## 36. Threads @jeong_do_ryeong — "터미네이터 T-1000 흉내내기" (Dola AI)

**기본 정보**
- 출처: Threads @jeong_do_ryeong, 게시 2026-09-22 10:12 KST
- 포스트 본문: "터미네이터 T-1000 흉내내기"
- 댓글에 프롬프트 전문 공개 (영어, 4-Phase 구조)
- 영상: ~10.2초. mp4 직접 추출 실패 (플레이어 구조상 <video> 접근
  불가) → 임베드 플레이어에서 타임스탬프별 스크린샷 6장 캡처
  (1.5·3·5·6.5·8·9.5s, 슬라이더 초 단위 검증)
- 증거 기반: prompt-derived (전문) + author-described (캡션) +
  **frame-derived (6 스크린샷)**

**관찰 — 4-Phase 상태 전이 체인** (prompt-derived + frame-derived)
- Phase 1 (Fluid Aggregation): 바닥의 은색 유체 웅덩이들이 표면
  기울기를 따라 흘러 하나의 덩어리로 수렴
- Phase 2 (Volumetric Rise & Phase Transition): 유체 덩어리가 수직
  부피를 얻어 성인 키·질량으로 확장. 척추가 수직으로 연장되고
  무게중심이 상승
- Phase 3 (Locomotion Transition & Surface Solidification): 전진 이동이
  인간 이족 보행으로 재조직 (체중 이동, heel-to-toe 접지, 반대팔
  스윙). 동시에 금속 유체 표면이 점진적으로 직조·경화되어 경찰 제복의
  질감·색·원단으로 완전 변환
- Phase 4 (Bipedal Resolution & Persistent Physics): 동일한 궤적으로
  카메라를 향해 계속 전진. 중력·균형 미세 보정
- 프레임 검증: 1.5s 바닥 은색 웅덩이 → 5s 통합 마운드 상승 →
  6.5s 금속 휴머노이드 (척추 연장 중) → 8s 크롬 제복 경관 보행 →
  9.5s 완전한 인간 경관 (네이비 제복, 넥타이, 벨트, 뱃지)
- **#8 GSTREC의 가장 세분화된 형제**: 변신이라는 비물리 현상을
  4단계 인과 체인으로 서술

**관찰 — 컷 없는 변신 vs CUT 변신** (prompt-derived)
- "A seamless phase transition occurs without cuts."
- #1 ("THE LAST TRAIN" — CUT을 변신 트리거로)과 정반대 문법.
  변신에는 두 문법이 공존: 컷-트리거형 vs 컷리스-모프형.
  프롬프트가 어느 쪽인지 명시해야 함

**관찰 — 수직 성장의 해부학 앵커** (prompt-derived + frame-derived)
- "The spine extends vertically, shifting the center of mass upward."
- 추상적인 "커진다"가 아니라 척추 연장+무게중심 상승이라는
  관찰 가능한 해부학 지표로 서술 (#33의 Concept Lowering 동계열)
- 6.5s 프레임: 마운드에서 수직으로 솟은 형상 — 수직 성장 성립

**관찰 — 재질 상전이의 점진성** (prompt-derived + frame-derived)
- "the metallic fluid surface progressively weaves and hardens,
  transforming completely from liquid metal into the detailed
  textures, colors, and fabric"
- 8s는 크롬 질감 제복 (중간), 9.5s는 완전한 원단 제복 (완료) —
  점진적 상전이의 2단계가 프레임에 포착됨

**관찰 — 배경 모핑 방지 (환경 락)** (prompt-derived + frame-derived)
- "the established architectural structure of the factory floor
  remains strictly spatially consistent without background morphing"
- 6프레임 모두 강철 그레이팅 바닥·공장 구조 동일 — 환경 락 성립
  (#19의 벽→창 네거티브와 같은 계열)

**관찰 — 반(反)로봇 불규칙성** (prompt-derived)
- "All transitions exhibit subtle irregular timing, avoiding perfectly
  smooth or mechanical motion" — #34와 동일한 문구 계열

**관찰 — 시선** (frame-derived)
- 9.5s 경관이 카메라를 향해 정면 접근. 얼굴 식별 가능하나 시선 방향은
  스틸 한계로 추정 (카메라 방향 응시 추정 — 미확인으로 기록)

**관찰 vs 추론**
- 관찰(6 스크린샷): 4-Phase 전이 성립, 수직 성장, 재질 상전이 2단계,
  배경 일관성, Dola AI 워터마크 우하단
- 미확인: 시선 방향 확정, 모션의 실제 부드러움 (스틸 불가)
- 추론: 없음

**Production description → Control Levels**
- Hard Lock: 4-Phase 순서, 컷 없는 전이, 배경 구조 일관성,
  반로봇 불규칙성, 동일 궤적 전진
- Soft Guidance: 50mm 아나모픽·얕은 심도, 산업 공장 바닥·림라이트,
  heel-to-toe·반대팔 스윙 생체역학
- Creative Freedom: 유체 흐름 경로, 경화 속도

**기여 패턴**: 1 (신규 — 컷리스-모프 문법: #1의 컷-트리거형과 대비되는
  변신 문법. 어느 쪽인지 명시가 필요), 2 (#8 GSTREC 동계열 —
  비물리 현상의 4단계 인과 체인), 3 (수직 성장의 해부학 앵커 —
  척추 연장+무게중심 상승), 4 (배경 모핑 방지 #19 동계열)

---

## 37. Threads @jeong_do_ryeong — 방송국 스포츠 시그널: 음악→LLM 시나리오→생성 프롬프트 (Dola AI)

**기본 정보**
- 출처: Threads @jeong_do_ryeong, 게시 2026-09-23 12:38 KST
- 포스트 본문: "방송국 스포츠 시그널을 음악을 영상으로 만든 것"
- 작성자 댓글 1: "이건 방송국 스포츠 시그널 음악 첨부하니 LLM이 써준
  시나리오" — Broadcast Opening Scenario Report (10s Cutdown) 전문
- 작성자 댓글 2: 생성 프롬프트 전문 (영어, 6비트 타임드 멀티샷)
- 영상: 10초 (24fps, 1280×720). 직접 다운로드 성공, 6프레임 추출
  (0.2·1.5·3·5·6.8·9s)
- 증거 기반: author-described (시나리오 리포트 + 프롬프트 전문) +
  **frame-derived (6프레임)**

**관찰 — 음악→영상 파이프라인의 실전 사례** (author-described)
- 음악 파일 첨부 → LLM이 시나리오 작성 → 생성 프롬프트.
  사용자의 장기 목표(음악+캐릭터 입력 → AI 기획 → 프롬프트)의
  현장 구현형. #32의 "Qwen에 프롬프트 확장"과 같은 LLM 중간층 패턴
- 시나리오 리포트는 오디오 실측 기반: 구간별 RMS(0.063→0.127),
  온셋 밀도 (초당 약 4회), 센트로이드 2203Hz
- "0:00–0:10 구간은 실측상 이완 없이 지속 HIGH" → "처음부터 끝까지
  압축된 임팩트" 구조로 설계. 오디오 측정값이 연출 구조를 결정

**관찰 — Necessity Test (가지치기 장치)** (author-described)
- 모든 요소가 실측 오디오에 대한 근거로 존재 이유를 증명해야 함
- "서서히 고조되는 연출은 불필요(있으나 마나 함)" → 즉시 절정 구조
- 반대로 얼굴 클로즈업은 유지: "완전히 삭제하면 브랜드가 차가워짐"
  (Necessity Test 근거로 유지) — 제거의 근거이자 유지의 근거
- ⚠️ 사용자 정정 (2026-09-25): Necessity Test는 "다 자르라"는 규칙이
  아니라 "모든 요소가 근거를 대라"는 규칙으로 읽어야 한다. 근거의
  출처는 실측(오디오 측정값)뿐 아니라 창작적 결정(감독·편집자·기획자의
  취향)도 된다. 예: 2001 스페이스 오디세이의 "차라투스트라는 이렇게
  말했다" + 유인원의 뼈가 날아오르는 장면 — 서서히 고조되는 연출이
  바로 그 장면의 necessity다. 고조 구조 자체를 금지하는 게 아니라,
  고조가 필요하면 그 필요를 명시하라는 것. 가이드의 "실측 vs PROPOSED"
  분리 표기가 바로 이 두 근거 출처를 구분하는 장치
- 과한 편집 장치 금지: "10초 안에 Match Cut 1회만 — 과한 편집 장치는
  피로감만 유발"

**관찰 — 실측 vs PROPOSED의 정직한 분리** (author-described)
- "이 지점의 오디오 컷은 원곡 구조 근거가 아니라 순수 편집 필요성
  (PROPOSED)이며, 실제 사용 시 오디오 엔지니어링이 별도로 필요하다"
- "10초는 실측 오디오가 제공하는 자연스러운 종결부가 아니므로,
  마지막 컷은 창작적 편집 결정"
- #24·#25의 실패 출처 명시와 같은 정직성 문법: 관찰된 것과 창작된 것을
  구분 표기

**관찰 — 가장 완전한 마스터 스펙 구조** (author-described)
- SCENE CONTEXT / LOCATION MAP / FIRST FRAME+BLOCKING /
  FORMAT MODE ("Timed multishot. Cuts only at the specified seconds;
  the camera does not cut on its own.") /
  비트별 타임라인 (HARD CUT 마커) / 비트별 OPTICS (FOV 12°·63°·84°·
  84°·18°·47°) / CAMERA / ACTION / PERFORMANCE / PHYSICS /
  LIGHTING / COLOR GRADE / AUDIO / STYLE / OUTPUT SETTINGS /
  POSITIVE LOCKS
- POSITIVE LOCKS: 엠블럼 기하학적 동일성, 블루-화이트 컬러 아이덴티티
  (스티링거·파이널 락 제외), 종목당 선수 정확히 1명 (헤드카운트 락),
  명시된 타임코드에서만 컷, "generic unbranded" 엠블럼

**관찰 — 프레임 검증** (frame-derived)
- 0.2s: 화이트-골드 플래시 블룸 풀프레임 — 스팅어 성립
- 1.5s: 거의 암전 + 미세한 오렌지 광점 — 프롬프트상 0.4–2.3s는
  스프린터 구간인데 암전 지속. **비트표 절대 시간 불신 (#31 재현)**:
  모델이 암전을 0.4s보다 길게 유지
- 3s: 스프린터가 스타팅 블록에서 폭발 (프롬프트상 2.3–4.0s는 농구
  구간인데 육상 렌더) — 전체 타임라인이 뒤로 밀림. 농구 버즈아이
  세그먼트는 6프레임 중 미포착 (압축·생략 추정, 샘플링 한계로 미확인)
  > ⚠️ 정정 (Claude, 2026-09-26): 농구 버즈아이 컷은 **3.71–4.54s에 존재**한다 (scene detect). 실측 컷 시각: 2.667 / 3.708 / 4.542 / 5.542 / 7.958s (프롬프트 0.4 / 2.3 / 4.0 / 5.6 / 8.0). evidence E3·E4.
- 5s: 축구 킥 + 블루 라이트 트레일 — 종목 구간 성립
- 6.8s: 선수 얼굴 클로즈업, 땀방울·림라이트, **렌즈 정면 응시** —
  "eyes lock forward"가 카메라 직시로 렌더. 방송 오프닝 장르 관습
  (#21 계열)
  > ⚠️ 정정 (Claude, 2026-09-26): 아래 9s 항목의 "원형 엠블럼"은 파일상 **금속성 "S"자 엠블럼**이다 (원형은 프롬프트 지정값). evidence E2.
- 9s: 라이트 트레일이 수렴한 원형 엠블럼, 시안→화이트 그라데이션 —
  기하학적 동일성 유지, 파이널 락 성립
- 라이트 트레일은 전 종목 구간에 등장 후 엠블럼으로 수렴 — "로고
  수렴의 씨앗". #31의 "같은 책"과 같은 연속성 토큰
- Dola AI 워터마크 우하단 전 구간

**관찰 — 시선** (frame-derived)
- 6.8s: 선수 눈이 렌즈를 정면으로 응시. 방송 오프닝 장르 관습상
  의도된 카메라 어드레스. 프롬프트 "direct forward stare"와 일치

**관찰 vs 추론**
- 관찰(6프레임): 스팅어·육상·축구·클로즈업·엠블럼 성립, 타임라인
  후방 드리프트, 농구 구간 미포착
- 미확인: 농구 세그먼트의 실제 렌더 여부 (프레임 샘플링 사이 구간),
  오디오 (스틸 불가)
  > ⚠️ 정정 (Claude, 2026-09-26): 아래 추론은 실측과 부분적으로 맞지 않는다. 스팅어는 +2.27s 늘어났고 중간 세 종목은 약 1s씩 압축됐다. 하지만 **얼굴·로고 컷은 −0.06 / −0.04s로 프롬프트 시각을 지켰다**. "순서만 유지"보다는 "앞은 늘어나고 끝은 지켜짐(1건)"이 실측에 가깝다. evidence E4.
- 추론: 모델이 6비트를 절대 시간대로 지키지 않고 순서를 유지한 채
  압축·이동 — #31의 "비트표 절대 시간 불신"과 동일 현상

**Production description → Control Levels**
- Hard Lock: 6비트 순서, 종목당 1명, 엠블럼 기하학적 동일성,
  명시 타임코드 외 컷 금지, unbranded 엠블럼
- Soft Guidance: 비트별 FOV·조명·컬러그레이드, 라이트 트레일 수렴,
  오디오 설계 (0.0s 타격음, 컷마다 whoosh, 10.0s chime)
- Creative Freedom: 종목별 구체 동작, 트레일 궤적

**기여 패턴**: 1 (신규 — Necessity Test: 실측 근거로 요소를 가지치기/
  유지하는 장치. 제거와 유지 양쪽의 근거), 2 (신규 — 실측 vs PROPOSED
  분리 표기: 관찰된 사실과 창작적 결정의 정직한 구분), 3 (신규 —
  음악→LLM 시나리오→프롬프트 파이프라인의 실전 사례. 사용자의
  장기 목표와 직접 연결), 4 (연속성 토큰 #31 동계열 — 라이트 트레일)

---

## 38. Threads @chase90re (CHAse) — 액션 시퀀스 실사 프롬프트 (약 60초)

**기본 정보**
- 출처: Threads @chase90re (CHAse, verified), 게시 2026-09-25 18:23 KST
- 포스트 본문: "액션 시퀀스 실사 프롬프트 🐰" / 795 views, 20 likes
- 작성자 댓글: 생성 프롬프트 전문 (한국어, 10개 렌즈 세그먼트 구조)
- 영상: 약 60.6초 (임베드 플레이어 슬라이더 aria-valuemax 기준).
  **프롬프트는 "30초, 16:9"를 주장** — 주장과 실제 산출물의 불일치
- 증거 기반: author-described (프롬프트 전문) + screenshot-derived
  (임베드 플레이어 4프레임: 썸네일·질주·근접전·엔드카드)
- 비고: @chase90re의 세 번째 항목 (#15 장미정원, #16 얼굴 없는
  캐릭터 시트). 한국어 장문 프롬프트 + 엄격한 규칙 서술이 작가의
  일관된 스타일

**관찰 — 참고 이미지 바인딩** (author-described)
- @Image1 = 주인공 신분·의상 참고 (얼굴형·장발·암홍색 외투·칼라·
  허리띠·넓은 바지·다리 붕대·신발 고정)
- @Image2 = 적 무리 외형 참고 (체형·피부·눈·송곳니·발톱을 추출해
  고밀도 적조로 확장)
- @Image3 = 전장 건축·공간 구조 참고 ("오직 떠 있는 나무 플랫폼,
  난간, 회랑, 계단, 대전 및 상하 교차 건축 관계만 채택")
- #9의 레퍼런스 권한 분리를 한국어로 구현한 형태. "오직 ~만 채택"
  이라는 배타적 문구가 핵심

**관찰 — 캐릭터·소품 락** (author-described)
- "전편 내내 주인공은 단 한 명뿐" — 헤드카운트 락 (#33·#37 동계열)
- "항상 동일한 실체 칼을 사용하며, 칼집은 허리 측면에 고정" —
  소품 락 (#10 동계열)
- "순간이동 금지. 실체 분신 금지. 두 번째 칼 금지." — 모델의 대표
  실패 모드 3종을 직접 금지하는 failure-sourced negatives
- "오른손 주로 쥐고, 강타 시 왼손이 동일한 손잡이를 보조" —
  양손 협응까지 지정한 그립 문법

**관찰 — 신체 연쇄 공격 문법** (author-described)
- "발로 땅을 차 → 엉덩이 회전 → 칼 휘두르기 → 손목 회수 → 연속 착지"
- 모든 공격은 실제 신체 동작에 의해 구동. #33 Universal Action
  Grammar의 검술 도메인 버전 (타격 문법의 이식)
- 연계 문법: "이전 베기의 수동 방향이 직접 다음 그룹 공격의 시작
  방향이 됨. 공격 후 멈춰 자세 재정비 금지." — #26의
  ACTION DIFFERENCE LOCK 동계열. 멈춤 금지가 곧 연속성의 증거

**관찰 — "속도의 출처" 규칙** (author-described)
- "미친 컷 전환으로 속도 생성 금지. 속도는 다음에서 나와야 함:
  인물 이동 / 적 무리 운동 / 신체 동작 / 전경 스치기 / 카메라 추적"
- 속도를 편집(컷)이 아닌 모션에서 꺼내도록 강제. #33의 anti-cheat
  ("the camera does not cut on its own")와 같은 계열의 부정문이지만,
  대상이 컷이 아니라 속도감 그 자체라는 점이 새로움
- "장기 얼굴 클로즈업 금지" — #37의 얼굴 클로즈업 유지와 정반대.
  같은 Necessity Test를 통과한 정반대 결정: 장르(검술 액션) 관습이
  authored 근거. §3(방법론 의견)의 "근거의 두 출처"를 보여주는 사례

**관찰 — 나침반식 공간 선언** (author-described)
- "주 플랫폼 원거리 계단 = 북. 입구 = 남. 좌우 양측은 각각 동, 서."
- 인물 이동 경로: 남부 → 동측 → 중앙 → 서측 → 북부
- #28의 마스터 스크린 방향 축을 실내 전장에 적용한 형태.
  방위를 명명하면 모델이 경로를 추적할 기준점이 생김
- "카메라는 항상 미청소 적 무리를 향해 전진" — 카메라의 임무를
  적진 기준으로 선언 (인물 추적이 아닌 목표 추적)

**관찰 — 시간 기반 금지, pacing lock** (author-described)
- "24초 이전에 전장을 대규모로 청소 금지"
- "인물이 지나간 후에야 부분적 틈새를 허용"
- 클라이맥스의 타이밍을 숫자로 잠그는 장치. 모션 버짓의 시간 버전
- 10개 렌즈 세그먼트 × 약 3초 = 30초 설계, Shot 1–10 비트표.
  "등장 없음. 칼 뽑기 없음. 기력 축적 없음. 첫 번째 초에 직접
  전투 진입." — #37 Necessity Test의 실전형 (도입부 가지치기)

**관찰 — 오디오를 부정문으로 정의** (author-described)
- "대화 없음. 전투 함성 없음. 자막 없음. 배경 음악 없음."
- 유지: "발소리 / 칼 휘두르는 소리 / 충돌 소리 / 목재 파괴 소리 /
  환경 공간 메아리"
- Audio DNA를 "넣을 것"이 아니라 "뺄 것"으로 먼저 정의.
  #5의 립싱크 할당과 같은 계열의 오디오 통제

**관찰 — 30초 주장 vs 60.6초 실제** (screenshot-derived + inference)
- 프롬프트 전문이 "30초"를 전제로 10×3초를 설계했는데, 실제 영상은
  약 60.6초. 두 배 차이
- #31·#37의 "비트표 절대 시간 불신"과 같은 주장-렌더 간극.
  원인 미확인 (생성 설정·모델의 길이 해석·이어붙이기 등 가능성은
  있으나 추론에 불과)
- 교훈: 작성자의 스펙 숫자(길이·시간)는 frame-derived로 재측정해야
  한다는 원칙의 재확인

**관찰 — 프레임 검증** (screenshot-derived)
- 썸네일(0s대): 목조 대전에 수백의 적 무리가 주인공을 포위.
  "적 수는 수백 마리", "중앙 플랫폼·양측 회랑에 항상 대량" 성립.
  규모감 렌더 성공
- 질주 프레임: 삿갓 쓴 주인공이 적들 사이를 질주, 분홍빛 호형 검기
  궤적. "유광 절단 + 파스텔 핑크 검기 잔상" 성립. 전경의 적이
  블러로 스치며 지나감 — 프롬프트의 "전경 스치기" 속도 문법이
  프레임에 그대로 보임
- 근접전 프레임: 뿔 달린 적과 일대일 구도 — Shot 7의 "실제 근거리
  공방"으로 추정. "단독 대결로 변형 금지"와 겉보기 충돌이나,
  주변에 다른 적들이 흐릿하게 보여 스틸의 한계로 판단 보류
- 엔드카드: "With CHASE SURE" (핑크 CHASE + 그린 SURE).
  #21·#25의 모델 워터마크 번인과 달리 의도된 크리에이터 크레딧

**관찰 — 시선** (author-described + screenshot-derived)
- 프롬프트: "시선은 항상 다음 적진 틈새를 찾음"
- 시선의 목표가 인물·물체가 아니라 "틈새"(negative space).
  시선 할당의 새 문법: gaze target = 빈 공간
- 프레임에서는 삿갓에 가려 눈 미확인 (스틸 한계)

**관찰 vs 추론**
- 관찰: 바인딩 3종의 역할 분리, 헤드카운트·소품 락, 신체 연쇄 문법,
  속도의 출처 규칙, 나침반 선언, 24초 pacing lock, 오디오 부정문,
  4프레임의 규모감·검기·전경 스치기·엔드카드 성립
- 미확인: 30초→60.6초 차이의 원인, 근접전 구도의 전후 맥락,
  삿갓 아래 시선, 오디오 (스틸 불가)
- 추론: 모델이 길이 스펙을 무시하고 확장 — #31·#37과 동일 계열의
  "스펙 숫자 불신" 현상

**Production description → Control Levels**
- Hard Lock: 주인공 1명, 동일한 칼 1자루, 순간이동·분신·두 번째 칼
  금지, 24초 이전 대규모 청소 금지, 방위(북=계단·남=입구),
  남→동→중앙→서→북 이동 경로, 오디오 5종만 허용
- Soft Guidance: 10개 렌즈 세그먼트 구성, 적 무리 밀도 분포,
  검기 색(파스텔 핑크), 먹빛 검정·희청색·나무 갈색 톤
- Creative Freedom: 26그룹 연계의 구체 동작, 적 개체의 외형 변주

**기여 패턴**: 1 (신규 — "속도의 출처" 규칙: 속도감을 편집이 아닌
  모션에서 꺼내도록 강제), 2 (신규 — 나침반식 공간 선언: 명명된
  방위 + 이동 경로), 3 (신규 — 시간 기반 금지/pacing lock: "24초
  이전 청소 금지"), 4 (신규 — 시선→틈새 할당: gaze target =
  negative space), 5 (참고 이미지 역할 분리 #9·#16 동계열 —
  "오직 ~만 채택"), 6 (신체 연쇄 공격 문법 #33 동계열), 7 (주장-렌더
  간극 #31·#37 동계열 — 30초 vs 60.6초), 8 ("등장 없음. 칼 뽑기
  없음" — Necessity Test 실전형 #37 동계열)

---

## 39. X @AIwithzayn — 한강 투신→수중 구조 K-드라마 (Seedance 2.5, 44.5초)

**기본 정보**
- 출처: X @AIwithzayn (verified, "AI Video Creation", 29.2K followers),
  게시 2026-09-25 12:30 KST
- 포스트 본문: "Made with seedance 2.5 and wait this actually looks real 😨
  Prompt 👇🏼" — 프롬프트는 작성자 셀프 댓글에 있으나 X 로그인 월 뒤에
  있어 미확보 (xcancel 정지, nitter 접속 불가, sotwe Cloudflare 차단).
  **프롬프트 미확보 항목** — 사용자가 X에서 직접 보고 붙여넣으면 추가
- 영상: 44.47초 (1067프레임/24fps, 직접 다운로드·프레임 수 검증).
  참고: X 임베드 플레이어는 00:32로 표시했으나 실제 파일은 44.47초 —
  플레이어 표기를 그대로 믿지 말 것 (#31의 비트표 절대 시간 불신과 같은
  교훈)
- 반응: 36 likes, 12 replies, 4 reposts, ~1,591 views. 댓글 3개는
  "프롬프트 어디 있냐"는 질문 (로그인 없이 보이는 댓글만)
- 증거 기반: frame-derived 9프레임 (2·5·10·15·20·25·30·35·40·42s).
  프롬프트 없으므로 전부 프레임 관찰

**관찰 — 서사 비트** (frame-derived)
- ~2s: 소녀 클로즈업. 눈 감고 울음, 머리카락이 얼굴에 날림, 밤 보케
- ~5s: 교복(흰 셔츠·어두운 스커트) 소녀가 밤의 다리 난간을 넘어감.
  가방은 바닥에 내려놓음. 좌상단 "AI" 워터마크
- ~10s: 다리 아래 강물에 첨벙이는 물보라 (투신)
- ~15s: 수중 — 떠다니는 머리카락, 기포, 위에서 내려오는 빛
- ~20s: 수중에서 남녀가 마주봄. 남자가 다가오고 소녀의 손이 뻗음.
  **상호 응시**
- ~25s: 수중 실루엣 — 두 인물이 끌어안은 채 빛을 향해 상승
- ~30–35s: 강변. 남자가 누운 소녀 위로 몸을 숙임. 둘 다 흠뻑 젖음.
  남자 얼굴에서 물이 뚝뚝 떨어짐. 소녀는 눈 감음. **일방 응시**
- ~40–42s: 남자가 계단을 올라 걸어감. 소녀는 강변에 누운 채 남음.
  **시선 단절** (등 돌림)

**관찰 — 시선의 호(arc)** (frame-derived)
- 감은 눈(슬픔) → 시선 없음(투신·수중 표류) → 수중 상호 응시(만남) →
  일방 응시(구조, 그녀는 무의식) → 시선 단절(떠남, 등)
- 감정선에 따라 시선을 열고 닫는 구조. #37의 "unresolved chemistry"
  시선 사다리와 같은 계열이나, 여기는 **시선의 개폐 자체가 서사**다.
  사용자의 2인 MV 목표(움직임·시선·카메라·조명 기획)에 직접 연결되는
  사례: 시선을 감정 비트의 악보로 쓴 것

**관찰 — K-드라마 구조 비트** (frame-derived)
- 투신→수중 만남→구조→떠남. 한국 드라마의 단골 구조를 44초에 압축
- 배경(한강스러운 다리·아파트 불빛·강변 계단)이 장르를 고정.
  로케이션 자체가 서사 약속

**관찰 — 리얼리즘의 근거** (frame-derived)
- "actually looks real"의 실체: 남자 얼굴에서 떨어지는 물방울,
  흠뻑 젖은 머리카락의 무게감, 밤 보케, 수중 부유물의 디테일
- #35의 "상태 구별화" 동계열 — 젖음이라는 물리 상태가 전 프레임에
  일관되게 유지됨 (수중→강변, 옷·머리카락·피부 전부 젖음)

**관찰 — "AI" 워터마크 번인** (frame-derived)
- ~5s 프레임 좌상단에 "AI" 워터마크. #25의 "Wavespeed SEEDANCE 2.5"
  우상단 번인, #21의 "Dola AI", #32의 더블 워터마크와 같은 계열 —
  모델/툴 레이어의 번인은 프롬프트로 막을 수 없음

**관찰 vs 추론**
- 관찰: 9프레임 서사 비트, 시선의 호, 워터마크, 44.47초 실측,
  젖음 상태 일관
- 미확인: 프롬프트 전문 (로그인 월), 오디오, 대사의 유무
- 추론: 수중 상승 샷(~25s)의 빛은 "희망"의 은유로 읽히나 이는 해석.
  프로덕션 스펙에 넣지 않음

**Production description → Control Levels** (프롬프트 미확보 — 프레임에서
  역추정한 잠금 포인트로만 기재)
- Hard Lock: 2인 캐릭터 일관성 (교복 소녀·검은 후드티 남자), 젖음 상태
  전 구간 유지, 시선 비트 순서 (상호 응시→일방 응시→단절)
- Soft Guidance: 밤 한강 로케이션, 수중→강변 공간 전이, K-드라마 톤
- Creative Freedom: 구체 카메라 무빙, 물방울·기포 디테일, 엔딩 여운

**기여 패턴**: 1 (신규 — 시선의 호: 감정선에 따른 시선 개폐를 서사로),
  2 (신규 — K-드라마 구조 비트의 압축: 투신→수중 만남→구조→떠남),
  3 (워터마크 번인 #21·#25·#32 동계열 — "AI" 좌상단), 4 (플레이어 표기
  00:32 vs 실측 44.47초 — #31의 시간 불신 교훈 재확인), 5 (젖음 상태
  일관 #35 동계열)

---

## 40. X @doctorwasif — CHASE 짐 브이로그 (Seedance 2.5, 15초)

**기본 정보**
- 출처: X @doctorwasif, 게시 2026-09-25 13:26 UTC (22:26 KST)
- 포스트 본문: "made with Seedance 2.5" + 프롬프트 전문 (author-described)
- 영상: 15.14초, 1920x1080, 24fps (직접 다운로드). "15s" 주장과 일치 —
  드물게 주장-렌더가 맞는 사례 (#38의 반대)
- 반응: 17 likes, 9 replies, 432 views
- 증거 기반: prompt-derived (프롬프트 전문) + frame-derived
  (컷별 6프레임: 1.2·3.7·6.2·8.7·11.2·13.7s)
- 비고: 사용자가 보낸 두 링크 중 두 번째. 첫 번째(#39, @AIwithzayn)는
  프롬프트가 댓글에 있어 브라우저 확인 중

**관찰 — 프롬프트 섹션 구조** (author-described)
- CAMERA / LOOK / STYLE / Character / Setting / Storyboard — 역할이
  분리된 섹션 템플릿. Storyboard는 6컷, 컷마다 "(~초, 카메라 배치,
  샷 사이즈)" + 대사
- 컷 시간 표기: 2.5·2.5·2.5·2·2.5·3s = 15s. 합이 맞는 비트표

**관찰 — 셀프 POV의 역설 해소** (author-described)
- "POV of CHASE holding the camera herself, occasionally propping it
  on the floor or a mat for hands-free core shots"
- "Camcorder never appears on screen"
- 들고 찍는 주체가 화면에 등장하지 않아야 한다는 것을 부정문으로 잠금.
  셀프 POV 장르의 대표 실패 모드(카메라·삼각대 노출)를 직접 차단.
  #22의 셀프 POV 동계열

**관찰 — 불완전함을 리얼리즘으로** (author-described)
- "Hand shake, misaligned framing, delayed focus pulls, clumsy zooms,
  occasional face cut-off framing, imperfect shots"
- MiniDV 테이프 질감: "Soft, slightly blurry tape quality, faint tape
  noise, bloomed highlights under gym lighting, flickering auto-exposure,
  muted contrast, realistic skin tones"
- #19(빗방울 침실 MiniDV) 동계열. 완벽함이 아니라 결함을 스펙으로 쓰는
  "카메라 DNA" 방식

**관찰 — 대사 + 전달 지정** (author-described)
- CHASE (strained): "Why does this get harder every single time—"
- CHASE (breathless): "Okay— that's it, I'm done—"
- 대사는 따옴표, 전달은 괄호, 호흡 끊김은 말줄임표(—)로 표기.
  #5의 한국어 IPA 립싱크와 같은 계열의 발화 통제

**관찰 — 컷별 오디오 온오프** (author-described)
- Cut 4: "Close-up on her hands gripping the mat edges during a leg
  raise, abs visibly working. No dialogue — ambient gym sound only."
- 오디오를 컷 단위로 켜고 끔. #38의 오디오 부정문 정의와 같은 계열

**관찰 — 스토리보드 충실도** (frame-derived)
- 6프레임 전부 스토리보드와 일치: 매트 위 팔꿈치 괴고 한숨(1.2s),
  플랭크 중 카메라 응시(3.7s), 크런치(6.2s), 손 매크로(8.7s),
  누워서 웃음(11.2s), 얼굴 위 셀카 마무리(13.7s)
- Setting 요소(물병·라커·거울벽·오버헤드 조명)가 전 프레임에서 유지
  > ⚠️ 정정 (Claude, 2026-09-26): 라커 열·벤치·물병·천장 조명은 확인된다. **거울벽은 2초 간격 콘택트 시트에서 확인되지 않는다** (거울벽은 프롬프트 지정값). evidence E6.
- 손 매크로 프레임: 손가락 5개 정상 렌더, 손등의 땀방울까지.
  AI 손 실패를 피한 증거. "shallow DOF" 지정도 성립

**관찰 — CHASE 캐릭터의 크로스 크리에이터 사용** (author-described + inference)
- "CHASE — Korean idol, 20s. Long black hair in a high ponytail,
  glowing skin with a light sweat sheen"
- #22(@QAiStudio CHASE 헬스장 브이로그 — 셀프 POV), #38의 @chase90re와
  동일 이름 "CHASE". 서로 다른 크리에이터가 같은 이름의 캐릭터를 사용
- 동일 인물인지는 미확인이나, 이름·연령대·장발 포니테일 스펙이 겹침.
  공유 캐릭터(community character) 현상으로 기록. 사용자의 2인 MV
  목표에서 캐릭터 공유 방식의 참고 사례

**관찰 — 시선** (frame-derived)
- 전편 카메라 직접 응시 (브이로그 문법). Cut 1·2·5·6에서 렌즈 응시 확인
- Cut 4 매크로만 얼굴 없음 (인서트 문법)
- "propped camera" 픽션: 카메라는 그녀가 내려놓은 물체이며, 그녀의
  시선은 그 물체를 관객으로 취급. 카메라 응시 금지 원칙(#12)의 정반대 —
  장르가 시선 문법을 결정

**관찰 vs 추론**
- 관찰: 15s 주장-15.14s 실제 일치, 6컷 전부 스토리보드 일치, 캠코더
  미등장, 손 매크로 정상, 전편 렌즈 응시
- 미확인: 오디오 (스틸 불가), 대사의 립싱크 정확도
- 추론: 없음. 스토리보드 충실도가 높아 추론의 여지가 적음

**Production description → Control Levels**
- Hard Lock: 15초·6컷 비트표, 캠코더 화면 미등장, CHASE 캐릭터 스펙
  (포니테일·회색 긴팔·레깅스), 컷별 대사 원문
- Soft Guidance: MiniDV 룩(노이즈·블룸·깜빡임), 불완전한 프레이밍,
  거울벽·물병 세팅
- Creative Freedom: 구체 표정·호흡 타이밍, 매크로 구도, 땀 표현 정도

**기여 패턴**: 1 (신규 — 셀프 POV 역설 해소: "Camcorder never appears
  on screen"), 2 (신규 — 주장-렌더 일치 사례: 15s vs 15.14s. #38의
  반대편 증거), 3 (불완전함 스펙 #19 동계열 — 흔들림·초점 지연·얼굴
  잘림을 명시), 4 (대사+전달 지정 #5 동계열 — 말줄임표 호흡 표기),
  5 (컷별 오디오 온오프 #38 동계열), 6 (CHASE 크로스 크리에이터 현상 —
  #22와 연결)

---

## 레포 승격 후보 (Candidate primitives / rules) — 2026-09-25 정리

아래는 40개 항목의 "기여 패턴"에서 수확한 후보 목록. 규칙은 "실전 테스트를
통과해야 승격"이라는 레포 원칙에 따라 전부 candidate로 둔다. 출처 번호는
분석집 항목 번호. 신뢰도 표기는 제안 단계: ★★★(독립 3건 이상) / ★★(2건) /
★(1건, 추가 검증 필요).

### A. 시선·블로킹
1. **Gaze assignment table** (Shot Graph 확장): 멀티 인물 샷마다
   `performer → gaze target (relative)` 테이블 필수. 공동 시선은 명명된
   동일 목표점, 분리 시선은 인물별 할당, 상호 시선은 양방향 서술.
   클로즈업에서는 이전 시선 이어주기. ★★★ (12·21·23·31)
2. **시선 사다리**: 시선의 강도를 단계별로 설계 (무시→인지→응시→정면).
   ★ (31)
3. **프레이밍 케이지**: 인물을 프레임 안에 가두는 구도 장치
   (문·창·거울 틀). ★ (31)
4. **샷별 헤드카운트 명시**: 샷마다 등장 인원수를 숫자로 고정.
   ★ (33·37)
5. **마스터 스크린 방향 축**: 시리즈 전체의 좌우 방향 기준선 선언.
   ★ (28)

### B. 물리·액션
6. **Trace-first physics writing**: 힘의 이름 대신 시각적 증거 5종
   (Trajectory / Momentum / Resistance / Impact / Weight Transfer)으로 서술.
   ★★★ (5·8·26·33·34)
7. **상태 전이 체인**: anticipation→contact→consequence를 끊지 않고 기술.
   ★★★ (8·26·33·35·36)
8. **상태 구별화**: 물리 상태 오류에 이름을 붙여 네거티브 어휘로 등록
   (예: buoyancy_zerogravity_confusion). ★★ (8·35)
9. **boundary lock**: 접촉하는 물체들의 물리적 경계 유지 선언
   (손–스틱–드럼헤드–심벌). ★ (34)
10. **반로봇 불규칙성**: "완벽히 매끄럽거나 동일하거나 로봇처럼 동기화된
    모션 금지" — 불완전함을 명시. ★ (34)
11. **13개 반응 증거 메뉴**: 타격 반응을 메뉴에서 골라 조합
    (Reaction Evidence의 어휘표). ★ (26)
12. **수직 성장의 해부학 앵커**: 모핑 시 척추 연장·무게중심 이동 같은
    해부학 기준점 기술. ★ (36)

### C. 컷·전이 문법
13. **컷리스-모프 vs 컷-트리거**: 변신은 끊김 없는 상전이(#36)와
    CUT 트리거(#1) 2종 문법이 공존 — 사용할 쪽을 명시. ★★ (1·36)
14. **"the camera does not cut on its own" anti-cheat**: 명시된 타임코드
    외 컷 금지를 선언문으로. ★★ (33·37)
15. **비트표는 순서만 신뢰**: 모델이 절대 시간을 지키지 않음 — 비트 순서는
    유지되나 압축·드리프트 발생 (#31·#37 프레임 검증). 비트표에 절대
    시간을 쓰지 말 것. ★★ (31·37)
16. **과한 편집 장치 금지**: 10초에 Match Cut 1회 같은 상한.
    ★ (37)

### D. 오디오·음악
17. **Exclusive lip-sync assignment**: 가사 줄마다 립싱크 담당 1명 고정,
    나머지는 "절대 따라하지 않음" 명시. ★ (5)
18. **음악→LLM 시나리오→프롬프트 파이프라인**: 오디오 실측(RMS·온셋·
    센트로이드) → LLM이 타임드 시나리오 → 생성 프롬프트. 사용자의 장기
    목표와 직결되는 검증된 프로토타입. ★★ (32·37)
19. **모델의 "숨" 삽입**: 강렬한 비트 사이에 의도적 정적/여백 구간.
    ★ (32)

### E. 프롬프트 작성법
20. **POSITIVE LOCKS**: 금지어보다 "이것은 고정" 선언을 우선
    (엠블럼 기하학적 동일성, 종목당 1명 등). ★★ (33·37)
21. **capability-calibrated 언어**: 모델이 할 수 있는 말로만 쓰기
    (측정 불가능한 물리량 대신 관찰 가능한 서술). ★ (33)
22. **관계형 부정문**: "no X without Y" 형태 — 조건부 네거티브
    (예: no weightless rotational drift without fluid drag). ★★ (33·35)
23. **레퍼런스 역할 분리**: 레퍼런스 이미지는 기능별 1역할만
    (identity-only / style-only / location-only). ★★ (4·9·16)
24. **실패 출처 명시 네거티브**: 네거티브에 "어떤 실패에서 왔는지" 기록.
    ★★★ (4·19·24·25)
25. **LLM 프롬프트 확장 워크플로**: 짧은 의도 → LLM(Qwen 등)이
    전체 프롬프트로 확장하는 중간층. ★ (32)
26. **모델별 프롬프트 언어 = 어댑터**: 같은 의도를 모델별 언어로 다르게
    쓰기 — Master Spec → Adapter 컴파일의 근거. ★ (26)

### F. 카메라·조명
27. **Camera DNA 6계열 무브 어휘표**: 42개 무브를 6계열로 정리한 어휘표
    (기사 기반, 명칭 오류 3건 정정됨). ★ (29)
28. **인과적 카메라 반응**: 타격·충격에 카메라가 물리적으로 반응
    (흔들림·후퇴). ★ (33)
29. **비트별 장소 앵커**: 비트마다 장소를 명시해 배경 표류 방지.
    ★ (33)
30. **연속성 토큰**: 구간을 관통하는 반복 요소로 통일감 부여
    (라이트 트레일 → 엠블럼 수렴, "같은 책"). ★★ (31·37)

### G. 메타 규칙
31. **Necessity Test**: 모든 요소는 근거를 대야 함. 근거의 출처는
    실측(measured)과 창작적 결정(authored) 둘 다 인정 — "다 자르라"가
    아니라 "근거 없이 넣지 마라". 2001 스페이스 오디세이의 차라투스트라+
    뼈 장면이 반례: 서서히 고조되는 연출이 그 장면의 necessity.
    ★ (37, 사용자 정정 반영)
32. **실측 vs PROPOSED 분리 표기**: 관찰된 사실과 창작적 결정을 표기상
    분리. #24·#25의 실패 출처 명시와 같은 정직성 문법. ★ (37)
33. **Before/After 교육법**: 실패 프롬프트 + 진단 + 수정 3단 구성으로
    가이드 작성. ★ (35)
34. **Motion budget caps**: 슬로모·불릿타임·배경 전환에 횟수 상한 +
    음악적 트리거를 수치로. ★★ (4·33)
35. **속도의 출처 규칙**: 속도감을 편집(컷 전환)이 아닌 모션(인물 이동·
    적 무리 운동·신체 동작·전경 스치기·카메라 추적)에서 꺼내도록 강제.
    ★ (38)
36. **나침반식 공간 선언**: 방위를 명명(북=계단·남=입구)하고 이동 경로를
    선언. #28의 마스터 스크린 방향 축을 실내 전장에 적용. ★ (28·38)
37. **Pacing lock (시간 기반 금지)**: "24초 이전 대규모 청소 금지"처럼
    클라이맥스 타이밍을 숫자로 잠금. ★ (38)
38. **시선→틈새 할당**: 시선 목표를 인물·물체가 아닌 빈 공간(negative
    space)에 할당 ("시선은 항상 다음 적진 틈새를 찾음"). ★ (38)
39. **Self-POV paradox lock**: "Camcorder never appears on screen" —
    들고 찍는 주체의 장비를 화면에서 금지. 셀프 POV 장르의 대표 실패를
    부정문 하나로 차단. ★ (40)
40. **컷별 오디오 온오프**: 컷마다 대화를 켜고 끄는 지정 ("No dialogue —
    ambient gym sound only"). 오디오 DNA를 전체가 아닌 컷 단위로.
    ★★ (38·40)
41. **시선의 호(eye-line arc)**: 감정선에 따라 시선을 열고 닫는 구조 —
    감은 눈→시선 없음→상호 응시→일방 응시→시선 단절. 시선의 개폐 자체가
    서사. 2인 감정 장면의 기획 단위. ★ (39)
42. **장르 구조 비트 압축**: K-드라마식 고정 비트(투신→수중 만남→구조→떠남)를
    44초에 압축. 로케이션 자체가 장르 약속. ★ (39)
43. **모델/툴 워터마크 번인**: "AI"·"Dola AI"·"Wavespeed SEEDANCE 2.5" 같은
    번인은 프롬프트로 막을 수 없는 레이어. 납품 전 프레임 확인 필요.
    ★★★ (21·25·32·39)
