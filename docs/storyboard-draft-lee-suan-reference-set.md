# Storyboard Draft 0 — 이수안 레퍼런스 세트 (4편)

> 상태: **Draft 0 (검토용)**. 사용자 승인, 러프 보드, 샘플, 렌더 모두 아직 안 했다.
> 캐릭터: `ch-lee-suan` (이수안). 정체성 참조: `reference_defaults.identity` (BATCH-004 `gpt-image-09.png`, 사용자 선택).
> 방법론: [Intent-Preserving Video Methodology](intent-preserving-video-methodology.md) + [Video Intent Contract](video-intent-contract.md).
> 레퍼런스 출처: [reference-state-analyses.md](reference-state-analyses.md) 항목 번호. 작성: Claude Code (`claude`).

## 0. 이번 방법론에서 달라진 점 (이 콘티에 적용한 것)

1. **콘티와 Intent Contract를 같이 만든다.** 각 클립 아래에 계약 초안(`status: draft`)을 붙였다. 승인하면 콘티
   리비전·해시와 계약이 한 쌍으로 묶이고, 그 뒤로는 프롬프트 단계에서 **동작 순서·시선·방향·카메라·생략·끝 상태를
   바꿀 수 없다.**
2. **창작 레벨은 허용 목록(allow-list)이다.** 아무 말 없는 항목은 금지다. 대부분 L1(렌즈·빛·심도·질감·작은 프레이밍
   조정만 허용)로 잡았다.
3. **실현 방식(feasibility)을 프롬프트 전에 정한다.** 렌더가 어려운 과정은 `IMPLY`/`OMIT`/`SPLIT`으로
   처리하고 (v1.1: 컷 뒤에 숨기는 것도 관객이 받는 정보에 따라 셋 중 하나로 적는다), 프롬프트를 길게 써서 해결하지 않는다.
4. **시간은 순서로 적는다.** 정확한 초는 대사·컷 포인트처럼 시간 자체가 의미일 때만.
5. **(v1.1, 작업 중 개정) 승인된 프롬프트 문장도 계약에 들어간다.** 각 동작마다 감독이 승인한 한 줄(`prompt_segments`)을
   계약에 넣고, 템플릿이 그대로 조립한다. LLM은 창작 슬롯에서 **미리 나열된 값(`allowed_values`) 중 고르기만** 한다.
   그래서 승인 단계에서 동작별 프롬프트 문장까지 같이 확정한다. 아래 초안의 `allowed` 목록은 승인 시 값 목록으로 바뀐다.
6. **평가는 두 축**: Intent Fidelity(의도 충실도)와 Cinematography Gain(촬영 이득). 예쁜데 의도가 틀리면 실패.

## 1. 레퍼런스 선정

79건 중 **인물 1명·장소 1곳·작은 사건 하나**로 성립하고, 로컬 H3(클립당 약 7.3초, 클립당 `[Shot]` 1개만 검증됨)로
나눠 찍을 수 있는 것을 골랐다. 액션·다인물·멀티샷 전용 문법은 제외했다.

| 편 | 레퍼런스 | 빌려오는 것 (증거 수준) | 이수안과 맞는 이유 |
|---|---|---|---|
| A | #19 빗방울 침실 MiniDV | 시선은 끝까지 렌즈를 안 보고 **이름 붙은 대상**(소매·수건·창)만 본다, 실시간 모션, 벽→창 변형 금지 네거티브 (prompt + frame) | 젖은 잔머리와 리본이 "비를 맞았다"는 증거가 된다. 차분한 기본 표정과 맞음 |
| B | #23 옥상 라디오 석양 | 단일 장소, 소품 물리, **대사가 있을 때만 렌즈를 봄**, 감정 강요 금지 (prompt + frame) | 뒷모습 와이드에서 리본 실루엣이 가장 잘 읽힌다 |
| C | #63 처음 구워본 꽁치 (+#67 대사 브릿지) | 조리 과정은 **보여주지 않고** 도구 자리 POV·김·한마디로 건너뜀, 맛은 얼굴로 (frame; 생략 의도는 inference) | 서툰 첫 요리라는 설정이 생략을 정당화. 손동작 위험을 피함 |
| D | #11 무언 감정연기 싱글테이크 | 인물은 움직이지 않고 **빛이 움직이며** 감정이 넘어감, 프레임 안 광원 없음 (prompt only, 렌더 미확인) | 클로즈업에서 회갈색 눈과 섬세한 얼굴이 주인공 |

