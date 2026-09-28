# MeiGen Top 20 Video Prompts — Case 11–13 (신규 스냅샷)
meigen-top20.md (Case 01–10)와 동일 15섹션 포맷. 증거 기반: frame-observed / prompt-derived / author-described / text-guide / inference. 인기 ≠ 품질. 추론은 production rule로 승격하지 않는다. SKILL.md 확정 금지.

---

## Case 11 — Kashberg "{" (JSON prompt) [신규 스냅샷 rank 15]

### 1. Source
- URL: https://www.meigen.ai/video/2086667012844199976
- creator: Kashberg (@Kashberg_0)
- model: Seedance (MeiGen 배지)
- duration: 34.21초 실측 (821프레임/24fps/1276x720)
- popularity: 신규 스냅샷 rank 15, 갤러리 카드 134 likes (페이지 schema.org에는 likes 3139 / views 334364으로 표기 — 집계 기준이 다름. 아래 13번은 갤러리 카드 기준)
- 비고: 이전 수집에서 이 URL에 prose 프롬프트("rainy neon street...")가 오귀속된 적 있음 — 피드 re-sort 타이밍 문제. detail page의 JSON이 정본임을 직접 확인

### 2. Evidence basis
- prompt-derived (detail page JSON 전문 직접 추출·검증)
- frame-observed (8프레임 + 컨택트시트. 7개 scene 전부 렌더 확인)
- author-described (타이틀 "{", Seedance 배지)
- inference: Why it may work B항

### 3. Prompt structure
JSON 오브젝트, 약 1370자. 코퍼스 최초의 machine-readable 구조. 구조 분해:
- video_generation.subject: character (외모 6요소) / clothing (3아이템 + '38' 슬리브 넘버) / vehicle ("Matte black fixed-gear bicycle") — 탈 것을 subject 하위 독립 키로 잠금
- video_generation.scenes: 7개 문자열 배열. 각 scene = 단일 문장, 단일 액션. scene 5에만 내장 이펙트 지시 ("causing noodles to fly in slow motion")
- video_generation.camera_work: 한 줄 ("Dynamic tracking shots, fast-paced action, brief slow-motion emphasis during the food spill") — 슬로모를 특정 scene(음식 유출)에 귀속
- video_generation.style: 한 줄 ("Ultra-realistic 3D animation, cinematic lighting, vibrant colors, motion blur")
- video_generation.render_settings: {resolution: "8K", quality, aesthetic} — 렌더 품질 선언 블록
- 없음: negative prompt, 타임스탬프, 대사, 오디오, 레퍼런스 이미지 문법, 명시적 컷 어휘

### 4. Subject / Character state
- identity lock: 텍스트 서술 (flat-top fade, goatee, neck/arm tattoos, hoop earrings, geometric reflective sunglasses) — 레퍼런스 이미지 없음
- wardrobe lock: varsity jacket '38' / black shorts / white socks — 렌더 확인 ✓ (컨택트시트에서 '38' 백넘버, 선글라스, 고티 모두 유지)
- vehicle lock: 무광 블랙 픽시 — 7개 scene 내내 동일 자전거 유지 ✓ (frame-observed)
- character count: 1 (+ 마지막 scene의 "a woman is waiting" — 미니멀 엑스트라, 락 없음)
- gaze assignment: 없음

### 5. Camera / Shot design
- 7 scenes = 암시적 7샷. 명시적 컷 어휘 없음
- camera_work 한 줄이 전체를 커버: dynamic tracking shots + "brief slow-motion emphasis during the food spill" — 이펙트(슬로모)를 특정 이벤트에 국소 바인딩 (Case 02의 신체-트리거 바인딩과 달리 scene-인덱스 바인딩)
- subject-camera relationship: 추적 관찰자. 셀피 아님
- 렌더 (frame-observed): 추적샷 위주, 모션 블러 가시적

### 6. Spatial / Continuity
사용 채널: identity (텍스트), wardrobe, vehicle. 도심 7개 로케이션을 이동하는 체인이라 공간 연속성 요구는 낮게 설계됨. 대신 character+vehicle의 샷 간 유지가 연속성의 전부 — 둘 다 유지됨 ✓. lighting/topology 명시적 락 없음.

