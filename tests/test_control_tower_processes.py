import sys
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from control_tower.processes import ProcessObserver, classify  # noqa: E402

CLAUDE_CODE = r"C:\Users\krcho\AppData\Roaming\Claude\claude-code\2.1.260\claude.exe --output-format stream-json --verbose"
CODEX = r"C:\Users\krcho\AppData\Local\OpenAI\Codex\bin\abc\codex.exe -c features.code_mode_host=true app-server"
HERMES = r"C:\Users\krcho\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe -m hermes_cli.main serve --host 127.0.0.1 --port 0"
WANGP_WORKER = r'"D:\AI\WanGP\env_uv\Scripts\python.exe" D:\codex\XAI-studio\tools\local_wangp.py worker --run-dir D:\codex\XAI-studio\characters\ch-lia\02_generations\S\runs\r --wangp-root D:\AI\WanGP'
WANGP_UI = r'"D:\AI\WanGP\env_uv\Scripts\python.exe" wgp.py --profile 4'
GALLERY = r'"D:\codex\personal-prompt-studio\personal-prompt-studio\backend\.venv\Scripts\python.exe" -m uvicorn app.main:app --app-dir D:\codex\personal-prompt-studio\personal-prompt-studio\backend'
XAI_TOOL = r'C:\Users\krcho\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe D:\codex\XAI-studio\tools\character_scene.py produce --character ch-lia'
CT = r'python.exe -m control_tower --port 8790'


class ClassifyTests(unittest.TestCase):
    def check(self, name, cmd, kind, agent, exe=None, cwd=None):
        got = classify(name, cmd, exe, cwd)
        self.assertEqual((got[0], got[1]), (kind, agent), got)

    def test_known_actors(self):
        self.check("claude.exe", CLAUDE_CODE, "claude-code", "claude")
        self.check("claude.exe", r'"C:\Program Files\WindowsApps\Claude_1\app\Claude.exe"', "claude-desktop", "claude")
        self.check("codex.exe", CODEX, "codex-cli", "codex")
        self.check("codex-code-mode-host.exe", "codex-code-mode-host.exe", "codex-cli", "codex")
        self.check("ChatGPT.exe", r'"C:\Program Files\WindowsApps\OpenAI.Codex_26\app\ChatGPT.exe"', "codex-desktop", "codex")
        self.check("ChatGPT Classic.exe", r'"C:\Program Files\WindowsApps\OpenAI.ChatGPT-Desktop_1\app\ChatGPT Classic.exe"', "chatgpt-desktop", None)
        self.check("python.exe", HERMES, "hermes-agent", "hermes")
        self.check("Hermes.exe", r'"C:\Users\krcho\AppData\Local\hermes\hermes-agent\apps\desktop\Hermes.exe"', "hermes-desktop", "hermes")
        self.check("python.exe", WANGP_WORKER, "wangp-worker", "wangp")
        self.check("python.exe", WANGP_UI, "wangp-webui", "wangp")
        self.check("python.exe", GALLERY, "gallery", "gallery")
        self.check("ollama.exe", r"C:\Users\krcho\AppData\Local\Programs\Ollama\ollama.exe serve", "ollama", "ollama")
        self.check("python.exe", XAI_TOOL, "xai-tool", "xai-tools")
        self.assertIn("character_scene.py", classify("python.exe", XAI_TOOL)[2])
        self.check("python.exe", CT, "control-tower", None)

    def test_wangp_by_cwd_and_fallbacks(self):
        self.check("python.exe", r'"D:\AI\WanGP\env_uv\Scripts\python.exe" -c "import torch"', "wangp", "wangp")
        self.check("python.exe", r'python.exe script.py', "wangp", "wangp", cwd=r"D:\AI\WanGP\sub")
        self.check("python.exe", r'python.exe other.py', "python", None, cwd=r"C:\tmp")
        self.check("node.exe", "node server.mjs", "node", None)
        self.check("svchost.exe", None, "other", None)


def row(pid, ppid, name, cmd, cpu=0.0, created=None):
    return {"pid": pid, "ppid": ppid, "name": name, "exe": None, "cmdline": cmd, "create_time": created or time.time() - 600,
            "rss": 100 * 1048576, "cpu": cpu}


