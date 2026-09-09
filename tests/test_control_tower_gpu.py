import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from control_tower import gpu  # noqa: E402


GPU_ROW = "0, NVIDIA GeForce RTX 4070 Laptop GPU, 610.88, 96 %, 41 %, 7412 MiB, 8188 MiB, 72, 78.51 W, [N/A], 2475 MHz, P0\n"
APPS = (
    "GPU-abc, 28141, D:\\AI\\WanGP\\env_uv\\Scripts\\python.exe, [N/A]\n"
    "GPU-abc, 27584, C:\\Program Files\\WindowsApps\\OpenAI.Codex_1\\app\\ChatGPT.exe, 120 MiB\n"
)


class ParseTests(unittest.TestCase):
    def test_parse_gpu_row(self):
        samples = gpu.parse_gpu_csv(GPU_ROW)
        self.assertEqual(len(samples), 1)
        s = samples[0]
        self.assertEqual(s.name, "NVIDIA GeForce RTX 4070 Laptop GPU")
        self.assertEqual(s.utilization_percent, 96.0)
        self.assertEqual(s.memory_used_mib, 7412.0)
        self.assertEqual(s.memory_total_mib, 8188.0)
        self.assertEqual(s.temperature_c, 72.0)
        self.assertAlmostEqual(s.power_draw_w, 78.51)
        self.assertIsNone(s.power_limit_w, "[N/A] must become None, never 0")
        self.assertEqual(s.sm_clock_mhz, 2475.0)
        self.assertEqual(s.pstate, "P0")

    def test_parse_apps(self):
        procs = gpu.parse_apps_csv(APPS)
        self.assertEqual([p.pid for p in procs], [28141, 27584])
        self.assertTrue(procs[0].name.endswith("python.exe"))
        self.assertIsNone(procs[0].used_memory_mib)
        self.assertEqual(procs[1].used_memory_mib, 120.0)

    def test_empty_and_garbage(self):
        self.assertEqual(gpu.parse_gpu_csv(""), [])
        self.assertEqual(gpu.parse_gpu_csv("No devices were found"), [])
        self.assertEqual(gpu.parse_apps_csv("garbage"), [])


class CollectorTests(unittest.TestCase):
    def test_missing_executable_reports_error_not_zeros(self):
        collector = gpu.NvidiaSmiCollector(executable="definitely-not-a-real-nvidia-smi-binary")
        sample = collector.sample()
        self.assertFalse(sample.ok)
        self.assertEqual(sample.gpus, [])
        self.assertIn("not found", sample.error)

    def test_sample_attaches_processes(self):
        collector = gpu.NvidiaSmiCollector()
        outputs = {"--query-gpu": GPU_ROW, "--query-compute-apps": APPS}

        def fake_run(args):
            for key, value in outputs.items():
                if args[0].startswith(key):
                    return value
            raise AssertionError(args)

        collector._run = fake_run  # type: ignore[assignment]
        sample = collector.sample()
        self.assertTrue(sample.ok)
        self.assertEqual(len(sample.gpus[0].processes), 2)
        d = sample.to_dict()
        self.assertEqual(d["gpus"][0]["processes"][0]["pid"], 28141)




class TailscaleServeParsingTests(unittest.TestCase):
    """The Open Gallery link must point at the tailnet when the dashboard is opened from a tablet."""

    SERVE_STATUS = (
        "https://artxorn.tailf10079.ts.net (tailnet only)\n"
        "|-- / proxy http://127.0.0.1:8787\n"
        "\n"
        "https://artxorn.tailf10079.ts.net:8443 (tailnet only)\n"
        "|-- / proxy http://127.0.0.1:8800\n"
        "\n"
        "https://artxorn.tailf10079.ts.net:8790 (tailnet only)\n"
        "|-- / proxy http://127.0.0.1:8790\n"
    )

    def test_finds_the_origin_serving_a_local_port(self):
        from control_tower.tailscale import parse_serve_status

        self.assertEqual(parse_serve_status(self.SERVE_STATUS, 8787), "https://artxorn.tailf10079.ts.net/")
        self.assertEqual(parse_serve_status(self.SERVE_STATUS, 8800), "https://artxorn.tailf10079.ts.net:8443/")
        self.assertEqual(parse_serve_status(self.SERVE_STATUS, 8790), "https://artxorn.tailf10079.ts.net:8790/")

    def test_unserved_port_and_junk_return_none(self):
        from control_tower.tailscale import parse_serve_status

        self.assertIsNone(parse_serve_status(self.SERVE_STATUS, 9999))
        self.assertIsNone(parse_serve_status("", 8787))
        self.assertIsNone(parse_serve_status("No serve config", 8787))

    def test_a_port_that_only_matches_as_a_suffix_is_not_accepted(self):
        from control_tower.tailscale import parse_serve_status

        status = "https://host.ts.net (tailnet only)\n|-- / proxy http://127.0.0.1:18787\n"
        self.assertIsNone(parse_serve_status(status, 8787))

    def test_missing_tailscale_cli_is_not_an_error(self):
        from control_tower.tailscale import detect_served_url

        self.assertIsNone(detect_served_url(8787, executable="definitely-not-tailscale"))


if __name__ == "__main__":
    unittest.main()
