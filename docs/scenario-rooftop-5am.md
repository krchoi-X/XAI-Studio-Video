# 옥상, 새벽 5시 — 초보 마법사 브이로그

> **기획**: Somni (Muse) — 2026-10-02. 레퍼런스 코퍼스 #1–#78의
> 분석을 바탕으로 기획한 오리지널 시나리오.
>
> **기획 의도**: 레퍼런스가 78개까지 쌓이자 사용자가 "너무 많이
> 모은 게 문제"라며 정말 잘되는 문법 몇 개만으로 실제 기획을
> 만들어보라고 요청했다. 선정 기준은 증거 강도 + 독립 수렴
> 횟수. 이 기획은 특히 사용자가 #75에서 제기한 "내 영상은
> 컷 이어짐이 어색하다"는 문제를 구조로 해결하는 데 초점을
> 맞췄다 — 매 샷의 HANDOFF(미완료 동작)가 다음 샷의 시작이
> 되도록 설계했고, 카메라를 뒤에 고정해 축을 넘지 않게 했다
> (#77). 스펙터클 엔진은 #76의 T-39(정적 주인공 × 동적 공간),
> 2인 구조는 #70의 데드팬+리액터 엔진을 가져왔다.
>
> **연출 해석 (감독 노트, 2026-10-02)**: 제목이 테제다.
> "바람을 깨우는 여자"라는 제목은 곧 "그녀는 의도적으로 바람을
> 깨운다"는 해석이다. 그래서 민서는 숨겨진 마법사처럼 엄숙하게
> 팔을 뻗고, 자기가 부른 바람에 놀라지 않는다. 놀라는 것은
> 리액터 지훈의 몫. 이것은 이 시나리오의 해석이지 일반 원칙이
> 아니다 — 시나리오에 따라 캐릭터가 몰라서 놀라는 것도 맞다.

> **파이프라인 계약 (제작자 노트, 2026-10-02)**: 각본가(콘티를 쓰는 AI)
> → 감독(영상을 생성하는 AI) → 제작자(사용자, 최종 승인). 콘티를
> 쓰는 AI는 자기가 생각한 의도·감정을 콘티에 명시해야 한다. 그래야
> 생성하는 AI가 제멋대로 재해석하지 않고 같은 의미로 만든다. 매번
> 제작자가 일일이 의견을 줄 수 없으므로, 의미는 콘티에 내재되어야
> 한다. 그래서 이 콘티의 모든 샷에는 감정(EMOTION) 칸이 있다 —
> "이 캐릭터는 이 감정을 표현해야만 한다"는 각본가의 지시다.
>
> **피벗 (제작자 노트, 2026-10-02)**: S3 생성에서 그녀가 카메라를
> 보고 웃어버렸다. 진지함이 깨진 것이다. 리테이크 대신 스토리를
> 고쳤다 — 그녀는 애초에 초보 마법사였다. 진지하게 바람을
> 불어일으키려 하지만 실수하고 들뜨는 브이로그. 푸티지를 이기려
> 하지 마라. 생성물이 준 것을 스토리가 받아먹게 하라. 이것이
> 진짜 감독의 일이다.

## 0. 선정된 문법 6개 (왜 이것들인가)

78개 레퍼런스에서 증거 강도 + 독립 수렴 횟수로 추렸다. 나머지는
일부러 안 쓴다.

| # | 문법 | 출처 | 왜 선정 |
|---|------|------|---------|
| 1 | P-15 역할 분리 | #4·#9·#16·#74 | 레퍼런스마다 1역할. 욕심내면 다 깨짐 |
| 2 | T-39 정적 주인공 × 동적 공간 | #76 (HIGH) | AI는 무술 못 그리고 유체·바람은 잘 그림. 스펙터클을 몸에서 떼어라 |
| 3 | T-33 관성 연결 | #47·#75·#76 | 컷은 진행 중인 동작에 실어 보낸다. 포즈로 멈추면 다음 컷이 새 우주 |
| 4 | P-30 소품 상태 원장 | #66·#71·#73·#77·#78 | 소품은 씬마다 상태를 다시 선언해야 carryover됨 |
| 5 | P-21 실패 카탈로그 네거티브 | #4·#19·#24·#25·#74 | 목격된 실패의 이름을 적는 게 방지의 시작 |
| 6 | INTENT (샷에게 일을 시켜라) | #78 + Necessity Test | 샷마다 목적 1개, 한 샷에 한 비트만 |

## 1. 시나리오

**로그라인**: 새벽 5시 옥상. 민서는 진지하게 바람을 깨우려 한다.
문제는 그녀가 초보다. 비장한 의식과 터져버리는 웃음 사이의
줄타기. 지훈은 그걸 핸드폰으로 찍는다.

**인물** (2인: 데드팬 + 리액터 — #70의 엔진)
- 민서 (A): 자칭 마법사, 실은 초보. 비장하게 의식을 치르려 하지만
  바람이 일어나면 신나서 카메라를 보고 웃어버림. "진지한 척"과
  "들뜸" 사이의 줄타기가 이 작품의 코미디 엔진.
  긴 흑발, 흰 셔츠, 청바지
- 지훈 (B): 친구. 핸드폰으로 촬영 (다이제틱 카메라). 리액터.
  놀라는 것은 지훈의 몫

**6비트 × 5초 = 30초**

| 비트 | 시간 | INTENT | 한 줄 |
|------|------|--------|-------|
| 1 | 0–5s | 비장한 시작 | 새벽 옥상, 민서는 진짜 마법사인 척 의식을 시작 |
| 2 | 5–10s | 소환 (애써 태연) | 손바닥을 펼치는 순간 셔츠 수평+비둘기 폭등. 민서는 태연한 척하지만 입꼬리가 올라감 |
| 3 | 10–15s | 터져버림 | 바람이 세지자 참았던 웃음이 터져 카메라를 봐버림 |
| 4 | 15–20s | 진지한 척 재시도 | 숨 의식으로 분위기 수습 시도. 웃음이 샐 듯 말 듯 |
| 5 | 20–25s | 완전히 무너짐 | 깃털이 렌즈에 붙자 빵 터짐. 마법사 코스프레 종료 |
| 6 | 25–30s | 쿨한 척 퇴장 | 비장한 뒷모습인 척 걸어가지만 어깨가 들썩임 |

## 2. 콘티 (컷 구성)

각 샷은 #78 포맷: INTENT → ACTION → FRAME → CAMERA →
CONTINUITY(시작→종료 상태, 다음 샷으로 넘기는 것) → NEGATIVES.

### Shot 1 (0–5s) — 확립

- **감정 (EMOTION)**: 민서 — 비장한 결의. "나는 진짜 마법사"라는
  얼굴로 의식을 시작. 아직은 진지함이 유지됨.
- **INTENT**: 장소와 정적을 확립. "아무 일도 없는 새벽"을 보여줘야
  뒤의 반응이 폭발한다
- **ACTION**: 민서가 옥상 난간 앞에 등을 보이고 서 있다. 바람 없음.
  지훈 (화면 밖): "야, 바람 한 점 없는데?" 민서가 오른손 검지를
  천천히 들어 올린다 (5초 끝까지 다 안 올라감 — 다음 샷으로 넘김)
- **FRAME**: 와이드. 옥상 전경 + 먼 도시 + 새벽 하늘
- **CAMERA**: 핸드헬드, 미세한 흔들림. 지훈의 폰이라는 게 느껴지게
- **CONTINUITY**: 시작=정적, 양손 내림 → 종료=검지 상승 중 (미완료)
- **HANDOFF → S2**: 올라가는 중인 검지
- **NEGATIVES**: 바람에 흔들리는 물체 없음 (아직). 민서가 카메라를
  보지 않음. 시네마틱 슬로모 금지

### Shot 2 (5–10s) — 첫 반응

- **감정 (EMOTION)**: 민서 — 애써 태연한 척. 속으로는 "됐다!"라고
  외치지만 겉으로는 평온을 유지하려 애씀. 입꼬리가 살짝 올라감.
  지훈 — 당혹과 흥분 (카메라 흔들림으로 표현).
- **INTENT**: 작은 동작 → 초대형 결과의 첫 증명
- **ACTION**: 검지 클로즈업에서 시작 → 손가락이 완전히 펴지는 순간,
  빨랫줄의 셔츠 3장이 동시에 수평으로 펄럭임. 물탱크에서 비둘기
  수십 마리 폭등. 지훈: "어어?!" 카메라가 크게 흔들림 (T-18)
- **FRAME**: 검지 극클로즈업 → 빨랫줄 미디엄으로 점프 (액션 매치)
- **CAMERA**: 흔들림은 원인이 있어야 (지훈의 놀람). 흔들린 뒤
  빨랫줄로 재프레이밍
- **CONTINUITY**: 시작=검지 상승 중 (S1에서 인계) → 종료=셔츠
  펄럭임 지속, 비둘기 상승 중
- **HANDOFF → S3**: 펄럭이는 셔츠 + 상승하는 비둘기
- **NEGATIVES**: 민서의 표정 변화 없음 (차분 유지). 셔츠가
  빨랫줄에서 떨어지지 않음. 비둘기가 민서에게 달려들지 않음

### Shot 3 (10–15s) — 증폭

- **감정 (EMOTION)**: 민서 — 터져버린 웃음. 참았던 게 터져서
  카메라를 보고 웃어버림. 곧 수습하려 하지만 이미 늦음.
  지훈 — 덩달아 터지는 웃음.
- **INTENT**: 반응의 스케일 업. 도시는 이제 민서에게 반응하는 중
- **ACTION**: 민서가 천천히 고개를 돌림 (3/4 측면). 아래층 어닝이
  돛처럼 부풀어 오름. 비닐봉지 2개가 소용돌이치며 상승. 지훈이
  웃음을 터뜨리고 카메라가 웃음 때문에 흔들림 (T-18 정석)
- **FRAME**: 민서 3/4 미디엄 → 어닝 와이드로 틸트다운
- **CAMERA**: 고개 돌림을 따라가다 아래로 틸트. 웃음 흔들림
- **CONTINUITY**: 시작=셔츠 펄럭임 (S2에서 인계) → 종료=어닝
  팽창 중, 비닐봉지 상승 중
- **HANDOFF → S4**: 부풀어 오른 어닝 (바람의 증거)
- **NEGATIVES**: 어닝이 찢어지지 않음. 민서가 포즈를 취하지 않음.
  정면을 보고 스킬 쓰듯 찍지 않음 (T-39 금기)

### Shot 4 (15–20s) — 리셋 (콘티 변경, 2026-10-02)

- **감정 (EMOTION)**: 민서 — 진지한 척 재시도. 눈을 감고 심호흡으로
  분위기를 되찾으려 함. 거의 평온을 되찾지만 입꼬리가 살짝 샐 듯.
  지훈 — "또 시작이네"라는 표정.
- **INTENT**: S3의 폭소와 S5의 무너짐을 잇는 다리. 바람이 잦아들고
  햇살이 비치며 잠시 평온이 돌아오는 비트
- **ACTION**: 민서 미디엄. 눈을 감고 팔을 내린 명상 자세로 깊게
  숨을 들이쉼. 바람이 잦아들며 머리카락이 가라앉고, 구름이 갈라지며
  따뜻한 햇살이 얼굴에 비침
- **FRAME**: 미디엄 고정
- **CAMERA**: 고정. 햇살이 강해지는 순간 미세한 노출 변화
- **CONTINUITY**: 시작=S3의 폭소·거센 바람 → 종료=바람 잦아듦,
  햇살 지속, 평온 (불안정한)
- **HANDOFF → S5**: 잦아든 바람, 햇살 — 고요해진 세계에 떨어지는 깃털
- **NEGATIVES**: 민서가 완전히 웃지 않음 (샐 듯 말 듯). 갑자기
  낮이 되지 않음. 렌즈 플레어 남발 금지

### Shot 5 (20–25s) — 코미디 정점

- **감정 (EMOTION)**: 민서 — 완전히 무너짐. 깃털이 렌즈에
  붙자 빵 터져서 더 이상 마법사 코스프레 불가. 지훈 — "야 이거
  내 폰에..."라며 같이 폭소.
- **INTENT**: 긴장 해제. 거대함 → 사소함으로의 반전
- **ACTION**: 민서가 손을 천천히 내림. 모든 바람이 멎음 (정적).
  1초 정적 후, 깃털 하나가 화면 위에서 떨어져 지훈의 폰 렌즈에
  착지. 지훈 클로즈업 (사팔뜨기): "야 이거 내 폰에..."
- **FRAME**: 민서 미디엄 (손 내림) → 렌즈에 떨어지는 깃털
  극클로즈업 → 지훈 얼굴 클로즈업
- **CAMERA**: 정적 구간은 고정. 깃털 낙하는 렌즈 POV
- **CONTINUITY**: 시작=햇살 (S4에서 인계) → 종료=깃털이 렌즈에
  (소품 원장에 신규 등록)
- **HANDOFF → S6**: 렌즈에 붙은 깃털
- **NEGATIVES**: 깃털이 여러 개가 되지 않음. 민서가 사라지지 않음.
  슬로모로 깃털을 과장하지 않음

### Shot 6 (25–30s) — 북엔드

- **감정 (EMOTION)**: 민서 — 쿨한 척 퇴장. "흥, 마법사는
  원래 이런 거야"라는 뒷모습이지만 어깨가 들썩임. 지훈 —
  "...내일도 와?" (웃음 참는 목소리)
- **INTENT**: 원 닫기. 스펙터클 후의 정적이 완결감 (T-34)
- **ACTION**: Shot 1과 같은 구도. 민서가 천천히 걸어감 (뒷모습).
  화면 구석에 렌즈의 깃털이 살짝 보임. 지훈: "...내일도 와?"
  민서 대답 없음. Cut to black
- **FRAME**: Shot 1과 동일한 와이드
- **CAMERA**: 고정. 움직임 없음
- **CONTINUITY**: 시작=깃털이 렌즈에 (S5에서 인계) → 종료=민서
  퇴장, 깃털만 잔류
- **NEGATIVES**: 민서가 돌아보지 않음. 해가 완전히 뜨지 않음.
  자막·엔딩 크레딧 없음

## 3. 소품 상태 원장 (P-30)

| 소품 | S1 | S2 | S3 | S4 | S5 | S6 |
|------|----|----|----|----|----|----|
| 빨랫줄 셔츠 3장 | 정적 | 수평 펄럭임 | 펄럭임 지속 | — | — | — |
| 비둘기 | 물탱크에 | 폭등 중 | 상승 | — | — | — |
| 어닝 | 접힘 | — | 돛처럼 팽창 | 팽창 유지 | — | — |
| 비닐봉지 2개 | — | — | 소용돌이 상승 | — | — | — |
| 입김 | — | — | — | 소멸 중 | — | — |
| 깃털 1개 | — | — | — | — | 렌즈에 착지 | 렌즈에 잔류 |
| 지훈의 폰 | 촬영 중 | 흔들림 | 웃음 흔들림 | 고정 | 깃털 받음 | 고정 |

## 4. 생성 프롬프트 (영어, I2V용 — 모션만 프롬프트)

> #78 T2V/I2V 구분: 이미지 레퍼런스가 캐릭터·구도를 이미 가지므로
> 프롬프트는 모션·카메라·연속성에 집중. 캐릭터 묘사는 LOCK 한 줄로.

**공통 캐릭터 LOCK** (전 샷): "The same young Korean woman
throughout: long black hair, white shirt, jeans. Calm, restrained
expression, minimal movement. Her male friend films on a phone
(diegetic handheld camera)."

**공통 네거티브** (P-21 카탈로그형 — 목격된 실패들):
"no extra people, no duplicated characters, no costume change,
no frontal hero pose, no slow motion, no lens flare abuse,
no neon effects, no subtitles, no cinematic stabilization"

### Prompt S1 (리테이크 — 마법사 디렉션)
"Handheld phone footage, dawn rooftop in Seoul, wide shot from
behind her. She slowly extends her right arm forward with grave
deliberation, fingers spreading open one by one into a conjuring
gesture, as if gathering the wind itself. Ritualistic, solemn,
unhurried. A male voice off-camera (Korean): '야, 바람 한 점
없는데?' Everything else frozen: no wind yet, hair and clothes
motionless. Subtle handheld shake. Cold blue dawn light."

### Prompt S2 (리테이크 — 마법사 디렉션)
"Keep the identical camera framing. The instant her palm opens
fully: a sudden gust — three shirts on the laundry line snap
horizontal simultaneously, dozens of pigeons burst upward from
the water tank. She does not react at all: eyes calm, expression
serene and commanding, arm holding the conjuring pose perfectly
still. She summoned this wind and finds it entirely expected.
The camera jolts once (the filmer gasps) then steadies."

### Prompt S3
"She slowly turns her head to 3/4 profile. As her head turns,
a shop awning below billows upward like a sail, two plastic bags
spiral into the air. The camera tilts down to follow, shaking
with the filmer's laughter. She never poses, never faces the
camera frontally."

### Prompt S4
"Close-up of her face. She exhales slowly — visible breath in
the cold dawn air. Clouds part and a single shaft of sunrise
light strikes the rooftop. Her hair lifts slightly. Slow push-in
timed to her breath. A quiet male voice: '너 뭐야...' (Korean).
No lens flare abuse, dawn light preserved."

### Prompt S5
"She slowly lowers her hand. All wind stops — one full second
of stillness. Then a single feather drifts down from above and
lands on the phone's lens. Cut to extreme close-up of the
feather on the lens, then the filmer's cross-eyed face (Korean):
'야 이거 내 폰에...' Exactly one feather, no slow motion."

### Prompt S6
"Same wide composition as the opening shot. She walks slowly
away from camera across the rooftop, back view. A feather is
faintly visible at the edge of the lens. Male voice (Korean):
'...내일도 와?' She does not turn around, does not answer.
Cut to black. No subtitles, no credits."

## 5. 이 기획이 쓰는 문법 체크리스트

- [ ] P-15: 레퍼런스마다 1역할 (인물 이미지=외모, 영상=바람·구름 모션)
- [ ] T-39: 민서는 작은 동작만, 도시는 거대하게 반응
- [ ] T-33: 매 샷 HANDOFF가 다음 샷의 시작 (검지 상승 중→완료→고개→숨→손 내림)
- [ ] P-30: 소품 원장 7행 추적, 깃털은 S5에 신규 등록
- [ ] P-21: 네거티브 8항, 전부 목격된 실패
- [ ] INTENT: 샷마다 목적 1개, 한 샷에 한 비트
