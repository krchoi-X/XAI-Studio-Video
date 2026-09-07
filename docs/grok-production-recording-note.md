# Grok Bot에게 전달할 안내 — 제작 기록 규칙 (2026-09-07)

작성: Claude Code · 대상: Grok Bot · 저장소: `D:\codex\XAI-studio`

---

## 요약

네가 남긴 `handoff.json`의 메모대로 두 가지가 막혀 있었어. 이제 둘 다 해결됐어.

- `character_scene.py --actor`에 `grok`이 없던 문제 → `grok`, `claude`, `user`가 추가됐어. 더 이상 `codex`로 표기하지 마.
- `local_wangp.py submit`에 요청자 플래그가 없던 문제 → `--requested-by`가 생겼어.

여기에 더해 세션 단위 기록을 남기는 명령을 추가했어. 세션을 한 번 등록해 두면 그 세션의 모든 제출이 요청자를 자동으로 물려받아.

## 지켜야 할 규칙

1. **요청자는 명시적으로만 기록된다.** 아무 데도 없으면 `null`로 남고, 컨트롤타워가 프로세스를 관측해 보완해. 확인하지 않은 값을 임의로 적지 마.
2. **네 가지 사실을 구분해라.** 요청자(`requested_by`, 너), 실행기(`executor`, 로컬 WanGP 워커), 엔진(`engine`, WanGP), 모델(`model`, 체크포인트). 컨트롤타워가 이 넷을 따로 보여줘.
3. **새 파일 규약을 만들지 마.** `session-provenance.json`이 표준 기록이야. 네 `handoff.json`은 그대로 둬도 되고, 도구가 건드리지 않아. 다만 요청자의 기준 파일은 `session-provenance.json`이야.
4. **제작 전에 기록하고, 끝나면 닫아라.** 첫 렌더 전에 세션을 등록하고, 끝나면 같은 명령을 `--status completed`로 다시 실행해.
5. **자신을 다른 에이전트로 표기하지 마.** 특히 `--actor codex`는 쓰지 마.

## 정확한 호출 예시

### 1. 세션 등록 (첫 렌더 전에 한 번)

```bash
python tools/wangp_recorder.py session --session-dir "D:/codex/XAI-studio/characters/ch-lia/02_generations/VIDEO-20260907-181254-lia-sundress-shift-cat" --requested-by grok --engine WanGP --model minimax_h3_ref2va_pruned --character-id ch-lia --title "Lia micro-vlog: sundress to shift to cat" --user-request "<사용자 요청 원문>" --status running
```

`<session>/session-provenance.json`이 생겨. 다시 실행하면 병합되고 `created_at`과 네가 추가한 키는 보존돼.

### 2. 샷 제출 (세션 등록 후에는 플래그 없이도 상속됨)

```bash
python tools/local_wangp.py submit --runs-root "<session>/runs" --prompt-file "<session>/beat-A.txt" --settings-file "<session>/beat-A.settings.json" --project-id "<session-id>" --prompt-id beat-A --output-dir "D:/AI_Studio/library/characters/ch-lia/videos/<session-id>" --requested-by grok
```

세션 밖에서 제출할 때는 `--requested-by grok`을 반드시 붙여. 스크립트 전체에 한 번에 걸려면 환경 변수를 써도 돼.

```bash
export XAI_REQUESTED_BY=grok
```

### 3. 캐릭터 스틸

```bash
python tools/character_scene.py produce --character ch-lia --request "<프롬프트>" --engines krea2 --count 2 --strategy strict_translation --actor grok
```

### 4. 세션 종료

```bash
python tools/wangp_recorder.py session --session-dir "<session>" --status completed
```

## 요청자 결정 순서

```text
--requested-by  →  $XAI_REQUESTED_BY  →  세션 기록  →  null
                                          session-provenance.json
                                          → handoff.json
                                          → batch.yaml session.created_by
                                          → prompt-trace.json invoked_by
```

## 확인 방법

```bash
python tools/local_wangp.py status --run-dir "<run-dir>"
```

컨트롤타워에서도 확인할 수 있어. 태블릿은 `http://100.122.180.40:8790/`, 이 PC는 `http://127.0.0.1:8790/`야. 네 작업은 `requested by grok (from record)`로 표시돼. 기록이 없으면 `(observed: process env marker)`처럼 관측 근거가 붙어.

## 과거 작업

`VIDEO-20260906-233747-lia-intro-10s-trio`와 `VIDEO-20260907-074621-lia-dynamic-motion-trio`는 기록이 남기 전에 끝나서 `D:\AI_Studio\control-tower\attributions.json`에 수동으로 귀속해 뒀어. 소급해서 세션 파일을 고칠 필요는 없어.

## 참고 문서

- [WanGP 기록 규칙](wangp-recorder.md#recording-a-production-session)
- [컨트롤타워 v0.1](control-tower-v0.1.md#requester-attribution-v011-2026-09-07)
- [GROK.md](../GROK.md)
