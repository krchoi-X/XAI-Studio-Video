# Evidence — Grok·Muse 레퍼런스 교차 검증 (2026-09-26)

> 이 파일은 **사실과 측정값만** 담는다. 해석·권고는 [claude-opinion.md](claude-opinion.md)에 있다.
> 모든 판정 행에는 출처와 재현 방법을 붙였다. 다른 에이전트는 §6 명령으로 독립 재현할 수 있다.
> 수집: Claude Code (claude-opus-5-5), 2026-09-26.

## 1. 수집물 인벤토리

### Grok — `D:/AI_Studio/ref-videos/2026-09-22-directing-patterns/` (git 밖, 176MB)
| 항목 | 수 | 비고 |
|---|---:|---|
| `cards/PAT-*.md` | 71 | 패턴 카드, 2026-09-22~25 |
| `cards/BATCH-*.md` | 14 | 배치 요약 |
| `videos/` | 56 | mp4(+`.jpg` 1). 5건은 영상 없음(`_SKIPPED.md`), ~12건 대용량 원본은 box에만 있음(`COPY-LOG.md`) |
| `prompts/` | 63 | 캡션·프롬프트·메모 |
| `look-vocab/` | 12 | README + sheets 5 + images 6 |

카드 섹션: Kind / Source evidence / Do not copy / Story function / Camera DNA / Blocking / Cut·generation / Continuity locks(Hard·Soft) / Soft motif / Prompt-solvable vs limit / Attach.

### Muse (Somni) — `docs/reference-state-analyses.md` (origin/main `2363226`, 3,519줄)
- 40개 분석. 1~9번 구 양식, 10~40번 신 양식. 근거 태그: prompt-derived / author-described / frame-derived / inference
- 마스터 패턴 20개 ↔ 프레임워크 매핑표, 승격 후보 43개(★ 신뢰도)
- 동반 문서: `docs/methodology-opinion-somni.md` (origin/main `47459d7`)

## 2. 겹치는 레퍼런스 매핑과 파일 실측

실측 대상은 Grok 로컬 파일(`videos/`)이다. Muse가 받은 파일은 레포에 없어서 Muse 문서에 적힌 수치를 그대로 옮겼다.

| Muse # | Grok 카드 | 원 게시물 | Grok 파일 실측 (W×H, fps, 길이) | Muse 기재 |
|---|---|---|---|---|
| 26 | cafeteria-soda-1v2-ladder | X @pyona_ai | 1920×1080, 24, 30.93s | "30초, 9:16 세로, 24fps" |
| 27 | liveaction-manga-cutladder | Threads @darkjl81 | 정지 이미지 1672×941 | 영상·이미지 없음, 프롬프트만 |
| 33 | warehouse-hitfeel-lt | Threads @jeong_do_ryeong | 1280×720, 24, 10.22s | 10초 |
| 34 | practice-drumcam-lt | Threads @jeong_do_ryeong | **480×848, 30, 3.34s** | **10초, 24fps, 1280×720 (영상1)** |
| 35 | freedive-buoyancy-lt | Threads @jeong_do_ryeong | 1280×720, 24, 10.22s | ~10초, 24fps, 1280×720 |
| 36 | t1000-polyalloy-rise-lt | Threads @jeong_do_ryeong | 1280×720, 24, 10.22s | ~10.2초 |
| 37 | sports-signal-open-ladder | Threads @jeong_do_ryeong | 1280×720, 24, 10.22s | 10초, 24fps, 1280×720 |
| 39 | bridge-dive-rescue-ladder | X @AIwithzayn | 1280×720, 24, 44.47s | 44.47초 |
| 40 | gym-core-vlog-height-ladder | X @doctorwasif | 1920×1080, 24, 15.14s | 15.14초, 1920×1080, 24fps |

Muse #38(@chase90re 60초 액션)에 대응하는 Grok 카드는 없다.

## 3. 불일치 항목과 판정 근거

### E1. #34 드럼 — 두 소스가 서로 다른 영상을 분석함
- Muse #34: "캐러셀 2개 영상 (각 10초, 24fps, 1280×720). 영상1 직접 다운로드". 심벌 진동·스포트라이트 프레임을 관찰.
- Grok 카드: 3.34s 480×848 30fps 실사 직캠을 이 게시물의 파일로 판단. "prompt.txt = unused concert gen text", "DOM extra mp4s (`cand-1` stage kit …) are feed siblings".
- 실측 (2026-09-26, 로그아웃 상태로 `threads.com/@jeong_do_ryeong/post/DdrVYeZiVap`를 열고 `<video>` 요소 확인):
  - 본문 캐러셀: 1280×720 **10.215s**, 1280×720 **10.111s**
  - 페이지 하단 "관련 스레드": **@drum_minjeong "아이쿠…" — 480×848 3.341s** ← Grok 파일과 같은 규격
  - 그 아래: @yu_h.8 "요거는 드럼직캠" — 480×854 75.84s
  - 작성자 댓글: 영어 3-Phase 프롬프트("Cinematic 60fps dynamic handheld shot, 35mm …")
