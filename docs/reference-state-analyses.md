# Reference State 분석집 — Evidence-First

> XAI-Studio-Video 레퍼런스 추출 양식(`docs/reference-extraction.md`)에 맞춘 분석집.
> 작성: 2026-09-24, 최종 정리: 2026-09-25. 분석: Somni (Muse).
> 원문 규칙: **Visible evidence first. Unsupported inference stays out of the production spec.**

## 증거 기반 표기

총 79건. 증거의 출처는 항목별로 밝힌다: 프롬프트에서 읽은 것은
`prompt-derived`, 영상 설명·작성자 댓글에서 읽은 것은 `author-described`,
실제 영상 프레임에서 본 것은 `frame-derived`, 내가 추론한 것은 `inference`.
추론은 프로덕션 스펙에 넣지 않는다 — 각 항목의 "관찰 vs 추론" 섹션에만 둔다.

- 프레임 분석 항목: 18·19·21·22·23·24·25·26·30·31·32·33·34·35·36(임베드
  스크린샷)·37·38(임베드 스크린샷)·39(직접 다운로드)·40(직접 다운로드)·
  41(임베드 스크린샷)·42(직접 다운로드)·43(직접 다운로드)·44(직접
  다운로드)·45(직접 다운로드)·46(임베드 스크린샷)·47(직접 다운로드)·
  48(직접 다운로드, 2버전)·49(직접 다운로드)·50(직접 다운로드)·51(직접
  다운로드)·52(직접 다운로드)·53(직접 다운로드)·55(직접 다운로드).
  24번은 실패 사례. 52번은 프롬프트가 X 로그인 월 뒤 — 작성자 댓글에
  공개되었으나 미확보, 사용자가 붙여넣으면 보강. 53번은 프롬프트가
  포스트 본문에 전문 공개. 54번은 텍스트 가이드 (영상 없음) —
  본문 말미가 끊겨 있고 이어지는 셀프리플라이 2개는 로그인 월 뒤.
  55번은 프롬프트 미공개 — frame-derived로만 기록. 56번은 텍스트
  가이드 (Threads 스레드, 영상 미확인 — 유튜브 페이지가 reCAPTCHA
  차단). 57번은 사용자 직접 제공 (포스트 전문+프롬프트 전문, 영상은
  사용자 다운로드 후 보강 예정). 58번은 브라우저 공개 시청
  (프레임 미추출, 프롬프트 미공개 — LoRA 데모). 59번은 텍스트
  가이드 (프롬프트 엔지니어링+오케스트레이션 이론, 첨부 영상 1개
  browser-described). 60번은 실사 상업 영상 (일본 이너웨어 모닝
  광고, 프레임 추출) + 클로저 편집 콘티 — AI는 모멘트만 생성하고
  사이는 관객의 뇌에 맡기는 전략. 61번은 중국어 프롬프트 전문
  (광학 줌 단일 운경 고풍 서사, 한국어 번역 포함).
- 기사 기반: 20·29. 프롬프트 표본(영상 미확인): 27·28.
- 39번(@AIwithzayn)은 프롬프트가 X 로그인 월 뒤에 있어 frame-derived로만
  기록. 프롬프트 확보 시 보강 예정.