후보에서 뺀 것: #75 비 속 컷온액션(좋지만 A와 비가 겹침 — A 대체안으로 보류), #31 도서관(2인), #60 이너웨어 광고(이번 범위와 무관).

## 2. 공통 설정

- 엔진(예정): WanGP `minimax_h3_ref2va_pruned`. 클립당 `video_length: 181` ≈ 7.29초. 한 클립 = 한 비트 = 한 카메라 상태.
- 화면비: 16:9 가로 (D만 미정 — 열린 결정 참조).
- 참조 역할: 정체성 = `reference_defaults.identity` 1장. 의상·장소는 텍스트 Scene Delta. 클립 연결에 이전 클립 마지막
  프레임을 쓸지는 샘플 후 결정(텍스트만으로 이어지는 클립은 몽타주로 간주).
- **DNA는 그대로**: 둥근 업두 + 흑백 리본 + 시스루 앞머리. 머리를 풀거나 리본을 빼지 않는다. 젖음·의상·화장은 장면 변수.
- 각 편 2~3클립, 15~22초. 클립 사이 컷은 동작 중간이나 동기 있는 가림에서만 (FAIL-014).

---

## A. 「비 오는 저녁, 젖은 리본」 — ref #19

### Director Intent
퇴근길 비를 맞고 원룸에 들어온 수안. 누군가(친구, 화면 밖)가 캠코더를 들고 있지만 그녀는 한 번도 렌즈를 보지 않는다.
젖은 소매 → 수건 → 창밖 비. 남는 것은 **아무도 안 보는 것 같은 사적인 저녁의 편안함**, 마지막의 아주 작은 졸린 미소.

### 보이는 세계 (클립 공통)
```text
           N  [ 3연창 + 시스루 커튼, 유리에 빗방울 ]
   ┌───────────────────────────────────────┐
   │ [침대]                      [책상+의자] │   의자 등받이에 흰 수건
 W │                                       │ E
   │          (카메라: 방 중앙, 남동쪽)      │
   └──[입구 문]────────────────────────────┘
      S-W 모서리
```
- 의상(Scene Delta): 젖어 어깨가 짙어진 베이지 트렌치코트(끝까지 입고 있음), 안에 크림색 니트. 리본은 젖어 살짝 처짐.
- 머리: 업두 유지, 앞머리와 볼 옆 잔머리만 젖어 붙음.
- 카메라: MiniDV 핸드헬드(작은 흔들림·AF 헌팅), 실시간 모션, 슬로모 없음. 사운드: 빗소리·문소리·천 소리만, 음악 없음.

### Beat / Shot Plan
| 클립 | 비트 | 프레이밍 | 동작 (순서) | 시선 | 진입 → 이탈 상태 |
|---|---|---|---|---|---|
| A1 | 도착 | MS, 문 쪽을 봄 | 문 열고 들어옴 → 문 닫힘 → 멈춰 코트 소매의 물방울을 내려다봄 → 젖은 앞머리를 손끝으로 넘김 | 소매 → (손) | 문 밖 → 문 안쪽 1m, 오른손 앞머리 |
| A2 | 닦기 | MCU, 책상 쪽 | (A1에서 몸을 돌리는 동작에 컷) 의자 등받이 수건을 집음 → 앞머리·볼을 두드려 닦음 → 손끝으로 리본을 만져 젖었는지 확인 → 작게 숨 내쉼 | 수건 → 리본 쪽(눈만 위로) | 책상 앞, 수건 양손 → 수건 왼쪽 어깨에 걸침 |
| A3 | 창 | MS, 3/4 뒷모습 → 옆얼굴 | 창가로 두 걸음 → 빗방울 유리를 봄 → 아주 작은 졸린 미소 | 창밖 비 | 창 앞, 수건 어깨 → 같은 자세로 정지 |

