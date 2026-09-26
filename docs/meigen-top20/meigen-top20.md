# MeiGen Top 20 Video Prompts — 구조적 패턴 채굴
작업 지시: XAI-Studio-Video 재사용 가능한 구조적 패턴 추출. 인기 ≠ 품질.
증거 기반: frame-observed / prompt-derived / author-described / text-guide / inference.
추론은 production rule로 승격하지 않는다. SKILL.md 확정 금지.

---

## Case 01 — Shore Lyn "PART 1 (0:00–0:15)" [rank 1]

### 1. Source
- URL: https://www.meigen.ai/video/2073631781644021850
- creator: Shore Lyn (@Shorelyn_)
- model: Seedance (MeiGen 배지)
- duration: 35.96초 실측 (863프레임/24fps/1276x718). 타이틀 "(0:00–0:15)"와 불일치
- popularity: rank 1, 237 likes (조회수 미표시)

### 2. Evidence basis
- prompt-derived (프롬프트 전문 확보)
- author-described (타이틀·모델 배지)
- frame-observed — 단, 프롬프트 검증용으로 사용 불가. 예시 영상이 프롬프트와 전혀 무관 (아래 "Gallery mismatch" 참조). 프레임은 mismatch 증거로만 기록
- inference: Why it may work B항

**Gallery mismatch (frame-observed):** 예시 영상 36초 전체가 밤의 드리프트 영상 — 흰색 "46" 그래피티 차량, 안경·타투의 애니메풍 운전자, 야간 시가지·다리. 프롬프트의 지중해 여행 셀피(여성, 보트, 야시장, 해변)와 겹치는 요소 0. 프롬프트-영상 불일치가 갤러리 차원에서 발생. 이 케이스의 인기는 프롬프트 품질의 증거로 쓸 수 없음.

### 3. Prompt structure
단일 문단, 약 270단어. 구조 분해:
- subject/identity block: "@image1 (uploaded photo)... the same woman from the reference image"
- wardrobe lock block: 4개 아이템 나열 (light-blue sleeveless top / sunglasses on head / silver necklace / pink mini shoulder bag strap)
- camera POV declaration: "The camera is a front-facing selfie perspective, held in her hand at arm's length"
- scene chain (시간 순서, 타임스탬프 없음): extreme close-up looking away → "for one heartbeat" eye-lock + half-smile → "Cut to:" over-the-shoulder (Mediterranean old town) → "Cut to:" montage (boat / cliffside golden hour / night market / beach sunset) → "End with a cinematic action shot"
- technical direction block: handheld selfie realism — slight natural shake, occasional focus pulls, lens flares
- grade block: 4K, shallow DOF, cinematic color grade (warm highlights, teal shadows), 24fps
- audio block: "Muffled city ambience, wind, laughter, distant music — raw and unpolished like a real vlog"
- 없음: negative constraints, reference role separation(@image1 단일), shot별 렌즈, 절대 타임스탬프

