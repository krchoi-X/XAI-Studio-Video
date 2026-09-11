#!/usr/bin/env python3
"""Build a local two-up page that asks which of two frames reads more like the character, and why.

    python tools/pairwise_preference.py --set LIBRARY/imports/derived/identity-set-YYYYMMDD \
        --out REPORT/preference --pairs 40

Why this exists: the similarity scores separate different people cleanly and say nothing about which frame of
one person looks most like her. Tested against 23 frames an operator picked by eye, every measure landed at
chance. A forced choice between two frames of the same angle carries that signal; a ranking does not.

Three rules, each one a correction to the first version of this page:

* **No image may dominate.** The first build sorted pairs by how differently the two recognisers ranked them,
  which put one outlier image into all nine frontal pairs - the operator saw the same face nine times and the
  result said nothing. Appearances are now capped and spread evenly.
* **The two frames come from different clips.** Neighbouring frames of one clip are near-identical, so the
  choice is a coin flip and the answer teaches nothing.
* **The reason is worth more than the click.** "The jaw is longer than I designed" told us more in one
  sentence than forty binary answers did, so each choice can carry which feature decided it.

The page is a plain local file with the images beside it. Nothing is uploaded, and the answers stay on the
machine until the operator saves them - these are private character assets.
"""
from __future__ import annotations

import argparse
import json
import random
import shutil
from pathlib import Path
from typing import Any

REASONS = ["턱·얼굴형", "눈매", "볼", "입", "피부", "전체 인상", "잘 모르겠음"]

PAGE = """<!doctype html>
<meta charset="utf-8">
<title>{title}</title>
<style>
  :root {{ color-scheme: dark; --bg:#17150f; --fg:#f2ede3; --dim:#9c968a; --line:#332f26; --gold:#c9a227; }}
  * {{ box-sizing:border-box; }}
  body {{ background:var(--bg); color:var(--fg); font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;
         margin:0; padding:20px; }}
  header, .pair, .bar, .reasons {{ max-width:1100px; margin-left:auto; margin-right:auto; }}
  h1 {{ font-size:18px; margin:0 0 4px; }}
  header p {{ color:var(--dim); margin:0 0 14px; font-size:14px; }}
  .pair {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; }}
  figure {{ margin:0; cursor:pointer; border:3px solid var(--line); border-radius:12px; overflow:hidden;
            background:#000; transition:border-color .12s, transform .12s; }}
  figure:hover {{ border-color:var(--gold); transform:translateY(-2px); }}
  figure.picked {{ border-color:#7ee787; }}
  img {{ display:block; width:100%; height:auto; }}
  figcaption {{ padding:7px 10px; font-size:12px; color:var(--dim); }}
  .reasons {{ margin-top:16px; display:none; gap:8px; flex-wrap:wrap; }}
  .reasons.on {{ display:flex; }}
  .reasons b {{ font-weight:600; font-size:14px; align-self:center; margin-right:4px; }}
  button {{ background:#26221a; color:var(--fg); border:1px solid var(--line); border-radius:9px;
            padding:9px 14px; font:inherit; font-size:14px; cursor:pointer; }}
  button:hover {{ border-color:var(--gold); }}
  .bar {{ margin-top:18px; display:flex; gap:10px; align-items:center; justify-content:space-between;
          border-top:1px solid var(--line); padding-top:14px; color:var(--dim); font-size:14px; }}
  .done {{ text-align:center; padding:70px 0; }}
</style>
<header>
  <h1>{title}</h1>
  <p>같은 각도의 두 장 중 <strong>더 이 인물 같은 쪽</strong>을 누르고, 이어서 <strong>무엇이 결정적이었는지</strong>
     한 번 더 눌러주세요. 판단이 어려우면 건너뛰세요. 아무것도 업로드되지 않습니다.</p>
</header>
<div id="stage"></div>
<div class="reasons" id="reasons"></div>
<div class="bar">
  <span id="count"></span>
  <span><button id="skip">건너뛰기</button> <button id="save">답변 저장</button></span>
</div>
<script>
// Every handler is attached here, never written into an attribute. The first build put the reason text
// inside an inline handler attribute; the quotes JSON.stringify produced closed the attribute early, so the
// handler never ran and the page silently refused to advance.
const PAIRS = {pairs};
const REASONS = {reasons};
const KEY = {storage};
let answers = JSON.parse(localStorage.getItem(KEY) || "[]");
let i = answers.length, pending = null;

const stage = document.getElementById("stage");
const box = document.getElementById("reasons");
const count = document.getElementById("count");

function render() {{
  box.className = "reasons"; box.textContent = ""; pending = null;
  count.textContent = `${{Math.min(i + 1, PAIRS.length)}} / ${{PAIRS.length}}`;
  stage.textContent = "";
  if (i >= PAIRS.length) {{
    stage.innerHTML = '<div class="done"><h1>끝났습니다</h1><p>저장 버튼을 눌러주세요.</p></div>';
    return;
  }}
  const pair = PAIRS[i];
  const grid = document.createElement("div");
  grid.className = "pair";
  [pair.a, pair.b].forEach((frame, n) => {{
    const figure = document.createElement("figure");
    const image = document.createElement("img");
    image.src = "images/" + frame.file;
    const caption = document.createElement("figcaption");
    caption.textContent = `${{pair.bucket}} · yaw ${{frame.yaw.toFixed(2)}}`;
    figure.append(image, caption);
    figure.addEventListener("click", () => choose(n, figure, grid));
    grid.append(figure);
  }});
  stage.append(grid);
}}

function choose(n, figure, grid) {{
  pending = n === 0 ? "a" : "b";
  Array.from(grid.children).forEach(child => child.classList.remove("picked"));
  figure.classList.add("picked");
  box.className = "reasons on";
  box.textContent = "";
  const label = document.createElement("b");
  label.textContent = "무엇이 결정적이었나요?";
  box.append(label);
  REASONS.forEach(reason => {{
    const button = document.createElement("button");
    button.textContent = reason;
    button.addEventListener("click", () => {{ if (pending) record(pending, reason); }});
    box.append(button);
  }});
}}

function record(choice, why) {{
  answers.push({{pair: PAIRS[i].id, bucket: PAIRS[i].bucket, a: PAIRS[i].a.file, b: PAIRS[i].b.file,
                choice: choice, reason: why || null}});
  localStorage.setItem(KEY, JSON.stringify(answers));
  i += 1; render();
}}

document.getElementById("skip").addEventListener("click", () => record("skip", null));
document.getElementById("save").addEventListener("click", () => {{
  const blob = new Blob([JSON.stringify(answers, null, 1)], {{type: "application/json"}});
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob); link.download = {filename}; link.click();
}});
render();
</script>
"""