### 7. Action grammar
- 각 scene = 단일 결과 문장. scene 5만 인과 구조: "bumping a man and causing noodles to fly in slow motion" — 접촉→결과의 micro cause-effect를 한 문장에 압축
- 슬로모는 scene 5의 결과(noodles fly)에만 귀속 — "언제 슬로모인가"를 이벤트로 지정
- anticipation 구조 없음. 34초/7scene ≈ scene당 5초의 여유로운 페이싱

### 8. Reference usage
- 없음 (텍스트 전용)

### 9. Audio / Dialogue
- 없음. 34초 액션 몽타주에 오디오 지시 전무 — 주목할 부재

### 10. Failure prevention
- negative prompt 없음. 실패 기반 네거티브도 없음
- 관찰된 drift (frame-observed): style이 "Ultra-realistic 3D animation"을 선언했으나 렌더는 스타일라이즈드 3D (사실적이지 않음). "sunlit city streets"는 유지 ✓. 네거티브 부재와 직접 연결짓기는 불가 (inference 금지선 준수)

### 11. Control Levels
- Hard Lock: character 서술, wardrobe 3아이템, vehicle, 7개 scene의 발생 사건
- Soft Guidance: camera_work, style
- Creative Freedom: scene 간 전환, 프레이밍, scene별 타이밍, 슬로모의 정확한 길이

### 12. Why it may work
A. Evidence-backed:
- 7개 scene 전부 렌더에서 확인됨 (frame-observed): 폰 하트 클로즈업 → 음료/자전거 탑승 → 도심 트래픽 질주 → (계단) → 음식시장 누들 → 더트점프 → 유리빌딩 앞 정지. scene 누락 0
- 각 scene이 단일 명사+단일 동사로 구성 — 모호한 형용사 없음. vehicle을 독립 키로 분리한 것이 7개 scene 내내 자전거 일관성에 기여했을 가능성 (관찰 사실: 유지됨)

B. Inference:
- JSON 키 구조가 모델에게 역할 분리(subject/scenes/camera/style)를 명시적으로 전달 — prose의 섹션 라벨(Case 02·03·05)과 같은 기능을 기계可読 형태로 수행할 수 있음. 단, 단일 케이스이며 렌더 성공이 JSON 덕분이라는 인과 증거 없음
- scene당 5초 페이싱은 모델의 액션 렌더 부담을 낮춤

### 13. Popularity signal
- rank: 15 (신규 스냅샷) / likes: 134 (갤러리 카드; schema.org는 3139)
- likely_driver: novelty (코퍼스 유일의 JSON 프롬프트 — 포맷 자체의 새로움), visual_subject (스타일라이즈드 사이클리스트), unknown (prompt_structure의 인과)
- 판단: 렌더 매칭은 완벽하나, 인기와 JSON 포맷의 인과관계는 단정 불가

### 14. Relation to existing XAI-Studio patterns
- Routine Montage: 강화 (scene 체인)
- Travel Coverage: 강화 (도시 이동 체인)
- Trailer Montage: 강화
- 섹션 라벨 블록: Case 02·03·05의 prose 라벨과 동형 — JSON은 새로운 serialization일 뿐, "의미 블록 분리"라는 패턴 자체는 기존 것의 강화
- Hard/Soft/Creative: 강화
- Reference Role Separation: 해당 없음

### 15. Candidate contribution
- 신규 후보 (format-level): **machine-readable key structure (JSON) as prompt container** — subject/scenes/camera_work/style/render_settings 키 분리. 코퍼스 최초. 단, 효과는 미검증 (단일 케이스, A/B 없음) — D 후보로만 올리고 rule 승격 금지
- 그 외는 reinforces existing patterns

---
## Case 12 — WasifAI "slice-of-life, 15 seconds..." [신규 스냅샷 rank 11]

### 1. Source
- URL: https://www.meigen.ai/video/2071932825583124810
- creator: WasifAI (@doctorwasif)
- model: Seedance
- duration: 15.15초 실측 (454프레임/30fps/1920x1080)
- popularity: 신규 스냅샷 rank 11, 갤러리 카드 130 likes (schema.org: 187 likes / 7625 views)
- 비고: 이 창작자는 reference-state-analyses #40·#45의 CHASE 짐 셀프POV 그 사람 — deliberate imperfection 계열의 연속선