### 4. Subject / Character state
- identity lock: @image1 (platform syntax) — 있음
- wardrobe lock: 4개 아이템 명시 — 있음 (Hard Lock에 가까움)
- prop lock: sunglasses on head (착용 위치 지정)
- pose/motion identity: 셀피 퍼포먼스 (웃음, 카메라를 향해 돌아보기)
- gaze assignment: "for one heartbeat — her eyes lock with the viewer" — 렌즈 직접 응시를 1비트로 지정 (#42의 유일 응시와 동형)
- character count: 1
- role separation: 해당 없음

### 5. Camera / Shot design
- multi-shot (암시적): "Cut to:" ×3
- explicit cuts: "Cut to:" — 액션 트리거 없음, 단순 장면 전환 선언
- camera role: 그녀 자신의 손 (selfie grammar) — 카메라=주체의 신체 연장
- framing progression: ECU (face looking away) → eye-lock → over-the-shoulder → montage (mixed) → action shot
- subject-camera relationship: 셀피 — 피사체가 카메라를 들고 있음
- handheld/selfie 문법. camera movement의 story function: "raw and unpolished like a real vlog" — 흔들림이 진정성(authenticity)의 증거로 기능 (#45 deliberate imperfection과 동계열)

### 6. Spatial / Continuity
실제로 사용된 채널: identity (@image1), wardrobe (4아이템), tone/grade (warm highlights, teal shadows). spatial/topology, prop 상태, lighting 채널의 명시적 락 없음. 몽타주 특성상 연속성 요구가 낮게 설계됨.

### 7. Action grammar
- 단순 결과 지시 + 퍼포먼스 동사 나열 (laughing, waving 아님 — turning, raising camera, dancing, spinning)
- micro-beat: "for one heartbeat — her eyes lock" — 시선을 시간 단위(heartbeat)로 지정. 상태 전이는 없음
- anticipation → contact → consequence 구조 없음
- action density: 낮음 (분위기·장소 나열 중심)

### 8. Reference usage
- @image1 = identity-only. 단일 authority. 역할 분리 없음

### 9. Audio / Dialogue
- dialogue: 없음 (No dialogue 명시)
- ambience: muffled city ambience, wind, laughter, distant music
- music: "distant music" — 배경 수준
- beat sync: 없음
- camera rhythm-오디오 연동: 없음

### 10. Failure prevention
실패 방지 문장 없음. generic negative도 없음. 주목할 부재.

### 11. Control Levels
- Hard Lock: @image1 identity, wardrobe 4아이템
- Soft Guidance: 장면 체인, 셀피 POV, imperfection spec, 컬러그레이드
- Creative Freedom: 몽타주 세부, 표정 디테일, "cinematic action shot"의 내용

### 12. Why it may work
A. Evidence-backed:
- 프롬프트에서 직접 확인: 구체적 의상 4종, 구체적 장소 5곳, 구체적 퍼포먼스 동사, imperfection spec ("slight natural shake, occasional focus pulls") — 모호한 형용사 대신 명사가 박혀 있음
- 단, 예시 영상이 불일치하므로 렌더 검증 불가

B. Inference:
- 셀피+여행 몽타주는 검증된 바이럴 원형. "for one heartbeat" eye-lock은 초반 후킹 비트로 모델 친화적 (단일 명확 지시)
- imperfection spec은 AI 특유의 과도하게 깨끗한 룩을 깨는 방향 — #45와 같은 계열의 추론
- 단일 문단·단일 인물·현실 로케이션 = 모델의 실패 표면이 작음

### 13. Popularity signal
- rank: 1 / likes: 237
- likely_driver: visual_subject (갤러리에 표시되는 예시 영상은 화려한 드리프트 영상 — 프롬프트와 무관), creator_reach (Shore Lyn은 10위권에 2개 진입), unknown (prompt_structure는 근거 없음)
- 판단: 이 케이스의 인기를 프롬프트 품질과 연결할 근거 없음

### 14. Relation to existing XAI-Studio patterns
- Identity-Locked Lifestyle: 강화
- Front-Covered Experience Vlog: 강화 (셀피 문법)
- Travel Coverage: 강화
- "PART 1" 타이틀: Series Master → Variant 패턴 강화
- Hard/Soft/Creative: 강화
- eye-lock 1비트: #42의 "유일 응시" 강화 (new rule 아님)

### 15. Candidate contribution
- reinforces existing patterns. 프롬프트 규칙으로서의 신규 기여 없음
- 방법론적 기여: 갤러리 예시 영상이 프롬프트와 불일치할 수 있음 → evidence-basis 규율의 필요성을 입증한 케이스. "예시 영상이 있다" ≠ "프롬프트가 검증됐다"

---
## Case 02 — Sairah "Setting: A cozy indoor room..." [rank 2]

### 1. Source
- URL: https://www.meigen.ai/video/2087136847734734939
- creator: Sairah (@Sairah_0)
- model: Seedance
- duration: 26.97초 실측 (809프레임/30fps/1276x718)
- popularity: rank 2, 219 likes

### 2. Evidence basis
- prompt-derived (전문 확보)
- frame-observed (27프레임 추출 + 컨택트시트 + 18초 확대 프레임). 프롬프트와 매칭됨 — 단, 부분 드리프트 관찰 (아래)
- inference: Why it may work B항

### 3. Prompt structure
단일 문단, 섹션 라벨 방식. 구조 분해:
- Setting block (장소): cozy indoor room, warm ambient lighting, plush carpet, shelf decor
- Character block: young girl, bright orange hoodie "MOMI 02", blue denim jeans
- Action block: dances hip-hop, smiles, expressive hand gestures "to the rhythm of the music"
- Visual Effect block (핵심): "Every time she moves her hands, vibrant graffiti-style animations and colorful doodles appear and swirl around her in sync with her movements" — VFX를 신체 트리거에 바인딩
- style spec: playful, bold outlines, neon colors, abstract shapes/stars/swirls/motion lines "follow her hand gestures precisely"
- Camera block: mostly static, slight follow to keep centered; occasional close-ups on hands "emphasize the graffiti effects blooming from her fingertips"
- Mood block: fun, youthful, vibrant
- ending condition: "smoothly blending back into real life by the end of the clip"
- 없음: negative constraints, 타임스탬프, 대사, 레퍼런스 지정

### 4. Subject / Character state
- identity lock: 없음 (레퍼런스 이미지 없음, 텍스트 서술만)
- wardrobe lock: 시도됨 — "bright orange hoodie with 'MOMI 02', blue denim jeans"
- 렌더 결과 (frame-observed): 회색 후디로 드리프트, "MOMI 02" 텍스트 없음, 청바지 미노출 (상반신 위주). wardrobe lock 실패 사례
- character count: 1 (+ VFX 그래픽)
- gaze assignment: 없음 (카메라를 보는 장면 있으나 지정 없음)

### 5. Camera / Shot design
- single shot (사실상): static, slight follow. "Occasional close-ups on hands" — 렌더에서는 클로즈업 컷 없이 단일 샷 유지
- camera role: 관찰자 (fixed observer)
- subject-camera relationship: 정면, 중앙 유지
- 촬영 문법: static + slight follow. movement의 story function: 중립 (VFX가 주인공이므로 카메라는 방해하지 않음)

### 6. Spatial / Continuity
사용 채널: identity (약함 — 텍스트 서술만), wardrobe (시도, 실패), lighting (warm ambient — 유지됨 ✓), environment (cozy room — 유지됨 ✓). spatial/topology 락 없음.

### 7. Action grammar
- 핵심: **trigger→effect coupling** — "Every time she moves her hands, [VFX] appear ... in sync with her movements". VFX의 발생 조건을 신체 부위(손)의 움직임에 바인딩. #1의 CUT-as-trigger, #46의 CUT ON과 같은 "트리거 문법" 계열 — 여기서는 컷이 아니라 이펙트의 트리거
- "blooming from her fingertips" — 이펙트의 발생 지점까지 지정 (손끝)
- 단순 결과 지시 + 상태 서술 혼합. anticipation→contact→consequence 없음
- motion budget: 단일 인물 댄스, 카메라는 정적 — VFX에 예산 집중

### 8. Reference usage
- 없음 (텍스트 전용)

### 9. Audio / Dialogue
- dialogue: 없음
- music: "the rhythm of the music" — 언급만, BPM·장르·싱크 지정 없음
- beat sync: 없음 (음악이 있다는 전제만)
- camera rhythm-오디오 연동: 없음

### 10. Failure prevention
실패 방지 문장 없음. 관찰된 실패 (frame-observed):
- wardrobe color drift: orange → gray
- effect style mutation: graffiti doodles → anime character overlay (Spider-Gwen풍 캐릭터 + 거대 카툰 손)
- scale drift: 손 그래픽이 비정상적으로 거대화
- text seep: 포스터의 거울 반전 난독 텍스트
→ "VFX 스타일"을 형용사(graffiti-style, playful)로만 지정했기 때문에 발생한 mutation. 스타일 락의 부재가 실패로 이어진 사례

### 11. Control Levels
- Hard Lock: 없음 (사실상)
- Soft Guidance: 장소, 캐릭터 서술, VFX 트리거 규칙, 카메라 static, 엔딩 조건
- Creative Freedom: VFX의 구체적 형태, 댄스 동작, 색상

### 12. Why it may work
A. Evidence-backed:
- VFX 트리거 규칙("Every time she moves her hands... in sync")이 렌더에서 동작함 — 손 움직임과 그래픽 출현의 동기화가 27초 내내 유지됨 (frame-observed)
- 단일 로케이션 + 정적 카메라 + 단일 인물 = 실패 표면 최소화. 엔딩 조건("blending back into real life")도 렌더에서 지켜짐

B. Inference:
- 트리거 바인딩은 모델에게 "언제 무엇을 할지"를 명확히 줌 — 시간 지정보다 신체 이벤트 기반이라 타이밍 추론 부담이 적을 수 있음
- 형용사 기반 스타일 지정(graffiti-style)은 mutation에 취약 — 관찰된 anime drift가 증거. 스타일을 명사로 고정(예: "flat 2D sticker, thick black outline, no character faces")했으면 덜 drift했을 것이라는 추론. 단, 추론은 규칙으로 승격하지 않음

### 13. Popularity signal
- rank: 2 / likes: 219
- likely_driver: visual_subject (손에서 튀어나오는 애니메이션 — 썸네일/첫인상 강함), novelty (VFX 트리거 컨셉), unknown (prompt_structure)
- 판단: 코어 메커닉이 렌더에서 동작하는 것은 확인되나, 인기와 프롬프트 품질의 인과관계는 단정 불가

### 14. Relation to existing XAI-Studio patterns
- Identity-Locked Lifestyle: 약한 형태 (텍스트 서술만 — 오히려 drift 사례로 기록)
- Trace-first physics: 부분 강화 — 손 움직임이 이펙트의 trace 역할
- "트리거 문법": #1 (CUT-as-trigger), #46 (CUT ON [action])과 동형 — VFX 버전으로 확장. 기존 패턴 강화
- 실패 사례로서의 가치: wardrobe drift, style mutation, text seep — Failure-Sourced Negatives의 새 표본

### 15. Candidate contribution
- new action grammar 후보: **VFX trigger binding** — "Every time [body part] moves, [effect] appears in sync". 트리거 문법의 VFX 이식. (최종 D에서 최대 5개 중 하나로 검토)
- 그 외는 reinforces existing patterns

---
## Case 03 — Sarah "15s / 145 BPM / 15 SHOTS / beat-synced routine" [rank 3]

### 1. Source
- URL: https://www.meigen.ai/video/2042840039378542846
- creator: Sarah (@AIwithSarah_)
- model: Seedance
- duration: 15.1초 실측 (363프레임/24fps/1280x720). "15s" 주장과 일치
- popularity: rank 3, 206 likes

### 2. Evidence basis
- prompt-derived (전문 확보)
- frame-observed (초 단위 15프레임, 주요 샷 6프레임 확인. reference-state-analyses.md #47과 동일 데이터)
- inference: Why it may work B항

### 3. Prompt structure
헤더 + 섹션 라벨 + 15샷 리스트. 구조 분해:
- FORMAT header: "15s / 145 BPM / 15 SHOTS / beat-synced routine" — 길이·템포·샷 수를 포맷 선언에
- SUBJECT: "@[image1] < ATTACH YOUR IMAGE." — 플랫폼 이미지 바인딩 문법
- WARDROBE: 집(잠옷 티+라운지 쇼츠) / 외출(테일러드 재킷+핏티드 탑+트라우저+레이스업 슈즈) — 2상태 의상 선언
- ENVIRONMENT: 6개 로케이션 나열 (tiny apartment → bedroom)
- MOOD: 4비트 감정 아크 ("Late-for-work panic, clipped momentum, breathless urgency, then an exhausted exhale")
- MUSIC: "Fast percussive electro-pop"
- COLOR LOGIC: "Hyperreal Pop Look" — 한 줄 컬러그레이드
- STYLE: "Ultra-Realistic."
- LOGIC RULE: "Keep logical consistency in wardrobe, props, locations, and action continuity across all shots." — 일관성 마스터 스위치
- SHOT 1–15: 각 샷 = [사이즈, 렌즈 mm, 카메라 무브] / 액션 서술 / "/ SFX:" 사운드. 전환 어휘: Cut on action, Match cut, Rhythmic cut, Object pass, Camera wipe, Whip pan transition, Sound bridge, Smash cut, L-cut
- 없음: negative constraints, 대사

### 4. Subject / Character state
- identity lock: @image1 — 있음
- wardrobe lock: 2상태 (집/외출) + SHOT 9에서 전환 명시 ("sleep tee disappears under a fitted top and tailored jacket") — 상태 전이로 잠금
- prop lock: tote, keys, transit card, access card — SHOT 9·13에서 소품 등장·사용 지정
- 렌더 확인 (frame-observed): 핑크 스트라이프 잠옷 → 블랙 테일러드 재킷 → 잠옷 복귀. 의상 아크 유지됨 ✓
- character count: 1
- gaze assignment: "quick clock glance" (SHOT 7), "tense glance toward the closing doors" (SHOT 12) — 기능적 시선. 렌더에서 SHOT 12의 시선은 반사에 가려짐
- role separation: 해당 없음

### 5. Camera / Shot design
- multi-shot: 15샷 명시
- explicit cuts: 전환 어휘 9종 (위). 컷 사이를 편집 문법으로 연결 — #46의 CUT ON [action]이 편집실 어휘로 확장된 형태
- camera role: 관찰자 (핸드헬드/고정 혼합)
- framing progression: ECU(폰) → WS → MCU → Insert(칫솔) → ... → WS(침대). 디테일 인서트 4개 (SHOT 4·6·8·10) — insert-shot economy
- front/rear/side: 정면 위주, SHOT 2 side light, SHOT 8 bird's-eye
- handheld/cinematic: "35mm handheld jolt", "50mm handheld" 등 샷별 지정
- camera movement의 story function: "Rhythmic cut", "whip pan" — 비트 싱크의 도구

### 6. Spatial / Continuity
사용 채널: identity (@image1), wardrobe (2상태+전이), prop (tote/keys/card), location (6곳 순서), lighting (SHOT 15 "cool window light" — 시간대 아크), audio-role (샷별 SFX). tone/grade (Hyperreal Pop Look). 사실상 전 채널 사용 — 15샷 구조에서 가장 넓은 커버리지

### 7. Action grammar
- state transition 중심: 잠옷→외출복→잠옷, 집→지하철→사무실→집
- SHOT 9: "sleep tee disappears under a fitted top" — 의상 전환을 액션으로 서술
- anticipation→contact→consequence: 약함 (루틴 나열형)
- action density: 높음 (15샷/15초 = 1샷/초)
- motion budget: 단일 인물, 로케이션 이동이 예산의 대부분

### 8. Reference usage
- @image1 = identity-only. 단일 authority

### 9. Audio / Dialogue
- dialogue: 없음
- BPM: 145 명시 (헤더). beat sync: "beat-synced routine" 선언 — 단, 샷별 비트 매핑은 없음
- SFX: 샷별 "/ SFX:" 15개 (alarm, sheet rustle / ... / room tone)
- music: "Fast percussive electro-pop"
- ambience/Foley: SFX 리스트에 포함
- camera rhythm-오디오 연동: 선언 수준 ("Rhythmic cut", "Sound bridge", "Smash cut"). 실제 싱크는 미확인 (오디오 미청취)

### 10. Failure prevention
실패 방지 문장 없음. 관찰된 실패 (frame-observed):
- 폰 UI 난독 텍스트 ("Mstrday, Rensey 11 0Y") — #30 재확인
- SHOT 12 시선 지시의 반사 흡수
- generic negative도 없음

### 11. Control Levels
- Hard Lock: FORMAT (15s/145BPM/15샷), 샷별 액션+SFX, LOGIC RULE, 의상 2상태+전이, 06:50 오프닝
- Soft Guidance: Hyperreal Pop Look, 감정 아크, 샷별 렌즈 mm, 전환 어휘
- Creative Freedom: 소품 디테일, 로케이션 세부, 표정

### 12. Why it may work
A. Evidence-backed:
- 15샷 중 확인한 6샷이 프롬프트와 매칭 (SHOT 1 폰 06:50 / SHOT 3 세면 / SHOT 7 토스트+시계 / SHOT 10 부츠 / SHOT 12 지하철 / SHOT 15 침대)
- 의상 아크와 하루 아크(day-cycle bookend: "collapsing into bed in the opening frame shape")가 렌더에서 유지됨
- 1샷/초의 밀도가 15초에 완결되는 구조 — 모델의 drift 누적 시간을 최소화

B. Inference:
- BPM 헤더는 음악 선택의 앵커 — 실제 싱크는 모델이 아니라 편집/음악 선택 단계에서 실현될 가능성. 즉 이 프롬프트는 "생성+후반" 파이프라인을 전제로 설계됐을 수 있음
- LOGIC RULE 한 줄이 15샷의 연속성을 지탱 — 거친 입자의 일관성 지시가 의외로 효과적일 수 있음. A/B 테스트 대상 (종합 F)

### 13. Popularity signal
- rank: 3 / likes: 206
- likely_driver: prompt_structure (샷 리스트의 완성도 — 복사해서 쓰기 쉬움), novelty (BPM 헤더), unknown (visual_subject — 일상 루틴이라 소재빨은 약함)
- 판단: 구조적 완성도가 인기 요인일 가능성이 있으나 단정 불가

### 14. Relation to existing XAI-Studio patterns
- Routine Montage: 강화 (대표 사례)
- Trailer Montage: 부분 강화 (밀도)
- Reference Role Separation: 강화 (@image1 identity-only)
- Hard/Soft/Creative: 강화
- #14 MASTER BEAT SYSTEM과 동형 — 다른 구현 (BPM 헤더 vs 비트 테이블)

### 15. Candidate contribution
- new prompt archetype 후보: **BPM-anchored format header** — "15s / 145 BPM / 15 SHOTS". (최종 D에서 검토)
- new audio rule 후보: **per-shot SFX list** — 샷별 "/ SFX:". (최종 D에서 검토)
- new continuity: **LOGIC RULE one-liner**. (최종 D에서 검토)
- 그 외 reinforces existing patterns

---
## Case 04 — Maria "Instagram fashion reel: 1 shirt, 10 ways" [rank 4]

### 1. Source
- URL: https://www.meigen.ai/video/2073318471849640082
- creator: Maria (@thisismariaa25)
- model: Seedance
- duration: 30.2초 실측 (906프레임/30fps/1920x1080)
- popularity: rank 4, 204 likes

### 2. Evidence basis
- prompt-derived (전문 확보)
- frame-observed (30프레임 컨택트시트. 프롬프트와 높은 매칭)
- inference: Why it may work B항

### 3. Prompt structure
헤더 + 번호 리스트 + 엔딩 조건. 구조 분해:
- hook block: "Create a trendy, ultra-realistic Instagram fashion reel featuring ... showing **10 ways to style the same oversized pastel yellow button-up shirt**"
- audio constraint: "No dialogue, only upbeat viral pop music with clean animated text labels for each look"
- format: "Vertical 9:16" (렌더는 16:9 — 불일치. 아래 참조)
- opening beat: "Open with the influencer holding the shirt on a hanger in a bright, minimalist apartment. She smiles at the camera and tosses the shirt forward as the text **'1 Shirt 🤍 10 Ways to Style'** appears" — 오프닝=액션+텍스트의 결합
- transition block: "smooth whip pans, spin transitions, jump cuts, and snap transitions"
- enumerated look list: 10개, 각 항목 = [룩 이름] – [셔츠 변형] with [하위·액세서리] (명사 수준 구체성)
- performance verb block: walking, posing, spinning, adjusting collar/sleeves, fixing sunglasses, holding coffee, checking mirror, smiling naturally
- shot coverage block: "Mix full-body shots, medium shots, close-ups of fabric, accessories, and outfit details" — Coverage Planning
- grade block: "Bright natural daylight, warm minimalist interiors, luxury Pinterest aesthetic, cinematic handheld, shallow DOF, realistic fabric physics, premium editorial, ultra-realistic 4K HDR"
- ending condition: "End with a quick collage of all 10 looks surrounding the final outfit and the text: **'10 Looks. 1 Shirt. 🤍 Which one's your favorite?'**"
- 없음: negative constraints, 타임스탬프, 레퍼런스 지정

### 4. Subject / Character state
- identity lock: 없음 (텍스트 서술: "stylish Gen Z female influencer")
- wardrobe lock: 단일 아이템 — "oversized pastel yellow button-up shirt". 10개 룩의 공통 분모. 렌더에서 30초 내내 유지됨 ✓ (frame-observed)
- prop lock: 없음 (소품은 룩마다 변경 — 선글라스, 커피, 가방)
- character count: 1
- gaze assignment: "She smiles at the camera" (오프닝) — 렌더에서 정면 응시 다수 ✓
- role separation: 해당 없음

### 5. Camera / Shot design
- multi-shot: 10룩 × (2~3샷) + 오프닝 + 엔딩 콜라주
- explicit cuts: 전환 어휘 나열 (whip pans, spin, jump cuts, snap) — 컷 사이의 문법 선언
- camera role: 관찰자 (편집된 릴)
- framing: full-body / medium / close-up 혼합 — 프롬프트가 직접 지정한 coverage
- opening transition: "tosses the shirt forward" — 오브젝트 토스를 컷의 트리거로 (#47의 "Object pass" 동형)
- handheld/cinematic: "cinematic handheld camera movement"

### 6. Spatial / Continuity
사용 채널: identity (텍스트 — 약함), wardrobe (단일 셔츠 — 강함, 유지됨 ✓), tone/grade (밝은 자연광 — 유지됨 ✓), environment (밝은 미니멀 아파트 — 유지됨 ✓). 룩마다 하의·액세서리 변경이 허용되므로 연속성 부담이 셔츠 1개에 집중 — 설계상 drift 내성

### 7. Action grammar
- opening micro-beat: shirt toss → text appears — 액션과 UI(텍스트)의 결합
- enumerated state changes: 10개 룩 = 10개 상태. 각 상태는 명사 조합으로 정의
- anticipation→contact→consequence: 없음 (카탈로그형)
- action density: 중간 (룩당 2~3 액션)

### 8. Reference usage
- 없음

### 9. Audio / Dialogue
- dialogue: 명시적 금지 ("No dialogue")
- music: "upbeat viral pop music" — 장르/무드만
- beat sync: 없음
- camera rhythm-오디오 연동: 없음
- text-as-audio-substitute: "clean animated text labels" — 대사를 텍스트로 대체. 렌더에서 라벨이 정확히 렌더됨 ✓ (frame-observed: "Look 1 - Casual Chic" ... "Look 8 - French Tuck" 가독)

### 10. Failure prevention
실패 방지 문장 없음. 관찰된 드리프트 (frame-observed):
- format drift: "Vertical 9:16" 지정 → 렌더 16:9. 어스펙트 지시 무시 사례
- 일부 룩의 하의·액세서리가 프롬프트와 미세하게 다름 (룩 9 등)
- 텍스트 렌더는 성공 — seep 사례(#2, #30)와 대조되는 성공 표본

### 11. Control Levels
- Hard Lock: 10개 룩의 명사 정의, 오프닝/엔딩 텍스트, No dialogue
- Soft Guidance: 전환 어휘, 샷 커버리지, 퍼포먼스 동사, 그레이드
- Creative Freedom: 룩별 포즈, 배경 디테일, 음악

### 12. Why it may work
A. Evidence-backed:
- 10개 룩이 각각 2~3초씩 할당되어 30초에 완결 — 룩당 할당 시간이 drift 누적 전에 컷으로 리셋됨
- 단일 셔츠가 30초 내내 유지됨 (frame-observed) — 연속성 앵커가 하나라서 모델이 지키기 쉬움
- 텍스트 라벨이 정확히 렌더됨 — 모델이 짧은 라벨 텍스트는 처리 가능함을 보여주는 성공 표본
- 오프닝 토스+엔딩 콜라주 = hook과 payoff가 명시된 완결 구조

B. Inference:
- "1개 아이템 × 10 변형"은 카탈로그형 구조 — 각 룩이 독립적이므로 샷 간 연속성 추론 부담이 낮음. 모델 친화적일 수 있음
- 번호 리스트는 복사-붙여넣기 친화적 — 인기의 구조적 요인일 수 있으나 단정 불가

### 13. Popularity signal
- rank: 4 / likes: 204
- likely_driver: prompt_structure (번호 리스트 — 재사용 용이), visual_subject (패션 릴), novelty (1 shirt 10 ways 컨셉), unknown
- 판단: 구조의 재사용성이 인기에 기여했을 가능성이 있으나 단정 불가

### 14. Relation to existing XAI-Studio patterns
- Identity-Locked Lifestyle: 부분 강화 (텍스트 서술 — 약한 형태)
- Coverage Planning: 강화 (full/medium/close-up 명시)
- Trailer Montage: 강화 (밀도)
- #47의 "Object pass": 오프닝 셔츠 토스로 강화
- ending collage: Day-cycle bookend 계열의 "recap ending" — 기존 패턴의 변형으로 강화

### 15. Candidate contribution
- new prompt archetype 후보: **enumerated look-list + on-screen labels** — 번호 리스트 × 텍스트 라벨 × 엔딩 콜라주의 결합. (최종 D에서 검토)
- new UI rule 후보: **text-as-audio-substitute** — "No dialogue" + "clean animated text labels". (최종 D에서 검토)
- 그 외 reinforces existing patterns

---
## Case 05 — Sophia "cinematic influencer reel, luxury lifestyle" [rank 5]

### 1. Source
- URL: https://www.meigen.ai/video/2079520974517805421
- creator: Sophia (@sophiaparkerr_)
- model: Seedance
- duration: 15.08초 실측 (362프레임/24fps/1280x720). "0:00–0:15" 구조와 일치
- popularity: rank 5, 198 likes

### 2. Evidence basis
- prompt-derived (전문 확보)
- frame-observed (15프레임 컨택트시트. 5샷 중 3샷 매칭, 1샷 부분, 핵심 이펙트 미렌더)
- inference: Why it may work B항

### 3. Prompt structure
글로벌 스타일 블록 + 타임스탬프 샷 리스트(5샷 × 3초). 구조 분해:
- Style block (글로벌): "Ultra-realistic cinematic influencer reel, luxury lifestyle aesthetic, 4K HDR, golden hour lighting, shallow DOF, smooth gimbal movements, subtle lens flares, vibrant city atmosphere, fashion-commercial quality, confident feminine energy"
- SHOT 1 (0:00–0:03): Camera (low-angle tracking, heels) / Action (coffee+phone, glance+smirk) / Audio (pop beat begins + city ambience)
- SHOT 2 (0:03–0:06): Camera (orbit, slow motion) / Action (wind lifts hair, sunglasses off→eye contact→on) / Effect (speed ramp, lens flare)
- SHOT 3 (0:06–0:09): Camera (wide, crosswalk) / Action (city freezes — cars stop, birds hang, pedestrians motionless; only she walks) / Effect (cinematic sound hit)
- SHOT 4 (0:09–0:12): Camera (FPV drone rise to skyline) / Action (sunglasses on → city comes back to life) / Effect (whip transition on beat)
- SHOT 5 (0:12–0:15): Camera (slow-mo close-up) / Action (sip coffee, wink, walk past lens; camera turns to reveal admirers) / Music (beat drop + logo-style ending)
- 없음: negative constraints, 대사, 레퍼런스 지정

### 4. Subject / Character state
- identity lock: 없음 (텍스트: "stylish", "confident feminine energy")
- wardrobe lock: 없음 (렌더: 노란 드레스+힐 — 샷 간 유지됨 ✓)
- prop lock: coffee cup, phone, sunglasses — 샷 1·2·5에서 사용. 렌더에서 커피컵 유지됨 ✓
- character count: 1 (+ 행인들)
- gaze assignment: "casually glances at the camera with a confident smirk" (SHOT 1), "makes eye contact" (SHOT 2), "playful wink" (SHOT 5) — 3개 샷에 시선 비트 배치. 렌더에서 응시 확인됨 ✓
- role separation: 해당 없음

### 5. Camera / Shot design
- multi-shot: 5샷, 각 3초, 타임스탬프 명시
- explicit cuts: "Whip transition synchronized to the music beat" (SHOT 4) — 비트 싱크 전환 선언
- camera role: 관찰자 (tracking/orbit/drone)
- framing progression: low-angle (heels) → orbit → wide → FPV aerial → slow-mo close-up — 상승 아크 (지면→공중→클로즈업)
- subject-camera relationship: 정면 응시 3회 — 카메라를 관객 대리자로 사용
- handheld/cinematic: "smooth gimbal movements"

### 6. Spatial / Continuity
사용 채널: identity (텍스트 — 약함), wardrobe (노란 드레스 — 유지됨 ✓), prop (커피컵 — 유지됨 ✓), location (European street → crosswalk → skyline — 동일 도시로 읽힘 ✓), lighting (golden hour — 유지됨 ✓), tone/grade (유지됨 ✓). 샷 간 이동이 크지만 동일 도시·동일 시간대로 묶임

### 7. Action grammar
- 핵심 장치: **world-state manipulation** — "the entire city freezes... Only she keeps walking" → "the frozen city instantly comes back to life". 주인공의 액션이 아니라 세계의 상태를 바꾸는 지시
- trigger: "As she puts on her sunglasses" → 세계 부활. 선글라스를 상태 토글로 사용 (트리거 문법의 변형)
- anticipation→contact→consequence: SHOT 3→4가 freeze→unfreeze의 상태 전이
- action density: 중간-높음

### 8. Reference usage
- 없음

### 9. Audio / Dialogue
- dialogue: 없음
- music: "Trendy upbeat pop beat begins", "Beat drops on the final frame" — 시작/종료 비트 지정
- beat sync: 선언 수준 ("synchronized to the music beat" — SHOT 4 whip transition)
- SFX: "Epic cinematic sound hit" (SHOT 3)
- ambience: "city ambience"
- camera rhythm-오디오 연동: 선언 수준. 실제 싱크 미확인

### 10. Failure prevention
실패 방지 문장 없음. 관찰된 실패 (frame-observed):
- **world-freeze 미렌더**: SHOT 3의 "entire city freezes" — 렌더에서 행인들이 모션 블러로 이동 중, 차량 이동. 핵심 이펙트 실패
- "birds hang in midair" — 새가 날고 있음 (정지 아님)
- "Pedestrians naturally move aside" (SHOT 1) — 렌더에서 비켜서지 않음
- "FPV drone smoothly rises from street level" (SHOT 4) — 연속 상승이 아니라 공중 샷으로 컷
→ world-state manipulation ("세계를 멈춰라") 계열 지시는 실패 확률이 높은 표본. Failure-Sourced Negatives의 새 표본

### 11. Control Levels
- Hard Lock: 5샷의 타임스탬프, 샷별 액션, 시선 비트 3개
- Soft Guidance: 스타일 블록, 카메라 무브, 이펙트 라인
- Creative Freedom: 행인 디테일, 도시 세부, 표정

### 12. Why it may work
A. Evidence-backed:
- 5샷 구조가 15초에 정확히 매핑됨 (3초×5). 샷 1·2·5의 액션(힐 워킹, 선글라스, 커피+윙크)이 렌더에서 확인됨
- 의상·소품·조명·톤의 샷 간 유지 — 앵커가 적지만 지켜짐
- 시선 비트 3개가 렌더에서 동작 — 모델이 "카메라 응시"를 안정적으로 처리

B. Inference:
- world-freeze 실패에도 불구하고 인기가 높은 이유 — 첫 6초(힐+선글라스)의 시각적 완성도가 썸네일/첫인상을 끌었을 수 있음. 즉 인기는 "앞부분"이 견인했을 가능성 (inference)
- 타임스탬프 샷 리스트는 모델보다 "작성자 본인의 설계"에 도움 — 샷 할당을 강제해 밀도를 보장

### 13. Popularity signal
- rank: 5 / likes: 198
- likely_driver: visual_subject (골든아워 패션 릴), prompt_structure (타임스탬프 샷 리스트 — 재사용 용이), unknown
- 판단: 핵심 이펙트 실패에도 인기 — 인기와 프롬프트의 렌더 성공은 별개일 수 있음

### 14. Relation to existing XAI-Studio patterns
- Identity-Locked Lifestyle: 약한 형태 (텍스트만)
- Trailer Montage: 강화 (3초×5 밀도)
- Hard/Soft/Creative: 강화
- 트리거 문법: "선글라스 착용 → 세계 부활" — #46 CUT ON 계열의 변형으로 강화
- world-state manipulation: 신규 시도이나 렌더 실패 — 규칙이 아니라 실패 표본으로 기록

### 15. Candidate contribution
- new failure-sourced negative 후보: **world-freeze 계열 지시의 실패** — "entire city freezes, only she moves" 렌더 실패. (최종 D/E에서 검토)
- new shot-list format 후보: **Camera/Action/Effect triplet + 타임스탬프** — #47(렌즈mm+SFX)와 다른 샷 리스트 문법. (최종 D에서 검토)
- 그 외 reinforces existing patterns

---
## Case 06 — simeon-sanai "hyperlapse selfie travel vlog: New 7 Wonders" [rank 6]

### 1. Source
- URL: https://www.meigen.ai/video/2071550858035396655
- creator: simeon-sanai (@Naiknelofar788)
- model: Seedance
- duration: 15.0초 실측 (360프레임/24fps/3840x2160)
- popularity: rank 6, 168 likes

### 2. Evidence basis
- prompt-derived (전문 확보)
- frame-observed (15프레임 컨택트시트. 7대 불가사의 전부 확인, 동일 인물 유지)
- inference: Why it may work B항

### 3. Prompt structure
섹션 라벨 방식 (9섹션). 구조 분해:
- premise: "cinematic hyperlapse selfie travel vlog ... across the New 7 Wonders of the World ... filmed over one unforgettable journey"
- STYLE: 렌즈(16–20mm ultra-wide), 셀피 스틱, handheld, motion blur, optical flow, temporal consistency
- CHARACTER CONSISTENCY: 속성 열거 — facial features, hairstyle, age, skin tone, body proportions, clothing continuity, accessories, personality, overall appearance
- EDITING: "hard cuts approximately every 0.4 seconds, synchronized perfectly to the music beat. Every cut introduces a new location, angle, or action while maintaining seamless visual continuity"
- LOCATIONS: 7대 불가사의 리스트 + 여행 모먼트 리스트 (공항, 기내, 기차, 시장, 루프탑, 야경 등)
- WARDROBE: 목적지별 의상 변경 허용 + "maintaining accessory continuity" — 변경 허용 범위를 명시
- PERFORMANCE: vlogger 에너지 — waving, peace signs, thumbs-up, finger hearts, laughter, pointing, spinning, dancing
- ENVIRONMENT: 시간대 (sunrise, golden hour, blue hour, nighttime) + 군중/날씨
- QUALITY: artifact negatives — "Avoid flickering, geometry distortions, ghosting, duplicated subjects, visual artifacts, or inconsistent accessories"
- FINAL RESULT: 한 줄 요약 ("premium 15-second cinematic hyperlapse travel vlog...")
- 없음: 타임스탬프, 대사, 레퍼런스 이미지

### 4. Subject / Character state
- identity lock: 텍스트 속성 열거 (레퍼런스 이미지 없음). 렌더에서 15초 내내 동일 인물 유지됨 ✓ (frame-observed) — 텍스트 락의 성공 사례
- wardrobe lock: 의도적 변경 허용 — "appropriate for each destination", 액세서리만 연속. 렌더에서 의상 변경됨 (타지마할 프레임은 노란 드레스) ✓ 설계대로
- prop lock: 없음 (셀피 스틱은 카메라 문법)
- character count: 1 (+ 배경 군중, 기차 옆 남성 1명 — 엑스트라 드리프트)
- gaze assignment: 없음 (셀피 특성상 렌즈 응시가 기본값)
- role separation: 해당 없음

### 5. Camera / Shot design
- multi-shot: ~37컷 (15초/0.4초)
- explicit cuts: "hard cuts" — 편집 선언
- camera role: 그녀 자신의 셀피 스틱 (selfie grammar)
- framing: close selfie framing 일관 — 프레임 구성이 전부 셀피. 로케이션만 바뀜
- subject-camera relationship: 셀피 — 피사체=촬영자
- camera movement의 story function: hyperlapse — 이동 자체가 서사

### 6. Spatial / Continuity
사용 채널: identity (텍스트 열거 — 성공 ✓), wardrobe (변경 허용+액세서리 락), location (7곳 리스트), lighting (시간대 다양성 — 의도적 변경), tone/grade (vibrant — 유지됨 ✓). 연속성 전략: "바뀌어도 되는 것"을 미리 선언 (의상, 시간대) — drift를 허용 범위로 흡수하는 설계

### 7. Action grammar
- 단순 결과 지시 + 퍼포먼스 동사 나열 (waving, peace signs, pointing, spinning...)
- anticipation→contact→consequence: 없음 (카탈로그형)
- action density: 매우 높음 (0.4초/컷)
- motion budget: 컷 자체가 예산 — 각 컷은 정적에 가까움

### 8. Reference usage
- 없음

### 9. Audio / Dialogue
- dialogue: 없음 (언급 없음)
- music: "synchronized perfectly to the music beat" — 비트 싱크 선언. 장르 미지정
- beat sync: 선언 수준 (0.4초 컷 = 비트 앵커). 실제 싱크 미확인
- camera rhythm-오디오 연동: 컷이 비트에 묶인다고 선언

### 10. Failure prevention
- generic negatives (QUALITY 섹션): flickering, geometry distortions, ghosting, duplicated subjects, visual artifacts, inconsistent accessories — artifact-targeted generic. failure-sourced 아님 (특정 실패 경험의 언급 없음)
- 관찰 (frame-observed): ghosting/duplication 없음 — negatives의 효과인지는 단정 불가
- 설계적 실패 방지: "바뀌어도 되는 것"의 사전 선언 (의상·시간대) — drift를 실패가 아니라 사양으로 처리

### 11. Control Levels
- Hard Lock: 7대 불가사의 리스트, 0.4초 하드컷, 셀피 프레이밍, 15초
- Soft Guidance: 스타일 스펙, 퍼포먼스 리스트, 환경 시간대
- Creative Freedom: 컷별 구도, 군중, 의상 디테일

### 12. Why it may work
A. Evidence-backed:
- 동일 인물이 15초·~37컷 내내 유지됨 (frame-observed) — 텍스트 속성 열거만으로 identity lock 성공
- 7대 불가사의가 전부 등장 — 로케이션 리스트의 커버리지 달성
- 0.4초 컷이 drift 누적 시간을 원천 차단 — 각 컷이 짧아서 모델이 망가질 시간이 없음

B. Inference:
- "변경 허용 범위 선언"은 연속성 실패를 사양으로 전환하는 설계 — 의상 drift가 실패가 아니라 의도가 됨. 이 패턴은 재사용 가치가 있을 수 있음 (inference — 규칙 아님)
- 셀피 단일 구도는 카메라 추론 부담을 최소화

### 13. Popularity signal
- rank: 6 / likes: 168
- likely_driver: visual_subject (7대 불가사의 — 썸네일 강함), novelty (hyperlapse 컨셉), prompt_structure (섹션 라벨 — 재사용 용이), unknown
- 판단: 소재의 힘이 클 가능성. 구조 기여도는 단정 불가

### 14. Relation to existing XAI-Studio patterns
- Travel Coverage: 강화 (대표 사례)
- Identity-Locked Lifestyle: 강화 — 텍스트 락의 성공 표본
- Front-Covered Experience Vlog: 강화 (셀피 문법)
- Trailer Montage: 강화 (0.4초 컷)
- Hard/Soft/Creative: 강화

### 15. Candidate contribution
- new prompt-architecture 후보: **attribute-enumerated consistency block** — CHARACTER CONSISTENCY 섹션처럼 일관성 속성을 전부 열거하는 명명된 블록. (최종 D에서 검토)
- new design-pattern 후보: **change-tolerance declaration** — "바뀌어도 되는 것"을 미리 선언해 drift를 사양으로 흡수 (의상·시간대). (최종 D에서 검토)
- 그 외 reinforces existing patterns

---
## Case 07 — Shore Lyn "KitKat storyboard presentation" [rank 7]

### 1. Source
- URL: https://www.meigen.ai/video/2077345203049148886
- creator: Shore Lyn (@Shorelyn_)
- model: Seedance
- duration: 15.19초 실측 (456프레임/30fps/1080x1920 세로)
- popularity: rank 7, 164 likes

### 2. Evidence basis
- prompt-derived (전문 확보)
- frame-observed (15프레임 컨택트시트. 스토리보드 컨테이너는 미렌더, 콘텐츠만 렌더)
- inference: Why it may work B항

### 3. Prompt structure
이중 레이어 (container + content). 구조 분해:
- container block: "professional commercial storyboard presentation ... 10 cinematic frames arranged in a clean 2×5 grid on a white presentation board. Thin black borders ... bold scene number (01–10), timestamp, short production caption" — 메타 프레젠테이션 지정
- title block: 'TITLE KITKAT "The Art of the Snap" Luxury Commercial Storyboard • 15 Seconds'
- style block: premium chocolate commercial aesthetic
- SCENE 01–10: 각 신 = (타임스탬프 1.5초씩) + [카메라/액션 서술] + "Caption: [짧은 캡션]"
  - 01 The Reveal (어둠에서 등장) → 02 Luxury Detail (매크로 로고) → 03 Ingredients Rise → 04 The Perfect Snap → 05 Floating Luxury (오빗) → 06 Chocolate Flow (붓기) → 07 Pure Indulgence (폭포) → 08 Frozen Perfection (정지) → 09 Hero Product → 10 Brand Signature (로고+태그라인)
- presentation style block: 반복 강조 (storyboard, pitch board, scene numbers, timestamps...)
- tech block: "ARRI Alexa 35 • Cooke Anamorphic 50mm • HDR • 8K"
- 없음: negative constraints, 대사, 레퍼런스 지정

### 4. Subject / Character state
- identity lock: 제품 — KitKat bar (단일 제품 앵커). 렌더에서 15초 내내 유지됨 ✓
- wardrobe lock: 해당 없음
- prop lock: 패키지 (SCENE 09에서 등장). 렌더에서 등장 ✓
- character count: 0 (인물 없음)
- gaze assignment: 해당 없음
- role separation: 해당 없음

### 5. Camera / Shot design
- multi-shot: 10신, 각 1.5초
- explicit cuts: 없음 (신 리스트만)
- camera role: 관찰자 (매크로/오빗)
- framing progression: darkness → extreme macro → floating → snap → orbit → pour → cascade → frozen → hero → logo — 제품 광고의 표준 아크
- container 무시: 2×5 그리드·씬 번호·타임스탬프·캡션 전부 미렌더. 모델이 컨테이너를 버리고 콘텐츠만 렌더

### 6. Spatial / Continuity
사용 채널: identity (제품 — 강함, 유지됨 ✓), prop (패키지), tone/grade (dark luxury — 유지됨 ✓), lighting (warm golden — 유지됨 ✓). spatial/topology 락 없음. 단일 제품이라 연속성 부담 최소

### 7. Action grammar
- state transition 중심: 등장→디테일→재료→스냅→유동→정지→히어로→로고 — 제품의 상태 변화 아크
- "Time almost freezes" (SCENE 04), "Everything freezes" (SCENE 08) — 정지를 연출 장치로 2회 사용 (#5의 world-freeze와 달리 제품 주변 파티클의 정지 — 범위가 좁음)
- anticipation→contact→consequence: SCENE 04 (snap → shards explode) — 부분적
- action density: 중간

### 8. Reference usage
- 없음

### 9. Audio / Dialogue
- dialogue: 없음
- music/SFX: 언급 없음 (무음 스펙)
- beat sync: 없음
- 특이: 오디오 블록 자체가 없음 — 제품 광고인데 무음

### 10. Failure prevention
실패 방지 문장 없음. 관찰된 현상 (frame-observed):
- **container collapse**: 스토리보드 그리드·번호·캡션이 전부 미렌더. 메타 프레젠테이션 지시가 무시되고 실제 광고 영상이 렌더됨
- text seep: 패키지의 "ORIGINAL" 난독, 한자풍 글자. 단, "KitKat" 로고와 "Enjoy Every Snap" 태그라인은 정확히 렌더 (유명 브랜드 텍스트는 안정적)
- 실패라기보다 모델의 선택 — 결과물은 갤러리에서 더 매력적

### 11. Control Levels
- Hard Lock: 10신의 타임스탬프, 신별 액션, 태그라인 문구
- Soft Guidance: 스타일 블록, 컨테이너 스펙, 테크 스펙
- Creative Freedom: 카메라 디테일, 파티클, 조명

### 12. Why it may work
A. Evidence-backed:
- 10신이 1.5초씩 15초에 정확히 매핑됨. 신별 액션(스냅, 붓기, 정지, 히어로)이 렌더에서 확인됨
- 단일 제품 앵커 — 15초 내내 KitKat bar 유지
- 유명 브랜드 텍스트(KitKat, Enjoy Every Snap)가 정확히 렌더 — 텍스트 안정성의 성공 표본

B. Inference:
- 컨테이너 붕괴가 오히려 유리하게 작용 — 스토리보드 이미지보다 실제 광고 영상이 갤러리에서 더 매력적. 인기는 렌더된 "광고"가 견인했을 가능성
- 제품 단일 앵커 + 어두운 배경 = 모델의 실패 표면 최소

### 13. Popularity signal
- rank: 7 / likes: 164
- likely_driver: visual_subject (럭셔리 초콜릿 광고 — 시각적 완성도), novelty (스토리보드 컨셉), unknown (prompt_structure)
- 판단: 인기는 렌더 결과물(광고)의 힘일 가능성이 큼. 프롬프트의 스토리보드 의도와 무관

### 14. Relation to existing XAI-Studio patterns
- Trailer Montage: 강화 (1.5초×10 밀도)
- Identity-Locked Lifestyle: 제품 버전으로 강화 (단일 앵커)
- Hard/Soft/Creative: 강화
- #47의 전환 어휘: 없음 — 신 리스트만으로 밀도 달성

### 15. Candidate contribution
- new model-behavior note 후보: **container collapse** — 메타 프레젠테이션(스토리보드 그리드, UI) 지시는 무시되고 콘텐츠만 렌더될 수 있음. (최종 D/E에서 검토 — 규칙이 아니라 주의사항)
- 그 외 reinforces existing patterns

---
## Case 08 — Oogie "Bullet time: falling businessman, Wall Street" [rank 8]

### 1. Source
- URL: https://www.meigen.ai/video/2041804634013184301
- creator: Oogie (@oggii_0)
- model: Seedance
- duration: 15.13초 실측 (363프레임/24fps/834x1112 세로)
- popularity: rank 8, 164 likes

### 2. Evidence basis
- prompt-derived (전문 확보)
- frame-observed (15프레임 컨택트시트. 이펙트는 매칭, 피사체/장소는 드리프트)
- inference: Why it may work B항

### 3. Prompt structure
단일 문단, 약 90단어. 구조 분해:
- effect declaration (선두): "Bullet time effect."
- subject/action: "A businessman in white shirt and black tie slipping and falling backwards on an icy wet street in Wall Street, New York"
- frozen detail block: "Coffee cup standing on ground, liquid exploding outward frozen in mid-air. Ice chunks, water droplets, and coffee splash all completely suspended time is frozen."
- environment: "Tall buildings on both sides creating a canyon effect."
- camera block (핵심): "The camera smoothly orbits 360 degrees around the falling man at low ground level angle, only the camera moves while everything else remains perfectly still."
- grade: "Cinematic, overcast dramatic lighting, wide angle lens distortion."
- 없음: negative constraints, 타임스탬프, 대사, 레퍼런스 지정

### 4. Subject / Character state
- identity lock: 없음 (텍스트: "businessman in white shirt and black tie")
- 렌더 결과 (frame-observed): 노란 트레이닝복 여성으로 드리프트. 화이트 셔츠/넥타이 없음
- wardrobe lock: 시도, 실패
- prop lock: "coffee cup" → 렌더에서는 장바구니·오렌지·바게트. 소품 전체 교체
- character count: 1
- gaze assignment: 없음
- role separation: 해당 없음

### 5. Camera / Shot design
- single shot (사실상): 360도 오빗 원테이크
- camera block이 프롬프트에서 가장 강한 제약: "only the camera moves while everything else remains perfectly still" — 움직임의 독점권을 카메라에 부여
- 렌더에서 오빗이 동작함 ✓ (frame-observed: 배경이 회전 — 집→거리→나무)
- camera role: 오빗 관찰자
- framing: low ground level angle — 유지됨 ✓
- subject-camera relationship: 피사체 중심 회전

### 6. Spatial / Continuity
사용 채널: camera-motion (강함 — 유지됨 ✓), frozen-state (유지됨 ✓), location (Wall Street → 교외 주택가로 드리프트 ✗), wardrobe (드리프트 ✗). 카메라 움직임과 정지 상태는 지켜지고, 피사체·장소는 바뀜

### 7. Action grammar
- 핵심: **motion-monopoly rule** — "only the camera moves while everything else remains perfectly still". 움직임의 주체를 카메라로 독점 지정. #5의 world-freeze와 달리 "정지"가 카메라 대비 개념으로 정의됨
- frozen detail의 열거: ice chunks, water droplets, coffee splash — 정지할 파티클을 명사로 지정
- anticipation→contact→consequence: 없음 (단일 정지 장면)
- action density: 낮음 (정지 장면 + 카메라 이동)

### 8. Reference usage
- 없음

### 9. Audio / Dialogue
- dialogue: 없음
- music/SFX: 언급 없음 (무음 스펙)

### 10. Failure prevention
실패 방지 문장 없음. 관찰된 드리프트 (frame-observed):
- subject drift: businessman → woman in yellow tracksuit
- location drift: Wall Street canyon → suburban street
- prop drift: coffee cup → groceries (oranges, baguettes)
- 유지된 것: 360 오빗, frozen mid-air, low angle
→ 카메라 움직임 지시는 지켜지고 피사체 서술은 바뀐 사례. "무엇을"보다 "어떻게 움직일지"가 더 강하게 지켜진 표본 (단일 사례 — 규칙 아님)

### 11. Control Levels
- Hard Lock: 360도 오빗, "only the camera moves", frozen state
- Soft Guidance: 피사체 서술, 장소, 그레이드
- Creative Freedom: (렌더에서 피사체·장소가 여기로 밀려남)

### 12. Why it may work
A. Evidence-backed:
- 360도 오빗 + 정지 파티클이 15초 내내 유지됨 (frame-observed) — 카메라 독점 규칙이 동작
- 프롬프트가 90단어로 짧음 — 지시 간 충돌이 적음

B. Inference:
- "only the camera moves"는 부정문(negative)이지만 동작 정의이므로 모델이 처리하기 쉬울 수 있음. "움직이지 마"가 아니라 "카메라만 움직여"라는 긍정적 독점 선언
- 짧은 프롬프트 + 단일 이펙트 = 실패 표면 최소. 길이가 경쟁력일 수 있음 (inference)

### 13. Popularity signal
- rank: 8 / likes: 164
- likely_driver: visual_subject (bullet time 오빗 — 시각적 임팩트), novelty, unknown (prompt_structure)
- 판단: 이펙트의 시각적 힘이 인기 요인일 가능성. 프롬프트 품질과 단정 불가

### 14. Relation to existing XAI-Studio patterns
- Continuous Action: 강화 (원테이크 오빗)
- Hard/Soft/Creative: 강화 — 단, Hard로 의도한 것(피사체)이 지켜지지 않은 역설적 표본
- #5의 world-freeze: 대조 표본 — 여기서는 freeze가 동작 (범위가 "파티클"로 좁고, 카메라 독점과 결합)

### 15. Candidate contribution
- new camera-rule 후보: **motion-monopoly declaration** — "only the camera moves while everything else remains perfectly still". 움직임의 독점권 선언. (최종 D에서 검토)
- 그 외 reinforces existing patterns

---
## Case 09 — Calira "luxury handbag commercial" [rank 9]

### 1. Source
- URL: https://www.meigen.ai/video/2073262158817972390
- creator: Calira (@CaliraVal)
- model: Seedance
- duration: 15.34초 실측 (461프레임/30fps/720x1240 세로)
- popularity: rank 9, 149 likes

### 2. Evidence basis
- prompt-derived (전문 확보)
- frame-observed (15프레임 컨택트시트. 제품 앵커 강하게 유지, 몰 장면 미렌더)
- inference: Why it may work B항

### 3. Prompt structure
단일 문단, 약 150단어. 구조 분해:
- subject block: "elegant designer leather handbag" + 재질 스펙 (premium leather texture, gold hardware, fine stitching)
- environment: "high-end boutique with warm ambient lighting"
- camera path (시간 순서): "starts with an extreme close-up ... before smoothly orbiting around the bag"
- human interaction: "gently picked up by a stylish woman, followed by graceful slow-motion shots as she walks through a modern luxury shopping mall"
- detail coverage: "Elegant close-ups highlight the handle, zipper, interior compartments, and premium craftsmanship" — Coverage Planning
- environment detail: "Soft bokeh lights, marble floors, floor-to-ceiling glass, natural reflections"
- grade block: "smooth gimbal movements, shallow DOF, luxury fashion advertisement, photorealistic, ultra-detailed, cinematic color grading, HDR, 8K, premium brand aesthetic, realistic physics, flawless lighting, high-end commercial quality"
- 없음: negative constraints, 타임스탬프, 대사, 레퍼런스 지정

### 4. Subject / Character state
- identity lock: 제품 — 민트색 핸드백 (단일 앵커). 렌더에서 15초 내내 디자인 유지됨 ✓ (frame-observed)
- wardrobe lock: 해당 없음 (인물이 소품)
- prop lock: 가방 자체가 prop
- character count: 0 (+ 손, 1명의 여성 — 핸들러 역할)
- gaze assignment: 해당 없음
- role separation: 인물은 "드는 손" — 캐릭터가 아니라 소품 조작자

### 5. Camera / Shot design
- multi-shot: ECU → orbit → pickup → detail close-ups
- camera path가 서사: "starts with ... before smoothly orbiting" — 카메라 이동을 시간 순서로 선언
- camera role: 제품 관찰자
- framing: extreme close-up → orbit → interior close-ups — 제품 광고의 표준 아크
- "she walks through a modern luxury shopping mall" — 렌더에서 미렌더 (스튜디오 배경 유지). 장소 이동 지시 실패

### 6. Spatial / Continuity
사용 채널: identity (제품 — 강함, 유지됨 ✓), prop (가방=주체), tone/grade (warm luxury — 유지됨 ✓), environment (boutique → 렌더는 스튜디오 — 부분 드리프트). 단일 제품이라 연속성 부담 최소

### 7. Action grammar
- human-as-handler: "gently picked up by a stylish woman" — 인물의 액션이 제품의 상태를 바꿈 (테이블→손에 들림)
- detail reveal: 핸들→지퍼→내부→장인정신 — 공개의 순서가 지정됨
- anticipation→contact→consequence: 약함 (공개형)
- action density: 낮음 (제품이 정적, 카메라가 움직임)

### 8. Reference usage
- 없음

### 9. Audio / Dialogue
- dialogue: 없음
- music/SFX: 언급 없음 (무음 스펙)

### 10. Failure prevention
실패 방지 문장 없음. 관찰된 드리프트 (frame-observed):
- location drift: luxury mall walk 미렌더 — 스튜디오 배경으로 고정
- 유지된 것: 제품 디자인, 재질, 색상, 카메라 패스
- 텍스트: "PARIS" 카드 가독, 엠보싱 브랜드 텍스트 부분 가독 — 제품 텍스트의 성공 표본
→ 장소 이동 지시는 실패, 제품 앵커는 성공. 앵커의 강도 차이

### 11. Control Levels
- Hard Lock: 제품 재질 스펙, 카메라 패스 (ECU→오빗), 디테일 커버리지
- Soft Guidance: 환경, 그레이드, "graceful slow-motion"
- Creative Freedom: 배경 디테일, 여성의 모습

### 12. Why it may work
A. Evidence-backed:
- 단일 제품 앵커가 15초 내내 유지됨 (frame-observed) — #7 KitKat과 같은 제품-앵커 성공 패턴
- 디테일 커버리지(핸들/지퍼/내부)가 렌더에서 실행됨 — 손이 지퍼를 열고 폰을 넣는 장면까지
- 카메라 패스(ECU→오빗)가 지켜짐

B. Inference:
- 제품 단일 앵커 + 정적 제품 + 움직이는 카메라 = 모델의 실패 표면 최소. 인물·장소 이동을 최소화한 설계
- "realistic physics, flawless lighting" 같은 품질 형용사의 실제 효과는 불명 — 단정 불가

### 13. Popularity signal
- rank: 9 / likes: 149
- likely_driver: visual_subject (럭셔리 제품 광고), unknown (prompt_structure)
- 판단: 제품 광고 장르의 시각적 매력. 구조 기여도 단정 불가

### 14. Relation to existing XAI-Studio patterns
- Identity-Locked Lifestyle: 제품 버전으로 강화 (#7과 쌍)
- Coverage Planning: 강화 (디테일 클로즈업 지정)
- Continuous Action: 부분 강화 (오빗)
- Hard/Soft/Creative: 강화

### 15. Candidate contribution
- reinforces existing patterns. 제품-앵커 + 카메라-패스 구조의 재확인
- #7과의 쌍으로 "product-anchor commercial" 아키타입의 반복 확인 (빈도 카운트용)

---
## Case 10 — 路飞 "魔法笔街头魔法Vlog" (magic pen street magic vlog) [rank 10]

### 1. Source
- URL: https://www.meigen.ai/video/2076942580504567870
- creator: 路飞 (@0xluffy_eth)
- model: Seedance
- duration: 10.17초 실측 (244프레임/24fps/720x1280 세로). 타이틀 "15秒"와 불일치 (5개 비트는 전부 렌더됨 — 압축)
- popularity: rank 10, 140 likes
- language: 중국어 간체 프롬프트 (Top 20 중 유일)

### 2. Evidence basis
- prompt-derived (전문 확보 — 중국어)
- frame-observed (10프레임 컨택트시트. 5개 비트 전부 매칭)
- inference: Why it may work B항

### 3. Prompt structure
헤더 + [섹션 라벨] + 5비트. 구조 분해:
- header: "[魔法笔街头魔法Vlog · 15秒 · 竖屏9:16]" — 컨셉·길이·어스펙트를 한 줄로
- [风格]: 实拍+扁平2D动漫贴纸合成, 第一人称, 一镜到底, 无剪辑无场景切换 ("one continuous take, no cuts, no scene changes")
- [摄影]: "原始未稳定手持手机镜头" — 흔들림, AF 서치, 노출 변화, 롤링셔터 젤리, HDR 색감. imperfection spec의 가장 상세한 버전
- [光线]: 황혼 태양 단일 방향, 모든 실물+애니메 캐릭터가 일치하는 접촉 그림자
- [场景]: 한국 도시 한 블록의 연속 경로 (고가 지하철→비둘기 인도→버스 차로→버스 정류장 벤치)
- [钢笔 — 魔法法则] (핵심): **universal transformation rule** — "每次变形遵循相同序列: 钢笔指向 → 'Biu!' → 蓝色手绘草图线条包裹目标 → 墨水扩散 → 目标变成扁平2D赛璐璐动漫角色 — 保持原始物体确切的大小、位置、速度、方向和透视，完全锚定在真实街道上. 角色保持扁平贴纸阴影，从未被现实世界光线重新照明；它们触碰的一切都以真实物理反应."
- 5 beats: [00:00-00:03] 기차→슈퍼히어로 / [00:03-00:06] 비둘기→카툰 새 / [00:06-00:10] 버스→거대 오렌지 고양이 / [00:10-00:12] 벤치 여성→애니메 일러스트 / [00:12-00:15] 펜을 하늘에 던짐→하늘 전체가 애니메 하늘, "THE END!" — 각 비트 = [카메라 액션] + 변형 + "SFX:" 라인
- ending: "唯一的文字" (유일한 텍스트) "THE END!" + 프리즈 프레임
- 없음: negative constraints(일반), 대사(대신 "Biu!" 의성어), 레퍼런스 지정

### 4. Subject / Character state
- identity lock: 펜을 든 손 — "照片级，可见毛孔" (포토리얼, 모공 보임). 렌더에서 손이 10초 내내 프레임 안에 있음 ✓
- wardrobe lock: 해당 없음
- prop lock: 검은 마커펜 — "始终在画面中" (항상 화면 안). 비트를 연결하는 시각적 가이드. 렌더에서 유지됨 ✓
- character count: 비트마다 1 (+ 배경 행인)
- gaze assignment: 없음 (1인칭)
- role separation: 펜=마법 도구, 손=시술자, 목표물=변형 대상 — 역할 분리 명확

### 5. Camera / Shot design
- single shot: "一镜到底...无剪辑。无场景切换" — 원테이크 선언. 렌더에서 원테이크 유지됨 ✓
- camera role: vlogger의 손 (1인칭)
- framing: 1인칭 핸드헬드
- "镜头以快速甩动平移跟随钢笔移动" — 카메라가 펜을 따라감. 카메라의 주체가 펜 (subject-camera relationship의 역전)
- handheld 문법의 story function: "真实智能手机后置摄像头画面的质感" — 리얼리티의 증거

### 6. Spatial / Continuity
사용 채널: identity (손), prop (펜 — 비트 연결 앵커), spatial/topology (연속된 한 블록 경로), lighting (단일 태양 방향 — 실물과 애니메 공통), tone/grade. **conservation law**: "保持原始物体确切的大小、位置、速度、方向和透视" — 변형 후에도 5개 속성을 보존하는 물리 보존 법칙. 렌더에서 거대 고양이가 버스의 크시·위치를 유지 ✓

### 7. Action grammar
- 핵심: **transformation sequence template** — 한 번 정의하고 5번 인스턴스화: [펜 포인팅] → ["Biu!"] → [스케치선 래핑] → [잉크 확산] → [2D 변형]. #1의 CUT-as-trigger, #46의 CUT ON과 같은 "트리거 문법" 계열의 변형 시퀀스 버전
- trigger: 의성어 "Biu!" — 소리가 변형의 트리거
- anticipation→contact→consequence: 스케치선(anticipation) → 잉크 확산(contact) → 변형(consequence) — 3단계가 템플릿에 내장
- action density: 높음 (5비트/10초)
- motion budget: 펜의 움직임이 예산의 중심

### 8. Reference usage
- 없음

### 9. Audio / Dialogue
- dialogue: 없음 (대신 의성어 "Biu!" ×5)
- SFX: 비트별 "SFX:" 라인 5개 (기차 굉음+마커 휘슬 / 날갯짓+종이 사각거림 / 엔진→발걸음+그르렁 / 스케치+반짝임 / 휘슬+수채화+마커 끽끽)
- music: 언급 없음
- beat sync: 비트 경계가 SFX와 묶임
- camera rhythm-오디오 연동: "Biu!"가 변형과 동기 — #47의 per-shot SFX와 동형

### 10. Failure prevention
- 특정 렌더링 제약 (failure-sourced로 보임): "角色保持扁平贴纸阴影，从未被现实世界光线重新照明" (캐릭터는 플랫 스티커 음영 유지, 현실 광원으로 재조명 금지) — 애니메 캐릭터가 현실 조명을 받는 실패를 겪어본 نویسنده의 문장으로 추정. 단, 작성자 확인 없으므로 prompt-derived로만 기록
- text constraint: "屏幕上唯一的文字" (화면 유일 텍스트) "THE END!" — 텍스트 seep 방지
- 관찰 (frame-observed): 변형된 캐릭터들이 플랫 음영 유지 ✓, "THE END!" 텍스트 미확인 (10초 압축으로 마지막 비트가 짧음 — 부분)
- generic negative: 없음

### 11. Control Levels
- Hard Lock: 魔法法则 (변형 시퀀스), conservation law (5속성 보존), "从未被现实世界光线重新照明", 원테이크, 펜 상시 프레임
- Soft Guidance: [摄影] imperfection spec, [光线], [场景] 경로
- Creative Freedom: 변형 캐릭터의 디자인, 행인

### 12. Why it may work
A. Evidence-backed:
- 5개 비트가 10초 안에 전부 렌더됨 (frame-observed) — 변형 시퀀스 템플릿이 동작
- conservation law가 지켜짐 — 거대 고양이가 버스의 크기·위치·방향 유지 ✓
- 펜이 10초 내내 프레임 안에 있음 — prop 앵커 유지 ✓
- 플랫 음영 유지 — 렌더링 제약이 동작 ✓

B. Inference:
- "한 번 정의, 여러 번 적용"은 모델의 추론 부담을 줄임 — 매 비트마다 새로 설명하지 않음
- 원테이크+단일 경로+펜 앵커 = 연속성 실패 표면 최소
- 의성어 "Biu!"는 트리거를 청각적으로도 고정 — 멀티모달 앵커일 수 있음 (inference)

### 13. Popularity signal
- rank: 10 / likes: 140
- likely_driver: novelty (매직펜 컨셉 — 독창성), prompt_structure (魔法法则 — 재사용 용이), visual_subject, unknown
- 판단: 컨셉의 독창성이 인기에 기여했을 가능성. 구조 기여도 단정 불가

### 14. Relation to existing XAI-Studio patterns
- Continuous Action: 강화 (원테이크 선언)
- Reference Role Separation: 강화 (펜/손/목표물의 역할 분리)
- Trace-first physics: 강화 — conservation law가 trace-first의 보존 법칙 버전
- Relative Spatial Coordinates: 강화 ("确切的大小、位置、速度、方向和透视")
- 트리거 문법: #1, #46, #2와 동형 — 변형 시퀀스 버전으로 확장
- #47의 per-shot SFX: 비트별 SFX 라인으로 강화
- #45의 deliberate imperfection: [摄影] 섹션으로 강화 (가장 상세한 버전)

### 15. Candidate contribution
- new rule 후보: **universal transformation rule (魔法法则)** — 변형 시퀀스를 한 번 정의하고 N번 적용. (최종 D에서 검토)
- new rule 후보: **conservation law** — "원본의 크기·위치·속도·방향·투시를 보존". (최종 D에서 검토)
- new failure-sourced negative 후보: **"never re-lit" rendering constraint** — 스타일화된 요소의 조명 고정. (최종 D에서 검토)
- 그 외 reinforces existing patterns

---
