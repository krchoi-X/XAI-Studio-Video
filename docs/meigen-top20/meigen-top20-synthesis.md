# MeiGen 인기 VIDEO 프롬프트 Top 20 구조 패턴 채굴 — 종합 분석 (A–G)

> 대상: Case 01~21 (21개 케이스, 실영상 20편 — Case 21은 Case 07과 동일 영상의 재관측으로 패턴 가중치는 1건으로 계산)
> 수집 스냅샷: 2026-09-26 21:14 KST Popular 탭 (re-sort되는 피드이므로 순위는 스냅샷 기준)
> 증거 규율: frame-observed / prompt-derived / author-described / text-guide / inference
> 원칙: 인기를 품질의 증거로 간주하지 않는다. 추론은 inference로 분리, production rule로 승격 금지.
> 본 종합은 SKILL.md 규칙 확정이 아님. 신규 후보는 후보로만 기록.

---

## A. 반복 공통 구조 빈도 (21 케이스 / 실영상 20편 기준)

### A-1. 프롬프트 컨테이너 형식
| 구조 | 해당 케이스 | 빈도 |
|---|---|---|
| 타임스탬프 비트 (00:00–00:03 형식) | C3, C5, C6, C7, C12, C17, C18, C19, C20 | 9/20 |
| 의미 블록 라벨 분리 (Setting/Character/Camera 등) | C2, C3, C10, C11(JSON 키), C12, C14 | 6/20 |
| 접속사 체인 (라벨 없이 시간 순서 prose) | C1, C9, C15, C16 | 4/20 |
| 스토리보드/프레젠테이션 컨테이너 포함 | C7, C19, C20, C21(중복) | 3/20 unique |
| 2-part 프롬프트 (이미지 생성 + 비디오 생성) | C19, C20 | 2/20 |
| JSON 머신 리더블 | C11 | 1/20 |

### A-2. 기능 장치
| 장치 | 해당 케이스 | 빈도 |
|---|---|---|
| 트리거 바인딩 (신체 동작→이펙트/상태) | C2(손→VFX), C5(선글라스→세계 부활), C10(변형 시퀀스), C14(스냅 푸시→카메라), C17(스냅→freeze/restore), C19(휘파람 정지→액션) | 6/20 |
| 화면 텍스트 지정 (라벨/엔딩/폰 화면) | C4, C7, C15, C16, C18, C20 | 6/20 |
| 레퍼런스 이미지 바인딩 (@image) | C3, C12, C14, C17, C19 | 5/20 |
| 네거티브 블록 | C12, C13, C14, C17, C18 | 5/20 |
| 오디오/SFX 스펙 (diegetic 리스트·비트별 SFX) | C3, C12, C18, C19 | 4/20 |
| 대사 포함 | C14, C15, C20 | 3/20 |
| 제품 앵커 (광고 아크) | C7, C9, C15, C16, C20 | 5/20 |

### A-3. 장르 분포
- 인물/브이로그/라이프스타일: C1, C2, C3, C6, C8, C12 (6)
- 제품 광고: C7, C9, C15, C16, C20 (5)
- VFX/월드 조작: C2, C5, C10, C13, C17, C18 (6)
- 패션/룩북: C4 (1)
- 내러티브 대결: C14 (1)
- 추격 액션: C19 (1)

---

## B. 길이·밀도 분석

### B-1. 실측 길이 분포 (ffprobe 프레임 실측)
| 길이 대역 | 케이스 |
|---|---|
| 10~14초 | C10(10.2), C15(12.1), C16(12.1), C17(13.5) |
| 15~18초 (주류, 13건) | C3(15.1), C5(15.1), C6(15.0), C7(15.2), C8(15.1), C9(15.3), C12(15.2), C13(15.1), C18(15.1), C20(15.0), C21(15.2), C19(17.7), C4는 30.2로 제외 |
| 27~36초 (장척) | C2(27.0), C4(30.2), C11(34.2), C1(36.0) |
| 60초+ (예외) | C14(69.5) — 코퍼스 최장 |

