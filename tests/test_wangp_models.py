import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import wangp_models  # noqa: E402


def write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def touch(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"weights")


class ModelSurveyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        base = "https://example/repo/resolve/main/"
        write(self.root / "defaults" / "base.json", {
            "model": {"name": "Base", "URLs": [base + "base_bf16.safetensors", base + "base_int8.safetensors"]},
            "num_inference_steps": 8, "guidance_scale": 0})
        # borrows the base weights and adds a LoRA
        write(self.root / "defaults" / "base_edit.json", {
            "model": {"name": "Base Edit", "URLs": "base", "loras": [base + "edit_v1.safetensors"]},
            "num_inference_steps": 20, "guidance_scale": 2})
        # borrows the base weights but needs a ControlNet module
        write(self.root / "defaults" / "base_control.json", {
            "model": {"name": "Base Control", "URLs": "base",
                      "modules": [[base + "control_bf16.safetensors", base + "control_int8.safetensors"]]}})
        write(self.root / "defaults" / "absent.json", {"model": {"name": "Absent", "URLs": [base + "absent.safetensors"]}})
        write(self.root / "finetunes" / "base_local.json", {
            "model": {"name": "Local finetune", "URLs": [str(self.root / "local" / "finetune.safetensors")]},
            "num_inference_steps": 8})
        touch(self.root / "ckpts" / "base_int8.safetensors")
        touch(self.root / "loras" / "family" / "edit_v1.safetensors")
        touch(self.root / "local" / "finetune.safetensors")
        self.rows = {r["model_type"]: r for r in wangp_models.survey(self.root)}

    def tearDown(self):
        self.tmp.cleanup()

    def test_installed_when_any_alternative_is_present(self):
        self.assertEqual(self.rows["base"]["status"], "usable")
        self.assertTrue(self.rows["base"]["weights"].endswith("base_int8.safetensors"))

    def test_borrowed_weights_and_present_lora_are_usable(self):
        self.assertEqual(self.rows["base_edit"]["status"], "usable")
        self.assertEqual(self.rows["base_edit"]["num_inference_steps"], 20)

    def test_missing_module_makes_a_variant_unusable(self):
        row = self.rows["base_control"]
        self.assertEqual(row["status"], "unusable")
        self.assertEqual(row["missing"], ["module:control_bf16.safetensors"])

    def test_absent_weights_are_reported(self):
        self.assertEqual(self.rows["absent"]["status"], "unusable")
        self.assertEqual(self.rows["absent"]["missing"], ["weights"])

    def test_finetune_with_an_absolute_local_path(self):
        self.assertEqual(self.rows["base_local"]["status"], "usable")
        self.assertEqual(self.rows["base_local"]["origin"], "finetune")

    def test_missing_lora_makes_it_unusable(self):
        (self.root / "loras" / "family" / "edit_v1.safetensors").unlink()
        rows = {r["model_type"]: r for r in wangp_models.survey(self.root)}
        self.assertEqual(rows["base_edit"]["missing"], ["lora:edit_v1.safetensors"])

    def test_check_exit_codes(self):
        args = ["--wangp-root", str(self.root), "--check"]
        self.assertEqual(wangp_models.main(args + ["base"]), 0)
        self.assertEqual(wangp_models.main(args + ["base_control"]), 2, "defined but unusable is not a pass")
        self.assertEqual(wangp_models.main(args + ["base_typo"]), 2, "unknown id must fail")

    def test_write_produces_a_generated_reference(self):
        out = self.root / "doc.md"
        self.assertEqual(wangp_models.main(["--wangp-root", str(self.root), "--write", str(out)]), 0)
        text = out.read_text(encoding="utf-8")
        self.assertIn("Generated file — do not edit by hand", text)
        self.assertIn("`base_edit`", text)
        self.assertIn("module:control_bf16.safetensors", text)

    def test_variant_detection_uses_underscore_boundaries(self):
        installed = {"z_image", "minimax_h3_ref2va_pruned", "flux_chroma"}
        self.assertTrue(wangp_models.is_variant_of("z_image_control2_1", installed), "extends an installed id")
        self.assertTrue(wangp_models.is_variant_of("minimax_h3_ref2va", installed), "installed id extends it")
        self.assertTrue(wangp_models.is_variant_of("flux_chroma_radiance", installed))
        self.assertFalse(wangp_models.is_variant_of("z_imagex", installed), "must not match mid-token")
        self.assertFalse(wangp_models.is_variant_of("wan2_2_text2video", installed))
        self.assertFalse(wangp_models.is_variant_of("z_image", installed), "an installed id is not its own variant")


if __name__ == "__main__":
    unittest.main()
