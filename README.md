# Video Explainer Production

An agent skill for producing animated explainer videos in the flat storybook style popularized by channels like Kok Bisa: generated illustration, layered compositing, camera moves over a living scene, text only as in-world labels, and a narration track that rules the timeline.

The skill is a production standard, not a script collection. It tells an AI agent how to run the whole pipeline and, just as importantly, how to prove the result is good: a locked golden sample as the quality benchmark, a beat sheet as the contract, and two audit points with measured gates.

## Scope

Shorts under 60 seconds. A full length production (10 minutes, 17 scenes, 89 beats) was completed with this skill as its maturity test and passed both audits, but it proved too slow and token-hungry to be the default. Longform is possible, just not recommended.

## How it works

1. **Timing first.** The narration audio is the absolute ruler. Phrase timings are measured from the real audio with faster-whisper before any timestamp is written.
2. **Beat sheet.** One beat per narration phrase with time range, visual, motion, SFX and transition, grouped into scenes. The user confirms the sheet before anything is built, and revisions are accepted only as beat sheet edits.
3. **Assets.** Every background and character is generated as an illustration in one locked style. Code never draws scenes; code only moves, composites and writes text. Transparent elements are keyed with a PIL and scipy flood fill route.
4. **Build.** Scenes live in a single HTML file at 1920x1080, driven by one deterministic `renderFrame(f)` function. Characters are independent layers with ground shadows, the camera zooms and travels per phrase, and no screen stays static for more than two seconds.
5. **Mix.** Narration plus a continuous ambient bed plus one SFX per action, normalized to -14 to -16 LUFS with true peak below -1 dB and no silence gap above 0.7 seconds.
6. **Render and assembly.** Frame by frame with puppeteer-core and full Chrome, JPEG capture, `yuv420p` output. Long videos are assembled in lossless chunks with frame count checkpoints, because a single long encode is fragile.
7. **Audit.** Two fixed gates: stills and plan before the full render, the finished file after. Motion density is measured with one fixed reproducible method and compared against the golden sample measured the same way. Failed rules block delivery; waivers are recorded, never hidden.

## Requirements

- An AI agent that can read skill files (Claude Code, Codex, Gemini CLI, Cursor and similar)
- An image generator for scene art
- ffmpeg
- Node.js with puppeteer-core and a full Chrome build
- Python with faster-whisper, PIL and scipy
- An SFX bank (the skill explains how to build one with licensed sources)

See the Environment notes at the end of `SKILL.md` for the pieces you need to map to your own setup, including producing your own golden sample.

## Install

Copy this folder into your agent's skills directory, for example:

```bash
cp -r video-explainer-production ~/.claude/skills/
```

Then say the trigger phrase **"mode explainer"** to your agent, and hand it a narration audio plus the script.

## Files

- `SKILL.md` — the full production standard: pipeline, universal technical rules, quality gates and the failure protocol.
- `skill.yaml` — skill metadata for agents that index skills by manifest.

## Battle test

First full production with v1.0 of this skill: "Dinasti Utsmaniyah", a 10 minute explainer (600 seconds, 17 scenes, 89 beats, 18,037 frames). Global motion density measured 4.41 against the golden sample's 1.16 on the identical full resolution method. The findings from that run (chunked assembly, range normalization at assembly time, the reproducible density metric, keying thresholds) are folded into v1.1, the version in this repo.

## License

MIT. See `LICENSE`.
