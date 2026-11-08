# SRT Analyst

The SRT Analyst is the first stage in the `short_ai_agents` workflow.

Purpose:
- validate subtitle timing and structure
- preserve original cue text and timestamps
- group related cue lines into beats
- hand off a structured beat map to the Storyboard Director

Scope:
- input: subtitle file (`.srt`)
- output: `*.beat_map.json`
- not responsible for visual creation, subtitle generation, or editing

Responsibilities:
1. Validate the file format and cue timestamps.
2. Detect malformed blocks, overlaps, or invalid ranges.
3. Keep the original cue timing and text unchanged.
4. Group adjacent cues into a beat when they are short, tightly connected, or part of the same idea.
5. Assign each beat a role such as `hook`, `explanation`, `contrast`, `climax`, or `cta`.
6. Produce a machine-readable beat map for Storyboard Director.

This stage is deterministic and lightweight. It should be run before any creative decisions are made.