생략(OMIT): 신발 벗기, 코트 벗기, 가방 내려놓기, 렌즈 응시. 실현: A1·A3 `SHOW`, A2 `SHOW`(수건은 두드리기만 — 문지르면 업두가 흐트러지는 위험).

### Intent Contract 초안 (A2 예시, A1·A3도 같은 형식)
```yaml
schema_version: 1
contract_id: intent_suan_rain_A2_v1
status: draft
source: {storyboard_id: sb_suan_rain_evening, revision: 1, sha256: <승인 시 계산>}
context:
  user_goal: 이수안의 사적인 비 오는 저녁을 관찰자 시점으로 보여준다.
  viewer_should_understand: 그녀는 비를 맞았고, 자기 상태를 혼자 확인하며 정리하고 있다.
  viewer_should_feel: 조용한 편안함, 엿보는 듯한 친밀감
  shot_purpose: 젖음의 증거 → 닦기 → 리본 확인으로 '돌봄의 순간'을 만든다
  rationale:
    no_lens_contact: 렌즈를 보면 관찰 다큐가 브이로그 출연으로 바뀐다 (ref #19 문법).
    pat_not_rub: 문지르기는 업두를 무너뜨려 DNA 앵커를 잃는다.
locked:
  ordered_events: [pick_up_towel, pat_bangs_and_cheek, touch_ribbon_check, small_exhale]
  gaze: {throughout: named_objects_only_towel_then_ribbon, lens: never}
  screen_direction: she_faces_desk_east_camera_left_side
  camera: {movement: handheld_static_operator, operator_visible: no}
  final_state: towel_over_left_shoulder_standing_at_desk
  omitted_events: [coat_removal, shoe_removal, hair_down]
  forbidden_additions: [lens_look, hair_untied, ribbon_removed, rubbing_hair]
creative_envelope:
  level: L1
  allowed: [lens_family, light_softness, depth_of_field, minidv_texture_strength]
  forbidden: [push_in, orbit, slow_motion]
feasibility: {decision: SHOW, rationale: 인물 1명, 한 자리, 손동작 세 개가 모두 큰 동작}
unresolved: [A1→A2 연결에 A1 마지막 프레임을 쓸지]
approval: {approved_by: <user>, approved_at: <승인 시>}
```
- A1 locks 요약: `[enter_door, door_closes, look_down_at_sleeve, brush_bangs]`, 시선 렌즈 never, 카메라 static handheld,
  omitted `[umbrella, bag_drop]`.
