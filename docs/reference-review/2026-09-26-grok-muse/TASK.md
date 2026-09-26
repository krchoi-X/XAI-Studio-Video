# Grok·Muse 레퍼런스 수집물 교차 리뷰 — 2026-09-26

Active editor: Claude Code (claude-opus-5-5)
Status: COMPLETE (리뷰 기록·정정 주석·카드 정리 완료, 미커밋) — 다른 에이전트 재검토 대기
Scope: 리뷰 기록 + Muse 분석집 정정 주석 + Grok 카드 정리. 코드·스키마·파이프라인 변경 없음.

## Goal
Grok(`D:/AI_Studio/ref-videos/2026-09-22-directing-patterns/`)과 Muse(`docs/reference-state-analyses.md`)가
모은 레퍼런스를 교차 검증하고, 다른 에이전트(Codex·Grok)가 객관적으로 재검토할 수 있게
**자료(evidence)** 와 **Claude 의견(opinion)** 을 분리해 기록한다.

## Constraints / Must Preserve
- Muse 원문은 수정하지 않는다. 정정은 `⚠️ 정정 (Claude, 2026-09-26)` 주석으로만 추가.
- Grok 카드 원본은 정리 전 백업(`_backup/`)하고 변경 로그를 남긴다. 비디오·프롬프트 파일은 건드리지 않음.
- 판정은 로컬 파일 실측(ffprobe·ffmpeg scene detect·프레임 추출)과 공개 페이지 확인에만 근거.

## Must NOT Do
미디어 삭제·다운로드, 패턴의 파이프라인 승격(별도 결정), push.

## Files
- [evidence.md](evidence.md) — 수집 자료와 실측 사실만. 해석 없음.
- [claude-opinion.md](claude-opinion.md) — Claude의 판단·권고. 반론 환영.
- Grok 폴더: `_CLEANUP-LOG-20260926.md`, `_backup/cards-pre-cleanup-20260926/`, `_review-20260926/`(콘택트 시트)

## Progress
- 2026-09-26: origin/main의 Muse 문서 2건(reference-state-analyses.md, methodology-opinion-somni.md)을 로컬 main에 머지(미push).
- 겹치는 9쌍 비교, 불일치 6건(E1~E6) 파일 실측·Threads 페이지로 판정.
- evidence.md / claude-opinion.md 작성. Muse 문서에 정정 주석 7곳(원문 불변, 추가만).
- Grok 카드 51개 "Soft" 노이즈 정리(7,444→120), 드럼 카드 소스 오류 경고, #27 프롬프트 병합 주석.

## Next
- 다른 에이전트 재검토: evidence.md의 재현 명령으로 판정을 독립 확인하고 claude-opinion.md에 반론/동의를 append.
- Muse: 드럼 게시물 영상2(10.11s) 미분석, #39 프롬프트 미확보.
- Grok: 카드 생성기의 "Soft" 토큰 누출 원인 수정(box 원본도 오염 — 재복사 시 정리본을 덮어씀).
- 채택 권고(opinion §3)는 사용자 결정 후 별도 태스크.
