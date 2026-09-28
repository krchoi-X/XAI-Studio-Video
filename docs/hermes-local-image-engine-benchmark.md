# Hermes 로컬 이미지 엔진 비교 시험

- 작성일: 2026-09-28
- 상태: 실행 전 시험 규격. 이 문서 자체는 생성 명령이 아니다.
- 실행자: Hermes
- 대상 엔진: Z-Image, Krea2, Qwen Image 2.1
- 목적: Codex·Claude·Grok의 생성 크레딧을 사용하지 않고, Studio에서 캐릭터 의상·자세 배치를 맡길 로컬 엔진의 용도별 적합성을 확인한다.

## 1. 시험에서 결정할 것

한 모델을 모든 작업의 승자로 정하지 않는다. 아래 역할별로 결과를 낸다.

1. **텍스트 지시 이행:** 의상, 자세, 구도, 인원 수를 가장 정확하게 따르는 엔진
2. **얼굴 마스터 유지:** 의상과 자세가 바뀌어도 같은 사람으로 보이는 엔진
3. **인체와 사진 품질:** 손·발·관절·천·피부·배경이 자연스러운 엔진
4. **탐색 효율:** 속도와 실패율이 좋아 많은 후보를 만들기 적합한 엔진
5. **성인 프롬프트 이행:** 명시적으로 승인된 성인 캐릭터 시험에서 불필요한 대체 의상이나 가림을 만들지 않는 엔진

최종 결론은 예를 들어 `얼굴 유지=Qwen`, `빠른 탐색=Z-Image`, `특정 편집=Krea2`처럼 역할별일 수 있다.

## 2. 역할 분리

| 역할 | 책임 |
|---|---|
| 사용자 | 시험 캐릭터와 얼굴 마스터 확정, 결과 육안 검토, 최종 선호 결정 |
| Hermes | 계획 파일 작성, GPU 사전 점검, 순차 생성, 상태·실패·경로 기록, Studio 동기화 |
| Codex·Claude·Grok | 시험 규격·프롬프트·코드 개선과 결과 분석. 개별 이미지 생성 반복에는 사용하지 않음 |
| WanGP | 실제 로컬 모델 실행 |
| Studio | 후보 열람, 비교, 채택/탈락 및 이유 기록 |

Hermes가 작성한 계획은 `strict_translation`으로 컴파일한다. 외부 LLM을 프롬프트마다 호출하지 않는다. 실제 요청자는 Hermes이면 `actor/requested_by=hermes`로 기록한다. Studio에서 사용자가 직접 만든 배치는 향후 requester와 executor를 분리하는 계약 수정 후 `requested_by=web`, executor=Hermes로 기록한다.

## 3. 공통 원칙

- 캐릭터의 canonical Stable DNA를 수정하지 않는다. 의상·자세·표정·장소는 모두 Scene Delta다.
- 캐릭터 기록에 명시된 성인 여부를 먼저 확인한다. 외모만 보고 성인으로 추정하지 않는다.
- 얼굴 마스터는 사람이 선택해 `reference_defaults.identity`로 기록된 이미지만 `character-default`로 사용한다.
- 이미지가 생성돼도 자동으로 얼굴 마스터, 승인 레퍼런스 또는 캐릭터 DNA가 되지 않는다. 모든 결과는 `needs_review`로 시작한다.
- 한 번에 WanGP 작업 하나만 실행한다. 실행 중인 다른 배치나 렌더를 중지하거나 빼앗지 않는다.
- 엔진 실패 시 다른 엔진 결과로 대체하지 않는다. 해당 엔진의 실패로 기록한다.
- 프롬프트, constraints, seed, 모델 설정, 참조 경로·해시, 실행 시간과 산출물 경로를 보존한다.
- 생성 완료, Studio 동기화, 사람 검토와 최종 채택은 서로 다른 상태다.

## 4. 전체 시험 규모

### 1차 — 텍스트 생성 비교

- 6개 장면 × 3개 엔진 × 1장 = **18장**
- 얼굴 이미지를 전달하지 않는다.
- Stable DNA 텍스트와 동일한 Scene Delta만으로 모델의 기본 표현력과 지시 이행을 비교한다.
- 엔진: `z-image`, `krea2`, `qwen21`

### 2차 — 얼굴 마스터 유지 비교