- A3 locks 요약: `[step_to_window, look_at_rain, tiny_sleepy_smile]`, 시선 창밖, 끝 상태 "창 앞에 정지, 미소 유지",
  forbidden `[turn_to_camera, open_window]`, 네거티브(ref #19 그대로): 벽이 창·문으로 변하지 않는다.

---

## B. 「잡혔다」 옥상 라디오 — ref #23

### Director Intent
해 질 무렵 빌라 옥상. 수안이 낡은 배터리 라디오를 켜 보지만 잡음뿐이다. 안테나를 뽑아 기울이다 노래가 잡히는 순간,
딱 한 번 카메라를 보며 "잡혔다." 그리고 의자에 앉아 노을을 본다. **작은 성공의 기쁨을 과장 없이**.

### 보이는 세계
- 장소 1곳: 옥상 콘크리트 난간(서쪽, 해가 지는 쪽), 빨랫줄, 화분 2개, 나무 테이블 위 라디오, 플라스틱 의자 1개.
- 라디오(외형 고정): 손바닥 두 개 크기의 크림색 플라스틱 몸체, 앞면 은색 그릴, 오른쪽 둥근 다이얼 1개, 위쪽 접이식 은색 안테나 1개.
- 의상: 오버사이즈 크림 카디건 + 연청 와이드 데님 + 흰 스니커즈. 리본 그대로.
- 빛: 클립을 지날수록 따뜻해짐(B1 옅은 금빛 → B3 짙은 주황). 사운드: 바람·먼 차 소리·라디오 잡음 → 원곡 멜로디. BGM 추가 없음.

### Beat / Shot Plan
| 클립 | 비트 | 프레이밍 | 동작 | 시선 | 진입 → 이탈 |
|---|---|---|---|---|---|
| B1 | 잡음 | MS, 테이블 옆 정면 3/4 | 라디오 다이얼을 천천히 돌림 → 잡음만 → 고개를 살짝 갸웃 | 라디오 | 서서 오른손 다이얼 → 같은 자세, 손 멈춤 |
| B2 | 잡힘 | MCU | (갸웃에서 이어 컷) 안테나를 끝까지 뽑음 → 천천히 기울임 → 잡음이 노래로 바뀜 → 손을 멈추고 **렌즈를 보며 "잡혔다."** → 다시 라디오로 시선 | 라디오 → 렌즈(대사 순간만) → 라디오 | 안테나 접힘 → 안테나 펼쳐 기울어진 채 정지 |
| B3 | 노을 | WS, 3/4 뒷모습 | 의자에 앉아 있음(앉는 과정은 컷 뒤로 숨김) → 노을을 봄 → 리본과 잔머리가 바람에 살짝 흔들림 | 노을 | 의자에 앉음 → 그대로 |

생략: 배터리 교체, 공구 수리, 라디오 들어 옮기기. B2→B3의 "앉는 동작"은 컷 뒤로 넘기므로 `OMIT`.

### Intent Contract 초안 (B2 — 이 세트에서 가장 중요한 시선 잠금)
```yaml
contract_id: intent_suan_radio_B2_v1
status: draft
source: {storyboard_id: sb_suan_rooftop_radio, revision: 1, sha256: <승인 시>}
context:
  user_goal: 작은 성공의 순간을 과장 없이 보여준다.
  viewer_should_understand: 안테나를 기울여서 노래가 잡혔다.
  viewer_should_feel: 소박한 기쁨, 그녀가 그 기쁨을 우리와 잠깐 나눔
  shot_purpose: 원인(안테나) → 결과(노래) → 한 번의 공유(렌즈+대사)
  rationale:
    single_lens_look: 렌즈 응시를 대사 순간 한 번으로 묶어야 '나눔'이 된다. 더 일찍 보면 포즈가 된다 (ref #23).
    cause_before_sound: 노래가 먼저 나오면 성공의 원인이 사라진다 (FAIL-011).
locked:
  ordered_events: [extend_antenna_fully, tilt_antenna_slowly, static_becomes_song, hand_stops, lens_look_says_japhyeotda, gaze_back_to_radio]
  gaze: {before_line: radio_only, during_line: brief_lens_contact, after_line: radio}
  screen_direction: radio_on_her_right_camera_left
  camera: {movement: static, framing: mcu}
  final_state: antenna_extended_tilted_hand_off_smiling_at_radio
  omitted_events: [battery_swap, tool_repair]
  forbidden_additions: [second_lens_look, dancing, lifting_radio, extra_dialogue]
creative_envelope:
  level: L1
  allowed: [lens_family, light_warmth, depth_of_field, background_clutter_detail]
  forbidden: [push_in, orbit, cut_within_clip]
feasibility: {decision: SHOW, rationale: 안테나는 큰 직선 동작 하나, 다이얼 미세조작을 피함 (FAIL-013)}
unresolved: [대사를 H3 오디오로 생성할지 후반에 녹음할지, 원곡 멜로디 출처]
```
- B1 locks: `[turn_dial_slowly, static_only, small_head_tilt]`, 시선 라디오만, 렌즈 never.
- B3 locks: `[seated_already, look_at_sunset, wind_moves_ribbon]`, 시선 노을, 카메라 static WS, forbidden `[stand_up, turn_to_camera]`.

---

## C. 「처음 끓여본 된장찌개」 — ref #63 (+ #67 대사 브릿지)

### Director Intent
밤 10시, 작은 부엌. 레시피를 보며 긴장한 수안 → 끓는 냄비 너머로 맛을 보는 얼굴 → 작은 상에서 "잘 먹겠습니다" 하고
한 숟갈, 눈을 감고 음미. **조리 과정은 한 번도 보여주지 않는다.** 김·불빛·한마디가 과정을 대신하고, 맛은 얼굴로 증명한다.

### 보이는 세계
- 부엌: 작은 원룸 주방, 가스레인지 1구 + 양은냄비(손잡이 2개), 도마 위 두부·애호박·대파(썰지 않은 상태), 레시피가 뜬 폰(세워둠, 화면 글자 비가독).
- 상: 같은 방 창가 쪽 낮은 원목 상, 뚝배기 한 그릇 + 밥 + 숟가락.
- 의상: 회색 맨투맨 + 소매 걷음, 앞치마 없음. 리본 그대로.
- 빛: 주방 형광등 + 레인지 주황 불빛 / 상은 스탠드 따뜻한 빛. 사운드: 보글보글, 환풍기, 숟가락 소리.

### Beat / Shot Plan
| 클립 | 비트 | 프레이밍 | 동작 | 시선 | 진입 → 이탈 |
|---|---|---|---|---|---|
| C1 | 준비 | MS, 조리대 정면 | 도마 앞에서 폰 레시피를 봄 → 재료를 봄 → 소매를 한 번 더 걷어 올리고 숨을 크게 들이쉼 | 폰 → 재료 | 재료 그대로 → 그대로(손만 소매) |
| C2 | 끓는 중 | CU, **냄비 너머 POV**(냄비 가장자리가 전경, 김이 화면을 가림) | 김 너머로 숟가락에 국물을 떠 후 불고 맛봄 → 눈이 커짐 → 작게 고개 끄덕임 | 숟가락 → 냄비 | 김 속 얼굴 → 끄덕임 정지 |
| C3 | 식사 | MCU, 상 맞은편 | 상 앞에 앉아 두 손 모으고 "잘 먹겠습니다." → 한 숟갈 → 눈 감고 음미 → 작게 웃음 | 그릇 → 눈 감음 → 그릇 | 앉음 → 숟가락 든 채 미소 |

생략(OMIT/IMPLY): 썰기, 재료 넣기, 그릇에 담기, 상으로 옮기기, 앉기. C1→C2는 `IMPLY`(김과 소리로 조리 중임을 알림),
C2→C3는 대사 브릿지로 건너뛰므로 `IMPLY`(담기·옮기기·앉기는 관객이 추론).

### Intent Contract 초안 (C2)
```yaml
contract_id: intent_suan_jjigae_C2_v1
status: draft
source: {storyboard_id: sb_suan_first_jjigae, revision: 1, sha256: <승인 시>}
context:
  user_goal: 서툰 첫 요리의 성공을 과정 없이 결과와 얼굴로 보여준다.
  viewer_should_understand: 찌개가 끓고 있고, 맛을 보니 생각보다 잘 됐다.
  viewer_should_feel: 조마조마 → 안도의 귀여움
  shot_purpose: 조리 과정을 대신하는 단 하나의 증거 컷
  rationale:
    pot_pov: 카메라를 냄비 자리에 두면 손 조리 동작 없이 '끓는 중'이 성립한다 (ref #63 석쇠 POV).
    no_process: 썰기·붓기 같은 손 과정은 렌더 붕괴 확률이 높다 (FAIL-013).
locked:
  ordered_events: [blow_on_spoon, taste, eyes_widen, small_nod]
  gaze: {throughout: spoon_then_pot, lens: never}
  screen_direction: camera_at_pot_position_looking_up_at_her
  camera: {movement: static, position: behind_pot_rim_low, foreground: pot_rim_and_steam}
  final_state: small_nod_spoon_lowered
  omitted_events: [chopping, adding_ingredients, pouring_into_bowl]
  forbidden_additions: [lens_look, adding_seasoning, burn_reaction]
creative_envelope:
  level: L2
  allowed: [lens_family, steam_density, rim_light_from_flame, depth_of_field]
  forbidden: [push_in, orbit]
feasibility: {decision: IMPLY, rationale: 김·불빛·소리로 조리 중임을 추론하게 한다}
unresolved: [H3가 '냄비 너머 낮은 POV'를 지키는지 — 러프 보드/샘플로 확인 필요]
```
- C1 locks: `[read_recipe_on_phone, look_at_ingredients, roll_sleeve, deep_breath]`, 렌즈 never, forbidden `[start_chopping]`.
- C3 locks: `[palms_together_says_jal_meokgetseumnida, one_spoonful, eyes_closed_savor, small_smile]`, 시선 렌즈 never,
  끝 상태 "숟가락 든 채 미소", forbidden `[talking_to_camera, second_line]`.

---

## D. 「말없이, 빛만」 — ref #11

### Director Intent
밤, 창가 책상. 수안이 손글씨 카드를 읽고 있다(내용은 보이지 않는다). 그녀는 거의 움직이지 않고, **빛이 바뀌며 감정이
넘어간다**: 참음 → 눈물이 고였다가 웃음이 새어 나옴 → 마지막에 짧게 렌즈를 본다. 대사 없음. 7초 싱글테이크 1클립.

### 보이는 세계
- 책상, 손에 든 작은 흰 카드(손글씨, 비가독). 프레임 안에 광원 없음(ref #11).
- 의상: 아이보리 블라우스. 리본 그대로. 화장 그대로(눈물 자국은 장면 변수).
- 사운드: 숨소리, 작은 훌쩍임, 새어 나오는 웃음 한 번. 음악 없음.

### Shot Plan (1클립)
| 순서 | 감정 | 빛 | 시선 |
|---|---|---|---|
| 1 | 참음: 아랫입술에 힘, 눈가에 눈물 고임 | 정면 부드러운 균등광 | 카드 |
| 2 | 넘어감: 눈물 한 줄이 흐르는데 입꼬리가 먼저 올라가며 작게 웃음 | 오른쪽 측광, 왼쪽 그늘 | 카드 → 아래 |
| 3 | 끝: 고개를 들어 **짧게 렌즈를 봄**, 젖은 눈으로 미소 | 따뜻한 촛불색 | 렌즈(마지막 순간만) |

프레이밍 CU 고정, 카메라 static(핸드헬드 질감 금지 — H3에서 "steady"가 이동을 막지 못한 기록이 있어 위험을 줄임).

### Intent Contract 초안 (D1)
```yaml
contract_id: intent_suan_silent_light_D1_v1
status: draft
source: {storyboard_id: sb_suan_silent_light, revision: 1, sha256: <승인 시>}
context:
  user_goal: 대사·움직임 없이 얼굴과 빛만으로 감정의 전환을 보여준다.
  viewer_should_understand: 카드가 그녀를 울렸고, 그 눈물은 슬픔이 아니라 고마움에 가깝다.
  viewer_should_feel: 먹먹함이 따뜻함으로 풀림
  shot_purpose: holding back → tears turn into a smile → one shared look
  rationale:
    late_lens_contact: 렌즈 응시를 마지막에 두어야 감정의 마침표가 된다. 일찍 보면 연기 시연이 된다.
    light_carries_change: 인물 동작을 줄여 얼굴 정체성 흔들림을 줄이고, 변화는 빛이 맡는다 (ref #11).
locked:
  ordered_events: [holding_back_tears_reading_card, tear_falls_while_smile_breaks, lift_head_brief_lens_look]
  gaze: {before_final: card_or_down, final_moment: brief_lens_contact}
  screen_direction: frontal_cu
  camera: {movement: static, framing: cu}
  final_state: wet_eyes_smiling_at_lens
  omitted_events: [card_text_visible, sobbing_breakdown]
  forbidden_additions: [table_slam, standing_up, wiping_with_sleeve_before_smile, visible_light_source]
creative_envelope:
  level: L2
  allowed: [light_sequence_front_side_warm, light_transition_softness, lens_family, depth_of_field]
  forbidden: [push_in, orbit, handheld_shake]
feasibility: {decision: SHOW, rationale: 1인 CU 1클립. 단, 눈물 인과와 빛 3단 전환의 H3 재현성은 미검증}
unresolved: [화면비 9:16 vs 16:9, H3가 한 클립 안 조명 전환을 따르는지(실패 시 SPLIT 2클립 + 빛은 컷에서 바꿈)]
```

---

## 3. 비교와 추천 순서

| 편 | 길이 | 클립 | 렌더 위험 | 이번에 시험되는 것 |
|---|---|---|---|---|
| B 옥상 라디오 | ~21초 | 3 | 중 (안테나 동작, 대사) | **시선 잠금(대사 순간 1회 렌즈)** — 새 방법론의 대표 사례 |
| A 비 오는 저녁 | ~21초 | 3 | 낮음 | 렌즈 never + 이름 붙은 시선 대상, 젖은 리본 연속성 |
| C 첫 된장찌개 | ~21초 | 3 | 중 (냄비 POV 구도) | IMPLY/OMIT로 과정 생략 |
| D 말없이, 빛만 | ~7초 | 1 | 높음 (눈물·빛 전환) | 한 클립 안 감정 전환 + 마지막 렌즈 |

추천: **B 먼저** (계약의 가치가 가장 잘 드러나고 실패 원인을 구분하기 쉽다) → A → C. D는 단독 실험으로 1샘플만.

## 4. 열린 결정 (사용자에게)

1. 4편 중 어떤 걸 진행할지, 아니면 하나를 더 다듬을지.
2. 화면비: 전부 16:9로 갈지, D(또는 전체)를 9:16 세로로 할지.
3. 대사 2곳("잡혔다.", "잘 먹겠습니다.")을 H3 오디오로 생성할지, 무음 렌더 후 따로 넣을지.
4. 클립 연결에 이전 클립 마지막 프레임을 참조로 쓸지(연속성↑, 정체성 드리프트 위험), 텍스트만으로 갈지.
5. 의상 Scene Delta(트렌치·카디건·맨투맨·블라우스) 그대로 좋은지.

## 5. 승인 후 진행 (아직 안 함)

1. 승인된 편의 콘티를 리비전 1로 고정 → 클립별 계약 JSON 작성(그 시점 스키마 기준) → 해시 계산 → 수신 확인(acknowledgement).
2. 필요하면 러프 보드(스틸) 1~2장으로 구도 확인 — 특히 C2 냄비 POV, B3 뒷모습 와이드.
3. 컴파일러 IR → 런타임 프롬프트 → `tools/video_intent_contract.py` 통과 → `--methodology intent-preserving-v1` 세션으로 WanGP 제출.
4. 렌더 리뷰: Intent Fidelity / Cinematography Gain 분리 채점, 실패 원인을 storyboard/compiler/renderer/edit으로 귀속.
