# MeiGen Top 20 — Cases 14/15/16 (신규 수집분)
작업 지시: XAI-Studio-Video 재사용 가능한 구조적 패턴 추출. 인기 ≠ 품질.
증거 기반: frame-observed / prompt-derived / author-described / text-guide / inference.
추론은 production rule로 승격하지 않는다. SKILL.md 확정 금지.
본 파일은 meigen-top20.md (Case 01~10)와 동일 15섹션 포맷. meigen-top20.md는 수정하지 않음.
프롬프트 인용은 2026-09-26 parent 제공 verbatim 정본에서만 가져옴.

---

## Case 14 — el.cine "raw film camera footage, overcast rainy day..." [신규 수집분]

### 1. Source
- URL: https://www.meigen.ai/video/2072724511884292524
- creator: el.cine (@EHuanglu)
- model: Seedance (갤러리 기본 탭 기준, author-described)
- duration: 69.5초 실측 (1668프레임/24fps/1280x720) — 코퍼스 최장
- popularity: 122 likes (2026-09-26 21:14 KST 스냅샷 기준 Popular position 3)

### 2. Evidence basis
- prompt-derived (전문 확보 — parent 제공 verbatim)
- frame-observed (컨택트시트 + 8프레임 중 f001·f008 확인). 프롬프트와 매칭됨 — 단, 스코프 불일치 (아래)
- inference: Why it may work B항
- audio: 프레임만으로 검증 불가 — 대사·보이스·diegetic sound 렌더 여부는 미확인으로 기록

**Prompt–video scope mismatch (frame-observed):** 프롬프트는 Shot 1·Shot 2까지만 기술하는데 영상은 69.5초. 프롬프트 범위를 넘어선 확장 배틀이 렌더됨 — 날아다니는 너겟 포격(f001의 모션블러), 거대 버거 강림(f008), 커널의 추격. 즉, 프롬프트는 개전(開戰) 2샷만 지정하고 전쟁의 전개는 모델에 위임한 under-specification 구조.

### 3. Prompt structure
섹션 라벨 방식 + 2샷. 정본 기준 구조 분해:
- look block (첫 문장): "raw film camera footage, overcast rainy day (grey cloudy sky, steady moderate rain with visible streaks — not a downpour, kept light enough to read faces — wet reflective streets and puddles, soft flat daylight)" — 촬영 매체(film)와 날씨를 최전방에. 비의 강도에 상한을 두고 이유를 명시 ("kept light enough to read faces" — 얼굴 판독 가능성)
- consistency declaration: "Same rain intensity in every shot" — 샷 간 날씨 일관성 선언
- anti-grade lock: "Natural light, NO color grading — looks like real unedited footage, not glossy, not graded" — 광택·그레이딩 금지
- CAMERA block: "handheld shaky throughout, highly dynamic: quick zoom in/out, fast whip-pans, snap pushes timed to throws/catches/impacts; steadier only on tight close-ups" — 카메라 움직임을 액션 임팩트에 타이밍 바인딩 ("timed to throws/catches/impacts")
- PERFORMANCE block (캐릭터별 연기 분리): "the Clown: rubbery, theatrical circus-clown physicality — bouncy springy movement, big sweeping arm flourishes, exaggerated lunges and recoils, elastic face (eyes popping wide, brows flying, mouth stretching huge), gleeful and unhinged, always over-the-top" / "the Colonel: cranky old-boomer energy — stiffer, slower, heavier; dismissive scowls and eye-rolls, a sour set mouth, deliberate cane taps and curt hand waves, grumpy and unimpressed even when he attacks" — 동일 프롬프트 안에서 두 인물의 연기 톤을 정반대로 지정. "Both read big and comedic but stay fully photoreal, never animated-looking" — 스타일 상한선
- EMOTION = BODY block: "EMOTION = BODY (not labels): show every feeling through visible movement: eyes, brows, mouth, head tilt, hands, shoulders, stance. Keep both characters alive in every shot even when still: breathing, blinks, small weight shifts, rain landing on them." — 감정을 라벨이 아닌 신체 채널 나열로 지정 + 정지 상태에서도 "살아있게" 유지하는 idle-life 규칙
- VOICE block: "lifelike voice (use this voice @[Audio 1](audio_1) for Colonel / use this voice @[Audio 2](audio_2) for Clown): natural breaths and rhythm, not flat TTS; the emotion of each line matches the action on screen (furious, taunting, straining, weak, smug)" — 캐릭터-보이스 1:1 매핑 + "not flat TTS" 실패 기반 네거티브 + 대사의 감정을 화면 액션에 매칭
- CHARACTERS block: '"the Colonel" (KFC — white suit, white goatee, glasses, cane) vs "the Clown" (McDonald's — red hair, yellow jumpsuit, red-white stripes); they duel by hurling food across the street — Colonel throws fried chicken, Clown throws burgers. @[Image 1](image_1) is the Colonel, @[Image 2](image_2) is the Clown' — 실존 브랜드 마스코트를 subject로 직접 지정 + 비대칭 투사체 (커널=치킨, 광대=버거)
- ENVIRONMENT block: "ENVIRONMENT (identical every gen): rainy wide American downtown street: overcast grey sky, steady moderate rain (visible streaks, not a downpour), wet reflective asphalt, puddles; two fast-food restaurants on opposite corners (red-white vs yellow-red). Reference @[Image 3](image_3) is wide street + @[Image 4](image_4) is KFC Store, @[Image 5](image_5) is McDonald's Store" — "identical every gen" 생성 간 일관성 선언 + 환경 레퍼런스 3종 분리
- STAGING block (fixed): "Colonel always at the KFC storefront, Clown always at the McDonald's storefront opposite, facing across the street — never together in the middle; each keeps his own store visible behind him." — 위치 고정 + 대치 구도 + 금지 구역("never together in the middle") + 배경 유지 조건
- AUDIO block: "no music or score; only diegetic sound (steady rain, footsteps in puddles, food whooshes, wet impacts and splashes, street tone)" — 음악 금지 + diegetic 사운드 나열
- TEXT block: "No on-screen text or subtitles." — 화면 텍스트·자막 금지 (명시적)
- Shot 1: 커널 미디엄샷 — 날아온 버거가 손바닥을 빗나가 얼굴에 정통으로 맞고 천천히 흘러내리며 소스 자국을 남김. quick zoom in 후 분노 억제 마이크로비트 체인: "his face begins to tremble — a vein bulging at his temple, jaw muscles twitching, nostrils flaring, one eye ticking, knuckles whitening as his fist crushes the cane — fighting with everything he has to hold his temper in. He drags one slow, shaking breath through gritted teeth." 대사는 폭발이 아닌 억제의 끝에서: "low and quaking with barely-contained fury, right on the edge of erupting but forcing it down: 'You brought a Happy Meal to a gunfire, boy.'"
- Shot 2: "hard cut to high angle close up shot of the Clown doubled over laughing, head thrown back, slapping his knee, eyes squeezed to manic slits. He howls: 'What about a cannon?' laugh and slapping his knee" — "hard cut" 명시적 전환 + 하이앵글 클로즈업
- 없음: Shot 3 이후 서술, generic negative