- 콘택트 시트: Grok 파일은 실사 연습실 영상이고 Dola 워터마크가 없다 (시트는 저장하지 않음. 실존 개인 영상이라서).

### E2. #37 스포츠 시그널 — 엠블럼 형태
- Muse #37 (frame-derived): "9s: 라이트 트레일이 수렴한 **원형 엠블럼**, 시안→화이트 그라데이션 — 기하학적 동일성 유지"
- Grok 카드: "prompt asked circular — file is S"
- 실측: 마지막 컷(7.96s~)은 **금속성 "S"자 엠블럼**이다. 그 직전에 오렌지 나선 트레일이 있다. `_review-20260926/sports-signal-contact-0.8s.jpg` 마지막 칸.

### E3. #37 스포츠 시그널 — 농구 컷 존재
- Muse #37: "농구 버즈아이 세그먼트는 6프레임 중 미포착 (압축·생략 추정, 샘플링 한계로 미확인)"
- 실측: 3.71~4.54s에 버즈아이 농구 골대 컷이 있다 (같은 시트 2행 2열).

### E4. #37 스포츠 시그널 — 컷 타이밍
- 프롬프트의 하드컷 시각 (Muse·Grok 모두 기재): 0.4 / 2.3 / 4.0 / 5.6 / 8.0s
- 실측 scene detect (threshold 0.2): **2.667 / 3.708 / 4.542 / 5.542 / 7.958s**

| 컷 | 프롬프트 | 실측 | 차이 |
|---|---:|---:|---:|
| 스팅어→육상 | 0.4 | 2.667 | +2.27 |
| 육상→농구 | 2.3 | 3.708 | +1.41 |
| 농구→축구 | 4.0 | 4.542 | +0.54 |
| 축구→얼굴 | 5.6 | 5.542 | −0.06 |
| 얼굴→(트레일·로고) | 8.0 | 7.958 | −0.04 |

- 구간 길이: 스팅어 2.67s(지정 0.4) / 육상 1.04 / 농구 0.83 / 축구 1.00 / 얼굴 2.42 / 로고 2.26
- Muse의 추론 문장: "모델이 6비트를 절대 시간대로 지키지 않고 순서를 유지한 채 압축·이동". Muse 방법론 문서 §5-3: "절대 시간 금지 … 프레임으로 두 번 확인됐다(#31·#37)"
- #31은 이번에 재측정하지 않았다 (Grok 대응 카드 없음).

### E5. #26 오렌지 소다 — 화면비
- Muse #26 기본 정보: "Seedance 2.5, 30초, **9:16 세로**, 24fps". 증거 기반 표기는 "prompt-derived + frame-derived (9프레임)"
- Grok 카드: "Prompt writes 9:16 / 4K — file is 16:9 1080p; follow the file"
- 실측: Grok 파일 **1920×1080**. 단, Muse가 다른 파일(다른 해상도의 배포본)을 받았을 가능성은 이 레포 자료로 배제할 수 없다.

### E6. #40 짐 브이로그 — 배경 요소
- Muse #40 (frame-derived): "Setting 요소(물병·라커·**거울벽**·오버헤드 조명)가 전 프레임에서 유지"
- Grok 카드: "Prompt writes mirror-wall gym … file is locker-row gym; follow the file"
- 실측 (`_review-20260926/gym-core-vlog-contact-2s.jpg`): 라커 열, 벤치, 물병, 천장 다운라이트는 보인다. 거울벽으로 식별되는 면은 이 시트에서 확인되지 않았다 (2초 간격 샘플이라 **부재를 증명한 것은 아님**).
- 참고: "MiniDV 질감"은 Muse가 author-described로 올바르게 태그했다. Grok 카드는 "file is cleaner than true MiniDV"라고 적었고, 시트에서도 테이프 노이즈나 블룸은 두드러지지 않는다.

### E7. #27 포니 다운힐 — 상호 보완
- Grok 카드: "prompt? No (`prompt-notes.txt` = credit only; replies = reaction)"
- Muse #27: 프롬프트 전문(한국어, CUT 1–9)을 확보했고, 첨부 이미지는 "CDN 만료로 미확인"
- 실측 (2026-09-26 로그아웃 페이지): 작성자 셀프 댓글에 프롬프트가 있고 `CUT n` 표기가 9회 나온다.
- 비교: Muse가 요약한 CUT 순서는 "1 와이드 접근 → 2 얼굴 ECU → 3 눈 ECU → 4 기어 → 5 페달 → 6 스티어링 → 7 와이드 진입 → 8 얼굴 CU → 9 외부 와이드 탈출"이다. Grok 보드 판독은 "cabin CU → exterior MW → eyes ECU → shifter → pedal → gauges → rear LS → profile CU"(약 8패널)다. 둘은 개수와 순서가 다르다.