### B-2. 프롬프트 길이 vs 영상 길이: 무관
- C13: 약 5947자(코퍼스 최장 프롬프트) → 15.1초
- C11: 약 1370자(JSON) → 34.2초
- C14: 2개 샷만 기술(under-specification) → 69.5초 (모델 자립 확장)
- C15: 단일 문단 최소 스펙 → 12.1초 완결
- **관찰**: 프롬프트 문자량은 영상 길이·완성도와 상관없다 (inference 아님, 4개 표본의 직접 비교). 길이가 아니라 구조(비트 수·밀도)가 길이를 결정하는 것으로 보임.

### B-3. 지정 vs 실측 불일치 6건 (frame-observed)
1. C1: 타이틀 "(0:00–0:15)" vs 실측 36.0초
2. C4: 9:16 의도 vs 16:9 렌더 (aspect drift)
3. C10: 타이틀 "15秒" vs 실측 10.2초 (5비트 전부 렌더 — 압축)
4. C17: "0:00–0:15" 구조 vs 실측 13.5초 (후반 압축)
5. C19: "0:00–0:15" 타임라인 vs 실측 17.7초 (2.7초 초과)
6. C20: "vertical 9:16" 지정 vs 1920x2160 렌더 (8:9 — 컨테이너 스트립의 흔적 가능)
- **관찰**: 비트 *순서*는 지켜지나 *절대 시간*은 모델 재량. 타임스탬프는 순서 앵커이지 시간 강제 장치가 아님 (E-3에서 심화).

### B-4. 오디오 설계의 부재 (코퍼스 공통)
- 명시적 오디오 스펙: 4건 (C3 per-shot SFX, C12 diegetic 리스트, C18·C19 비트별 SFX)
- 대사: 3건 (C14, C15, C20 — 각 2개)
- BPM 헤더: 1건 (C3)
- 나머지 14건은 무음 전제 또는 미지정. **인기 영상이라도 사운드 디자인은 프롬프트 밖(후반/플랫폼)에 맡기는 것이 기본값**으로 보임.

---

## C. 5대 패턴 (강화 빈도 순, §14 집계)

### 1위. Hard Lock / Soft Guidance / Creative Freedom — 20/20
전 케이스에서 강화. 사실상 코퍼스의 문법적 기본값. 단, C8처럼 "Hard로 의도한 것(피사체)이 지켜지지 않은 역설적 표본"도 있어, Hard Lock의 실효는 지시 *대상*에 따라 다름 (카메라/물리 > 피사체/장소 — E-5 참조).

### 2위. Trailer Montage (고밀도 비트 체인) — 9/20
C3(15샷/15초), C4(10룩), C5(5샷), C6(0.4초 컷), C7(10씬), C11(7씬), C18(5비트×3초), C19(6비트), C20(9씬). "1~3초/비트" 밀도가 15초 완결형의 표준. C3의 분석대로 밀도는 모델의 drift 누적 시간을 최소화하는 효과가 있을 수 있음 (inference).

### 3위. Identity-Locked Lifestyle (+제품 앵커 변형) — 8/20
C1, C6, C9, C12, C20이 강한 형태. C2·C4·C5는 텍스트 약형(부분 drift). 제품 버전(C7, C9, C15, C16, C20)은 "단일 앵커 15초 유지"가 반복 성공 — 광고 아크의 표준형.

### 4위. 트리거 문법 (trigger-bound effects) — 6/20
C2(손→VFX), C5(선글라스→세계 부활), C10(변형 시퀀스), C14(스냅 푸시→카메라 무브), C17(스냅→freeze/restore 토글), C19(휘파람 정지→액션, 오디오 버전). #1의 CUT-as-trigger, #46의 CUT ON에서 시작된 계열이 VFX·카메라·오디오로 확장됨. **코퍼스에서 가장 활발히 변주되는 장치.**