### 2. Evidence basis
- prompt-derived (전문 확보)
- frame-observed (8프레임 + 컨택트시트. 7개 비트 전부 매칭)
- author-described (타이틀, Seedance 배지)
- inference: Why it may work B항

### 3. Prompt structure
prose, 약 2006자. 구조 분해:
- header: "slice-of-life, 15 seconds. @ image1 = Main Subject. Preserve exact face, hairstyle, features, skin tone, body proportions."
- OUTFIT block: 4아이템 + 상태 서술 ("Shirt damp/sweat-stained at collar, underarms, chest. Hair loosely down... strands stuck to face/neck. Unglamorous.") — 의상을 아이템이 아니라 상태로 잠금
- LOCATION block: 명사 리스트 (stilt houses, banana/palm trees, bamboo fences, clay water jars, hanging chilies/herbs, chickens, cooking smoke...) + "Zero modern elements." — 배제형 락으로 마감
- CAMERA block: "Late-2000s flip cam vlog." + 12개 imperfection 항목 (Heavy handheld shake / Imperfect reframing / Off-center/cropped framing / Aggressive autofocus hunting / Exposure swings / Rolling shutter / Motion blur / Warm faded muddy tones / Blown highlights / Crushed blacks / Digital noise/compression artifacts) — 결함을 스펙으로 지정 (긍정 스펙의 전도)
- 7비트 타임스탬프 (00:00–00:15): 각 비트 = [장소]. [카메라]. [액션 micro-event]. 카메라 동작이 액션으로 기재됨 ("Camera breathes between face/dog", "Late reframe", "Focus hunts", "Cuts abruptly")
- negative list: "No posing. No glamour. No stabilization. No modern grading. No music." — 모델의 기본倾向을 겨냥한 5연타
- AUDIO block: diegetic 명사 리스트 (birds, roosters, chatter, dog, water, fire crackle, footsteps, leaves, wind, ceramic sounds)
- aspect: "16:9." 한 줄 선언

### 4. Subject / Character state
- identity lock: @image1 — 있음
- wardrobe lock: olive sleeveless linen shirt / dusty burgundy wide-leg trousers / rubber sandals / gold hoop earrings — 렌더 확인 ✓. 상태 잠금 (damp/sweat-stained) — 프레임에서 땀 얼룩은 불명확
- "Unglamorous." 캐릭터 지시 — 렌더 관찰 (frame-observed): 피사체가 글래머러스하게 렌더됨. "No glamour"는 부분 실패
- character count: 1 (+ 배경 엑스트라: elder woman, stray dog — dog는 비트 2·4에 연속 등장)
- gaze assignment: "casual talk to lens" (비트 1·7) — 렌즈 응시 2비트

### 5. Camera / Shot design
- 7비트, 비트별 카메라 지정: arm's-length self-shot (비트 1·7, 셀피 문법) / handheld from behind / low handheld / side tracking
- imperfection이 카메라의 정체성: 흔들림·AF 헌팅·노출 변동을 "포함할 것"으로 지정 — 네거티브가 아닌 긍정 스펙
- "Cuts abruptly" — 엔딩을 anti-ending으로 지정 (페이드아웃 없음)
- 렌더 (frame-observed): 비트 구성 전부 유지. flip-cam 특유의 강한 디그레이드는 프레임에서 미약 — 영상은 비교적 깨끗하게 렌더됨 (imperfection spec의 렌더 강도는 불명)

### 6. Spatial / Continuity
사용 채널: identity (@image1), wardrobe, location (명사 리스트 + "Zero modern elements" 배제 락). 비트가 마을 하위 로케이션을 이동 — dog의 비트 2·4 연속 등장, elder woman의 비트 6 배경 등장으로 약한 연속성 유지. spatial 좌표 락 없음.

### 7. Action grammar
- 비트 = [시간] — [장소]. [카메라]. [micro-event]. micro-event는 작음: "weeds brushing past", "chicken crosses ahead", "breeze lifts hair", "sips tin cup"
- 카메라 동작을 액션 문법 안에 씀: "Camera breathes", "Late reframe", "Focus hunts" — 카메라가 주어인 문장
- slice-of-life: 아크·클라이맥스 없음. 상태의 나열

### 8. Reference usage
- @image1 = identity-only. 단일 authority