- 6개 장면 × 2개 엔진 × 1장 = **12장**
- 얼굴 측정용 상반신 장면 2개 × 2개 엔진 × 1장 = **4장**
- 같은 얼굴 마스터를 해시 고정 입력으로 전달한다.
- 엔진: Krea2 Identity Edit, Qwen Image 2.1 reference mode
- Z-Image는 현재 Character Manager에서 얼굴 마스터를 직접 받는 reference engine이 아니므로 이 비교에서 제외한다.

### 기본 시험 합계

캐릭터 한 명의 기본 시험은 총 **34장**이다. 1차 결과를 먼저 검토하고 명백한 파이프라인 오류가 없을 때 2차를 실행한다. 처음부터 80~100장을 만들지 않는다.

### 후속 반복성 시험

각 역할의 상위 엔진에 대해서만 대표 장면 2개를 고르고 seed 3개로 반복한다. 최대 `2장면 × 3seed × 선택 엔진 수`다. 첫 결과가 나쁜 장면을 무작정 여러 번 재생성하지 않는다.

## 5. 고정 변수와 허용 변수

### 모든 엔진에서 고정

- 캐릭터와 Stable DNA 버전/해시
- 영문 요청문 원문
- `strict_translation`
- `coverage`와 `wardrobe` HARD constraints
- 장면의 인원 수, 의상, 자세, 장소, 카메라 거리와 방향
- 세로 전신 비율을 목표로 하는 동일한 의미의 해상도/종횡비
- 장면당 출력 수 1
- 같은 장면 ID와 평가 항목

### 엔진 고유값으로 기록하되 억지로 같게 만들지 않음

- checkpoint/model type
- inference steps, CFG/guidance, sampler와 scheduler
- reference mode 문법
- 엔진이 요구하는 내부 해상도

서로 다른 모델에 같은 steps나 CFG를 강요하면 각 모델의 정상 설정을 비교하지 못한다. 각 엔진의 현재 검증된 Studio 기본값을 사용하고 실제값을 기록한다.

### Seed 해석

모든 장면에 같은 정수 seed를 기록해 재현성을 높이되, 서로 다른 모델에서 같은 seed가 같은 구도나 노이즈를 뜻한다고 해석하지 않는다. Seed 비교는 한 엔진 안에서만 유효하다.

기본 seed 제안: `20260928`. 후속 반복성 시험: `20260928`, `20260929`, `20260930`.

## 6. 공통 시험 장면

아래 문장은 모델 중립 원문이다. 실제 캐릭터 이름은 `<NAME>`으로 대체한다. Stable DNA의 얼굴·체형·머리 정보를 프롬프트 문장에 새로 창작하지 않는다.

| ID | 축 | HARD constraints | 모델 중립 요청문 |
|---|---|---|---|
| T01 | 평상복·정면 | `coverage=clothed`; `wardrobe=cream cotton T-shirt, straight-leg blue jeans, white low-top sneakers` | `Photoreal live-action full-body photograph of exactly one adult woman <NAME> standing naturally beside a neighborhood cafe window, facing the camera. She wears a cream cotton T-shirt, straight-leg blue jeans, and white low-top sneakers. Head-to-toe framing, soft natural daylight, no jacket, coat, cardigan, text, or other person.` |
| T02 | 드레스·보행 | `coverage=clothed`; `wardrobe=burgundy ankle-length wrap dress, low black heels` | `Photoreal live-action full-body photograph of exactly one adult woman <NAME> walking naturally through a quiet gallery corridor in a burgundy ankle-length wrap dress and low black heels. Three-quarter body orientation with her face clearly visible, realistic indoor light, no coat, shawl, trousers, text, or other person.` |
| T03 | 한복·정적 자세 | `coverage=clothed`; `wardrobe=ivory jeogori, indigo full-length chima, deep navy goreum ribbon, simple white traditional shoes` | `Photoreal live-action full-body photograph of exactly one adult woman <NAME> standing in a quiet hanok courtyard. She wears an ivory jeogori, indigo full-length chima, deep navy goreum ribbon, and simple white traditional shoes. Respectful natural styling, head-to-toe, no Western jacket, invented layer, text, or other person.` |
| T04 | 운동복·동작 | `coverage=clothed`; `wardrobe=white tennis polo, cobalt pleated tennis skirt with integrated shorts, white tennis shoes, white visor` | `Photoreal live-action full-body photograph of exactly one adult woman <NAME> on a tennis court preparing to return a ball. She wears a white tennis polo, cobalt pleated tennis skirt with integrated shorts, white tennis shoes, and a white visor. One clear athletic action, both hands and both feet visible, no jacket, text, or other person.` |
| T05 | 수영복·전신 | `coverage=clothed`; `wardrobe=charcoal athletic racerback one-piece swimsuit, barefoot` | `Photoreal live-action full-body photograph of exactly one adult woman <NAME> standing at the edge of a quiet indoor pool in a charcoal athletic racerback one-piece swimsuit, barefoot. Neutral catalog pose, head-to-toe, realistic pool lighting, no towel, robe, cover-up, text, or other person.` |
| T06 | 앉은 자세·45도 | `coverage=clothed`; `wardrobe=sage-green linen shirt, black ankle-length trousers, brown loafers` | `Photoreal live-action full-body photograph of exactly one adult woman <NAME> seated naturally on a simple wooden chair with her head and shoulders turned about 45 degrees to her left. She wears a sage-green linen shirt, black ankle-length trousers, and brown loafers. Both hands and both feet visible, plain studio background, no extra layer, text, or other person.` |