### 5위. Reference Role Separation — 5/20 (+대비 1)
C3(@image1 identity-only), C10, C14(캐릭터/환경/보이스 인덱스 그룹 분리 — 가장 명시적), C17(identity-only), C20(컨테이너 역할 유지). C19는 role bleed(캐릭터 시트→콘텐츠 삽입)의 대비 사례로 패턴의 경계를 보여줌.

### 차순위 (6~7위, 각 5/20)
- Failure-Sourced Negatives: C2, C12, C13(크리처 40항목), C14, C18
- Continuous Action: C8, C9, C10, C17, C19

---

## D. 신규 후보 (최대 5 — "진짜 새로울 때만", 규칙 승격 금지)

### D-1. trigger-bound world-state toggle (C17)
- 내용: world-state 지시(시간 정지 등)는 (1) 단일 신체 동작 트리거에 바인딩하고, (2) 정지 범위를 좁히며, (3) freeze→restore 대칭 토글로 상태 전이를 닫을 것.
- 근거: C5 실패("entire city freezes" 미렌더) vs C17 성공(행인·비둘기 수준 정지 렌더)의 대조 쌍. 동일 계열 지시의 실패/성공 쌍은 코퍼스에서 유일.
- 상태: 후보. 추가 표본 필요.

### D-2. EMOTION = BODY, not labels (C14)
- 내용: 감정을 형용사 라벨이 아니라 신체 채널 나열(eyes, brows, mouth, head tilt, hands, shoulders, stance)로 지정.
- 근거: C14 verbatim "EMOTION = BODY (not labels)". #41의 emotion performance를 명명된 규칙으로 정식화한 첫 사례.
- 상태: 후보. C14 단일 표본.

### D-3. persistent force as character (C13)
- 내용: 바람 같은 환경 힘을 "third character"로 지정하고 영향 대상 리스트 + 행동 스펙(delayed secondary motion) + 연속성 채널(wind direction)을 부여.
- 근거: C13. 환경 블록과 분리된 "힘" 단위 스펙은 코퍼스 최초. 7샷 전부 렌더에서 바람 연속성 유지 확인 (frame-observed).
- 상태: 후보. C13 단일 표본.

### D-4. fixed staging declaration (C14)
- 내용: "STAGING (fixed): always at X, never together in the middle" — 위치 고정 + 금지 구역의 블로킹 락.
- 근거: C14. Spatially Anchored Scene의 블로킹 수준 확장. 69.5초 장척에서 두 캐릭터의 위치 관계가 유지됨 (frame-observed).
- 상태: 후보. C14 단일 표본.

### D-5. container-content congruence 가설 (C19/C20/C7 — 가설, rule 아님)
- 내용: 프롬프트 속 컨테이너(스토리보드 그리드·프레젠테이션 보드)의 렌더 운명은 내용과의 합동성에 달림 — (a) 서사 콘텐츠 자체(패널=씬 묘사)면 유지(C20 하단 스트립), (b) 순수 메타 포장(테두리·번호·캡션)이면 버려짐(C7/C21 완전 붕괴), (c) 레퍼런스성 컨테이너(캐릭터 시트)는 컷어웨이로 삽입(C19).
- 근거: 3-case 비교. A/B 테스트 필요 (F-5).
- 상태: **가설**. production rule 승격 금지.

### D-탈락 (note로만 기록)
- JSON container (C11): format-level 장치이나 효과 미검증 (단일 케이스, A/B 없음)
- per-shot SFX (C3), BPM header (C3), LOGIC RULE one-liner (C3): C1~10 종합 후보로 유지, 이번에 추가 표본 없음
- idle-life rule (C14): D-2에 흡수 가능 — 독립 후보에서 제외
- scale-as-physics-lock (C18): Trace-first physics의 특수형으로 기록, 분리 보류
- persistent container strip (C20): 단일 관측 — F A/B로 이관
- VFX trigger binding (C2): C17·C19 강화로 트리거 문법(4위 패턴)의 하위 장치로 편입