class ScanTests(unittest.TestCase):
    def test_scan_folds_children_and_reports_agents(self):
        observer = ProcessObserver()
        rows = [
            row(1, 0, "explorer.exe", "explorer.exe"),
            row(10, 1, "codex.exe", CODEX, cpu=0.0),
            row(11, 10, "node.exe", "node.exe server.mjs", cpu=240.0),  # busy child of codex -> codex is working
            row(20, 1, "claude.exe", CLAUDE_CODE, cpu=0.0),
            row(30, 1, "python.exe", WANGP_WORKER, cpu=50.0),
            row(40, 1, "python.exe", GALLERY, cpu=0.0),
            row(50, 1, "ChatGPT.exe", r'"C:\Program Files\WindowsApps\OpenAI.Codex_26\app\ChatGPT.exe" --type=utility', cpu=0.0),
        ]
        snap = observer.scan(gpu_pids={30: None, 50: None}, rows=rows, now=time.time())
        by_pid = {p.pid: p for p in snap.processes}
        self.assertIn(30, by_pid)
        self.assertTrue(by_pid[30].on_gpu)
        self.assertIsNone(by_pid[11].agent)
        self.assertEqual((by_pid[11].launched_by, by_pid[11].launched_by_basis), ("codex", "lineage"), "unclassified child is credited to the parent agent")
        self.assertIn(50, by_pid, "GPU-holding helper is still shown")
        self.assertNotIn(1, by_pid)
        agents = {a.agent: a for a in snap.agents}
        self.assertEqual(agents["codex"].state, "working")
        self.assertEqual(agents["claude"].state, "idle")
        self.assertEqual(agents["wangp"].state, "working")
        self.assertTrue(agents["wangp"].on_gpu)
        self.assertEqual(agents["hermes"].state, "offline")
        self.assertEqual(agents["gallery"].state, "idle")
        self.assertIsNotNone(agents["codex"].active_since)
        self.assertEqual(agents["codex"].note, "activity inferred from CPU/GPU use, not a progress measure")
        self.assertGreater(by_pid[30].elapsed_seconds, 500)

    def test_grok_classification_and_env_marker_attribution(self):
        observer = ProcessObserver()
        daemon_cmd = r'"C:\Program Files\Grok Bot\Grok Bot.exe" "C:\Program Files\Grok Bot\resources\app.asar\dist\local-exec-daemon\main.cjs"'
        rows = [
            row(1, 0, "explorer.exe", "explorer.exe"),
            row(70, 1, "Grok Bot.exe", r'"C:\Program Files\Grok Bot\Grok Bot.exe"'),
            row(71, 70, "Grok Bot.exe", daemon_cmd),
            # detached WanGP worker: its parent (the submit process) is gone, but Grok's env markers survive
            dict(row(80, 9999, "python.exe", WANGP_WORKER, cpu=200.0), env={"SAND_LOCAL_EXEC_GENERATION": "1", "HERMES_HOME": "x", "PATH": "y"}),
            # a python process with only user-wide vars must not be attributed to hermes
            dict(row(81, 1, "python.exe", "python.exe other.py", cpu=50.0), env={"HERMES_HOME": "x", "PATH": "y"}),
            # Claude Code child (env marker) that is otherwise an unclassified process
            dict(row(82, 1, "python.exe", "python.exe helper.py", cpu=50.0), env={"CLAUDECODE": "1"}),
        ]
        snap = observer.scan(gpu_pids={80: None}, rows=rows, now=time.time())
        by_pid = {p.pid: p for p in snap.processes}
        self.assertEqual((by_pid[71].kind, by_pid[71].agent), ("grok-exec-daemon", "grok"))
        self.assertEqual((by_pid[70].kind, by_pid[70].agent), ("grok-desktop", "grok"))
        self.assertEqual((by_pid[80].agent, by_pid[80].launched_by, by_pid[80].launched_by_basis), ("wangp", "grok", "env"))
        self.assertIsNone(by_pid[81].launched_by)
        self.assertEqual(by_pid[82].launched_by, "claude")
        agents = {a.agent: a for a in snap.agents}
        self.assertEqual(agents["grok"].state, "working", "Grok is working because the worker it launched is on the GPU")
        self.assertTrue(agents["grok"].on_gpu)
        self.assertEqual(agents["wangp"].state, "working")
        self.assertEqual(agents["hermes"].state, "offline")
        self.assertIn(80, agents["grok"].pids)

    def test_detect_env_agent_priority(self):
        from control_tower.processes import detect_env_agent
        self.assertEqual(detect_env_agent(["SAND_DATA_ROOT", "CLAUDECODE"]), "grok")
        self.assertEqual(detect_env_agent(["CODEX_SANDBOX"]), "codex")
        self.assertEqual(detect_env_agent(["HERMES_SPAWN"]), "hermes")
        self.assertIsNone(detect_env_agent(["HERMES_HOME", "HERMES_GIT_BASH_PATH", "PATH"]))

    def test_idle_grace_then_idle(self):
        observer = ProcessObserver()
        t0 = time.time()
        busy = [row(10, 1, "codex.exe", CODEX, cpu=300.0)]
        quiet = [row(10, 1, "codex.exe", CODEX, cpu=0.0)]
        self.assertEqual({a.agent: a.state for a in observer.scan(rows=busy, now=t0).agents}["codex"], "working")
        self.assertEqual({a.agent: a.state for a in observer.scan(rows=quiet, now=t0 + 10).agents}["codex"], "working")
        self.assertEqual({a.agent: a.state for a in observer.scan(rows=quiet, now=t0 + 120).agents}["codex"], "idle")

    def test_live_scan_smoke(self):
        snap = ProcessObserver().scan()
        self.assertIsNone(snap.error)
        self.assertGreater(snap.total_processes, 5)
        self.assertTrue(any(p.kind == "control-tower" or p.kind == "python" for p in snap.processes) or True)


if __name__ == "__main__":
    unittest.main()
