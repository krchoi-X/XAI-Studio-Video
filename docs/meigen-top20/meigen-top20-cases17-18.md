# MeiGen Top 20 — Case 17·18 (15섹션 분석)

> 분석 파일 분리본. 본편(meigen-top20.md)은 건드리지 않음.
> 증거 규율: frame-observed / prompt-derived / author-described / text-guide / inference.
> 주의: 두 케이스의 프롬프트 verbatim 전문은 브라우저 수집 핸드오프에 있었으나 컨텍스트 컴팩션으로 소실. detail 페이지 직접 접근은 403 차단으로 재확인 불가. 아래 prompt-derived 내용은 수집 요약(태스크 경유)에 보존된 인용 구절과 구조 사실에만 근거하며, 인용 부호가 없는 서술은 요약 기반 재구성임을 표시함.

---

## Case 17 — K "Inception-style time-stop, finger snap trigger" [재수집 스냅샷 rank 6]

### 1. Source
- URL: https://www.meigen.ai/video/2069634741926867051
- creator: K (@ChillaiKalan__)
- model: Seedance (MeiGen 배지)
- duration: 13.54초 실측 (809프레임/60fps/1920x1080). 프롬프트의 0:00–0:15 구조보다 약 1.5초 짧음
- popularity: 재수집 스냅샷 rank 6, 118 likes (조회수 미표시)

### 2. Evidence basis
- prompt-derived (수집 핸드오프 요약 경유 — verbatim 전문 소실, detail 페이지 403으로 재확인 불가. 인용 구절은 핸드오프 원문 유지분)
- frame-observed (8프레임 추출 + 컨택트시트). 프롬프트와 매칭됨 — 핵심 이펙트(시간 정지) 렌더 확인
- inference: Why it may work B항

### 3. Prompt structure
타임스탬프 5비트 구조 ([0:00–0:03] ~ [0:12–0:15]). 수집 요약 기준 구조 분해:
- style anchor: Inception식 시간정지 (영화 레퍼런스 한 줄로 전체 톤·이펙트 방향을 전달)
- identity block: "Use the reference image as the exact protagonist"
- trigger definition: 손가락 스냅 = 세계 정지/복원의 토글 (스냅 한 번에 freeze, 다시 스냅에 restore)
- beat chain: shockwave → freeze → walk (정지된 세계를 걸음) → snap → restore
- negative: "No coffee cup" (소품 제거 지시)
- duration 설계: 15초. 실측 13.5초로 미달 — 비트 압축 또는 후반 비트 단축으로 추정 (inference)

### 4. Subject / Character state
- identity lock: reference image ("exact protagonist") — 있음
- wardrobe lock: 갈색 티셔츠 + 선글라스 + 실버 체인 — 렌더에서 전 구간 유지됨 ✓ (frame-observed)
- prop lock: 없음 ("No coffee cup"으로 손 주변 소품 제거)
- character count: 1 (+ 정지된 군중 — 배경 액터)
- gaze assignment: 프롬프트 지정 여부 미확인. 렌더에서 오버숄더 카메라 응시 확인 (f005) — frame-observed

### 5. Camera / Shot design
- single continuous shot (사실상): 정지된 세계를 걸어가는 원테이크. 명시적 컷 선언 없음
- camera role: 동반자 — 주인공과 함께 이동하며 정지된 군중을 스쳐 지나감
- subject-camera relationship: 정면 워킹 → 오버숄더 돌아보기 (f005). 카메라를 관객 대리자로 사용
- movement의 story function: 카메라의 움직임이 "유일하게 살아있는 것"의 증거 — 정지된 세계와 움직이는 카메라의 대비가 이펙트를 증명

### 6. Spatial / Continuity
사용 채널: identity (reference — 유지됨 ✓), wardrobe (유지됨 ✓), location (NYC 거리 — 유지됨 ✓), lighting (골든아워 — 유지됨 ✓). 세계 상태(world-state) 채널이 핵심: 행인·비둘기·차량의 "정지"가 장면 전체의 연속성 조건으로 작동. 정지된 요소들의 자세가 프레임 간 고정됨 (f003 — 미드스트라이드 행인, 공중 정지 비둘기).

### 7. Action grammar
- 핵심 장치: **trigger-bound world-state toggle** — 손가락 스냅이라는 단일 신체 동작이 세계 상태의 토글(freeze/restore)에 바인딩됨
- anticipation → contact → consequence: shockwave (anticipation) → snap (contact) → freeze (consequence) → walk → snap → restore. 대칭 구조
- Case 05의 "선글라스 착용 → 세계 부활" 토글과 동형, Case 02의 "손이 움직일 때마다 VFX" 바인딩과 동계열 — 트리거 문법의 반복 출현
- action density: 중간 (걷기 단일 액션 + 세계 상태 전이가 전부)