T05는 명시적으로 성인인 캐릭터만 사용한다. 일반 의상 시험과 분리된 무검열 확인이 필요하면 아래 11절의 선택 시험을 사용한다.

## 7. 1차 계획 — 텍스트 생성 비교

각 장면을 엔진별 독립 item으로 만들어 동일한 seed를 명시한다. 총 18 items이며 각 item의 `engines`에는 엔진 하나만 넣는다. 이렇게 하면 실패와 실행 시간이 엔진별로 분리되어 기록된다.

예시:

```json
{
  "schema_version": 1,
  "title": "<NAME> local engine benchmark phase 1 text-only",
  "source_request": "Compare Z-Image, Krea2 and Qwen Image 2.1 with the frozen six-scene wardrobe and pose benchmark. Hermes executes locally; all results require human review.",
  "items": [
    {
      "character_id": "<CHARACTER_ID>",
      "prompt": "<T01 exact prompt>",
      "engines": ["z-image"],
      "count": 1,
      "seed": 20260928,
      "prompt_strategy": "strict_translation",
      "immutable_constraints": {
        "coverage": "clothed",
        "wardrobe": "cream cotton T-shirt, straight-leg blue jeans, white low-top sneakers"
      },
      "scene_spec": {
        "pose": "natural standing pose facing the camera",
        "camera": "full-body head-to-toe vertical photograph"
      },
      "variation_axes": {
        "benchmark_phase": "text-only",
        "scene_id": "T01",
        "engine": "z-image"
      }
    }
  ]
}
```

같은 T01 item을 `krea2`, `qwen21`로 복제하고, T02–T06도 동일하게 확장한다. 프롬프트나 constraints는 엔진에 따라 고치지 않는다. 엔진 특화 문법은 adapter가 담당한다.

## 8. 2차 계획 — 얼굴 마스터 유지 비교

### 사전 조건

- 캐릭터에 사용자가 선택한 `reference_defaults.identity`가 있어야 한다.
- 참조 파일이 존재하고 준비 시점과 제출 시점의 SHA-256/크기가 일치해야 한다.
- 같은 얼굴 마스터를 Krea2와 Qwen 모두에 사용한다.
- 얼굴 마스터의 기존 의상은 테스트 의상보다 우선하지 않는다. 요청문과 HARD wardrobe constraints가 변경 의상이다.

각 장면을 Krea2와 Qwen item으로 따로 만든다. T01–T06 12 items와 아래 얼굴 측정용 I01–I02 4 items를 합쳐 총 16 items이다.

### 얼굴 측정용 보정 장면

1차 실제 시험에서는 전신 이미지의 검출 얼굴이 49–96 px에 그쳐 150 px 최소 기준을 만족하지 못했다. 2차 정체성 시험은 전신 장면의 육안 평가만으로 끝내지 않고 아래 두 장면을 추가한다.

