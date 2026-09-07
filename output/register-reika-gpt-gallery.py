"""Register existing GPT outputs using Studio's existing batch import contract."""
import json
import hashlib
import shutil
from pathlib import Path

repo = Path('D:/codex/XAI-studio')
library = Path('D:/AI_Studio/library/characters/ch-mizuki-reika/generations')
base = repo / 'output/reika-gpt-candidates-20260906'
study = repo / 'output/reika-gpt-expression-study-20260906'
source_manifest = json.loads((study / 'manifest.json').read_text(encoding='utf-8'))
groups = [('GPT-20260906-reika-base-candidates', '레이카 · GPT 기본 얼굴 후보 10장', [(p, (base / 'prompt.txt').read_text(encoding='utf-8'), None) for p in sorted(base.glob('reika-gpt-*.png'))])]
for face in ('06', '09'):
    for scene, label in [('editorial', '검은 재킷 화보'), ('smile', '환하게 웃는 일상')]:
        items = [(study / x['file'], x['prompt'], str(base / f'reika-gpt-{face}.png')) for x in source_manifest['images'] if x['face'] == face and x['scene'] == scene]
        groups.append((f'GPT-20260906-reika-face-{face}-{scene}', f'레이카 · GPT {face}번 · {label} 3장', items))
for session_id, title, items in groups:
    records = repo / 'characters/ch-mizuki-reika/02_generations' / session_id
    outputs = library / session_id / 'outputs/gpt'
    outputs.mkdir(parents=True, exist_ok=True)
    records.mkdir(parents=True, exist_ok=True)
    provenance = []
    for source, prompt, reference in items:
        target = outputs / source.name
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        if target.exists():
            assert hashlib.sha256(target.read_bytes()).hexdigest() == digest, target
        else:
            shutil.copy2(source, target)
        provenance.append({'file': source.name, 'original_path': str(source), 'sha256': digest, 'prompt': prompt, 'reference_image': reference})
    manifest = {'schema_version': 1, 'session': {'id': session_id, 'character_id': 'ch-mizuki-reika', 'title': title, 'status': 'completed', 'visibility': 'standard', 'asset_root': str(outputs.parent), 'prompt_file': 'prompt.txt'}, 'jobs': [{'backend': 'openai', 'provider': 'OpenAI', 'model': 'GPT built-in image generation', 'count': len(items), 'output_dir': 'outputs/gpt', 'status': 'completed'}], 'review': {'initial_state': 'needs_review'}}
    (records / 'batch.yaml').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    (records / 'prompt.txt').write_text('\n\n'.join(f'{x[0].name}\n{x[1]}' for x in items), encoding='utf-8')
    (records / 'import-provenance.json').write_text(json.dumps(provenance, ensure_ascii=False, indent=2), encoding='utf-8')
    print(session_id, len(items))