### 8. Reference usage
- reference image = protagonist identity-only. 단일 authority, 역할 분리 있음 (identity vs. 세계/장소는 텍스트)

### 9. Audio / Dialogue
- dialogue: 없음 (수집 요약에 대사 정보 없음)
- SFX/music: 수집 요약에 오디오 정보 없음 — 기록 불가. shockwave·스냅 계열 SFX 존재 가능성은 inference로만 남김

### 10. Failure prevention
- "No coffee cup" — 네거티브. 스냅 손동작을 가릴 수 있는 소품을 사전 제거하는 실패 기반일 가능성이 있으나 (inference), 근거 없으므로 generic/실패 기반 구분 불가로 기록
- 관찰된 드리프트 (frame-observed): duration drift — 15초 설계 vs 13.5초 실측. 비트 구조는 유지된 것으로 보임

### 11. Control Levels
- Hard Lock: reference identity, 스냅=토글 트리거, 5비트 타임스탬프, "No coffee cup"
- Soft Guidance: Inception-style 톤, NYC 거리, 정지 대상(행인·비둘기) 범위
- Creative Freedom: 군중 구성, 차량·간판 디테일, 워킹 리듬

### 12. Why it may work
A. Evidence-backed:
- 핵심 이펙트 렌더 성공 (frame-observed): 공중 정지 비둘기, 미드스트라이드 정지 행인, 정지된 차량 — "세계 정지"가 화면에 구현됨
- **Case 05와의 결정적 대비**: C05의 "entire city freezes"는 미렌더(행인 모션 블러, 차량 이동)였으나 C17의 정지는 렌더됨. 구조상 차이점 — (1) C05는 단일 샷의 액션 라인에 정지를 선언, C17은 5비트 구조의 중심 장치 + 스냅 트리거로 명시. (2) 정지 범위가 좁음 (C05: 도시 전체·차량·새 / C17: 행인·비둘기 수준). (3) freeze→restore 대칭 토글로 상태 전이가 닫힘
- 의상·로케이션·조명의 전 구간 유지 — 앵커가 지켜짐

B. Inference:
- 스냅 트리거는 단일·명확한 신체 동작 — Case 02의 손 움직임 바인딩 성공과 같은 계열. 트리거가 신체에 바인딩되고 범위가 좁을수록 world-state 지시의 렌더 성공률이 높은 것으로 보임 (C05 실패 vs C17 성공의 가설 — 추가 표본 필요)
- "Inception-style" 한 줄 앵커는 톤·이펙트·무드를 저비용으로 전달하는 장치
- 정지된 세계 속 "유일하게 움직이는 카메라"는 이펙트의 증거를 자동으로 생성 — 별도 설명 샷 불필요

### 13. Popularity signal
- rank: 6 (재수집 스냅샷) / likes: 118
- likely_driver: visual_subject (정지된 NYC 군중 속 워킹 — 썸네일·첫 3초 임팩트), prompt_structure (스냅 토글 — 재사용 용이), unknown
- 판단: 핵심 이펙트의 렌더 성공이 확인된 케이스 — C05와 달리 프롬프트-렌더 정합성이 높음. 단, 인기와 렌더 성공의 인과로 단정할 근거는 없음

### 14. Relation to existing XAI-Studio patterns
- world-state manipulation: C05는 실패 표본이었으나 C17은 성공 표본 — "정지 자체가 불가능한 게 아니라 범위·트리거 명시 방식의 문제"였음을 시사. C05의 Failure-Sourced Negatives 항목에 대조 표본으로 추가 필요 (new rule 아님, 기존 실패 표본의 정제)
- 트리거 문법: 강화 (C05 선글라스 토글, C02 손 움직임 바인딩과 동계열)
- Continuous Action: 강화 (원테이크 워킹)
- Reference Role Separation: 강화 (identity-only)
- Hard/Soft/Creative: 강화

### 15. Candidate contribution
- 신규 후보: **trigger-bound world-state toggle** — "스냅 한 번=freeze, 두 번째=restore" 대칭 토글 구조. C05의 실패와 C17의 성공을 가른 차이(트리거 바인딩 + 좁은 범위 + 대칭 복원)로, "world-state 지시는 트리거에 바인딩하고 범위를 좁혀라"는 정제 형태로 신규 후보 가능. (최종 D에서 검토)
- 방법론적 기여: 동일 계열 지시(C05 world-freeze)의 실패/성공 쌍 — 실패 표본 하나만으로 규칙을 닫지 말아야 한다는 증거 규율의 사례
- 그 외 reinforces existing patterns