| ID | 목적 | HARD constraints | 모델 중립 요청문 |
|---|---|---|---|
| I01 | 정면 얼굴 재구성 | `coverage=clothed`; `wardrobe=plain black crew-neck top` | `Head-and-shoulders studio photograph of the same adult woman shown in the provided identity reference image, facing the camera with a neutral expression. Preserve her facial identity, facial proportions, skin features and hair. She wears a plain black crew-neck top. Plain light-grey background, soft even light, no jewelry, text or other person.` |
| I02 | 45도 얼굴 유지 | `coverage=clothed`; `wardrobe=plain black crew-neck top` | `Head-and-shoulders studio photograph of the same adult woman shown in the provided identity reference image, with her head turned about 45 degrees to her left and both eyes visible. Preserve her facial identity, facial proportions, skin features and hair. She wears a plain black crew-neck top. Plain light-grey background, soft even light, no jewelry, text or other person.` |

I01–I02 결과의 검출 얼굴이 실제로 150 px 이상인지 확인한다. 기준보다 작으면 자동 유사도 결과를 사용하지 않고 측정 불가로 기록한다.

Krea2 예시:

```json
{
  "character_id": "<CHARACTER_ID>",
  "prompt": "<T01 exact prompt>",
  "engines": ["krea2"],
  "count": 1,
  "seed": 20260928,
  "prompt_strategy": "strict_translation",
  "identity_reference": "character-default",
  "immutable_constraints": {
    "coverage": "clothed",
    "wardrobe": "cream cotton T-shirt, straight-leg blue jeans, white low-top sneakers"
  },
  "scene_spec": {
    "pose": "natural standing pose facing the camera",
    "camera": "full-body head-to-toe vertical photograph"
  },
  "variation_axes": {
    "benchmark_phase": "identity-locked",
    "scene_id": "T01",
    "engine": "krea2"
  }
}
```

Qwen item은 `engines`만 `["qwen21"]`로 바꾼다. 의상 사진 자체의 재현 능력을 별도로 시험할 때만 Qwen item에 `additional_references: [{"role":"wardrobe","path":"<PATH>"}]`를 추가하며, 기본 30장 시험에는 추가하지 않는다.

준비된 설정에서 반드시 확인한다.

| 엔진 | 필수 확인 |
|---|---|
| Krea2 | `model_type=krea2_turbo_edit`, 얼굴 마스터가 `image_refs`에 있음, `_xai.reference_sha256s` 존재 |
| Qwen | `model_type=qwen_image_21_uncensored_q4_k_m`, `video_prompt_type=I`, 얼굴 마스터가 `image_refs` 첫 항목, `_xai.reference_sha256s` 존재 |

어느 엔진도 얼굴 참조가 빠졌을 때 텍스트 생성으로 계속 진행하면 안 된다.

## 9. Hermes 실행 절차

### 9.1 계획 작성

1. canonical character record와 Stable DNA 해시를 확인한다.
2. 1차 계획의 18 items를 작성한다.
3. 원문·constraints·scene ID·engine label이 표와 일치하는지 검사한다.
4. 계획의 예상 이미지 수가 18인지 계산한다.

### 9.2 GPU 사전 점검

```powershell
cd D:\codex\XAI-studio
D:\AI\WanGP\env_uv\Scripts\python.exe -m control_tower --check
D:\AI\WanGP\env_uv\Scripts\python.exe tools\local_wangp.py doctor --wangp-root D:\AI\WanGP
```

필수 조건:

- 다른 생성 job의 `active=0`, `running=0`
- WanGP doctor `ok=true`
- Hermes의 로컬 27B 모델이 유의미한 VRAM을 계속 점유하지 않음

Hermes 런타임을 안전하게 내릴 수 없거나 다른 프로세스가 GPU를 사용하면 기다리거나 명확히 실패한다. 알 수 없는 프로세스를 강제 종료하지 않는다.

### 9.3 큐 등록

```powershell
D:\AI\WanGP\env_uv\Scripts\python.exe tools\hermes_night_batch.py create `
  --plan-file "<ABSOLUTE_PHASE_1_PLAN_JSON>"
