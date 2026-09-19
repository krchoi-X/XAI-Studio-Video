"""Where a local-model call goes, and what it looks like when it gets there."""
import importlib.util
import json
import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))
SPEC = importlib.util.spec_from_file_location("character_manager", TOOLS / "character_manager.py")
cm = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(cm)


class _Response:
    def __init__(self, payload):
        self._payload = payload

    def read(self):
        return json.dumps(self._payload).encode()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


class LocalModelRouterTests(unittest.TestCase):
    def setUp(self):
        self.sent = {}
        self._urlopen = cm.urllib.request.urlopen
        self._discover = cm.discover_gateway_key
        cm.discover_gateway_key = lambda base_url: None
        cm._DISCOVERED_KEY.clear()
        for name in (cm.HERMES_BASE_URL_ENV, cm.HERMES_API_KEY_ENV, cm.HERMES_MODEL_ENV):
            cm.os.environ.pop(name, None)

    def tearDown(self):
        cm.urllib.request.urlopen = self._urlopen
        cm.discover_gateway_key = self._discover
        cm._DISCOVERED_KEY.clear()
        for name in (cm.HERMES_BASE_URL_ENV, cm.HERMES_API_KEY_ENV, cm.HERMES_MODEL_ENV):
            cm.os.environ.pop(name, None)

    def _capture(self, payload):
        def fake(request, timeout=0):
            self.sent = {
                "url": request.full_url,
                "headers": {key.lower(): value for key, value in request.headers.items()},
                "body": json.loads(request.data.decode()),
                "timeout": timeout,
            }
            return _Response(payload)

        cm.urllib.request.urlopen = fake

    # ---------------------------------------------------------------- ollama
    def test_without_a_gateway_the_call_goes_to_ollama_exactly_as_before(self):
        self._capture({"message": {"content": json.dumps({"ok": True})}})
        result = cm.chat_json("compile this", "meromero26b", temperature=0.15, timeout=42)
        self.assertEqual(cm.active_chat_route(), "ollama")
        self.assertEqual(self.sent["url"], cm.OLLAMA_CHAT)
        self.assertEqual(self.sent["body"]["format"], "json")
        self.assertEqual(self.sent["body"]["options"]["temperature"], 0.15)
        self.assertEqual(self.sent["body"]["model"], "meromero26b")
        self.assertEqual(self.sent["timeout"], 42)
        self.assertNotIn("authorization", self.sent["headers"])
        self.assertEqual(result, {"ok": True})

    # ---------------------------------------------------------------- hermes
    def test_a_configured_gateway_takes_the_call_instead(self):
        cm.os.environ[cm.HERMES_BASE_URL_ENV] = "http://127.0.0.1:18434/v1/"
        cm.os.environ[cm.HERMES_API_KEY_ENV] = "test-key"
        self._capture({"choices": [{"message": {"content": json.dumps({"ok": True})}}]})
        result = cm.chat_json("compile this", "meromero26b", temperature=0.25, timeout=7)
        self.assertEqual(cm.active_chat_route(), "hermes")
        self.assertEqual(self.sent["url"], "http://127.0.0.1:18434/v1/chat/completions")
        self.assertEqual(self.sent["headers"]["authorization"], "Bearer test-key")
        self.assertEqual(self.sent["body"]["response_format"], {"type": "json_object"})
        self.assertEqual(self.sent["body"]["temperature"], 0.25)
        self.assertNotIn("format", self.sent["body"])
        self.assertEqual(result, {"ok": True})

    def test_the_gateway_model_can_be_named_separately_from_the_caller_s(self):
        cm.os.environ[cm.HERMES_BASE_URL_ENV] = "http://127.0.0.1:18434/v1"
        cm.os.environ[cm.HERMES_API_KEY_ENV] = "test-key"
        cm.os.environ[cm.HERMES_MODEL_ENV] = "Huihui-Qwen3.8-27B-abliterated-UD-DW-Q4_K_M"
        self._capture({"choices": [{"message": {"content": "{}"}}]})
        cm.chat_json("compile this", "meromero26b")
        self.assertEqual(self.sent["body"]["model"], "Huihui-Qwen3.8-27B-abliterated-UD-DW-Q4_K_M")

    # ------------------------------------------------------------ half-config
    def test_an_address_alone_is_enough_because_the_key_can_be_found(self):
        cm.os.environ[cm.HERMES_BASE_URL_ENV] = "http://127.0.0.1:18434/v1"
        cm._DISCOVERED_KEY.clear()
        cm.discover_gateway_key = lambda base_url: "found-key"
        self.assertEqual(cm.hermes_chat_config()[1], "found-key")

    def test_an_address_with_nothing_serving_it_is_not_a_gateway(self):
        cm.os.environ[cm.HERMES_BASE_URL_ENV] = "http://127.0.0.1:18434/v1"
        cm._DISCOVERED_KEY.clear()
        cm.discover_gateway_key = lambda base_url: None
        self.assertIsNone(cm.hermes_chat_config())
        self.assertEqual(cm.active_chat_route(), "ollama")

    def test_a_restarted_router_is_followed_rather_than_failing_the_call(self):
        """Hermes issues a new key on every launch and stores it nowhere."""
        cm.os.environ[cm.HERMES_BASE_URL_ENV] = "http://127.0.0.1:18434/v1"
        cm.os.environ[cm.HERMES_API_KEY_ENV] = "stale-key"
        cm._DISCOVERED_KEY.clear()
        cm.discover_gateway_key = lambda base_url: "fresh-key"
        seen = []

        def fake(request, timeout=0):
            seen.append(request.headers["Authorization"])
            if seen[-1].endswith("stale-key"):
                raise cm.urllib.error.HTTPError(request.full_url, 401, "Invalid API Key", {}, None)
            return _Response({"choices": [{"message": {"content": json.dumps({"ok": True})}}]})

        cm.urllib.request.urlopen = fake
        self.assertEqual(cm.chat_json("compile", "m"), {"ok": True})
        self.assertEqual(seen, ["Bearer stale-key", "Bearer fresh-key"])

    def test_a_key_that_is_simply_wrong_is_not_retried_forever(self):
        cm.os.environ[cm.HERMES_BASE_URL_ENV] = "http://127.0.0.1:18434/v1"
        cm.os.environ[cm.HERMES_API_KEY_ENV] = "stale-key"
        cm._DISCOVERED_KEY.clear()
        cm.discover_gateway_key = lambda base_url: "stale-key"

        def fake(request, timeout=0):
            raise cm.urllib.error.HTTPError(request.full_url, 401, "Invalid API Key", {}, None)

        cm.urllib.request.urlopen = fake
        with self.assertRaises(cm.urllib.error.HTTPError):
            cm.chat_json("compile", "m")

    def test_a_key_without_an_address_is_not_a_gateway(self):
        cm.os.environ[cm.HERMES_API_KEY_ENV] = "test-key"
        self.assertIsNone(cm.hermes_chat_config())
        self.assertEqual(cm.active_chat_route(), "ollama")

    def test_a_blank_setting_counts_as_unset_rather_than_as_a_gateway(self):
        cm.os.environ[cm.HERMES_BASE_URL_ENV] = "   "
        cm.os.environ[cm.HERMES_API_KEY_ENV] = "test-key"
        self.assertEqual(cm.active_chat_route(), "ollama")

    # -------------------------------------------------------------- callers
    def test_every_tool_asks_the_router_rather_than_a_hardcoded_address(self):
        """The unload path stays Ollama-specific on purpose; it unloads Ollama."""
        routed = ("character_scene.py", "dna_proposal_worker.py", "idea_production_worker.py")
        for name in routed:
            source = (TOOLS / name).read_text(encoding="utf-8")
            self.assertNotIn("11434", source, name)
            self.assertIn("chat_json(", source, name)
        manager = (TOOLS / "character_manager.py").read_text(encoding="utf-8")
        endpoints = {"OLLAMA_CHAT", "OLLAMA_PS", "OLLAMA_GENERATE"}
        named = {line.split("=")[0].strip() for line in manager.splitlines() if "11434" in line}
        self.assertEqual(named, endpoints, "the router owns every Ollama address")


