# Character Architect 도입 검토 — 캐릭터 기획과 정체성 고정의 분리

- 작성: 2026-10-11
- 상태: **제안 / 구현 전 검증 필요**
- 범위: Character DNA, visual identity, wardrobe, behavior, image/video prompt adapters
- 배경: 외부의 장문 'CHARACTER DESIGN ARCHITECT / Keyword-Based Character Creation Master Prompt' 검토
- 원칙: 기존 canonical spec, Hard Lock/Soft Guidance/Creative Freedom, storyboard-first 및 disposable runtime prompt 구조를 **변경하지 않는다**.

## 요약 / 결정

**조건부 도입 권고.** 외부 프롬프트를 통째로 시스템 프롬프트에 추가하지 않는다. 캐릭터 최초 기획을 위한 선택적 `Character Architect` 단계로 핵심 개념만 채택한다. 확정된 Character DNA의 얼굴/신체 동일성을 새로운 기획 설명이나 장면 프롬프트가 자동으로 재설계할 수 없게 한다.

목표가 다르다:
- 외부 방법론: 키워드로 풍부하고 기억에 남는 *새 캐릭터* 만들기.
- Studio: 동일 캐릭터를 이미지·영상·콘티·만화와 여러 렌더러에서 *반복 재현*하기.

## 원문에서 도입할 요소

| 요소 | 채택 이유 | 구체적 통합 |
|---|---|---|
| Keyword Integration | 세계관/직업/성격과 시각 결정의 설득력 | **Design Rationale**에 이유 기록; 매번 실행 프롬프트로 전달하지 않음 |
| Visual Hierarchy (1s/3–5s/close) | 강한 인상과 미세한 생활 디테일 구분 | primary/secondary/tertiary 읽기 수준; 중요도 혼동 방지 |
| Wardrobe DNA | 의상을 매번 고정하지 않고 동일인의 취향 유지 | 취향·선택 규칙은 별도 저장; 현재 착장은 Outfit에만 |
| Humanity Detail | 완벽한 디자인 오브젝트 같은 인상 완화 | 습관·애착 물건·수선 흔적 등 선택적 설정; 모든 장면에 강제하지 않음 |
| Distinctiveness Test | 반복 생성에 앞서 캐릭터의 기억성 점검 | 얼굴/실루엣/색/세계관 기준; 여기에 Identity Invariance Test 추가 |

주의: shape language(원/사각/삼각), silhouette, controlled exaggeration은 **스타일화 캐릭터의 선택적 보조 도구**로만. 실사 인물에는 얼굴의 실제 기하학적 비율과 자연스러움 우선. '직업=특정 체형', '성격=특정 눈매' 식 단정 금지.

## 제안되는 단계와 데이터 경계

```text
User Keywords / World / Role / Personality
            ↓
[Optional] Character Architect (creative exploration)
   ├─ Concept / profile / design rationale
   ├─ visual hierarchy / style cues
   ├─ wardrobe preferences / behavior ideas
   └─ candidate identity design (NOT locked)
            ↓  master image approval / identity review
Character DNA + Master Image(s)  [HARD LOCK]
            ↓
Wardrobe DNA [SOFT]    Behavior DNA [SOFT]
            ↓                 ↓
Scene + Outfit + Blocking + Expression [PER-SHOT]
            ↓
Canonical Storyboard / Master Spec
            ↓
Model-specific Adapter (Krea / Flux / NAI / video ...)
            ↓
Disposable Runtime Prompt
```

### 구분된 소유권

- **Character Concept**: 인물의 동기·성격·세계관. 외모 설계의 배경이지 이미지 렌더링 명령 자체는 아님.
- **Character DNA**: 확정된 얼굴/신체 비율, 인식 가능한 고유 특성, 불변 식별 정보. 명시적 재승인 없이 변경 불가.
- **Master Images / references**: 정면·사선·측면 등 확인된 시각적 기준. 텍스트 DNA만으로 픽셀 수준의 얼굴 동일성 보장 불가.
- **Wardrobe DNA**: 선호색·소재·실루엣·착장 선택 규칙. 실제 의상명·색·질감은 **Outfit**의 소유. 포즈/조명/카메라에 복장 정보 중복 기입 금지.
- **Behavior DNA**: 표정 폭·제스처·자세의 습관. 샷의 요구가 우선하며 신체 구조를 변경하지 않음.
- **Scene / Shot**: 현재 위치·환경·빛·감정·행동·구도·장면용 착장.
- **Renderer Adapter**: 모델별 인식 가능한 표현(예: NAI 태그형, Krea/Flux 관찰 가능 묘사, 영상의 동작 순서·방향·지속시간·시작·종료). 캐릭터 재설계 권한 없음.

## 외부 프롬프트를 그대로 통합하면 생기는 위험