## 4. 기타 사실

- **저자 중복**: Muse #8·#33·#34·#35·#36·#37은 모두 Threads @jeong_do_ryeong이다. Muse 승격 후보 중 출처가 이 저자로만 이루어진 ★★ 항목: #8 상태 구별화(8·35), #14 anti-cut(33·37), #15 비트표(31·37 — 31은 다른 저자), #20 POSITIVE LOCKS(33·37), #22 관계형 부정문(33·35).
- **CHASE 이름**: #22(@QAiStudio), #38(@chase90re), #40(@doctorwasif)에 같은 이름 "CHASE"가 쓰인다 (Muse 기재).
- **Grok 카드 노이즈**: 카드 85개 중 51개에 ` Soft` 토큰이 비정상적으로 삽입돼 있었다 (합계 7,444회, 09-25 카드는 전체 단어의 최대 약 40%). 정리 내역은 Grok 폴더 `_CLEANUP-LOG-20260926.md`, 원본은 `_backup/cards-pre-cleanup-20260926/`.

## 5. Muse 승격 후보와 현재 레포 문서의 대응 (grep 결과, `docs/` `skills/` `SKILL.md`, Muse 문서 2건 제외)

| 후보 개념 | 레포 내 기존 언급 |
|---|---|
| Control Levels / Hard Lock | `docs/architecture.md`, `docs/reference-extraction.md`, `docs/render-broker.md` |
| Motion Budget (#34) | `docs/architecture.md`, `docs/reference-driven-production-pipeline.md`, `SKILL.md` |
| Audio DNA | `docs/architecture.md`, `SKILL.md` |
| Physics Lock / Reaction Evidence (#6·#11) | `docs/action-design.md`, `docs/architecture.md`, `SKILL.md` |
| Action Grammar (#7) | `docs/action-design.md`, `docs/architecture.md`, `docs/reference-driven-production-pipeline.md` |
| Shot Graph / 시선 (#1) | `docs/architecture.md` 외 시선 관련 17개 파일 |
| POSITIVE LOCKS (#20) | `docs/director-memory/compiled-video-prompt-anatomy.md` (다른 레퍼런스 기반) |
| 레퍼런스 역할 분리 (#23) | `docs/director-memory/intent-alignment-method.md` 외 |
| lip-sync (#17) | `docs/director-memory/failures.md` 외 4 |
| headcount (#4), "does not cut on its own" (#14), 관계형 부정문 (#22), 실패 출처 네거티브 (#24), Necessity (#31), irregular timing (#10) | 없음 |

렌더러 맥락 (`docs/director-memory/capabilities.md`, 2026-09-16 스냅샷): 기본 로컬 경로는 WanGP(H3 포함)와 Krea 2 스틸이다. Muse 40건 중 모델이 명시된 것은 주로 Seedance 2.5 / Dola AI이고, 둘 다 한 번 생성에 여러 컷을 담는 엔진이다.

## 6. 재현 명령

```bash
V=D:/AI_Studio/ref-videos/2026-09-22-directing-patterns/videos
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate:format=duration -of csv=p=0 $V/PAT-20260925-sports-signal-open-ladder.mp4
ffmpeg -hide_banner -i $V/PAT-20260925-sports-signal-open-ladder.mp4 -vf "select='gt(scene,0.2)',showinfo" -f null - 2>&1 | grep -oE 'pts_time:[0-9.]+'
ffmpeg -v error -y -i $V/PAT-20260925-sports-signal-open-ladder.mp4 -vf "select='isnan(prev_selected_t)+gte(t-prev_selected_t\,0.8)',scale=320:-1,tile=4x3" -vsync vfr -frames:v 1 sports.jpg
ffmpeg -v error -y -i $V/PAT-20260925-gym-core-vlog-height-ladder.mp4 -vf "fps=0.5,scale=400:-1,tile=4x2" -frames:v 1 gym.jpg
```

Threads 확인: 로그아웃 브라우저로 게시물 URL을 열고 개발자 콘솔에서
`[...document.querySelectorAll('video')].map(v=>[v.videoWidth,v.videoHeight,v.duration])` 실행.
캐러셀·관련 스레드의 영상 위치는 `getBoundingClientRect().top`과 본문 텍스트 순서로 구분했다.

## 7. 이번에 확인하지 않은 것

- 겹치지 않는 Muse 31건과 Grok 카드 62개의 내용 정확도
- Muse #31(비트표 시간 불신의 다른 근거)의 재측정
- 드럼 게시물 영상2(10.11s)의 내용 (다운로드하지 않음)
- #39의 프롬프트 (두 소스 모두 미확보)
- Grok 카드 중 box에만 남은 대용량 원본 영상
