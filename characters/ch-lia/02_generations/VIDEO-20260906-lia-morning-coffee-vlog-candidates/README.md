# Lia morning-coffee vlog candidates (MiniMax H3 Ref2VA, 10 s)

Start image: window-lit selfie of Lia holding a speckled ceramic mug, heather blue-gray T-shirt, sea and beach through the window, three red-and-blue bracelets on her right wrist. Supplied by the user on 2026-09-06 as a runtime reference only; it is not an approved canonical reference.

Life DNA source: `XAI-Studio-Private/XAI-Studio-Video/docs/characters/lia-life-dna-v1.1.md` (seaside detached house, one cat, convenience-store part-time job, ukulele hobby, beach walks with ice cream, near-expiry rice ball). The cat's appearance is still pending canon, so every prompt keeps the cat off-screen as sound only.

Settings: copy `../VIDEO-20260905-lia-icecream-hi-pilot/minimax-h3-ref2va.settings.json`, replace `image_refs` with the new image path, and set `video_length` to 243 (17*14+5 on the H3 24 fps grid, 10.125 s). 226 frames (9.4 s) is the next shorter valid length.

Voice and speech style are still pending in the Life DNA; all dialogue is short, soft, and English like the pilot.

| File | Episode | Dialogue |
| --- | --- | --- |
| prompt-01-good-morning-cat.txt | Morning greeting, cat meows off-screen | "Morning." / "She's up before me, as usual." |
| prompt-02-sea-is-calm-today.txt | Looks at the sea, plans a beach walk | "The sea is really calm today." / "Maybe a walk later. Ice cream on the way." |
| prompt-03-off-to-work.txt | Morning before the convenience-store shift | "Okay. Shift starts at ten." / "I'll bring a rice ball home." |
| prompt-04-ukulele-cat-complaint.txt | Clumsy ukulele, cat complains | "Everyone's a critic." |

## Run log (2026-09-06)

| Episode | Run | Result | Notes |
| --- | --- | --- | --- |
| 01 | run-20260906-002654-ac69262f | needs_review, 10.125 s, 608x736 H.264 + AAC, 24 min render | Identity, mug, T-shirt, bracelets and window scene held across all sampled frames (`review-01/`). Sip, glance-down and speaking beats are visible. Audio present (mean -20 dB, peak -0.6 dB). `prompt_exact_match` false as in the pilot (WanGP embeds its own prompt copy). Cat stays off-screen. |
| 02 | run-20260906-005142-29e8ca26 | needs_review, 10.125 s, audio present (mean -17 dB, peak -0.4 dB), 25 min render | Identity, mug, T-shirt, bracelets and window scene held (`review-02/`). Head turn to the window, left-hand hair tuck, and closing lowered gaze all appear in order. Smile is wider and more toothy than the DNA's "faint quiet smile" while speaking; consider "small closed-mouth smile" wording if refining. |
| 03 | run-20260906-011642-2f5f3a6f | needs_review, 10.125 s, audio present (mean -19 dB, peak -1.1 dB), 24 min render | Identity, T-shirt, bracelets and window scene held (`review-03/`). Last sip, mug leaving frame, both hands gathering hair to one shoulder, and the closing line with hair still held all appear in order; bangs stay down and no ponytail is completed. Expression again more animated than the DNA's quiet default while speaking. |
| 04 | run-20260906-014111-04975d8a | needs_review, 10.125 s, audio present (mean -25 dB, peak -4.4 dB), 24 min render | Identity, T-shirt, bracelets and window scene held (`review-04/`). Mug leaves frame, a natural-wood four-string ukulele enters, she looks down at the strings while strumming, then looks up with a laugh and the closing line. Finger-to-string contact is plausible in sampled frames. The ukulele reads slightly large (tenor-sized) rather than soprano. Cat stays off-screen. |

All four runs finished between 00:26 and 02:05 KST on 2026-09-06 with the Web UI still resident; no OOM. Sequence status: `sequence-status.json`, log: `sequence-log.txt`.
