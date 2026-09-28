# MeiGen Top 20 — Cases 19–21 (15섹션)

작업 지시: XAI-Studio-Video 재사용 가능한 구조적 패턴 추출. 인기 ≠ 품질.
증거 기반: frame-observed / prompt-derived / author-described / text-guide / inference.
추론은 production rule로 승격하지 않는다. SKILL.md 확정 금지.
본 파일은 meigen-top20.md (Cases 01–10)의 속편. 해당 파일은 건드리지 않음.

순위 표기 주의: MeiGen Popular 탭은 고정 순위가 아니라 스크롤·시간에 따라 re-sort되는 피드임이 검증됨 (2026-09-26 21:14 KST 스냅샷 기준). 아래 rank는 해당 스냅샷 기준이며 유동적.

공통 주제: 세 케이스 모두 스토리보드/프레젠테이션 '컨테이너' 구조를 프롬프트에 포함. 컨테이너 렌더 여부가 3가지로 갈림 — 유지(Case 20) / 부분 붕괴(Case 19) / 완전 붕괴(Case 21). 비교는 각 케이스 12번 A항에 증거 기반으로 정리.

---

## Case 19 — Latte "Kitchen Hunt: baker NUO vs cockroach ROCKY" [snapshot rank 8]

### 1. Source
- URL: https://www.meigen.ai/video/2050154597340287143
- creator: Latte (@0xbisc)
- model: Seedance (MeiGen 배지)
- duration: 17.70초 실측 (531프레임/30fps/1080x1080 정사각형 1:1). 프롬프트 타임라인은 0:00–0:15까지만 기술 — 실측이 2.7초 김
- popularity: snapshot rank 8, 123 likes (조회수 미표시)

### 2. Evidence basis
- prompt-derived (2-part 프롬프트 전문 확보)
- frame-observed (초당 1프레임 18장 + 개별 프레임. 애니메이션 구간/디자인 시트 구간/스플릿 전환/엔딩 로고 확인)
- author-described (Seedance 배지)
- inference: Why it may work B항
- 오디오(SFX·휘파람·립싱크)는 프레임으로 검증 불가 — prompt-derived로만 기록

### 3. Prompt structure
2-part (이미지 레퍼런스 프롬프트 + 비디오 프롬프트). 구조 분해:

PART 1 (Image · 1 — 캐릭터 디자인 시트):
- subject block: 인간 제빵사와 의인화된 바퀴벌레, 나란히 배치
- material spec block: 제빵사 — soft subsurface scattering skin, stylized denim textures / 바퀴벌레 — glossy segmented chitinous exoskeleton, sharp specular highlights
- presentation block: primary full-body render + 3개 표정 행 + dynamic action poses
- layout block: structured grid, sans-serif typography, 하단 texture close-up callouts
- light/camera block: soft neutral studio lighting, flat orthographic layout, sharp focus throughout
- style tags (bulleted): Style / Key elements / Lighting / Camera

PART 2 (Video · 2 — 비디오 프롬프트):
- SUBJECTS block (2인): Pastry Chef — adult, chef uniform, ground level, 대형 스테인리스 케이크 주걱으로 카운터 edge를 따라 추격, controlled swings → uncontrolled strikes로 격화 (character reference @ image1) / Cockroach — small, 항상 카운터 위, low-position rapid crawling, 오른쪽으로 단방향 전진 + 좌우 dodge·급정지·방향전환 (character reference @ image2)
- ENVIRONMENT block: home kitchen, continuous long countertop with clear depth, 카운터 위 일반 주방 오브젝트, "Window is closed"
- STYLE block: Realistic 3D animation, strong physical feedback
- CAMERA DETAILS block: POV = 바퀴벌레 뒤를 바짝 따르는 close-following rear perspective, low angle forward; 공격은 위·측면에서 press in; 단 한 번의 정면 대치만 예외
- Timeline (6비트, 각 비트 = 샷 스펙 + 액션 + SFX):
  - 0:00–0:02: Medium shot 35mm slow push-in. 셰프가 카운터 왼쪽에서 가볍게 휘파람 불며 정리, "mouth movement perfectly synchronized with the whistling sound (lip-sync)". SFX: whistling (only present in this phase), subtle crawling
  - 0:02–0:04: Low-angle tracking 28mm forward. 바퀴벌레 가속+회피, 셰프 돌진+타격 시작, "the whistling sound completely stops the moment the action begins". SFX: footsteps, heavy metal impact
  - 0:04–0:10: POV 20mm close-follow high-speed. 카메라는 뒤돌아보지 않고 전진, serpentine dodging, 타격이 주변 오브젝트에 accidental하게 명중하며 혼돈 상태 생성·유지. SFX: continuous heavy impacts, object collisions
  - 0:10–0:12: POV slows. 창문 앞 카운터에서 바퀴벌레가 멈춰 정면으로 셰프를 마주보고 smug smile + provocative gesture. SFX: brief pause
  - 0:12–0:14: Medium shot push-in. 셰프가 주걱을 투척, 빗나가 창문 유리를 깨뜨림, 바퀴벌레가 깨진 틈으로 탈출. SFX: air slice, glass shatter
  - 0:14–0:15: Wide static. 셰프 빈손, 카운터 전체가 엉망 ("all struck objects remain scattered, overturned, and dirty"), 잠시 정지 후 breakdown scream. SFX: silence → breakdown scream