1. 24개 섹션을 19개 출력으로 강제하면 장문·반복·일반화가 증가하고 모델별 맥락 예산을 차지함.
2. '성격을 얼굴로 표현', '직업을 체형에 표현'은 장면마다 얼굴 기하학이나 신체 비율이 흔들리는 원인이 될 수 있음.
3. 시그니처 의상·액세서리·배경/조명을 DNA에 결합하면 복장·헤어·장소 변경을 막음.
4. 하나의 FINAL IMAGE GENERATION PROMPT에 컨셉/의상/포즈/조명 전부를 합치면 기존에 관찰된 블록 간 의상 정보 오염을 재현함.
5. 실사 캐릭터는 검은 실루엣보다 **헤어/복장이 바뀌어도 같은 얼굴인가**가 더 중요한 경우가 많음.
6. 원문의 도형 비율(예: square 65% + circle 35%)과 절대적 디자인 수치에는 검증 근거가 없으므로 의미적 휴리스틱으로 취급.
7. 동일성 보장의 기술 수준을 과장하지 않는다. 텍스트 DNA, 참조 이미지, LoRA 등은 렌더러에 따라 성능이 달라지는 수단임.

## 신규 검증: Identity Invariance Test

확정된 master identity를 기준으로 다음 교차 테스트를 권고한다.

| 테스트 축 | 최소 비교 |
|---|---|
| 시점 | 정면 / 3·4뷰 / 좌우 측면 |
| 표정 | neutral / smile / serious / unguarded |
| 외형 가변 요소 | 머리 묶음/풀림, 앞머리 변경, 완전히 다른 의상 |
| 장면 | 스튜디오 / 자연광 실내 / 야외 |
| 모델 | 가능하면 Krea 기준 후 Flux/다른 모델 중 하나 |

**검수 기준**: 얼굴 골격·눈 간격·눈의 형태·코·입·턱·광대의 관계, 체형 비율의 유지 여부를 사람이 시각 검수한다. 의상/표정/빛이 같다는 이유로 동일 인물 점수를 높이지 않는다. 참조 이미지에서 포즈·구도까지 복제되는 과적합도 별도 결함으로 기록한다.

정량 face embedding 점수는 사용 가능하더라도 보조지표일 뿐이며, threshold는 실제 테스트로 보정한다. 실패 컷은 단순히 프롬프트를 길게 만들기보다 원인(참조/모델/adapter/pose/lighting/overconstraint)을 분류한다.

## 마이그레이션 및 적용 규칙

- 기존 레이카/마야/미라 등 **확정 캐릭터의 Character DNA를 자동 수정하지 않는다**.
- 신규 캐릭터에만 Character Architect를 실험적으로 시작한다.
- 결과는 우선 *candidate design + design rationale*로 보관하고, 승인된 마스터 이미지 이후에만 DNA를 승격한다.
- 의상 취향(Wardrobe DNA)과 실제 착장(Outfit)을 분리하며, 헤어스타일 역시 정체성 자체가 아니라 교체 가능한 상태로 관리하되 고유한 두상/헤어라인 등은 보존한다.
- 성격은 행동/표정의 **선택 가능한 경향**으로 남기고 표정 고정 명령으로 쓰지 않는다.
- 엔진별 프롬프트를 표준 DNA 저장소로 역수입하지 않는다.
- Studio의 기존 canonical-spec / storyboard / adapters 설계를 유지한다.

## Codex / Claude / Hermes 검토 과제 (우선순위)

1. **P1 문서 통합**: 기존 Character DNA 및 reference-driven production 문서와 연결 가능한 파일/필드를 찾고, 새 스키마를 무리하게 늘리지 않는 최소 패치안 작성.
2. **P1 컴파일 경계**: Character DNA ↔ Wardrobe DNA ↔ Outfit ↔ Pose ↔ Lighting 간 소유권 및 중복 검증 규칙 제안.
3. **P1 회귀 테스트**: 레이카 또는 마야 master 기준으로 착장·헤어·표정·시점 변화 테스트; identity drift와 wardrobe leakage 기록.
4. **P2 새 캐릭터 파일럿**: Character Architect 사용/미사용으로 최초 컨셉의 차별성 및 재현성 비교.
5. **P2 어댑터 실험**: NAI 태그/Krea·Flux 묘사/영상 motion grammar가 각각 적합한지 모델별 작은 검증 세트 확보.
6. **P3 승격 결정**: 반복 재현성과 수정 용이성의 개선이 확인된 규칙만 공식 스킬/템플릿으로 승격.

## 판단 상태

**추천: '선택적 프런트엔드 기획 단계' 채택.** 기존 불변 DNA와 모델별 어댑터를 교체하지 않는다. 장기적으로 단일 장문 프롬프트가 아니라 단계적 창작 → 승인 → 고정 → 장면별 조합 → 모델별 컴파일의 경계를 강화하는 방향이 유리하다.

근거 성격: [원리] 책임 분리·불변 조건 보존, [경험] 기존 Studio의 얼굴/복장/장면 오염 사례, [추론] Character Architect의 효과(실제 A/B 검증 전).