### 4. Subject / Character state
- identity lock: @[Image 1](image_1) = Colonel, @[Image 2](image_2) = Clown (platform syntax) — 캐릭터별 레퍼런스 분리
- acting direction: 캐릭터별 정반대 지정 — 광대(rubbery theatrical, "gleeful and unhinged, always over-the-top") vs 커널(cranky old-boomer, "grumpy and unimpressed even when he attacks")
- emotion spec: 라벨이 아닌 신체 채널 나열 (eyes, brows, mouth, head tilt, hands, shoulders, stance) + idle-life (breathing, blinks, small weight shifts, rain landing on them)
- wardrobe lock: 마스코트 고정 의상 (IP 자체가 의상)
- projectile asymmetry: 커널=fried chicken, 광대=burgers — 투사체가 캐릭터 정체성과绑定
- 렌더 결과 (frame-observed): 69.5초 전 구간에서 두 캐릭터 식별 유지 ✓ — 8프레임 모두에서 광대/커널이 즉시 판별됨
- character count: 2 (+ 음식 투사체, 거대 버거)
- gaze assignment: 없음

### 5. Camera / Shot design
- multi-shot: Shot 1·2 선언 + 모델이 확장한 배틀 시퀀스
- "hard cut" 명시적 전환 (Shot 2)
- camera role: raw film camera — 관찰자. "handheld shaky throughout", "snap pushes timed to throws/catches/impacts" — 카메라 푸시를 투척/포획/임팩트에 타이밍 바인딩. f001에서 강한 모션블러 확인 (날아다니는 너겟의 궤적 블러) — "raw film" 룩이 렌더에서 동작
- "steadier only on tight close-ups" — 클로즈업에서만 안정화되는 조건부 카메라 규칙
- framing: 와이드 배틀 장면 ↔ 캐릭터 클로즈업(버거를 든 광대, 주먹을 쥔 커널) 교차. Shot 1의 "quick zoom in"은 분노 억제 비트의 타이밍에 묶임
- subject-camera relationship: 거리 대치 구도. 두 마스코트가 번갈아 카메라를 응시하며 대사를 치는 토키(talky) 배틀 구조
- 촬영 문법: handheld film realism. movement의 story function: 블러와 흔들림이 "날것의 현장감"으로 기능 ("looks like real unedited footage")

### 6. Spatial / Continuity
사용 채널: identity (@[Image1/2] — 유지됨 ✓), environment (@[Image3/4/5], "identical every gen" — KFC·맥도날드 매장 외관 유지됨 ✓), weather ("Same rain intensity in every shot" — 젖은 아스팔트·회색 하늘 유지됨 ✓), staging (fixed — "never together in the middle" — 전 구간 거리 대치 유지 ✓), tone/grade ("NO color grading" — 모션블러·거친 질감 ✓). STAGING의 위치 고정 + 금지 구역 선언이 69.5초 연속성의 뼈대로 동작.