- 없음: negative constraints, aspect ratio 지정, dialogue

### 4. Subject / Character state
- identity lock: 이미지 레퍼런스 (@ image1 = 셰프, @ image2 = 바퀴벌레). 단 PART 1은 단일 이미지로 기술되어 image2의 실체가 모호 — 할당 불일치 (prompt-derived)
- 캐릭터명: 시트에는 "NUO THE BAKER" / "ROCKY THE COCKROACH" (frame-observed). 비디오 프롬프트는 "Pastry Chef"/"Cockroach"로만 호칭 — 명칭 불일치
- wardrobe lock: 셰프 유니폼+토크 (유지됨 ✓)
- prop lock: 대형 스테인리스 케이크 주걱 — 0:12–0:14 투척 후 "no tool remains in hand" (프롭 상태 전이 명시, 렌더 확인 ✓)
- character count: 2
- role separation: 추격자(셰프) vs 도망자·조롱자(바퀴벌레) — 명확
- gaze assignment: 0:10–0:12 "turns to face the chef directly" — 바퀴벌레의 정면 응시 비트 (렌더 확인 ✓)

### 5. Camera / Shot design
- multi-shot: 6비트
- explicit cuts: 없음 (비트 경계만)
- camera role: 바퀴벌레 뒤를 따르는 주관적 추격 카메라 — 카메라=도망자의 시점/호흡에 동조
- lens spec per beat: 35mm → 28mm → 20mm (광각으로 격화)
- framing progression: medium push-in → low-angle tracking → POV high-speed → POV slow → medium push-in → wide static (정지)
- "the camera continuously advances without looking back" — 카메라 움직임에 서사 태도 부여
- container 구간: 디자인 시트는 정지 풀프레임으로 삽입 (카메라 움직임 없음)

### 6. Spatial / Continuity
사용 채널: identity (시트 레퍼런스 — 강함), location (단일 주방 카운터 — 강함, 유지됨 ✓), prop state (명시적 상태 유지 지시 — "gradually creating and maintaining a chaotic state", "all struck objects remain scattered, overturned, and dirty" — 렌더에서 엉망 카운터 확인 ✓), tone (Pixar풍 3D — 유지됨 ✓).
선언-충돌 관찰 (frame-observed): ENVIRONMENT의 "Window is closed" vs 0:12–0:14 비트의 창문 파손 — 렌더는 파손을 따름 (깨진 창문 확인 ✓). 구체적 후행 비트 지시가 일반 환경 선언을 덮음.

### 7. Action grammar
- escalation arc: controlled swings → fully uncontrolled strikes → breakdown scream — 격화 곡선이 프롬프트에 명시
- chase grammar: accelerate / dodge / abrupt stop / direction change — 도망자의 이동 어휘가 비트마다 지정
- comedic reversal: smug smile + provocative gesture (0:10–0:12) → 투척 빗나감 → 유리 파손 → 빈손 (0:12–0:15) — 조롱-역전 구조
- anticipation → contact → consequence: "each strike accidentally and realistically hitting objects along the way" — 타격마다 접촉 결과가 오브젝트에 기록됨
- chaos-state maintenance: 혼돈을 일회성 이펙트가 아니라 유지해야 할 상태로 지정 — 상태 지속 지시
- action density: 높음

