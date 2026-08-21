# Evidence-First Reference Extraction

Use this guide when reverse-engineering an image or video reference into a reusable production description.

The objective is not to guess how the source was made. The objective is to extract enough visible structure to recreate its useful properties while clearly separating observation from inference.

## Core rule

**Visible evidence first. Unsupported inference stays out of the production spec.**

## What to extract

### Subject state

- pose
- gaze direction
- face orientation
- body orientation
- weight distribution when visible
- contact with floor, furniture, props, or other subjects
- visible expression
- visible wardrobe and accessories

### Composition

- framing
- crop
- subject position in frame
- camera-height impression
- foreground / midground / background relationships
- dominant lines and shapes
- occlusion relationships
- negative space

### Camera-relevant evidence

Describe observable geometry rather than invented hardware.

Prefer:
- ground-level viewpoint
- wide-perspective distortion
- compressed perspective
- shallow depth of field
- deep focus
- off-center composition

Avoid unsupported claims such as an exact lens, camera body, sensor, or rig.

### Lighting

- apparent direction
- hardness / softness
- relative contrast
- highlight behavior
- shadow direction
- backlight / rim behavior
- practical or environmental sources that are actually visible

Do not invent hidden studio equipment merely to explain the result.

### Material and texture

- skin rendering character
- hair texture
- fabric behavior
- wet / dry / glossy / matte properties
- surface roughness
- atmospheric haze, dust, rain, condensation, etc.

### Spatial blocking

Record story-relevant geometry:
- who is where
- what each subject faces
- distance relationships
- prop ownership
- foreground blockers
- potential paths of motion

Spatial blocking is often more useful for video continuity than aesthetic description.

### Movable elements

Identify what could plausibly move in a generated clip:
- hair strands
- clothing
- plants
- curtains
- water
- loose paper
- suspended dust
- practical lights / reflections

For each, record the likely physical cause only when the source supports it.

## Observation vs inference

Use this distinction explicitly when uncertainty matters.

```text
Observation:
Strong highlight from frame left; shadow falls toward frame right.

Inference:
Could be late-afternoon sun or a hard artificial source.

Production description:
Strong directional key from frame left with crisp but natural shadow falloff.
```

The production description should preserve the visible effect without depending on an unverified explanation.

## Reference State template

```yaml
subject:
  pose:
  gaze:
  face_orientation:
  body_orientation:
  contacts:
  expression:
  wardrobe:

camera:
  apparent_height:
  perspective_character:
  framing:
  crop:
  depth_of_field:

composition:
  foreground:
  midground:
  background:
  dominant_geometry:
  occlusions:

lighting:
  direction:
  hardness:
  contrast:
  highlight_behavior:
  shadow_behavior:

materials:
  skin:
  hair:
  fabric:
  surfaces:

blocking:
  subject_positions:
  prop_relationships:
  motion_paths:

movable_elements:
  - element:
    plausible_motion:
    cause:

uncertainties:
  - unsupported inference to avoid
```

## From reference to prompt

Do not dump the entire extraction into the Runtime Prompt.

Use the extraction to decide:
1. what the reference input already supplies,
2. what must be protected as a Hard Lock,
3. what should be restated as Soft Guidance,
4. what can be left to Creative Freedom,
5. what the target model adapter actually needs in text.

## Series Master use

A strong reference can become a Series Master when multiple future outputs should inherit its identity or visual grammar.

Preserve only robust anchors. Do not turn incidental details into permanent DNA unless repeated experiments show they matter.