### 7. Action grammar
- 핵심: **conflict premise + escalation** — "음식 던지기 결투"라는 단 하나의 충돌 전제 + 비대칭 투사체. 프롬프트는 개전(Shot 1·2)만 주고, 에스컬레이션(너겟 포격 → 거대 버거 → 추격)은 모델이 채움
- Shot 1의 마이크로비트 체인: impact(버거가 얼굴에) → slow peel(천천히 흘러내림) → tremble escalation(vein/jaw/nostrils/eye/knuckles의 신체 나열) → breath(이를 악문 느린 호흡) → suppressed line — 분노를 폭발이 아닌 억제로 연출. EMOTION=BODY의 실전 적용
- anticipation → contact → consequence: 투사체 발사(anticipation) → 명중(contact) → 거대화 반격(consequence)의 체인이 배틀 전체에 반복
- 대사는 배틀의 비트 마커로 기능 (도발 → 에스컬레이션 선언)
- action density: 높음 — 69.5초 내내 투사체·추격·거대 오브젝트. motion budget이 액션에 전부 할당되고 카메라는 관찰자에 머무름

### 8. Reference usage
- @[Image 1](image_1) = Colonel, @[Image 2](image_2) = Clown (character-only) / @[Image 3](image_3) = wide street, @[Image 4](image_4) = KFC Store, @[Image 5](image_5) = McDonald's Store (environment-only) / @[Audio 1](audio_1) = Colonel voice, @[Audio 2](audio_2) = Clown voice (voice-only) — 인덱스 범위 자체가 역할을 분리. Reference Role Separation의 교과서적 사례
- 보이스까지 역할 분리에 포함된 점이 특기

### 9. Audio / Dialogue
- dialogue: 2개 (prompt-derived). "You brought a Happy Meal to a gunfire, boy." (억제된 분노 — "low and quaking with barely-contained fury") / "What about a cannon?" (howl + 무릎치기). 렌더 여부는 프레임으로 검증 불가 — 미확인
- voice: 캐릭터별 1:1 매핑 + "not flat TTS" + "the emotion of each line matches the action on screen (furious, taunting, straining, weak, smug)" — 대사의 감정을 화면 액션에 매칭시키는 규칙
- music: "no music or score" — 명시적 금지
- ambience: diegetic only — "steady rain, footsteps in puddles, food whooshes, wet impacts and splashes, street tone" (나열형 diegetic spec)
- beat sync: 없음 (카메라 푸시의 임팩트 타이밍이 리듬 역할을 대신)