### 8. Reference usage
- @ image1 = 셰프 캐릭터 레퍼런스 (prompt-assigned), @ image2 = 바퀴벌레 레퍼런스 (PART 1 단일 이미지 기술과 불일치 — 모호)
- **role bleed (frame-observed)**: 레퍼런스로 지정된 디자인 시트가 캐릭터 가이드 역할을 넘어 풀프레임 정지 컷어웨이로 직접 렌더됨 (약 2초, 시트 전체가 정지 이미지로 삽입). 경계에는 수직 split-wipe 전환 프레임 존재. Reference Role Separation 패턴과 대비되는 사례 — 레퍼런스가 콘텐츠가 됨

### 9. Audio / Dialogue
- dialogue: 없음
- SFX: 비트별 6종 지정 (위 §3 참조)
- audio-action binding (prompt-derived): "the whistling sound completely stops the moment the action begins" — 액션 시작 비트에 오디오 상태 변화를 바인딩. 휘파람 구간 한정 립싱크 ("mouth movement perfectly synchronized with the whistling sound")
- beat sync: SFX가 비트 경계에 1:1 매핑
- 프레임으로 오디오 검증 불가 — 전부 prompt-derived

### 10. Failure prevention
명시적 네거티브 없음. 관찰된 현상 (frame-observed):
- 시트 내 마이크로 타이포그래피는 판독 불가 수준 (text seep 경미 — 헤더 "NUO THE BAKER"/"ROCKY THE COCKROACH"는 판독 가능)
- 애니메이션 구간 해부학 파탄 없음 (스틸 한계 내)
- "Window is closed" 선언 vs 파손 비트 — 모델은 후행 구체 비트를 따름 (실패라기보다 우선순위 관찰)

### 11. Control Levels
- Hard Lock: 6비트 타임라인, 2인 역할 분리, 바퀴벌레 추격 POV, 비트별 SFX, 프롭 상태 전이 (투척 후 빈손)
- Soft Guidance: Pixar풍 3D, strong physical feedback, 비트별 렌즈 수치, 휘파람-립싱크
- Creative Freedom: 추격 디테일, 표정, 혼돈 연출의 구체상

### 12. Why it may work
A. Evidence-backed:
- 6비트의 순서와 상대 길이가 렌더에서 유지됨. 시트 인터루드(약 2초)로 전체가 ~1–2초 뒤로 밀렸으나 비트 순서는 지킴 (per-second 프레임 대조)
- 2인 역할 분리(추격자/도망자)가 전 구간 유지됨. 프롭 상태 전이(주걱 투척→빈손) 렌더 확인
- chaos 상태 유지 지시가 코미디 아크(조롱→빗나감→엉망→절규)를 떠받침
- 컨테이너 3-way 비교 (frame-observed):
  - Case 19 = 부분 붕괴: 디자인 시트가 약 2초간 풀프레임 정지 컷어웨이로 삽입되고 경계는 split-wipe. 나머지 구간은 순수 애니메이션. 컨테이너가 버려지지도, 고정되지도 않음
  - Case 20 = 유지: 9패널 스토리보드 그리드가 하단 스트립으로 전 구간 고정. 1920x2160 = 16:9 상단(시네마틱) + 16:9 하단(그리드) 스택
  - Case 21 = 완전 붕괴: 2x5 그리드·씬 번호·캡션 전무, 광고 본편만 렌더 (Case 07과 동일 영상 — 재관측)

B. Inference:
- 추격+조롱-역전 코미디는 검증된 애니메이션 원형. Pixar풍 3D는 현 모델 세대의 강점 영역으로 보임
- "휘파람이 액션 시작과 동시에 완전히 멈춤" 같은 오디오-액션 바인딩은 비트 경계를 모델에게 명확히 전달 (Case 02의 "손이 움직일 때마다" 트리거 바인딩과 동형)
- 시트 인터루드는 프롬프트에 없는 삽입 — 모델이 레퍼런스 이미지를 '보여줄 것'으로 해석한 결과로 보임 (가설)

### 13. Popularity signal
- snapshot rank: 8 / likes: 123
- likely_driver: visual_subject (Pixar풍 캐릭터 애니메이션 — 갤러리 썸네일 매력), novelty (디자인 시트 컷어웨이 삽입이라는 이례적 구성), unknown (prompt_structure — 인과 근거 없음)
- 판단: 인기를 프롬프트 구조 품질과 연결할 근거 없음. 렌더 결과물(캐릭터+개그)의 힘일 가능성

