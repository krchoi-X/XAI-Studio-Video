# "잡아봐" (Catch Me) — 남친셔츠 원테이크 속편

- 전편: 남친셔츠 원테이크 v2 (어깨 너머 "잡아봐" 눈빛으로 끝)
- 길이: 기획 50초 / 5샷 → 실제 Muse 파이프라인 산출 30초 / 3샷
- 날짜: 2026-10-03
- 캐릭터 앵커: `media-generation-boyfriend-shirt-still-0-3dff2f97-6da5-44e0-a962-2d49f0470471.webp` (전편 스틸)

## 스토리

그녀가 도망간다. 잡힐 듯 잡히지 않는다. 남친(카메라)이 쫓아가며 찍는다.
복도 추격 → 소파에서 일어남 → 커튼 뒤 숨는 "척" (햇살 역광 미인샷) →
마주침 → 손으로 렌즈를 가리며 끝.

감정 아크: 장난기 → 설렘 → 수줍음 → 포근함 (인과 순서)

## 하드 제약 (전 프롬프트에 verbatim 복사)

```
Same woman: long wet-look black hair, oversized white button-up shirt.
Boyfriend's POV, handheld phone, vertical 9:16.
Warm indoor lighting. Photorealistic, no slow motion.
```

## 콘티 v2 (renderability 4문항 통과분)

| 샷 | 시간 | 내용 | 판정 |
|----|------|------|------|
| S1 | 0–10s | 복도 추격. 그녀가 뛰어가며 뒤돌아봄. 항상 프레임 안. 카메라 흔들림 | DIRECT (몸 상태 1개, 공간 관계 2개, 중간 상태 없음) |
| S2 | 10–20s | 거실 소파. 앉아있다가 카메라 다가오면 일어남. 소파는 이 씬에만 | DIRECT (앉음→일어남 1개 전이) |
| S3 | 20–30s | 창가 커튼. 숨는 "척" — 일부러 보이게. 창밖 햇살 역광 미인샷 | DIRECT (서있기 1개, 복잡한 가려짐 없음) |
| S4 | 30–40s | 클로즈업. 카메라 정면으로 보며 숨 고르고 웃음. 시선 목표물=렌즈 | DIRECT |
| S5 | 40–50s | 오른손 뻗어 렌즈 가림 (손바닥 렌즈 향함). 어두워지며 끝 | CONSEQUENCE_ONLY |

## 실제 산출 (Muse 파이프라인, 2026-10-03)

- `catchme-full-v1.mp4` (30.1초, 720x1280, a=1): S1 → S4 → S5
- S2, S3 영상은 Muse 도구에서 생성 불가 (integrity_check_failed, 재시도 금지)
- S3 커튼 역광 스틸은 정상 산출 → 썸네일/레퍼런스용으로 보관

## 알려진 이슈 + 로컬 파이프라인 수정안

1. **S1 복도가 저택처럼 길다** (사용자 QC, 2026-10-03)
   → S1 스틸/비디오 프롬프트에 추가: `short ordinary apartment hallway, modest and narrow, not a grand mansion corridor`
2. S2, S3는 로컬 파이프라인에서 시도 (Muse에서는 불가)
3. S2 소파는 해당 씬에만 등장 → 씬 내 일관성만 맞추면 됨

## 프롬프트 (영어, 로컬 파이프라인용)

### 캐릭터 앵커
전편 스틸을 kind:image / image prompt로 전 샷에 참조.

### S1 — 복도 추격 (스틸)
```
Vertical smartphone photo, boyfriend's POV: the same young woman from the
reference image (long wet-look black hair, oversized white button-up shirt)
running away down a short ordinary apartment hallway, modest and narrow,
not a grand mansion corridor, glancing back over her shoulder at the camera
with a playful teasing smile, mid-stride, clearly visible in frame.
Warm tungsten indoor lighting, intimate domestic atmosphere,
photorealistic, phone-camera feel.
```
### S1 — 복도 추격 (비디오)
```
Animate this exact still photo. Boyfriend's POV chasing her: she runs down
the hallway away from the camera, glancing back over her shoulder with a
playful teasing smile, staying clearly visible in frame the whole time —
never running far. The camera follows her with handheld shake, like a
boyfriend chasing while filming. Warm tungsten indoor lighting constant.
Photorealistic, no slow motion.
```

### S2 — 소파 (스틸)
```
Vertical smartphone photo, boyfriend's POV: the same young woman from the
reference image (long wet-look black hair, oversized white button-up shirt)
sitting on a sofa in a warmly lit living room, looking at the camera with a
playful smile, about to stand up, a cushion beside her.
Warm tungsten indoor lighting, photorealistic, phone-camera feel.
```
### S2 — 소파 (비디오)
```
Animate this exact still photo. Boyfriend's POV: she is on the sofa smiling
playfully at the camera; as the camera approaches with slight handheld
shake, she begins to stand up from the sofa, laughing softly, ready to run
again. Warm indoor lighting constant. Photorealistic, no slow motion.
```

### S3 — 커튼 (스틸)
```
Vertical smartphone photo, boyfriend's POV: the same young woman from the
reference image (long wet-look black hair, oversized white button-up shirt)
standing beside a window curtain, partially veiled by the sheer curtain,
beautifully backlit by warm sunlight streaming through the window, glowing
hair, gentle teasing smile toward the camera.
Warm indoor lighting, photorealistic, phone-camera feel.
```
### S3 — 커튼 (비디오)
```
Animate this exact still photo. She stands half-veiled by the sheer window
curtain, beautifully backlit by warm sunlight streaming through the window,
smiling teasingly at the camera, curtain swaying very gently. The camera
slowly approaches with slight handheld shake. Warm glowing light constant.
Photorealistic, no slow motion.
```

### S4 — 마주침 (스틸)
```
Vertical smartphone photo, boyfriend's POV, close-up: the same young woman's
face from the reference image (long wet-look black hair), looking directly
into the lens, softly smiling, slightly catching her breath, warm light on
her face. Intimate, photorealistic, phone-camera feel.
```
### S4 — 마주침 (비디오)
```
Animate this exact still photo. Close-up, boyfriend's POV: she looks
directly into the lens, softly smiling, slightly catching her breath after
running, warm light on her face, a few strands of wet hair moving gently.
Camera fixed with slight handheld shake. Photorealistic, intimate,
no slow motion.
```

### S5 — 가림 (스틸)
```
Vertical smartphone photo, boyfriend's POV, extreme close-up: the same young
woman's right hand from the reference image reaching toward the camera, palm
facing the lens about to cover it, her smiling face softly blurred behind
the hand. Warm indoor lighting, photorealistic, phone-camera feel.
```
### S5 — 가림 (비디오)
```
Animate this exact still photo. Her right hand moves toward the lens, palm
facing the camera, gradually covering it until the frame goes almost dark.
Her smiling face stays softly blurred behind the hand. Camera fixed.
Warm indoor lighting. Photorealistic, no slow motion.
```

## 기획 과정에서 얻은 교훈

- S2 초안("소파 뒤에 숨었다가 빼꼼히")은 기획 단계에서 DIRECT로 잘못 태그됨.
  사용자 지적 후 4문항 interrogation 도입: ① 몸 상태 개수 ② 공간 관계 개수
  ③ 모델이 지어내야 할 중간 상태 유무 ④ 같은 비트의 더 쉬운 버전.
  ③이 "있음"이면 DIRECT가 아니다.
- Renderability 태그는 검증 없이 붙이면 장식에 불과하다.