### 10. Failure prevention
실패 기반 네거티브 (정본에서 직접 확인 — prompt-derived):
- "not flat TTS" — TTS 특유의 평탄한 낭독 실패를 겪어본 문장
- "never animated-looking" — 코믹 연기가 카툰화로 붕괴하는 실패를 막는 스타일 상한선
- "NO color grading — looks like real unedited footage, not glossy, not graded" — AI 특유의 광택 그레이딩 실패를 막는 anti-gloss 락
- "not a downpour, kept light enough to read faces" — 이유가 명시된 제약 (얼굴 판독 가능성). 제약+이유의 결합형
- "No on-screen text or subtitles." — 화면 텍스트 seep 방지 (명시적)
- generic negative: 없음
관찰된 성공 (frame-observed): 간판 텍스트(KFC·McDonald's)가 환경의 일부로 판독 유지 — 추가 그래픽 텍스트·자막 없음 ✓ ("No on-screen text" 준수). 캐릭터 photoreal 유지 ✓ ("never animated-looking" 준수).

### 11. Control Levels
- Hard Lock: @[Image1/2] 캐릭터 identity, @[Image3/4/5] 환경 ("identical every gen"), STAGING fixed ("never together in the middle"), 캐릭터별 연기 형용사, EMOTION=BODY 신체 채널, raw film look + rainy day ("NO color grading"), "No on-screen text or subtitles", "no music or score"
- Soft Guidance: Shot 1·2 서술, 대사 2개 + 감정 지정, 보이스 매핑, diegetic 사운드 나열, 카메라 무브 어휘
- Creative Freedom: Shot 3 이후의 배틀 전개 전체 — 모델이 에스컬레이션을 창작 (69.5초 중 대부분)

### 12. Why it may work
A. Evidence-backed:
- 두 캐릭터가 69.5초 전 구간에서 식별 유지 (frame-observed) — 레퍼런스 분리가 장척에서도 동작
- STAGING fixed가 지켜짐 — 전 구간 거리 대치, 중간에서 합류 없음 ✓
- rainy + raw film 룩이 전 구간 유지 — "Same rain intensity in every shot" 준수 ✓
- "never animated-looking" 준수 — photoreal 유지 ✓ / 추가 텍스트·자막 없음 ✓

B. Inference:
- IP 마스코트는 모델에게 가장 강한 visual prior 중 하나 — identity 유지 부담이 텍스트 서술 대비 현저히 낮을 수 있음
- "충돌 전제 하나 + 연기 톤 둘 + 고정 스테이징"의 최소 스펙이 오히려 장척 연속 액션을 가능하게 함 — 매 샷을 지정하지 않았으므로 모델이 자신의 강점(연속 모션 생성)으로 메움. 단, 추론은 규칙으로 승격하지 않음
- EMOTION=BODY는 감정 라벨("angry") 대신 신체 채널을 나열하므로 모델이 "어떻게 보여줄지"를 직접 추론하지 않아도 됨 — 라벨→표현의 추론 단계를 제거한 구조일 수 있음 (inference)

### 13. Popularity signal
- likes: 122 (스냅샷 기준 position 3)
- likely_driver: visual_subject (실존 브랜드 마스코트 결투 — 썸네일/첫인상의 즉각적 인지), novelty (패스트푸드 마스코트 음식 배틀 컨셉), unknown (prompt_structure — 인과 근거 없음)
- 판단: 컨셉의 즉각성과 IP 인지가 인기에 기여했을 가능성. 프롬프트 구조 기여도는 단정 불가

### 14. Relation to existing XAI-Studio patterns
- Reference Role Separation: 강화 — 인덱스 그룹별 역할 분리의 가장 명시적 사례 (캐릭터/환경/보이스 3종)
- Spatially Anchored Scene: 강화 — STAGING fixed ("always at X", "never together in the middle")는 블로킹 수준의 공간 고정으로 확장
- Relative Spatial Coordinates: 강화 — "facing across the street", "each keeps his own store visible behind him" (상대 위치 + 배경 유지 조건)
- 캐릭터별 연기 지정: #41 (emotion performance)의 캐릭터별 분리 버전으로 강화
- Hard/Soft/Creative: 강화 — Creative Freedom 구간(Shot 3 이후)이 전체의 대부분을 차지하는 극단적 배분 사례
- Failure-Sourced Negatives: 강화 — "not flat TTS", "never animated-looking", "NO color grading", 이유 명시 제약("kept light enough to read faces")의 새 표본
- 트리거 문법: "snap pushes timed to throws/catches/impacts" — 카메라 무브의 임팩트 타이밍 바인딩으로 강화 (C03 per-shot SFX의 카메라 버전)

### 15. Candidate contribution
- new rule 후보: **EMOTION = BODY (not labels)** — 감정을 라벨이 아닌 신체 채널 나열(eyes, brows, mouth, head tilt, hands, shoulders, stance)로 지정. #41의 emotion performance를 명명된 규칙으로 정식화한 사례. (최종 D에서 검토)
- new rule 후보: **idle-life rule** — "Keep both characters alive in every shot even when still: breathing, blinks, small weight shifts" — 정지 상태에서도 캐릭터를 살려두는 최소 생명 유지 규칙. (최종 D에서 검토)
- new rule 후보: **fixed staging declaration** — "STAGING (fixed): always at X, never together in the middle" — 위치 고정 + 금지 구역의 블로킹 락. Spatially Anchored Scene의 블로킹 버전. (최종 D에서 검토)
- 그 외 reinforces existing patterns
- 방법론적 관찰 (규칙 아님): 프롬프트는 2샷만 기술했으나 영상은 69.5초 — under-specification + model continuation 사례. 강한 identity lock(IP + 분리 레퍼런스) + 단일 충돌 전제 + 고정 스테이징이 있으면 모델이 장척을 자립 생성할 수 있다는 관찰. 단일 표본이므로 패턴으로 승격하지 않음

---
## Case 15 — Ruzaina "A young creator walks into a bright living room holding a..." [신규 수집분]

### 1. Source
- URL: https://www.meigen.ai/video/2078048308707414389
- creator: Ruzaina (@RuzainaMeer)
- model: Seedance (갤러리 기본 탭 기준, author-described)
- duration: 12.08초 실측 (290프레임/24fps/1280x720)
- popularity: 120 likes (2026-09-26 21:14 KST 스냅샷 기준 Popular position 4)

### 2. Evidence basis
- prompt-derived (전문 확보 — parent 제공 verbatim)
- frame-observed (컨택트시트 + 8프레임 중 f008 확인). 프롬프트와 매칭됨 — 제품 히어로샷, 엔딩 텍스트 렌더 확인
- inference: Why it may work B항
- audio: 프레임만으로 검증 불가 — 대사·음악 렌더 여부는 미확인으로 기록

### 3. Prompt structure
단일 문단, 단일 문장들의 나열. 정본 기준 구조 분해:
- opening beat: "A young creator walks into a bright living room holding a pair of sleek wireless earbuds still inside their charging case." — 입장(entrance)으로 시작. 주어가 "they"로 성별 무지정
- gaze+line beat: "Looking directly into the camera, they smile and say, 'These have honestly become my everyday essential.'" — 렌즈 응시 + 미소 + 대사를 한 비트에 결합. 오프닝 후킹 비트
- demo chain: "They open the case, put the earbuds in, and instantly transition into a quick montage of working on a laptop, making coffee, and taking a short walk outside while music plays." — "instantly transition into a quick montage" 명시적 전환 선언 + 몽타주 3비트(노트북 작업·커피·야외 산책) + "while music plays" (몽타주 구간 음악 지정)
- product close-up purpose clause: "Close-up shots highlight the earbuds' premium design and secure fit." — 클로즈업의 목적을 명시 (디자인 + 착용감)
- toward-camera presentation: "The creator finishes by holding the charging case toward the camera and says, 'Great sound, all-day comfort, and I barely need to recharge them.'" — 제품을 카메라를 향해 내미는 피날레 + 클레임 3종(sound·comfort·battery)을 대사 한 줄에 압축
- ending lock: 'End with a clean product hero shot on a table and on-screen text: "Upgrade your everyday audio."' — "End with" 명시적 엔딩 지정 + 히어로샷 + 화면 텍스트
- style tail: "Natural facial expressions, smooth handheld camera movement, cinematic depth of field, authentic UGC feel, high-quality audio, realistic lighting, premium commercial quality." — 날것("Natural", "authentic UGC feel")과 프리미엄("cinematic depth of field", "premium commercial quality")을 한 문장에 병치한 tone duality
- 없음: 섹션 라벨, 타임스탬프, negative constraints, 레퍼런스 문법

### 4. Subject / Character state
- identity lock: 레퍼런스 문법 없음 (텍스트 전용). 주어가 성별 무지정 "they"/"a young creator"
- 렌더 결과 (frame-observed): 8프레임 전 구간에서 동일 청년(밝은 셔츠, 같은 얼굴) 유지 ✓ — 텍스트 서술만으로 12초 identity가 유지된 사례
- wardrobe lock: 밝은 셔츠 — 유지됨 ✓
- prop lock: 이어버드 + 케이스 — 다크 컬러 제품으로 전 구간 일관 ✓. "holding the charging case toward the camera" 피날레가 렌더됨 ✓
- gaze assignment: "Looking directly into the camera" — 오프닝 1비트에 렌즈 응시 지정 (#42의 유일 응시와 동형)
- performance note: "Natural facial expressions", "they smile" — 자연스러운 표정 지정
- character count: 1

### 5. Camera / Shot design
- multi-shot: 입장(와이드) → 케이스 오픈·착용(미디엄) → "quick montage" 3비트 → 제품 클로즈업 → toward-camera 피날레 → 테이블 히어로샷(정물)
- explicit transition: "instantly transition into a quick montage" — 전환 선언
- camera role: 관찰자 + 제품 매크로. "smooth handheld camera movement" (C14의 shaky와 대조 — 여기서는 smooth) + "cinematic depth of field"
- subject-camera relationship: 오프닝과 피날레에서 카메라를 응시·대면하는 UGC식 정면 컷, 중간은 무의식적인 생활 컷 — tone duality의 카메라 버전
- 촬영 문법: "realistic lighting". movement의 story function: 중립 (제품이 주인공)

### 6. Spatial / Continuity
사용 채널: environment (bright living room — 유지됨 ✓), lighting ("realistic lighting" — 밝은 데이라이트 유지됨 ✓), product (이어버드/케이스 — 유지됨 ✓), wardrobe (밝은 셔츠 — 유지됨 ✓). spatial/topology 락 없음. 단일 집 + 야외 1컷의 짧은 동선이라 연속성 부담이 낮게 설계됨.

### 7. Action grammar
- 핵심: **routine-integrated product demo** — 일상 동작(입장, 케이스 열기, 착용, 노트북 작업, 커피, 야외 산책)이 곧 제품 시연. "quick montage"로 일상을 압축
- claim/action 분리: 대사가 클레임(sound·comfort·battery)을 전달하고 액션은 라이프스타일을 보여줌 — 대사가 설명 부담을 짊어지므로 액션은 단순하게 유지 (motion budget 절약)
- toward-camera presentation: "holding the charging case toward the camera" — 제품을 렌즈를 향해 내미는 광고 피날레 문법
- anticipation → contact → consequence: 케이스 오픈(anticipation) → 착용(contact) → "toward the camera" + 클레임 대사(consequence)
- action density: 낮음 — 12초 광고 규격에 맞는 절제

### 8. Reference usage
- 없음 (텍스트 전용)

### 9. Audio / Dialogue
- dialogue: 2개 (prompt-derived). "These have honestly become my everyday essential." (오프닝, 구어적 진정성 — "honestly") / "Great sound, all-day comfort, and I barely need to recharge them." (피날레, 클레임 3종 압축). 렌더 여부는 프레임으로 검증 불가 — 미확인
- music: "while music plays" — 몽타주 구간에 음악 지정 (장르·BPM 미지정)
- "high-quality audio" — 오디오 품질 스펙
- beat sync: 없음

### 10. Failure prevention
실패 방지 문장 없음. 관찰된 성공 (frame-observed):
- ending text: "Upgrade your everyday audio."가 최종 히어로샷에 판독 가능하게 렌더 ✓ — 텍스트 락 성공
- product consistency: 이어버드·케이스의 형태·컬러가 8프레임 전 구간에서 일관 — 제품 앵커 유지
- "secure fit" — 착용 클로즈업에서 이어버드가 귀에 고정된 모습 ✓ (목적절 "highlight ... secure fit" 준수)
→ C09(Calira 핸드백)의 제품 앵커 성공과 동형

### 11. Control Levels
- Hard Lock: 대사 2개, 엔딩 텍스트 + 히어로샷 ("End with"), tone duality tail, "Looking directly into the camera" (오프닝 응시)
- Soft Guidance: 데모 체인 순서, 몽타주 3비트, "while music plays", 클로즈업 목적절, "toward the camera"
- Creative Freedom: 구체적 동작 디테일, 표정, 야외 컷의 내용, 몽타주 내부 리듬

### 12. Why it may work
A. Evidence-backed:
- 12초 안에 입장→응시+대사→몽타주→클로즈업→toward-camera 피날레→히어로샷+엔딩 텍스트의 완결된 광고 아크가 렌더됨 (frame-observed)
- 제품 identity가 전 구간 유지되고 엔딩 텍스트가 판독됨 — 광고로서의 최소 요건 충족
- tone duality가 렌더에서 확인됨 — UGC식 정면 토크 컷과 프리미엄 정물 히어로샷의 병치

B. Inference:
- claim은 대사, 증거는 액션으로 분리했기 때문에 액션 설계가 단순해도 광고가 성립 — 대사가 무거운 설명 부담을 짊어짐
- UGC register는 AI 특유의 과도한 광택을 "의도된 날것"으로 재해석하게 만들 수 있음 (#45 deliberate imperfection과 동계열의 추론). 단, 추론은 규칙으로 승격하지 않음
- 성별 무지정 주어("they")는 identity 추론 부담을 낮출 수 있음 (inference)

### 13. Popularity signal
- likes: 120 (스냅샷 기준 position 4)
- likely_driver: unknown (인과 근거 없음). visual_subject (깔끔한 프리미엄 룩)는 가능성에 불과
- 판단: 광고 아크의 완결성은 확인되나, 인기와 프롬프트 품질의 인과관계는 단정 불가

### 14. Relation to existing XAI-Studio patterns
- Routine Montage: 강화 — 일상 루틴 동작에 제품을 통합하는 데모 문법 ("quick montage" 명시 선언 포함)
- 제품 앵커: C09 (Calira 핸드백)와 동형 — 12초 제품 identity 유지 성공으로 강화
- ending text lock: C10의 "THE END!" 텍스트 제약과 동형 — 화면 텍스트 seep 없이 렌더된 성공 사례로 강화
- toward-camera presentation: 제품을 렌즈 향해 내미는 피날레 — 기존 제품 앵커 패턴의 제스처 버전으로 강화 (new rule 아님)
- tone duality ("authentic UGC feel" + "premium commercial quality"): #45 deliberate imperfection의 상업광고 버전으로 강화 (new rule 아님)
- claim/action 분리: 대사가 설명을 담당하는 구조 — 기존 패턴의 변형으로 강화
- 오프닝 렌즈 응시: #42의 "유일 응시" 강화 ("Looking directly into the camera")

### 15. Candidate contribution
- reinforces existing patterns. 신규 규칙 없음
- 대조 표본으로서의 가치: 텍스트 전용 identity 서술 + 성별 무지정 + 12초 + 단일 문단으로도 인물·제품·엔딩 텍스트가 모두 유지된 최소 스펙 성공 사례. "짧고 단순한 프롬프트도 광고 아크를 완결할 수 있다"는 하한선 데이터로 기록

---
## Case 16 — Avelyrah "A stylish young woman walking confidently down a busy New..." [신규 수집분]

### 1. Source
- URL: https://www.meigen.ai/video/2094420859960045616
- creator: Avelyrah (@AvelyrahnAI)
- model: Seedance (갤러리 기본 탭 기준, author-described)
- duration: 12.08초 실측 (290프레임/24fps/720x1280 — 9:16 세로, 실측 기준)
- popularity: 119 likes (2026-09-26 21:14 KST 스냅샷 기준 Popular position 5)

### 2. Evidence basis
- prompt-derived (전문 확보 — parent 제공 verbatim)
- frame-observed (컨택트시트 + 8프레임 중 f004 확인). 프롬프트와 매칭됨 — 정지 비트, 매크로 인서트, 브랜드 텍스트 렌더 확인. 단, 마지막 "댄스"는 프롬프트에 없음 (아래)
- inference: Why it may work B항
- audio: 프레임만으로 검증 불가 — 미확인

**Prompt–video note (frame-observed):** 프롬프트는 "everything drops back to the pavement"에서 끝나며 댄스를 언급하지 않음. 그런데 최종 프레임에서 여성이 양팔을 든 축하/댄스풍 포즈를 취함 — 모델이 Creative Freedom 구간에서 추가한 릴리스 비트로 기록. 프롬프트 귀속이 아니므로 구조 분석에서 분리.

### 3. Prompt structure
단일 문단, 사실상 한 문장(세미콜론 연결). 정본 기준 구조 분해:
- subject block: "A stylish young woman walking confidently down a busy New York city sidewalk during golden hour, wearing a dark fitted t-shirt, relaxed dark jeans, and sneakers, talking on her smartphone and holding an iced coffee and a cafe menu, with a golden retriever dog walking on a leash beside her" — 인물+의상 3종(명시적) + 동시 수행 3중 액션(통화 중·커피·메뉴 소지) + 보조 subject(개, 리드줄 명시)
- trigger: "suddenly, she trips and drops her phone, iced coffee cup, and a 'YA HALA COFFEE - FALL MENU' flyer mid-stride" — "suddenly" 트리거 + "mid-stride" 타이밍 정밀도. 손에 든 "a cafe menu"가 떨어지는 순간 브랜드명을 가진 "flyer"로 특정됨 — 브랜드 reveal이 낙하 비트에 타이밍됨
- freeze block: "causing the items to suspend mid-air in slow motion with magical liquid splashes and floating autumn leaves" — 시간 조작(slow motion) + 마법 요소(liquid splashes, autumn leaves). 인과 연결사 "causing"으로 트립→정지를 묶음
- macro transition: 'transitioning to a macro close-up of the branded coffee cup and a smartphone displaying an incoming call from "BOSS"' — "transitioning to" 명시적 전환 + 매크로 인서트 2종(브랜드 컵 / "BOSS" 수신전화 화면). 폰 화면이 서사 비트
- resume: "before everything drops back to the pavement" — "before"로 정지→낙하 재개를 연결
- style tail: "in a dynamic, high-octane commercial cinematic style" — 커머셜 톤 선언
- 없음: 섹션 라벨, 타임스탬프, negative constraints, 대사, 9:16 지정 (세로는 실측 결과)

### 4. Subject / Character state
- identity lock: 레퍼런스 문법 없음 (텍스트 전용)
- wardrobe lock: "a dark fitted t-shirt, relaxed dark jeans, and sneakers" — 3종 명시. 렌더 결과 (frame-observed): 전 구간 유지 ✓
- prop lock: 폰, iced coffee cup, cafe menu/flyer — 세 프롭이 비트마다 일관되게 등장. 낙하 순간 "cafe menu" → "'YA HALA COFFEE - FALL MENU' flyer"로 브랜드 특정 (관찰)
- secondary subject: "a golden retriever dog walking on a leash" — 전 구간에서 같은 개로 유지 ✓ (보조 subject의 연속성도 지켜짐)
- gaze assignment: 없음
- character count: 1 (+ 개 1)

### 5. Camera / Shot design
- 9:16 세로 — 실측 기준 (프롬프트에 지정 없음). 플랫폼 네이티브 규격이 렌더 기본값으로 적용된 사례
- continuous take + time-ramp: 트립 순간에 slow-mo freeze로 시간 조작, "transitioning to" 매크로 인서트 2개(컵·폰 화면), "drops back to the pavement"으로 재개
- camera role: 추적 관찰자. freeze 구간에서는 카메라가 제품 매크로로 전환 — "시간이 멈추면 카메라가 제품을 본다"는 상업 문법
- subject-camera relationship: 인물이 카메라를 응시하지 않음 — 제3자 관찰 시점
- 촬영 문법: 골든아워 (frame-observed — 따뜻한 톤 유지 ✓). movement의 story function: freeze가 시선을 제품으로 강제 이동

### 6. Spatial / Continuity
사용 채널: location (busy New York city sidewalk — 유지됨 ✓), time/light (golden hour — 따뜻한 톤 유지됨 ✓), product text props (전단지·컵 로고 판독 유지 ✓), wardrobe (3종 유지됨 ✓), secondary subject (개 — 유지됨 ✓). spatial/topology 락은 없으나 단일 거리 연속 테이크라 부담이 낮음.

### 7. Action grammar
- 핵심: **trip → freeze → inspect → fall** — 4비트 체인 ("suddenly" 트리거 → "causing" 인과 → "transitioning to" 매크로 → "before" 재개). 접속사(suddenly/causing/transitioning to/before)가 비트 간 인과·전환을 문법적으로 고정 — 단일 문장 안에서 시간 구조를 완성
- C05의 world-freeze와 동형 — 단, 여기서는 freeze가 렌더에서 완전히 동작 (폰·커피·전단지가 공중에 정지, f004 확인)
- freeze 구간의 정지물은 "움직이지 않는 피사체"라 텍스트(브랜드 로고·"BOSS")가 흔들림 없이 판독 — 시간 조작이 텍스트 렌더의 안정화에 기여한 구조
- "magical liquid splashes": 컵 매크로에서 액체 스플래시 확인 (frame-observed). "floating autumn leaves"는 확인한 프레임에서 미확인 — prompt-derived로만 기록
- 마지막 댄스풍 포즈: 프롬프트에 없음 — 모델이 추가한 릴리스 비트 (frame-observed, Creative Freedom). 구조 분석에서 프롬프트 귀속과 분리
- action density: 중간 — 한 문장에 4비트 + 매크로 2개. motion budget이 freeze(정지)와 낙하(동적)에 분배

### 8. Reference usage
- 없음 (텍스트 전용)

### 9. Audio / Dialogue
- dialogue: 없음
- phone-screen beat: "a smartphone displaying an incoming call from 'BOSS'" — 청각이 아닌 시각적 서사 비트. 전화벨 소리 지정은 없음
- music/beat sync: 언급 없음. "high-octane"은 톤 선언이지 비트 싱크 지정이 아님

### 10. Failure prevention
실패 방지 문장 없음. 관찰된 성공 (frame-observed):
- branded text legibility: "YA HALA COFFEE - FALL MENU" 전단지와 컵 로고가 매크로에서 판독 가능 — text seep/mirror-text 없음. C02(거울반전 포스터)의 반대 사례
- "BOSS" 폰 화면 텍스트 판독 ✓
- freeze 물체의 공중 정지 — 물리 붕괴 없이 유지
→ 텍스트 프롭이 많은 프롬프트임에도 텍스트 실패가 없었음 — freeze(정지) 구간이 텍스트 안정화에 기여했을 가능성 (inference, 규칙 아님)

### 11. Control Levels
- Hard Lock: 제품 텍스트 프롭("YA HALA COFFEE - FALL MENU"), freeze 비트 ("suspend mid-air in slow motion"), "BOSS" 수신전화 매크로, 의상 3종, "golden hour"
- Soft Guidance: 4비트 액션 체인 (접속사로 연결), "dynamic, high-octane commercial cinematic style", 개 동반
- Creative Freedom: freeze 물체의 배치, 행인, 마지막 댄스풍 포즈 (모델 추가)

### 12. Why it may work
A. Evidence-backed:
- freeze 비트가 렌더에서 완전히 동작 — 폰·커피·전단지가 공중에 정지 (f004, frame-observed)
- 매크로 인서트 2개(브랜드 컵, "BOSS" 화면)가 렌더됨 — 제품 검수 비트 동작
- 브랜드 텍스트가 판독 가능 — 텍스트 프롭 앵커 성공
- 한 문장(세미콜론 연결) 안에 trigger→freeze→macro→resume의 완결 구조 — 접속사가 시간 구조를 고정

B. Inference:
- freeze는 모델에게 "정지된 정물" 구간을 줌 — 움직이는 텍스트보다 정지된 텍스트가 렌더 안정성이 높을 수 있음. 텍스트 프롭 광고에서 시간 조작이 품질에 기여하는 구조일 수 있음. 단, 추론은 규칙으로 승격하지 않음
- "suddenly / causing / transitioning to / before"의 접속사 체인은 샷 리스트 없이도 시간 순서를 강제 — 섹션 라벨의 경량 대체제로 기능할 수 있음 (inference)

### 13. Popularity signal
- likes: 119 (스냅샷 기준 position 5)
- likely_driver: visual_subject (공중 정지 모먼트 — 썸네일/첫인상의 강렬함), novelty (타임프리즈 + 매크로 인서트), unknown (prompt_structure — 인과 근거 없음)
- 판단: 정지 비트의 시각적 후킹이 인기에 기여했을 가능성. 프롬프트 구조 기여도는 단정 불가

### 14. Relation to existing XAI-Studio patterns
- 제품 앵커: C09 (Calira), C15 (이어버드)와 동형 — 텍스트 프롭(전단지·컵 로고) 버전으로 강화
- world-freeze beat: C05와 동형 — C05는 핵심 이펙트 미렌더였으나 여기서는 성공. 성공/실패 대조 쌍으로 강화
- text-in-frame 성공: Failure-Sourced Negatives의 대조 표본 (C02 text seep의 반대 증거)
- phone-screen-as-story-beat: 폰 화면을 서사 비트로 쓰는 구조 — 기존 패턴의 변형으로 강화 (new rule 아님)
- 접속사 체인 시간 구조: 섹션 라벨 없이 시간 순서를 고정한 경량 문법 — 기존 샷 리스트 패턴의 변형으로 강화

### 15. Candidate contribution
- reinforces existing patterns. 신규 규칙 없음
- 대조 표본으로서의 가치: (1) C05 world-freeze의 성공 버전 — 동일 디바이스의 성공/실패 쌍 완성, (2) C02 text seep의 반대 증거 — 브랜드 텍스트가 판독된 사례, (3) 마지막 댄스풍 포즈는 프롬프트에 없는 모델 추가 비트 — Creative Freedom 구간의 자립 생성 관찰로 기록, 규칙화하지 않음

---
