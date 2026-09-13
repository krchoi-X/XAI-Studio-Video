# Noa self-introduction short — six speaking shots

Character `ch-shindo-noa` at v2 (`161a5aea608b`), reference `noa-21` portrait plus its face crop, engine
`minimax_h3_ref2va_pruned`, rendered locally. Six shots, 181 frames each at 24 fps — about 7.5 s per shot,
roughly a 45 second short. Nothing here is approved; nothing was pushed.

## The capability this depends on, which had gone unused

`minimax_h3_ref2va_pruned` is **Reference-to-Video-and-Audio**. Its own definition at
`D:\AI\WanGP\defaults\minimax_h3_ref2va_pruned.json` says so, and carries a worked example containing a
lip-synced spoken line:

> ... saying clearly (S1) `<d>`[English] Some journeys begin when the map runs out.`</d>`

together with the `overall_soundscape` and `non_diegetic_music` trailer fields, which shape the stereo
track. Every clip rendered for this character since 2026-09-12 carries a real AAC stream; measured, they
sit at −85.5 dB mean, because every prompt so far ended with "a quiet neutral room tone and nothing else."
The audio path was working the whole time and was being asked for silence.

So a talking-head short needs no separate text-to-speech, no lip-sync model, and no external service. None
of `InfiniteTalk`, `MultiTalk` or `S2V` is installed here, so without this the short would not have been
possible locally at all.

## Verification gate

**Shot 1 renders and is inspected alone before the other five are queued.** Lip sync quality and the
generated voice are unverified on this build, and a speaking prompt may also cost identity. The checks on
shot 1 are: the audio track is no longer near-silent, the mouth moves with the words, and the face still
measures as Noa against the `noa-21` prototype. One clip lost is better than six.

There is a known cost going in. The angle work measured that keeping the reference's own room was the
single largest identity lever, worth about +0.13 ArcFace, and these shots deliberately move her into three
new locations. Each prompt therefore restates the identity anchors — eye shape, brow-to-eye distance, brow
line, midface, nose and chin — and the result will be measured rather than assumed.

## Script

Language is English on the operator's instruction. It is also the only variant the model definition
demonstrates, so Japanese and Korean lip-sync remain untested here.

| Shot | Location | Wardrobe | Line |
|---|---|---|---|
| `intro-1-name` | the flat, morning | home tee | My name is Noa. Shindo Noa. I live alone, near the river. |
| `intro-2-work` | the shop display | work blazer | I build shop windows for a beauty brand. People slow down. That is the job. |
| `intro-3-history` | the shop display | work blazer | I started on the sales floor. I studied at night for four years. |
| `intro-4-things` | the flat, table | home tee | I do not own much. What I keep, I keep for a long time. |
| `intro-5-help` | a street at dusk | bomber | I am not good at asking for help. I am working on that. |
| `intro-6-close` | the flat, evening | home tee | That is me. Thank you for stopping. |

Every fact spoken is from the record's own `scene_defaults`: the visual-merchandiser job, advancing from
retail through night study, the small 1LDK near Shin-Maruko / Musashi-Kosugi, few possessions kept a long
time, and being slow to ask for help. The three wardrobes are its `wardrobe_direction`. Nothing was
invented, and the lines are written to the record's restraint — no jokes, no performed warmth, and shot 6
allows warmth only in the eyes.

## Assembly

Output is 576x768, which is 3:4 rather than a short's 9:16. This resolution is the one every clip for this
character has used and it is left alone rather than changed untested. Two deliverables come out of post,
both by ffmpeg concat with no GPU cost:

- a 3:4 master at native resolution;
- a 9:16 crop at 432x768, centred, which loses a quarter of the width and is safe for a centred subject.

## What to judge

The face, the voice, and whether the lines sound like her. If the writing is wrong that is a script fix and
costs nothing. If the *character* is wrong — if she would not say these things — that is a
`scene_defaults.personality` conversation, not a prompt one.

---

## Results, 2026-09-13

Seven clips rendered (six shots plus one replacement). The finished cut is 43.8 s, in
`D:\AI_Studio\library\characters\ch-shindo-noa\generations\SHORT-20260913-noa21-self-introduction\edit\`
as `noa-self-intro-3x4.mp4` (576x768) and `noa-self-intro-9x16.mp4` (432x768).

### Speech: six of six exact

Every shot was transcribed with Whisper and compared to its intended line. All six came back word-for-word,
and the assembled cut transcribes as the whole script in order. Mean volume −15.3 to −19.2 dB against the
−85.5 dB of every earlier clip. Mouth articulation is visible frame by frame, not a static mouth.

The gate worked as intended: shot 1 was rendered and checked alone before the other five were committed.

### Identity: the score here measures framing, not the room

| Shot | Face | ArcFace |
|---|---|---|
| `intro-1-name` | 236-302 px | 0.813-0.826 |
| `intro-6-close` | 176-206 px | 0.811-0.819 |
| `intro-3-history` | 106-107 px | 0.806-0.835 |
| `intro-2-work` | 90-94 px | 0.757-0.784 |
| `intro-4-things` | 82-88 px | 0.700-0.721 |
| `intro-5-help` | **47-48 px** | 0.512-0.558 |

**This revises the reading recorded earlier in the day.** The drop was first attributed to moving her out of
the reference's own room, which the angle work measured at about +0.13 ArcFace. That effect is real but it
is not what orders this table: a shop shot at 107 px scores 0.835 while a home shot at 85 px scores 0.72.
Face size in frame explains the ordering almost perfectly and the location does not.

So `intro-5-help` at 0.51 must **not** be read as a different person. Forty-seven pixels is far below what
either recogniser can resolve, the same caveat already applied to the full-body clips. The number is
measuring the framing.

`intro-5-help` was still replaced, for an editorial reason rather than a measured one: a person occupying a
tenth of the frame gives a self-introduction nothing. `intro-5b-help` reframes and measures 89-91 px and
0.762-0.809, with the line still transcribing exactly.

### The framing lesson, which is reusable

"A steady medium shot holds her standing on the pavement, the street receding softly behind her" produced a
wide street scene. "A steady close-up holds her head and shoulders" produced a close-up. **Describing what
fills the frame works; describing what is behind the subject invites a wide, and the word "steady" does not
prevent a push-in** — shot 1 travelled from full length to an extreme close-up despite it.

### Open questions for the operator

- The voice is the model's choice. Whether it can be steered is unknown and untested.
- `intro-2-work` is the weakest shot on both identity and background; the short still reads at five shots.
- If the lines are wrong in *character* rather than in wording, that is a `scene_defaults.personality`
  question, not a prompt one.
