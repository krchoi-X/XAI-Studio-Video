from __future__ import annotations

import json
import re
from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parents[1]
KNOWLEDGE = Path(r"D:\codex\personal-ai-knowledge\creative-studio\projects\character-library")
EXPERIMENTS = REPO / "examples" / "character-lab" / "experiments"

CHARACTERS = [
    ("ch-han-seorin", "한서린", "Han Seorin", 3),
    ("ch-lee-suan", "이수안", "Lee Suan", 4),
    ("ch-mizuno-aoi", "미즈노 아오이", "Mizuno Aoi", 5),
    ("ch-oh-jian", "오지안", "Oh Ji-an", 6),
    ("ch-yuna", "유나", "Yuna", 7),
]

OVERRIDE = """

Create a standardized photorealistic upper-body character audition portrait. Show one young adult woman alone, framed from approximately the waist or upper hips to above the head, with both shoulders and the complete hairstyle visible. She faces the camera directly or at a restrained three-quarter angle with a calm neutral expression or an almost imperceptible smile. Preserve the character-specific face, hair, skin, and recognition anchors above.

Use a clean seamless soft-white studio background, bright soft even artificial lighting, gentle dimensional shadows around the eyes, nose, jawline, neck, and collarbones, and a realistic full-frame 70-85mm portrait-photography look. Wardrobe is a simple modest sleeveless or short-sleeved knit top in white, cream, or very pale gray. Natural skin pores, believable eye reflections, individual hair strands, subtle natural asymmetry, and minimal beauty retouching. Premium editorial casting-test photograph intended to decide whether this visual character should continue into development.

Avoid: extra people, cropped crown or missing hairstyle, hands prominently covering the face, wide-angle distortion, warped anatomy, malformed eyes, mismatched gaze, plastic skin, excessive smoothing, heavy makeup, flashy glamour styling, jewelry as a dominant feature, props, clutter, text, logos, and watermarks.
""".strip()


def source_prompt(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^## Source prompt\s*$\n(.*?)(?=^## Editable overrides\s*$)", text, re.MULTILINE | re.DOTALL)
    if not match:
        raise ValueError(f"Source prompt section not found: {path}")
    return match.group(1).strip()


def main() -> None:
    for character_id, korean_name, romanized_name, batch_number in CHARACTERS:
        root = EXPERIMENTS / f"BATCH-00{batch_number}-{character_id.removeprefix('ch-')}-upper-body-audition"
        root.mkdir(parents=True, exist_ok=True)
        prompt_source = KNOWLEDGE / "production" / "prompt-modules" / character_id / "appearance-base.md"
        prompt = source_prompt(prompt_source) + "\n\n" + OVERRIDE + "\n"
        (root / "prompt.txt").write_text(prompt, encoding="utf-8")
        common = {
            "settings_version": 2.73,
            "image_mode": 1,
            "resolution": "768x1024",
            "num_inference_steps": 8,
            "batch_size": 10,
            "repeat_generation": 1,
            "activated_loras": [],
            "loras_multipliers": "",
            "image_quality": "jpeg_95",
            "NAG_scale": 1,
            "NAG_tau": 3.5,
            "NAG_alpha": 0.5,
        }
        z_settings = common | {
            "model_type": "z_image",
            "model_filename": "https://huggingface.co/DeepBeepMeep/Z-Image/resolve/main/ZImageTurbo_quanto_bf16_int8.safetensors",
            "seed": 830202600 + batch_number * 10 + 1,
            "type": "Z Image Turbo",
        }
        krea_settings = common | {
            "model_type": "krea2_turbo_moody_krea",
            "base_model_type": "krea2_turbo",
            "model_filename": r"D:\AI\Models\image-generation\krea2\moodyKrea2Mix_v70_INT8.safetensors",
            "seed": 830202600 + batch_number * 10 + 2,
            "type": "Moody Krea 2 V7 INT8",
        }
        (root / "z-image.settings.json").write_text(json.dumps(z_settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (root / "krea2.settings.json").write_text(json.dumps(krea_settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        manifest = {
            "schema_version": 1,
            "session": {
                "id": root.name,
                "character_id": character_id,
                "character_name": korean_name,
                "romanized_name": romanized_name,
                "title": f"{romanized_name} Upper-Body Character Audition",
                "status": "running",
                "prompt_file": "prompt.txt",
                "source_prompt": str(prompt_source),
            },
            "jobs": [
                {"backend": "local-wangp", "model": "z_image", "count": 10, "seed": z_settings["seed"], "resolution": "768x1024", "steps": 8, "settings_file": "z-image.settings.json", "output_dir": "outputs/z-image", "status": "queued"},
                {"backend": "local-wangp", "model": "krea2_turbo_moody_krea", "count": 10, "seed": krea_settings["seed"], "resolution": "768x1024", "steps": 8, "settings_file": "krea2.settings.json", "output_dir": "outputs/krea2", "status": "queued"},
                {"backend": "codex-imagegen", "model": "gpt-image", "count": 10, "seed": None, "prompt_file": "prompt.txt", "output_dir": "outputs/gpt-image", "status": "queued"},
            ],
            "review": {"surface": "personal-prompt-studio", "initial_state": "needs_review"},
        }
        (root / "batch.yaml").write_text(yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False), encoding="utf-8")
        for engine in ("z-image", "krea2", "gpt-image"):
            (root / "outputs" / engine).mkdir(parents=True, exist_ok=True)
        print(root)


if __name__ == "__main__":
    main()
