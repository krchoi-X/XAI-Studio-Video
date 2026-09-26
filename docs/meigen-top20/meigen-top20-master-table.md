# MeiGen Top 20 — Master Comparison Table (Case 01~21)

> 21 케이스 / 실영상 20편 (C21 = C07 동일 영상의 재관측 — 행은 유지, 패턴 가중치는 1건으로 계산)
> 실측: ffprobe 프레임 수 기준. likes: 갤러리 카드 기준 (스냅샷 2026-09-26 21:14 KST, 구 1~10위는 이전 스냅샷)
> 증거 등급: ◎=프롬프트-렌더 정합 확인됨 / ○=부분 정합·드리프트 있음 / ✕=핵심 불일치

| Case | Creator | 실측 길이·스펙 | 프롬프트 구조 | 핵심 장치 | 렌더 정합 | likes | 비고 |
|---|---|---|---|---|---|---|---|
| C01 | Shore Lyn @Shorelyn_ | 36.0s · 24fps · 1276x718 | prose (여행 셀피) | — | ✕ 프롬프트(셀피)≠영상(드리프트) | 237 | 갤러리 불일치; 타이틀 0:15 vs 36초 |
| C02 | Sairah @Sairah_0 | 27.0s · 30fps · 1276x718 | 의미 블록 라벨 (Setting/Character/Action/VFX/Camera/Mood) | "Every time she moves her hands" VFX 트리거 바인딩 | ○ 트리거 동작; wardrobe drift(주황→회색), graffiti→anime 변이, text seep | 219 | 트리거 문법의 VFX 이식 |
| C03 | Sarah @AIwithSarah_ | 15.1s · 24fps · 1280x720 | FORMAT 헤더(15s/145BPM/15샷) + 15샷 + 샷별 SFX | BPM 헤더, LOGIC RULE 한 줄 | ○ 6/15샷 확인; 의상 아크 유지 | 206 | 1샷/초 밀도 |
| C04 | Maria @thisismariaa25 | 30.2s · 30fps · 1920x1080 | 10룩 번호 리스트 + 화면 텍스트 라벨 | 엔딩 콜라주 | ○ 콜라주 성공; 9:16→16:9 aspect drift | 204 | Day-cycle bookend 변형 |
| C05 | Sophia @sophiaparkerr_ | 15.1s · 24fps · 1280x720 | 5샷 타임스탬프 | "선글라스 착용 → 세계 부활" 토글 | ○ world-freeze 미렌더; 시선 비트 3개 동작 | 198 | C17의 실패 대조쌍 |
| C06 | simeon-sanai @Naiknelofar788 | 15.0s · 24fps · 3840x2160 | 하드컷 몽타주 (0.4초) | change-tolerance 선언 | ◎ 7대 불가사의 커버리지 | 168 | Travel Coverage 대표 |
| C07 | Shore Lyn @Shorelyn_ | 15.2s · 30fps · 1080x1920 | 스토리보드 프레젠테이션 프롬프트 | 제품 앵커 (KitKat) | ○ 광고만 렌더, 컨테이너 완전 붕괴 | 164 | container collapse 원형 |
| C08 | Oogie @oggii_0 | 15.1s · 24fps · 834x1112 | 단일 연속 샷 (360 오빗 + 정지) | 카메라 독점 + 파티클 정지 | ○ 피사체 불일치(정장남→츄리닝女); 오빗·정지는 동작 | 164 | 카메라 지시 > 피사체 서술 |
| C09 | Calira @CaliraVal | 15.3s · 30fps · 720x1240 | prose 제품 광고 | 제품 앵커 15초 유지 | ◎ 앵커 유지; "몰 걷기" 미렌더 | 149 | C15·C16과 동형 |
| C10 | 路飞 @0xluffy_eth | 10.2s · 24fps · 720x1280 | 魔法法则(변형 시퀀스 정의) + 5비트 | conservation law, trace-first | ◎ 5비트 전부 렌더 — 최고 매칭 | 140 | 타이틀 15秒 vs 10.2초(압축) |
| C11 | Kashberg @Kashberg_0 | 34.2s · 24fps · 1276x720 | **JSON** (subject/scenes[7]/camera_work/style/render_settings) | 탈것을 subject 하위 키로 잠금; 슬로모 국소 바인딩 | ◎ 7씬 전부 렌더 | 134 | 코퍼스 유일 JSON; 네거티브·오디오 지시 없음 |
| C12 | WasifAI @doctorwasif | 15.2s · 30fps · 1920x1080 | 의미 블록(OUTFIT/LOCATION/CAMERA) + 7비트 + 네거티브 5연타 | 12항목 imperfection 긍정 스펙, @image1 | ○ 7비트 전부 매칭; "Unglamorous" 미렌더(글래머러스) | 130 | deliberate imperfection 최완전 표본 |
| C13 | Sharon Riley @Just_sharon7 | 15.1s · 24fps · 1280x720 | 7샷 파라그래프 + 네거티브 ~40항목 | 바람을 "third character"로 지정; 스케일 부등식 락 | ○ 7샷 전부 렌더; 의상 단순화 drift | 125 | ~5947자, 코퍼스 최장 프롬프트 |
| C14 | el.cine @EHuanglu | 69.5s · 24fps · 1280x720 | 의미 블록(CAMERA/PERFORMANCE/VOICE/…) + 2샷 | EMOTION=BODY, STAGING fixed, 인덱스 레퍼런스 3종 | ○ 2샷만 기술→모델이 69.5초 자립 확장 | 122 | under-specification 사례; 코퍼스 최장 영상 |
| C15 | Ruzaina @RuzainaMeer | 12.1s · 24fps · 1280x720 | 단일 문단 UGC 광고 | toward-camera 피날레, 엔딩 텍스트 고정 | ◎ 인물·제품·엔딩 텍스트 유지 | 120 | 최소 스펙 성공 — 하한선 데이터 |
| C16 | Avelyrah @AvelyrahnAI | 12.1s · 24fps · 720x1280 | 단일 문단 접속사 체인 | freeze→매크로→"BOSS" 수신전화 | ◎ 동결·매크로·전화 비트 렌더 | 119 | C05 freeze의 성공 대조쌍 |
| C17 | K @ChillaiKalan__ | 13.5s · 60fps · 1920x1080 | 5비트 타임스탬프 + 스냅 트리거 | snap=freeze/restore 대칭 토글 | ◎ 정지 이펙트 렌더 (C05와 정반대) | 118 | D-1 핵심 근거 |
| C18 | Oogie @oggii_0 | 15.1s · 24fps · 1920x1080 | 5비트 × 비트별 Camera/SFX | "1:15" 수치 스케일 락, "CHALLENGE COMPLETE" | ○ 5비트 전부; convenience→supermarket drift(무해) | 116 | C3와 동형 구조 |
| C19 | Latte @0xbisc | 17.7s · 30fps · 1080x1080 | 2-part (캐릭터시트 + 6비트 추격 타임라인) | 휘파람-정지 오디오 트리거 바인딩 | ○ 비트 순서 유지(오프셋 있음); 시트 컷어웨이 삽입 | 123 | 컨테이너 부분 붕괴; role bleed |
| C20 | Sharon Riley @Just_sharon7 | 15.0s · 60fps · 1920x2160 | 2-part (9패널 인포그래픽 + 9씬) | "Strict chronological shot order" | ◎ 9씬 순서 준수; 컨테이너 하단 스트립 유지 | 130 | 컨테이너 유지; 9:16 지정 vs 8:9 렌더 |
| C21 | Shore Lyn @Shorelyn_ | 15.2s · 30fps · 1080x1920 | 스토리보드 그리드 프롬프트 | (C07과 동일) | ○ (C07과 동일) 광고만 렌더 | 164 | **C07 중복** — 패턴 가중치에서 제외 |

### 길이 분포 요약
- 15초 전후(12~18s): 13건 — 주류
- 장척(27~36s): C1, C2, C4, C11 — 4건
- 예외: C14 69.5s (under-spec 자립 확장), C10 10.2s (압축)
