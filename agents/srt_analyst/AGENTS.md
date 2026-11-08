# short_ai_agents

This project starts at the SRT Analyst stage.

## Workflow

SRT -> Beat Map -> Storyboard -> Visual Design -> Video Builder -> QA -> Upload

## Current stage: SRT Analyst

The analyst receives an `.srt` file and outputs a structured beat map.

## Files

- `agents/srt_analyst/README.md` — role definition
- `agents/srt_analyst/schema.json` — output contract
- `agents/srt_analyst/srt_analyst.py` — parsing script

## Next steps

1. Validate the SRT parser against real subtitle inputs.
2. Add a stronger beat grouping heuristic.
3. Define the Storyboard Director handoff.
