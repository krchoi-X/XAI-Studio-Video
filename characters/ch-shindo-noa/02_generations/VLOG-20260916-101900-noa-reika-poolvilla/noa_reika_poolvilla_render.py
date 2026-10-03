# -*- coding: utf-8 -*-
"""Noa+Reika pool-villa ~60s sequential H3 Ref2VA pipeline."""
import json
import time
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

PY = Path(r"D:\AI\WanGP\env_uv\Scripts\python.exe")
REPO = Path(r"D:\codex\XAI-studio")
WANGP = Path(r"D:\AI\WanGP")
NOA_PORTRAIT = Path(r"D:\AI_Studio\library\characters\ch-shindo-noa\imports\derived\noa-21-portrait.jpg")
NOA_FACE = Path(r"D:\AI_Studio\library\characters\ch-shindo-noa\imports\derived\noa-21-facecrop.png")
REIKA_FACE = Path(
    r"D:\AI_Studio\library\characters\ch-mizuki-reika\generations\GPT-20260906-reika-face-09-editorial\outputs\gpt\face-09-editorial-1.png"
)

SESSION_ID = "VLOG-20260916-101900-noa-reika-poolvilla"
SESSION = Path(r"D:\codex\XAI-studio\characters\ch-shindo-noa\02_generations") / SESSION_ID
LIB_OUT = (
    Path(r"D:\AI_Studio\library\characters\ch-shindo-noa\generations")
    / SESSION_ID
    / "outputs"
    / "minimax-h3"
)
LIB_EDIT = Path(r"D:\AI_Studio\library\characters\ch-shindo-noa\generations") / SESSION_ID / "edit"
PROMPTS_ROOT = Path(r"D:\AI_Studio\outputs\video-prompts\projects") / SESSION_ID
STITCH_NAME = "noa-reika-poolvilla.mp4"
LOG = SESSION / "pipeline.log"
STATUS = SESSION / "STATUS.txt"

KST = timezone(timedelta(hours=9))


def now_kst():
    return datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S KST")


def append_status(msg: str):
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    with STATUS.open("a", encoding="utf-8") as f:
        f.write(f"[{now_kst()}] {msg}\n")
    print(msg, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"[{now_kst()}] {msg}\n")


