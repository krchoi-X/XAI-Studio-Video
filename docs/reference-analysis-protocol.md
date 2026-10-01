# 레퍼런스 분석 프로토콜 (Reference Analysis Protocol)

출처: Codex 지시사항 — 사용자가 2026-09-30 전달.
적용 범위: #68 이후 모든 레퍼런스 분석. 방향: 새 항목 수를
늘리는 것보다 기존 taxonomy를 정제하는 것을 우선한다.

## 1. 분석 순서 (고정)

새 레퍼런스를 분석할 때 먼저 기존 T/P 항목으로 설명 가능한지
확인한다. 새 사례에 대해 다음을 먼저 판정한다:

- 기존 항목의 독립 증거를 강화하는가 (strengthen)
- 기존 항목의 범위를 좁히거나 넓히는가 (scope)
- 특정 모델의 capability evidence인가 (model_capability_only)

## 2. 새 T/P 번호 발급 조건 (모두 충족해야 함)

- 기존 항목으로 설명할 수 없고,
- 별도의 제작 문제를 해결하며,
- 관찰 가능한 근거와 재사용 가능한 형태가 있을 때만.

## 3. 증거 표기 분리

각 분석에는 evidence_strength와 cross_model_generality를
분리해 기록한다.

- 사례가 많다고 범용성이 높은 것은 아니다.
- 고전 영화문법은 사례가 적어도 범용성이 높을 수 있다.

## 4. Capability evidence (renderer의 일시적 한계)

영구 규칙으로 만들지 않는다. 다음 형태로 기록한다:

```
model / version / evidence date / task /
observed success or failure / confidence
```

## 5. Promotion summary (각 분석 끝에 붙임)

```yaml
knowledge_update:
  existing_T: [T-..]
  existing_P: [P-..]
  evidence_strength: MEDIUM
  cross_model_generality: HIGH
  promotion_target: DIRECTOR_RECIPE
  action: strengthen_existing
  notes: "..."
```

action 값 (6종):
- strengthen_existing — 기존 항목의 독립 증거 강화
- scope_existing — 기존 항목의 범위 조정 (좁히기/넓히기)
- merge_candidate — 기존 항목과의 병합 검토 대상
- model_capability_only — 특정 모델의 capability evidence로만 기록
- new_candidate — 신규 T/P 후보 (2항 조건 충족 시에만)
- evidence_only — 규칙화 없이 증거로만 보관

## 6. 기존 규칙 (유지)

- 분석 끝마다 핵심 규칙 1개를 Control Level(Hard Lock /
  Soft Guidance / Creative Freedom)과 함께 붙여넣기 카드로
  (2026-09-25 사용자 승인).
- 증거 출처 표기: frame-observed / prompt-derived /
  author-described / text-guide / inference 분리. 추론은
  production rule로 승격 금지.
- 인기를 품질의 증거로 간주하지 않는다.