- 양식 변천: 1–9번은 구 양식(Subject state / Composition / Camera evidence…),
  10–47번은 신 양식(기본 정보 / 관찰 / 관찰 vs 추론 / Control Levels /
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
- 5s: 축구 킥 + 블루 라이트 트레일 — 종목 구간 성립
- 6.8s: 선수 얼굴 클로즈업, 땀방울·림라이트, **렌즈 정면 응시** —
  "eyes lock forward"가 카메라 직시로 렌더. 방송 오프닝 장르 관습
  (#21 계열)
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

## 41. Threads @jeong_do_ryeong — 분노 연기 프롬프트 (감정 문법, 10초)

**기본 정보**
- 출처: Threads @jeong_do_ryeong, 게시 2026-09-26 13:16 KST (공유 링크
  BAZ0OMGoku → /post/DdvJzIpgLNv)
- 포스트 본문: "연기 하는 건 또 물리적인 표현과 달라 많은 연구가 필요할
  것 같습니다 / 연구 중인 프롬프트는 댓글에 있습니다" (author-described)
- 영상: 10.215초 (라이트박스 슬라이더 aria-valuemax 실측), 단일 샷(컷
  없음), 오디오 트랙 존재(라이트박스 언뮤트 확인, 내용 미확인). 영상 URL은
  DOM에서 추출 불가
- 반응: 458 views, 11 likes, 3 replies, 1 repost, 1 share
- 증거 기반: prompt-derived (작성자 셀프 댓글 전문) + frame-derived
  (임베드 스크린샷 4장: 2.59·5.00·7.39·10.215s)
- 비고: #8·#33–37 동일 작성자. 물리 제어 시리즈에서 감정 연기로 확장.
  "Dola AI" 워터마크 우하단 번인

**관찰 — 감정 문법 헤더** (prompt-derived)
- Emotion: anger / Intention: explode / Performance State: manic /
  Trajectory: Explosive — 4필드 헤더. #33의 Universal Action Grammar에
  대응하는 감정 문법
- Trajectory 서술: rising → escalating → explosion → fading

**관찰 — 백분율 페이즈** (prompt-derived + frame-derived)
- Phase 1 [rising] range 0-25: BUILD_UP / agitated /
  control_starts_slipping / speech_rate +1 → 2.59s 프레임: 입 살짝 벌림,
  렌즈 고정, 끓어오르는 긴장 ✓
- Phase 2 [escalating] range 25-55: ESCALATION / manic / control_lost /
  pitch_contour +1, rate_change +1 → 5.00s 프레임: 타이트 클로즈업 고함,
  광기 어린 분노 ✓
- Phase 3 [explosion] range 55-70: BURST / manic /
  emotion_overwhelms_control / trigger: key_phrase / loudness +2,
  vocal_intensity +2 / events: voice_break
- Phase 4 [fading] range 70-100: DECAY / exhausted /
  burst_exhausts_energy / loudness -1 → 7.39s·10.215s 프레임: 고개 숙임→
  무너짐, 얼굴 가림 ✓
- 페이즈를 절대 초가 아닌 백분율로 지정 — #31(비트표 절대 시간 불신)의
  해법. 4개 페이즈 경계가 프레임 4장과 맞아떨어짐

**관찰 — Speech Axes** (prompt-derived)
- 목소리를 5축으로 파라메트릭 제어: speech_rate, pitch_contour,
  rate_change, loudness, vocal_intensity — 축마다 페이즈별 수정자
- axisBias: loudness +2, vocal_intensity +2, rate_change +2 — 축 전체에
  걸리는 마스터 게인

**관찰 — 키 프레이즈 트리거 + 운율 표기** (prompt-derived)
- trigger: key_phrase — 폭발 페이즈의 트리거를 대사 문구에 바인딩
- "왜 이러는지 말을 해보라고.. 왜~~~~ 왜~~~~" — 물결표(~~~~)로 발성
  (울부짖음) 길이를 표기. 말줄임표 호흡 표기(#40 동계열)의 확장
- WORD_VOLUME_SPIKE / WORD_STRESS: key_phrase에 볼륨 스파이크 + 강세 지정

**관찰 — 발화 수행 구조** (prompt-derived)
- Onset: delay=1 hesitation=0 breathBefore=false — 1단위 지연 시작,
  망설임·선행 호흡 없음
- Phrase roles: opening(rising) → middle(escalating) →
  emphasis(explosion) → final(fading) — 대사 구조를 페이즈에 매핑
- Ending: release=0 sustain=0 drop=1 rise=0 — 엔딩 에너지 벡터를 4축으로.
  최종 프레임의 무너진 자세와 일치

**관찰 — 모듈러 참조** (prompt-derived)
- "Coupling: ON (existing speech_coupling text applies)" — 외부 공유
  텍스트 블록을 참조하는 모듈러 프롬프트 구조. XAI-Studio-Video의 마스터
  스펙 철학과 수렴

**관찰 — 시선** (frame-derived)
- rising~explosion: 렌즈 정면 응시 — 카메라는 상대역(2인칭 호소의 대상).
  #40(렌즈=관객)·#12(응시 금지)·#39(렌즈 무관여)와 다른 네 번째 문법:
  렌즈=씬 파트너
- fading: 얼굴 가림, 시선 철수 — 감정의 호가 시선의 호: 고정→격렬→철수
  (#41의 시선 호)

**관찰 vs 추론**
- 관찰: 백분율 페이즈 4개가 프레임 4장과 일치, 키 프레이즈·엔딩 벡터·축
  제어 전부 프롬프트 원문, Dola AI 워터마크
- 미확인: 오디오 내용(트랙 존재만 확인), 빨간 조명의 출처 — 페이즈 4
  프레임에서 배경이 빨갛게 변하는데 프롬프트에 조명 언급 없음. 모델
  해석이거나 다른 모듈일 수 있음
- 추론: 없음

**Production description → Control Levels**
- Hard Lock: 백분율 페이즈 구간, 4필드 감정 헤더, 축 수정자 수치, 키
  프레이즈 원문, 엔딩 벡터
- Soft Guidance: 축 바이어스 값, Onset/Ending 파라미터, 모듈 참조
  (Coupling)
- Creative Freedom: 빨간 조명(출처 미확인 — 명시하거나 빼야 함), 표정의
  미세 디테일

**기여 패턴**: 1 (신규 — 백분율 페이즈: #31 문제의 해법), 2 (신규 —
  Speech Axes 파라메트릭 음성 제어), 3 (신규 — 키 프레이즈 트리거 +
  운율 표기), 4 (신규 — 엔딩 벡터 4축), 5 (신규 — 렌즈=씬 파트너 시선
  문법), 6 (모듈러 참조 — XAI-Studio-Video 수렴), 7 (Dola AI 워터마크 —
  후보 43에 #41 추가)

---

## 42. X @mehvishs25 — 오버헤드 원테이크 루틴 (Seedance 2.5 on Higgsfield, 15초)

**기본 정보**
- 출처: X @mehvishs25 (Meem), 게시 2026-09-26 02:38 UTC (11:38 KST)
- 포스트 본문: "Seedance 2.5 on Higgsfield AI" + 프롬프트 전문
  (author-described)
- 영상: 15.125초, 1280x720, 24fps, 363프레임 (직접 다운로드)
- 반응: 53 likes, 31 replies, 2 reposts, 1473 views
- 증거 기반: prompt-derived (프롬프트 전문) + frame-derived (6프레임:
  1·3·5·9·13·14.5s)
- 비고: Higgsfield = #20 메이킹의 주인공 플랫폼. <image1> 캐릭터
  레퍼런스 바인딩 (#38 동계열)

**관찰 — 카메라: 절대 오버헤드 락** (prompt-derived + frame-derived)
- "POV overhead follow in a strict bird's eye view, locked directly
  above the top of her head at all times, perfectly centered over her
  body from start to finish, floating smoothly with no shake, tilt,
  angle drift, or side offset"
- "passing through ceilings and door frames as one uninterrupted camera
  event" — 카메라는 건축을 통과. 인물만 물리에 묶이고 카메라는 자유
  (Phantom camera)
- 24mm wide, digital clean look
- 프레임 확인: 1·3·5·9s 전부 정수리 직상방, 인물 중앙 고정 ✓. 9s에서
  욕실→주방으로 벽을 통과하는 중 ✓

**관찰 — 카메라에 서사적 정체 부여** (prompt-derived)
- MOOD: "Detached routine turns quietly uncanny, as if an unseen
  presence is floating above her and waiting for her to notice."
- 카메라는 단순 시점이 아니라 캐릭터 — 위에서 떠다니며 그녀가
  알아차리길 기다리는 보이지 않는 존재. 마지막 비트(렌즈 응시)가 그
  존재를 알아차리는 순간으로 수렴

**관찰 — 비트마다 락 재확인** (prompt-derived)
- SCENE의 각 비트가 카메라 관계로 시작: "Sits up under the lens" /
  "Still centered under the lens" / "Under the same overhead lock" /
  "The lens tracks directly above her" / "Still pinned overhead" /
  "Stops exactly under the lens"
- 락을 한 번 선언하고 끝이 아니라 비트마다 재확인하는 문법

**관찰 — 손-소품 배정** (prompt-derived + frame-derived)
- 오른손=담배 전편 고정: "keeps the cigarette in her right hand" 반복.
  "Extends that arm away from the running water" — 물을 틀 때 담배 든
  팔을 멀리 뻗는 소품 보호 동작
- 왼손=작업: 수도꼭지·세수·유리잔. "Turns on the tap with her left
  hand. Splashes water onto her face with her left hand."
- 최종 인벤토리: "Holds the cigarette in her right hand and the glass in
  her left hand" — 14.5s 프레임에서 확인 ✓ (화면 좌=그녀의 오른손 담배,
  화면 우=왼손 유리잔)

**관찰 — 소품 연속성 체인** (prompt-derived)
- 담배+라이터 줍기 → 입에 물기 → 불 붙이기(3s 프레임에서 라이터 불꽃
  확인 ✓) → 라이터는 매트리스에 떨굼 → 담배는 전편 휴대 → 주방에서
  유리잔 추가. 라이터는 탈락, 담배는 생존 — 소품별 생애주기

**관찰 — 파이널 비트 7연타** (prompt-derived + frame-derived)
- "Stops exactly under the lens. Freezes. Looks right. Looks left.
  Takes a drag from the cigarette. Snaps her head straight up into the
  lens. Blows smoke toward the camera. Locks eye contact."
- 13s: 고개 치켜들고 렌즈 응시 ✓ / 14.5s: 카메라를 향해 연기 뿜기, 눈
  맞춤 고정 ✓
- 전편 유일의 렌즈 응시를 클라이맥스로 배치 — 응시의 희소성이 공포 문법

**관찰 — 시선** (frame-derived)
- 1~13s: 렌즈를 단 한 번도 안 봄. 시선은 아래·작업 대상에만
  (detached). 시선 회피가 "unseen presence"의 존재감을 키움
- 13s→14.5s: 오른쪽→왼쪽 확인 후 렌즈로 스냅, 연기 뿜으며 눈 맞춤
  고정. 다섯 번째 시선 문법: 렌즈=unseen presence, 응시=정체 드러남
  (#41 렌즈=씬 파트너의 변주 — 여긴 적대가 아니라 목격)

**관찰 — COLOR LOGIC 한 줄** (prompt-derived + frame-derived)
- "COLOR LOGIC: Matrix Green Look" — 네임드 그레이드를 한 줄로 고정.
  프레임의 그린 네온·블라인드 빛과 일치 ✓

**관찰 — SFX 인벤토리** (prompt-derived)
- "SFX: lighter flick, inhale, faint city hum, refrigerator buzz, soft
  bare footsteps, water run." + 파티클("Sodium amber particles, toxic
  green neon reflect off tile, smoke, bottles, and damp surface")

**관찰 vs 추론**
- 관찰: 15.1초 원테이크, 오버헤드 락 전편 유지, 손-소품 배정 일치,
  파이널 7연타 프레임 일치, 그린 룩 일치
- 미확인: 오디오 내용
- 추론: 없음

**Production description → Control Levels**
- Hard Lock: 정수리 직상방 절대 고정·중앙 유지, 오른손 담배·왼손 작업,
  파이널 7연타 순서, Matrix Green Look
- Soft Guidance: 24mm wide·digital clean, 방 구조(매트리스→복도→욕실→
  주방), SFX 목록
- Creative Freedom: 담배 연기의 모양, 세수의 물튀김 정도, 표정의 미세 변화

**기여 패턴**: 1 (신규 — Camera-as-presence: MOOD로 카메라에 서사 정체
  부여), 2 (신규 — Phantom camera: 건축 통과), 3 (신규 — 비트마다 락
  재확인), 4 (신규 — Handedness lock + 소품 보호 동작), 5 (신규 —
  COLOR LOGIC 한 줄), 6 (신규 — 파이널 비트 7연타: 유일 응시를
  클라이맥스로), 7 (<image1> 바인딩 #38 동계열)

---

## 43. X @aiwithaayat — 로드트립 우정 필름 (Seedance 2.0, 32초)

**기본 정보**
- 출처: X @aiwithaayat (Ayat), 게시 2026-09-26 04:21 UTC (13:21 KST)
- 포스트 본문: "Some moments are never planned..." + "Created on seedance
  2.0" + 프롬프트 전문 (author-described)
- 영상: 32.2초, 848x550, 30fps, 966프레임 (직접 다운로드). "30-second"
  주장과 대략 일치
- 반응: 137 likes, 50 replies, 7 reposts, 1039 views
- 증거 기반: prompt-derived (프롬프트 전문, 1385자·단일 문단) +
  frame-derived (6프레임: 2·6·10·18·26·30s)
- 비고: 사용자가 "프롬프트는 간단한데 시점 처리가 완벽해"라고 지정한
  사례. Seedance 2.0 (2.5 아님)

**관찰 — 단순 프롬프트** (prompt-derived)
- 단일 문단, 샷 번호·타임스탬프·기술 스펙 없음. 카메라 큐가 서술 안에
  내장: "playful low-angle shot from inside a shopping cart",
  "intimate close-up moments", "dynamic cinematic shots", "smooth
  tracking shots"
- "keeping their faces, hairstyles and outfits consistent throughout
  the video" — 일관성 지시를 한 줄로. 32초·6셋업에서 두 얼굴 유지됨 ✓

**관찰 — Diegetic camera seat** (frame-derived)
- 매장: 카메라가 카트 안에 있음 — 전경에 카트의 캔들(아웃포커스), 그
  너머 두 친구 (6s). "from inside a shopping cart"를 말로만 하지 않고
  전경 물건으로 증명
- 차: 뒷좌석 시점의 투샷 — 운전자의 뒷모습 + 조수석이 운전자를 보는
  구도, 윈드실드 너머 골든아워 (10s)
- 전망대: 카메라가 풍경의 자리에 — 차는 작게, layered hills와 오렌지
  하늘이 주인공 (18s)
- 밤: 손/캔 매크로 (26s) → 스트링 라이트 보케 속 얼굴 클로즈업 (30s)
- 카메라는 매 장소의 네이티브 자리를 차지 — 항상 참여자, 이방인 아님

**관찰 — 시간대 아크** (prompt-derived + frame-derived)
- 낮(밝은 매장) → 골든아워(드라이브) → 일몰(전망대) → 밤(스트링
  라이트). 편집 로직을 컷이 아니라 빛의 진행이 담당
- 프롬프트의 서술 순서가 그대로 시간대 순서

**관찰 — 시선** (frame-derived)
- 매장: 친구끼리 상호 응시 + 카메라를 향한 장난스러운 피스사인 (2s) —
  카메라는 가벼운 확인 대상
- 차: 조수석이 운전자를 봄, in-world 상호 시선 (10s)
- 전망대: 풍경을 향한 시선 (18s)
- 밤: 두 사람이 함께 폰을 봄 — 공동 시선, 이름 붙은 동일 목표점 (30s)
- 여섯 번째 시선 문법: 카메라는 참여자-관찰자. 지속적인 렌즈 응시 없이도
  친밀감이 유지됨 (#40의 전편 응시와 대조)

**관찰 vs 추론**
- 관찰: 6개 셋업 전부 프롬프트 서술과 일치, 두 얼굴 32초 일관, 카트 전경
  POV·시간대 아크 프레임 확인
- 미확인: 오디오, 14·22s 프레임 (드라이브 외부 샷으로 추정)
- 추론: 없음

**Production description → Control Levels**
- Hard Lock: 두 인물의 얼굴·헤어·의상 일관, 시간대 순서
  (낮→골든아워→일몰→밤), 카트 내부 시점
- Soft Guidance: "cinematic lifestyle", "warm, natural and nostalgic",
  필름 그레인·얕은 심도
- Creative Freedom: 각 셋업의 구체 구도, 캔들의 배치, 표정 디테일

**기여 패턴**: 1 (신규 — Diegetic camera seat: 매 장소의 네이티브 자리),
  2 (신규 — Foreground POV proof: 전경 물건으로 시점 증명), 3 (신규 —
  시간대 아크: 빛의 진행이 편집 로직), 4 (일관성 한 줄 지시의 검증 사례 —
  32초·6셋업 두 얼굴 유지), 5 (Seedance 2.0 단순 프롬프트 성공 사례)

---

## 44. X @itxsarmadd — WATERBENDING AMBUSH (Seedance 2.5, 10초)

**기본 정보**
- 출처: X @itxsarmadd (Sarmad Tahir), 게시 2026-09-26 03:55 UTC
  (12:55 KST)
- 포스트 본문: "This AI video is absolutely amazing 🔥 Created with
  Seedance 2.5" + 프롬프트 전문 (author-described)
- 영상: 10.1초, 1280x720, 30fps, 303프레임 (직접 다운로드). "exactly 10
  seconds" 주장과 대략 일치
- 반응: 58 likes, 50 replies, 5 reposts, 788 views
- 증거 기반: prompt-derived (프롬프트 전문, 3603자) + frame-derived
  (4프레임: 1·3·5·9s)
- 비고: 사용자가 "물 마법이 그럴듯해 보여"라고 지정. ARMAN 캐릭터 + 5명의
  갑옷 적, 정글 사원

**관찰 — 단일 연속 질량** (prompt-derived + frame-derived)
- "Water remains a single continuous moving mass." — 물은 전편 하나의
  질량. 순간이동·소멸·재생성 없음
- "The main water mass whips around him with believable inertia" —
  관성을 가진 채 휘감김
- 프레임: 1s 몸을 감는 소용돌이 → 3s 허리 높이 회전 → 5s 측면 타격으로
  적 날아감 → 9s 다음 적을 향해 가속. 물의 위치가 연속적으로 이어짐 ✓.
  그럴듯함의 첫 번째 출처

**관찰 — 샤드 생명주기** (prompt-derived + frame-derived)
- "Several sections split from the moving water, instantly freeze into
  sharp ice shards, and fire" — 분리→동결→발사의 3단계 상태 전이. 질량
  보존 (#35·#36 동계열)
- 1s 프레임에서 물기둥에서 분리된 얼음 파편 확인 ✓

**관찰 — Grounded negatives** (prompt-derived)
- "No glowing effects, energy beams, neon trails, or anime aura." /
  "grounded CGI" / "realistic water physics" / "seamless VFX integration,
  no digital-art appearance"
- 판타지를 실사 물리로 렌더 — "그럴듯해"의 두 번째 출처

**관찰 — 절대 타임스탬프 비트** (prompt-derived + frame-derived)
- 0.0–2.5 SURROUNDED / 2.5–5.0 ROTATING PRESSURE / 5.0–7.5 WATER IMPACT /
  7.5–10.0 COMBO CONTINUES
- 프레임 매칭: 1s 포위 ✓ / 3s 회전 ✓ / 5s 측면 타격 ✓ / 9s 콤보 지속 ✓
- #31(절대 시간 불신)·#41(백분율 해법)과 대조 — 10초 단尺에서는 절대
  타임스탬프도 비트가 맞았음. 관찰로만 기록

**관찰 — END BEFORE IMPACT** (prompt-derived + frame-derived)
- "END BEFORE IMPACT. SMASH CUT. ACTION INTERRUPTED MID-COMBO. END." /
  "Final frame preserves active combat momentum for Scene 02."
- 9s 최종 구간: Arman이 물을 적에게 가속하는 중 — 임팩트 직전 정지 ✓.
  해결 없는 엔딩, 시리즈 연결용

**관찰 — 적 AI 부정문** (prompt-derived)
- "Five active enemies remain engaged throughout." / "No enemy stands
  and watches." — #7·#33의 anti-cheat 동계열
- "Combat never slows down." / "zero pauses, zero idle moments" /
  "Every action directly causes the next event." / "Fight begins
  mid-combat" (in medias res)

**관찰 — 레퍼런스 3분리** (prompt-derived)
- IMAGE 1 ARMAN (인물) / IMAGE 2 MASTER ENVIRONMENT SHEET (환경) /
  IMAGE 3 ENEMY REFERENCE (적) — 각각 "preserve exactly". #38 동계열

**관찰 — 카메라가 젖음** (prompt-derived)
- "occasional water spray crossing lens" — 카메라가 전투 공간 안에 있음.
  "No floating virtual camera." 리액티브 핸드헬드

**관찰 — 오디오 부정문** (prompt-derived)
- "SOUND: Raw action only... NO MUSIC." #38 동계열

**관찰 — 시선** (frame-derived)
- 전투 시선: Arman은 위협을 보고, 적들은 Arman을 봄. 상호 전투 응시.
  카메라는 응시 대상 아님 — #12 계열 (액션은 렌즈를 보지 않음). 일곱
  번째 시선 문법: 전투 할당 시선

**관찰 vs 추론**
- 관찰: 물의 연속성·샤드 생명주기·비트 매칭·END BEFORE IMPACT 전부 프레임
  일치, grounded 룩 확인
- 미확인: 오디오, 7s 프레임
- 추론: 없음

**Production description → Control Levels**
- Hard Lock: 물=단일 연속 질량, 샤드 3단계 전이, 적 5명 전편 교전, END
  BEFORE IMPACT, grounded negatives
- Soft Guidance: 정글 사원 환경, 리액티브 핸드헬드, raw action 사운드
- Creative Freedom: 물보라의 모양, 적의 갑옷 디테일, 모션 블러 강도

**기여 패턴**: 1 (신규 — 단일 연속 질량: 그럴듯함의 출처), 2 (신규 — 샤드
  생명주기), 3 (신규 — Grounded negatives), 4 (신규 — END BEFORE IMPACT),
  5 (신규 — In medias res: mid-combat 시작), 6 (적 AI 부정문 #7·#33
  동계열), 7 (레퍼런스 3분리 #38 동계열), 8 (절대 타임스탬프가 10초尺에서
  맞은 사례 — #31·#41과 대조되는 관찰)


---

## 45. X @doctorwasif — CHASE 코어데이 짐 브이로그 (Seedance 2.5, 15초)

**기본 정보**
- 출처: X @doctorwasif (WasifAI), 게시 2026-09-25 13:26 UTC (22:26 KST)
- 포스트 본문: "made with Seedance 2.5" + 프롬프트 전문
  (author-described)
- 영상: 15.08초, 1280x720, 24fps, 362프레임 (직접 다운로드)
- 반응: 631 likes, 57 reposts, 34 replies, 33364 views — #40(후속편)보다
  큰 반응
- 증거 기반: prompt-derived (프롬프트 전문, 2314자) + frame-derived
  (6프레임: 1.5·4·6.5·9·11.5·13.5s)
- 비고: #40의 원본(전편). 사용자가 "이것도 좋네"라고 지정

**관찰 — Deliberate imperfection** (prompt-derived + frame-derived)
- CAMERA: "Hand shake, misaligned framing, delayed focus pulls, clumsy
  zooms, occasional face cut-off framing, imperfect shots"
- LOOK: "Soft, slightly blurry tape quality, faint tape noise, bloomed
  highlights under gym lighting, flickering auto-exposure, muted
  contrast, realistic skin tones"
- 불완전함을 스펙으로 명시 — MiniDV 룩의 핵심. #40 동계열

**관찰 — Propped camera grammar** (prompt-derived + frame-derived)
- "POV of CHASE holding the camera herself, occasionally propping it on
  the floor or a mat for hands-free core shots"
- 컷별 카메라 모드: 1 propped / 2 propped / 3 propped / 4 macro insert /
  5 handheld / 6 arm's-length selfie
- 셀프 POV 역설의 물리적 해법: 손이 필요하면 카메라를 내려놓는다
- 13.5s: 암즈렝스 셀피 — 그녀의 팔이 프레임 안에 (카메라를 든 팔).
  기기는 안 보이지만 든 손은 보임. "Camcorder never appears on
  screen"(#40)의 완성형

**관찰 — 6컷 스토리보드** (prompt-derived + frame-derived)
- 15s/6컷, 컷마다 길이·카메라·액션·대사 지정. 6컷 전부 프레임 매칭 ✓
  (1.5s 한숨 / 4s 플랭크 / 6.5s 크런치 / 9s 손 매크로 / 11.5s 드러눕기 /
  13.5s 셀피 피날레)

**관찰 — Cut-level audio** (prompt-derived)
- 컷 4: "No dialogue — ambient gym sound only" — 손 매크로 인서트는 대사
  없이. #40 동계열

**관찰 — 대사 전달 지정** (prompt-derived)
- "(strained)" "(breathless)" / "talking through gritted teeth" /
  "complaining between reps" — #41 Speech Axes의 산문 버전

**관찰 — 톤 가드레일** (prompt-derived)
- "Playful, self-deprecating gym-vlog tone — genuine strain mixed with
  humor" / "energy staying light and funny throughout rather than fully
  exhausted" — 감정 아크의 상한선

**관찰 — 의상 스펙** (prompt-derived + frame-derived)
- "Modest long-sleeve athletic top... (arms and torso fully covered)...
  no jewelry" + "loose joggers or fitted leggings" 중 택일 — 렌더는
  레깅스 선택 ✓

**관찰 — 시선** (frame-derived)
- 여덟 번째 시선 문법: 셀프 브이로그 — 렌즈 = 그녀 자신의 시청자. 전편
  렌즈를 보고 말함 (#40과 동일 문법)
- 유일한 예외는 컷 4 (손 매크로) — 카메라는 노력의 증거를 보고, 대사는
  없음

**관찰 vs 추론**
- 관찰: 6컷 전부 프레임 일치, propped/handheld/selfie 카메라 모드 전부
  확인, imperfection 룩 확인
- 미확인: 오디오, 대사 립싱크
- 추론: 없음

**Production description → Control Levels**
- Hard Lock: CHASE 캐릭터, 6컷 스토리보드, 컷별 카메라 모드, 불완전함
  스펙, 의상 커버리지
- Soft Guidance: MiniDV 룩, 톤 가드레일, 대사 전달
- Creative Freedom: 땀의 정도, 물병 위치, 조명 디테일

**기여 패턴**: 1 (신규 — Deliberate imperfection spec), 2 (신규 — Propped
  camera grammar: held/propped 두 모드), 3 (신규 — Cut-level audio),
  4 (#40의 원본 — CHASE 크로스 크리에이터 시리즈의 시작점), 5 (대사 전달
  지정 — #41 동계열 산문 버전), 6 (톤 가드레일: 감정 아크의 상한선)


---

## 46. Threads @imhealingmachine — 스카이 파이럿 액션 코미디 (Seedance 2.5, 30초)

**기본 정보**
- 출처: Threads @imhealingmachine (verified, "AI Threads"), 게시
  2026-09-26 (페이지 표기 8:29 PM KST)
- 포스트: 9단계 제작 파이프라인 공개 (캡션) + Midjourney 캐릭터 프롬프트
  (답글 1) + Seedance 2.5 프롬프트 전문 (답글 2, author-described)
- 영상: 31.3초 (플레이어 슬라이더 31.299093s), painterly sci-fi
  sky-pirate action-comedy, 12샷/11컷
- 반응: 7 likes, 2 comments, 1 repost, 1 share
- 증거 기반: prompt-derived (프롬프트 전문) + frame-derived (임베드
  스크린샷 5장: 0·7.8·15.7·23.5·29.2s)
- 비고: "본 영상은 Newtake의 지원을 받아 제작" — #3·#20의 Newtake 연결.
  사용자의 취향(만화식 컷 문법+실사 렌더, #27)과 직결되는 사례

**관찰 — 9단계 파이프라인** (caption-derived)
- 1. Midjourney 캐릭터 제작 → 2. GPT 스토리 기획 → 3. GPT 프롬프트 제작
  → 4. 480p 30초 초안 → 5. GPT 프롬프트 수정 → 6. 480p 최종 → 7. 720p
  최종 → 8. 2~3 클립 편집 → 9. Topaz 1080p 업스케일
- "1번 단계에 가장 시간을 많이 써요... 이미지를 눈으로 봐야 제작할
  영상이 떠오르더라구요" — image-first, asset-first (#20 동계열)

**관찰 — Midjourney 캐릭터 파이프라인** (reply-derived)
- "--sref 4255785265 --profile z7c2z8i kc68erk --stylize 500 --hd --v 8.2"
  — 두 캐릭터 프롬프트에 동일 sref로 스타일 통일
- "시댄스에서 영상화 느낌이 잘 나오는 조합" — Seedance로 잘 옮겨지는
  Midjourney 조합을 이미 확보

**관찰 — Enemy arithmetic** (prompt-derived)
- "six rounds, no reload. First hit: one enemy becomes two. Next two
  shots... four. Final three hits... five, six, seven."
- "Only the struck enemy recoils and splits into TWO solid bodies; the
  original becomes the pair, never a third figure."
- "Three pursuers fall; four stay aboard and merge into one." / "Fallen
  enemies never teleport back."
- 수의 보존: 1→2→4→5→6→7→4→1. #60 샤드 생명주기의 적 버전

**관찰 — CUT ON [action]** (prompt-derived)
- 11개 컷 전부 액션 트리거: "CUT ON her rising shoulder" / "CUT ON his
  backward recoil" / "CUT ON their synchronized stare" ...
- #1의 CUT-as-trigger를 12샷 구조로 일반화

**관찰 — Shooting axis lock** (prompt-derived)
- "Initially captain screen-left, enemy screen-right... Preserve the
  shooting axis." / SHOT 03 "staying on the established side of the
  axis" — #28 master-axis의 명시적 선언

**관찰 — Ammo economy** (prompt-derived)
- "six rounds, no reload" → "two dry clicks" → "fully seats the revolver
  in her right-hip holster and releases it" → "The gun remains holstered"
- 소품의 총량을 12샷 전체에 걸어 잠금

**관찰 — Pre-planted board** (prompt-derived)
- "already hovers below the escape edge, concealed by hull and framing
  until Shot 11" / SHOT 10 "Keep the board below frame"

**관찰 — No fixed beauty pose** (prompt-derived)
- "Exaggerate her expressions as directed in each shot while preserving
  her face. Expressions visibly respond to discoveries; no fixed beauty
  pose."

**관찰 — Animation principles** (prompt-derived)
- "selective speed smears, hair and fabric follow-through; effects never
  hide impacts" / "Cuts continue actions without resetting"
- 만화 애니메이션 원리를 프롬프트에 직접 기입

**관찰 — Music direction** (prompt-derived)
- "Music drops for the clicks, then percussion resumes" / "accelerates
  during the sprint, lifts at escape, then yields to a low
  reverse-suction sound for the final merge"

**관찰 — 절대 타임스탬프 검증** (frame-derived)
- 12샷의 시간대 [0-2s]...[27-30s]가 5개 스크린샷과 전부 매칭 ✓ (0s
  랜딩 / 7.8s 쇼크 클로즈업 / 15.7s 트래킹 마스터 / 23.5s 도약 /
  29.2s 탈출)
- #44에 이은 두 번째 사례: 30초尺에서도 절대 타임스탬프가 통함

**관찰 — 최종 머지 미확인** (frame-derived)
- 29.2s 프레임에서 4명의 적이 아직 합쳐지지 않음 — 마지막 ~2초의 머지
  장면은 프레임으로 미확인

**관찰 — 시선** (frame-derived)
- 전투 할당 시선 (#44 계열): 그녀는 적을 조준, 적들은 그녀를 봄. 과장된
  리액션 표정과 결합
- SHOT 12: 합쳐진 적이 "tilts his X-eyed mask toward the distant
  captain" — 시선으로 다음 씬을 예고

**관찰 vs 추론**
- 관찰: 12샷 구조·적 산수·컷 트리거·축 고정 전부 프롬프트 명시, 5개
  스크린샷과 샷 매칭 확인
- 미확인: 오디오, 최종 머지 장면 (29.2s 이후), Midjourney 이미지와 렌더의
  일치도
- 추론: 없음

**Production description → Control Levels**
- Hard Lock: 적의 수 (1→2→4→5→6→7→4→1), 6발 노리로드, CUT ON 트리거,
  슈팅 축, 보드 사전 배치
- Soft Guidance: painterly 스타일, 과장된 표정, 음악 방향
- Creative Freedom: 구름·도시 디테일, 코트 펄럭임의 정도

**기여 패턴**: 1 (신규 — Enemy arithmetic), 2 (신규 — CUT ON [action]
  11연), 3 (신규 — Shooting axis lock), 4 (신규 — Ammo economy), 5 (신규
  — Pre-planted board), 6 (신규 — No fixed beauty pose), 7 (신규 —
  Animation principles in prompt), 8 (신규 — Resolution stepping
  파이프라인), 9 (Midjourney→Seedance 캐릭터 파이프라인), 10 (Newtake
  지원 크리에이터 — #3·#20 연결)


---

## 47. MeiGen @AIwithSarah_ — 145 BPM 비트-싱크 루틴 (Seedance, 15초)

**기본 정보**
- 출처: meigen.ai "Free AI Prompts Gallery" — 영상 프롬프트는 전부
  Seedance. Videos 카테고리 인기순 3위 (206 likes)
- 프롬프트: "FORMAT: 15s / 145 BPM / 15 SHOTS / beat-synced routine"
  (Sarah @AIwithSarah_, author-described). 예시 영상 제공
- 영상: 15.1초 (363프레임, 약 24fps, 1280x720, 직접 다운로드).
  MeiGen "AI" 워터마크 좌상단
- 증거 기반: prompt-derived + frame-derived (초 단위 15프레임 추출,
  주요 샷 6프레임 확인)

**관찰 — BPM header** (prompt-derived)
- "FORMAT: 15s / 145 BPM / 15 SHOTS / beat-synced routine" — 길이·템포·
  샷 수를 포맷 선언에. #14의 MASTER BEAT SYSTEM과 다른 구현: 음악 템포가
  샷 구조의 상위 선언

**관찰 — 샷별 렌즈 + 카메라 문법** (prompt-derived)
- "SHOT 1: ECU, 85mm push-in" / "SHOT 5: Interior fridge view, 24mm
  wide" / "SHOT 8: Bird's-eye insert, 35mm overhead" — 샷마다 사이즈·
  렌즈 mm·무브먼트. #30의 비트별 렌즈와 동계열

**관찰 — Edit-grammar transitions** (prompt-derived)
- 컷 연결 어휘: Sound bridge (12), Smash cut (13), L-cut (15), Match cut
  (4, 7, 10), Cut on action (3, 8), Rhythmic cut (2, 9, 14), Camera wipe
  (9), Object pass (5). #46의 CUT ON [action]이 편집실 문법으로 확장된
  형태

**관찰 — Per-shot SFX** (prompt-derived)
- 각 샷 끝에 "/ SFX:" — "alarm, sheet rustle" (1) / "mattress bounce,
  blanket whip, sharp breath" (2) / ... / "door shut, bag drop, fabric
  rustle, blanket rustle, room tone" (15). 오디오가 샷 설계의 일부

**관찰 — LOGIC RULE** (prompt-derived)
- "Keep logical consistency in wardrobe, props, locations, and action
  continuity across all shots." — 일관성 마스터 스위치 한 줄. #26의
  ACTION DIFFERENCE LOCK보다 거친 입자

**관찰 — MOOD arc + COLOR LOGIC** (prompt-derived)
- "Late-for-work panic, clipped momentum, breathless urgency, then an
  exhausted exhale" — 4비트 감정 아크 한 줄
- "COLOR LOGIC: Hyperreal Pop Look" — #42의 Matrix Green Look과 같은
  한 줄 컬러그레이드

**관찰 — Day-cycle bookend** (prompt+frame-derived)
- SHOT 1 "06:50 on the phone screen" (프레임 01: 주름진 침대 위 폰,
  06:50 표시 ✓) → SHOT 15 "bedroom in cool window light... collapsing
  into bed in the opening frame shape" (프레임 15: 쿨톤 침실, 잠옷으로
  침대에 붕괴 ✓)
- 하루의 아크 + 첫 프레임 모양으로 돌아오는 원형 구성. #43의 시간대
  아크 동계열

**관찰 — 의상 연속성 유지** (frame-derived)
- 샷 1~8: 핑크 스트라이프 잠옷 티 (세면대·주방 프레임 ✓) → 샷 11~14:
  블랙 테일러드 재킷 (지하철 폴대 프레임 ✓) → 샷 15: 잠옷 복귀 ✓.
  LOGIC RULE이 렌더에서 지켜짐

**관찰 — 샷 매칭** (frame-derived)
- SHOT 3 세면 (프레임 03 ✓, 물방울) / SHOT 7 주방 토스트+시계 흘긋
  (프레임 06 ✓) / SHOT 10 레이스업 부츠 인서트 (프레임 09 ✓) /
  SHOT 12 지하철 폴대+크롬 반사 (프레임 11 ✓)
- SHOT 12의 "closing doors를 향한 tense glance"는 반사에 가려진 얼굴로
  렌더 — 시선 지시가 반사 샷으로 흡수됨

**관찰 — 폰 UI 난독 텍스트** (frame-derived)
- 프레임 01의 폰 화면: "Mstrday, Rensey 11 0Y", "NTRE ET" — #30과 동일한
  텍스트 번짐. 날짜·요일 텍스트는 렌더 불가 영역

**관찰 — 시선** (frame-derived)
- 작업 고정 시선: 그녀는 대부분 과제에 시선을 둠. SHOT 4 "mirror eye"
  (양치하며 거울 응시) — 거울을 통한 간접 시선
- 렌즈 직접 응시 없음. #40/#45 셀프 브이로그와 대조: 같은 1인칭 일상
  소재지만 여기는 관찰자 카메라

**관찰 vs 추론**
- 관찰: 15샷 구조·샷별 렌즈·SFX·전환 어휘 전부 프롬프트 명시, 6개
  프레임과 샷 매칭 확인, 의상 아크·하루 아크 렌더에서 유지 확인
- 미확인: 오디오 (145 BPM 음악과의 실제 싱크), 나머지 9개 샷의 렌더
- 추론: 없음

**Production description → Control Levels**
- Hard Lock: 15s/145 BPM/15 SHOTS 포맷, 샷별 액션+SFX, LOGIC RULE,
  의상 아크 (잠옷→외출복→잠옷), 06:50 오프닝
- Soft Guidance: Hyperreal Pop Look, 감정 아크, 샷별 렌즈 mm
- Creative Freedom: 소품 디테일, 물방울·반사의 정도, 도시 풍경

**기여 패턴**: 1 (신규 — BPM header), 2 (신규 — Per-shot SFX), 3 (신규 —
  Edit-grammar transitions), 4 (신규 — LOGIC RULE), 5 (신규 — Day-cycle
  bookend), 6 (신규 — Insert-shot economy), 7 (신규 — MOOD arc line),
  8 (폰 UI 난독 텍스트 — #30 재확인), 9 (MeiGen 갤러리라는 새 소스)

---

## 48. @xazinga_com — 마왕 vs 성기사 30초 실사 검투 (Seedance 2.5, 2버전)

**기본 정보**
- 출처: X @xazinga_com (verified), 2026-09-26 17:09 KST 게시
- 포스트 본문 (author-described): "코덱스에서 마왕님과 가영이 액션스쿨중..
  CODEX 훈련중. 첫번째 애니메이션 칼 액션 프롬프트 실사화로 변경해서 나온
  영상. 실사화하면서 액션의 움직임이 현실가능한 부분으로 다운그레이드..
  이팩트 살려달라고 요청하고 액션도 추가 요청한 영상"
- 프롬프트: 작성자 셀프 리플라이에 전문 공개 (한국어). "30초 실사 IMAX
  초고속 신급 검투. 마왕과 대천사가 강림한 성기사의 정면 격돌"
- 영상: 2-video carousel. v1·v2 모두 30.1초 실측 (722프레임, 24fps,
  1280x720, 직접 다운로드 — X blob URL이라 vxtwitter API 경유 확보)
- 모델: Seedance 2.5 (포스트에서 craisee.com 언급, 50% 할인 중이라고 밝힘)
- @Arvin007o 언급: "이런 화려한 액션은 @Arvin007o 의 프롬프트를 자주
  참고합니다" — #49와 직접 연결되는 사슬
- 증거 기반: prompt-derived (셀프리플라이 전문) + frame-derived (두 영상
  초단위 프레임) + author-described (포스트 본문)

**관찰 — 속도 수치화** (prompt-derived)
- "매초 3–5회의 선명한 검격 교환을 목표로 한다. 각 3초 구간에 약 9–15회의
  공격·차단·회피·반격이 연속된다"
- 횟수의 정의까지 명시: "횟수는 실제 칼의 새로운 공격 궤적으로 보여준다.
  같은 자세에서 섬광만 반복하지 않는다" — 수치+반례를 한 쌍으로 잠금
- #47의 "15s / 145 BPM / 15 SHOTS" 포맷 선언과 동계열: 속도가 형용사가
  아니라 스펙

**관찰 — 10비트 구조** (prompt-derived)
- 0–3 / 3–6 / … / 27–30, 10개 비트. 각 비트마다 액션 + 카메라 한 쌍
- 비트 제목: 첫 프레임 신급 충돌 → 지면을 찢는 고속 추격 → 검은 폭풍과
  황금 광익 → 석주를 박차는 공중 연참 → 낙하하면서 검격 난무 → 착지 즉
  초근접 폭연 → 마왕의 압도적인 흑검 연타 → 대천사 성광 폭발과 황금 연참 →
  초고속 교차 돌진 → 전장을 뒤집는 최종 격돌
- "두 인물은 첫 프레임부터 이미 최대 전투 상태다. 등장 의식, 변신 장면,
  힘을 모으는 대기 장면 없이 곧바로 검이 충돌한다" — 0초 앵커를 금지
  리스트가 아니라 긍정 선언으로

**관찰 — 상시 오라** (prompt-derived)
- "두 사람의 오라는 공격할 때만 켜지는 효과가 아니다. 이동, 방어, 회피,
  피격과 반격 중에도 계속 유지된다. 강한 공격에서 더 크게 폭발한 뒤에도
  기본 오라는 사라지지 않는다"
- 트리거형 이펙트(때리면 켜짐)를 원천 차단. 상태(state)가 아니라
  속성(property)으로 선언

**관찰 — 이펙트 4층 분리** (prompt-derived)
- "검날은 선명한 중심선. 검기는 그 중심선에서 뻗는 거대한 힘. 충격 폭발은
  실제 접촉점에서 발생한다. 환경 파괴는 검기와 충격파가 도달한 뒤 발생한다"
- "이펙트가 화면 대부분을 채우는 순간에도 두 사람의 실루엣과 검의
  교차점이 남아 있어야 한다" — 가독성의 하한선을 명시

**관찰 — 물리·촬영 섹션** (prompt-derived)
- "주요 접촉 직전 카메라가 극히 짧게 안정되어 충돌을 읽히고, 접촉 후 힘의
  방향으로 밀린다. 상시 무작위 흔들림은 없다"
- "파편과 물은 충격으로 날아간 뒤 중력에 따라 떨어진다"
- "바닥의 균열, 잘린 석주와 잔해는 다음 구간에도 남는다" — damage
  persistence를 비트 경계 너머로 선언 (#49의 打斗痕迹累积과 동형)

**관찰 — 금지 리스트** (prompt-derived)
- 느린 칼싸움, 검을 맞댄 정지 힘겨루기, 제자리 팔 휘두르기, 섬광만 반복,
  대치·준비자세·기모으기, 공격할 때만 켜지는 오라, 작고 약한 검기,
  마기/성광 소실, 임의 색 오라, 인물 복제, 실체 검 복제, 슬로모션·불릿
  타임·hit-stop·명중 정지, 얼굴·검 식별 불가 흐림, 전체화면 순백/순흑,
  게임 컷신 표면, 무중력 파편, 자동 복구 지형, 텍스트·UI·워터마크·로고
- 실패 모드를 이렇게까지 열거한 프롬프트는 코퍼스에서 #19(실패 기반
  네거티브) 이후 처음

**관찰 — 오디오 + 종료 조건** (prompt-derived)
- 오디오: "초당 3–5회 검격에 맞춘 빠르고 선명한 금속 충돌음… 대사,
  내레이션, 자막 없음"
- 종료: "두 사람이 다음 검격을 향해 고속 재접근하는 도중 종료. 멈춤,
  대치, 승리 포즈 없음" — 끝맺음도 상태 전이의 일부로 규정

**관찰 — v1 vs v2 대조** (frame-derived)
- v1 (실사화 다운그레이드): 낮, 돌다리 위 갑옷 기사(방패) vs 뿔 달린 흰셔츠
  남성. 검은 마기·황금 성광·광익 없음. 프롬프트의 이펙트 스펙이 렌더에서
  제거됨 — "현실가능한 부분으로 다운그레이드"가 그대로 반영
- v2 (이펙트 버전): 밤의 고대 유적, 달, 검은 연기(마왕 측) vs 황금 광익
  (성기사 측, 프레임 15s에서 날개 확인), 검 충돌 지점 불꽃. 프롬프트의
  "검은 마기 vs 황금 성광" 2색 대립이 렌더됨
- 두 영상 모두 정확히 2인 유지, 실체 검 1자루씩 (복제 없음 ✓)
- v1 프레임 01s: 이미 공중에서 검이 맞붙는 중 — "첫 프레임부터 최대
  전투" 렌더 확인
- v1의 배경이 01s(돌다리)와 10s(어두운 암석 지형)에서 다르게 보임.
  프롬프트는 "전체 30초 동안 같은 전장"을 요구 — 동일 전장 내 이동인지
  장면 전환인지는 초단위 프레임만으로 단정 불가 (미확인으로 둠)

**관찰 vs 추론**
- 관찰: 프롬프트 전문(셀프리플라이), v1·v2 각 30.1초 실측, 이펙트
  on/off 대조, 10비트·속도 수치·상시 오라·4층 분리·금지 리스트 전부
  프롬프트 명시, 2인/1검 유지와 첫 프레임 전투 상태는 프레임 확인
- 미확인: 오디오 실제 싱크, 10비트 각각의 렌더 매칭 (초단위 프레임만
  확인), v1 배경 변화의 성격
- 추론: "v2가 이펙트 요청의 결과물"이라는 연결은 포스트 본문의 서술 순서
  + 내용에 근거 (author-described에 준함)

**Production description → Control Levels**
- Hard Lock: 2인 고정 (마왕/성기사), 실체 검 1자루씩·복제 금지, 30초 단일
  전장, 초당 3–5회 검격, 상시 오라, 슬로모·hit-stop·힘겨루기 정지 금지,
  재접근 중 종료
- Soft Guidance: 10비트 액션+카메라, 이펙트 4층 분리, 오디오 스펙, damage
  persistence
- Creative Freedom: 개별 검격 궤적, 파편 디테일, 유적의 구체 형상

**기여 패턴**: 1 (신규 — 속도 수치화: 초당 검격 수+반례 쌍), 2 (신규 —
상시 오라: 트리거형 이펙트 차단), 3 (신규 — 이펙트 4층 분리:
검날/검기/충격/환경파괴), 4 (신규 — 동일 프롬프트 2버전 대조: 실사
다운그레이드 vs 이펙트), 5 (신규 — 종료 조건 명시: 승리 포즈 없음),
6 (금지 리스트의 실패 모드 열거 — #19 확장), 7 (첫 프레임 최대 전투 —
#49의 0帧起手와 동형)

---

## 49. @Arvin007o — 小师妹 6대招 30초 선협 액션 (Seedance, 프롬프트 본문 공개)

**기본 정보**
- 출처: X @Arvin007o (verified), 2026-09-18 게시 (self-quote-repost)
- 원본 포스트: "猜猜小师妹在师姐那里到底学了多少本事 / 这个视频里总共放了
  几个大招？" (quote된 원본에도 영상 1편)
- 프롬프트: 포스트 본문에 전문 공개 (중국어, "视频提示词："). 30초,
  6개 大招 각 5초. 첨부: 史诗打斗提示词生成器_v4.12_技能版.pdf
- 영상: 27.3초 실측 (820프레임, 30fps, 1280x720, 직접 다운로드).
  프롬프트의 30초보다 2.7초 짧음 — 비트 경계는 순서 앵커로만 기능
- 자산 참조: [@小师妹] (주인공 3D 고정 자산) / [@0_3] (암흑 마물 군단) /
  [@w_ww_wb_Colossal_ancient_C] (구천 현공 고대 신전 폐허) — MeiGen
  분석(#3~#21)의 @자산 참조 문법과 동형
- #48의 @xazinga_com이 "이런 화려한 액션은 @Arvin007o 의 프롬프트를 자주
  참고합니다"라고 명시 — 크리에이터 간 참조 사슬 실측
- 증거 기반: prompt-derived (포스트 본문 전문) + frame-derived (초단위
  27프레임 추출, 주요 비트 6프레임 확인)

**관찰 — SSS级一句话总合成** (prompt-derived)
- 30초 전체를 먼저 한 문단으로 요약: 6개 大招의 시각 체계를 순서대로
  나열 (经文镇压 → 凤凰焚狱 → 彗星陨落 → 次元斩裂 → 鲲鹏吞潮 → 五法归一终焉)
- 분镜表 앞에 두는 총괄 선언. Master Spec의 한 줄 요약과 같은 역할

**관찰 — 8대 철칙** (prompt-derived)
- ① 30초 6大招 철칙: 각 5초, "禁止普通攻击, 禁止空白过渡, 禁止喘气,
  禁止站立等待" — 평타·빈틈·숨고르기·대기 4금지를 한 줄에
- ② 매 5초가 완전한 大招 연출: "瞬间起势 → 主体展开 → 满屏爆发 → 魔潮反击 →
  主角空中闪避 → 大招持续扩张 → 余波无缝转入下一招" — 7단계 상태 전이
  체인. #8·#26의 anticipation→contact→consequence를 비트 내부에 내장
- ③ 6招 시각 절대 중복 금지: "禁止六段都变成圆形法阵, 禁止六段都变成光柱,
  禁止六段都变成爆炸" — 흔한 수렴 형태 3종을 지명해서 차단
- ④ 0帧起手: "上一招余波还没结束，下一招已经开始" — 이전 招의 여파가
  끝나기 전에 다음 招 시작. #48의 "첫 프레임부터 최대 전투"와 동형
- ⑤ 주인공 전 구간 공중: "脚不沾地" — 착지 금지를 이동 제약으로
- ⑥ 매 5초 마물 2종 이상 반격: 비행 급강하/다방향 포위/암흑 촉수/흑무
  압제/대형 마물 돌진/파토 기습 중 2종 필수. "禁止'放大招的时候怪物全部
  站着看'" (大招 쏠 때 몬스터가 서서 구경하는 것 금지) — 적을 배경으로
  전락시키는 실패 모드를 직접 지명
- ⑦ 무 슬로모: "全程60帧高速。禁止慢放, 禁止定格, 禁止子弹时间"
- ⑧ 전투 흔적 누적: 1招 경문 낙인 → 2招 유리 초토 → 3招 운석공 →
  4招 공간 균열 → 5招 지형 찢김 → "第6招必须能够看到前五段留下的所有痕迹.
  场景绝不刷新" (6招에서 앞 5개 흔적이 전부 보여야, 장면 절대 리셋 금지)

**관찰 — 분镜表 7필드** (prompt-derived)
- 6개 샷 × (景别 / 位置·移动 / 动作 / 特效 / 魔物反击 / 打斗痕迹 / 运镜)
- 매 샷에 "魔物反击"과 "打斗痕迹" 필드가 독립적으로 존재 — 적의 행동과
  환경 누적을 샷 설계의 1급 필드로 승격

**관찰 — 尾帧 스펙** (prompt-derived)
- 마지막 0.3–0.5초: 주인공 여전히 공중, 흑발·옷자락 여파에 날림, 이마
  神纹 고휘도 유지, 5개 大招 잔영 소멸 중, 아래는 완전 파괴된 폐허
- "不收剑、不转身、不落地、不表现离场" (검 거두기·뒤돌기·착지·퇴장
  연출 금지) — #48의 "승리 포즈 없음"과 동형의 종료 조건

**관찰 — 색상 규율 + 특효 비율** (prompt-derived)
- 主色: 冰蓝 + 紫金 + 玄金 / 魔潮: 玄黑 + 暗红. "不能出现杂乱彩虹配色"
  (잡다한 무지개 색 금지)
- "特效比例严格保持: 流体60% + 粒子25% + 环境水汽15%" — 이펙트 재질을
  비율로 수치화. 코퍼스에서 이펙트 조성비를 숫자로 잠근 첫 사례

**관찰 — 전체 네거티브** (prompt-derived)
- 60개 이상 항목. "禁止场景破坏自动恢复" (장면 파괴 자동 복구 금지),
  "禁止魔物残骸凭空消失" (마물 잔해 허공 소실 금지) 등 누적·잔류系 금지가
  철칙 ⑧과 쌍을 이룸

**관찰 — 6비트 렌더 매칭** (frame-derived)
- a_01 (1s): 주인공 공중, 하늘 가득 황금 고문(经文) — 大招1 ✓
- a_08 (8s): 전면 화염 속 빙청 봉황 형체 — 大招2 ✓
- a_11 (11s): 운해 속 인물 위로 성광 폭발 — 大招3(彗星) 전환부로 보임
- a_20 (20s): 운해에서 솟는 거대 鲲鹏 — 大招5 ✓
- a_26 (26s): 다색 에너지 폭발 속 부유하는 주인공 — 大招6(终焉) ✓
- 6개 시각 체계가 순서대로 전부 렌더. 단 실측 27.3s라 프롬프트의 5초
  경계와 1:1 대응은 안 됨 — 비트표는 순서 앵커 (#13 패턴 재확인)
- 大招4(次元斩裂)의 공간 균열은 확인한 프레임에서 식별 불가 (미확인)

**관찰 vs 추론**
- 관찰: 프롬프트 전문(포스트 본문), 27.3초 실측, 8대 철칙·분镜表·尾帧·
  색상 규율·특효 비율 전부 프롬프트 명시, 6비트 시각 체계의 순서 렌더는
  프레임 확인
- 미확인: 오디오, 大招4 공간 균열의 렌더, 마물 반격 2종/5초의 실제 빈도,
  전투 흔적 누적의 최종 프레임 가시성 (a_26은 폭발로 가려짐)
- 추론: 없음. "#48과의 참조 사슬"은 @xazinga_com 포스트 본문의 직접
  언급 (author-described)

**Production description → Control Levels**
- Hard Lock: 6大招 각 5초·시각 체계 6종 고정, 평타·빈틈·대기 금지,
  0帧起手, 주인공 전 구간 공중, 매 5초 마물 2종 반격, 슬로모 금지,
  장면 리셋·잔해 소실 금지, 尾帧 4금지(검 거두기·뒤돌기·착지·퇴장)
- Soft Guidance: SSS 한 줄 총합성, 분镜表 7필드, 색상 규율, 특효 비율
  60/25/15, 尾帧 연출
- Creative Freedom: 마물 개체 디자인 변주, 운해·폐허의 구체 형상

**기여 패턴**: 1 (신규 — 0帧起手: 여파 중첩 시작), 2 (신규 — 적 반격
의무화: 매 비트 2종, "서서 구경 금지"), 3 (신규 — 전투 흔적 누적:
비트별 잔류물 지정+최종 샷 가시성), 4 (신규 — 특효 비율 수치화
60/25/15), 5 (신규 — 尾帧 스펙: 마지막 0.5초+4금지), 6 (신규 — 시각
중복 금지: 수렴 형태 3종 지명 차단), 7 (신규 — SSS 한 줄 총합성),
8 (@자산 3종 참조 — MeiGen 문법과 동형), 9 (신규 — 크리에이터 간 참조
사슬 #48→#49), 10 (비트표 순서 앵커 — #13 재확인), 11 (실측 27.3s vs
명시 30s — 타임스탬프 불일치 재확인)

---

## 50. Threads @jeong_do_ryeong — 아날로그 필름 아티팩트 제어 가이드 (10초, 프롬프트 엔지니어링)

**기본 정보**
- 출처: Threads @jeong_do_ryeong, 2026-09-26 21:23 KST 게시 (share 링크 →
  /@jeong_do_ryeong/post/DdwBLPRANUY)
- 포스트 본문 (author-described): "[프롬프트 엔지니어링 가이드] AI 비디오
  프롬프트 공학: 아날로그 필름 아티팩트 & 레트로 룩 제어 가이드. AI 비디오
  생성 모델에서 아날로그 필름의 물리적·화학적 열화 현상과 레트로 질감을
  인과율 파탄이나 피사체 뭉개짐(Morphing) 없이 제어하기 위한 물리적 원인
  분류, 프롬프트 엔지니어링 3대 핵심 법칙, 실전 프롬프트 작성법 및 디버깅
  인덱스를 종합 정리한 교육 자료"
- 제목은 "3대 핵심 법칙"이라 쓰였으나 본문은 5대 법칙을 열거
  (author-described 불일치)
- 프롬프트: 작성자 셀프리플라이에 전문 공개 (한국어, permalink DdwBsQFiZXJ)
  — 4대 분류 + 5대 통제 법칙 + 예시 프롬프트
- 영상: 10.1초 실측 (240프레임, 24fps, 1280x720, 직접 다운로드 — CDN 서명
  URL 경유). muted
- 반응: Like 4, Comment 1, Share 1. "AI content" 라벨
- 증거 기반: prompt-derived (셀프리플라이 전문) + frame-derived (초단위
  프레임) + author-described (포스트 본문)

**관찰 — 4대 분류** (prompt-derived)
- ① 기계적 진동: Film Jitter / Gate Weave / Gate Jitter / Frame Jump /
  Frame Shake / Film Shrinkage / Splice Marks
- ② 화학적 열화: Color Fading / Color Shift / Chemical Staining / Silvering /
  Vinegar Syndrome / Emulsion Damage
- ③ 표면 광학·입자: Scratches 계열 / Dust·Dirt·Specks·Hairs 계열 /
  Film Grain / Light Leak & Film Burn / Optical Abrasion & Frame Edge Wear
- ④ 영사 기계 노이즈: Film Flicker / Projection Flicker / Projector Noise
- 핵심 장치: 각 항목마다 영어 Visual Evidence 병기 ("high-frequency
  vertical jitter", "organic wavy warping of flat planes" 등). "old film
  look" 같은 추상 수식어는 화면 뭉개짐·젤리 변형을 유발하므로 금지하고,
  물리·화학적 발생 원인으로 구획화

**관찰 — 5대 통제 법칙** (prompt-derived)
- ① 레이어 분리: 기계적 진동과 화학적 열화는 서로 다른 무대에서 독립 연산.
  한 문장에 섞으면 신호 충돌 → [기계적 물리 레이어]/[화학적 색조 레이어]
  구문 분리
- ② 디지털 완벽성 토큰의 조건부 네거티브: "no smooth digital
  stabilization, no clean digital rendering, no gimbal-smooth motion,
  no vector-like surface" — AI 인코더 내부의 디지털 보정 메커니즘을 끄는
  Relational Negative
- ③ Observer Perspective Lock: 모든 아티팩트는 피사체의 형상 변화가 아니라
  관찰 매체(셀룰로이드 스트립, 영사기 게이트, 렌즈)의 광학 특성으로 명시.
  피사체에 부여하면 Morphing(크로넨버그 현상) 발생
- ④ 3D 카메라 무빙과 2D 게이트 흔들림의 물리적 독립: "The camera maintains
  a stable, independent move, while the analog frame shake occurs solely as
  a mechanical gate-level overlay"
- ⑤ 세로 스크래치 프레임 고정 선언: "vertically fixed, persistent scratch
  lines running consistently through the gate" — 프레임마다 순간이동하는
  환각 차단

**관찰 — 예시 프롬프트 3섹션** (prompt-derived)
- [ANALOG MEDIUM OVERLAY] / [OPTICAL & SURFACE] / [STABILITY LOCK]
- STABILITY LOCK: "Underlying physical geometry and character anatomy remain
  strictly stable and intact. Single continuous shot. Avoid smooth digital
  stabilization, clean digital rendering, gimbal-smooth motion, or
  pixel-perfect alignment"

**관찰 — 데모 영상 렌더** (frame-derived)
- 정적인 가죽 암체어 단일 샷, 10초. 피사체·카메라 모두 정지 — 움직임은
  아티팩트 레벨에서만 발생 (그레인, 플리커, 스크래치, 먼지)
- 렌더 확인: 세로 스크래치 (f_4 우측 밝은 수직선, f_8 좌측 가는 선), 화면
  모서리 먼지 입자 (f_8 우상단 백색 스펙), 프레임 테두리 마모/비네팅,
  앰버-옐로우 색조, 좌측 테두리의 둥근 직사각형 글로우 (전 프레임 고정 위치)
- 스크래치는 프레임마다 다른 위치에서 관측 (f_0 우측 희미 → f_4 우측 밝은
  선 → f_8 좌측 가는 선). 4초 간격 샘플링이라 같은 스크래치의 순간이동
  (법칙 ⑤의 차단 대상)인지, 예시 프롬프트가 의도한 "frame-by-frame on/off"
  인지는 판단 불가 (미확인)
- 피사체(암체어)는 전 구간 형상 안정 — Observer Perspective Lock의 주장과
  일치 (frame-derived)
- 우하단 스파클 워터마크: 생성 AI 표시

**관찰 vs 추론**
- 관찰: 가이드 전문(셀프리플라이), 10.1초 실측, 4대 분류·5대 법칙 전부
  프롬프트 명시, 데모 영상의 아티팩트 렌더는 프레임 확인
- 미확인: 오디오 (muted), 예시 프롬프트가 이 데모 영상을 만든 프롬프트인지
  여부 (포스트에 명시 없음), 스크래치 순간이동 여부
- 추론: 없음. "3대 vs 5대" 표기 불일치는 포스트 본문의 직접 관측

**Production description → Control Levels**
- Hard Lock: 아티팩트는 관찰 매체의 광학 특성으로만 명시 (피사체 형상 변화
  금지 — Morphing 방지), 기계적/화학적 레이어 구문 분리, 스크래치는
  게이트상 수직 고정 선언, 카메라 무빙과 게이트 흔들림 독립 선언
- Soft Guidance: 4대 분류 중 사용할 아티팩트 선택, Relational Negative
  배치, [ANALOG MEDIUM OVERLAY]/[OPTICAL & SURFACE]/[STABILITY LOCK]
  3섹션 구조
- Creative Freedom: 아티팩트 강도·조합, 시대 설정 (예시: 1970s 16mm)

**기여 패턴**: 1 (신규 — Observer Perspective Lock: 아티팩트를 피사체가 아닌
관찰 매체에 귀속), 2 (신규 — 기계적/화학적 레이어 구문 분리), 3 (신규 —
Relational Negative: 디지털 완벽성 토큰 조건부 억제), 4 (신규 — 3D 무빙/2D
게이트 흔들림 물리적 독립 선언문), 5 (신규 — 스크래치 프레임 고정 선언),
6 (동일 작성자 #8·#33–37·#41 — 프롬프트 가이드 시리즈, 피사체측에서
관찰매체측으로 확장), 7 (제목 "3대" vs 본문 "5대" 표기 불일치)

---

## 51. X @EEJ_OOXO — 손 쓸기+표정 전환 개그 이전 셀카 (10초, 개그 트랜스퍼)

**기본 정보**
- 출처: X @EEJ_OOXO (OOXO, AI Content Creator — 프로필에 Pollo AI·Newtake·
  DomoAI·Nemo Video·GenPresso 파트너 표기), 2026-09-27 02:53 KST 게시
- 포스트 본문 (author-described): "아 시밬ㅋㅋㅋㅋ 내가 만들어 놓고 개처웃기네
  ㅋㅋㅋㅋㅋ\n\n프롬프트 아래⬇️"
- 인용: @LioraSolveil의 포스트 "가을이라 감정기복 개심한 니가 생각났다."
  (9.9초 세로 영상) — 이 영상의 손 쓸기+표정 전환 개그를 재현한 것
- 프롬프트: 작성자 셀프리플라이에 전문 공개 (영어)
- 영상: 10.1초 실측 (242프레임, 24fps, 2160x2160 정사각형, 직접 다운로드 —
  vxtwitter API 경유). "Made with AI" 라벨, 우상단 G 워터마크
- 모델: 명시 없음
- 반응: Like 13, Repost 7, Reply 5, 조회 1,466
- 증거 기반: prompt-derived (셀프리플라이 전문) + frame-derived (초단위
  프레임) + author-described (포스트 본문·인용 관계)

**관찰 — 레퍼런스 역할 분리** (prompt-driven)
- <<<image_1>>>: 전경 캐릭터 정체성+의상 (주황 별 캡, 트윈 브레이드, 화이트
  키홀 크롭탑, 어깨에 걸친 크림 재킷, 액세서리)
- <<<image_2>>>: 후경 캐릭터 정체성+의상 (앞머리 긴 흑발, 그레이 수트, 화이트
  블라우스, 주황 비즈 블랙 초커)
- <<<image_3>>>: 방의 구조·가구·색·조명 (셀카 앵글에 맞게 조정)
- <<<video_1>>>: 첫 9초의 손 안무·표정 타이밍·두부 움직임·상대 배치만 담당.
  "Its performers' appearances and clothing do not transfer" — 출연자
  외형·의상은 이전되지 않음을 명시
- "The gray circles on the full-body views are reference masks and must not
  appear" — 레퍼런스 시트의 마스크 원이 렌더에 스며드는 실패 모드를 직접
  차단
- "The selfie image fills the output frame without the reference video's
  black side padding" — 원본의 레터박스를 출력에 끌고 오지 않음

**관찰 — 개그 타이밍 3구간** (prompt-derived)
- 0.0–0.7s: 무표정 오프닝+손 준비
- 0.7–9.0s: 후경이 손을 위아래로 빠르게 교대 쓸기 (전경 얼굴을 스치듯 가림),
  전경은 환한 이빨 미소↔무표정 전환. "Use the reference's precise motion
  timing rather than inventing additional gestures" — 타이밍은 창작 금지,
  원본 그대로
- 9.0–10.0s: 개그 붕괴 — 둘 다 터져 웃음. "End while both are still laughing,
  without a freeze or posed finish" (#48/#49의 종료 장치와 동형)
- 코미디 장치: 후경은 전 구간 "deliberately deadpan" — 표정 전환은 전경만,
  후경은 무표정 유지로 대비

**관찰 — 렌더 매칭** (frame-derived)
- f_0: 둘 다 정면 무표정 ✓ (FIRST FRAME)
- f_4: 손이 얼굴 앞을 스치는 블러+전경 눈 찡긋 — 개그 진행 중 ✓
- f_8: 전경 환한 미소, 후경 무표정 ✓ (deadpan 대비)
- f_9 (9.3s): 둘 다 입 크게 벌리고 폭소 — 눈 찡그림, 어깨 들썩 ✓
  (9.0–10.0s)
- 3구간 전부 순서대로 렌더. 실측 10.1s vs 명시 10s — 거의 일치

**관찰 — 연속성 장치** (prompt-derived)
- "Maintain each character's face, hairstyle, clothing, and accessories
  through all hand occlusions" — 손에 가려져도 정체성 유지
- "<<<image_2>>>'s hands remain anatomically connected to her arms" —
  손목 잘림 방지
- LOCAL CONSTRAINTS: "Exactly two characters... No mirror shot, extra hands,
  face masks, captions, wardrobe changes"

**관찰 vs 추론**
- 관찰: 프롬프트 전문(셀프리플라이), 10.1초 실측, 레퍼런스 4종 역할 분리
  전부 프롬프트 명시, 3구간 타이밍의 프레임 렌더 확인, 인용 관계
  (vxtwitter qrt)
- 미확인: 오디오(웃음소리), 사용 모델, <<<video_1>>>이 인용 원본과 동일한지
  (포스트 맥락상 동일으로 보이나 명시 없음)
- 추론: 없음. "G 워터마크=GenPresso"는 작성자 프로필의 파트너 표기와의
  연결이나 확정 표기는 아님 (inference로 분리)

**Production description → Control Levels**
- Hard Lock: 레퍼런스 역할 분리 (video_1은 안무·타이밍만, 외형·의상 이전
  금지), 정확히 2명, 거울 샷·여분 손 금지, 손 가림 중 정체성 유지, 종료는
  웃음 중 (프리즈·포즈 금지)
- Soft Guidance: 3구간 타이밍, 후경 deadpan 대비, 레퍼런스 마스크 원 배제,
  레터박스 미이전
- Creative Freedom: 방 장식 디테일, 웃음의 강도

**기여 패턴**: 1 (신규 — 개그 트랜스퍼: 안무 레퍼런스와 정체성 레퍼런스의
완전 분리 + "외형 이전 금지" 명시문), 2 (신규 — deadpan 대비: 한 캐릭터만
표정 전환, 다른 한 명은 무표정 고정), 3 (신규 — 레퍼런스 마스크 오염 차단:
"gray circles must not appear"), 4 (신규 — 레터박스 미이전 선언), 5 (종료
장치 — #48/#49와 동형: 끝나지 않은 상태로 종료), 6 (인용 개그: 원본 포스트의
"감정기복" 텍스트가 표정 전환 개그의 의미 앵커)

---

## 52. X @ShamiWeb3 — 존재하지 않는 한국 여자아이의 하루 (30초, 캐릭터 시트 선행)

**기본 정보**
- 출처: X @ShamiWeb3 ("Shami", verified individual, ~19.2K 팔로워),
  2026-09-26 14:11 KST 게시
- 포스트 본문 (author-described): "A Korean girl who never agreed to be in
  the video.\n\nMade with GPT Image 2 and Seedance 2.5 on @FishCreativeHQ
  \n\nThe prompt is in the comments 👇" — "출연에 동의한 적 없는 한국
  여자아이" = 그녀는 존재하지 않음 (AI 생성 캐릭터)
- 프롬프트: 작성자 댓글에 공개되었으나 X 로그인 월 뒤 — 미확보
  (vxtwitter/xcancel 등 우회 실패, Cloudflare 월). 사용자가 댓글
  프롬프트를 붙여넣으면 보강 예정
- 영상: 30.1초 실측 (722프레임, 24fps, 1280x720, 직접 다운로드 —
  vxtwitter API 경유)
- 모델: GPT Image 2 (캐릭터 시트) → Seedance 2.5 (영상) —
  author-described. 캐릭터 시트는 사용자가 "상세하게 만들었다"고
  주목한 포인트
- 반응: Like 274, Repost 12, Reply 69, 조회 16,901
- 증거 기반: frame-derived (초단위 프레임) + author-described (포스트
  본문). 프롬프트 미확보이므로 전부 프레임 기반 관찰

**관찰 — 멀티샷 정체성 일관성** (frame-derived)
- 6개 프레임(f_0/5/10/15/20/25) 전체에서 동일 인물의 얼굴·헤어(긴 흑발,
  하프업/로우 포니테일)·의상(브라운 리브드 긴팔 미니 드레스)·액세서리
  (브라운 숄더백, 손목 브레이슬릿) 고정 확인
- 로케이션이 4곳으로 바뀌는데도 의상·소품이 전혀 바뀌지 않음:
  주택 대문 앞(주소판 25) → 골목길 (후면 보행) → 편의점 입구 → 음료
  마시기 (노점) → 골목 (물병+종이봉투 들고 보행)
- 소품 연속성: f_15의 생수 2병+종이봉투가 손에 쥐어진 채로 자연스럽게
  이어짐 (쇼핑→귀가 서사의 인과)
- 종료: f_25에서 화면이 어두운 블러 — 카메라가 가려지거나 내려진 듯한
  "촬영 종료" 장치 (연출된 마무리 포즈 없음, #51의 "웃음 중 종료"와 동형)

**관찰 — 한국 동네 렌더** (frame-derived)
- 벽돌담, 기와 지붕, 주소판 "25", 전봇대·전선, 편의점 유리문과 한글
  간판이 전부 실사급으로 렌더
- 한글 텍스트는 일부 가짜 렌더: "미즈드시" 표기는 실제 상호가 아닌
  문자 흉내 (#21의 text seep와 동형). 주소판 "25" 같은 단순 문자는
  정확, 복잡한 상호는 흉내 — 텍스트 렌더의 난이도 기울기
- 황혼 시간대+흐린 하늘로 전 샷의 조명 무드가 통일 (일관된 시간대)

**관찰 — 셀프리플라이 전 캐릭터 시트 파이프라인** (author-described)
- 이미지 모델(GPT Image 2)로 캐릭터 시트를 먼저 만든 뒤 비디오
  모델(Seedance 2.5)로 영상화 — 정체성 생성과 모션 생성을 분리한
  2단계 파이프라인
- 캐릭터 시트 이미지는 포스트에 첨부되지 않음 (영상 단일 첨부)

**관찰 vs 추론**
- 관찰: 30.1초 실측, 6프레임 전 구간 정체성 고정 확인, 4개 로케이션,
  캐릭터 시트 선행 파이프라인 (작성자 표기), 텍스트 렌더의 정확/흉내
  기울기, f_25 종료 장치
- 미확인: 캐릭터 시트 구성 (전면/측면/의상 상세 — 작성자 댓글에 있으나
  미확보), 샷 분할 방식 (Seedance 2.5 단일 30초 생성인지 멀티 클립
  편집인지)
- 추론: 없음. "시트에 액세서리까지 고정됐다"는 프레임에서 확인된 사실만
  기록 (의상·가방·브레이슬릿이 전 샷 동일)

**Production description → Control Levels**
- Hard Lock: 캐릭터의 얼굴·헤어·의상·액세서리를 모든 샷·모든
  로케이션에서 고정 — 로케이션이 바뀌어도 의상·소품 변경 금지
  (소품은 서사적 인과가 있을 때만 추가: 쇼핑 후 물병+봉투)
- Soft Guidance: 전 샷 동일한 시간대·조명 무드 (황혼), 한국 동네
  요소 (벽돌담·기와·주소판·한글 간판), 종료는 촬영 중단형 (포즈 금지)
- Creative Freedom: 샷 순서, 카메라 무브, 컷 구성

**기여 패턴**: 1 (신규 — 캐릭터 시트 선행 2단계 파이프라인: 이미지
모델로 정체성 고정 → 비디오 모델로 모션, #51의 레퍼런스 역할 분리와
동형의 "역할 분리"), 2 (신규 — 로케이션 변화에도 불변하는
의상·액세서리 고정: #47의 LOGIC RULE을 정체성에 적용), 3 (신규 —
텍스트 렌더 난이도 기울기: 단순 문자 정확 vs 복잡 상호 흉내), 4
(종료 장치 — #48/#49/#51과 동형: 끝나지 않은 상태로 종료)

---

## 53. X @ayzalnooor24521 — 시골 장터 채소 파는 소녀 브이로그 (33초, Seedance 2.0, 프롬프트 본문 전문)

**기본 정보**
- 출처: X @ayzalnooor24521, 2026-09-26 13:23 KST 게시
- 포스트 본문 (author-described): "A simple day at a Korean village
  market\nSelling fresh veggies, meeting customers, and enjoying the
  little moments of daily life.\nCreated with AI, inspired by real
  countryside vibes.\n\nCreated on seedance 2.0\n\nPrompt:" 이하
  프롬프트 전문 공개 (영어)
- 모델: Seedance 2.0 (작성자 명시 — 2.5가 아님)
- 영상: 33.2초 실측 (796프레임, 24fps, 1280x720, 직접 다운로드 —
  vxtwitter API 경유). 프롬프트는 "30-second"라고 명시 — 실측과 불일치
  (코퍼스 내 타임스탬프 불일치 6번째 사례)
- 반응: Like 195, Repost 4, Reply 72, 조회수 미표기 (fxTwitter 미반환)
- 증거 기반: prompt-derived (본문 전문) + frame-derived (5초 간격
  6프레임)

**관찰 — 타임스탬프 스토리보드** (prompt-derived, 일부 frame-derived
대조)
- 3s: medium close-up로 카메라를 보고 웃으며 인사 → f_5에서 정확히
  렌더 ✓ (미소 정면 클로즈업)
- 6s: 손님이 채소를 요청, 손으로 골라 재사용 봉투에 담기 → f_10에서
  손님 응대 중 ✓
- 10–14s: 옛날식 시장 저울로 무게 재기, 정성껏 포장 ("Keep realistic
  hand movements")
- 14–17s: 손님이 돈을 내고, 그녀는 미소로 받으며 감사
- 17–20s: 시장 와이드 — 손님들이 오가는 동안 계속 일하기
- 20–23s: 상추 한 단을 카메라 쪽으로 들어 보이며 "These are fresh
  today!" 같은 자연스러운 멘트 → f_15에서 상추를 손님 쪽으로 내밀며
  말하는 장면 ✓
- 23–26s: 손님이 하나 더 와서 시장이 약간 바빠짐
- 26–28s: 미소 클로즈업, 카메라를 똑바로 보고 작은 웨이브
- End: 평화로운 와이드 — 시골·산 배경으로 계속 일하기, "subtle natural
  ending feeling" → f_25에서 한옥 지붕·산 배경 와이드로 종료 ✓
  (#48/#49/#51/#52의 "끝나지 않은 상태로 종료" 장치와 동형)
- f_0은 완전한 블랙 — 페이드인 오프닝 (명시 없음, frame-derived)

**관찰 — 정체성 마스터 스위치** (prompt-derived + frame-derived)
- 프롬프트 말미의 한 단락: "Important: Keep the same Korean girl, same
  face, hairstyle, outfit and apron throughout the entire video.
  Maintain strong character consistency between every shot." —
  #47의 LOGIC RULE와 동형의 한 줄 마스터 스위치
- 캐릭터 스펙: 크림 니트 스웨터, 다크브라운 앞치마, 갈색 머리 루즈한
  메지 번+소프트 뱅
- 프레임 확인: f_5/10/15/20 전부 크림 스웨터+다크 앞치마+메지 번
  동일 ✓. 손 클로즈업(f_15, f_20)에서도 손가락 왜곡·여분 손가락 없음 ✓
  (네거티브 리스트에 "distorted hands, extra fingers" 명시)

**관찰 — 의도적 불완전 스펙** (prompt-derived)
- "handheld smartphone/vlog camera, gentle camera shake, occasional
  close-ups... slight imperfect framing, realistic movement, no excessive
  camera effects" — #19의 failure-based negative, #45의
  deliberate-imperfection과 동형
- 네거티브: "not like a commercial or polished AI advertisement",
  "excessive beauty filters, or an overly cinematic commercial
  appearance" — 미적 방향을 "광고 같지 않음"으로 정의하는 네거티브
  미학
- 배경 인물: "Make the customers and background people look natural
  and realistic" — f_10/f_20의 손님 (중년 여성, 자연스러운 얼굴) ✓

**관찰 vs 추론**
- 관찰: 프롬프트 전문(본문), 33.2초 실측 vs "30-second" 명시 불일치,
  타임스탬프 4구간의 프레임 매칭(3s/6s/20–23s/End), 정체성 4프레임
  고정, 손 렌더 정상, f_0 페이드인
- 미확인: 10–17s 구간의 저울·결제 장면 (5초 간격 샘플이라 프레임
  미포착), 오디오 (멘트·시장 소리), 클립이 단일 생성인지 편집인지
- 추론: 없음

**Production description → Control Levels**
- Hard Lock: "Keep the same Korean girl, same face, hairstyle, outfit
  and apron throughout the entire video" — 정체성 마스터 스위치 한 줄.
  손 렌더 네거티브 (distorted hands, extra fingers)
- Soft Guidance: 타임스탬프 스토리보드, 핸드헬드+약한 흔들림+약간
  불완전한 프레이밍, "광고 같지 않음" 네거티브 미학
- Creative Freedom: 손님 얼굴, 채소 종류, 시장 배경 디테일

**기여 패턴**: 1 (신규 — 정체성 마스터 스위치 한 줄 선언: #47의
LOGIC RULE을 캐릭터에 적용, "throughout the entire video"), 2 (신규 —
"광고 같지 않음"을 미적 목표로 명시하는 네거티브 미학:
"not like a commercial or polished AI advertisement"), 3 (신규 —
타임스탬프 스토리보드의 실측 불일치: 30s 명시 vs 33.2s 실측 —
타임스탬프는 순서 앵커라는 MeiGen 종합 결론과 일치), 4 (종료 장치 —
#48/#49/#51/#52와 동형: 계속 일하는 와이드로 자연스럽게 끝남)

---

## 54. X @paperwiz0 — AI 영상 제작 8역할론 (텍스트 가이드, 영상 없음)

**기본 정보**
- 출처: X @paperwiz0 ("paperwiz"), 2026-09-26 21:07 KST 게시
- 형식: 텍스트 설명 포스트 (영상·이미지 첨부 없음) — 사용자가 "그냥
  설명"이라고 지목한 케이스
- 본문 (author-described): AI 영상 제작이 어려운 이유는 툴이 어려워서가
  아니라, 드라마·영화 현장의 세분화된 역할(시나리오 작가·감독·촬영감독·
  미술팀·배우·편집·음향)이 혼자 만드는 AI 영상에서는 한 사람에게
  몰리기 때문이라는 문제 제기. 이어서 8단계 제작론을 제시
- 본문 말미가 "다시 보면 이런 문제가 자주 보입니다."에서 끊김 —
  QC 체크리스트로 이어지는 셀프리플라이 2개는 X 로그인 월 뒤라 미확보
- 반응: Like 2, Repost 0, Reply 2
- 증거 기반: text-guide (본문 전문). 영상·프롬프트 없음 — 전부
  작성자의 제작론 서술

**관찰 — 8역할 제작론** (text-guide)
1. **작가처럼 이야기부터**: 목표→장애물→행동→결과→마지막 이미지.
   30초라면 복잡한 세계관보다 이 5비트만 명확해도 강한 영상
2. **감독처럼 장면 분해**: "시장 질주→다리 진입→도심 이동→목적지 도착".
   핵심 — 앞 장면의 마지막 행동이 다음 장면의 시작 원인이 되어야 함
   ("왜 다음 장면으로 넘어가는가")
3. **미술감독처럼 고정**: 캐릭터 얼굴·헤어·의상·소품·장소 구조·시간대·
   색감을 기준 이미지로 미리 고정. "AI에게 매번 새로운 세계를 만들게
   하지 않고, 이미 정해진 제작물을 계속 사용하게"
4. **촬영감독처럼 카메라 설계**: 장면 목적별 카메라 (달리기→뒤 추적,
   규모 공개→와이드, 타격→측면, 감정→클로즈업, 소품→손 인서트).
   핵심 — 한 장면에 여러 카메라 무브를 넣지 말고 한 액션 비트에
   하나의 핵심 무브만
5. **배우 연출처럼 행동-감정 분리**: "슬픈 표정"이 아니라
   눈 피하기→멈춤→다시 보기→작게 웃기로 감정을 행동으로 변환.
   큰 표정보다 시선·호흡·손 위치·짧은 정지
6. **편집자처럼 앞뒤 연결**: 각 블록 마지막에 다음 장면이 이어받기
   좋은 상태를 남김 — 오른쪽으로 달리며 끝→다음도 같은 방향 시작,
   소품 왼손→왼손에서 시작, 카메라 뒤→갑자기 정면 금지
7. **음향감독처럼 소리**: 화면의 원인→소리 순서. 발소리·충격음·호흡·
   빗소리를 행동의 일부로
8. **QC**: 예쁘다고 통과시키지 말고 다시 보기 (체크리스트는 미확보)

**관찰 — 코퍼스와의 정합** (text-guide vs corpus)
- 2번(감독)의 "앞 장면 마지막 행동 = 다음 장면 시작 원인"은
  #48/#49/#51/#52/#53의 "끝나지 않은 상태로 종료" 장치를 이론으로
  뒷받침 — 종료 장치는 곧 다음 클립의 handoff 상태
- 3번(미술감독)의 "기준 이미지로 고정"은 #52의 캐릭터 시트 선행
  파이프라인, #51의 레퍼런스 역할 분리, #53의 정체성 마스터 스위치와
  정확히 일치
- 4번(DP)의 "한 액션 비트에 하나의 핵심 카메라 무브"는 MeiGen
  종합의 카메라 문법 (단일 샷=단일 무브)과 일치
- 5번(배우)의 "감정을 행동으로 변환"은 #14의 EMOTION=BODY,
  #11의 5단계 연기 조명과 동형
- 6번(편집)의 연결 규칙은 #46의 shooting axis lock, #28의
  master-axis, #47의 LOGIC RULE과 동형
- 7번(음향)의 "화면의 원인→소리"는 #47의 per-shot SFX와 동형
- 이 글은 코퍼스가 프레임·프롬프트에서 귀납한 패턴들을 제작론
  언어로 연역한 셈 — 양방향 정합 확인

**관찰 vs 추론**
- 관찰: 8역할 제작론 전문(본문), 코퍼스 패턴과의 정합 7건,
  8번 QC 체크리스트 미확보
- 미확인: 8번 체크리스트 내용, 작성자의 실제 작업물 (포스트에 없음)
- 추론: 없음. "이론과 코퍼스의 정합"은 관찰된 문장들의 대조이지
  검증된 인과가 아님 (text-guide이므로 production rule로 직접 승격
  불가 — 기존 원칙 유지)

**Production description → Control Levels**
- Hard Lock: 3번의 고정 목록 (얼굴·헤어·의상·소품·장소 구조·시간대·
  색감) — 기준 이미지로 선행 고정
- Soft Guidance: 1번의 5비트 스토리, 4번의 장면 목적별 카메라,
  6번의 handoff 연결 규칙 (방향·소품 손·카메라 위치 유지)
- Creative Freedom: 5번의 감정-행동 변환 디테일, 7번의 사운드 디자인

**기여 패턴**: 1 (신규 — 8역할 제작론 자체: 혼자 만드는 AI 영상의
역할 분담 프레임워크), 2 (신규 — "앞 장면 마지막 행동 = 다음 장면
시작 원인"의 handoff 문법 명문화), 3 (신규 — "한 액션 비트에 하나의
핵심 카메라 무브" 안정성 원칙), 4 (신규 — 음향을 행동의 일부로 보는
"화면의 원인→소리" 순서), 5 (메타 — 코퍼스의 귀납 패턴과 제작론의
연역이 7개 항목에서 정합: 양방향 검증)

---

## 55. X @bmx_ai13 — MJ 영감 댄스: 스토리보드 검증 레이어 분할 화면 (30초, 프롬프트 미공개)

**기본 정보**
- 출처: X @bmx_ai13 (BMX), 2026-09-26 05:48 KST 게시. #17 (Troy
  브이로그)의 작성자와 동일
- 포스트 본문 (author-described): "A Super Simple Workflow: Michael
  Jackson→ Inspired Dance Concept → My created custom GPT Plugins→
  Seedance 2.5" — 워크플로우만 공개, 프롬프트 미공개
- 영상: 30.1초 실측 (901프레임, 30fps, 1440x1440 정사각형, 직접
  다운로드 — vxtwitter API 경유). 흑백
- 반응: Like 56, Repost 4, Reply 15
- 증거 기반: frame-derived (5초 간격 6프레임) + author-described
  (포스트 본문). 프롬프트 미확보

**관찰 — 분할 화면 구조** (frame-derived)
- 화면 상단: 젖은 무대 위 MJ 룩 댄서 (페도라·블랙 수트·화이트 셔츠·
  로퍼+흰 양말)의 안무 수행 — 6프레임 전부 동일 인물·동일 의상
- 화면 하단: 12패널 스토리보드 (P01–P12, 0–30s)가 전 구간 정적
  오버레이로 고정. 스토리보드는 영상 안에서 "계획"을, 상단은
  "수행"을 보여주는 검증 레이어
- 즉 이 영상은 최종 결과물이 아니라 custom GPT 플러그인의 산출물
  데모: 스토리보드(계획)와 퍼포먼스(수행)의 정합을 한 화면에서 증명

**관찰 — 스토리보드 패널 스펙** (frame-derived, 패널 텍스트 판독)
- P01 0–2s Cinematic entrance: "Camera: Wide, centered, static |
  Action: Dancer walks in confidently."
- P02 2–4s Hat gesture and attitude beat: "Medium-wide, slight
  push-in | Hat gesture, body isolation, strong pose."
- P03 4–7s Clean full-body dance hit: "Wide, static | readable space."
- P04 7–10s Smooth heel-toe glide: "Wide, side view, static |
  side travel."
- P05 10–13s Rhythmic footwork combo / P06 13–16s Sharp isolations
  (chest hit, hand accent) / P07 16–19s Traveling dance combo
  ("tracking feel (or static)") / P08 19–22s Spin and stop
  ("One controlled spin and stop") / P09 22–25s Signature pop-dance
  sequence / P10 25–27s Energy build ("faster combo, rhythmic hits") /
  P11 27–29s Final movement phrase ("slight low angle, strong
  extension") / P12 29–30s Hero ending pose ("clean hold")
- 패널 내 모션 화살표 (P04/P05/P07/P08/P09/P10): 이동 방향·스핀을
  화살표로 표기 — #28의 master-axis를 스토리보드 문법으로 구현
- PRODUCTION NOTES: "0–7s Edit-friendly clean footage (stable framing,
  clear negative space for later effects) | 7–29s Continuous dance
  performance (main choreography section) | 29–30s Final hold for
  smooth transition" — 후반 작업을 전제로 한 촬영 설계

**관찰 — 카메라 규율** (frame-derived)
- 12패널 중 9개가 "Wide, static". 움직이는 카메라는 P02/P06의
  "slight push-in", P11의 "slight low angle"뿐 — #54의 "한 액션 비트에
  하나의 핵심 카메라 무브"를 스토리보드 스펙으로 구현
- 상단 퍼포먼스도 전 구간 와이드 고정 — 카메라는 움직이지 않고
  댄서가 움직임 (움직임의 주체를 댄서에게 양보)

**관찰 vs 추론**
- 관찰: 30.1초 실측, 분할 화면 구조, 12패널 텍스트 전문 판독,
  카메라 스펙 12개, production notes, 의상 고정 6프레임
- 미확인: custom GPT 플러그인의 실제 동작, 스토리보드 패널이
  플러그인 출력인지 후반 합성인지, 오디오
- 추론: 없음. "하단 패널이 검증 레이어"라는 해석은 구조 관찰에서
  직접 도출되나, 작성자의 의도 표기는 없음 (author-described 없음)

**Production description → Control Levels**
- Hard Lock: 댄서 의상 전 구간 고정 (페도라·수트·셔츠), 흑백 톤 통일
- Soft Guidance: 12패널 타임스탬프 안무 비트, 패널별 카메라 스펙
  (기본 Wide static, 강조 비트에만 push-in/low angle), 모션 화살표로
  이동 방향 표기
- Creative Freedom: 안무 디테일, 무대 조명

**기여 패턴**: 1 (신규 — 스토리보드 검증 레이어: 계획을 영상 안에
  정적 오버레이로 렌더해 수행과 정합을 화면에서 증명), 2 (신규 —
  "Edit-friendly clean footage": 후반 작업용 네거티브 스페이스 확보를
  촬영 스펙에 명시), 3 (신규 — "Final hold for smooth transition":
  29–30s를 다음 클립 연결용으로 비워두는 handoff 설계 — #54의 6번과
  동형), 4 (카메라 규율 — #54의 "한 비트에 하나의 무브"를 패널 스펙으로
  구현, 12패널 중 9개 Wide static)

---

## 56. Threads @tuberithm — "How to Make Viral AI Movies" 제작 파이프라인 정리 (텍스트 가이드)

**기본 정보**
- 출처: Threads @tuberithm, 2026-09-27 게시 (본문 1개 + 작성자
  셀프리플라이 6개). 조회수 1K, Like 6, Comment 6, Repost 1
- 형식: 유튜브 영상 "How to Make Viral AI Movies Like @mythrafilms"
  (youtu.be/IY430T84h3U)의 내용을 6개 리플라이로 풀어쓴 정리 스레드.
  영상 자체는 미확인 — 유튜브 페이지가 reCAPTCHA 차단으로 읽기 실패
- 본문 (author-described): "AI 영화, 요즘 유튜브 완전 장악하고 있는 거
  아나 🎬 어떤 영상은 8일 만에 조회수 백만, 구독자 십만 명을 훌쩍
  넘겼다고 한다. AI 툴만으로도 이런 고퀄리티 영화를 만들 수 있다는
  사실. 이 영상이 그 완벽한 가이드를 풀어놨다"
- 증거 기반: text-guide (스레드 전문). 영상 본편·설명란 미확인 —
  전부 스레드 작성자의 요약 서술

**관찰 — 마스터 프롬프트 체인** (text-guide)
1. 아이디어: ChatGPT "영상 아이디어 마스터 프롬프트"에 장르+대략
   스토리를 던지면 10개 아이디어 제안 → 선택. 없으면 ChatGPT가 직접
   제안. 이어서 "영화 스토리 마스터 프롬프트"로 감정선 있는 스토리
2. 장면 분석: "AI 영화 장면 분석 프롬프트"로 캐릭터·장소·스토리 흐름
   상세 분석 → "캐릭터 생성 프롬프트"로 전 캐릭터의 이미지 프롬프트
   생성 → 구글 플로우 "Nanobana 2" 모델로 이미지 생성. 완성된 이미지
   파일명은 캐릭터 이름으로 변경
3. 핵심 이미지: ChatGPT "이미지 프롬프트"는 4부분으로 나뉜 상세
   프롬프트 (등장 캐릭터 이름 강조) → 구글 플로우에서 캐릭터 이미지를
   끌어와 함께 생성하면 영화의 한 장면 완성. 모든 이미지 반복
4. 영상화: SeaArt 2.5로 최대 30초 영상 (Flow AI 활용). ChatGPT
   "비디오 프롬프트" 4부분 → 구글 플로우 "Omni 1.1 Flash" 모델로
   12 크레딧 → 해당 이미지를 끌어다 놓으면 클립 완성. 모든 이미지
   반복 후 전부 다운로드
5. 편집: 클립 합치기, 지루한 부분 과감히 절단, CapCut·오디오
   라이브러리·픽사베이 BGM (볼륨 살짝 낮게), 클립 사이 자연스러운
   전환 효과+필터, 고화질 내보내기
6. 썸네일+SEO: "썸네일 마스터 프롬프트"로 경쟁 채널 스타일 참고
   썸네일 프롬프트 → 구글 플로우+캐릭터 이미지로 썸네일. PDF의 SEO
   프롬프트로 노출 작업. "AI Movie Masterclass Needed" 댓글 200개면
   2편

**관찰 — 코퍼스와의 정합** (text-guide vs corpus)
- 마스터 프롬프트 체인 (아이디어→스토리→장면→캐릭터→이미지→비디오→
  썸네일→SEO)은 사용자의 XAI-Studio-Video 구조 (Master Spec → 모델별
  어댑터)와 독립적으로 수렴한 동일 아키텍처 — 기획을 한 번에 끝내고
  실행만 단계별로 위임
- "이미지 파일명은 캐릭터 이름으로 변경"은 #52의 캐릭터 시트 선행,
  #51의 레퍼런스 역할 분리와 동형의 정체성 관리 (파일명=앵커)
- "4부분으로 나뉜 프롬프트" (이미지·비디오 공통)는 구조화된 프롬프트
  포맷의 반복 — #49의 분鏡表 7필드, #48의 10비트 구조와 동형
- 캐릭터 이미지를 매 장면 생성에 끌어오기 = #51의 image_1 역할
  (정체성 레퍼런스), #52의 시트 선행 파이프라인
- 30초 클립 × N → 편집 조립 = MeiGen 종합의 Trailer Montage 패턴
  (9/20), #47의 15샷 조립과 동형
- "지루한 부분은 과감히 잘라내서 몰입도" = 편집 단계의 Necessity Test
  (사용자 원칙과 정합)
- 모델명 (Nanobana 2, Omni 1.1 Flash, SeaArt 2.5)은 스레드 작성자의
  표기 — 미검증 (author-described, inference 금지)

**관찰 vs 추론**
- 관찰: 스레드 7개 포스트 전문, 6단계 파이프라인, 프롬프트 체인
  명칭 8종, 코퍼스와의 정합 6건
- 미확인: 유튜브 본편 (reCAPTCHA 차단), 본편 설명란, 모델명의 실제
  존재 여부, "8일 만에 조회수 백만" 주장의 사실 여부
- 추론: 없음. "이 파이프라인이 실제로 동작한다"는 검증되지 않음 —
  text-guide이므로 production rule로 직접 승격 불가

**Production description → Control Levels**
- Hard Lock: 캐릭터 이미지 파일명을 캐릭터 이름으로 고정 (전 단계
  공통 앵커), 캐릭터 이미지를 매 장면·매 클립 생성에 레퍼런스로
  끌어오기
- Soft Guidance: 마스터 프롬프트 체인 (아이디어→스토리→장면 분석→
  캐릭터→이미지→비디오→썸네일→SEO), 4부분 구조화 프롬프트,
  30초 클립 단위 생성 후 편집 조립
- Creative Freedom: BGM 선정, 전환 효과·필터, 썸네일 스타일

**기여 패턴**: 1 (신규 — 마스터 프롬프트 체인: 기획을 프롬프트
체인으로 전문화하는 파이프라인 아키텍처, 사용자의 Master Spec 구조와
독립 수렴), 2 (신규 — 파일명=캐릭터 이름: 정체성 앵커를 파일명으로
고정), 3 (신규 — 4부분 구조화 프롬프트의 반복: 이미지·비디오 공통
포맷), 4 (조립 편집 — MeiGen Trailer Montage와 동형: 30초 클립×N →
  절단→조립), 5 (메타 — #54의 8역할론과 정합: 이 파이프라인은 8역할을
  프롬프트 체인으로 외주화한 구현)

## 57. Threads @omonge222 — 주짓수 실영상 모션 레퍼런스 전이 (프롬프트 전문 확보)

**기본 정보**
- 출처: Threads @omonge222, 2026-09-28 게시. "이제 @zcre.co.kr
  주짓수 래퍼런스에 감을 잡은거 같아요. 일단 성별은 동일하면 좋을거
  같아요. 원본과 비교영상 올립니다" — 실 주짓수 영상을 모션
  레퍼런스로 삼아 캐릭터 둘이 싸우는 장면 재현
- 출연: @bihyeonsil_station의 비연(가칭) (author-described)
- 증거 기반: 사용자가 포스트 전문+댓글+프롬프트 전문을 직접 제공.
  영상 자체는 미확인 — 사용자가 다운로드 후 프레임 보강 예정.
  prompt-derived + user-provided-post. frame-observed는 보강 시 추가

**관찰 — 프롬프트 구조** (prompt-derived, 전문)
- 첫 줄 전제 선언: "원본 영상을 모션 레퍼런스로만 사용한다."
- [캐릭터]: "영상의 인물은 오직 @Image1을 유일한 캐릭터
  레퍼런스로 사용한다." 얼굴·헤어·체형·신체 비율·외모·의상 유지,
  프레임·카메라 변화에도 안정. "@Image1에 없는 새로운 인물이나
  캐릭터는 추가하지 않는다." — 원본에 두 인물이 싸우는데도
  캐릭터 레퍼런스는 @Image1 하나만 허용 (두 파이터 모두 동일
  외형으로 렌더되는 구조 — prompt-derived, 프레임 미확인이라
  실제 렌더는 미검증)
- [의상]: 디자인·색상·소재·레이스·장식·액세서리·스타킹·신발의 주요
  특징 강하게 유지, 영상 중 임의 변경 금지
- [모션]: "원본 영상에서는 오직 두 인물의 움직임, 자세, 대치,
  상호작용, 액션 순서, 타이밍과 카메라 움직임만 가져온다. 원본의
  인물이나 외형은 복사하지 않고 @Image1의 캐릭터가 동일한 모션을
  수행한다." 손·팔 움직임, 중심 이동, 다리 움직임, 공격·방어 동작의
  액션 흐름 유지
- [배경]: 원본 배경 완전 무시 → "깊고 음침한 자연 동굴 내부"로
  교체 (거대 암벽, 불규칙한 바위, 습기·물방울, 울퉁불퉁한 암반+흙
  바닥, 젖은 돌·작은 물웅덩이, 차갑고 어두우며 긴장감). "인물은
  얼굴과 의상이 명확하게 보이도록 적절한 보조광을 유지한다."
  (조명 고정). 네거티브 리스트: 체육관·경기장·관중석·운동장·무대 등
  원본 배경 요소 절대 등장 금지
- [카메라]: 원본의 카메라 이동·줌·팬·촬영 거리·타이밍 유지. 단
  "원본의 자막, 텍스트, 로고, 워터마크, 그래픽은 절대 복사하지
  않는다."
- [오디오]: "원본 오디오는 완전히 무시한다." 음악·대사·목소리·
  효과음 미사용 → "새로운 오리지널 오디오를 생성한다."
  동굴 울림·물방울·발걸음·흙과 돌 밟는 소리·의상 마찰음·액션 효과음
- 말미 핵심 요약 5줄: 원본=모션과 카메라 레퍼런스만 / @Image1=
  캐릭터와 의상 레퍼런스 / 배경=음침한 자연 동굴 / 자막·로고·
  워터마크=완전 무시 / 오디오=완전히 새롭게 생성

**관찰 — 작성자 코멘트** (user-provided-post, author-described)
- "일단 성별은 동일하면 좋을거 같아요" — 모션 전이 시 원본 출연자와
  생성 캐릭터의 성별 일치가 유리하다는 작성자의 체감
- "원본 오디오를 아예 죽이고도 한번 테스트 해봐야 할거 같아요.
  프롬에 오디오 지시 넣어도 잘 안먹네요😅" — [오디오] 섹션의 "완전히
  무시" 지시가 프롬프트만으로는 잘 안 먹는다는 실패 관측.
  원본 오디오가 새 오디오 생성에 새는(leak) 현상. #19의 실패 기반
  네거티브, #47의 per-shot SFX와 연결되는 실패 데이터
- 댓글 반응: zcre.co.kr "이건 너무 디테일하게 잘 만들었잖아요",
  pyona_ai "이...이게 된다고???", watchmegom "액션 시퀀스 영상만
  많이 확보한다면 액션씬으로도 활용도가 높겠다" — 모션 레퍼런스
  풀(pool) 확보가 액션씬 생산성으로 직결된다는 커뮤니티 반응

**관찰 vs 추론**
- 관찰: 프롬프트 전문 7섹션, 작성자 코멘트 2건 (성별 일치·오디오
  실패), 커뮤니티 반응 3건
- 미확인: 영상 프레임 (사용자 다운로드 후 보강), 실제 모션 전이
  품질, 두 파이터의 실제 외형 (프롬프트상 동일 외형), 오디오
  실패의 재현성
- 추론: 없음

**코퍼스 정합**
- Reference Role Separation (MeiGen 종합 패턴 #5): #51의
  "video_1=안무·타이밍만, 출연자 외형은 전이 금지"와 동형 — 이 케이스는
  "원본=모션+카메라만, @Image1=캐릭터+의상만"으로 역할 분리가 더
  명시적
- #53의 정체성 마스터 스위치와 동형의 단일 레퍼런스 고정
  ("오직 @Image1을 유일한 캐릭터 레퍼런스")
- #50의 Relational Negative와 동형의 배경 네거티브 리스트
  (체육관·경기장·관중석 절대 금지)
- #54 8역할론의 음향 역할 (화면의 원인→소리)과 정합되는 [오디오]
  섹션 — 단, 작성자 관측상 지시 이행이 안 되는 실패 케이스

**Production description → Control Levels**
- Hard Lock: "원본=모션+카메라 레퍼런스만, @Image1=캐릭터+의상
  레퍼런스" 역할 분리 선언. 자막·텍스트·로고·워터마크·그래픽 절대
  복사 금지. 원본 배경 요소(체육관·경기장·관중석 등) 절대 등장 금지.
  @Image1 외 신규 인물 추가 금지
- Soft Guidance: 배경을 음침한 자연 동굴로 교체 (보조광 유지),
  원본 카메라 이동·줌·팬·타이밍 유지, 오리지널 오디오 신규 생성
  (동굴 울림·물방울·발걸음·의상 마찰음)
- Creative Freedom: 없음 (프롬프트가 전 구간을 잠금)

**기여 패턴**: 1 (신규 — 모션 전용 레퍼런스 선언: 실영상을 모션+
  카메라로만 쓰고 외형 전이를 원천 차단. #51의 안무 전용 전이보다
  명시적), 2 (신규 — 오디오 무시 지시의 프롬프트 이행 실패:
  author-described 실패 데이터. "원본 오디오를 아예 죽이는" 전처리가
  필요하다는 가설), 3 (신규 — 성별 일치: 모션 전이 시 원본 출연자와
  생성 캐릭터의 성별 일치가 유리하다는 작성자 체감), 4 (배경 완전
  교체 + 네거티브 리스트 — #50 Relational Negative와 동형),
  5 (단일 캐릭터 레퍼런스 고정 — #53 정체성 마스터 스위치와 동형)

## 58. Facebook @류내원 — MiniMax H3 Character Swap LoRA 데모 (2×2 비교)

**기본 정보**
- 출처: Facebook reel (facebook.com/reel/2654859714968536),
  작성자 류내원, Public. 사용자가 "이거 비슷한 거야"라며 #57과
  함께 보라고 전달 (Kyoungryoul이 공유한 링크)
- 캡션 전문 (author-described): "MiniMax H3 Character Swap LoRA
  example / X toyxyz3님의 MiniMax H3 Character Swap LoRA 테스트
  사례입니다. / MiniMax H3 Character Swap LoRA에 대한 설명은 이전 글
  참고: https://www.facebook.com/share/p/1KGs7ZkT4E/ / LoRA:
  https://huggingface.co/akatz-ai/MiniMax-H3-Character-Swap-LoRA /
  #CharacterSwap #MiniMaxH3 #LoRA #AiVideoCreation #AiVideoGeneraion
  #영상제작 #wonwizard"
- Like 35, Shares 14. 영상 길이는 페이지에 표시 없음
- 증거 기반: browser-described (브라우저 읽기 전용 태스크로 릴
  공개 시청 — 로그인 월은 X 버튼으로 닫힘). 프레임 미추출,
  프롬프트 미공개 — LoRA 데모라 프롬프트 자체가 산출물이 아님

**관찰 — 영상 구성** (browser-described)
- 2×2 비교 그리드: 왼쪽 열=원본 실사 영상, 오른쪽 열=애니메이션
  스타일로 캐릭터 스왑된 버전. 동일 포즈·동일 장면
- 상단: 검은 가죽 의상의 여성이 목조 벽/창문의 매트릭스식 도장에서
  선 자세 (원본) → 분홍 머리 애니메이션 소녀로 스왑 (동일 장면)
- 하단: 주차장에서 역동적인 무술/댄스 포즈의 실사 2인 (원본) →
  분홍 머리·빨강 머리 애니메이션 소녀 2인으로 스왑 (동일 포즈)
- 영상 내 텍스트 오버레이 없음

**관찰 vs 추론**
- 관찰: 캡션 전문, 2×2 그리드 구성, 상·하단 두 쌍의 스왑 내용,
  LoRA 링크 (HuggingFace akatz-ai/MiniMax-H3-Character-Swap-LoRA)
- 미확인: 영상 프레임 (미추출), LoRA 학습 방식·품질, 원본 X
  @toyxyz3의 테스트 원문
- 추론: 없음

**코퍼스 정합 — #57의 거울상**
- #57 (omonge222): 원본=모션+카메라만 가져오고 캐릭터·배경을
  교체. 이 케이스는 정반대 배분 — 원본=장면+모션+포즈를 유지하고
  캐릭터만 교체. 모션 레퍼런스 전이의 두 가지 역할 배분:
  ① #57식 (모션 추출, 나머지는 재생성) vs ② LoRA 스왑식
  (장면·모션 유지, 캐릭터만 교체)
- #51의 레퍼런스 역할 분리, #52의 캐릭터 시트 선행과 동형 —
  이쪽은 "학습된 캐릭터" (LoRA)가 정체성 레퍼런스 역할을 수행
- #57의 "원본과 비교영상 올립니다"와 동형의 비교 그리드 포맷
  (원본 vs 결과를 나란히) — 모션 전이 주장의 증거 제시 방식
- #54 8역할론의 미술감독 역할 (기준 이미지 선행 고정)이
  LoRA라는 형태로 구현된 사례

**배경 조사 — 공식 vs 커뮤니티** (browser.search, 2026-09-28)
- MiniMax H3 (2026-07-31 출시, omni-modal 비디오 모델)의 공식
  패러다임 자체가 레퍼런스 역할 분리: "Reference images lock what a
  subject looks like. Reference videos lock what it does." 프롬프트에서
  "Video 1"은 모션, "Image 1"은 캐릭터로 인덱스 지명 — #57의
  프롬프트 구조와 정확히 일치 (공식 문서: runware.ai MiniMax H3
  가이드)
- Character Swap LoRA (akatz-ai, HuggingFace)는 커뮤니티 제작 —
  MiniMax 공식 제공이 아님. #58 캡션의 "X toyxyz3님의 테스트
  사례"도 커뮤니티 테스트
- 유사 커뮤니티 산출물: Alissonerdx의 head-swap LoRA
  (`minimax_h3_head_swap_v1.0_r32`, 트리거 `head_swap:` —
  얼굴 이미지는 native ref 경로, 원본 영상은 Add Guide로),
  FaceSwap_MiniMaxH3_REF2VA (트리거 `Faceswap`), mark9009의
  ComfyUI-H3-LongTake (얼굴 클로즈업을 ref_image_2로 연결하는
  캐릭터 스왑 워크플로우), Playtime-AI의 캐릭터 LoRA 시리즈,
  Turbo/StyleTransfer LoRA 등 — H3 ref2va용 LoRA 생태계가 형성 중

**Production description → Control Levels**
- Hard Lock: (LoRA 사용 시) 원본의 포즈·장면·카메라 구도는 유지,
  캐릭터만 교체 — 프롬프트가 아닌 학습된 가중치로 잠금
- Soft Guidance: 비교 그리드 (원본 vs 스왑)로 전이 품질을
  검증하는 제시 포맷
- Creative Freedom: 스왑 대상 캐릭터의 스타일 (이 케이스는
  애니메이션 스타일)

**기여 패턴**: 1 (신규 — 모션 전이의 거울상 배분: #57이
  모션만 취하고 장면을 버린다면, 이쪽은 장면·모션을 유지하고
  캐릭터만 교체. 목적에 따라 선택하는 두 가지 전이 전략),
  2 (신규 — LoRA=학습된 정체성 레퍼런스: #51/#52의 프롬프트 기반
  정체성 고정을 가중치로 구현), 3 (비교 그리드 — 모션 전이의
  증거 제시 포맷, #57과 동형)

## 59. Threads @jeong_do_ryeong — 프롬프트 엔지니어링+오케스트레이션 가이드 (텍스트 가이드)

**기본 정보**
- 출처: Threads @jeong_do_ryeong (AI Threads), 2026-09-29 게시.
  "[프롬프트 엔지니어링 가이드] AI 비디오 프롬프트 엔지니어링에서
  오케스트레이션(Orchestration) 가이드" — 본문 1개+작성자
  셀프리플라이 1개 (PART 1~3 전문). Like 5, Reply 1, Share 1
- 첨부 영상 1개 (browser-described): AI 생성 영상, 하단 중앙 흰색
  "Newtak" 워터마크 (inference: Newtake로 생성된 것으로 보임).
  빗물 젖은 밤거리 부츠 클로즈업과 네온 복싱짐 장면이 교차.
  영상 길이는 페이지에 표시 없음 (프레임 미추출)
- 증거 기반: text-guide (가이드 전문) + browser-described (첨부
  영상). 채굴할 프롬프트 없음 — 이론 가이드이므로 #50·#54와
  동급

**관찰 — PART 1: 프롬프트 엔지니어링 4대 법칙** (text-guide)
1. 관찰 가능한 시각 증거 서술 (Write the Visible): "멋진",
   "긴장감 넘치는" 같은 추상·감정 형용사 금지 → 카메라에 포착되는
   물리적 상태 변화와 관찰 가능한 동작으로 치환. ❌"영웅이 엄청나게
   멋지고 강력하게 땅에 착지한다" → ✅"수퍼히어로가 20m 높이에서
   수직 하강하여 무릎을 굽히며 지면을 강타한다. 타격 순간 먼지가
   방사형으로 폭발하고 충격파가 번진다"
2. Phase 기반 시공간 분할 (Phase Grammar): 접근→충돌 정점→
   반발력 및 에너지 전달→감쇠 및 잔여 상태의 4단계 인과 사슬.
   젤리화(Morphing)·무중력·시간순서 엉킴 예방
3. 인과적 카메라 동기화 (Camera Causality): 카메라는 물리적 사건에
   반응해서만 움직임. 충돌 전 이유 없는 흔들림=Shake Leakage
   금지, 충돌의 정확한 마이크로초에만 Directional Camera Jolt 발동
4. 정체성 및 물리적 경계 고정 (Boundary & Identity Lock):
   신체 융합(Cronenberg Effect)·메쉬 관통 방지. "5개의
   해부학적으로 정확한 손가락", "피사체 간 명확한 물리적 경계 유지"

**관찰 — PART 2: 오케스트레이션 5단계 파이프라인** (text-guide)
- 정의: 단일 텍스트 문장에 운을 맡기지 않고 피사체·카메라·물리학·
  시간축·조명·엔진 특성을 통합 파이프라인으로 연결·제어·검증·
  변환하는 메타 연출 시스템. 연출 의도를 중간 표현(IR)으로 격상 →
  엔진별 입력 특성에 맞춰 하향 컴파일(Lowering)
- Stage 1 의도 파싱: 5대 시각 속성 (Subject & Identity /
  Action & Phase / Camera & Optics / Environment & Space /
  Physics & Dynamics)
- Stage 2 도메인 매핑: Performance (감정 명칭이 아닌 근육 반응·
  시선·땀·호흡) / Camera Causality / Spatial Integrity (배경
  토폴로지 고정)
- Stage 3 검증·수술: 5대 시공간 파탄 오류+자동 교정 공식 —
  ① Effect Dumping (사건→정점→강조→반응 순차 배치)
  ② Shake Leakage (충돌 전 스무스 트래킹, 충돌 프레임에만 Jolt)
  ③ Weightless Impact (충격량 비례 Displacement·Recoil 명시)
  ④ Anatomical Merging (물리적 경계 선언·손가락 고정)
  ⑤ Morphing (기하학적 형상 유지·배경 토폴로지 고정)
- Stage 4 엔진 Lowering: 서사형(Sora/Veo)→시네마틱 문장,
  모션·파라미터형(Runway/Kling)→압축+Negative 분리,
  노드 파이프라인(ComfyUI)→모션 브러시·뎁스맵·포즈프레임 조건값
- Stage 5 멀티숏 확장: 샷-그래프 확장, 인물/장소 일관성 유지.
  예시: EWS→Ground Level→OTS→Close-Up→Wide Pull-Out

**관찰 — PART 3: Universal Master Block 템플릿** (text-guide)
- 10대 마스터 블록: [SCENE CONTEXT] / [FIRST FRAME & BLOCKING] /
  [SUBJECT & IDENTITY LOCK] / [MOTION & PHASE SEQUENCE]
  (Phase 1 Approach→2 Impact Peak→3 Force Transfer→4 Settling) /
  [CAMERA TRAJECTORY & OPTICS] / [LIGHTING & COLOR PALETTE] /
  [PHYSICS & DYNAMICS] / [SURFACE & PERFORMANCE] /
  [OUTPUT SETTINGS & STYLE]

**관찰 vs 추론**
- 관찰: 가이드 전문 (PART 1~3), 첨부 영상 설명, 워터마크 "Newtak"
- 미확인: 첨부 영상 프레임 (미추출), 가이드 주장의 실증 여부
- 추론: Newtake 생성 (워터마크 기반) — inference로 분리

**코퍼스 정합 — 이 가이드는 코퍼스의 이론화**
- Write the Visible = #50의 Visual Evidence 병기, 코퍼스의
  증거-tier 기율과 동형 (추상어 금지→관찰 가능한 서술)
- Phase Grammar = #48의 10비트, #49의 철칙 구조의 일반화
- Shake Leakage / Cronenberg Effect = 명명된 실패 모드.
  #19의 실패 기반 네거티브, #24의 명명된 실패 케이스와 동형 —
  "Shake Leakage"는 코퍼스 신규 용어
- Engine Lowering (IR→엔진별 컴파일) = 사용자의 XAI-Studio-Video
  (Master Spec→모델별 어댑터)와 정확히 일치. #56의 마스터
  프롬프트 체인과도 정합
- 5대 오류+교정 공식 = #54의 QC 역할, #57의 오디오 누출 실패
  데이터와 같은 "실패→교정 공식" 문법
- 멀티숏 샷-그래프 = MeiGen Trailer Montage 패턴, #47의
  15샷 조립의 이론화

**Production description → Control Levels**
- Hard Lock: 추상·감정 형용사 금지 → 관찰 가능한 물리적 상태
  변화로 치환 (Write the Visible). 액션은 Phase 1~4 인과 사슬로
  서술. 카메라는 물리적 사건의 정확한 순간에만 반응 (Shake
  Leakage 금지). 피사체 간 물리적 경계 선언
- Soft Guidance: 5단계 오케스트레이션 파이프라인 (파싱→매핑→
  검증→엔진 Lowering→멀티숏 확장), 10대 마스터 블록 템플릿
- Creative Freedom: 없음 (가이드가 전 구간을 규격화)

**기여 패턴**: 1 (신규 — Phase Grammar 4단계: Approach→Impact
  Peak→Force Transfer→Settling. 코퍼스 액션 프롬프트들의 공통
  구조를 명명한 일반화), 2 (신규 — Shake Leakage: 충돌 전 카메라
  흔들림을 명명한 실패 모드+교정 공식), 3 (신규 — Cronenberg
  Effect: 신체 융합 실패의 명명), 4 (신규 — Engine Lowering:
  IR→엔진별 컴파일. 사용자 시스템과 독립 수렴한 아키텍처),
  5 (신규 — 5대 시공간 파탄 오류+자동 교정 공식: 실패→교정
  공식의 문법화), 6 (메타 — 이 가이드 전체가 코퍼스 귀납 패턴의
  이론화: #48/#49/#50/#53/#54/#56/#57의 발견이 각 섹션에 대응)

---

## 60. X @DavidCliff42190 — 일본 이너웨어 모닝 광고 (실사 레퍼런스 + 클로저 편집 콘티)

**기본 정보**
- 출처: X @DavidCliff42190 (2026-09-30 게시, 리포스트된 상업 영상).
  유니클로 LifeWear 스타일의 일본 이너웨어 광고 (마지막 샷에
  UNIQLO 로고 + "シンプルなのに" 카피)
- 영상 실측: 30.08초, 1280x720, 24fps, 722프레임. vxtwitter
  API 경유 mp4 직접 다운로드 성공 (yt-dlp 조각 다운로드는
  불안정했음). 키 프레임 8장 추출·관찰
- 사용자 요청: "AI 영상이 아니라 실제 영상 같은데" 확인 +
  이런 영상을 만들기 위한 콘티·기획·프롬프트 아이디어.
  이어진 논의에서 사용자가 클로저(관객의 뇌가 컷 사이를 메우는
  현상)를 이용한 편집 전략을 제안 → 아래 콘티는 그 원칙을
  반영한 개정판
- 증거 기반: frame-observed (추출 프레임) + user-described
  (기획 의도). AI 생성물이 아니므로 프롬프트 채굴 없음 —
  실사 레퍼런스를 AI로 재현하기 위한 역설계 콘티

**관찰 — 원본 영상의 4샷 구조** (frame-observed)
1. 침대 위 여성의 뒷모습 미디엄샷. 팔을 올린 기지개, 흩날리는
   긴 머리. 따뜻한 아침 침실광, 얕은 심도. 노출은 등으로만 암시
2. 옆모습 익스트림 클로즈업. 얼굴에 흩날리는 머리카락, 희미한
   미소. 자막 "おはよう"(좋은 아침)
3. 거울 샷. 베이지 심리스 브라를 입고 스트랩을 정리하며 거울
   속 자신과 눈을 맞춤. 커튼 사이 데이라이트. 자막 "シンプル
   なのに ぷるんと美胸"
4. 포니테일로 묶은 옆모습 클로즈업, 밝은 미소. UNIQLO
   LifeWear 로고 + "シンプルなのに" 태그라인 오버레이

**핵심 원칙 — AI는 모멘트를, 편집은 모션을** (user-described +
  assistant-synthesized)
- 사용자 통찰: 사람은 내용이 잘 이어지면 컷 사이 빠진 부분을
  알아서 상상해서 채움 (클로저/쿨레쇼프 효과). AI에게 "이어지게"
  시키면 사이 구간을 어거지로 채우려다 모핑이 터져서 오히려
  실감이 떨어짐
- 전략 반전: AI에게는 완결된 "비트"(정점 모멘트)만 생성시키고,
  사이 구간은 만들지 않음. 연결은 하드컷+관객의 뇌가 담당
- #59 Phase Grammar의 선별 적용: Phase 1(Approach)과
  Phase 3(Force Transfer)은 통째로 생략, Phase 2(Peak)와
  Phase 4(Settling)만 생성. 정점끼리는 인과가 자명해서 뇌가
  메우기 쉬움
- 함정: 틈은 "상상 가능한" 크기여야 함. 인과 사슬이 끊기면
  클로저가 아니라 혼란이 됨 (침대→거울은 상상 가능,
  침대→갑자기 바다는 불가)

**개정 콘티 — 샷별 상세** (클로저 편집 반영)

■ 전체 편집 문법
- 4샷 전부 하드컷. 트랜지션 이펙트·디졸브 금지 (AI 모핑 구간을
  감추려다 오히려 가짜 느낌이 남)
- 각 클립은 필요한 길이보다 길게 생성 → 앞뒤 1초가량의 모핑
  구간을 잘라내고 중간만 사용. 인점=모션이 시작된 후,
  아웃점=정점 또는 정돈 상태
- 오디오 베드: 룸톤+침구 바스락거림을 0–30초 전 구간에 연속
  배치. 화면은 끊겨도 소리가 이어지면 뇌는 "같은 장면"으로
  믿음. 샷 경계에 J-컷/L-컷 (소리를 먼저 넘김)
- 자막·로고·카피는 전부 후반 작업에서 오버레이. AI에게 텍스트
  렌더링을 시키지 않음 (깨질 확률 높음)

■ Shot 1 (0–8s): 기지개 — 침대 뒷모습
- 카메라: 미디엄샷, 고정+매우 느린 푸시인
- 생성할 것: 팔을 올린 기지개의 정점 전후 6초. 뒷모습,
  머리카락이 흩날리다 정돈되는 흐름. 따뜻한 좌측 윈도우 키,
  얕은 심도, 린넨 침구 전경
- 인점: 팔이 이미 올라가기 시작한 후 (첫 1초 모핑 구간 버림)
- 아웃점: 팔이 내려오며 머리카락이 가라앉는 순간
- 관객이 채우는 것: "잠에서 깼다"는 전사 — 보여주지 않음
- 오디오: 이불 바스락거림 시작 → Shot 2로 L-컷 (소리가 먼저 넘어감)
- 프롬프트:
```
IDENTITY LOCK: East Asian woman, late 20s, long dark-brown wavy hair,
natural no-makeup look, soft facial features, calm gentle demeanor.
Same person in every shot. Photorealistic, premium commercial aesthetic.
Medium shot from behind: the woman sits on a bed in a warm bedroom,
arms raised in a slow morning stretch, long hair falling and swaying
softly then settling. Bare back to camera, tasteful and non-explicit,
artistic. Warm morning window light from the left, shallow depth of
field, soft linen bedding foreground. Camera: static with very slow
push-in. End on arms lowering, hair at rest. No text, no watermark.
```

■ Shot 2 (8–13s): 속삭임 — 옆모습 클로즈업
- 카메라: 프로필 익스트림 클로즈업, 미세한 슬로우 드리프트
- 생성할 것: 머리카락 사이로 번지는 미소의 정점 5초.
  밝은 소프트 키, 깨끗한 배경
- 매치컷 노트: Shot 1에서 머리카락이 흩날린 방향과 동일한
  방향으로 머리카락이 얼굴을 스치게. 방향만 맞으면 뇌가 연결함
- 관객이 채우는 것: 침대에서 일어나 세면대/거울 앞으로 이동한
  과정 — 통째로 생략
- 자막 "좋은 아침"은 후반 작업 (AI 텍스트 렌더링 금지)
- 프롬프트:
```
[IDENTITY LOCK]
Extreme close-up profile of her face, soft genuine smile blooming
through strands of hair drifting slowly across her cheek in the same
direction as the previous shot. Bright soft key light, shallow depth
of field, clean light background. Intimate, whisper-quiet mood.
Subtle slow camera drift. Hold the smile at its peak. No text, no watermark.
```

■ Bridge Beat (13–16s): 브라를 집는 손 — 인과의 경첩
- 사용자 제안의 구체화: 누드처럼 보이는 상태(A) → 브라를 집는
  제스처 → 입은 모습(B). 가운데 제스처가 인과를 이어주는 경첩
  역할을 해서, 뇌가 "입는 과정"을 통째로 상상함
- 왜 이 제스처가 정답인가: "입는 과정"은 끈 흔들림+팔 끼우기+
  위치 잡기의 연속 물리라 AI가 못 만듦. 반면 "집어 드는 동작"은
  단일 제스처의 정점 — 필요한 물리는 중력에 의한 원단 드레이프
  뿐이라 2–3초 인서트에서는 AI가 감당 가능. 과정 전체를 가장
  상징적인 한 동작으로 대체하는 것
- 카메라: 클로즈업 인서트샷, 얕은 심도. 침대 협탁(또는 침대 위)에
  놓인 베이지 심리스 브라를 손가락이 집어 드는 순간
- 생성할 것: 손이 브라를 집어 올리고, 끈이 살짝 흔들리다
  가라앉는 3초. 원단의 자연스러운 드레이프
- 매치컷 노트: Shot 4(거울)의 브라와 동일한 베이지 심리스
  디자인, 동일한 손/피부톤. 집어 든 브라가 화면 오른쪽으로
  나가면, 다음 샷 거울상은 오른쪽에서 등장하는 느낌으로
- 관객이 채우는 것: 입는 과정 전체
- 프롬프트:
```
[IDENTITY LOCK]
Close-up insert shot, shallow depth of field: a woman's hand reaches
for a beige seamless bra resting on a bedside table and lifts it,
fingers grasping the fabric gently. The bra drapes naturally with
gravity, one strap swaying softly then settling. Warm morning light,
intimate quiet mood. Single decisive gesture, hold the lifted peak
moment. No text, no watermark.
```

■ Shot 3 (16–24s): 거울 — 스트랩 정리
- 카메라: 거울 앞 미디엄샷 (본인+거울상 동시 프레임)
- 생성할 것: 스트랩 정리를 마치고 거울 속 자신과 눈을 맞춘
  정점 8초. 베이지 심리스 브라, 커튼 사이 데이라이트
- 관객이 채우는 것: 브라를 입는 과정 — 보여주지 않음.
  (옷 입는 과정은 AI가 가장 깨지기 쉬운 구간이므로 생략 자체가
  품질 전략. Necessity Test: 보여주지 않아도 되는 건 보여주지
  않는다)
- 주의: 미러 리플렉션 물리가 AI 약점. 리플렉션이 어긋나면
  여러 번 재생성하거나, 대체안으로 거울 없이 창가 샷으로 변경
- 프롬프트:
```
[IDENTITY LOCK]
The woman stands before a full-length mirror wearing a beige seamless
bra, having just finished adjusting one strap, making soft eye contact
with her reflection. Bright daylight through sheer curtains behind her.
Clean, minimal premium lingerie-commercial look. Real mirror reflection
must match her pose exactly. Slow subtle camera movement. Hold the
composed final pose. No text, no watermark.
```

■ Shot 4 (24–30s): 포니테일 미소
- 카메라: 프로필 클로즈업, 젠틀한 슬로우 드리프트
- 생성할 것: 로우 포니테일로 묶은 머리의 밝은 미소 정점 5초.
  밝고 균일한 소프트광, 상쾌한 아침 에너지
- 관객이 채우는 것: 머리를 묶는 과정 — 생략
- 브랜드 로고·태그라인은 후반 작업에서 오버레이 (가상 브랜드명
  사용, 실존 상표 금지)
- 프롬프트:
```
[IDENTITY LOCK]
Close-up profile, hair tied in a low ponytail, bright genuine smile,
looking slightly upward. Clean bright soft-lit background, fresh
morning energy. Gentle slow camera drift. Hold the smile at its peak.
No text, no watermark.
```

■ 편집 타임라인 (30초)
```
영상: [Shot1 0–8s] hard cut [Shot2 8–13s] hard cut [Bridge 13–16s] hard cut [Shot3 16–24s] hard cut [Shot4 24–30s]
오디오: |=== 룸톤+바스락거림 연속 베드 (0–30s) ===| + "좋은 아침" 속삭임 (8s 지점)
자막:                    [좋은 아침]      [심플한데도, 탄력 있는 아름다움]   [브랜드 로고]
```
- 속삭임 오디오는 영상 생성과 분리: TTS 또는 직접 녹음 후
  믹싱 (#57 교훈 — 오디오 지시는 프롬프트에서 잘 안 먹음)

**관찰 vs 추론**
- 관찰: 추출 프레임 8장의 샷 구성·조명·자막·브랜드,
  영상 실측치 (30.08초/720p/24fps)
- 미확인: 원본 광고의 실제 브랜드 캠페인명, 촬영 스펙
- 추론: 유니클로 LifeWear 캠페인 계열 (로고·카피 기반) —
  inference로 분리. 사용자의 재현물은 오리지널 기획으로
  진행 (실존 상표 사용 금지)

**코퍼스 정합**
- 클로저/쿨레쇼프 = 코퍼스 신규 명명. #59 Phase Grammar의
  실전 운용법 (Peak/Settling 선별 생성)
- "보여주지 않아도 되는 건 보여주지 않는다" = Necessity Test의
  편집 적용 (브라 착용 과정 생략)
- 오디오 분리 믹싱 = #57의 오디오 누출 실패 데이터의 역이용
- 매치컷 방향 일치 = #14의 매치컷 체인
- 앞뒤 1초 버리고 중간만 사용 = #19/#24의 실패-회피 편집
  (모핑이 터지는 구간을 생성하지 않고 잘라냄)

**Production description → Control Levels**
- Hard Lock: 전부 하드컷, 트랜지션 금지. 각 클립 앞뒤 모핑
  구간 제거 후 중간만 사용. 자막·로고·카피의 AI 렌더링 금지
  (후반 오버레이). 실존 브랜드명 사용 금지
- Soft Guidance: Peak/Settling 선별 생성, 오디오 브리지+J/L컷,
  매치컷 방향 일치, Identity Lock 4샷 고정, 미러샷 리플렉션 검증
- Creative Freedom: 비트 순서, 자막 카피, 속삭임 대사, 브랜드명

**기여 패턴**: 1 (신규 — 클로저 편집: AI는 모멘트만 생성하고
  사이는 관객의 뇌에 맡기는 전략. "AI는 모션을 만들게 하지
  말고 모멘트를 만들게 하라"), 2 (신규 — 생략 자체를 품질
  전략으로: 깨지기 쉬운 구간은 생성하지 않고 잘라냄),
  3 (정합 — #59 Phase Grammar, #14 매치컷, #57 오디오
  분리, Necessity Test의 실전 조합), 4 (신규 — 상태 A →
  제스처 → 상태 B: AI가 못 만드는 연속 과정(끈 흔들림·팔
  끼우기·위치 잡기)을 가장 상징적인 단일 제스처(브라를 집어
  드는 손)로 대체. 제스처가 인과의 경첩이 되어 뇌가 과정
  전체를 상상함)

---

## 62. X @ALauchaire9dap — 태국 드라마 탱크톱 벗기기 (실사 모션 분석)

**기본 정보**
- 출처: X @ALauchaire9dap, 2026-09-30 게시. 포스트 본문은
  미러 링크 2개뿐 (cdnw.twiwg.ink). 379 likes. 영상은 태국
  Channel 3 드라마 클립으로 보임 (우상단 "3 HD" 로고)
- 영상 실측: 16.07초, 1280x720, 30fps, 482프레임.
  vxtwitter API 경유 mp4 직접 다운로드 성공 (yt-dlp 조각
  다운로드는 실패). 오디오 스트림 존재 (미청취)
- 증거 기반: frame-observed (2fps 32장 + 벗기기 구간 6fps).
  사용자 질문: "옷을 벗기는 움직임을 AI로 재현할 수 있을까?"

**관찰 — 타임라인**
- 0–5s: 두 여성이 포옹. 한 명은 줄무늬 탱크톱, 다른 한 명은
  흰 톱 착용
- 5.5–7.5s: **탱크톱 벗기기** (상대방 보조). 밑단을 잡고 위로
  끌어올림 → 옷이 머리 위에서 뭉치며 얼굴 완전 가림 →
  긴 머리카락이 옷에 걸려 함께 흔들림 → 팔이 빠지면서 옷이
  자유 물체가 됨 → 우상방으로 날아감
- 7.5–16s: 키스 지속. 흰 톱은 끝까지 착용 상태 유지

**관찰 — 벗기기 모션의 5단계 분해**
1. Grip: 밑단을 잡는 손. 몸 뒤쪽이라 손이 가려진 채 시작
2. Pull-up: 옷이 몸통을 따라 위로 미끄러지며 늘어남
3. Head-pass: 옷이 머리를 덮음. 얼굴 완전 오클루전, 머리카락
   간섭 발생
4. Release: 팔이 빠지면서 옷이 신체에서 분리, 위상 변화
   (입은 옷 → 뭉친 천 → 자유 물체)
5. Toss: 2차 모션. 옷이 관성으로 날아감

**판정 — AI 재현 가능성**
- 원테이크 직접 재현: **불가에 가까움**. 5대 파탄 지점:
  ① 가려진 채 밑단을 잡는 손가락 (오클루전 하의 손 몰핑)
  ② 얼굴이 옷에 가려졌다 드러나는 순간 (가림-드러남 경계의
  identity drift — 얼굴이 바뀌어 나옴)
  ③ 옷의 위상 변화 (입은 상태→뒤집힌 뭉침→날아가는 물체 —
  연속 모션으로 표현 불가한 불연속 상태 전이)
  ④ 머리카락-옷 간섭 (두 개의 서로 다른 물리계가 얽힘)
  ⑤ 2인 협동 타이밍 (보조하는 손과 벗는 몸의 동기화)
- 브릿지 비트 + 컷 전략: **가능**. #60의 "상태 A → 제스처 →
  상태 B"를 그대로 적용:
  샷1 상태A (입은 채 포옹) → 브릿지 (밑단을 잡고 끌어올리는
  손 클로즈업 인서트 — 얼굴은 프레임 밖) → 컷 → 샷2 상태B
  (날아가는 옷 단독 샷 + 맨어깨, 가라앉는 머리카락).
  머리 통과(Head-pass) 순간은 절대 직접 렌더하지 않고
  브릿지/컷 안에 숨김
- #60 대비: 사용자가 #60에서 "입는 동작(끈 흔들림·팔 끼우기)은
  AI가 못 만든다"고 했는데, 벗기기는 다른 축으로 어려움.
  입기가 미세 손-원단 정밀도에서 깨진다면, 벗기기는
  가림-드러남 경계의 얼굴 드리프트 + 옷의 위상 변화에서
  깨짐. 단, 벗기기가 컷 친화적이라 브릿지 전략은 더 잘 먹음
- 정책 레이어 (별개 장벽): 상용 비디오 모델의 undressing
  필터는 기술적 가능성과 무관하게 작동. 우회 방법은 다루지
  않음

**규칙 카드 (붙여넣기용)**
```
[가림-드러남 경계 비렌더 원칙 — Hard Lock]
얼굴·신체가 옷/물체에 완전히 가려졌다가 드러나는 순간
(head-pass, occlusion-reveal boundary)은 연속 생성으로
절대 렌더하지 않는다. 그 순간은 브릿지 비트(손 클로즈업
인서트 등) 또는 컷 안에 숨기고, 상태 A(가려지기 전)와
상태 B(드러난 후)만 보여준다. 경계를 렌더하면 identity
drift가 확정적으로 발생한다.
```

**관찰 vs 추론**
- 관찰: 위 전부와 5단계 분해, 5대 파탄 지점의 위치
  (프레임 기반)
- 추론: "원테이크 불가" 판정은 현행 모델들의 오클루전-리빌
  실패 패턴에 대한 일반적 지식에서 온 추론. 특정 모델로
  테스트한 것은 아님 — inference로 분리
- 미확인: 드라마 제목, 오디오 내용

**코퍼스 기여**
- 6 (신규 — 가림-드러남 경계 비렌더 원칙. #60의 브릿지
  비트를 오클루전-리빌 문제에 특화한 것. 옷의 위상 변화를
  불연속 상태 전이로 명시한 것도 신규), 5 (정합 — #60의
  "상태 A → 제스처 → 상태 B" 직접 적용 사례)

---

## 61. X @GrayNoteLab(灰度笔记) — 점진적 광학 줌 고풍 서사 (프롬프트 전문)

**기본 정보**
- 출처: X @GrayNoteLab (灰度笔记), 2026-09-30 게시.
  "变焦切换景别是AI视频创作常用的方法" — 줌 경별 전환
  가이드. 프롬프트 전문이 포스트 본문에 공개 (중국어)
- 영상 실측: 15.09초, 3840x2160(다운로드본), 24fps 추정.
  vxtwitter API 경유 mp4 직접 다운로드 성공. 오디오 스트림
  존재 (대사 "好久不见"의 실제 발화 여부는 미확인).
  키 프레임 7장 추출·관찰 (f01/f04/f06)
- 증거 기반: prompt-derived (전문) + frame-observed.
  포스트 상단 번역: "好久不见 🥳 / 줌으로 경별(샷 사이즈)을
  바꾸는 건 AI 영상 창작에서 자주 쓰는 방법~ / 주인공을
  교묘하게 보여줄 수 있어 🙌🙌 / 프롬프트는 아래와 같아:"

**프롬프트 전문 (중국어 원문)**
```
【全局设定】
古风写实电影镜头，东方古典生活叙事，雨后江南古镇：青石台阶、
青砖黛瓦、木质廊檐、雕花木门、竹帘、湿润石板巷道。阴天柔和漫射光，
低对比度，冷灰青与温暖木色融合，轻微35mm胶片颗粒，真实皮肤、
木石与织物纹理，电影级浅景深，8K，16:9。

女主A：图1
女主B：图2

全片严格保持角色身份、空间位置、左右关系、行进方向、天气、
光线、色调连续。

【核心摄影技法】
全片以"渐进式光学变焦"为唯一核心运镜。摄影机尽量固定机位，
不依赖实体移动，通过缓慢连续的光学推近、拉远改变人物画面占比
与空间关系。保持真实镜头压缩、景深变化和光学特征，禁止数字裁切。
前景遮挡、浅景深、焦点转移辅助叙事，形成"远处发现→隔巷对视→
空间压缩→情绪确认"。

【0-4s】
中景起幅，35mm，固定机位，视线高度。女主A沿青石台阶缓慢下行至
巷口，停步转身抬头，看见远处廊檐下的女主B。镜头从较宽环境关系构图
开始，仅缓慢光学推近，逐渐收紧至女主A中景，摄影机不移动。

古镇行人先后从左右前景横向经过，近距离形成自然虚化遮挡，女主A
始终保持清晰；遮挡期间曝光、色温、光影稳定。变焦持续平滑克制，
最终形成女主A与远处女主B隔巷对视。

【4-9s】
承接上一段，机位完全不变。女主B从画面右侧前景缓慢进入，靠近
木质廊柱，与廊柱形成天然前景框；女主A位于左中部巷道深处。

缓慢连续光学变焦，女主A先保持清晰，随后画面逐渐收紧，女主B前景
占比增大，女主A退入背景并柔和虚化。逐渐进入长焦端，通过真实空间
压缩使古巷纵深被压缩，两人实际距离不变，但视觉距离明显拉近。
焦点平滑由女主A转向女主B，最终女主B侧脸清晰、女主A虚化。
摄影机不横移、不摇摄、不绕拍，曝光与色调连续。

【9-13s】
保持固定机位与长焦关系。女主B站在木质廊柱旁缓慢转身，看向女主A。
仅进行一次极缓慢光学推近，从双人关系构图收紧至女主B中近景。
画面左侧保留女主A局部虚化轮廓，形成窥视式前景框架。

女主B成为主要焦点，看向女主A，短暂停顿后轻声说："好久不见。"
露出极轻微笑意。竹帘被雨后微风吹动，屋檐水滴自然落下，湿润青石
反射柔和天光。镜头稳定推进，在近距离情绪确认中结束。

【镜头控制】
核心必须是"光学变焦制造叙事距离变化"，而非摄影机移动。镜头语言
依次完成：环境建立→发现女主A→缓慢收紧→女主B进入前景→长焦空间
压缩→焦点转移→情绪确认。变焦速度缓慢连续，具有真实镜头惯性；
保持自然人物比例、真实景深与稳定曝光，明确呈现光学变焦感，
但无廉价数码放大感。

【连续性与负面约束】
严格遵循角色卡，禁止外貌、发型、服装漂移；保持空间地理关系、
左右位置、运动方向、光线方向一致。禁止现代建筑、交通工具、
路牌、现代物件、字幕、水印；禁止新增主要人物、人物重复、
肢体异常、身份交换。禁止横移、环绕、快速推轨、突然摇镜、
无人机运动、强手持抖动、数字变焦、数码裁切、透视异常、焦距跳变、
景深瞬切、曝光闪烁、色温漂移、过度雾化、过度磨皮、AI塑料皮肤。
```

**프롬프트 한국어 번역**
- [전역 설정] 고풍 실사 영화 스타일, 동양 고전 생활 서사,
  비 온 뒤 강남 고진(江南古镇): 청석 계단, 청전대와(푸른 기와),
  목조 처마, 조각 목문, 죽렴, 젖은 석판 골목. 흐린 날 부드러운
  확산광, 낮은 대비, 냉회청(차가운 회청색)과 따뜻한 목재 색의
  융합, 미세한 35mm 필름 그레인, 리얼한 피부·목석·직물 질감,
  영화급 얕은 심도, 8K, 16:9
- 여주인공A: 그림1 / 여주인공B: 그림2 (캐릭터 카드 이미지
  레퍼런스)
- 전편에 걸쳐 캐릭터 정체성, 공간 위치, 좌우 관계, 진행 방향,
  날씨, 조명, 색조 연속성 엄격 유지
- [핵심 촬영 기법] 전편의 유일한 핵심 운경은 "점진적 광학 줌".
  카메라는 최대한 고정하고 물리적 이동에 의존하지 않으며,
  느리고 연속적인 광학적 푸시인/풀아웃으로 인물의 화면 비중과
  공간 관계를 바꿈. 실제 렌즈 압축·심도 변화·광학 특성 유지,
  디지털 크롭 금지. 전경 가림·얕은 심도·포커스 이동이 서사를
  보조하며 "먼 곳에서 발견→골목 사이 마주봄→공간 압축→감정
  확인"의 흐름 형성
- [0–4s] 미디엄샷 시작, 35mm, 고정, 시선 높이. 여주인공A가
  청석 계단을 천천히 내려와 골목 어귀에서 멈춰 돌아서서
  올려다보며 멀리 처마 아래 여주인공B를 발견. 넓은 환경 관계
  구도로 시작해 느린 광학 푸시인만으로 여주인공A 미디엄샷까지
  조임. 카메라 이동 없음. 고진 행인들이 좌우 전경을 차례로
  가로지르며 근거리에 자연스러운 아웃포커스 가림 형성,
  여주인공A는 계속 선명 유지. 가림 구간에도 노출·색온도·명암
  안정. 최종적으로 두 사람이 골목을 사이에 두고 마주보는 구도
- [4–9s] 카메라 위치 완전 고정. 여주인공B가 화면 오른쪽
  전경에서 천천히 들어와 목조 기둥에 다가가 천연 전경 프레임
  형성. 여주인공A는 왼쪽 중앙 골목 깊숙한 곳. 느리고 연속적인
  광학 줌으로 여주인공B의 전경 비중이 커지고 여주인공A는
  배경으로 물러나 부드럽게 아웃포커싱. 망원단으로 들어가 실제
  공간 압축으로 골목 깊이가 압축됨 — 두 사람의 실제 거리는
  그대로지만 시각적 거리는 확연히 가까워짐. 포커스가 부드럽게
  A에서 B로 이동, 최종적으로 B 옆모습 선명·A 흐릿. 패닝·틸트·
  회전 없음
- [9–13s] 고정 위치와 망원 관계 유지. 여주인공B가 기둥 옆에서
  천천히 돌아서며 여주인공A를 바라봄. 극도로 느린 광학 푸시인을
  한 번만 실시해 2인 관계 구도에서 여주인공B 미디엄
  클로즈업까지 조임. 화면 왼쪽에 여주인공A의 부분적 아웃포커스
  실루엣을 남겨 엿보는 듯한 전경 프레임 형성. 여주인공B가 주
  포커스가 되어 바라보다 잠시 멈춘 뒤 나직이 "好久不見
  (오랜만이야)". 극히 미세한 미소. 비 온 뒤 미풍에 죽렴이
  흔들리고 처마 물방울이 떨어지며 젖은 청석이 하늘빛을 반사.
  근거리 감정 확인으로 마무리
- [렌즈 컨트롤] 핵심은 "광학 줌으로 서사적 거리의 변화를
  만든다"는 것이지 카메라 이동이 아님. 순서: 환경 구축→A
  발견→느린 조임→B의 전경 진입→망원 공간 압축→포커스
  이동→감정 확인. 줌 속도는 느리고 연속적이며 실제 렌즈의
  관성을 가짐. 광학 줌 느낌을 명확히 살리되 값싼 디지털 확대
  느낌 금지
- [연속성 및 네거티브] 캐릭터 카드 엄격 준수, 외모·헤어·의상
  드리프트 금지. 현대 건축물·교통수단·간판·현대 오브제·자막·
  워터마크 금지. 인물 추가·인물 중복·사지 기형·정체성 뒤바뀜
  금지. 횡이동·주회·급속 푸시 트랙·급틸트·드론·강한 핸드헬드·
  디지털 줌·디지털 크롭·투시 이상·초점거리 점프·심도 급변·노출
  플리커·색온도 드리프트·과도한 안개·과도한 피부 보정·AI
  플라스틱 피부 금지

**관찰 — 프레임 정합** (frame-observed)
- f01: 여주인공A(연청 드레스, 땋은 머리)가 청석 계단을 내려옴.
  좌상단 아웃포커스 우산 전경, 우측 목문 — 0–4s 구도와 일치
- f04: 여주인공B(전통 머리장식) 오른쪽 전경 프로필 선명,
  여주인공A 왼쪽 배경 흐릿 — 4–9s 포커스 랙 결과와 일치
- f06: 9초 이후 샷. **프롬프트와 달리 하드컷이 존재함.**
  d018(9.0s)→d019(9.5s)에서 카메라 앵글이 바뀜: d018까지는
  B의 옆모습(오른쪽 전경, A를 바라봄)+A가 왼쪽 배경에 흐릿하게
  있었는데, d019부터는 B가 카메라를 정면으로 보다시피 바라보고
  A의 뒷모습이 왼쪽 전경에 크게 아웃포커스로 잡힘. 0.5초 만에
  일어날 수 없는 구도 변화이므로 연속 무브가 아닌 하드컷.
  프롬프트의 "机位完全不变/保持固定机位" 주장과 실제 출력이
  어긋난 지점
- 같은 공간으로 느껴지는 장치 (컷을 봉합하는 고전 문법):
  ① 180도 법칙 — 컷 전후 B는 오른쪽, A는 왼쪽으로 좌우 관계
  유지. 축을 넘지 않아 뇌가 같은 공간으로 인식
  ② 시선 매치 — d018에서 B가 왼쪽(A 방향)을 바라보다가,
  d019에서는 A 쪽에서 본 B가 됨. 시선의 방향이 이어짐
  ③ 기둥 앵커 (축 오브젝트) — 목조 기둥이 컷 전후 모두 화면
  중앙에 있어 공간의 축 역할. 프롬프트는 기둥을 두 번 언급
  ("B가 기둥에 다가가 천연 전경 프레임을 형성", "B가 기둥 옆에
  서서 돌아섬")하지만 어디까지나 B의 위치 설명일 뿐, 컷을
  넘어서는 앵커로 쓰라는 지시는 없음 (프롬프트는 컷이 없다고
  주장하므로). 사용자 통찰: 기둥이 두 사람 *사이*에 있어서
  앵글이 바뀌어도 무의식이 기대하는 위치(중앙, 둘 사이)에
  그대로 있음. 액션의 축선 위에 있는 오브젝트는 리버스숏에서도
  좌우가 뒤집히지 않으므로 뇌가 "같은 장소"로 인식. 이를
  축 오브젝트(Axis Object)라 명명: 인물들 사이의 축선 위에
  두드러진 오브젝트를 배치하면 앵글 변경을 꿰매는 랜드마크가 됨
  ④ 포커스 상태 연속 — 컷 직전(B 선명/A 흐릿)과 직후 동일
  ⑤ 색조·조명·날씨·의상·헤어 완전 연속
  → 교과서적인 숏/리버스숏(shot/reverse-shot). 프롬프트가
  주장한 "고정 카메라"가 아니라 고전 연속성 편집이 실제로
  공간을 봉합한 것. #60의 클로저 테제와 정확히 일치:
  뇌가 두 앵글 사이를 같은 공간으로 꿰맴
- 미세한 불일치 2: 프롬프트 구간 합이 13초(0–4/4–9/9–13)인데
  실제 영상은 15.09초. 프롬프트 타임라인보다 여유 있게 생성된
  것으로 보임

**관찰 vs 추론**
- 관찰: 프롬프트 전문, 추출 프레임 3장의 구도·포커스 상태,
  오디오 스트림 존재, 영상 길이 실측치
- 미확인: "好久不见" 대사의 실제 발화 여부 (오디오 미청취),
  캐릭터 카드 이미지(图1/图2)의 내용
- 프롬프트 vs 출력의 어긋남: 프롬프트는 전 구간 카메라 고정을
  주장하지만, 실제 영상 9초 지점에 리버스 앵글로의 하드컷이
  있음. 자세히 보면 프롬프트 자체가 모순임: 9–13s 구간이
  "B가 기둥 옆에 서서 돌아서고, A의 뒷모습이 왼쪽 전경에
  흐릿하게 잡힘"이라는 리버스 구도를 묘사하면서 동시에
  "机位完全不变"을 선언. 고정 카메라로는 찍을 수 없는 구도.
  엔진(또는 편집자)은 이 모순을 하드컷으로 해소했고, 컷의
  연속성 장치(180도 법칙·시선 매치)는 자동 적용됨.
  기둥-두 사람 배치도 엔진의 독창이 아니라 프롬프트 제약
  (기둥 옆 B + 왼쪽 전경 A + 좌우 관계 락)이 기하학적으로
  강제하는 해. 엔진 언급은 포스트에 없음 (댓글 1개는 로그인
  월 뒤라 미확인) — 엔진 미상
- 추론: 없음

**코퍼스 정합**
- 광학 줌을 유일한 운경으로 고정 = 움직임의 최소화 역설.
  카메라를 안 움직일수록 서사가 선명해짐. #59의 Camera
  Causality와 정합 (줌은 서사적 거리 변화에만 반응)
- 망원 공간 압축의 감정적 사용 = 코퍼스 신규. 실제 거리는
  그대로인데 시각적 거리만 좁혀 "가까워진 마음"을 광학 현상
  그대로로 표현. 물리 장치를 서사 장치로 전환한 사례
- 전경 행인 가림막 = 자연스러운 와이프. #14의 매치컷 체인과
  정합. 가림 중 노출·색온도 안정까지 명시한 점이 정밀함
- 포커스 랙 서사 (A 선명→B 선명) = 시선의 주도권 이동을
  포커스로 표현. #42의 카메라 존재감과 같은 계열
- 캐릭터 카드(图1/图2) = #52의 시트-퍼스트, #57의 역할 분리
- 광학 특화 네거티브 (투시 이상·초점거리 점프·심도 급변·AI
  플라스틱 피부) = #19의 실패 기반 네거티브 어휘 확장

**Production description → Control Levels**
- Hard Lock: 카메라 위치 완전 고정, 광학 줌만 허용 (디지털 줌·
  크롭·패닝·틸트·주회·드론 전면 금지). 캐릭터 카드 준수,
  좌우 관계·진행 방향·조명 방향 일관. 현대 오브제·자막·
  워터마크 금지
- Soft Guidance: 점진적 광학 줌의 속도 (느리고 연속적, 렌즈
  관성). 전경 가림막의 배치, 포커스 랙의 타이밍, 망원 압축의
  정도. "발견→마주봄→압축→확인" 4단계 서사 아크
- Creative Freedom: 행인의 수·타이밍, 죽렴·물방울 등 환경
  디테일, 대사의 어조

**기여 패턴**: 1 (신규 — 광학 줌 단일 운경: 카메라 고정+줌만으로
  서사적 거리를 조종), 2 (신규 — 망원 공간 압축의 감정적 사용:
  실제 거리는 그대로, 시각적 거리만 좁혀 마음을 표현),
  3 (신규 — 전경 행인 가림막: 자연스러운 와이프+가림 중
  노출 안정 명시), 4 (확장 — 광학 특화 네거티브 어휘:
  초점거리 점프·심도 급변·AI 플라스틱 피부),
  5 (정합 — #59 카메라 인과성, #52 시트-퍼스트, #14
  매치컷 체인), 6 (신규 — 프롬프트 선언 vs 출력 실제의 어긋남:
  "카메라 고정"을 선언했지만 실제 출력은 9초에 리버스 앵글로
  하드컷. 숏/리버스숏의 고전 연속성 장치(180도 법칙·시선 매치·
  공간 앵커·포커스 상태 연속)가 공간을 봉합. #60 클로저
  테제의 실증 사례 — 프롬프트만 읽고 프레임 검증을 빼면
  놓치는 지점)

---

## 63. X @AI__TSUBAKI — 처음 구워본 꽁치 (Seedance 2.5 on Higgsfield, 30초)

**기본 정보**
- 출처: X @AI__TSUBAKI, 2026-09-30 게시. "Tried grilling sanma
  for the first time. Cast: Emma. Seedance 2.5 on @higgsfield".
  36 likes. 포스트에 프롬프트 없음
- 영상 실측: 30.04초, 2880x2160, 24fps, 721프레임.
  vxtwitter API 경유 mp4 직접 다운로드 성공
- 증거 기반: frame-observed (2fps 60장)

**관찰 — 타임라인**
- 0–7s: 일본식 부엌. 토끼귀 머리띠+세일러복 차림의 Emma가
  도마 위에서 종이에 싼 꽁치를 풂 (준비)
- ~14s: **인서트** — 잘린 유자(스다치) 매크로 클로즈업.
  얕은 심도, 그녀는 배경에 흐릿하게
- ~10s: **석쇠 POV** — 석쇠 너머로 그녀의 얼굴. 연기가 피어오르고
  아래에서 불빛. 카메라가 석쇠 자리에 있음
- ~20s: 합장 클로즈업 + 자막 "Itadakimasu."
- ~25s: 먹는 클로즈업 — 젓가락, 눈을 감고 음미하는 표정
- ~29s: 와이드 — 일본 가옥 exterior, 낮은 상에서 식사 중,
  마당의 화로 불빛. Higgsfield 로고 번인

**관찰 — 보여주지 않은 것**
- 정작 **구이 과정 자체는 한 번도 직접 안 나옴**: 석쇠에 생선을
  올리기, 뒤집기, 집게질, 접시에 담기 — 전부 생략. 불+연기+석쇠
  POV 한 컷으로 "굽고 있다"를 암시하고, "Itadakimasu" 한마디로
  구이→식사로 점프
- 맛은 음식이 아니라 **얼굴로** 보여줌 (눈 감고 음미). 음식
  클로즈업은 유자 인서트 1컷뿐

**기법 판독**
- T-24 다이제틱 카메라 시트의 변형: 카메라가 석쇠의 네이티브
  자리. 석쇠살이 전경 프레임이 됨
- T-04 가림막 와이프의 자연형: 연기가 전이를 덮음. 어려운 손
  동작(생선 뒤집기)은 연기와 컷 안에 숨김
- T-01 생략 컷의 교과서: "준비 → (한마디) → 식사". 사용자의
  테제 — "상태 A → 대사(의도) → 컷 → 상태 B" — 의 실전 사례.
  자막 "Itadakimasu."가 브릿지 대사 역할
- T-02 결과만 보여주기: 구이 과정 대신 먹는 얼굴(결과)만
- T-30 인서트 이코노미: 유자 매크로 1컷이 페이스와 "맛"의
  증거를 만듦
- 난이도 캐스팅 관점: "처음 구워본다"는 서사가 서툼을 정당화.
  불·연기·생선은 몸이 아는 난이도인데, 정작 어려운 동작은
  전부 생략하고 분위기(연기·불빛·표정)로 실감을 만듦

**관찰 vs 추론**
- 관찰: 타임라인, 보여주지 않은 것의 목록, 자막 문구, 로고 번인
  (프레임 기반)
- 추론: "구이 과정을 의도적으로 생략했다"는 연출 의도 판단 —
  결과물에서 읽은 것이므로 inference. 프롬프트가 없어서
  확인할 수 없음
- 미확인: 프롬프트 전문, Emma 캐릭터의 정체(시리즈물로 보임)

**코퍼스 기여**
- 1 (신규 — 석쇠 POV: T-24의 조리 장면 적용. "카메라를 도구가
  있던 자리에"의 확장), 2 (정합 — T-01 "대사 한마디 브릿지"의
  자막형 실전 사례. 사용자의 샷뱅크 테제와 직접 연결),
  3 (정합 — T-04 연기 가림막의 자연 발생 사례), 4 (재확인 —
  툴 워터마크 번인 #43번 규칙. Higgsfield 로고가 최종 샷에)

**규칙 카드 (붙여넣기용)**
```
[대사 한마디 브릿지 — Soft Guidance]
렌더할 수 없는 과정(조리·수리·이동)은 보여주지 말고
한마디로 건너뛴다. "준비 상태 → 'Itadakimasu' → 식사 중".
대사(또는 자막)가 의도를 선언하면 관객은 중간 과정을
스스로 메운다. 과정의 디테일을 묘사할수록 깨질 확률이
올라간다 — 말은 짧을수록 강하다.
```

---

## 64. X @AIwithWania — CHASE 짐 브이로그 (Seedance 2.5, 30초, 프롬프트 본문 공개)

**기본 정보**
- 출처: X @AIwithWania, 2026-09-30 게시. "No soft reps, no safe
  limits how much burn can you really handle? 🔥 Crafted with
  Seedance 2.5". 43 likes. **프롬프트 본문 전문 공개**
- 영상 실측: 30.1초, 848x478, 24fps, 721프레임.
  vxtwitter API 경유 mp4 직접 다운로드 성공
- 증거 기반: prompt-derived (전문) + frame-observed (2fps 60장).
  프롬프트의 8컷 스토리보드가 프레임에 실제로 반영됐는지 대조
- CHASE 현상 4번째 (#22·#40·#45에 이은 동일 캐릭터 짐 브이로그)

**관찰 — 프롬프트 구조**
- 섹션: CAMERA / LOOK / STYLE / REFERENCE IMAGE / OUTFIT /
  SETTING / STORYBOARD (8 cuts, 컷별 ~3–6s) / IMPORTANT
- CAMERA: "DV 16mm tape camcorder handheld feel. POV of CHASE
  holding the camera herself, occasionally propping it on the
  gym floor or mat for hands-free workout shots... Camcorder
  never appears on screen."
- LOOK: tape noise, bloomed highlights, flickering auto-exposure
  등 **불완전함을 스펙으로 명시**
- STORYBOARD: 컷마다 (시간·카메라 모드·샷 사이즈·동작·대사).
  컷7에 "Close-up insert of her hands gripping the mat" 명시
- IMPORTANT: "Keep every movement realistic... No repetitive
  shaking, hip thrusting... or sexualized posing." — 모션
  네거티브를 신체 부위 동사로 구체화

**관찰 — 프레임 대조**
- 컷1 (propped, 미디엄): 거울 벽 앞 워밍업. 물병 좌측 — 프롬프트대로
- 컷3 (low propped): 앉아서 스트레칭, 양말 신은 발이 렌즈 쪽으로
  — 전경 POV 증명 (T-24)
- 컷6 (handheld): 덤벨 컬, 카메라 보며 대화 — 벽시계 포착
- 컷8 (arm's-length selfie): 매트에 누워 셀카 피니시. 높은
  포니테일, 땀 — 프롬프트의 "tired but confident smile"대로
- 아이덴티티 8컷 전편 유지 (얼굴·포니테일·버건디 탑·차콜 레깅스)
- 거울 벽이 **가상 세컨드 카메라**로 작동: 고정 카메라 1대로
  정면+거울 속 측면/후면을 동시에 확보

**기법 판독**
- **신규 — 거울 커버리지**: 카메라를 안 움직이고도 거울로
  멀티앵글 확보. 고정 카메라의 한계를 공간 장치로 우회
- Propped camera grammar (#45) 재확인: 손이 필요하면 카메라를
  내려놓는다. 바닥/매트 거치가 hands-free의 물리적 해법
- Self-POV paradox lock (#40) 재확인: "Camcorder never appears
  on screen" 한 줄
- 컷별 대사 = 브이로그 장르 문법: 대사가 각 컷의 이유가 됨
- 연속성 토큰 (T-27): 벽시계, 물병이 8컷을 관통
- T-30 인서트: 컷7의 손 클로즈업이 페이스를 만듦
- 명시적 콘텐츠 가드: "never sexualized" + 금지 동작 리스트 —
  모션 네거티브로 작동 (정책 레이어가 아니라 연출 제어)

**관찰 vs 추론**
- 관찰: 프롬프트 전문, 8컷-프레임 대조, 거울·시계·물병의 반복
  등장 (프레임+텍스트 기반)
- 추론: "거울을 의도적으로 세컨드 카메라로 썼다"는 판단 —
  프롬프트에 거울의 용도가 명시돼 있지 않아 inference.
  단 결과물에서 기능하고 있음은 frame-observed
- 미확인: 레퍼런스 이미지의 원본, 립싱크 품질 (오디오 미청취)

**코퍼스 기여**
- 1 (신규 — 거울 커버리지. T-35로 DB 등록), 2 (정합 — propped
  camera grammar 3번째 확인 #45·#40), 3 (정합 — paradox lock
  3번째 확인), 4 (신규 — 프롬프트 섹션 아키텍처의 완성형 표본.
  P-01로 프롬프트 DB 등록), 5 (정합 — T-23 의도적 불완전함의
  프롬프트 명시 사례), 6 (정합 — T-27 연속성 토큰)

**규칙 카드 (붙여넣기용)**
```
[거울 커버리지 — Soft Guidance]
카메라를 움직일 수 없을 때(고정·거치 샷) 거울·유리·반사면을
화면에 넣어라. 고정 카메라 1대로 정면+반사 속 다른 각도를
동시에 확보할 수 있다. 거울은 "가상 세컨드 카메라"다.
단, 거울 속 모습도 아이덴티티가 유지돼야 하므로 캐릭터
락이 전제된다.
```

---

## 65. X @xazinga_com — 영춘권 vs 시스테마 (바 싸움, 30초, 프롬프트는 댓글)

**기본 정보**
- 출처: X @xazinga_com (verified, Korean), 2026-09-30 게시.
  "영춘권 vs 시스테마. 막판이 좀 이상하지만 그냥..
  20-24초 구간만 좀 다듬어서 사용하시길!" 10 likes, 2 replies.
  프롬프트는 댓글에 있음 (로그인 월 뒤 — 미확보)
- 영상 실측: 30.1초, 854x480, 24fps, 722프레임.
  vxtwitter API 경유 mp4 직접 다운로드 성공
- 증거 기반: frame-observed (2fps 60장) + prompt-derived.
  프롬프트 전문을 사용자가 직접 붙여넣음 (2026-09-30). 단,
  "@image2는 시스테마 고수를 정의한다" 문장의 주어(@image2
  토큰)가 붙여넣기 과정에서 소실된 것으로 보임 — "은 시스테마
  고수를 정의한다 — 얼굴"로만 남아 있음
- #48(마왕 vs 성기사 검투)의 동일 작가. 사용자 관찰: "요즘은
  이런 싸움 장면이 많이 올라와" — 액션 클러스터(#7·#10·#33·#38·
  #44·#46·#48·#49·#65)는 코퍼스 최대 장르군

**관찰 — 타임라인**
- 0–7s: 바. 흰 무복 여성(영춘권) vs 전술 조끼 남성(시스테마).
  남성의 주먹이 여성 얼굴 앞에 — 맞기 직전/막기 직전
- ~7s: 쟁반이 공중에서 회전 (던져진 소품). 모션 블러
- ~15s: 와이드 — 두 사람의 격투 스탠스. 적색 네온 바
- ~20s: 여성이 당구 큐를 장봉처럼 잡음 (영춘권 육점반자곤의
  즉흥 무기화)
- 20–24s: **문제 구간** — 큐를 쥔 손 클로즈업에서 손가락이
  뭉개짐 (hand–cue 접촉부 모핑). 여성 얼굴에 붉은 자국
  (혈흔인지 아티팩트인지 불명)
- 26–30s: 여성이 서 있고 남성이 쓰러짐. 부서진 바 의자 잔해.
  당구대 위에 칼이 꽂혀 있음 (출처 불명 — 던진 것인지
  아티팩트인지 프레임만으로 판단 불가)

**관찰 — 왜 나머지는 통하는가**
- 접촉 순간이 짧다: 주먹-얼굴, 손-큐의 접촉은 찰나. 길게
  붙어 있으면 깨지는데 (#62의 5대 파탄과 같은 축), 여기서는
  스침
- "전투는 원경으로" (#17 규칙): 대부분 미디엄–와이드.
  클로즈업은 대치(비접촉) 순간에만
- 소품이 강체: 쟁반·당구 큐는 단순한 막대/원반. 휘어지지
  않으니 모핑이 티가 덜 남. 날아가는 쟁반의 모션 블러는
  모핑의 카모플라주
- 반응 중심: 맞는 순간보다 스탠스·표정·잔해(결과)에 무게.
  T-02(결과만 보여주기)의 액션 버전

**관찰 — 작가의 셀프 진단이 곧 데이터**
- "막판이 좀 이상하지만 그냥.. 20-24초 구간만 좀 다듬어서
  사용하시길!" — 깨진 4초를 잘라내고 26초를 쓰는 **publish-
  and-trim** 실전. AI 영상은 원테이크가 아니라 편집용 소재라는
  작가의 작업관 (author-described)
- 문제 구간(20–24s)과 프레임 관찰(손-큐 모핑)이 일치 — 작가의
  진단이 정확했음. 즉 "어디가 깨졌는지 아는 눈"이 워크플로우의
  일부

**프롬프트 대조 (prompt-derived)**
- 아키텍처: [한 줄 요약] → [글로벌 설정] → [타임스탬프
  스토리보드 10비트×3초] → [글로벌 마무리]. #48(동일 작가)과
  동일한 10비트×3초 정형 — 작가의 시리즈 문법. #64의 섹션
  아키텍처(P-01)와 독립 수렴
- 캐릭터 락: @image1=하린(얼굴·헤어·흰 쿵푸 수련복·허리끈),
  @image2=시스테마 고수(얼굴). "캐릭터 시트의 흰 배경은
  사용하지 않는다" — 배경 분리 지시
- 상처 규칙 (상태 락): 칼끝이 하린 얼굴에 정확히 세 개의 얕은
  상처 — 뺨(0-3초), 턱선(9-12초), 이마 옆(18-21초). 핏줄기·
  핏방울, 위치·개수 고정, 증식·소멸·이동 금지. frame_048(24초)의
  관자놀이 핏줄기는 18-21초 세 번째 상처와 정합. #48의
  damage persistence 계승
- 양방향 논스톱: 어느 쪽도 일방적으로 몰리지 않음. "한 합이
  끝나기 전에 다음 합이 물린다" — 시차를 두고 겹치는 연쇄
- 아슬아슬함의 원칙: 단검의 모든 궤적은 몇 밀리 차이로 스치거나
  마지막 순간에 흘려짐 — 여유 있는 회피 금지. 접촉을 짧게
  만드는 물리 문법 (T-36 신규)
- **칼의 정체 해결**: 24-27초 비트에 "단검이 손에서 튕겨 날아가
  당구대 펠트에 꽂힌다" — frame_058의 당구대 위 칼은 아티팩트가
  아니라 스크립트. "미확인" 플래그 해소 (prompt-derived)
- 소품 규칙: 장면에 존재하는 것만 사용, 허공 생성 금지. 단검은
  한 자루뿐. 부서진 것은 복원·소멸 없이 남는다
- 전신 발력: "팔만 뻗기 금지" (P-24 계열 모션 네거티브).
  하린의 이동은 "헛점프 금지, 바 카운터·당구대 위 슬라이드
  허용" — 허용/금지의 경계 명시
- 카메라: 정면 응시 샷 금지(측면·3/4·오버숄더·후면만), 인물
  단독 프레임 회피, 구간마다 카메라 위치 변경, 삼분할
  오프센터+리드룸+좌/우 교차. 크래시 줌은 임팩트·칼날 궤적에만
- 오디오: 음악 없음, 현장음만. 비트마다 <사운드 리스트> 지정
- 깨진 21-24초 = 프롬프트의 "최고조" 비트: "단검 최고속 연격이
  전부 몇 밀리로 스치고... 칼날이 단봉을 쳐 날리고 하린은
  맨손이 된다". 최고속+손-단봉 접촉의 타이트 측면 — 가장
  밀도 높은 비트에서 깨짐. 반면 15-18초 "손목과 팔꿈치가
  얽히고 풀리는" 트래핑 공방(난이도 최고점)은 오버숄더(덜
  타이트)로 상대적 통과 — 난이도와 카메라 거리의 트레이드오프
  (inference)

**관찰 vs 추론 (수정)**
- 관찰: 타임라인, 문제 구간의 손 모핑, 작가의 코멘트 원문
- 프롬프트로 해소: 당구대 위 칼 = 스크립트 (24-27초 비트)
- 추론: "모션 블러가 모핑을 가린다", "난이도×카메라 거리
  트레이드오프" — 그럴듯하나 대조 실험 없음. inference로 분리
- 미확인: 오디오 실제 출력 (현장음 리스트가 렌더됐는지)

**코퍼스 기여**
- 1 (신규 — publish-and-trim: 깨진 비트는 잘라내고 올린다.
  AI 영상을 편집 소재로 취급하는 작업관), 2 (정합 — P-09
  boundary lock 실패의 실전 표본. 손-큐 접촉부가 정확히 그
  지점), 3 (정합 — #17 "전투는 원경으로" 규칙), 4 (신규 —
  모션 블러=모핑 카모플라주 가설. ★ 1개, 검증 필요),
  5 (정합 — T-02 결과 중심의 액션 버전), 6 (신규 — P-29
  상태 락: 상처를 타임스탬프·위치 고정으로 지정하는
  damage persistence), 7 (신규 — T-36 아슬아슬함의 원칙:
  칼날은 몇 밀리 차이로 스친다), 8 (정합 — P-01 섹션
  아키텍처와 #64의 독립 수렴, 동일 작가의 시리즈 문법
  #48→#65)

**규칙 카드 (붙여넣기용)**
```
[깨진 비트는 잘라낸다 — Soft Guidance]
AI 영상은 원테이크가 아니라 편집용 소재다. 30초 중 4초가
깨졌으면 그 4초를 잘라내고 26초를 올린다. 통째로 버리지
말고 쓸 수 있는 구간만 쓴다. "어디가 깨졌는지 아는 눈"이
프롬프트 실력만큼 중요하다 — 작가의 셀프 트림이 곧 QC다.
```

---

---

## 66. X @john_my07 — 서울 골목 홈비디오 (30초, 롱테이크형 연속성 파탄)

**기본 정보**
- 출처: X @john_my07 (Johnn), 2026-09-30 게시.
  "Seedance 2.5 on @wavespeed_ai" + 프롬프트 전문 공개 (본문).
  44 likes, 32 replies, 3 retweets
- 영상 실측: 30.0초, 1280x720, 24fps, 721프레임.
  vxtwitter API 경유 mp4 직접 다운로드 성공
- 증거 기반: frame-observed (2fps 60장) + prompt-derived
  (프롬프트 전문 확보)
- 사용자 가설: "처음 볼 때는 그럴듯하지만 보다보면 안맞는게
  보여. 돈을 줄 때 왜 돈이 손에 있느냐, 비닐봉지는 어디서
  났느냐. 전부 롱테이크처럼 보이느라 헛점이 생긴거잖아"

**관찰 — 프롬프트의 구조**
- 6개 씬: 집 나서기(장바구니) → 빵집(동전 결제) → 친구와
  포옹 → 과일가게(복숭아 구매→가방에) → 나무 아래서
  페이스트리 먹기 → 엔딩 "Bye bye!" 웨이브
- CAMERA STYLE: "early-2000s consumer MiniDV home-video...
  made by a friend or family member" — 연속 촬영 홈비디오
- 오디오: 현장음만, 음악·자막·내레이션 금지

**관찰 — 연속성 파탄 인벤토리 (전부 frame-observed)**
1. **가방 순간이동**: 시작(frame_003, 왼손에 흰 비닐봉지) →
   빵집·친구·과일가게·나무 아래 전 구간 소실 →
   엔딩(frame_058)에서 왼손에 **복귀**. 프롬프트의 엔딩
   문장("carrying her bag and peach")이 가방을 다시 소환함
2. **돈의 물질화**: 빵집 결제(frame_020)에서 손이 이미 동전을
   든 채로 뻗음. 지갑·가방에서 꺼내는 장면 없음. 프롬프트는
   "pays with coins"만 쓰고 동전의 출처를 안 적음
3. **페이스트리 소실**: 빵집에서 고르는 장면까지만 있고 이후
   영원히 등장 안 함
4. **복숭아 순간이동**: 과일가게에서 고름(frame_034, 결제·
   봉투에 넣기 없음) → 나무 아래에서 갑자기 먹고 있음
   (frame_040). 프롬프트의 "pays the vendor, places it inside
   her shopping bag"는 렌더 안 됨
5. **씬-5 위반**: 프롬프트 "eating her pastry" → 실제 렌더는
   복숭아를 먹음. 빵집 씬의 산출물(페이스트리)과 과일가게 씬의
   산출물(복숭아)이 뒤바뀜
6. **가방 타입 불일치**: 프롬프트 "small reusable shopping
   bag" → 렌더는 흰 비닐봉지

**관찰 — 가설 검증 (사용자 가설 지지)**
- 렌더는 6개 씬을 컷 없이 하나의 연속 팔로우로 이어붙임 —
  가짜 롱테이크. 모션 연속성(걷기·카메라 팔로우)은 유지되지만
  **소품 상태 연속성은 스티치 지점에서 carryover 안 됨**
- 각 비트는 텍스트에서 새로 생성되므로, 그 비트에 언급된
  소품만 존재함. 엔딩 비트에 "bag"이 언급되자 가방이 부활
- 프롬프트 자체의 내적 모순: 씬 구조(상태 전이 서사) +
  카메라 스타일(롱테이크 홈비디오)을 동시 요구. 모델은
  모순을 "모션은 연속, 상태는 드롭"으로 해소
- 처음엔 통하는 이유: MiniDV 미학(T-23 의도적 불완전함 —
  흔들림·AF 헌팅·소프트 디테일)이 "실제 촬영"을 팔고,
  첫 시청은 모션·얼굴을 좇지 소품을 추적하지 않음. 다시
  보면 시선이 소품으로 이동하며 구멍이 보임 — 사용자의
  "처음 볼 때는 그럴듯하지만 보다보면"과 정확히 일치

**관찰 vs 추론**
- 관찰: 파탄 인벤토리 6건, 가짜 롱테이크 구조, 프롬프트 원문
- 추론: "비트별 새로 생성이라 언급된 소품만 존재"는 렌더
  메커니즘에 대한 추론 — 프레임 패턴과는 정합하나 모델
  내부는 미확인. inference로 분리
- 미확인: 오디오("Bye bye!" 발화 여부), 32개 리플라이의 내용
  (구멍 논쟁인지 — 로그인 월 뒤)

**코퍼스 기여**
- 1 (신규 — T-37: 상태 전이는 컷에 숨긴다. 상태가 바뀌는
  이야기에 롱테이크는 틀린 형식), 2 (신규 — P-30 소품 상태
  원장: 씬별 소품의 위치·소지자·내용물을 표로 고정),
  3 (정합 — T-23 의도적 불완전함이 역설적으로 구멍을
  나중에 더 도드라지게 함), 4 (정합 — T-27 연속성 토큰의
  실패 사례: 가방이 토큰이었으나 모델이 드롭), 5 (신규 —
  프롬프트의 내적 모순(씬 구조×롱테이크 카메라)이 렌더
  파탄의 원인. P-21 실패 출처 명시 계열)

**규칙 카드 (붙여넣기용)**
```
[상태 전이는 컷에 숨긴다 — Hard Lock]
상태가 바뀌는 이야기에 롱테이크는 틀린 형식이다. 산다→
봉지에 넣는다→먹는다, 이 전이들은 컷이 있어야 숨을 구멍이
생긴다. 가짜 롱테이크에서는 모션만 이어지고 소품 상태는
스티치 지점에서 드롭된다 — 돈은 손에 물질화되고 가방은
순간이동한다. 롱테이크를 고집하면 모든 소품에 상태 락을
걸어라: "흰 비닐봉지는 전 구간 왼손. 포옹할 땐 왼 손목에.
동전은 숄더백 앞주머니에서 꺼낸다."
```

---

---

## 67. X @Just_sharon7 — 식당 MiniDV 15초 (컷 문법의 정석)

**기본 정보**
- 출처: X @Just_sharon7 (Sharon Riley), 2026-09-30 게시.
  "This AI video made me question what 'AI-looking' even means
  anymore." Seedance 2.5 on @TapNow_AI + 프롬프트 전문 공개.
  357 likes, 92 replies
- 영상 실측: 15.1초, 1280x720, 24fps, 362프레임.
  vxtwitter API 경유 mp4 직접 다운로드 성공
- 증거 기반: frame-observed (3fps 45장) + prompt-derived

**관찰 — 컷 문법**
- 15초를 5비트×3초로 분할. 하드컷은 단 1개:
  "00:06–00:09 — INSIDE: Natural handheld cut as she pushes
  open the glass restaurant door." 문이 컷의 핑계 (동기 있는
  가림막). 프레임 대조: sframe_016(메뉴판 앞) → sframe_022
  (실내) — 외→내 전이가 문 뒤에 숨음
- 음식 등장(12-15초)은 컷 없이 처리 — "steaming bowl of
  kimchi-jjigae is placed in front of her". 상태 전이를
  인과 제시(누가 놓는다)로 해결. 컷이 필요 없는 경우의
  정석
- 대사 브릿지 매 비트 (T-01/P-28): "아… 배고프다" →
  "뭐 먹을래?"/"잠깐만…" → "어서 오세요"/"안녕하세요" →
  "야…"/"안 떨어졌잖아" → "와… 맛있겠다"

**관찰 — #66의 포지티브 컨트롤**
- 같은 모델(Seedance 2.5)+같은 장르(서울 MiniDV 홈비디오)+
  같은 플랫폼. 차이는 컷+원장. 여기의 가방은 "어깨에서
  미끄러지자 보지도 않고 추켜올린다" — 소품을 손으로
  능동 관리 (#66의 순간이동과 정반대)
- 09-12초 "작은 사고" 비트: 젓가락 통이 기울자 양손으로
  낚아챔. sframe_034에서 눈 커진 표정 그대로 렌더.
  "extremely ordinary human moment" — 스펙터클이 아니라
  극도로 평범한 순간의 유머. 표정 아크 지정
  (sleepy→hunger→concentration→surprise→embarrassment→
  laughter→excitement)
- 메뉴판 한글은 AI 난독증 (frame-observed) — 배경 텍스트는
  여전히 깨지지만 세트 소품이라 서사에 영향 없음
- 인기도는 분해된 신호로만: 357 likes / 92 replies (#66의
  44/32 대비). 인과 증거 아님

**관찰 vs 추론**
- 관찰: 컷 1개의 위치와 동기, 가방 관리 묘사, 사고 비트 렌더,
  메뉴판 난독증
- 미확인: 오디오(대사 렌더 여부)

**코퍼스 기여**
- 1 (정합 — T-37 v2의 하드컷 표본: 문 핑계 컷), 2 (정합 —
  P-30의 포지티브 케이스: 가방을 마이크로 액션으로 관리),
  3 (정합 — T-01/P-28 대사 브릿지의 5비트 연속 사용),
  4 (신규 — 상태 전이의 3종 처리법 중 "인과 제시"형:
  음식은 누가 놓는다. T-37 v2에 편입)

**규칙 카드 (붙여넣기용)**
```
[컷에는 핑계가 필요하다 — Soft Guidance]
컷을 자를 땐 문·가림막·몸이 핑계를 댄다. "유리문을 밀며
자연스럽게 컷" — 외→내 전이는 문 뒤에 숨는다. 핑계 없는
컷은 어색하고, 컷 없는 상태 전이는 파탄난다.
```

```yaml
knowledge_update:
  existing_T: [T-37, T-01, T-04]
  existing_P: [P-30, P-28]
  evidence_strength: HIGH
  cross_model_generality: HIGH
  promotion_target: DIRECTOR_RECIPE
  action: scope_existing
  notes: "#66 파탄 사례의 포지티브 컨트롤. T-37을 하드컷+
    인과 제시로 확장. 동기 있는 컷은 고전 영화문법이라
    사례 1건으로도 범용성 높음."
```

---

## 68. X @Soranlan — 데스크탑 녹화풍 3단 전환 (중국어 프롬프트)

**기본 정보**
- 출처: X @Soranlan (Soran), 2026-09-30 게시. "还有更狠的"
  (더 매운 거 왔다) + 중국어 프롬프트 전문 공개 (번역済).
  37 likes, 8 replies
- 영상 실측: 20.1초, 1056x608, 24fps, 482프레임.
  vxtwitter API 경유 mp4 직접 다운로드 성공
- 증거 기반: frame-observed (3fps 60장) + prompt-derived
  (중국어→한국어 번역)

**관찰 — 샷 문법 (T-37의 일반화)**
- 20초에 단 3개 샷 세그먼트. **하드컷 금지**
  ("禁止生硬硬切") — 모든 전환은 인물이 카메라 앞을
  스치며 몸으로 화면을 가리는 와이프 ("无痕转场",
  흔적 없는 전환)
- 갈아입기는 가림막 뒤에서: "任何换装必须在转场遮挡完成后、
  人物不可见的阶段完成" (의상 교체는 가림막 전환 완료 후
  인물이 안 보이는 단계에서만). T-10(위상 분리)+T-04
  (가림막 와이프)의 융합 표본 — 와이프는 변장한 컷
- 프레임 대조: rframe_015/017(샷1, 소파+데스크탑 UI) →
  rframe_037(샷3, 의상 교체됨). UI 프레임(작업표시줄·
  아이콘·자막 영역·파형)은 전 구간 유지 — 연속성 앵커

**관찰 — 프롬프트 기법**
- S1/S2 표기: 화면 여성=S1 고정, 화면 밖 남성 목소리=S2
  (절대 등장 금지). "S2说话时S1必须闭嘴" — 립싱크 규율
  (P-16의 음성 확장)
- 자막 UI 스펙: 발음에 맞춰逐字 타이핑, 선행 표시 금지,
  문장 끝 0.3초 유지 후 페이드. 자막이 픽션의 일부
  (화면 녹화 컨셉)
- 연속성 하드 제약 11항: 같은 얼굴·헤어·목소리·소파·
  쿠션·방·UI. 네거티브도 구체적 ("丝袜、鞋子、裙摆在行走中
  随机变化" 금지 — P-24 계열)
- 컨셉: "컴퓨터 전체화면 동적 데스크탑 녹화 시뮬레이션" —
  영상 자체가 살아있는 벽지. 기록 장치가 픽션 안에 있음
  (T-24 다이제틱 카메라의 UI 버전)

**관찰 vs 추론**
- 관찰: 3세그먼트 구조, UI 앵커 유지, 의상 교체 렌더,
  자막逐字 렌더 (rframe_037에서 타이핑 중 포착)
- 추론: 전환 순간의 정확한 가림막 메커니즘은 프레임
  사이(3fps 샘플링)에 있어 직접 미포착. inference로 분리
- 미확인: 오디오(S1/S2 음성 분리·덕킹 여부)

**코퍼스 기여**
- 1 (신규 — T-37 v2의 근거: 하드컷 금지 선언 하에서도
  상태 전이는 화면 밖에서 일어난다. 와이프=변장한 컷),
  2 (정합 — T-10+T-04 융합), 3 (정합 — P-16 음성 확장),
  4 (관찰 — 다이제틱 UI 컨테이너: 자막·파형·작업표시줄이
  픽션의 일부. T-24 계열 변형으로 기록, 신규 T 아님)

**규칙 카드 (붙여넣기용)**
```
[갈아입기는 화면 밖에서 — Hard Lock]
의상 교체는 몸이 화면을 가린 동안, 인물이 안 보이는
단계에서만 일어난다. "无痕转场" — 가림막 와이프는
변장한 컷이다. 하드컷을 금지해도 법칙은 안 바뀐다:
상태 전이는 화면 밖에서.
```

```yaml
knowledge_update:
  existing_T: [T-37, T-10, T-04]
  existing_P: [P-16]
  evidence_strength: MEDIUM
  cross_model_generality: HIGH
  promotion_target: DIRECTOR_RECIPE
  action: scope_existing
  notes: "하드컷 금지 선언 하에서도 상태 전이는 화면 밖에서.
    와이프=변장한 컷으로 T-37 일반화. S1/S2 음성 규율은
    P-16 확장. 전환 메커니즘은 3fps 샘플링 사이 구간이라
    직접 미포착 (inference로 분리)."
```

---

## 69. X @CharaspowerAI — 심리 호러 트레일러 30초 (불가능성 인벤토리)

**기본 정보**
- 출처: X @CharaspowerAI (Pierrick Chevallier | IA), 2026-09-30 게시.
  "AI horror doesn't need monsters to be terrifying. I wanted to test
  something much harder: 30 seconds of pure psychological tension built
  with acting, dialogue, reflections and tiny details that feel… wrong."
  44 likes, 8 replies. 프롬프트 전문은 사용자가 직접 붙여넣음
- 생성 모델: 미공개 (포스트에 모델명 없음)
- 영상 실측: 30.2초, 1280x720, ~24fps, 723프레임.
  vxtwitter API 경유 mp4 직접 다운로드 성공
- 증거 기반: frame-observed (2fps 60장) + prompt-derived

**프로토콜 판정 (기존 T/P 우선)**
- T-35 (거울 커버리지): 거울이 나오지만 용법이 다름. #64는
  커버리지용 "가상 세컨드 카메라", 여기는 불가능의 무대
  (반사상이 기하학을 어김). → scope_existing (용법 2 추가)
- T-37 v2: 각 비트가 불가능성을 품고 비트 경계에서 리셋
  ("The elevator opens. Everything is normal again").
  불가능한 상태가 비트 밖으로 새지 않음 → strengthen
- T-01: 대사가 비트를 뒤집는다 ("You already asked me that
  yesterday") → strengthen
- P-16 (캐릭터 락): "stable character continuity, realistic
  reflections" 명시. 거울 프레임에서 아이덴티티 유지
  (cframe_025) → strengthen
- 신규 T 조건 검토: "몬스터·고어·VFX 없이 공포"는 기존 T로
  설명 불가. #25의 "불가능성의 카탈로그"(패턴 8, T 미발급)와
  독립 수렴 2건째. 별도 제작 문제 해결 + 관찰 근거 +
  재사용 형태("impossibility inventory") 충족 → new_candidate

**관찰 — 불가능성 6종 (프롬프트 명세)**
1. 엘리베이터 거울: 반사상이 카메라를 직접 보는데 실제 얼굴은
   외면. cframe_025에서 거울 디프티크 렌더 확인 (frame-observed).
   정확한 시선 기하학은 2fps 샘플링상 미확정 — inference로 분리
2. 유리 표면에 비치는 낯선 사람 형상의 반사 (prompt-derived)
3. 가족사진에 모르는 사람이 한 명 추가 (prompt-derived)
4. 잠긴 서랍 안에서 울리는 전화 — 열어보면 안에 없음
   (prompt-derived)
5. 대치: "Tell me I'm imagining this." / "You already asked me
   that yesterday." cframe_045에서 클로즈업 렌더 확인
6. 파이널: 복도에서 그녀 자신의 목소리 "Don't go back to sleep."
   욕실 거울에 비친 그녀는 아직 침대에서 자고 있음.
   cframe_056에서 침실 스테이징 확인. "Hard cut to black"

**관찰 — 연출 문법**
- 6비트×5초, 비트마다 다른 카메라 언어 (돌리인→핸드헬드
  클로즈업→고정 불편한 와이드→급속 몽타주→타이트 클로즈업→
  파이널 리빌). 트레일러는 비트 단위 — #60의 비트 편집과 동형
- 네거티브가 곧 컨셉: "no supernatural spectacle, no gore...
  no visible threat, no attack, no gore, no disturbing body
  imagery, no readable text". 빼기로 공포를 만듦
- 작가의 난이도 선언: "I wanted to test something much
  harder" — 몬스터보다 심리 텐션이 더 어렵다는 창작적 판단
  (author-described). 사용자의 "어려움으로 달려가기" 전략과
  정합

**Capability evidence (모델 미공개)**
- model: undisclosed (CharaspowerAI post, 2026-09-30) /
  version: n/a / evidence date: 2026-09-30 /
  task: impossible mirror reflection (reflection looks at
  camera while real face turned away) /
  observed: success (cframe_025 — identity stable in mirror,
  disobedient composition rendered) / confidence: MEDIUM
  (2fps sampling; exact gaze geometry unverified)

**코퍼스 기여**
- 1 (신규 — T-38 불가능성 인벤토리: #25와 독립 2건째),
  2 (scope — T-35에 "불가능의 무대" 용법 추가),
  3 (strengthen — T-37 v2 비트 경계 리셋, T-01 대사 뒤집기,
  P-16 거울 아이덴티티)

**규칙 카드 (붙여넣기용)**
```
[불가능성은 명세다 — Hard Lock]
"이상한 일이 일어난다"고 쓰지 말고 "거울 속 그녀는
카메라를 본다"고 써라. AI는 추상을 못 그리고 명세를
그린다. 불가능성마다 자기 비트를 주고 담담하게 렌더 —
강조는 관객의 뇌가 한다.
```

```yaml
knowledge_update:
  existing_T: [T-35, T-37, T-01]
  existing_P: [P-16]
  evidence_strength: HIGH
  cross_model_generality: HIGH
  promotion_target: DIRECTOR_RECIPE
  action: new_candidate
  notes: "T-38 불가능성 인벤토리 신규 후보. #25(불가능성의
    카탈로그)와 독립 수렴 2건째. 기존 T로 설명 불가한 별도
    제작 문제(무몬스터·무고어 호러) 해결. 담담한 불가능
    디테일은 고전 호러 문법이라 범용성 높음."
```

---

## 70. X @CharaspowerAI — 스쿠터 탄 고양이 로드레이지 (파운드푸티지 30초)

**기본 정보**
- 출처: X @CharaspowerAI (Pierrick Chevallier | IA), 2026-09-30 게시.
  "Want to make the kind of AI video people would swear was randomly
  filmed on the street? ... Seedance 2.5 is ridiculously fun for this
  kind of viral found-footage concept." 183 likes, 12 replies (#69의
  44 likes의 4배 — 같은 작가의 두 장르, 반응은 코미디가 압승)
- 생성: Seedance 2.5 (author-described). 프롬프트 전문은 포스트
  본문에 공개 (vxtwitter API로 전문 확보)
- 영상 실측: 30.1초, 1280x720, ~24fps, 721프레임.
  프롬프트는 "20 seconds"라 명시했으나 실제 30.1초 —
  prompt-derived 20s vs frame-observed 30.1s 불일치
- 증거 기반: frame-observed (2fps 60장) + prompt-derived

**프로토콜 판정 (기존 T/P 우선)**
- T-23 (의도적 불완전함): "Raw handheld phone camera, strong natural
  shake, accidental reframing, bad digital zoom, autofocus hunting,
  compression artifacts, wind on microphone... Absolutely no cinematic
  stabilization" — 코퍼스 사상 가장 완전한 T-23 스펙 → strengthen
- T-25 (카메라=존재): 보이지 않는 행인이 영어로 흥분하며 중계.
  카메라는 관찰자가 아니라 등장인물 → strengthen
- T-18 (인과적 카메라 반응): "Camera shakes from laughter and nearly
  points at the pavement" — 웃음이 흔들림의 원인. T-18의 금기
  "원인 없는 흔들림"을 정면으로 지킴 → strengthen
- T-01: 필머의 대사가 펀치라인 버튼 ("BRO HAS ROAD RAGE!",
  "HE'S GOT PLACES TO BE!") → strengthen
- P-16: "one cat only" 카운트 락 → strengthen
- 신규 T 검토: "무표정 피사체 + 흥분한 리액터" 구조는
  T-25+T-18+T-01의 조합으로 완전 설명됨. 새 제작 문제 없음 →
  strengthen_existing (신규 발급 없음)

**관찰 — 코미디 엔진**
- 고양이는 아무것도 안 함: "stares straight ahead like an exhausted
  commuter", "dead-serious sideways glance". 웃긴 건 전부 필머의
  리액션. 데드팬 피사체 + 과잉 리액터의 대비가 엔진
- 5비트×4s 에스컬레이션: 발견→공개→빨간불 정지→클랙슨 � 빵→
  페이오프. dframe_020에서 빨간불 앞 정지+옆 차 운전자의
  어이없음 표정 확인 (frame-observed)
- 엔딩 "Hard cut." — #69의 "Hard cut to black"과 같은 작가의
  습관 (author-described 스타일 지문)

**관찰 — 스펙 미준수 2건 (장르가 흡수)**
1. 차량: 프롬프트가 "MOTORIZED CITY SCOOTER... NOT a kick
   scooter... seat, engine, handlebars and footboard"를 3번
   강조했으나, 렌더는 킥보드형에 가까움 (dframe_020 — 시트·
   엔진 미확인). 관객은 스펙을 검사하지 않음 — 코미디가 흡수
2. 길이: 20초 스펙 → 30.1초 렌더. 비트 타이밍(0-4s...16-20s)이
   실제와 어긋남. #25의 "beat displacement"와 동형

**Capability evidence**
- model: Seedance 2.5 (author-described) / version: 2.5 /
  evidence date: 2026-09-30 / task: vehicle-type compliance
  (motor scooter vs kick scooter, explicit triple-spec) /
  observed: partial failure (kick-scooter-like render) /
  confidence: MEDIUM

**코퍼스 기여**
- 3 (strengthen — T-23/T-25/T-18/T-01/P-16 전부 기존 항목 강화.
  신규 T 없음. 프로토콜의 "정제 우선"이 의도대로 작동한 케이스)

**규칙 카드 (붙여넣기용)**
```
[못 찍은 척을 명세하라 — Soft Guidance]
"bad digital zoom, autofocus hunting, wind on mic" —
아마추어스러움은 우연이 아니라 스펙이다. 불완전함도
설계여야 티가 안 난다. 흔들림마다 원인을 붙여라
(발견→낚아챔, 펀치라인→웃음).
```

```yaml
knowledge_update:
  existing_T: [T-23, T-25, T-18, T-01]
  existing_P: [P-16]
  evidence_strength: HIGH
  cross_model_generality: HIGH
  promotion_target: DIRECTOR_RECIPE
  action: strengthen_existing
  notes: "신규 T 없음 — T-25+T-18+T-01 조합으로 완전 설명.
    T-23은 코퍼스 최완전 스펙으로 강화. 스펙 미준수(킥보드형·
    30초)는 코미디 장르가 흡수. 파운드푸티지 문법은 고전이라
    범용성 높음."
```

---

## 71. X @Promptwhat — 괴수 액션 제작 과정 공유 (246만뷰, 텍스트 가이드)

**기본 정보**
- 출처: X @Promptwhat (Prompt_what), 2026-10-01 게시. 한국어
  제작 과정 공유글. "246만뷰 영상 제작과정을 전부 공유합니다."
  133 likes, 10 replies. 프롬프트 전문은 댓글(로그인 월)에 있어
  미확보 — 포스트 본문만 prompt-derived
- 영상 실측: 59.1초, 1920x822, 59프레임(1fps 추출).
  vxtwitter API 경유 mp4 직접 다운로드 성공
- 증거 기반: frame-observed (영상) + author-described (제작법)
- 참고: 조회수 246만은 인기도 신호일 뿐 품질 증거 아님 (standing rule)

**프로토콜 판정 (기존 T/P 우선)**
- 스케일 명세 ("방파제 네 개 길이", "등대가 허벅지에 닿는
  몸집"): 기존 P에 스케일 서술 항목 없음. 추상 형용사→모델이
  몸집을 줄이는 구체적 실패 모드 관찰됨 → new_candidate (P-31)
- 2클립 이어붙이기 ("뒤편 프롬프트에 앞편이 끝난 상태를 그대로
  적어두면"): P-30 금기 "상태는 씬마다 다시 선언해야
  carryover됨"의 클립 단위 확장. 같은 방파제·젖은 머리·의상·
  적은 화면 오른쪽 → strengthen (P-30)
- 스케일 후킹 (첫 프레임부터 스케일로 때리기, 2초 만에 설명
  없이): T-22(셋업 없이 한가운데서 열기)의 메커니즘 변형 →
  scope_existing (T-22)
- 1~2초 인과 교대 (손짓 컷 ↔ 물 반응 컷): 고전 액션 문법.
  T-33(전이 어휘)과 층위가 다르고 신규 번호가 필요할 정도의
  별도 문제는 아님 → evidence_only
- Higgsfield Soul Cinema 추천: 도구 추천은 영구 규칙 불가 →
  model_capability_only

**관찰 — 스케일 문법 (frame-observed + author-described)**
- kframe_002: 괴수가 창문 달린 건물만 한 바위를 들고 있음.
  건물=기준물 — 첫 프레임에서 스케일 확정, 설명 없음
- kframe_045: 방파제 위 작은 인물(지팡이 든 로브) vs 양옆으로
  갈라진 바닷물 vs 먼 곳의 괴수. 인물·방파제·괴수의 3단
  대비가 스케일을 말함
- 작가의 실패 모드 관찰: "멀리", "크게"라고만 적으면 "거리는
  좁히고 몸집은 작아지는 사고가 발생" — 추상 형용사에 대한
  모델의 체계적 반응. 프롬프트의 1/3을 스케일 설명에 할당

**관찰 — 도구 불일치 (기록용)**
- 영상에 "spellcraft.ai" 워터마크 번인 (frame-observed)
- 작가는 "실사감은 배경에서 먼저 결정... 가장 애용하는 툴은
  힉스필드 소울 시네마" (author-described)
- 둘은 다른 단계/도구일 수 있음. 단정 불가 → inference로 분리.
  워터마크는 네거티브로 못 막은 툴 레이어 유출 (#25와 동형)

**Capability evidence**
- tool: Higgsfield Soul Cinema (author-described, 2026-10-01) /
  task: photorealistic backgrounds / observed: author claims
  "어느 툴보다 실제로 찍은 사진처럼" / confidence: LOW
  (author claim, no A/B)
- tool: Spellcraft AI (frame-observed watermark) /
  task: kaiju action render / observed: success (59s coherent
  action) / confidence: MEDIUM

**코퍼스 기여**
- 1 (신규 — P-31 스케일 기준물 명세),
  3 (strengthen — P-30 클립 단위 상태 인계),
  2 (scope — T-22 스케일 후킹 변형),
  4 (model_capability_only — Higgsfield/Spellcraft)

**규칙 카드 (붙여넣기용)**
```
[크기는 눈에 보이는 것으로 — Hard Lock]
"크게", "멀리"라고 쓰지 말고 "방파제 네 개 길이",
"등대가 허벅지에 닿는 몸집"이라고 써라. 추상 형용사는
모델이 거리를 좁히고 몸집을 줄이는 사고를 낸다.
스케일 설명에 프롬프트의 3분의 1을 써라.
```

```yaml
knowledge_update:
  existing_T: [T-22]
  existing_P: [P-30]
  evidence_strength: MEDIUM
  cross_model_generality: HIGH
  promotion_target: PROMPT_RECIPE
  action: new_candidate
  notes: "P-31 스케일 기준물 명세 신규 후보. 추상 형용사→축소
    실패 모드가 관찰된 별도 제작 문제. 기준물 대비는 고전
    영화 문법(인물·건물 대비)이라 범용성 높음. 2클립 인계는
    P-30 강화로 처리."
```

---

## 72. X @baike888 — 《你过来》 남친 시점 원테이크 (Doubao)

**기본 정보**
- 출처: X @baike888 (马化晨), 2026-10-01 게시. 53 likes, 12 replies
- 포스트 전문 (중국어, 번역): "白嫖豆包第五发 (공짜 豆包로 뽑기
  다섯 번째). 쓸데없는 말 말고 프롬프트: 제목 《你过来》(이리 와).
  15초, 9:16 세로, 형식: 남친 시점(男友视角), 원테이크(一镜到底).
  장면: 참조 이미지."
- 영상 실측: 15.1초, 720x1280 세로. vxtwitter API 경유 다운로드
- 모델: Doubao (author-described, "白嫖豆包" = 무료 티어)
- 증거 기반: prompt-derived (포스트 본문) + frame-observed (영상)

**프로토콜 판정 (기존 T/P 우선)**
- 남친 시점 = 카메라가 등장인물: T-25(카메라=존재)의 신체형 변형.
  #42는 보이지 않는 존재였고, 여기는 촬영자의 손이 프레임에
  들어오고 상대가 그 손을 잡는다. 같은 장치, 새 증거·새 형태 →
  strengthen (T-25)
- 렌즈 직시: T-14 시선 설계의 "인물 → 렌즈" 할당 케이스 →
  cross-ref, 별도 액션 없음
- 원테이크(一镜到底): 컷을 쓰지 않는 선택. T-37의 역 — 컷의
  핑계가 필요 없는 구조. 친밀 장르의 문법으로 관찰만 기록
- 신규 T/P 없음

**관찰 — 친밀감의 엔진 (frame-observed)**
- kframe_002: 남자의 손이 프레임 오른쪽으로 들어오고, 여자가
  그 손을 잡음. 카메라는 더 이상 시점이 아니라 "잡히는 몸"
- kframe_008: 여자가 두 손으로 남자의 손을 감싸고 렌즈를
  똑바로 봄. 렌즈 응시 + 신체 접촉의 결합
- kframe_013: 얼굴이 닿을 듯한 거리. 남자 얼굴 일부가 프레임
  왼쪽에 들어옴 — 촬영자도 화면의 일부가 됨
- 구조: 접촉(손) → 응시(렌즈) → 접근(얼굴). 15초 원테이크라
  감정이 끊기지 않음

**Capability evidence**
- Doubao (author-described, free tier, 2026-10-01) / two-person
  hand contact + sustained lens-directed eye contact, 15s one-take /
  observed success / MEDIUM

**코퍼스 기여**
- 1 (strengthen — T-25 신체형 변형: 손이 프레임에 들어오고
  상대가 잡는다), T-14 cross-ref

**규칙 카드 (붙여넣기용)**
```
[카메라는 몸이다 — Soft Guidance]
남친 시점에선 카메라가 사람이 된다. 손을 프레임에 넣고,
상대가 그 손을 잡게 하라. 렌즈를 보는 눈 + 잡히는 손이
친밀감을 만든다. 원테이크로 끊지 마라.
```

```yaml
knowledge_update:
  existing_T: [T-25, T-14]
  existing_P: []
  evidence_strength: MEDIUM
  cross_model_generality: HIGH
  promotion_target: DIRECTING_TECHNIQUE
  action: strengthen_existing
  notes: "T-25 강화. #42(보이지 않는 존재) → #72(손이 보이는
    몸). 남친 시점 장르에서 카메라=등장인물이 신체 접촉까지
    확장됨. 고전 POV 문법이라 범용성 높음. 신규 번호 없음."
```

---

## 73. X @saniaspeaks_ — 2000년대 도쿄 가족 저녁 브이로그 (Seedance 2.5)

**기본 정보**
- 출처: X @saniaspeaks_ (Sania), 2026-10-01 게시. 61 likes,
  33 replies. 포스트 본문에 영어 프롬프트 전문 공개
- 모델: Seedance 2.5 (author-described)
- 영상 실측: 30.1초, 1280x720, 24fps, 721프레임. 스펙 30초와
  일치. vxtwitter API 경유 다운로드
- 증거 기반: prompt-derived (전문) + frame-observed (영상)

**프로토콜 판정 (기존 T/P 우선)**
- CONTINUITY 섹션: "The purchased ingredients must be the same
  ones used for cooking and served at dinner" — P-30 원리의
  작가 독립 서술. 장보기→씻기→조리→상차림의 사물 생애주기 →
  strengthen (P-30)
- DV 스펙: "No 4K sharpness, stabilization, beauty filters,
  VHS effects or cinematic lighting" — 불완전함 스펙의 완성형.
  "VHS effects 금지"가 포인트 (필터로 시대를 흉내내지 말고
  시대를 렌더하라는 지시) → strengthen (T-23)
- 섹션 구조: EXACT ORDER + ERA LOCK + CAMERA STYLE +
  CONTINUITY + FINAL FEEL — P-01의 LOCK 명명법 변형 →
  strengthen (P-01)
- "Use the SAME young Japanese woman from the reference image
  throughout" — 이미지 레퍼런스 정체성 고정 → strengthen (P-16)
- 신규 T/P 없음

**관찰 — 사물의 생애주기 (frame-observed)**
- kframe_006: 슈퍼에서 팽이버섯 팩을 집어 듦 (가격표·바코드
  클로즈업 — "고르고 있다"는 행위의 증거)
- kframe_019: 주방에서 표고버섯을 씻는 손. 산 재료가
  조리 단계로 이어짐
- kframe_028: 식탁 — 가운데 냄비에 버섯·채소. 산 것 = 씻은 것
  = 먹는 것. 3인 가족(부부+딸 추정) 자연스러운 젓가락질
- 가격표 일본어는 작고 흐릿함 — AI 난독증의 리스크 관리
  패턴 (작게·흐리게)

**관찰 — 시대 고증 (frame-observed)**
- 쇼지, 백열등 색온도, 브라운관 시대의 주방. 스마트폰·LED
  화면 없음. ERA LOCK의 포지티브+네거티브 병기가 렌더에 반영됨

**Capability evidence**
- Seedance 2.5 (author-described, 2026-10-01) / 30s 7-beat
  continuity, ingredient identity across beats, family dinner
  scene, DV look / observed success / MEDIUM

**코퍼스 기여**
- 3 (strengthen — P-30 사물 생애주기, T-23 DV 스펙 완성형,
  P-01 LOCK 명명법 변형), 1 (strengthen — P-16 이미지
  레퍼런스 정체성)

**규칙 카드 (붙여넣기용)**
```
[사물은 이력을 가진다 — Hard Lock]
장 본 재료는 씻겨서 냄비에 들어가야 한다. 산 장면, 쓰는
장면, 먹는 장면의 사물이 같은 것이어야 한다. 소품에도
생애주기가 있다.
```

```yaml
knowledge_update:
  existing_T: [T-23]
  existing_P: [P-01, P-16, P-30]
  evidence_strength: HIGH
  cross_model_generality: HIGH
  promotion_target: PROMPT_RECIPE
  action: strengthen_existing
  notes: "P-30의 독립 수렴 — 작가가 원리를 그대로 서술.
    T-23은 'VHS effects 금지' 추가로 완성형. P-01은 LOCK
    명명법 변형으로 강화. ERA LOCK은 P-01의 섹션 타입으로
    처리 (신규 번호 없음). 텍스트는 작게·흐리게 둘 것."
```

---

## 74. X @xhuozhong — 바이낸스 댄스 영상 샷별 재현 스펙 (중국어 8천자 프롬프트)

**기본 정보**
- 출처: X @xhuozhong (KEYVAN🔥小火種), 2026-10-01 게시.
  46 likes, 27 replies. 포스트 본문에 중국어 프롬프트 전문
  (~22KB) 공개
- 작업: 레퍼런스 틱톡 댄스 영상을 샷별로 복제하되, 남녀
  주인공 2명을 이미지 2장의 인물로 교체 + 분홍 스튜디오를
  바이낸스 노랑 + 바이낸스 로고(이미지 3)로 교체
- 스펙: 26.67초, 16:9, 1920×1080, 30fps. 실측 26.67초로
  스펙과 정확히 일치 (스펙 준수 사례)
- 모델/도구: 본문에 명시 없음. {{Mixed N}} 멀티모달 입력
  문법 사용 (inference: 비디오+이미지 혼합 입력 지원 도구)
- 완성본 영상: 별도 포스트(2104949243681394704)에 공개.
  "CZ作为鼓手好像也不错🤣" (CZ가 드러머 해도 괜찮네).
  526 likes, 63 replies — 프롬프트 공유글(46 likes)의 10배.
  남주는 바이낸스 창업자 CZ (author-described)
- 완성본 실측: 27.1초, 1922x1080, 컬러 정상. vxtwitter API
  경유 다운로드
- 레퍼런스: 로제(Rosé)의 "APT." 뮤직비디오 (사용자 관찰).
  분홍 스튜디오→바이낸스 노랑 교체의 원본
- **데이터 주의**: 프롬프트 글의 첨부 mp4는 무채색(CDN본 자체).
  색상·브랜드 검증은 완성본 영상으로 수행. 아래 관찰은 완성본
  기준
- 증거 기반: prompt-derived (전문) + frame-observed (완성본)

**프로토콜 판정 (기존 T/P 우선)**
- 멀티 레퍼런스 + 비디오 역할 + 충돌 우선순위: P-15의
  비디오 확장. @视频1=동작·카메라·편집 전용 ("얼굴·헤어·
  의상은 상속 금지"), @图片1/2=외모·의상, @图片3=로고.
  "发生冲突时: 外貌→图片, 动作→视频, 标志→图片3" →
  strengthen (P-15)
- 점·문신 미세 식별자 락: "痣不要移动到嘴角，不要左右镜像，
  不要在特写中消失" / "禁止纹身转移到左臂，禁止左右手臂
  同时出现纹身" → strengthen (P-16)
- 실패 카탈로그형 네거티브 (섹션 八): "禁止纹身换边",
  "禁止把背景标志做成跟随镜头的水印", "禁止全画面黄色滤镜
  污染肤色和红裙" — 각각 목격된 실패 모드 → strengthen (P-21)
- 하드컷의 소품 허가: "不同拍摄段可以通过原片硬切更换眼镜
  道具，但同一个连续镜头内不能凭空出现、消失或变形" —
  T-37의 정밀 서술 → strengthen (T-37)
- 임시 소품 레이어 규칙 (선글라스를 기존 안경 위에 씌우고,
  바깥 레이어만 벗김) → P-30에 노트
- 신규 T/P 없음

**관찰 — 프롬프트 구조 (prompt-derived)**
- 17개 샷의 타임스탬프 분해 (镜头1~17, 0–26.67s)
- 섹션 七 (소리): 원곡 트랙 위치·박자·가창 순서 유지, 립싱크는
  음절 변화 추종, 브랜드 내레이션 삽입 금지
- "不是重新编排剧情" — 작업 유형의 네거티브 선언 (재현이지
  재해석이 아님)
- 헤어 물리 스펙: "发根稳定，发束有自然惯性，不变短、不变金色、
  不穿过脸部" — 정체성(길이·색 유지) + 물리(관성, 얼굴 관통 금지)

**관찰 — 완성본 (frame-observed)**
- kframe_005: CZ풍 남자(백발 섞인 짧은 머리, 선글라스) 검정
  티셔츠 "EXCHANGE THE WORLD" 문구 판독 가능. 여자 빨간
  드레스, 어깨에 기대는 포즈. 노랑 스튜디오 + 양옆 스피커/
  앰프. 필름 프레임 테두리 2D 그래픽 효과 ("少量二维图形特效")
- kframe_014: 입 극클로즈업 (镜头 리스트의 "嘴部极近特写").
  빨간 입술, 가창 중
- kframe_024: 둘이 바닥에 앉아 건배. 여자 빨간 드레스 유지
  (바지 변형 없음). 벽에 바이낸스 로고 (검정 둥근 사각형+노랑
  마크, 부분 노출). 노랑 배경이 피부·빨간 드레스를 오염시키지
  않음 — P-21 네거티브 "禁止全画面黄色滤镜污染肤色和红裙" 성립
- 2명만 등장. 분홍 잔재 없음

**Capability evidence**
- model: undisclosed ({{Mixed}} syntax tool, 2026-10-01) /
  27s APT.-style recreation: yellow studio without skin
  pollution, legible shirt text, logo on wall, 2-person lock /
  observed success / MEDIUM-HIGH

**코퍼스 기여**
- 4 (strengthen — P-15 비디오 역할+충돌 우선순위, P-16 미세
  식별자 락, P-21 실패 카탈로그 네거티브, T-37 하드컷 소품 허가),
  1 (note — P-30 임시 소품 레이어)

**규칙 카드 (붙여넣기용)**
```
[역할을 나누고, 충돌엔 순위를 — Hard Lock]
레퍼런스가 여러 개면 각각 1역할만: 비디오는 동작·카메라·
편집 전용, 얼굴과 옷은 상속 금지. 충돌 시 우선순위를
명시하라 — 외모는 이미지, 동작은 비디오, 로고는 이미지3.
```

```yaml
knowledge_update:
  existing_T: [T-37]
  existing_P: [P-15, P-16, P-21, P-30]
  evidence_strength: HIGH
  cross_model_generality: HIGH
  promotion_target: PROMPT_RECIPE
  action: strengthen_existing
  notes: "P-15의 비디오 확장 + 충돌 우선순위 명시가 최대 수확.
    P-21은 섹션 八 전체가 실패 카탈로그 — 완성본에서 노랑
    피부오염 방지가 실제로 성립함. T-37은 하드컷의 소품 허가로
    정밀화. 완성본 526 likes는 프롬프트글 10배 — 결과물이
    과정을 압도 (인기도 분해 신호). 신규 번호 없음."
```

---

## 75. X @HAL2400_AI — 비 속 소녀 25초 (컷온액션 교과서)

**기본 정보**
- 출처: X @HAL2400_AI (일본 크리에이터), 2026-10-01 게시.
  48 likes, 1 reply. "AIでエモい動画作ってみたら、想像以上に
  エモかった"
- 실측: 25.1초, 1920x1080. 모델 미공개
- 증거 기반: frame-observed

**프로토콜 판정 (기존 T/P 우선)**
- 전 컷이 진행 중인 동작에 실려 넘어감 (cut on action) →
  strengthen (T-33)
- 신규 T/P 없음

**관찰 — 시퀀스 (frame-observed)**
- k_002: 클로즈업 — 처마 밑에서 손을 비에 내밈
- k_007: 미디엄 — 처마 밑에서 거리로 걸어 나옴 (후면)
- k_012: 와이드 — 비 오는 주택가를 뜀 (후면)
- k_016: 공원 — 정자를 향해 걸어감 (후면)
- k_020: 정자 밑 — 젖은 포니테일을 짬, 뒤를 돌아봄
- k_024: 클로즈업 — 젖은 앞머리로 카메라를 보고 웃음

**관찰 — 연결이 매끄러운 이유 4종**
1. **운반되는 동작**: 손 내밀기 → 걸어 나가기 → 뛰기. 컷이
   동작의 한가운데서 잘림. 동작이 끝나고 자르면 다음 컷이
   새로 시작하는 느낌이 됨
2. **방향 불변**: 전 컷에서 카메라에서 멀어지며 앞으로.
   방향이 뒤집히지 않음
3. **인과 사슬**: 비 → 나가기 → 뛰기 → 젖음 → 대피 →
   머리 짜기 → 웃음. 각 컷이 "그래서?"에 답함
4. **상태 누적**: 젖음이 논리적으로 쌓임. 마지막 웃음은 젖은
   앞머리가 증명 (소품=증거)

**코퍼스 기여**
- 1 (strengthen — T-33 cut on action의 교과서 사례)

**규칙 카드 (붙여넣기용)**
```
[컷은 동작에 실어 보내라 — Soft Guidance]
컷을 동작의 한가운데서 자르고, 다음 샷은 그 동작의
계속으로 시작하라. 동작이 끝난 지점에서 자르면 다음 컷은
새 우주가 된다. 방향·인과·상태는 전 컷에 걸쳐 고정.
```

```yaml
knowledge_update:
  existing_T: [T-33]
  existing_P: []
  evidence_strength: HIGH
  cross_model_generality: HIGH
  promotion_target: PROMPT_RECIPE
  action: strengthen_existing
  notes: "T-33 어휘 중 cut on action의 완성형 사례. 사용자의
    '내 컷은 왜 어색한가' 질문에 대한 진단 재료로 직접 사용.
    신규 번호 없음."
```

---

## 76. X @LioraSolveil — 임금 수묵 액션 33초 (한국어 프롬프트 전문)

**기본 정보**
- 출처: X @LioraSolveil, 2026-10-01 게시. 33 likes, 19 replies.
  "이 AI 영상은 걸작입니다. 한국형 캐릭터에 어울리게 프롬프트
  수정함. 임금과 수묵으로 표현해봄. @lansenai 원본 프롬프트"
- 프롬프트 계보: @lansenai 원본 → LioraSolveil 한국어 수정
  (임금+수묵). 사용자가 프롬프트 전문을 채팅에 붙여넣음
- 제작: Newtake 지원 (author-described, #newtakecrew)
- 실측: 33.5초, 3840x2160 (4K). 30초 스펙 대비 3.5초 초과
- 증거 기반: prompt-derived (전문) + frame-observed +
  author-described (Newtake, lansenai 원본)

**프로토콜 판정**
- **T-39 신규** (new_candidate): "정적 주인공 × 동적 공간".
  기존 T로 설명 불가 (T-18은 카메라 반응, T-21은 임팩트
  타이밍 — 주인공/공간의 대비를 스펙터클 엔진으로 쓰는
  기법은 없음). 별도 제작 문제 해결: AI는 복잡한 무술
  동작을 못 그리고 유체·파티클·잉크는 잘 그림 → 스펙터클을
  몸에서 떼어 공간으로 옮김. 관찰 근거: 프롬프트 명시 +
  프레임 3종 수렴
- T-34 strengthen (원형 구성): 시작=낮은 후측면에서 천천히
  걷기 → 종료=같은 구도로 걷기. 발뒤꿈치 뒤 가느다란 먹자국
  하나만 남음
- T-09 strengthen (공간 방향): "카메라가 움직여도 공간의
  앞뒤와 좌우 관계가 뒤집히지 않는다" + 석주 위치 전편 고정
- T-33 note (관성 연결): "기술과 기술 사이에 멈춰서 포즈를
  잡지 않는다. 모든 액션은 이전 동작의 관성에서 다음 동작으로
  연결된다" — #75의 컷온액션과 수렴
- P-06 strengthen (충격 프레임 시간 명세): 0.05/0.1/0.15초
  등급 + 레이어 스택 순서 ("흑백 수묵 충격 프레임 → 부분 반전
  → 카메라 축 흔들림 → 먹점 튐")

**관찰 — 핵심 장치 (prompt-derived + frame-observed)**
- "미친 듯이 움직이는 것은 주인공의 몸이 아니라, 주인공의
  동작에 의해 발생하는 공간과 에너지의 변화다"
- k_003: 임금이 차분히 걸어가는데 뒤에서 거대한 검은 붓질이
  공간을 가로지름. k_015: 한 팔만 뻗고 공중에 뜸, 아래는
  잉크 산맥+부유석. k_030: 파괴된 수묵 세계 중심에 조용히
  서 있음. 몸은 정적, 공간은 격동 — 3프레임 모두 수렴
- 수묵은 화면 필터가 아니라 실제 3D 공간의 물질
  ("수묵화가 현실 세계를 침범하는 듯")
- 카메라: "정면에서 세워놓고 스킬을 보여주듯 촬영하지 않는다".
  초저각·후측면·3/4 위주. 얼굴은 필요할 때만
- 7개 기술(먹보→오행묵류)+최종기(먹계·천지전도). Time Ramp
  100%→250%→30%→300%
- 타임스펙 초과: 30초 스펙 → 33.5초 렌더 (#70의 20→30초와
  같은 스펙 드리프트 계열)

**Capability evidence**
- model: Newtake (author-described, 2026-10-01) / 33s ink-wash
  action, static protagonist + kinetic environment, 4K /
  observed success / MEDIUM

**코퍼스 기여**
- 1 (new_candidate — T-39 정적 주인공 × 동적 공간),
  4 (strengthen — T-34, T-09, T-33 note, P-06)

**규칙 카드 (붙여넣기용)**
```
[움직이지 않는 몸, 폭발하는 공간 — Hard Lock]
스펙터클을 몸에서 떼어 공간으로 옮겨라. 주인공은 차분히
걷고, 세상이 미친 듯이 반응한다. AI는 복잡한 무술보다
유체·파티클·잉크를 잘 렌더한다. 수묵은 필터가 아니라
공간에서 발생하는 물질이다.
```

```yaml
knowledge_update:
  existing_T: [T-34, T-09, T-33]
  existing_P: [P-06]
  new_T: [T-39]
  evidence_strength: HIGH
  cross_model_generality: MEDIUM-HIGH
  promotion_target: PROMPT_RECIPE
  action: new_candidate
  notes: "프롬프트 명시 + 3프레임 수렴으로 evidence HIGH.
    대비 엔진 자체는 모델 비의존이나 잉크 렌더 품질은 모델
    의존 → generality 분리 표기. 30초→33.5초 스펙 드리프트는
    capability evidence로 별도 기록."
```

---

## 77. X @saniaspeaks_ — 2000년대 도쿄 버스 여행 30초 (동행자 방향 동기화)

**기본 정보**
- 출처: X @saniaspeaks_ (Sania, #73과 동일 작가), 2026-10-01
  게시. 17 likes, 8 replies. "Bus rides are better with your
  bestie. Seedance 2.5 on higgsfield"
- 포스트 본문에 영어 프롬프트 전문 공개 (6비트 타임스탬프
  스토리보드)
- 실측: 30.1초, 1280x720. 모델: Seedance 2.5 (author-described)
- 증거 기반: prompt-derived + frame-observed

**프로토콜 판정 (기존 T/P 우선)**
- FRIEND LOCK: "The SAME Japanese female friend stays with
  her throughout" — 주인공 외 동행 인물의 별도 락 →
  strengthen (P-16)
- 동행자 방향 동기화: 두 소녀가 항상 같은 방향을 보고 같은
  방향으로 걸음. 카메라는 전편 뒤에 고정 (친구가 찍는 POV) →
  strengthen (T-09)
- 종이 버스 티켓의 6비트 추적 ("Same girls, outfits, bags
  and tickets throughout") → note (P-30)
- ERA LOCK·DV 스펙은 #73과 동일 레시피 — 추가 강화 없음
- 신규 T/P 없음

**관찰 — 사용자의 지적과 수렴 (frame-observed)**
- k_003: 둘이 함께 버스 시간표를 봄 (시선 목표 일치)
- k_011: 둘이 함께 버스에 탑승 (이동 방향 일치, 티켓 손에)
- k_027: 둘이 함께 목적지로 걸어감 (후면, 의상·가방 유지)
- 사용자가 말한 "시선이나 걷는 방향 모두"가 정확함. 카메라가
  축을 넘지 않으니 방향이 깨질 일이 없음 — #75의 "방향 불변"과
  동일 원리

**Capability evidence**
- model: Seedance 2.5 via Higgsfield (author-described,
  2026-10-01) / 30s 2-person vlog, gaze/direction sync,
  6-beat continuity / observed success / MEDIUM

**코퍼스 기여**
- 3 (strengthen — P-16 FRIEND LOCK, T-09 동행자 방향 동기화 /
  note — P-30 티켓 추적)

**규칙 카드 (붙여넣기용)**
```
[동행자는 같은 방향을 본다 — Soft Guidance]
함께 걷는 인물들의 시선·이동 방향을 일치시켜라. 카메라는
뒤에 고정. 축을 안 넘으면 방향이 안 깨진다.
```

```yaml
knowledge_update:
  existing_T: [T-09]
  existing_P: [P-16, P-30]
  evidence_strength: HIGH
  cross_model_generality: HIGH
  promotion_target: PROMPT_RECIPE
  action: strengthen_existing
  notes: "사용자가 직접 포착한 사례 ('시선이나 걷는 방향 모두').
    #75 방향 불변과의 수렴. FRIEND LOCK은 2인 락의 명시형.
    신규 번호 없음."
```

---

## 78. X @beginnersblog1 — 9단계 프롬프트 프레임워크 (텍스트 가이드)

**기본 정보**
- 출처: X @beginnersblog1 (Beginnersblog), 2026-10-02 게시.
  98 likes, 7 replies. "Most AI video prompts fail before
  generation even starts"
- 영상 없음. 텍스트 가이드 + 예시 이미지 1장. #54와 같은
  텍스트 가이드 카테고리
- 사용자가 "네가 말하던거 많이 정리되어 있어"라며 직접 공유
- 프레임워크: INTENT → SUBJECT + ACTION → FRAME → OPTICS →
  CAMERA → PERFORMANCE + PHYSICS → LIGHT + SPACE → CONTINUITY
- 증거 기반: text-guide (author-described)

**프로토콜 판정**
- 외부 이론의 독립 수렴 케이스 (#54·#56과 동형). 코퍼스가
  유도한 패턴들과의 매핑이 핵심
- P-06 strengthen: "Prompt visible behavior" ("Man is scared"
  → "freezes at the doorway, eyes tracking toward the sound").
  Trace-first의 영어권 독립 서술. 마이크로 퍼포먼스 추가
  (breathing, hesitation, weight shifts, foot contact)
- P-30 strengthen: "Every shot exists between two states" —
  start position → screen direction → costume → props →
  end position. 샷의 양끝 상태 명세
- T-18 note: "one motivated camera behavior. The camera should
  move because the story gains something"
- T2V vs I2V 구분 ("stop describing the reference image again.
  Prompt the motion") — 기존 P 없음. P-32 후보로 보류
  (단일 출처, 두 번째 독립 사례 대기)
- 신규 T/P 번호 없음

**수렴 매핑**
- INTENT ("shot has no purpose → camera language will not
  save it") ↔ 사용자의 Necessity Test + #75 "관통하는 의도"
- "One shot. One camera setup. One clear beat." ↔ 비트
  디시플린 (8초 생성에 5개 액션을 쑤셔 넣지 말 것)
- OPTICS ("Do not add 35mm because it sounds cinematic. Know
  why it is there.") ↔ 렌즈 의도성
- PERFORMANCE + PHYSICS ("This is where many AI shots
  collapse") ↔ 사용자의 embodied difficulty 전략

**코퍼스 기여**
- 3 (strengthen — P-06, P-30 / note — T-18), 1 (candidate —
  P-32 T2V/I2V 구분 보류)

**규칙 카드 (붙여넣기용)**
```
[샷에게 일을 시켜라 — Hard Lock]
샷마다 목적을 먼저 정해라. 목적 없는 샷은 카메라 언어로
못 살린다. 그리고 한 샷에 한 비트만. 8초 생성에 다섯 개
액션을 쑤셔 넣지 마라.
```

```yaml
knowledge_update:
  existing_T: [T-18]
  existing_P: [P-06, P-30]
  evidence_strength: MEDIUM
  cross_model_generality: HIGH
  promotion_target: PROMPT_RECIPE
  action: strengthen_existing
  notes: "텍스트 가이드 단일 출처 → evidence MEDIUM. 가치는
    수렴 자체 (#54·#56과 동형). T2V/I2V는 P-32 후보로 보류,
    두 번째 독립 사례 나오면 번호 발급. 신규 번호 없음."
```

---

## 79. X @7998l201 — 남친 시점 가재 먹이기 10초 원테이크 (중국어)

**기본 정보**
- 출처: X @7998l201 (Ryan), 2026-10-02 게시. 64 likes, 12 replies.
  "Muse 视频直出，男友视角视频提示词（续集）" (Muse 직접 출력,
  남친 시점 프롬프트 속편)
- 포스트 본문에 중국어 프롬프트 전문 공개 (10초 타임스탬프
  스토리보드 + 环境动态 + 声音 + 限制 섹션)
- 실측: 10.1초, 720x1280 세로 9:16. 모델: Muse (author-described)
- 증거 기반: prompt-derived + frame-observed

**한국어 번역 (요지)**
- 설정: "전편에 이어. 밤 아파트 거실, 진짜 아이폰 생활 스냅.
  심야 커플의 방탕한 행복 — '드디어 집이다, 오늘 밤은 우리 둘의 것'"
- 인물: 전편과 동일한 젊은 동양 여성. 그의 오버사이즈 다크
  티셔츠 + 맨발 + 대충 틀어 올린 머리
- 0-2s: 그녀가 당신의 손을 잡아끌고 현관에서 거실로. 소파에
  앉힘. 외卖袋(배달 봉투)가 식탁에
- 2-5s: 소파에 다리를 꼬고 앉아 배달 개봉 — 샤오룽샤(가재).
  일회용 장갑 끼고 가재살을 발라 당신의 입에 가져다 댐
- 5-8s: 당신이 그녀 뺨을 꼬집자 볼을 부풀리고 삐진 척하다
  웃음 터짐. 까놓은 새우가 상자에 떨어짐. 품에 안기며
  "벌로" 가재 하나 더 까달라고 손가락으로 콕콕
- 8-10s: 올려다보며 "以后不许这么晚回来，听见没？" (앞으로
  이렇게 늦게 들어오면 안 돼, 알았지?). 이마로 당신의 턱을
  쿵 — 도장 찍듯. 웃음+흔들림 속 종료
- 촬영: "10초 하나의 연속镜头, 不切镜" (원테이크 무컷).
  아이폰 기본 카메라, 앉은 남친 시점 눈높이. 스태빌라이저·
  큰 푸시풀·오빗·슬로모 금지

**프로토콜 판정 (기존 T/P 우선)**
- 남친 시점 원테이크 속편: 카메라=몸 (앉은 눈높이) + 원테이크로
  감정을 끊지 않음 + "接上一集" (전편 이어짐) →
  strengthen (T-25, T-27)
- 环境动态 (환경 동태) 독립 섹션: 김 오름·비닐 바스락·새우껍질
  쌓임·소파 꺼짐/복원·옷감 마찰 → note (P-06)
- 반(反)글래머 네거티브: "不要电影级浅景深、不要商业广告
  写真感" (영화급 얕은 심도 금지, 광고 사진 느낌 금지) —
  미적 방향을 네거티브로 지정 → strengthen (P-21)
- 사운드 설계 (폴리 리스트 + 마지막 대사의 "带笑意的嗔怪语气")는
  관찰로 기록. 오디오 프롬프트는 DB 범위 밖 (P-31 분리 방침)
- 신규 T/P 없음

**관찰 (frame-observed)**
- k_004: 오버사이즈 다크 티셔츠 + 파란 일회용 장갑 끼고 가재
  까는 중. 따뜻한 거실광
- k_008: 까놓은 가재살을 카메라(남친) 입에 넣어주는 순간.
  그녀가 기대며 손가락으로 가리킴 — 친밀감의 육체적 난이도가
  그대로 렌더됨
- 사용자의 embodied difficulty 전략과 정면 수렴: 장갑 끼고
  가재를 까서 남의 입에 넣어주는 것은 "몸이 아는 번거로움" 그
  자체. 쉬운 장면(쳐다보기·웃기)이 아니라 어려운 접촉이 리얼함을
  만듦

**Capability evidence**
- model: Muse direct output (author-described, 2026-10-02) /
  10s one-take boyfriend POV, crayfish peeling+feeding with
  gloves, seamless emotion shifts (得意/耍赖/撒娇) /
  observed success / MEDIUM

**코퍼스 기여**
- 3 (strengthen — T-25 남친 시점 원테이크 속편, T-27 속편
  연속성, P-21 반글래머 네거티브 / note — P-06 환경 동태 섹션)

**규칙 카드 (붙여넣기용)**
```
[카메라는 몸이다 — Soft Guidance]
남친 시점에서는 카메라가 몸을 가진다. 앉은 눈높이, 손이
프레임에 들어오고 상대가 그 손을 잡는다. 원테이크로 감정을
끊지 마라.
```

```yaml
knowledge_update:
  existing_T: [T-25, T-27]
  existing_P: [P-06, P-21]
  evidence_strength: HIGH
  cross_model_generality: MEDIUM
  promotion_target: PROMPT_RECIPE
  action: strengthen_existing
  notes: "중국어 프롬프트 전문 공개 + 프레임 검증. T-25의
    #72 신체형 변형을 10초 원테이크 속편으로 확장. 사용자의
    embodied difficulty 전략과 정면 수렴 (장갑 낀 가재 까기).
    신규 번호 없음."
```

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
    ★★★ (21·25·32·39·41)
44. **백분율 페이즈**: 페이즈 구간을 절대 초가 아닌 백분율
    (0-25·25-55·55-70·70-100)로 지정. #31(모델은 절대 시간을 못 지킴)의
    해법 — #41에서 4개 페이즈 경계가 프레임 4장과 맞아떨어짐. ★ (41)
45. **Speech Axes**: 목소리를 축 단위로 파라메트릭 제어
    (speech_rate·pitch_contour·rate_change·loudness·vocal_intensity) +
    axisBias 마스터 게인. 감정 연기의 "음성 이퀄라이저". ★ (41)
46. **키 프레이즈 트리거 + 운율 표기**: 폭발 페이즈의 트리거를 키
    프레이즈에 바인딩하고 "왜~~~~" 같은 물결표로 발성 길이를 표기.
    WORD_VOLUME_SPIKE / WORD_STRESS로 강세 위치 지정. ★ (41)
47. **엔딩 벡터**: 엔딩 에너지 방향을 4축으로 지정
    (release/sustain/drop/rise). "drop=1"은 무너지는 엔딩. ★ (41)
48. **렌즈=씬 파트너**: 분노의 대상이 렌즈 자체 — 2인칭 호소 장면의 시선
    문법. 관객(#40)·금지(#12)·무관여(#39) 다음 네 번째. 감정의 호가
    곧 시선의 호(고정→격렬→철수). ★ (41)
49. **모듈러 프롬프트 참조 (Coupling)**: "Coupling: ON (existing
    speech_coupling text applies)" — 공유 텍스트 블록을 참조하는 모듈
    구조. XAI-Studio-Video 마스터 스펙 철학과 수렴. ★ (41)
50. **Camera-as-presence**: MOOD 한 줄에 카메라의 서사적 정체 선언 —
    "unseen presence floating above her, waiting for her to notice".
    카메라는 시점이 아니라 캐릭터이며, 마지막 비트(렌즈 응시)가 그
    존재를 알아차리는 순간으로 수렴. ★ (42)
51. **Phantom camera**: "passing through ceilings and door frames as one
    uninterrupted camera event" — 카메라는 건축을 통과, 인물만 물리에
    묶임. ★ (42)
52. **비트마다 락 재확인**: SCENE의 각 비트를 카메라 관계로 시작
    ("Still centered under the lens", "Under the same overhead lock",
    "Still pinned overhead"). 락을 한 번 선언하고 끝내지 않음. ★ (42)
53. **Handedness lock**: 오른손=담배 전편 고정, 왼손=작업
    (수도·세수·유리잔). "Extends that arm away from the running water" —
    소품 보호 동작까지 지정. ★ (42)
54. **COLOR LOGIC 한 줄**: "COLOR LOGIC: Matrix Green Look" — 네임드
    그레이드를 한 줄로 고정. ★ (42)
55. **파이널 비트 7연타**: "Stops exactly under the lens. Freezes. Looks
    right. Looks left. Takes a drag. Snaps her head straight up into the
    lens. Blows smoke toward the camera. Locks eye contact." — 전편
    유일의 렌즈 응시를 클라이맥스로 배치. 응시의 희소성이 공포 문법.
    ★ (42)
56. **Diegetic camera seat**: 매 장소에 카메라의 네이티브 자리를 지정 —
    카트 안·차 뒷좌석·전망대·밤의 매크로. 카메라는 항상 참여자, 이방인
    아님. ★ (43)
57. **Foreground POV proof**: "from inside X"는 말로 끝내지 말고 전경
    물건으로 증명 — 카트 샷에서 캔들을 렌즈와 피사체 사이에. ★ (43)
58. **시간대 아크**: 낮(매장)→골든아워(드라이브)→일몰(전망대)→밤. 편집
    로직을 컷이 아니라 빛의 진행으로. 프롬프트 서술 순서 = 시간대 순서.
    ★ (43)
59. **단일 연속 질량**: 물(불·모래 등 유체 마법)은 전편 하나의 연속된
    질량으로. 순간이동·소멸·재생성 금지. "그럴듯함"의 첫 번째 출처.
    ★ (44)
60. **샤드 생명주기**: 물에서 분리된 부분이 즉시 얼어 발사체로 —
    분리→동결→발사 3단계, 질량 보존. ★ (44)
61. **Grounded negatives**: "No glowing effects, energy beams, neon
    trails, or anime aura" — 판타지를 실사 물리로 렌더. "그럴듯함"의 두
    번째 출처. ★ (44)
62. **END BEFORE IMPACT**: 임팩트 직전에 스매시 컷. 최종 프레임은 다음
    씬(Scene 02)을 위한 모멘텀 보존. 해결 없는 엔딩. ★ (44)
63. **In medias res**: "Fight begins mid-combat" — 셋업 없이 전투 중부터
    시작. 10초 단尺의 필수 장치. ★ (44)
64. **Deliberate imperfection spec**: "misaligned framing, delayed focus
    pulls, clumsy zooms, occasional face cut-off framing, imperfect
    shots" — 불완전함을 스펙으로 명시. MiniDV 룩의 핵심. ★ (45)
65. **Propped camera grammar**: 셀프 POV의 두 모드 — held와 propped. 컷마다
    카메라 모드 지정 (바닥/매트에 거치). 손이 필요하면 카메라를 내려놓는다.
    셀프 POV 역설의 물리적 해법. ★ (45)
66. **Cut-level audio**: 컷 4 "No dialogue — ambient gym sound only".
    컷별 오디오 온오프. ★ (45)

67. **Enemy arithmetic**: 증식/분열하는 적의 총수를 수식으로 명시 —
    1→2→4→5→6→7→(3 fall)→4→1. "the original becomes the pair, never a
    third figure". 맞은 적만 나뉘고, 떨어진 적은 텔레포트로 복귀 금지.
    ★ (46)
68. **CUT ON [action]**: 11개 컷 전부 액션 트리거로 연결 — "CUT ON his
    backward recoil", "CUT ON their synchronized stare". #1의
    CUT-as-trigger를 12샷 구조로 일반화. ★ (46)
69. **Shooting axis lock**: "Preserve the shooting axis... staying on the
    established side of the axis" — #28 master-axis의 명시적 선언.
    ★ (46)
70. **Ammo economy**: "six rounds, no reload" → two dry clicks → "fully
    seats the revolver in her right-hip holster" → "The gun remains
    holstered". 소품의 총량을 12샷 전체에 걸어 잠금. ★ (46)
71. **Pre-planted escape device**: 보드는 처음부터 있었지만 "concealed by
    hull and framing until Shot 11" / SHOT 10 "Keep the board below
    frame". ★ (46)
72. **No fixed beauty pose**: "Exaggerate her expressions... no fixed
    beauty pose" — 표정은 발견에 반응. ★ (46)
73. **Animation principles in prompt**: "selective speed smears, hair and
    fabric follow-through; effects never hide impacts" — 만화 애니메이션
    원리를 프롬프트에 직접. 사용자의 취향(만화식 컷 문법+실사 렌더, #27)과
    직결. ★ (46)
74. **Resolution stepping**: 480p 초안 → GPT 수정 → 480p 최종 → 720p 최종 →
    2~3클립 편집 → Topaz 1080p. 싸게 반복하고 비싸게 마무리. ★ (46)

75. **BPM header**: "FORMAT: 15s / 145 BPM / 15 SHOTS / beat-synced
    routine" — 템포를 포맷 선언에 박음. ★ (47)
76. **Per-shot SFX**: 각 샷 끝에 "/ SFX:" — 샷별 사운드 디자인 (alarm,
    sheet rustle / mattress bounce, blanket whip...). ★ (47)
77. **Edit-grammar transitions**: "Sound bridge / Smash cut / L-cut /
    Match cut / Cut on action / Camera wipe / Object pass" — 컷 사이를
    편집 문법 어휘로 연결. ★ (47)
78. **LOGIC RULE**: "Keep logical consistency in wardrobe, props,
    locations, and action continuity across all shots." — 일관성 마스터
    스위치 한 줄. ★ (47)
79. **Day-cycle bookend**: 06:50 알람 → 침대 붕괴, "collapsing into bed
    in the opening frame shape" — 첫 프레임 모양으로 돌아오는 원형 구성.
    ★ (47)
80. **Insert-shot economy**: 15샷 중 4개가 Insert — 디테일 컷어웨이가
    페이스를 만듦. ★ (47)
81. **MOOD arc line**: "Late-for-work panic, clipped momentum, breathless
    urgency, then an exhausted exhale" — 4비트 감정 아크 한 줄. ★ (47)