---

## Case 18 — Oogie "Miniature Tiny-Person FX" [재수집 스냅샷 rank 7]

### 1. Source
- URL: https://www.meigen.ai/video/2077652652641681568
- creator: Oogie (@oggii_0)
- model: Seedance (MeiGen 배지)
- duration: 15.12초 실측 (362프레임/24fps/1920x1080). 00:00–00:15 구조와 일치
- popularity: 재수집 스냅샷 rank 7, 116 likes (조회수 미표시)

### 2. Evidence basis
- prompt-derived (수집 핸드오프 요약 경유 — verbatim 전문 소실, detail 페이지 403으로 재확인 불가. 인용 구절은 핸드오프 원문 유지분)
- frame-observed (8프레임 추출 + 컨택트시트). 5비트 전부 매칭, 엔딩 텍스트 확인. 단, 배경 드리프트 관찰 (아래)
- inference: Why it may work B항

**배경 드리프트 (frame-observed):** 프롬프트는 convenience store(편의점)이나 렌더는 대형 supermarket(슈퍼마켓) — 넓은 통로, 대형 진열대, 쇼핑카트. 장소 서술이 상위 카테고리(대형 마트)로 교체됨. C02·C08 계열의 장소 드리프트와 동형. 핵심(스케일·액션)은 유지되어 인기에 무해한 것으로 보임.

### 3. Prompt structure
5비트 타임스탬프 + 비트별 Camera/SFX 지정. 수집 요약 기준 구조 분해:
- FX declaration: "Miniature Tiny-Person FX" — 이펙트 카테고리를 장르 라벨로 선언 (스타일 블록 대신 이펙트 블록이 최상위)
- scale lock: 1:15 수치 고정 — 스케일을 숫자로 못박음
- beat chain (5비트 × 3초): 스낵선반 스윙 → 병뚜껑 파쿠르 → 집라인 → 소다캔 서핑 → 승리 피날레
- per-beat Camera + SFX 지정 (세부 내용은 요약에 없음)
- ending condition: 골드 텍스트 "CHALLENGE COMPLETE" — 화면 텍스트를 엔딩 조건으로 지정
- VISUAL REQUIREMENTS (네거티브 블록): "No animation, cartoons, narration, subtitles, outfit changes, or scale inconsistencies" — 6개 항목
- 없음: 대사, 레퍼런스 지정

### 4. Subject / Character state
- identity lock: 없음 (텍스트 서술만)
- scale lock: 1:15 — 렌더에서 유지됨 ✓ (거대 스낵백·병뚜껑·소다캔 대비 미니어처 인물. f001, f004)
- wardrobe lock: 렌더에서 점프수트 계열 전 구간 유지 (frame-observed — "outfit changes" 네거티브와 정합)
- character count: 1
- gaze assignment: 미확인 (수집 요약에 없음)

### 5. Camera / Shot design
- multi-shot: 5비트, 각 3초, 타임스탬프 명시
- per-beat Camera 지정 (세부 미확인 — 요약에 "비트별 Camera 지정" 사실만 있음)
- camera role: 액션 추적 — 스윙·파쿠르·집라인을 따르는 다이내믹 무브 (frame-observed: 로우앵글 추적, 매크로 느낌의 근접 촬영)
- framing: 거대 소품 대비 미니어처를 강조하는 로우앵글·클로즈업. 스케일 대비가 프레이밍의 주제
- Case 03(Sarah)의 비트별 SFX 구조와 동형 — 3초×5비트 밀도 문법의 반복 출현

### 6. Spatial / Continuity
사용 채널: scale (1:15 — 유지됨 ✓), prop (스낵백·병뚜껑·집라인·소다캔·쇼핑카트 — 유지됨 ✓), wardrobe (유지됨 ✓), location (convenience store → supermarket 드리프트 ✗). 스케일 락이 핵심 연속성 장치로 작동 — 장소가 바뀌어도 스케일 대비가 장면을 묶음.

### 7. Action grammar
- 핵심 장치: **scale-contrast action chain** — 1:15 스케일이 전 비트의 물리 조건. 일상 소품이 장애물/탈것으로 전환됨 (스낵백=대지, 병뚜껑=플랫폼, 집라인=이동 수단, 소다캔=서핑보드, 냉장고=등반 벽)
- anticipation → contact → consequence: 각 비트가 독립 미니 아크 (도전→수행→이동)
- "CHALLENGE COMPLETE" — 게임 클리어 문법. 5비트를 "도전 과제"로 묶어 완결감을 부여
- action density: 높음 (5개 액션 세트피스)