---

## E. 과대평가 가능 패턴 (5)

### E-1. 네거티브 프롬프트의 만능설
- C12: "Unglamorous", "No glamour" 5연타에도 피사체가 글래머러스하게 렌더됨 (frame-observed) — 추상 네거티브의 실패 역표본.
- 효과 있었던 네거티브는 실패 모드 특정형: C13 크리처 40항목(변형·해부학 오류 직접 열거), C18 VISUAL REQUIREMENTS, C17 "No coffee cup"(스냅 손동작 가림 방지).
- **정제**: 네거티브는 만능이 아니라 "관측된 실패 모드의 역열거"일 때만 가치. 일반 형용사 부정은 신뢰하지 말 것.

### E-2. "상세할수록 정합적"
- C13(5947자)와 C15(단일 문단) 모두 성공. C2의 상세 wardrobe 서술은 drift(주황→회색 후디).
- 문자량은 품질과 무관 (B-2). **밀도(비트 수/초)와 앵커(락 대상)가 변수이지 분량이 아님.**

### E-3. 타임스탬프의 시간 강제력
- 6건의 지정-실측 불일치 (B-3). 비트 순서는 지켜지나 절대 시간은 모델 재량.
- 타임스탬프는 순서 앵커이지 타이머가 아님. "0:12–0:15에 X"는 "마지막 비트에 X"로 읽어야 함.

### E-4. 인기 = 품질 (원칙 재확인)
- Popular 탭은 re-sort되는 피드 (C21=C07이 rank 7→10으로 재진입).
- C1은 프롬프트(여행 셀피)와 영상(드리프트)이 불일치하는데 rank 1.
- like 집계 기준 불일치 (갤러리 카드 vs schema.org — C11: 134 vs 3139).
- **인기는 발견 신호이지 품질 증거가 아님.** 본 종합의 모든 "may work" 판단은 렌더 정합(frame-observed)에만 근거.

### E-5. 장소/피사체 서술의 우선순위
- C18: convenience store→supermarket drift가 무해 (핵심인 스케일·액션이 지켜짐).
- C8: 피사체 불일치(정장남→노란 츄리닝女)에도 360 오빗 카메라 지시는 동작 — **카메라 지시가 피사체 서술보다 강함.**
- C2: wardrobe drift에도 VFX 트리거는 동작.
- **우선순위 가설** (inference, 규칙 아님): 카메라/물리/트리거 지시 > 장소/피사체/의상 서술. Hard Lock을 걸 대상은 전자 쪽.

---

## F. A/B 테스트 (최대 5)

1. **LOGIC RULE one-liner 유무** (C3): 동일 15샷 프롬프트에서 "Keep logical consistency in ..." 한 줄 제거 시 의상·소품 연속성 차이 측정.
2. **JSON vs prose 동일 내용** (C11): subject/scenes 키 구조를 prose로 풀어쓴 대조군 — 컨테이너 형식의 효과 검증.
3. **world-state 범위** (C5 vs C17): "도시 전체 정지" vs "행인·비둘기 수준 정지 + 스냅 트리거" — 정지 이펙트 렌더 성공률 비교.
4. **네거티브 구체성** (C12 vs C13): 일반형("no glamour") vs 실패-특정형(40항목 열거) — drift 억제율 비교.
5. **스토리보드 컨테이너 포함/제외** (C7/C21): 동일 씬 묘사에서 그리드·번호·캡션 제거 시 collapse 재현 여부 — D-5 가설 검증.

---

## G. 방법론 한계·주의