### 14. Relation to existing XAI-Studio patterns
- Trailer Montage: 강화 (6비트/17.7초 밀도)
- Continuous Action: 강화 (추격전 단일 액션)
- Reference Role Separation: 대비 사례 — role bleed (레퍼런스→콘텐츠). 패턴의 경계를 보여주는 음성 증거
- Hard Lock/Soft Guidance/Creative Freedom: 강화
- Case 02의 트리거 바인딩: 강화 (whistle-stop은 오디오 버전의 트리거 바인딩)
- Case 10의 conservation law와 공명: 프롭 상태 전이(주걱 투척→빈손)의 명시

### 15. Candidate contribution
- new model-behavior note 후보: **container-content congruence 가설** — 컨테이너가 서사 콘텐츠 자체를 담고 있으면(스토리보드 패널 = 씬 묘사) 유지되고, 순수 메타 포장(프레젠테이션 보드·테두리·번호)이면 버려지며, 레퍼런스성 컨테이너(캐릭터 시트)는 컷어웨이로 삽입될 수 있음. 3-case 비교 기반 가설이며 A/B 테스트 필요 — production rule 승격 금지
- 그 외: reinforces existing patterns (Trailer Montage, Continuous Action, trigger binding)

---

## Case 20 — Sharon Riley "b-Smooth 9-panel storyboard + luxury skincare commercial" [snapshot rank 9]

### 1. Source
- URL: https://www.meigen.ai/video/2064650854570025026
- creator: Sharon Riley (@Just_sharon7)
- model: Seedance (MeiGen 배지)
- duration: 15.0초 실측 (899프레임/60fps/1920x2160). 1920x2160 = 8:9 — 프롬프트 지정 "vertical 9:16"과 불일치 (아래 §5·§10 참조)
- popularity: snapshot rank 9, 130 likes (조회수 미표시)

### 2. Evidence basis
- prompt-derived (2-part 프롬프트 전문 확보 — 정본 verbatim 대조 완료)
- frame-observed (초당 1프레임 15장 + 개별 프레임. 상단 시네마틱/하단 그리드 스플릿 구조, 9씬 시간 순서, 제품 텍스트 렌더 확인)
- author-described (Seedance 배지)
- inference: Why it may work B항
- 오디오(대사 2줄)는 프레임으로 검증 불가 — prompt-derived로만 기록

### 3. Prompt structure
2-part (스토리보드 인포그래픽 프롬프트 + 비디오 프롬프트). 구조 분해:

PART 1 (Image · 1 — storyboard infographic prompt):
- format block: wide-format 9-panel, 16:9 canvas, clean 3x3 grid, numbered panels (01–09), bold scene titles, 패널당 2–3 short bullet points (camera angle / action / mood)
- Visual Style bullets (10개): Luxury skincare commercial / Warm dark brown → deep amber gradient / Black accents + baby-pink highlights / Golden rim lighting / Korean-Western beauty campaign aesthetic / Shallow DOF creamy bokeh / Ultra-realistic skin textures / Premium fashion editorial / High-end beauty cinematography / Minimalist luxury layout
- Panel 01–09 (각 = 번호 + "제목" + 3 bullets):
  - 01 "Product Emerges" (extreme macro, aloe-vera pump bottle, fish-eye) → 02 "Luxury Reveal" (rotating beauty shot) → 03 "First Touch" (펌프→크림) → 04 "Silk Application" (이마·볼 도포) → 05 "Glow Transformation" (흡수·광채) → 06 "Product Ritual" (3제품 진열: b-Straighten PREP WASH / b-Smooth / STEP 3 POST TREATMENT) → 07 "Sensory Texture" (크림 pour macro) → 08 "Empowered Beauty" (히어로 미디엄샷, eye contact) → 09 "Final Hero Frame" (전 제품+블러 모델)
- Character Reference block: 24-year-old Western woman — flawless luminous skin, light hazel-green eyes, sleek wet-look blonde low slick bun, baby-pink luxury dress
- Overall Design bullets (11개): presentation / white panel borders / numbered scenes / bold titles / production notes / warm palette / pitch-deck quality / campaign board / hyper-realistic / 8K / smooth storytelling
- 없음: negative constraints, 카메라 수치