if __name__ == "__main__":
    unittest.main()


class FreeVramTests(unittest.TestCase):
    """A render starts seconds after the compile, while the model that compiled is warm."""

    def setUp(self):
        self._urlopen = cm.urllib.request.urlopen

    def tearDown(self):
        cm.urllib.request.urlopen = self._urlopen

    def test_every_resident_model_is_asked_to_leave(self):
        asked = []

        def fake(request, timeout=0):
            # The listing is fetched by URL; the unloads are posted as Request objects.
            if isinstance(request, str):
                return _Response({"models": [{"name": "meromero26b"}, {"name": "other"}]})
            asked.append(json.loads(request.data.decode()))
            return _Response({})

        cm.urllib.request.urlopen = fake
        message = cm.free_local_model_vram()
        self.assertEqual([item["model"] for item in asked], ["meromero26b", "other"])
        self.assertTrue(all(item["keep_alive"] == 0 for item in asked))
        self.assertIn("meromero26b", message)

    def test_an_empty_card_is_reported_rather_than_poked(self):
        def fake(request, timeout=0):
            self.assertEqual(request, cm.OLLAMA_PS)
            return _Response({"models": []})

        cm.urllib.request.urlopen = fake
        self.assertEqual(cm.free_local_model_vram(), "nothing loaded")

    def test_no_ollama_is_not_an_error(self):
        def fake(request, timeout=0):
            raise OSError("connection refused")

        cm.urllib.request.urlopen = fake
        self.assertEqual(cm.free_local_model_vram(), "ollama not reachable")

    def test_the_render_path_frees_vram_before_it_submits(self):
        source = (TOOLS / "character_scene.py").read_text(encoding="utf-8")
        submit = source[source.index("def submit("):]
        self.assertLess(submit.index("free_local_model_vram"), submit.index("batch.yaml"))
