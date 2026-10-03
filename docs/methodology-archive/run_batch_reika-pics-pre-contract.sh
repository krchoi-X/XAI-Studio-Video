#!/bin/bash
# Historical pre-contract helper retained for provenance only.
# Do not run: it predates the intent-preserving-v1 contract gate and its
# submissions are intentionally rejected by the current local_wangp CLI.
echo "Archived pre-contract helper; use the intent-preserving workflow." >&2
exit 2

# Original helper follows for auditability.
# shellcheck disable=SC2317
submit_scene() {
  local session_name=$1
  local title=$2
  local request=$3
  local prompt_rel_path="characters/ch-mizuki-reika/02_generations/$session_name/prompt.txt"
  local settings_rel_path="characters/ch-mizuki-reika/02_generations/$session_name/settings.json"
  local session_dir="characters/ch-mizuki-reika/02_generations/$session_name"
  local output_dir="D:/AI_Studio/library/characters/ch-mizuki-reika/videos/${session_name,,}"

  echo "Submitting $title..."
  # Record session first using wangp_recorder.py
  python tools/wangp_recorder.py session --session-dir "$session_dir" --requested-by hermes --engine WanGP --model krea2_turbo_moody_krea --character-id ch-mizuki-reika --title "$title" --user-request "$request" --status running && \
  # Submit run using local_wangp.py
  python tools/local_wangp.py submit --runs-root "$session_dir/runs" \
    --prompt-file "$prompt_rel_path" \
    --settings-file "$settings_rel_path" \
    --project-id "$session_name" --prompt-id shot-01 \
    --output-dir "$output_dir" --requested-by hermes
}

# Execute each scenario one after another to prevent GPU lock contention
submit_scene "SCENE_DRESS_STUDIO" "Reika Dress Studio" "Batch dress studio"
submit_scene "SCENE_DRESS_GARDEN" "Reika Dress Garden" "Batch dress garden"
submit_scene "SCENE_LINGERIE_STUDIO" "Reika Lingerie Studio" "Batch lingerie studio"
submit_scene "SCENE_BIKINI_GARDEN" "Reika Bikini Garden" "Batch bikini garden"
submit_scene "SCENE_NUDE_STUDIO" "Reika Nude Studio" "Batch nude studio"