PART 2 (Video · 2 — video generation prompt):
- format declaration: "Create a premium luxury skincare commercial in vertical 9:16 format"
- style paragraph: ultra-realistic beauty cinematography + editorial fashion + product videography, warm chocolate-amber gradient, baby-pink accents, shallow DOF, "Korean-Western beauty advertising aesthetics"
- SCENE 1–9 (각 = 타임스탬프 + [카메라/액션] + "Clean cut" 전환 선언):
  - SCENE 1 (0:00–0:02) PRODUCT EMERGES — extreme macro, bottle emerges from darkness, slow push-in, fish-eye edges
  - SCENE 2 (0:02–0:03) LUXURY REVEAL — rotating bottle, camera slides around
  - SCENE 3 (0:03–0:05) FIRST TOUCH — pump→palm, macro texture, focus alternates nozzle/cream
  - SCENE 4 (0:05–0:07) SILK APPLICATION — forehead/cheeks/jawline, camera floats. Soft dialogue: "This feels like silk on my skin..."
  - SCENE 5 (0:07–0:08) GLOW TRANSFORMATION — extreme close-up, push toward eyes, "preserving realistic pores and texture"
  - SCENE 6 (0:08–0:10) PRODUCT RITUAL — 3제품 tabletop lineup, slow slide
  - SCENE 7 (0:10–0:11) SENSORY TEXTURE — extreme macro slow-motion pour
  - SCENE 8 (0:11–0:13) EMPOWERED BEAUTY — hero medium shot, baby-pink dress, "looks directly into the lens". Soft dialogue: "My skin has never felt this alive."
  - SCENE 9 (0:13–0:15) FINAL HERO FRAME — symmetric product foreground, blurred model behind, final push-in
- CINEMATIC REQUIREMENTS bullets (17개, 말미): "... / No clutter / Minimalist luxury environment / 8K ultra-detailed realism / **Strict chronological shot order with no scene rearrangement**"
- 없음: negative constraints, SFX/music 블록, 자막 지시

### 4. Subject / Character state
- identity lock: 제품 (3 SKU — 15초 내내 유지됨 ✓). 모델은 텍스트 스펙 기반 (이미지 레퍼런스 아님)
- Character Reference (텍스트): 24yo Western woman, hazel-green eyes, wet-look blonde low slick bun, baby-pink luxury dress — 렌더에서 유지됨 ✓
- wardrobe lock: baby-pink luxury dress (SCENE 8, 렌더 확인 ✓)
- prop lock: 3제품 (b-Straighten PREP WASH / b-Smooth / STEP 3 POST TREATMENT)
- character count: 1 (+ 제품 3)
- gaze assignment: SCENE 8 "looks directly into the lens" — 렌더 확인 ✓ (s11–12)
- role separation: 해당 없음 (단일 모델)

### 5. Camera / Shot design
- multi-shot: 9신
- explicit cuts: "Clean cut" ×8 (매 신 전환 선언)
- camera role: 관찰자 (macro / push-in / slide / orbit)
- framing progression: extreme macro (product) → rotating beauty → macro touch → intimate close-up → extreme close-up (eyes) → tabletop slide → macro pour → hero medium → symmetric hero
- fish-eye: "only on selected dynamic macro shots" (prompt-derived — 스틸에서 확정 불가)
- **split-screen 렌더 (frame-observed)**: 영상은 상단 시네마틱 + 하단 9패널 그리드 스트립의 수직 스플릿. 1920x2160 = 16:9 상단 + 16:9 하단 스택. "vertical 9:16" 지정은 미준수 — 모델이 두 16:9 영역을 쌓는 타협안 선택 (aspect drift)

### 6. Spatial / Continuity
사용 채널: identity (제품 3SKU — 강함, 유지됨 ✓), model identity (텍스트 스펙 — 유지됨 ✓), tone/grade (warm chocolate-amber — 강함, 유지됨 ✓). spatial/topology: 추상 그라디언트 환경이라 연속성 부담 최소. "No clutter / Minimalist luxury environment"가 공간 단순성을 하드 스펙으로 못박음.

