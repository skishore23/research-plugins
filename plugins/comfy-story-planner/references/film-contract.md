# Film contract
The original FilmPlan validator checks unique shot IDs, exact summed duration, cast presence/absence conflicts, earlier dependencies, state preconditions, cue bounds and declared languages. The wrapper additionally reports 24 fps alignment and the 15-second per-shot rendering limit. It does not impose those render limits on editorial validation.

Required top-level fields: project_id, title, target_duration_ms, initial_facts, shots. Each fact has key and value. Each shot has shot_id, duration_ms, purpose, action, present; optional requires/effects contain facts; depends_on contains earlier shot IDs. Dialogue cue fields: cue_id, start_ms, end_ms, text, language, speaker. Cue offsets are relative to the shot. SRT export makes them global. See the complete bundled example.

Return the portable film sidecar for review or use with a compatible Comfy Story installation. This is not a complete ComfyUI workflow or inputs bundle. Model weights, reference images, approved takes and rendering are separate. The package includes unmodified AGPL-3.0-only contracts with source and notices.