def choose_pairs(members: list[dict[str, Any]], wanted: int, cap: int, rng: random.Random) -> list[tuple]:
    """Spread the clicks: take the least-used images first, and never pair a clip with itself.

    Two frames of one clip a few hundred milliseconds apart are the same picture for this purpose - the
    operator reported the first round as hard to judge, and that is part of why.
    """
    appearances = {member["file"]: 0 for member in members}
    used: set[frozenset] = set()
    chosen = []
    for _ in range(wanted * 40):
        if len(chosen) >= wanted:
            break
        pool = [m for m in members if appearances[m["file"]] < cap]
        if len(pool) < 2:
            break
        rng.shuffle(pool)
        pool.sort(key=lambda m: appearances[m["file"]])
        first = pool[0]
        partners = [m for m in pool[1:] if m["clip"] != first["clip"]
                    and frozenset((first["file"], m["file"])) not in used]
        if not partners:
            appearances[first["file"]] = cap  # retire an image that can no longer be paired
            continue
        second = partners[0]
        used.add(frozenset((first["file"], second["file"])))
        appearances[first["file"]] += 1
        appearances[second["file"]] += 1
        chosen.append((first, second))
    return chosen


def build(args: argparse.Namespace) -> dict[str, Any]:
    source = Path(args.set).resolve()
    manifest = json.loads((source / "identity-set.json").read_text(encoding="utf-8"))
    out_dir = Path(args.out).resolve()
    images = out_dir / "images"
    shutil.rmtree(images, ignore_errors=True)
    images.mkdir(parents=True, exist_ok=True)

    by_bucket: dict[str, list[dict[str, Any]]] = {}
    for member in manifest["members"]:
        by_bucket.setdefault(member["yaw_bucket"], []).append(member)

    # Frontal gets the largest share: it is the bucket where the operator's choices and the scores disagree,
    # and the one a master is eventually chosen from.
    weights = {"frontal": 0.35, "three_quarter": 0.20, "deep_three_quarter": 0.22, "profile": 0.23}
    rng = random.Random(args.seed)
    pairs, appearances = [], {}
    for bucket, members in sorted(by_bucket.items()):
        wanted = round(args.pairs * weights.get(bucket, 1 / len(by_bucket)))
        for first, second in choose_pairs(members, wanted, args.max_appearances, rng):
            for member in (first, second):
                target = images / member["file"]
                if not target.exists():
                    shutil.copyfile(source / member["file"], target)
                appearances[member["file"]] = appearances.get(member["file"], 0) + 1
            left, right = (first, second) if rng.random() < 0.5 else (second, first)
            pairs.append({"id": len(pairs), "bucket": bucket,
                          "a": {"file": left["file"], "yaw": left["yaw_proxy"], "clip": left["clip"]},
                          "b": {"file": right["file"], "yaw": right["yaw_proxy"], "clip": right["clip"]}})
    rng.shuffle(pairs)
    for index, pair in enumerate(pairs):
        pair["id"] = index

    page = PAGE.format(title=args.title, pairs=json.dumps(pairs, ensure_ascii=False),
                       reasons=json.dumps(REASONS, ensure_ascii=False),
                       storage=json.dumps(f"pref-{manifest['character_id']}-{args.round}"),
                       filename=json.dumps(f"preference-{manifest['character_id']}-{args.round}.json"))
    if "onclick=" in page:
        raise ValueError("inline handlers are not allowed: data in an onclick attribute breaks on quotes")
    (out_dir / "index.html").write_text(page, encoding="utf-8")
    (out_dir / "pairs.json").write_text(json.dumps(
        {"character_id": manifest["character_id"], "round": args.round, "source_set": str(source),
         "reasons": REASONS, "pairs": pairs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"page": str(out_dir / "index.html"), "pairs": len(pairs),
            "per_bucket": {b: sum(1 for p in pairs if p["bucket"] == b) for b in sorted(by_bucket)},
            "distinct_images": len(appearances),
            "max_appearances_of_one_image": max(appearances.values(), default=0)}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--set", required=True, help="a directory holding identity-set.json")
    parser.add_argument("--out", required=True)
    parser.add_argument("--pairs", type=int, default=40)
    parser.add_argument("--max-appearances", type=int, default=2,
                        help="how often one image may be shown; the point is that no image dominates")
    parser.add_argument("--round", default="r2", help="keeps rounds from resuming each other's answers")
    parser.add_argument("--seed", type=int, default=20260911)
    parser.add_argument("--title", default="어느 쪽이 더 이 인물 같나요?")
    return parser


def main() -> int:
    print(json.dumps(build(build_parser().parse_args()), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
