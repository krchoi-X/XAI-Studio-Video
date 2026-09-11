"""Faithful one-time registration of the user's imported DNA v1 documents."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools import character_manager as cm

UNSPECIFIED = 'Not specified in source DNA; unresolved, do not establish a new identity constraint'
DATA = {
    'jun': {
        'name': '준', 'romanized_name': 'Jun', 'age': 'adult man approximately 25–27 years old',
        'face': dict(shape='slightly elongated slim face with subtly prominent cheekbones and a relatively narrow lower face', eyes='sharp horizontally elongated narrow eyes with subtly lifted outer corners', eyebrows='straight defined eyebrows', nose='refined straight nose', lips='natural understated lips', jaw='clean refined jawline without exaggerated V-shape'),
        'body': dict(height_impression='tall, around 184–186 cm', limb_proportions='long-limbed, slender and flexible', shoulders='narrow-to-moderate, never bulky', torso='slender with subtle muscle tone and core strength, not heavily muscular', bust='not a bodybuilding chest; other details unspecified', waist='slim waist', pelvis_hips=UNSPECIFIED, lower_body='long-limbed slender flexible proportions', body_hair=UNSPECIFIED),
        'hair': 'black or very dark brown medium-long layered hair, natural side part or loose front strands around forehead and ears, never helmet-like',
        'marks': [], 'anchors': ['subtly prominent cheekbones', 'sharp elongated eyes with subtly lifted corners', 'slightly long slim face', 'dark medium-long layered hair silhouette', 'tall lean flexible proportions'],
        'scene': dict(expression='calm, thoughtful, observant, mildly serious; quiet amusement or ordinary confusion may vary by scene', gaze='calm analytical gaze', glasses='optional thin metal-frame glasses for reading, work or analysis; not a permanent identity marker', wardrobe='restrained tailoring at work; lightweight casual clothing at home; simple functional pilates or yoga wear'),
    },
    'rio': {
        'name': '리오', 'romanized_name': 'Rio', 'age': 'adult man approximately 21–23 years old',
        'face': dict(shape='youthful soft oval face of short-to-moderate length', eyes='calm warm eyes with neutral-to-gentle outer corners', eyebrows=UNSPECIFIED, nose='natural realistic nose; finer details unspecified', lips='natural realistic lips; finer details unspecified', jaw='smooth natural jawline, not sharply angular'),
        'body': dict(height_impression='moderate height, around 175–178 cm', limb_proportions='compact athletic proportions with toned arms and legs', shoulders='moderate, never oversized or extreme V-taper', torso='functional muscle and core strength with relatively low body fat, no bodybuilding bulk or exaggerated vascularity', bust='no bodybuilding chest or extreme muscle emphasis', waist='functional athletic core; exact waist shape unspecified', pelvis_hips=UNSPECIFIED, lower_body='toned athletic legs, strong balance and quick weight transfer', body_hair=UNSPECIFIED),
        'hair': 'short dark practical lightly textured hair with natural fringe or subtle forward texture',
        'marks': ['always wears exactly one small understated earring on one ear; side and shape unresolved until human reference approval'],
        'anchors': ['soft youthful oval facial structure', 'warm eyes with neutral-to-gentle outer corners', 'short dark textured hair silhouette', 'compact athletic proportions with moderate shoulders', 'small single earring'],
        'scene': dict(expression='relaxed friendly gentle and open; serious mode becomes still and neutral without altering facial structure', gaze='warm by default; quietly focused in serious mode', wardrobe='plain T-shirt, hoodie, sweatshirt or functional athletic clothes; suit only for special occasions'),
    },
}

for slug, data in DATA.items():
    if (ROOT / 'characters' / f'ch-{slug}' / 'character.json').exists():
        raise RuntimeError(f'ch-{slug} already exists; refuse overwrite')
    source = ROOT / 'docs' / 'characters' / f'{slug}.md'
    stamp = cm.now()
    record = dict(schema_version=1, id=f'ch-{slug}', name=data['name'], romanized_name=data['romanized_name'], status='draft', version=1,
        stable_dna=dict(adult_age_range=data['age'], visual_background='original adult East Asian man', face=data['face'], body=data['body'], hair=data['hair'], skin='realistic natural skin texture with small asymmetries; exact skin tone unspecified', distinctive_marks=data['marks'], recognition_anchors=data['anchors']),
        scene_defaults=data['scene'], approved_references=[], prompt_sources=[f'docs/characters/{slug}.md'], lora_associations=[], video_test_associations=[],
        provenance=dict(created_at=stamp, updated_at=stamp, created_by='codex', sources=[f'docs/characters/{slug}.md', f'https://github.com/krchoi-X/XAI-Studio-Private/blob/a9d4bbd2d9ae72641bea2e5539cc6822f2a1eef3/docs/characters/{slug}.md'], change_reason='User requested Studio registration of authored DNA v1; faithful mapping, unspecified fields remain unresolved'))
    draft = cm.save_draft(record, source.read_text(encoding='utf-8'))
    print(cm.promote(draft, False, 'Register user-authored DNA v1 in Studio'))
    assert cm.cmd_validate(f'ch-{slug}') == 0