### 9. Audio / Dialogue
- dialogue: "casual talk to lens" — 대사는 없고 행위만 지정 (대사 내용은 Creative Freedom)
- music: "No music" 명시
- AUDIO: diegetic 명사 10개 리스트. beat sync 없음

### 10. Failure prevention
실패 기반 네거티브의 강한 표본:
- "No posing. No glamour. No stabilization. No modern grading. No music." — AI의 기본倾向(포즈·글래머·손떨방·현대적 그레이딩·BGM)을 정면으로 겨냥
- "Zero modern elements." — 로케이션 오염 방지
- 관찰된 실패 (frame-observed): "Unglamorous"/"No glamour"에도 불구하고 피사체가 글래머러스하게 렌더됨 — 네거티브가 모델의 미화 바이어스를 완전히 못 막은 사례

### 11. Control Levels
- Hard Lock: @image1, outfit 아이템, location 명사 리스트, 7비트 타임스탬프 구조, 네거티브 5연타, "No music"
- Soft Guidance: imperfection spec (흔들림의 정도 등), micro-event, "Zero modern elements"
- Creative Freedom: 대사의 실제 내용, 프레이밍 디테일, "casual talk"의 말투

### 12. Why it may work
A. Evidence-backed:
- 7개 비트 전부 프레임에서 확인됨 (frame-observed): 대나무길 셀피 → 마당+개 → 물두멍 세수 → 개 먹이주기 → 닭 지나가는 길 → 할머니와 찻잔 → 마무리 셀피. 비트 누락 0
- LOCATION 명사 리스트의 요소들 (stilt house, clay jars/pots, bamboo fence, chicken, thatch roof)이 프레임에 전부 존재 — 명사 지정의 렌더 적중률 높음

B. Inference:
- imperfection을 긍정 스펙으로 지정하면 모델의 "깨끗하게/예쁘게" 바이어스와 정면충돌 — #45 deliberate imperfection과 같은 계열의 추론. 렌더가 비교적 깨끗한 것은 spec 강도 부족 또는 모델의 미화 우선일 수 있음 (단정 불가)
- "No X" 5연타는 실패 모드를 직접 열거한 것으로 Failure-Sourced Negatives의 정석형

