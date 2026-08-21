# Example: Summer_Garden_EyeContact_v1

**Status:** reference example / unvalidated cross-model master spec

## Director Intent

An eleven-second midsummer memory rather than a fashion commercial: while filming flowers in a quiet garden, the camera seems to discover an adult woman among the flowers. She notices the camera late, shares a brief quiet gaze with the lens, then the moment passes.

The emotional peak is the silent eye contact near the end.

## Character Priority

**P0 — identity preservation**

The source image is the first frame and primary visual identity reference.

Maintain throughout:
- same adult woman
- same facial geometry and proportions
- same eyes, nose, mouth
- same skin tone
- same hairstyle and hair length
- same wardrobe design, pattern and color
- same body proportions

If visual spectacle conflicts with identity stability, identity wins.

## Duration / Format

- duration: ~11 s
- aspect: 9:16 vertical
- structure: one continuous observational shot
- preferred mode: I2V with first-frame identity reference

## Emotional Shot Graph

```text
DISCOVERY → AWARENESS → SUSPENSION → CONNECTION → RELEASE
```

### S0 / 0–2 s — Discovery

- composition remains close to source image
- foreground orange flowers and green leaves softly blurred
- subject leans slightly among flowers
- she looks at a nearby flower, not the camera
- subject nearly still except for natural breathing
- weak coherent summer breeze moves foreground plants
- minimal handheld breathing

### E1 / 2–5 s — Awareness

- eyes begin to move toward camera first
- face/head follows only slightly
- one natural blink
- camera begins an extremely slow subtle push-in
- no abrupt zoom

### E2 / 5–8 s — Summer air and light

- one gentle warm breeze passes through scene
- flowers and leaves move softly
- only a few long hair strands move across/near face
- clothing reacts minimally
- dappled sunlight changes subtly as leaves move
- soft warm rim/halo on hair edge
- restrained bloom/halation when sunlight meets lens
- mild atmospheric texture suggests warm humid air

### S1 / 8–10 s — Connection / Killing Point

- subject establishes quiet direct eye contact
- holds lens for about one second
- expression suggests she has only just realized she is being filmed
- corners of mouth soften into an almost imperceptible micro-smile
- no deliberate posing
- camera push-in stops
- camera settles
- this is the most beautiful and temporally emphasized frame range

### E3 / 10–11 s — Release

- gaze lowers slightly back toward flowers
- foreground flower drifts partially across frame
- warm sunlight enters lens
- soft film flare/bloom spreads gently
- natural fade-out

## Camera DNA

- intimate observational handheld cinematography
- optical reference: approximately 50 mm-like portrait perspective
- shallow depth of field
- one extremely slow subtle push-in only
- minimal handheld breathing at the scale of a real operator's breathing
- slightly off-center framing
- natural negative space
- foreground flowers/leaves may be imperfectly cropped
- camera observes person and environment together

Avoid unnecessary orbit, dramatic dolly, fast pan/tilt, rapid cuts, or large viewpoint changes.

## Motion Budget

**LOW**

```text
body        very low
head        very low
eyes        low-to-medium
expression  very low
hair        low
clothing    very low
plants      low
camera      very low
lighting    very low
```

## Micro Motion

- natural breathing
- approximately one blink
- gaze leads head correction
- almost invisible head movement
- final micro-smile only
- a few hair strands respond to breeze
- clothing responds minimally

Canonical rhythm:

```text
stillness → subtle motion → stillness
```

## Ambient Motion Field

Physical cause: one weak summer breeze plus moving leaves affecting sunlight.

- flowers: low-amplitude coherent sway
- leaves: low-amplitude coherent sway
- hair: only a few strands
- clothing: very slight movement
- light: dapple pattern changes only as leaves move
- atmosphere: subtle warm humidity / dust texture
- camera: minimal breathing

## Visual DNA

### Natural light

- real midsummer afternoon light
- strong sunlight passing through foliage
- warm humid air
- slight distant heat softness
- moving leaf shadows produce very small changes on skin/background
- occasional highlights may clip gently like film

### Analog mood

Reference character:
- 1990s to early-2000s summer-memory film aesthetic
- Portra 400 / Superia 400 inspired color response
- warm natural skin
- soft cyan-biased shadows
- subtle magenta skin undertone
- lifted blacks
- soft highlight roll-off
- low-to-moderate saturation
- fine organic grain
- subtle bloom and halation
- restrained natural vintage flare
- slight analog scan texture
- slightly imperfect organic focus rather than hyper-sharp digital rendering

Camera/film brand names are references, not hard technical claims.

## Audio DNA

### 0–2 s

Natural ambience first:
- distant birds
- weak summer breeze
- flowers/leaves brushing softly

### After 2 s

Original instrumental BGM slowly fades in:
- warm dreamy summer acoustic ambient
- ~70–78 BPM
- soft acoustic or clean guitar
- subtle ambient pad
- very light lo-fi texture
- no strong drums / fast beat

### 8–10 s eye-contact peak

- lower BGM slightly
- make wind, leaves and distant birds a little clearer
- preserve intimacy and spatial air

### Ending

- guitar/ambient reverb tail
- natural fade-out

## Hard Constraints

Desired stable state:
- same facial identity throughout
- stable facial proportions
- stable hairstyle and hair length
- stable wardrobe design/pattern/color
- stable body proportions
- natural anatomy and hands
- stable background geometry
- stable lighting logic
- minimal realistic facial motion
- coherent gentle wind
- restrained optical effects

Known unwanted behaviors:
- face morphing / identity drift
- facial feature changes
- body-proportion changes
- warped hands or duplicated limbs
- exaggerated smile/expression
- continuous posing
- beauty-commercial acting
- unnatural blinking or artificial eye movement
- excessive head/body/hair motion
- strong artificial wind
- unrealistic plant motion
- fast zoom / aggressive push-in / orbit / rapid pan/tilt
- excessive handheld shake
- background morphing
- plastic skin / heavy beauty filtering
- excessive HDR/sharpening/flare/bloom
- flicker / unstable face / unstable lighting
- generic AI-like floating motion
- text / subtitles / logos / watermark

## Example I2V Runtime Prompt (generic concise form)

```text
Continuous intimate observational shot. The woman initially looks quietly at the nearby flowers. Her eyes slowly shift toward the camera first, followed by an almost imperceptible head movement. She blinks naturally once. A very gentle coherent summer breeze moves nearby flowers and leaves, a few strands of her hair, and her clothing subtly. Dappled sunlight shifts slightly across her skin and hair as the leaves move. The camera performs one extremely slow subtle push-in with minimal natural handheld breathing. Near the final third she establishes quiet direct eye contact and holds it briefly; her expression softens into an almost imperceptible micro-smile while the camera settles and becomes nearly still. Near the end her gaze lowers slightly back toward the flowers as foreground flowers drift partly across frame. Stable facial identity throughout, minimal subject motion, natural causal environmental motion, warm midsummer memory, organic film-like texture.
```

## Evaluation focus

1. identity consistency
2. gaze realism
3. ability to settle into stillness
4. coherent wind across flowers/hair/fabric
5. eye-contact emotional peak
6. avoidance of beauty-ad posing
7. absence of continuous AI-like floating motion

This example should be revised after real MiniMax/Kling/Veo/Runway tests rather than treated as final.