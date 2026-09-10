#!/usr/bin/env python3
"""Build a local two-up page that asks which of two frames reads more like the character.

    python tools/pairwise_preference.py --set LIBRARY/imports/derived/identity-set-YYYYMMDD \
        --out REPORT/preference --pairs 40

Why this exists: the similarity scores separate different people cleanly and say nothing about which frame of
one person looks most like her. Tested against 23 frames an operator picked by eye, ArcFace scored AUC 0.44,
the per-region eye/cheek/mouth comparisons 0.42-0.44 and eye aperture 0.50 - all chance. Ranking is the wrong
shape of question to learn from: "I kept these 23" does not say what was rejected and why. A forced choice
between two frames of the same angle does, and it is the standard way to fit a preference.

The page is a plain local file with the images beside it. Nothing is uploaded, and the answers stay on the
machine until the operator saves them with the button - these are private character assets.

Pairs are drawn inside one yaw bucket so the comparison is fair, and biased towards pairs the current
measures rank *differently* from each other, which are the informative ones.
"""
from __future__ import annotations

import argparse
import json
import random
import shutil
from itertools import combinations
from pathlib import Path
from typing import Any

PAGE = """<!doctype html>
<meta charset="utf-8">
<title>{title}</title>
<style>
  :root {{ color-scheme: dark; --bg:#17150f; --fg:#f2ede3; --dim:#9c968a; --line:#332f26; }}
  body {{ background:var(--bg); color:var(--fg); font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;
         margin:0; padding:24px; }}
  header {{ max-width:1100px; margin:0 auto 18px; }}
  h1 {{ font-size:19px; margin:0 0 6px; }}
  p {{ color:var(--dim); margin:0; font-size:14px; }}
  .pair {{ max-width:1100px; margin:0 auto; display:grid; grid-template-columns:1fr 1fr; gap:18px; }}
  figure {{ margin:0; cursor:pointer; border:2px solid var(--line); border-radius:12px; overflow:hidden;
            transition:border-color .12s, transform .12s; background:#000; }}
  figure:hover {{ border-color:#c9a227; transform:translateY(-2px); }}
  img {{ display:block; width:100%; height:auto; }}
  figcaption {{ padding:8px 10px; font-size:12px; color:var(--dim); }}
  .bar {{ max-width:1100px; margin:18px auto 0; display:flex; gap:12px; align-items:center;
          justify-content:space-between; border-top:1px solid var(--line); padding-top:14px; }}
  button {{ background:#26221a; color:var(--fg); border:1px solid var(--line); border-radius:9px;
            padding:9px 14px; font:inherit; font-size:14px; cursor:pointer; }}
  button:hover {{ border-color:#c9a227; }}
  .done {{ max-width:1100px; margin:0 auto; text-align:center; padding:60px 0; }}
</style>
<header>
  <h1>{title}</h1>
  <p>같은 각도의 두 장 중 <strong>더 리아 같은 쪽</strong>을 누르세요. 판단이 어려우면 건너뛰세요.
     아무것도 업로드되지 않습니다. 끝나면 저장 버튼을 눌러 JSON을 내려받아 알려주세요.</p>
</header>
<div id="stage"></div>
<div class="bar">
  <span id="count"></span>
  <span>
    <button onclick="skip()">건너뛰기</button>
    <button onclick="save()">답변 저장</button>
  </span>
</div>
<script>
const PAIRS = {pairs};
let i = 0;
const answers = JSON.parse(localStorage.getItem({storage}) || "[]");
i = answers.length;

function render() {{
  const stage = document.getElementById("stage");
  document.getElementById("count").textContent = `${{Math.min(i + 1, PAIRS.length)}} / ${{PAIRS.length}}`;
  if (i >= PAIRS.length) {{
    stage.innerHTML = '<div class="done"><h1>끝났습니다</h1><p>아래 저장 버튼을 눌러주세요.</p></div>';
    return;
  }}
  const p = PAIRS[i];
  stage.innerHTML = '<div class="pair">' + [p.a, p.b].map((f, n) =>
    `<figure onclick="choose(${{n}})"><img src="images/${{f.file}}" alt="">` +
    `<figcaption>${{p.bucket}} · yaw ${{f.yaw.toFixed(2)}}</figcaption></figure>`).join("") + "</div>";
}}
function record(choice) {{
  answers.push({{pair: PAIRS[i].id, bucket: PAIRS[i].bucket, a: PAIRS[i].a.file, b: PAIRS[i].b.file,
                choice: choice}});
  localStorage.setItem({storage}, JSON.stringify(answers));
  i += 1; render();
}}
function choose(n) {{ record(n === 0 ? "a" : "b"); }}
function skip() {{ record("skip"); }}
function save() {{
  const blob = new Blob([JSON.stringify(answers, null, 1)], {{type: "application/json"}});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = {filename};
  a.click();
}}
render();
</script>
"""


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

    def disagreement(a: dict[str, Any], b: dict[str, Any]) -> float:
        """How differently the two current measures order this pair - the pairs worth spending a click on."""
        sa, sb = a["scores_vs_frontal_prototype"], b["scores_vs_frontal_prototype"]
        gaps = [abs((sa.get(name) or 0) - (sb.get(name) or 0)) for name in ("sface", "arcface")]
        return abs(gaps[0] - gaps[1]) + min(gaps)

    rng = random.Random(args.seed)
    candidates = []
    for bucket, members in by_bucket.items():
        pool = list(combinations(members, 2))
        rng.shuffle(pool)
        pool.sort(key=lambda pair: -disagreement(*pair))
        share = max(1, round(args.pairs * len(members) / len(manifest["members"])))
        candidates.extend((bucket, a, b) for a, b in pool[:share])
    rng.shuffle(candidates)
    candidates = candidates[:args.pairs]

    pairs = []
    for index, (bucket, a, b) in enumerate(candidates):
        for member in (a, b):
            target = images / member["file"]
            if not target.exists():
                shutil.copyfile(source / member["file"], target)
        first, second = (a, b) if rng.random() < 0.5 else (b, a)   # side must not encode anything
        pairs.append({"id": index, "bucket": bucket,
                      "a": {"file": first["file"], "yaw": first["yaw_proxy"]},
                      "b": {"file": second["file"], "yaw": second["yaw_proxy"]}})

    page = PAGE.format(title=args.title, pairs=json.dumps(pairs, ensure_ascii=False),
                       storage=json.dumps(f"pref-{manifest['character_id']}"),
                       filename=json.dumps(f"preference-{manifest['character_id']}.json"))
    (out_dir / "index.html").write_text(page, encoding="utf-8")
    (out_dir / "pairs.json").write_text(json.dumps(
        {"character_id": manifest["character_id"], "created_at": manifest["created_at"],
         "source_set": str(source), "pairs": pairs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"page": str(out_dir / "index.html"), "pairs": len(pairs),
            "buckets": sorted({p["bucket"] for p in pairs}), "images": len(list(images.iterdir()))}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--set", required=True, help="a directory holding identity-set.json")
    parser.add_argument("--out", required=True)
    parser.add_argument("--pairs", type=int, default=40)
    parser.add_argument("--seed", type=int, default=20260910)
    parser.add_argument("--title", default="어느 쪽이 더 리아 같나요?")
    return parser


def main() -> int:
    print(json.dumps(build(build_parser().parse_args()), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