1. **순위 불안정**: Popular 탭은 고정 랭킹이 아니라 re-sort되는 피드. 모든 rank 표기는 2026-09-26 21:14 KST 스냅샷 기준. "Top 20"은 그 시점의 단면일 뿐.
2. **중복 집계**: C21은 C07과 동일 영상. 패턴 빈도 계산 시 1건으로 처리 (본 파일의 모든 "/20" 분모는 unique 20편 기준).
3. **오귀속 위험**: C11 수집 초기에 prose 프롬프트가 잘못 귀속된 사건 발생. detail-page 정본 대조를 원칙으로 함 (§2 Evidence basis에 명시).
4. **오디오 미검증**: 프레임 기반 분석의 한계. SFX·대사·립싱크의 렌더 여부는 prompt-derived로만 표기하고 12-A의 근거로 사용하지 않음.
5. **like 수 이중 기준**: 갤러리 카드 수치와 schema.org 수치(예: C11 134 vs 3139)가 다름. 13번 섹션은 갤러리 카드 기준, 병기만 함.
6. **verbatim 한계**: C17·C18은 detail 페이지 403으로 verbatim 전문 재확인 불가 — 수집 요약의 인용 구절 + 구조 사실에만 근거 (파일 상단에 명시). C11·C12·C13은 curl로 detail HTML에서 정본 재추출·검증됨.
7. **인과 단정 금지**: likely_driver는 13번 섹션에서 근거 없으면 unknown. 본 종합의 모든 패턴은 "반복 출현"이지 "인기 원인"이 아님.

---

## 붙여넣기 카드 — 신규 후보 5종 (Control Level 포함)

```
[RULE CANDIDATE] trigger-bound world-state toggle
Control: Hard Lock (트리거 바인딩) + Soft Guidance (정지 범위)
내용: 세계 상태 조작(시간 정지 등)은 단일 신체 동작(스냅 등)에 바인딩하고,
정지 범위를 좁게(행인·비둘기 수준) 선언하며, freeze→restore 대칭 토글로 닫는다.
근거: C5 실패 vs C17 성공 (MeiGen Top20 종합 D-1)
상태: 후보 — 추가 표본 필요, 규칙 승격 금지
```

```
[RULE CANDIDATE] EMOTION = BODY, not labels
Control: Hard Lock (신체 채널 지정)
내용: 감정을 형용사로 쓰지 말고 신체 채널 나열로 지정한다.
(eyes, brows, mouth, head tilt, hands, shoulders, stance)
근거: C14 "EMOTION = BODY (not labels)" (MeiGen Top20 종합 D-2)
상태: 후보 — C14 단일 표본
```

```
[RULE CANDIDATE] persistent force as character
Control: Soft Guidance (힘의 행동 스펙)
내용: 바람 등 환경 힘을 "third character"로 지정하고 영향 대상 리스트 +
행동 스펙(지연된 2차 모션) + 연속성 채널(풍향)을 부여한다.
근거: C13, 7샷 전부 렌더에서 바람 연속성 유지 (MeiGen Top20 종합 D-3)
상태: 후보 — C13 단일 표본
```

```
[RULE CANDIDATE] fixed staging declaration
Control: Hard Lock (블로킹)
내용: "STAGING (fixed): always at X, never together in the middle" —
캐릭터의 위치 고정 + 금지 구역을 블로킹으로 선언한다.
근거: C14, 69.5초 장척에서 위치 관계 유지 (MeiGen Top20 종합 D-4)
상태: 후보 — C14 단일 표본
```

```
[HYPOTHESIS — 규칙 아님] container-content congruence
Control: (해당 없음 — 모델 행동 가설)
내용: 프롬프트 속 스토리보드 컨테이너의 렌더 운명은 내용과의 합동성에 달림.
서사 콘텐츠(패널=씬 묘사)는 유지되고, 순수 메타 포장(테두리·번호)은 버려지며,
레퍼런스성 컨테이너(캐릭터 시트)는 컷어웨이로 삽입될 수 있다.
근거: C19/C20/C7 3-case 비교 (MeiGen Top20 종합 D-5)
상태: 가설 — A/B 테스트(F-5) 후 검토, 규칙 승격 금지
```