def idle():
    p = subprocess.run(
        [str(PY), "-m", "control_tower", "--check"],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    t = (p.stdout or "") + "\n" + (p.stderr or "")
    return ("running=0" in t) and ("active=0" in t) and ("RUNNING" not in t)


def wait_idle():
    while not idle():
        append_status("BUSY waiting for GPU idle (running=0 active=0)")
        time.sleep(60)


def extract_last(mp4: Path, png: Path):
    png.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(
        ["ffmpeg", "-y", "-sseof", "-0.15", "-i", str(mp4), "-frames:v", "1", "-q:v", "2", str(png)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if r.returncode != 0 or not png.is_file():
        r2 = subprocess.run(
            ["ffmpeg", "-y", "-sseof", "-1", "-i", str(mp4), "-update", "1", "-q:v", "2", str(png)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if r2.returncode != 0 or not png.is_file():
            raise RuntimeError(r.stderr or r2.stderr or "ffmpeg last-frame fail")


def wait_run(run_dir: Path, out: Path):
    rj = run_dir / "run.json"
    while True:
        if not rj.is_file():
            append_status(f"wait {run_dir.name} (no run.json yet)")
            time.sleep(20)
            continue
        rec = json.loads(rj.read_text(encoding="utf-8"))
        st = rec.get("status")
        append_status(f"wait {run_dir.name} status={st}")
        if st in {"succeeded", "needs_review", "failed", "cancelled", "interrupted", "timed_out"}:
            if st not in {"succeeded", "needs_review"}:
                err = rec.get("error")
                raise SystemExit(f"fail {st} {err}")
            arts = rec.get("artifacts") or []
            if arts:
                return Path(arts[0]["path"])
            mp4s = sorted(out.glob(f"{run_dir.name}*.mp4"))
            if not mp4s:
                raise SystemExit(f"no mp4 for {run_dir}")
            return mp4s[0]
        time.sleep(45)


def settings(length, refs):
    return {
        "model_type": "minimax_h3_ref2va_pruned",
        "video_prompt_type": "KI",
        "audio_prompt_type": "",
        "resolution": "576x768",
        "video_length": length,
        "sliding_window_size": min(max(length * 2, 362), 481),
        "sliding_window_overlap": 18,
        "num_inference_steps": 20,
        "guidance_scale": 1.0,
        "flow_shift": 12.0,
        "sample_solver": "euler",
        "skip_steps_start_step_perc": 25,
        "skip_steps_multiplier": 0.08,
        "denoising_strength": 1.0,
        "image_mode": 0,
        "image_refs_relative_size": 125,
        "remove_background_images_ref": 0,
        "seed": -1,
        "image_refs": refs,
    }


NOA_DNA = (
    "Picture 1 is Noa (noa-21): lean youthful mid-20s face, large horizontally elongated "
    "almond dark-brown eyes with visible sclera, low brow-to-eye distance, straight refined "
    "nose, clean lean jaw, upright posture, restrained presence. Adult woman. "
    "Picture 1 face and body proportions only; ignore its background."
)

REIKA_DNA = (
    "Picture 2 is Reika (face-09): adult Japanese woman about 23, long jet-black hair, "
    "individual eye spacing, nose, lips and jaw locked from the master face; soft cool "
    "editorial features. Use face identity only; ignore jacket, clothing and studio background."
)


def conti_line():
    return (
        "Picture 3 is the previous shot final frame for continuity of place, light, wardrobe "
        "and body pose - do not replace either woman's face."
    )


SHOTS = [
    (
        "b1-meet",
        241,
        10,
        "hook LS",
        NOA_DNA
        + " "
        + REIKA_DNA
        + "\nFRAME LS: Morning suburban street; a classic convertible or vintage coupe parked roadside; "
        "soft early sun. Steady long shot holds both full figures as they meet and shake hands; "
        "Noa in a light mini-dress, Reika in a short top and shorts; both small-to-medium in frame for place.\n"
        "ACTION: They greet, handshake once; Noa says clearly (S1) <d>[Japanese] おはよう。</d> "
        "then a short shared laugh; Reika soft smile.\n"
        "SOUND: morning birds, distant street, soft laugh. Prompt enhancer off.",
    ),
    (
        "b2-board",
        193,
        8,
        "bridge MS",
        NOA_DNA
        + " "
        + REIKA_DNA
        + " "
        + conti_line()
        + "\nFRAME MS: Medium shot at the classic car door; morning light continuous from previous beat.\n"
        "ACTION: Unhurried board - Noa slips into driver seat, Reika passenger; doors close once; "
        "bags briefly visible. No dialogue.\n"
        "SOUND: car door, soft fabric, quiet street. Prompt enhancer off.",
    ),
    (
        "b3-drive",
        289,
        12,
        "info MCU",
        NOA_DNA
        + " "
        + REIKA_DNA
        + " "
        + conti_line()
        + "\nFRAME MCU: Cabin medium close-up two-shot; Noa drives, Reika beside her; mountain road "
        "blur outside windows; same morning wardrobe.\n"
        "ACTION: Easy chat while driving. Reika says (S2) <d>[Japanese] 今日いい天気だね。</d> "
        "then (S2) <d>[Japanese] プール楽しみ。</d> Noa answers once (S1) <d>[Japanese] うん。</d>\n"
        "SOUND: soft engine, wind through open window. Prompt enhancer off.",
    ),
    (
        "b4-pool",
        529,
        22,
        "bridge LT",
        NOA_DNA
        + " "
        + REIKA_DNA
        + " "
        + conti_line()
        + "\nFRAME LT: One unbroken long take at a mountain pool villa: car arrives at timber villa "
        "with outdoor pool; both women exit and run lightly toward the pool deck; they undress "
        "naturally (mini-dress / short top+shorts off onto lounge chairs) then nude pool entry "
        "together; water settles. Adult bodies, non-pornographic documentary calm; no strip-show posing.\n"
        "ACTION: Arrive, run, undress, enter water once. Short cheer only - Reika (S2) <d>[Japanese] やったー！</d>\n"
        "SOUND: car stop, footsteps on wood, cloth, water splash, mountain air. Prompt enhancer off.",
    ),
    (
        "b5-enter",
        193,
        8,
        "bridge MS",
        NOA_DNA
        + " "
        + REIKA_DNA
        + " "
        + conti_line()
        + "\nFRAME MS: Medium shot continuous place - nude exit from pool, quick towel or wrap optional "
        "but bodies still bare-ish wet; they fetch bags from the classic car then enter the villa building "
        "through glass doors. Mountain villa architecture readable.\n"
        "ACTION: Exit pool, grab bags, enter building once. No dialogue.\n"
        "SOUND: water drip, bag zip, door. Prompt enhancer off.",
    ),
]


STORYBOARD = """# Noa + Reika ~60s — classic car to mountain pool villa

**Brief:** User approved go-go. Two adult fictional women (Noa mid-20s / Reika ~23) drive a classic car to a mountain pool villa; nude pool entry intentional.
**Engine:** WanGP local `minimax_h3_ref2va_pruned` Ref2VA KI 576x768.
**Publish:** NO.
**Refs:** Picture1=noa-21-portrait; Picture2=reika face-09-editorial; Picture3=prev last (shots 2–5).

| # | id | role | code | ~sec (frames) | visual | dialogue |
|---|---|---|---|---|---|---|
| 1 | b1-meet | hook | **LS** | 10s (241) | Classic car morning meet + handshake; light mini-dress + short top/shorts | (S1) おはよう + short laugh |
| 2 | b2-board | bridge | **MS** | 8s (193) | Unhurried board car | none |
| 3 | b3-drive | info | **MCU** | 12s (289) | Noa drives, Reika chat | (S2) 今日いい天気だね。 / プール楽しみ。 (S1) うん。 |
| 4 | b4-pool | bridge | **LT** | 22s (529) | Arrive villa → run → undress → nude pool entry one take | (S2) やったー！ short cheer |
| 5 | b5-enter | bridge | **MS** | 8s (193) | Nude exit → bags from car → enter building | none |

**Total ~60s.** Assembly: ffmpeg concat copy → `edit/noa-reika-poolvilla.mp4`.
"""


PROJECT_MD = f"""# {SESSION_ID}

Noa + Reika classic car → mountain pool villa ~60s / 5 H3 Ref2VA shots.

- Studio session: `{SESSION}`
- Library outputs: `{LIB_OUT}`
- Final stitch: `{LIB_EDIT / STITCH_NAME}`
- Model: minimax_h3_ref2va_pruned / KI / 576x768
- Requested-by: grok
- Publish: no
"""


def write_setup():
    for d in [
        SESSION,
        SESSION / "runs",
        SESSION / "continuity",
        LIB_OUT,
        LIB_EDIT,
        PROMPTS_ROOT / "prompts",
    ]:
        d.mkdir(parents=True, exist_ok=True)

    (SESSION / "storyboard.md").write_text(STORYBOARD, encoding="utf-8")
    (PROMPTS_ROOT / "project.md").write_text(PROJECT_MD, encoding="utf-8")

    prompt_entries = []
    for shot, length, sec, role, prompt in SHOTS:
        txt = prompt.strip() + "\n"
        (SESSION / f"{shot}.txt").write_text(txt, encoding="utf-8")
        (PROMPTS_ROOT / "prompts" / f"{shot}.txt").write_text(txt, encoding="utf-8")
        # shot1 settings written now; later shots rewritten at submit with continuity refs
        if shot == "b1-meet":
            refs = [str(NOA_PORTRAIT), str(REIKA_FACE)]
            sp = SESSION / f"{shot}.settings.json"
            sp.write_text(json.dumps(settings(length, refs), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        else:
            # placeholder refs; pipeline overwrites before submit
            refs = [str(NOA_PORTRAIT), str(REIKA_FACE)]
            sp = SESSION / f"{shot}.settings.json"
            sp.write_text(json.dumps(settings(length, refs), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        prompt_entries.append(
            {
                "prompt_id": shot,
                "title": f"{shot} {role} ~{sec}s",
                "prompt_file": str(SESSION / f"{shot}.txt"),
                "settings_file": str(SESSION / f"{shot}.settings.json"),
                "seconds": sec,
                "video_length": length,
                "role": role,
            }
        )

    handoff = {
        "project_id": SESSION_ID,
        "status": "running",
        "target_renderer": "local-wangp",
        "model": "minimax_h3_ref2va_pruned",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_idea": "노아 레이카 둘이 풀빌라 가는거 제작 고고",
        "session_dir": str(SESSION),
        "runs_root": str(SESSION / "runs"),
        "output_dir": str(LIB_OUT),
        "edit_path": str(LIB_EDIT / STITCH_NAME),
        "references": {
            "noa_portrait": str(NOA_PORTRAIT),
            "noa_facecrop": str(NOA_FACE),
            "reika_face09": str(REIKA_FACE),
        },
        "prompts": prompt_entries,
        "requested_by": "grok",
        "publish": False,
    }
    (PROMPTS_ROOT / "handoff.json").write_text(
        json.dumps(handoff, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    append_status(f"SETUP complete session={SESSION_ID}")


def provenance_running():
    subprocess.run(
        [
            str(PY),
            "tools/wangp_recorder.py",
            "session",
            "--session-dir",
            str(SESSION),
            "--requested-by",
            "grok",
            "--engine",
            "WanGP",
            "--model",
            "minimax_h3_ref2va_pruned",
            "--character-id",
            "ch-shindo-noa",
            "--title",
            "Noa+Reika classic car to mountain pool villa ~60s",
            "--user-request",
            "노아 레이카 둘이 풀빌라 가는거 제작 고고",
            "--status",
            "running",
        ],
        cwd=str(REPO),
        check=False,
    )
    append_status("provenance status=running")


def provenance_done(ok: bool):
    subprocess.run(
        [
            str(PY),
            "tools/wangp_recorder.py",
            "session",
            "--session-dir",
            str(SESSION),
            "--status",
            "completed" if ok else "failed",
        ],
        cwd=str(REPO),
        check=False,
    )
    append_status(f"provenance status={'completed' if ok else 'failed'}")


def submit_shot(shot: str):
    sub = subprocess.run(
        [
            str(PY),
            "tools/local_wangp.py",
            "submit",
            "--runs-root",
            str(SESSION / "runs"),
            "--prompt-file",
            str(SESSION / f"{shot}.txt"),
            "--settings-file",
            str(SESSION / f"{shot}.settings.json"),
            "--project-id",
            SESSION_ID,
            "--prompt-id",
            shot,
            "--wangp-root",
            str(WANGP),
            "--output-dir",
            str(LIB_OUT),
            "--requested-by",
            "grok",
        ],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if sub.returncode != 0:
        raise SystemExit(sub.stderr or sub.stdout or f"submit fail {shot}")
    info = json.loads(sub.stdout)
    (SESSION / f"{shot}.submit.json").write_text(
        json.dumps(info, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return info


def run_pipeline():
    write_setup()
    wait_idle()
    provenance_running()
    prev = None
    arts = []
    try:
        for i, (shot, length, sec, role, prompt) in enumerate(SHOTS):
            wait_idle()
            if i == 0:
                refs = [str(NOA_PORTRAIT), str(REIKA_FACE)]
            else:
                refs = [str(NOA_PORTRAIT), str(REIKA_FACE), str(prev)]
            sp = SESSION / f"{shot}.settings.json"
            sp.write_text(json.dumps(settings(length, refs), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            append_status(f"SUBMIT {shot} length={length} refs={len(refs)}")
            info = submit_shot(shot)
            run_id = info.get("run_id") or Path(info["run_dir"]).name
            append_status(f"SUBMITTED {shot} run_id={run_id} run_dir={info.get('run_dir')}")
            mp4 = wait_run(Path(info["run_dir"]), LIB_OUT)
            if not mp4.is_file():
                raise SystemExit(f"missing mp4 {mp4}")
            arts.append(mp4)
            frame = SESSION / "continuity" / f"{shot}-last.png"
            extract_last(mp4, frame)
            prev = frame
            append_status(f"DONE {shot} -> {mp4} last={frame}")

        LIB_EDIT.mkdir(parents=True, exist_ok=True)
        stitch = LIB_EDIT / STITCH_NAME
        lst = SESSION / "stitch.txt"
        lst.write_text("".join(f"file '{a.as_posix()}'\n" for a in arts), encoding="utf-8")
        ff = subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(stitch)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if ff.returncode != 0 or not stitch.is_file():
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-f",
                    "concat",
                    "-safe",
                    "0",
                    "-i",
                    str(lst),
                    "-c:v",
                    "libx264",
                    "-pix_fmt",
                    "yuv420p",
                    "-c:a",
                    "aac",
                    str(stitch),
                ],
                check=False,
            )
        append_status(f"STITCH {stitch} exists={stitch.is_file()}")
        # update handoff
        hp = PROMPTS_ROOT / "handoff.json"
        if hp.is_file():
            h = json.loads(hp.read_text(encoding="utf-8"))
            h["status"] = "needs_review"
            h["stitch"] = str(stitch)
            h["updated_at"] = datetime.now(KST).isoformat()
            hp.write_text(json.dumps(h, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        provenance_done(True)
        append_status("PIPELINE_COMPLETE")
    except Exception as e:
        append_status(f"PIPELINE_FAILED {e!r}")
        provenance_done(False)
        raise


if __name__ == "__main__":
    run_pipeline()