```

반환된 batch ID와 `D:\AI_Studio\workspace\hermes-night-batches\<BATCH_ID>\status.json`을 기록한다. 등록됐다는 사실을 완료로 보고하지 않는다.

### 9.4 완료 확인

- night-batch `status.json`이 `completed` 또는 `completed_with_errors`
- 각 성공 item의 session `batch.yaml` job이 `completed`
- 각 run `run.json`이 `needs_review`이고 artifact가 실제로 존재
- 기대한 engine 디렉터리와 model type이 일치
- 성공 세션이 Studio에 동기화됐는지 별도로 확인
- 실패 item은 원인과 재시도 여부를 남기고 결과 수를 부풀리지 않음

1차 결과의 파이프라인 이상 여부를 확인한 뒤 같은 방법으로 2차 12-item 계획을 실행한다.

## 10. 사람 검토표

각 이미지를 1–5점으로 평가한다. 비교 화면에서는 가능하면 엔진 이름을 먼저 숨기고 이미지 자체를 고른 뒤 엔진을 공개한다.

### 1차 텍스트 생성 점수

| 항목 | 가중치 | 질문 |
|---|---:|---|
| 의상 준수 | 25 | 지정한 모든 의상과 금지한 추가 레이어를 정확히 지켰는가? |
| 자세·구도 준수 | 20 | 전신, 방향, 동작, 손·발 노출을 지켰는가? |
| 인체 품질 | 20 | 얼굴, 손, 발, 관절과 비율이 자연스러운가? |
| 인물 매력·사진 품질 | 20 | 사용자가 원하는 캐릭터 이미지로 매력적이고 사진다운가? |
| 배경·소품 정확성 | 5 | 장소와 소품이 요청과 일치하는가? |
| 속도·안정성 | 10 | 생성 시간, 실패율, VRAM 부담이 실용적인가? |

### 2차 얼굴 유지 점수

| 항목 | 가중치 | 질문 |
|---|---:|---|
| 사람 육안 정체성 | 35 | 얼굴 마스터와 같은 사람으로 즉시 보이는가? |
| 의상 변경 성공 | 20 | 얼굴 마스터의 옷이 새 의상으로 정확히 바뀌었는가? |
| 각도·자세에서의 정체성 | 15 | 45도·보행·착석·동작에서도 얼굴이 유지되는가? |
| 인체 품질 | 15 | 손·발·관절·체형이 자연스러운가? |
| 사진 품질 | 10 | 조명, 피부, 천과 배경의 완성도가 높은가? |
| 속도·안정성 | 5 | 생성 시간과 실패율이 실용적인가? |

ArcFace/SFace 같은 자동 유사도는 보조 증거다. 정면용 수치를 측면·프로필에 그대로 적용하지 않는다. 최종 정체성 판단은 사용자의 육안 검토가 우선한다.

### 즉시 탈락 사유

- 다른 인물 또는 여러 사람 생성
- 얼굴 참조가 필요한 시험에서 reference가 실제로 전달되지 않음
- 핵심 의상 종류가 다르거나 얼굴 마스터의 옷이 남음
- 심한 손·발·관절 오류
- 요청한 전신/자세를 평가할 수 없는 구도
- artifact 누락 또는 기록과 실제 파일 불일치

## 11. 선택 시험 — 성인 프롬프트 이행

기본 30장 결과와 섞지 않는다. 사용자가 이 시험을 명시적으로 요청하고, canonical record가 성인임을 확인한 캐릭터에만 실행한다.

권장 최소 구성:

- 중립적인 속옷 카탈로그 장면 1개
- 중립적인 누드 스튜디오 레퍼런스 장면 1개
- 3개 엔진 × 장면당 1장 = 6장

목표는 선정성 경쟁이 아니라 다음을 분리해 확인하는 것이다.

- 요청한 coverage를 지키는가
- 임의의 옷·수건·가림·검열 요소를 추가하는가
- 인체 품질이 무너지는가
- 해당 엔진이 실패 또는 대체 결과를 명확히 기록하는가

이 결과 역시 restricted/needs_review 상태를 유지하며 자동으로 공개·승인하지 않는다.

## 12. 결과 기록 형식

시험 보고서에는 최소한 다음을 기록한다.

```json
{
  "benchmark_id": "BENCH-<date>-<character>",
  "character_id": "<CHARACTER_ID>",
  "stable_dna_sha256": "<HASH>",
  "identity_reference": {
    "path": "<PATH_OR_NULL>",
    "sha256": "<HASH_OR_NULL>"
  },
  "phases": ["text-only", "identity-locked"],
  "scene_ids": ["T01", "T02", "T03", "T04", "T05", "T06", "I01", "I02"],
  "engines": ["z-image", "krea2", "qwen21"],
  "batch_ids": [],
  "expected_images": 34,
  "actual_images": 0,
  "failures": [],
  "human_review_status": "pending",
  "role_decisions": {
    "text_adherence": null,
    "identity_preservation": null,
    "anatomy_quality": null,
    "exploration_speed": null,
    "adult_prompt_compliance": null
  }
}
```

각 후보 행에는 `phase`, `scene_id`, `engine`, `model_type`, `seed`, `session_dir`, `run_dir`, `artifact_path`, `elapsed_seconds`, 점수, 탈락 사유와 자유 의견을 둔다.

## 13. 판정과 다음 단계

1. 장면별 육안 선택을 먼저 완료한다.
2. 가중 점수, 실패율, 평균 생성 시간을 계산한다.
3. 하나의 종합 순위와 함께 역할별 승자를 기록한다.
4. 동점이거나 seed 민감성이 의심될 때만 후속 3-seed 시험을 실행한다.
5. 선택된 모델과 설정을 Studio 기본값으로 만들기 전 사용자 승인을 받는다.
6. 이후 wardrobe pattern pack은 승자 모델과 `exploration`/`identity-locked` 모드를 선택하는 Studio 배치 프리셋 후보가 된다.

시험 결과만으로 canonical DNA, 얼굴 마스터, 승인 reference 또는 기존 채택 이미지를 바꾸지 않는다.

## 14. 1차 실제 실행 기록 — 2026-09-29

- Batch: `NIGHT-20260929-031004-8c0d6e`
- 범위: Lee Suan과 Mizuki Reika, 각각 T01–T06 × 3 engines
- 결과: 36/36 completed, 모든 run은 `needs_review`, identity reference 없음
- 보고서: `D:\AI_Studio\reports\benchmark-20260929-phase1\README.md`
- 비교 시트: 같은 폴더의 `ch-mizuki-reika-full.jpg`, `ch-mizuki-reika-faces.jpg`, `ch-lee-suan-full.jpg`, `ch-lee-suan-faces.jpg`

관찰:

- Qwen21은 T06의 약 45도 회전 지시를 두 캐릭터에서 가장 분명히 따랐다. T04 테니스 동작은 Lee Suan에서만 라켓과 동작을 모두 충족해, 모든 캐릭터에 대해 검증된 규칙으로 일반화하지 않는다.
- Z-Image가 가장 빨랐고, Krea2, Qwen21 순이었다. 기록된 평균은 약 60초, 91초, 174초다.
- Krea2 Reika T03 한복 결과 한 장이 `coverage=clothed`를 위반했다. 동일 장면의 다른 엔진과 Lee Suan Krea2는 정상이라 단일 candidate failure로 피드백에 기록했다. Krea2 공통 규칙 변경 전 같은 T03을 2–3 seeds로 재현 확인한다.
- 전신 이미지의 얼굴은 자동 정체성 측정에 너무 작았다. 이 관찰 때문에 2차에 I01–I02 보정 장면을 추가했다.
- Reika만 사용자 선택 얼굴 마스터가 있다. Lee Suan은 `reference_defaults.identity`가 없으므로 사람이 얼굴 마스터를 선택하기 전에는 2차 identity-locked 시험 대상이 아니다.

이 기록은 사용자의 육안 점수를 대신하지 않는다. 1차의 최종 선호와 2차 진행 결정은 사람 검토 뒤 확정한다.

## 15. 이번 문서가 하지 않는 것

- 지금 즉시 이미지를 생성하지 않는다.
- 모델을 다운로드·업데이트하지 않는다.
- Krea2, Qwen 또는 Z-Image 중 하나를 미리 기본값으로 정하지 않는다.
- Grok이 수집한 프롬프트 전체를 검증된 엔진 규칙이라고 간주하지 않는다.
- Mira의 일회성 `tmp` runner를 정식 실행기로 채택하지 않는다.
- Studio UI나 데이터베이스를 변경하지 않는다.

## 16. 관련 자료

- `docs/hermes-wardrobe-library-stills-playbook.md`
- `docs/wardrobe-library-patterns/`
- `docs/qwen-image-2.1-codex-acceptance-review.md`
- `docs/artifact-and-review-contract.md`
- `D:\codex\XAI-Studio-Private\shared-skills\character-manager\SKILL.md`
