# Storyboard Director

The Storyboard Director transforms the SRT beat map into a cinematic plan for the visual team.

Purpose:
- convert narrative beats into shot structure
- define frame composition, scene rhythm, and transition logic
- propose visual motifs and camera language
- hand off a storyboard to Visual Designer and Video Builder

Scope:
- input: `*.beat_map.json`
- output: `*.storyboard.json`
- not responsible for final frame drawing or rendering

Responsibilities:
1. Read the beat map and map each beat to a shot or sequence of shots.
2. Decide the visual goal of each beat: hook, reveal, contrast, climax, call-to-action.
3. Define shot type, framing, motion, and pacing.
4. Keep the styling consistent with the chosen project style: `Cinematic Storybook 2D` or `Theater of Choices`.
5. Produce a machine-readable storyboard for the Visual Designer.

This stage decides the visual structure before any actual design or animation is created.