### 13. Popularity signal
- rank: 11 (신규 스냅샷) / likes: 130 (갤러리 카드; schema.org 187)
- likely_driver: creator_reach (CHASE 시리즈로 검증된 창작자 — #40·#45), visual_subject, unknown (prompt_structure의 인과)
- 판단: 동일 창작자의 전작(#40)이 프롬프트 전문 공개형 바이럴이었던 점이 이 케이스의 확산에도 작용했을 가능성 — inference이며 인과 단정 불가

### 14. Relation to existing XAI-Studio patterns
- deliberate imperfection (#45, #19 MiniDV): 강화 — 코퍼스에서 가장 완전한 12항목 defect 스펙
- Failure-Sourced Negatives: 강화 ("No posing. No glamour..." 5연타 + "Zero modern elements")
- Identity-Locked Lifestyle: 강화
- Front-Covered Experience Vlog: 강화 (비트 1·7 셀피)
- 타임스탬프 비트: Case 05와 동형 — 강화
- Hard/Soft/Creative: 강화

### 15. Candidate contribution
- reinforces existing patterns. 신규 규칙 없음
- 표본으로서의 가치: (1) imperfection-as-positive-spec의 최완전형 — deliberate imperfection 패턴의 대표 표본으로 승격 검토 가능 (패턴 자체는 기존). (2) "Unglamorous → 글래머러스 렌더"는 네거티브의 한계를 보여주는 실패 표본 — Failure-Sourced Negatives의 역표본으로 기록 가치 있음

---
## Case 13 — Sharon Riley "giant dragon, alpine summit" [신규 스냅샷 rank 12]

### 1. Source
- URL: https://www.meigen.ai/video/2080906169309442468
- creator: Sharon Riley (@Just_sharon7)
- model: Seedance
- duration: 15.12초 실측 (362프레임/24fps/1280x720). "15-second" 주장과 일치
- popularity: 신규 스냅샷 rank 12, 갤러리 카드 125 likes

### 2. Evidence basis
- prompt-derived (전문 확보, 약 5947자 — Case 01–10 중 최장급)
- frame-observed (8프레임 + 컨택트시트. 7개 샷 전부 매칭)
- author-described (타이틀, Seedance 배지)
- inference: Why it may work B항

### 3. Prompt structure
prose, 섹션 블록 + 7샷. 구조 분해:
- header: 포맷 선언 ("15-second... in 16:9", "shot on anamorphic 35mm lenses, realistic camera physics, subtle handheld movement, natural lens breathing, cinematic motion blur, restrained film grain, physically accurate lighting")
- environment block: 알파인 서밋 명사 리스트 + "Maintain perfect environmental continuity throughout every shot." — 마스터 연속성 스위치
- character block: 여성 (25세, blonde, blue eyes, athletic) + 중세 탐험가 의상 7아이템 + 검 + "Preserve her exact facial features, hairstyle, clothing, body proportions, and identity consistently throughout the entire video."
- companion block: 드래곤 (pink-red, amber eyes, horns, translucent wing membranes with visible veins...) + 행동 스펙 ("behaves like a real undiscovered animal" + breathing/shifting muscles/moist eyes/weight/physically accurate interactions) + 스케일 락 ("The dragon always remains vastly larger than the woman.")
- wind block: "A powerful alpine crosswind acts as a third character throughout the sequence" + 영향 대상 리스트 (hair, clothing, satchel straps, grass, dust, gravel, wing membranes, neck spines) + "believable delayed secondary motion" — 물리에 시간 지연 지정
- 7샷 파라그래프: 각 샷 = 카메라 무브 + 액션 + 환경 반응. 전환 어휘: "Cut to", "Transition into", "Move into", "Finish with"
- master line: "Maintain absolute live-action realism throughout with consistent lighting, geography, scale, anatomy, wind direction, environmental continuity, and character identity." — 7개 채널을 한 줄에 잠금 (Case 03의 LOGIC RULE과 동형)
- Negative Prompt: 약 40항목 (아래 10번 참조)

### 4. Subject / Character state
- identity lock: 텍스트 서술 (레퍼런스 이미지 없음)
- wardrobe lock: leather tunic / dark trousers / tall boots / bracers / satchel / belt / medieval sword — 렌더 관찰 (frame-observed): 다크 톤 상의 위주로 단순화됨. 7아이템 풀킷은 미렌더 — 부분 drift
- companion: 드래곤 — 스케일 부등식 락 ("always remains vastly larger"). 렌더에서 7샷 내내 유지 ✓
- dragon behavior lock: "real undiscovered animal" + 6개 행동 명사 — 렌더에서 breathing/weight감 가시적
- character count: 2 (여성 + 드래곤)
- gaze assignment: "Focus shifts naturally from her fingers... to the dragon's amber eye and finally to her genuine smile" (샷 4) — 포커스 이동으로 시선 유도

### 5. Camera / Shot design
- 7샷, 샷별 카메라 무브 명명: extreme ground-level hidden camera → dynamic forward-moving low perspective → fast lateral tracking (foreground boulders hide/reveal) → close reverse circular orbit → snout-mounted close-up → perfectly vertical top-down aerial → cliff-edge aerial + dive-back + fly-by + wide end
- "seamless multi-shot transitions" 헤더 선언
- 카메라의 물리적 피격: "The dragon's heavy breathing creates subtle camera movement", "the camera receives a subtle physical bump, creating an authentic documentary feel" — 카메라를 씬 안의 물체로 취급
- foreground occlusion을 전환 장치로 사용 ("Foreground boulders repeatedly hide and reveal the action")
- 렌더 (frame-observed): 7샷 전부 확인 (날개 오버헤드 → 로우 추적/발톱 → 이마 맞대기 → 스나웃 클로즈업 → 날개 펼치기 이륙 → 공중 플라이바이 → 와이드 엔딩)

### 6. Spatial / Continuity
사용 채널: environment (마스터 스위치), lighting, geography, scale, anatomy, wind direction, character identity — master line에서 7채널 일괄 잠금. wind direction을 연속성 채널로 명시한 것이 특이. "Maintain perfect environmental continuity throughout every shot" — Case 03 LOGIC RULE의 강화형.

### 7. Action grammar
- 샷 파라그래프 = 카메라 무브 + 캐릭터 액션 + 환경 반응의 3층 구조
- 감정 비트: forehead touch (샷 4), playful snort + nudge (샷 5), laughing while shielding face (샷 6)
- cause→effect 체인: wing passes → pressure gust / wingbeat → concentric pressure wave / snort → hair flies backward — 물리 인과의 명시적 서술
- wind의 "delayed secondary motion": 힘의 전달에 시간 지연을 지정 — 물리 시뮬레이션적 서술

### 8. Reference usage
- 없음 (텍스트 전용)

### 9. Audio / Dialogue
- 없음. 15초 시네마틱에 오디오 지시 전무 — 주목할 부재 (Case 11과 동일)

### 10. Failure prevention
- Negative Prompt 약 40항목. 실패 기반 항목: "morphing, duplicated characters, anatomy changes, inconsistent scale, extra limbs, deformed wings" (크리처 렌더의 전형적 실패 모드), "text, captions, subtitles, logos, watermarks, interface elements" (text seep 방지 — Case 02의 거울반전 포스터 실패와 대조), "CGI, animation, cartoon, stylized fantasy" (스타일 drift 방지), "unrealistic physics, weightless movement" (물리 실패 방지)
- 관찰된 drift (frame-observed): "Preserve... clothing... consistently"에도 불구하고 중세 탐험가 풀킷이 다크 상의로 단순화 — wardrobe lock 부분 실패. 네거티브에 의상 항목이 없었던 점과 무관하지 않을 수 있으나 인과 단정 불가

### 11. Control Levels
- Hard Lock: 환경 서술, 캐릭터 identity 서술, 드래곤 스케일 부등식, 네거티브 프롬프트, 7샷 시퀀스, master continuity line
- Soft Guidance: 카메라 무브, wind 행동, 감정 비트
- Creative Freedom: 샷별 정확한 타이밍, 전환의 렌더링 방식

### 12. Why it may work
A. Evidence-backed:
- 7개 샷 전부 렌더에서 확인됨 (frame-observed). 스케일 락("vastly larger") 7샷 내내 유지 ✓. 바람의 머리카락 흩날림 가시적 ✓
- 네거티브가 크리처 실패 모드(anatomy changes, extra limbs, deformed wings, inconsistent scale)를 직접 열거 — 해당 실패가 렌더에서 관찰되지 않음

B. Inference:
- 바람을 "third character"로 지정하면 모델이 샷을 관통하는 단일 물리 시스템(원인 1개 → 효과 다수)을 유지할 수 있음 — 환경 블록과 별개로 힘(force)에 행동 스펙을 부여한 것이 연속성에 기여했을 가능성. 단, 인과 증거 없음
- "delayed secondary motion"은 물리의 시간축을 언어로 지정한 드문 사례 — 모델의 물리 추론을 돕는 방향일 수 있음

### 13. Popularity signal
- rank: 12 (신규 스냅샷) / likes: 125
- likely_driver: visual_subject (드래곤 — 썸네일/첫프레임 스펙터클), novelty (생물학적 리얼리즘 크리처), unknown (prompt_structure의 인과)
- 판단: 5947자 프롬프트의 길이와 인기 사이의 인과관계는 단정 불가

### 14. Relation to existing XAI-Studio patterns
- Trace-first physics: 강화 — 바람이 손 움직임(Case 02) 대신 전 샷을 관통하는 trace로 기능. "delayed secondary motion"은 trace의 시간 지연 명시
- Failure-Sourced Negatives: 강화 — 크리처 특화 네거티브 40항목
- LOGIC RULE 마스터 스위치 (Case 03): 강화 — "Maintain absolute live-action realism throughout with consistent [7 channels]"
- Coverage Planning: 강화 (7샷)
- 카메라 물리성: #40·#45의 "Camcorder never appears on screen"(카메라 은폐)의 역형 — 여기서는 "camera receives a subtle physical bump"(카메라 피격). 카메라를 물리적 존재로 취급한다는 점에서 동계열의 변주

### 15. Candidate contribution
- 신규 후보: **persistent force as character (환경 힘의 캐릭터화)** — 바람을 "third character"로 지정하고 영향 대상 리스트 + 행동 스펙(delayed secondary motion) + 연속성 채널(wind direction)을 부여. 환경 블록과 분리된 "힘" 단위의 스펙은 코퍼스 최초. (최종 D에서 최대 5개 중 하나로 검토)
- "scale lock as inequality" ("always remains vastly larger") — Relative Spatial Coordinates의 강화형으로 기록
- 그 외는 reinforces existing patterns