### 7. Action grammar
- product ritual arc: emerge → reveal → touch → apply → transform → ritual → texture → empowered → hero — 제품 광고의 표준 아크 (Case 07/21의 KitKat 아크와 동형)
- action density: 낮음 — 무드·질감 중심. "Cream glides", "viscosity forms smooth folds" 같은 물질 묘사가 액션을 대신
- dialogue beats: 2개 대사 (SCENE 4 silk / SCENE 8 alive)가 감정 곡선의 정점에 배치 — 대사가 구조적 마커
- anticipation → contact → consequence: SCENE 3 (펌프→크림 분출) — 부분적

### 8. Reference usage
- PART 1 image = storyboard infographic — 역할: container. 렌더에서 컨테이너 역할을 그대로 유지 (하단 스트립으로 전 구간 고정, 정지 이미지)
- PART 2의 Character Reference는 텍스트 스펙 (이미지 아님) — 모델 외모를 텍스트로 락
- Reference Role Separation 패턴의 강화 사례: 레퍼런스(인포그래픽)가 콘텐츠(시네마틱)와 분리된 채 각자의 역할을 유지 — Case 19의 role bleed와 정반대

### 9. Audio / Dialogue
- Soft dialogue 2줄 (prompt-derived): SCENE 4 "This feels like silk on my skin..." / SCENE 8 "My skin has never felt this alive."
- music/SFX: 언급 없음 (무음 스펙 — Case 07/21과 동일)
- beat sync: 없음
- 자막 미렌더 (frame-observed) — 프롬프트에 자막 지시 없음. 대사가 오디오로만 존재하는 스펙
- 오디오 자체는 프레임으로 검증 불가

### 10. Failure prevention
명시적 네거티브 없음. 관찰된 현상 (frame-observed):
- 제품 텍스트 안정: "b-Smooth" 정확 렌더 ✓, "b-Straighten PREP WASH" 부분 렌더 (잘림), "STEP 3 POST TREATMENT" 판독 가능 — 3 SKU 중 앵커 제품(b-Smooth)이 가장 안정적
- 패널 타이틀 ("01 PRODUCT EMERGES" 등) 판독 가능, 불릿 마이크로 텍스트는 판독 불가 수준
- aspect drift: "vertical 9:16" 지정 → 1920x2160 (8:9) 렌더. 단, 스플릿 구조상 두 16:9 영역 스택은 컨테이너(16:9 인포그래픽)를 살리는 선택 — 드리프트이자 적응

### 11. Control Levels
- Hard Lock: 9신의 타임스탬프, "Strict chronological shot order with no scene rearrangement", 신별 카메라/액션, 대사 2줄의 배치 위치
- Soft Guidance: 스타일/그레이드 블록, fish-eye 선별 적용, "No clutter"
- Creative Freedom: 모델 표정 디테일, bokeh, 크림 질감 연출

### 12. Why it may work
A. Evidence-backed:
- 9신의 시간 순서가 렌더(상단 시네마틱)에서 확인됨 — "Strict chronological shot order" 준수
- 제품 3 SKU가 15초 내내 유지됨. 앵커 제품 "b-Smooth" 텍스트 정확 렌더
- 그리드 컨테이너가 하단 스트립으로 전 구간 유지 — Case 07/21의 완전 붕괴와 대비되는 성공 표본
- 컨테이너 3-way 비교 (frame-observed):
  - Case 19 = 부분 붕괴: 디자인 시트가 약 2초간 풀프레임 정지 컷어웨이로 삽입, 경계는 split-wipe
  - Case 20 = 유지: 9패널 그리드가 하단 스트립으로 전 구간 고정 (1920x2160 = 16:9+16:9 스택)
  - Case 21 = 완전 붕괴: 2x5 그리드·번호·캡션 전무, 광고 본편만 (Case 07과 동일 영상 — 재관측)
- 그리드 패널 썸네일이 상단 시네마틱 씬과 일치 — 컨테이너와 콘텐츠가 서로를 비춤

B. Inference:
- 스토리보드 패널 자체가 씬 묘사(콘텐츠)이므로 컨테이너-콘텐츠 정합성이 높음 — 유지의 조건으로 보임 (가설, A/B 필요)
- 럭셔리 뷰티 광고는 현 모델 세대의 강점 영역으로 보임 (Case 09 Calira와 동계열)
- "Strict chronological shot order" 같은 순서 하드락은 밀도 높은 멀티씬에서 모델의 재배열 실패를 막는 장치로 보임