### 8. Reference usage
- 없음

### 9. Audio / Dialogue
- dialogue: 없음 — "No narration" 네거티브로 명시
- SFX: 비트별 지정 (세부 미확인 — 요약에 사실만 있음)
- music: 미확인 (수집 요약에 없음)
- beat sync: 3초×5비트 구조 — 선언 수준. 실제 싱크 미확인

### 10. Failure prevention
- VISUAL REQUIREMENTS 네거티브 블록 6개 항목: "No animation, cartoons, narration, subtitles, outfit changes, or scale inconsistencies"
- "scale inconsistencies"·"outfit changes"는 미니어처 FX의 대표 실패(스케일 붕괴·의상 변경)를 겨냥한 실패 기반일 가능성이 높으나 (inference), 근거 없으므로 구분 불가로 기록
- "animation, cartoons"는 스타일 드리프트 방지 (실사 유지), "narration, subtitles"는 오디오·텍스트 채널 잠금
- 관찰된 드리프트: 배경 장소 교체 (convenience → supermarket) — 네거티브 블록에 장소 락이 없었던 부재와 대응

### 11. Control Levels
- Hard Lock: 1:15 스케일, 5비트 타임스탬프, 엔딩 텍스트 "CHALLENGE COMPLETE", VISUAL REQUIREMENTS 네거티브 6개
- Soft Guidance: 비트별 Camera/SFX, 소품 구성 (스낵·병뚜껑·집라인·소다캔)
- Creative Freedom: 마트 내부 세부, 조명, 인물의 표정·동작 디테일, 장소 (drift 허용된 셈)

### 12. Why it may work
A. Evidence-backed:
- 5비트 전부 렌더에서 확인 (frame-observed): 스낵선반 위 질주, 가격택($9.99) 스윙, 병뚜껑 파쿠르, 통로 집라인, 쇼핑카트 위 스낵 더미, 소다캔 서핑, 냉장고 등반, 엔딩 골드 "CHALLENGE COMPLETE" 텍스트
- 1:15 스케일 유지 — 수치 고정이 전 구간에서 지켜짐
- "CHALLENGE COMPLETE" 화면 텍스트 렌더 성공 — C04의 화면 텍스트 라벨 성공과 동형
- Case 03의 비트별 SFX + 3초×5비트 구조와 동형 — 동일 밀도 문법의 반복 출현 (패턴 강화 증거)

B. Inference:
- 스케일 대비는 모델 친화적 — 단일 수치(1:15)가 장면 전체의 물리·프레이밍을 지배하므로 지시가 단순하고 실패 표면이 작음
- 게임 클리어 문법("CHALLENGE COMPLETE")은 완결감을 주는 저비용 엔딩 장치 — 별도 엔딩 샷 설계 불필요
- 배경 드리프트(convenience→supermarket)가 무해했던 이유 — 핵심 락(스케일·액션·소품)이 지켜지면 장소는 교체 가능한 변수. "장소 서술 < 물리 조건"의 우선순위 사례

### 13. Popularity signal
- rank: 7 (재수집 스냅샷) / likes: 116
- likely_driver: visual_subject (미니어처 vs 거대 소품 대비 — 썸네일 임팩트), prompt_structure (5비트 타임스탬프 — 재사용 용이), novelty (Tiny-Person FX 장르 라벨), unknown
- 판단: 렌더 정합성이 높은 케이스 (5비트 전부·스케일·엔딩 텍스트 모두 동작). 단, 인기와 렌더 성공의 인과로 단정할 근거는 없음

### 14. Relation to existing XAI-Studio patterns
- Trailer Montage: 강화 (3초×5비트 밀도 — C03·C05와 동일 문법)
- Failure-Sourced Negatives: 강화 (VISUAL REQUIREMENTS 6개 블록 — 실패 기반 가능성)
- Trace-first physics: 강화 — 1:15 스케일이 장면의 물리 조건으로 작동
- 화면 텍스트 엔딩: C04 강화 (new rule 아님)
- Hard/Soft/Creative: 강화
- C03과의 동형성: 비트별 Camera/SFX 지정 구조 반복 — 기존 패턴 강화 증거 (new rule 아님)

### 15. Candidate contribution
- 신규 후보: **scale-as-physics-lock** — "1:15" 수치 스케일 선언이 장면 전체의 물리·프레이밍 조건으로 작동. 기존 Trace-first physics의 특수형이나, 수치 스케일 고정이 독립 장치로 반복 출현하면 분리 검토. (최종 D에서 검토)
- 그 외 reinforces existing patterns
