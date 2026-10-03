import json, subprocess, sys
from pathlib import Path
ROOT = Path(r"D:\codex\XAI-studio")
PANEL = sys.argv[1]
brief = Path(r"D:\codex\XAI-studio\characters\ch-shindo-noa\02_generations\SB-20260916-noa-reika-poolvilla-redesign\panel-briefs")
req = (brief / f"{PANEL}-request.txt").read_text(encoding="utf-8")
constraints = (brief / f"{PANEL}-constraints.json").read_text(encoding="utf-8")
scene = (brief / f"{PANEL}-scene.json").read_text(encoding="utf-8")
cmd = [
  sys.executable, str(ROOT / "tools" / "character_scene.py"), "produce",
  "--character", "ch-shindo-noa",
  "--request", req,
  "--count", "1",
  "--engines", "krea2",
  "--strategy", "strict_translation",
  "--constraints-json", constraints,
  "--scene-spec-json", scene,
  "--actor", "grok",
]
print("RUNNING", PANEL, flush=True)
proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
print(proc.stdout)
print(proc.stderr, file=sys.stderr)
sys.exit(proc.returncode)