### 13. Popularity signal
- snapshot rank: 9 / likes: 130
- likely_driver: visual_subject (럭셔리 뷰티 광고 — 시각적 완성도), novelty (스토리보드 스플릿 스크린이라는 이례적 포맷), unknown (prompt_structure — 인과 근거 없음)
- 판단: 인기는 렌더 결과물의 힘일 가능성이 큼

### 14. Relation to existing XAI-Studio patterns
- Trailer Montage: 강화 (9신/15초 밀도)
- Identity-Locked Lifestyle: 제품 버전으로 강화 (3 SKU 단일 앵커)
- Reference Role Separation: 강화 (컨테이너 역할 유지 — Case 19의 bleed와 대비되는 양성 증거)
- Hard Lock/Soft Guidance/Creative Freedom: 강화
- Case 04의 화면 텍스트 라벨: 강화 (패널 번호·타이틀이 렌더에서 판독됨)
- Case 07/21의 KitKat 아크: 동형 (emerge→reveal→ritual→hero)

### 15. Candidate contribution
- new model-behavior note 후보: **persistent container strip** — 컨테이너를 별도 씬이 아니라 고정 스트립(하단 1/2)으로 유지하는 렌더 패턴의 첫 관측. 1920x2160 같은 비표준 종횡비가 그 흔적일 수 있음. 단일 사례 — A/B 테스트 필요, 규칙 승격 금지
- container-content congruence 가설(Case 19 §15)의 지지 증거 1건: 패널=씬 묘사인 경우 컨테이너 유지
- 그 외: reinforces existing patterns

---

## Case 21 — Shore Lyn "KitKat storyboard presentation" (Case 07 재관측) [snapshot rank 10]

### 1. Source
- URL: https://www.meigen.ai/video/2077345203049148886 — **Case 07과 동일 URL, 동일 영상**
- creator: Shore Lyn (@Shorelyn_)
- model: Seedance
- duration: 15.19초 실측 (456프레임/30fps/1080x1920 세로) — Case 07 실측과 동일
- popularity: snapshot rank 10, 164 likes (Case 07 기록 당시 rank 7 → rank 10으로 이동. Popular re-sort의 직접 증거)

### 2. Evidence basis
- prompt-derived (전문 확보 — Case 07과 동일 텍스트, 정본 verbatim 대조 완료)
- frame-observed (8프레임 컨택트시트 — Case 07과 동일 영상. 스토리보드 컨테이너 미렌더, 광고 본편만 렌더)
- author-described (Seedance 배지)
- inference: Why it may work B항
- **재관측 표기**: 독립 아티팩트가 아니므로 패턴 증거 가중치는 1건으로 계산

### 3. Prompt structure
Case 07과 동일 텍스트. 구조 분해 (Case 07 §3과 동일):
- container block: "professional commercial storyboard presentation ... 10 cinematic frames arranged in a clean 2x5 grid on a white presentation board. Thin black borders ... bold scene number (01–10), timestamp, short production caption" — 메타 프레젠테이션 지정
- title block: 'TITLE KITKAT "The Art of the Snap" Luxury Commercial Storyboard • 15 Seconds'
- style block: premium chocolate commercial aesthetic
- SCENE 01–10: 각 신 = (타임스탬프 1.5초씩) + [카메라/액션 서술] + "Caption: [짧은 캡션]"
  - 01 The Reveal → 02 Luxury Detail → 03 Ingredients Rise → 04 The Perfect Snap → 05 Floating Luxury → 06 Chocolate Flow → 07 Pure Indulgence → 08 Frozen Perfection → 09 Hero Product → 10 Brand Signature
- presentation style block: 반복 강조 (storyboard, pitch board, scene numbers, timestamps...)
- tech block: "ARRI Alexa 35 • Cooke Anamorphic 50mm • HDR • 8K"
- 없음: negative constraints, 대사, 레퍼런스 지정

### 4. Subject / Character state
Case 07과 동일:
- identity lock: 제품 — KitKat bar (단일 제품 앵커). 렌더에서 15초 내내 유지됨 ✓
- prop lock: 패키지 (SCENE 09). 렌더에서 등장 ✓
- character count: 0 (인물 없음)
- role separation: 해당 없음

