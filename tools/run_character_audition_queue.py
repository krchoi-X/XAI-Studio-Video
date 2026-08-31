from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PYTHON = Path(sys.executable)
RUNNER = REPO / "tools" / "local_wangp.py"
EXPERIMENTS = REPO / "examples" / "character-lab" / "experiments"
BATCHES = sorted(EXPERIMENTS.glob("BATCH-00[3-7]-*-upper-body-audition"))


def submit(root: Path, engine: str, settings_name: str) -> None:
    command = [
        str(PYTHON), str(RUNNER), "submit",
        "--runs-root", str(root / "runs"),
        "--prompt-file", str(root / "prompt.txt"),
        "--settings-file", str(root / settings_name),
        "--project-id", root.name,
        "--prompt-id", f"{root.name}-v1",
        "--output-dir", str(root / "outputs" / engine),
    ]
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", check=True)
    submitted = json.loads(result.stdout)
    run_dir = Path(submitted["run_dir"])
    expected = 10
    while True:
        record = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
        if record.get("status") == "failed":
            raise RuntimeError(f"{root.name}/{engine} failed: {record.get('error')}")
        if len(record.get("artifacts") or []) >= expected:
            print(f"completed {root.name}/{engine}", flush=True)
            return
        time.sleep(10)


def main() -> None:
    if len(BATCHES) != 5:
        raise RuntimeError(f"Expected five audition batches, found {len(BATCHES)}")
    for root in BATCHES:
        submit(root, "z-image", "z-image.settings.json")
        submit(root, "krea2", "krea2.settings.json")


if __name__ == "__main__":
    main()
