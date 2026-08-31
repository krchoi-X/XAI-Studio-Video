# Harim — Hair DNA

Version: 0.1

## Why hair is part of identity

Harim's hairstyle is a recognition anchor, not a completely free scene variable.

The goal is not to keep one hairstyle forever, but to restrict changes to a small set of recurring, recognizable Hair States so that image and video variations still read as the same person.

## Stable hair properties

- naturally dark brown to near-black
- long hair, normally reaching around mid-back
- straight or only softly naturally bent
- fine-to-medium strand thickness
- smooth texture
- healthy controlled shine
- stable hairline shape
- no heavy default wave/curl pattern

## Hair State A — Primary / High Ponytail

This is Harim's primary signature hairstyle and should be the default for identity-establishing images.

- high ponytail tied near the upper back/crown area
- soft natural crown volume
- long ponytail
- thin natural face-framing strands
- light wispy fringe or soft side-bangs
- forehead partially visible
- clean neckline
- should emphasize her long neck, small face, and narrow shoulders

## Hair State B — Long Hair Down

- long straight hair worn down
- center or softly off-center part
- light face-framing strands
- some hair may be tucked behind one ear
- avoid excessive salon waves or oversized volume

## Hair State C — Slim Black Headband

- slim matte black headband
- approximately 1–1.5 cm visual width
- forehead more exposed than usual
- clean minimal form
- no bow
- no oversized decorative ornament

Purpose:
Creates a recognizable alternate look while clearly remaining Harim.

## Hair State D — Compact Updo with Signature Pin

- hair twisted into a loose but compact updo
- secured with a slim dark tortoiseshell or brushed-silver U-shaped hairpin
- minimal design, no jewel-heavy decoration
- a few thin natural strands may remain around the face and nape

## Continuity rules

Do not silently change:
- hair color
- baseline hair length
- hairline
- strand character

Do not introduce by default:
- blonde/reddish dye
- short bob
- very heavy blunt bangs
- strong curls
- oversized teased volume

## State-selection rule

For each generation or video shot, metadata should explicitly record:

`hair_state: A | B | C | D`

If a new recurring hairstyle is desired, add a new named Hair State rather than allowing ad-hoc drift.