### 5. Camera / Shot design
Case 07과 동일:
- multi-shot: 10신, 각 1.5초. explicit cuts 없음 (신 리스트만)
- framing progression: darkness → extreme macro → floating → snap → orbit → pour → cascade → frozen → hero → logo
- container 무시: 2x5 그리드·씬 번호·타임스탬프·캡션 전부 미렌더. 모델이 컨테이너를 버리고 콘텐츠만 렌더 (재확인)

### 6. Spatial / Continuity
Case 07과 동일: 사용 채널 — identity (제품 — 강함 ✓), prop (패키지), tone/grade (dark luxury ✓), lighting (warm golden ✓). spatial/topology 락 없음. 단일 제품이라 연속성 부담 최소.

### 7. Action grammar
Case 07과 동일: state transition 중심 (등장→디테일→재료→스냅→유동→정지→히어로→로고). "Time almost freezes" (SCENE 04), "Everything freezes" (SCENE 08) — 정지를 연출 장치로 2회. SCENE 04 snap → shards explode (anticipation→contact→consequence 부분적).

### 8. Reference usage
없음 (Case 07과 동일)

### 9. Audio / Dialogue
없음 — 오디오 블록 자체가 없음 (Case 07과 동일)

### 10. Failure prevention
실패 방지 문장 없음. 관찰된 현상 (frame-observed, Case 07과 동일):
- **container collapse** (재확인): 스토리보드 그리드·번호·캡션 전부 미렌더
- text seep: 패키지의 서브 텍스트 난독 (판독 불가 수준). "KitKat" 로고와 "Have a Break. Enjoy Every Snap." 태그라인은 정확히 렌더 ✓ (유명 브랜드 텍스트 안정성 재확인)

### 11. Control Levels
Case 07과 동일:
- Hard Lock: 10신의 타임스탬프, 신별 액션, 태그라인 문구
- Soft Guidance: 스타일 블록, 컨테이너 스펙, 테크 스펙
- Creative Freedom: 카메라 디테일, 파티클, 조명

### 12. Why it may work
A. Evidence-backed:
- Case 07의 container collapse를 동일 영상에서 재확인 — 3-way 비교의 '완전 붕괴' 축을 고정하는 반복 관측
- 10신이 1.5초씩 15초에 매핑, 신별 액션 렌더 확인, 단일 제품 앵커 유지, 브랜드 텍스트 정확 렌더 (Case 07 §12A와 동일)
- 컨테이너 3-way 비교 (frame-observed):
  - Case 19 = 부분 붕괴: 디자인 시트가 약 2초간 풀프레임 정지 컷어웨이로 삽입, 경계는 split-wipe
  - Case 20 = 유지: 9패널 그리드가 하단 스트립으로 전 구간 고정 (1920x2160 = 16:9+16:9 스택)
  - Case 21 = 완전 붕괴: 2x5 그리드·번호·캡션 전무, 광고 본편만 렌더 (본 케이스 = Case 07 재관측)
- 동일 아티팩트의 반복 관측이므로 종합 시 패턴 증거 가중치는 1건으로 계산해야 함

B. Inference:
- Case 07 §12B와 동일 (컨테이너 붕괴가 오히려 유리하게 작용했을 가능성, 제품 단일 앵커의 실패 표면 최소)

### 13. Popularity signal
- snapshot rank: 10 / likes: 164 (Case 07 기록 시 rank 7 → 현재 rank 10)
- 순위 변동 자체가 Popular 탭 re-sort의 직접 증거 — "인기 순위"의 시간 불안정성
- likely_driver: visual_subject (Case 07과 동일 판단 — 럭셔리 초콜릿 광고의 시각적 완성도), novelty, unknown
- 판단: Case 07과 동일. 인기는 렌더 결과물(광고)의 힘일 가능성이 큼

### 14. Relation to existing XAI-Studio patterns
- Case 07과 동일: Trailer Montage 강화, Identity-Locked 제품 버전 강화, Hard/Soft/Creative 강화
- 중복 아티팩트이므로 기존 패턴 강화 증거로도 1건으로 계산 — 이중 계상 금지

### 15. Candidate contribution
- "reinforces Case 07" — 신규 기여 없음
- 단, 동일 영상의 재진입(rank 7→10)은 갤러리 re-sort 하에서 '인기'라는 신호 자체의 시간 불안정성을 보여주는 메타 증거. 종합 G의 방법론 주의사항으로 이관
