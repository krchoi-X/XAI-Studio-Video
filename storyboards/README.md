# Storyboard Collection / 콘티 모음

이 폴더는 `scenarios/`의 특정 각본 개정본에서 파생된 **Hermes 프로덕션 콘티 개정본**을 보관한다. 작가 원본, 모델별 프롬프트, 렌더 결과를 이 폴더에 섞지 않는다.

## 저장 구조

```text
scenarios/
  RW-001-rewind.md              # 기존 무접미 파일은 revision 1
  RW-001-rewind.r002.md         # 수정된 작가 각본은 새 파일

storyboards/
  RW-001/
    storyboard-r001.md          # Hermes 콘티 revision 1
    storyboard-r001.preflight.json # deterministic coverage/preflight sidecar
    storyboard-r002.md          # 같은 콘티 계보의 수정본
```

- 시나리오 revision과 콘티 revision은 독립적이다.
- 어떤 시나리오가 수정돼도 이전 콘티를 덮어쓰지 않는다.
- 어떤 콘티가 수정돼도 작가 시나리오를 덮어쓰지 않는다.
- 새 시나리오 개정본에서 콘티를 다시 시작할 때는 새 `storyboard_id`와 `storyboard-r001.md`를 만든다.
- 같은 콘티를 수정할 때는 `storyboard_id`를 유지하고 revision을 올리며 부모 콘티 경로·revision·SHA-256을 기록한다.

## 필수 결합 정보

모든 콘티는 `templates/external-screenplay-storyboard.md` 형식의 YAML frontmatter로 다음을 고정한다.

- 콘티 ID, revision, 상태
- 원본 시나리오 ID, revision, 저장소 상대 경로, SHA-256
- 이전 콘티 revision의 경로·revision·SHA-256(두 번째 revision부터)
- 실제 작성 주체 `hermes`와 선택 모델

SHA-256은 파일의 원시 바이트가 아니라 정규화된 UTF-8 텍스트를 사용한다. UTF-8 BOM을 제거하고 CRLF/CR을 LF로 바꾼 뒤 계산하므로 Windows와 다른 체크아웃에서도 같은 내용은 같은 해시가 된다. 반드시 아래 명령으로 계산한다.

```powershell
python tools/storyboard_revision.py hash --path scenarios/RW-001-rewind.md
```

검증:

```powershell
python tools/storyboard_revision.py validate `
  --storyboard storyboards/RW-001/storyboard-r001.md `
  --json
```

원본 또는 부모 파일이 결합 이후 바뀌면 검증은 실패한다. 그 파일을 고쳐 맞추지 말고 새 revision을 만든다.

## 콘티 내용 원칙

1. Story Locks와 Staging Proposals를 먼저 분리한다.
2. 사건·인과·정보 공개 시점·결말·대사·금지 요소는 잠금으로 취급한다.
3. 카메라 위치·프레이밍·숏 분할·정보 전달 방식은 잠금 안에서 수정할 수 있다.
4. Hermes 변경은 `legibility`, `cause-shot`, `source-clarification`, `feasibility`, `continuity`, `contradiction-fix`, `scope-coverage` 중 하나로 기록한다.
5. 승인된 콘티만 기존 Intent Contract와 cutboard 단계로 넘긴다.
6. 부분 제작이나 티저는 포함 범위를 명시하고, 범위 밖 비트는 `intentionally_unproduced`로 남긴다.
7. 카메라 설정별 시작 프레임뿐 아니라 reveal·반응 원인·새 요소 출처가 보이는 핵심 정보 순간도 정지 프리뷰로 확인한다.
8. Hermes의 성공 문구나 Markdown의 `pass` 표는 완료 증거가 아니다. `storyboard_pipeline.py`가 실제 파일 변경을 확인하고 preflight sidecar가 `ready: true`일 때만 사용자 검토 단계로 이동한다.
