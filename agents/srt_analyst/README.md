# SRT Analyst

The SRT Analyst reads the subtitle file, validates it, and converts subtitle cues into a beat map that the Storyboard Director can use.

Responsibilities:
- Validate timestamp format and ordering
- Detect malformed entries or overlaps
- Keep original text and timing intact
- Group adjacent or related cues into beats
- Tag each beat with a role (hook, explanation, contrast, climax, call-to-action)
- Produce a JSON beat map for the next stage

This stage does not create scenes or visuals. It prepares the narrative structure.
