# Character Lab: 정해원

정해원 포트레이트를 여러 이미지 엔진으로 생성하고 비교하기 위한 파일 기반 실험 장부다. 핵심 단위는 개별 이미지가 아니라 **한 표정·한 구도·한 목적을 가진 하나의 batch experiment**다.

## 구조

```text
character-lab/
├─ README.md
├─ character-dna.md
├─ sources/                         원본 레퍼런스
├─ experiments/
│  └─ BATCH-001-master-portrait-neutral/
│     ├─ batch.yaml                 목적, 공통 조건, 엔진/모델/설정
│     ├─ canonical-prompt.md        모든 엔진이 공유하는 비교 기준
│     ├─ engine-prompts/            실제 엔진별 runtime prompt
│     ├─ outputs/<engine>/          엔진별 원본 생성물
│     ├─ contact-sheets/            엔진별 자동 비교 시트
│     ├─ ratings.csv                이미지별 평가와 선택 여부
│     ├─ notes.md                   배치 결론과 실패 패턴
│     └─ selected/manifest.yaml     survivor의 출처와 선정 이유
├─ candidates/                      여러 배치에서 살아남은 후보
└─ character-sheet/                 최종 승인 세트와 provenance
```

이미지와 영상은 로컬 작업 데이터로 Git에서 제외된다. 프롬프트, 설정, 평가, manifest는 Git으로 추적한다.

## 새 배치 만드는 법

1. `experiments/BATCH-001-master-portrait-neutral/`을 복사하고 다음 번호와 목적을 이름에 쓴다.
2. `batch.yaml`에 만들려는 포트레이트, 고정 조건, 엔진별 모델과 생성 설정을 먼저 기록한다.
3. `canonical-prompt.md`에 공통 비교 프롬프트를 작성한다.
4. `engine-prompts/<engine>.md`에는 실제로 제출한 문장을 그대로 저장한다. 공통 프롬프트 그대로인지, 엔진 최적화판인지도 표시한다.
5. 결과를 `outputs/<engine>/`에 원본 파일명 그대로 넣는다.
6. 저장소 루트에서 다음 명령으로 contact sheet를 만든다.

```powershell
python tools/make_character_contact_sheet.py examples/character-lab/experiments/BATCH-001-master-portrait-neutral
```

7. `ratings.csv`에는 최소한 `identity, realism, eyes, skin_lips, distinctiveness, selected, notes`를 기록한다.
8. 엔진마다 1~2장만 `selected/`에 복사하고 `selected/manifest.yaml`에 원본 경로와 이유를 기록한다.
9. 여러 배치의 survivor는 `candidates/`에서 비교한다. 최종 승인본은 `character-sheet/manifest.yaml`로 batch → engine → prompt/settings까지 역추적할 수 있어야 한다.

점수보다 선택 이유와 실패 이유가 중요하다. 실제 실험이 10~20회 쌓이기 전에는 DB나 UI로 확장하지 않는다.
