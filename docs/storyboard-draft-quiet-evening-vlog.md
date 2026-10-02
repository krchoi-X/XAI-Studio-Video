# Storyboard Draft 0 — 별일 없는 저녁

> 상태: 기획 초안. 아직 사용자 승인·캐스팅·엔진 컴파일·생성을 하지 않았다.
>
> 원격 병합 근거: [레퍼런스 분석 #78–#79](reference-state-analyses.md),
> [연출 기법 DB](directing-technique-db.md), [프롬프트 공예 DB](prompt-craft-db.md).
> #79의 특정 인물·연인 관계·가재 장면을 복제하지 않고, **카메라를 장면 속 존재로
> 두기**, **한 샷에 한 비트**, **생활 소리와 손에 잡히는 행동**, **광고처럼 꾸미지
> 않기**만 일상 브이로그 문법으로 각색했다.

## Director Intent

늦게 귀가한 사람이 편의점 컵라면으로 조용히 하루를 마무리하는 30초 안팎의
세로형 브이로그다. 사건을 만들기보다 피곤함이 작은 안도감으로 바뀌는 순간을
관찰한다. 시청자가 기억할 것은 화려한 연출이 아니라 "나도 저런 날이 있다"는
생활감과 마지막의 짧은 웃음이다.

## Target Medium

- 세로형 소셜 비디오, 9:16
- 목표 길이: 약 28–32초
- 기본 구조: 5개 샷을 각각 독립 생성·검토한 뒤 편집
- 카메라: 휴대폰을 실제 가구 위에 올려 둔 고정 촬영이 중심
- 스타일: 기본 카메라에 가까운 생활 영상, 실내 실용등, 자연스러운 노출 변화
- 캐스팅: 미정. 승인된 캐릭터를 선택하기 전까지 외모·의상 DNA를 쓰지 않는다.

## Director Memory Routing

- 모드: `placed_camera_vlog` (safe lane)
- 선택한 문법: `placed_camera_opening`, `purposeful_action`,
  `continuity_handoff`
- 적용 이유: 촬영 장치를 장면의 일부로 보이고, 말보다 행동을 먼저 두며, 각
  샷의 끝 상태를 다음 샷이 이어받게 하기 위해서다.

## Emotional / Narrative Arc

```text
피곤한 귀가 → 아무것도 하기 싫음 → 간단한 준비에 몰입
→ 첫입의 작은 위로 → 내일을 가볍게 약속하고 하루를 닫음
```

## Beat Sheet

| Beat | 목적 | 진입 상태 | 행동 / 변화 | 종료 상태 | 감정 | 생존 우선순위 |
|---|---|---|---|---|---|---|
| B1 귀가 | 인물과 촬영 방식 확립 | 빈 현관, 카메라 고정 | 인물이 편의점 봉투를 들고 들어와 카메라를 확인하고 "오늘은 진짜 아무것도 안 할래"라고 말함 | 봉투를 든 채 주방 쪽으로 이동 | 지침, 무방비 | HIGH |
| B2 꺼내기 | 저녁의 소박함 제시 | 봉투가 조리대 위 | 컵라면, 젓가락, 캔 음료를 하나씩 꺼내고 주전자 스위치를 누름 | 컵라면 뚜껑이 반쯤 열리고 물이 끓기 시작 | 체념이 루틴으로 바뀜 | HIGH |
| B3 기다리기 | 생활의 시간감을 만듦 | 뜨거운 물을 붓기 직전 | 물을 붓고 뚜껑 위에 젓가락을 올린 뒤 휴대폰 타이머 3:00을 누름 | 김이 얇게 오르고 타이머가 작동 | 잠깐의 멍함 | MEDIUM |
| B4 첫입 | 작은 위로의 정점 | 낮은 테이블에 완성된 컵라면과 캔 | 첫입을 먹고 뜨거워서 짧게 숨을 내쉰 뒤 카메라를 보고 작게 웃음 | 젓가락은 컵 위, 어깨가 조금 풀림 | 안도, 자기풍자 | HIGH |
| B5 마감 | 하루를 닫고 북엔드 완성 | 다 먹은 컵과 빈 캔 | 분리수거통에 정리하고 현관 카메라 앞으로 돌아와 "내일은 제대로 먹을게"라고 말한 뒤 불을 끔 | 빈 현관, 생활 소리만 남음 | 가벼운 회복 | HIGH |

## Narrative Tempo Map

| Beat | tempo role | weight | attention hold | motion density | camera energy | transition pressure | 길이 힌트 |
|---|---|---:|---|---|---|---|---:|
| B1 | establish | HIGH | normal | subtle | very low | soft | 6s |
| B2 | observe | MEDIUM | normal | moderate | very low | neutral | 6s |
| B3 | linger | MEDIUM | extended | subtle | still | soft | 5s |
| B4 | payoff | HIGH | extended | subtle | still | soft | 7s |
| B5 | release | HIGH | normal | subtle | very low | soft | 6s |

## Annotated Shot Plan

### S1 / B1 — 현관에 카메라를 둔다

- **Narrative purpose**: 브이로그의 촬영 방식과 오늘의 피로를 동시에 설명한다.
- **Frame**: 신발장 또는 낮은 선반 위 휴대폰, 현관과 방 안 일부가 함께 보이는
  미디엄 와이드. 화면 앞쪽에 손이 잠깐 들어와 각도를 맞춘 흔적을 허용한다.
- **Action**: 문이 열리고 인물이 들어온다. 신발을 벗고 봉투를 들어 보인 뒤
  짧은 대사를 한다. 큰 표정 연기 없이 숨을 한번 내쉰다.
- **Camera**: 완전한 짐벌 고정이 아니라 가구 위 휴대폰의 미세한 흔들림만.
- **Handoff**: 오른손에 든 편의점 봉투와 주방으로 향하는 방향을 S2가 이어받는다.
- **Audio**: 도어록, 문, 비닐 봉투, 신발 소리. BGM 없음.

### S2 / B2 — 오늘 저녁을 꺼낸다

- **Narrative purpose**: 말보다 소품과 행동으로 "간단히 먹고 쉬는 밤"을 보여준다.
- **Frame**: 조리대 높이의 고정 미디엄. 얼굴과 손, 봉투 안이 모두 읽히되 손
  극클로즈업은 피한다.
- **Action**: 컵라면 → 젓가락 → 캔 음료 순으로 꺼낸다. 주전자 스위치를 한 번
  누르고 컵라면 뚜껑을 반만 연다. 한 샷에서 추가 조리를 시키지 않는다.
- **Camera**: 고정. 인물이 프레임 밖으로 완전히 사라지지 않는다.
- **Handoff**: 반쯤 열린 컵라면, 오른쪽의 캔, 끓기 시작한 주전자를 S3가 그대로
  이어받는다.
- **Audio**: 비닐 바스락, 물 끓는 소리, 스위치 클릭.

### S3 / B3 — 3분을 기다린다

- **Narrative purpose**: 아무 일도 없는 기다림을 생활감으로 바꾼다.
- **Frame**: 컵라면과 손이 중심인 타이트 미디엄. 배경에 인물 상반신이 일부 남아
  관계가 끊기지 않게 한다.
- **Action**: 물을 한 번에 붓고 뚜껑을 닫고 젓가락을 가로로 올린다. 휴대폰
  타이머 3:00을 누른 뒤, 손이 프레임 밖으로 빠지고 1초 정도 그대로 기다린다.
- **Camera**: 고정. 과도한 증기나 매크로 음식 광고 연출 없음.
- **Handoff**: 뚜껑 위 젓가락과 얇은 김이 S4의 완성된 컵라면으로 시간 점프한다.
- **Transition**: 물 끓는 소리를 짧게 유지한 사운드 브리지 후 부드러운 컷.

### S4 / B4 — 첫입이 오늘의 보상이다

- **Narrative purpose**: 피곤함이 작은 안도로 바뀌는 유일한 감정 정점.
- **Frame**: 낮은 테이블 건너편 고정 미디엄. 카메라가 함께 앉아 있는 친구처럼
  느껴지되, 연인 관계를 전제하지 않는다.
- **Action**: 뚜껑을 완전히 열고 첫입을 먹는다. 뜨거워서 짧게 숨을 내쉬고,
  과장하지 않은 채 렌즈를 한번 보고 작게 웃는다.
- **Camera**: 움직이지 않는다. 이 샷은 표정과 어깨가 조금 풀리는 변화를 위해
  다른 샷보다 1초 더 머문다.
- **Handoff**: 컵과 캔의 위치, 오른손의 젓가락, 조금 편안해진 자세를 보존한다.
- **Audio**: 뚜껑, 젓가락, 작은 숨, 방의 냉장고 소리. 대사 없음.

### S5 / B5 — 내일을 핑계로 끝낸다

- **Narrative purpose**: 거창한 결심 없이 하루를 닫고 시작 구도로 돌아간다.
- **Frame**: 첫 샷과 같은 현관 구도. 첫 2초는 분리수거 동작의 결과만 짧게
  보여준 뒤 인물이 카메라 앞으로 돌아온다.
- **Action**: 빈 컵과 캔을 정리하고, 카메라를 집기 전에 "내일은 제대로 먹을게"
  라고 말한다. 본인도 믿지 않는 듯 아주 작게 웃고 불을 끈다.
- **Camera**: 고정. 암전 직전 손이 렌즈 쪽으로 오지만 렌즈를 완전히 가릴 필요는
  없다.
- **Exit state**: 빈 현관, 소품 정리 완료, 실내등 꺼짐.
- **Audio**: 캔 소리, 스위치, 멀리서 들리는 실내 생활 소리. 검은 화면에서 0.5초
  유지 후 종료.

## Prop State Ledger

| 소품 | S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|---|
| 편의점 봉투 1개 | 오른손에 듦 | 조리대 위, 내용물 꺼냄 | 화면 밖 보관 | 화면 밖 | 분리수거 또는 보관 완료 |
| 컵라면 1개 | 봉투 안 | 조리대, 뚜껑 반개방 | 물을 붓고 뚜껑 닫힘 | 테이블, 뚜껑 완전 개방 | 빈 컵, 정리됨 |
| 나무젓가락 1벌 | 봉투 안 | 컵 옆 | 뚜껑 위 가로로 놓임 | 오른손 사용 후 컵 위 | 컵과 함께 정리 |
| 캔 음료 1개 | 봉투 안 | 컵 오른쪽 | 같은 위치 | 테이블 오른쪽 | 빈 캔, 정리됨 |
| 휴대폰 카메라 | 현관 선반 | 주방 고정 카메라 | 타이머 소품과 촬영 카메라는 별도라고 명시 | 테이블 건너편 | 현관 선반, 종료 시 회수 직전 |

## Reference Roles

- **Character reference**: 추후 캐스팅된 인물의 승인된 정체성·헤어·체형만 담당.
- **Wardrobe reference**: 사용 시 이번 에피소드 의상만 담당. 승인된 캐릭터 DNA와
  충돌하지 않게 별도 검토.
- **Storyboard Spec**: 비트 순서, 프레이밍, 감정 리듬, 소품 상태, 샷 간 인계 담당.
- **Location reference**: 현관·주방·낮은 테이블의 공간 관계만 담당.
- 한 레퍼런스가 모든 역할을 통제한다고 가정하지 않는다.

## Constraints and Creative Freedom

### Hard Locks

- 샷마다 핵심 행동은 하나만 둔다.
- 컵라면은 하나, 캔은 하나, 젓가락은 한 벌로 유지한다.
- 인물 정체성과 의상은 한 에피소드 안에서 바뀌지 않는다.
- S1과 S5의 현관 구도와 카메라 높이는 같은 장소로 읽혀야 한다.
- 소품은 원장의 상태 변화 없이 생성·복제·소실되지 않는다.

### Soft Guidance

- 스마트폰 기본 카메라에 가까운 노출과 생활 조명.
- 대사는 짧고, 먼저 행동한 뒤 말한다.
- 렌즈를 보는 순간은 S1과 S4, S5에만 짧게 둔다.
- 피곤함은 처진 어깨, 느린 호흡, 작은 웃음으로 보이고 과장 연기는 피한다.

### Creative Freedom

- 정확한 집 구조와 소품 브랜드.
- 자연스러운 눈 깜박임과 작은 자세 교정.
- 냉장고·복도·바깥 차량 같은 낮은 레벨의 생활 소리.

## Anti-Commercial Direction

코퍼스 #79의 반(反)글래머 방향을 이 장면에 맞게 적용한다.

- 영화급 얕은 심도, 광고용 음식 광택, 완벽하게 정돈된 쇼룸 주방을 목표로 하지
  않는다.
- 과도한 짐벌 이동, 오빗, 슬로모션, 뮤직비디오식 조명 전환을 쓰지 않는다.
- 먹방식 큰 리액션, 과장된 감탄, 제품 로고 강조를 쓰지 않는다.
- 네거티브는 보편 규칙이 아니라 이 기획에서 피하려는 실패 방향이다. 실제 엔진
  컴파일 때는 관찰된 모델 실패에 맞춰 최소화한다.

## Rough Storyboard Rendering Prompt

```text
A five-panel rough storyboard for a vertical everyday phone vlog.
Panel 1: a tired person enters a small apartment carrying one convenience-store bag,
seen from a phone placed on a shoe cabinet.
Panel 2: fixed kitchen-counter view as the person removes one cup noodle, one pair of
chopsticks and one canned drink, then presses the kettle switch.
Panel 3: warm water is poured into the cup; chopsticks rest across the lid; a 3:00 timer
starts, followed by a quiet one-second wait.
Panel 4: fixed low-table view; the person takes the first bite, exhales because it is hot,
then gives the camera a small unperformed smile.
Panel 5: return to the opening hallway composition after cleanup; the person says goodnight
and switches off the light.
Natural practical lighting, ordinary lived-in apartment, restrained acting, readable prop
continuity, no commercial food styling, no dramatic camera moves. Rough planning quality,
clear panel IDs S1-S5, arrows only for subject movement and continuity handoffs.
```

## Assumptions / Open Creative Decisions

- **가정**: 사용자가 말한 "무난한"을 캐릭터 중립·일상적·저난도·저비용의 의미로
  해석했다.
- 캐릭터, 실제 집의 공간, 의상, 음성 유무는 아직 결정하지 않았다.
- 컵라면이 너무 평범하면 같은 구조를 차·토스트·편의점 디저트로 바꿀 수 있다.
  이 경우에도 비트와 카메라 문법은 유지하고 소품 원장만 갱신한다.
- S3의 물 붓기와 S4의 식사 동작은 손·소품 상호작용 위험이 있어 샘플 단계에서
  먼저 검증할 대상이다.
- 실제 엔진을 정한 뒤 각 샷을 런타임 프롬프트로 따로 컴파일한다. 이 문서는
  런타임 프롬프트가 아니다.

## Review State

- Revision: Draft 0
- Accepted decisions: 없음 (사용자 검토 전)
- Rejected decisions: 판타지 스펙터클, 연인 관계 전제, 다중 인물, 빠른 몽타주
- Review questions: 컵라면 소재가 충분히 자연스러운지, 대사를 더 줄일지, S4의
  렌즈 시선을 유지할지
- 다음 게이트: 사용자 방향 승인 후에만 캐스팅·참조 역할·엔진별 샷 패킷으로 전환
