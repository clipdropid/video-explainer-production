#!/usr/bin/env python3
"""Parse an SRT file and produce a beat map JSON.

Input:
    srt_path

Output:
    beat_map.json
"""

import json
import re
import sys
from pathlib import Path

TIME_RE = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2},\d{3})")


def srt_to_ms(ts: str) -> int:
    h, m, rest = ts.split(":")
    s, ms = rest.split(",")
    return int(h) * 3600000 + int(m) * 60000 + int(s) * 1000 + int(ms)


def parse_srt(path: str):
    text = Path(path).read_text(encoding="utf-8")
    blocks = [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]

    cues = []
    for idx, block in enumerate(blocks, start=1):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if len(lines) < 2:
            raise ValueError(f"Malformed SRT block #{idx}: {block[:120]}")

        m = TIME_RE.match(lines[0] + " --> " + lines[1]) if len(lines) >= 2 else None
        if len(lines) >= 2 and m is None:
            # Support the common case where the first line is timestamp and the second and later lines are text.
            if "-->" in lines[0]:
                time_line = lines[0]
                text_lines = lines[1:]
            else:
                raise ValueError(f"Invalid timestamp line in block #{idx}")
        else:
            time_line = lines[0]
            text_lines = lines[1:]

        # A more robust timestamp extraction path
        time_match = re.search(r"(\d{2}:\d{2}:\d{2},\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2},\d{3})", block)
        if not time_match:
            raise ValueError(f"No valid time range found in block #{idx}")

        start_ts, end_ts = time_match.groups()
        start_ms = srt_to_ms(start_ts)
        end_ms = srt_to_ms(end_ts)
        text_full = "\n".join(text_lines)
        duration = max(0.0, (end_ms - start_ms) / 1000.0)

        cues.append({
            "cue_id": idx,
            "start": start_ms / 1000.0,
            "end": end_ms / 1000.0,
            "duration": duration,
            "text": text_full,
        })

    return cues


def group_beats(cues):
    beats = []
    current = None
    for cue in cues:
        text = cue["text"].strip()
        if not text:
            continue

        if current is None:
            current = {
                "beat_group_id": f"beat_{len(beats) + 1}",
                "cues": [],
                "start": cue["start"],
                "end": cue["end"],
                "text": [],
            }

        current["cues"].append(cue)
        current["text"].append(text)
        current["end"] = cue["end"]

        if len(current["cues"]) >= 2:
            # Heuristic: if next cue is a short follow-up sentence, keep merging.
            # Otherwise, cut the beat when a cue is clearly a new idea.
            beats.append(current)
            current = None

    if current is not None:
        beats.append(current)

    out = []
    for beat in beats:
        cue_ids = [c["cue_id"] for c in beat["cues"]]
        text = " ".join(beat["text"]) if beat["text"] else ""
        out.append({
            "beat_group_id": beat["beat_group_id"],
            "start": beat["start"],
            "end": beat["end"],
            "duration": beat["end"] - beat["start"],
            "cue_ids": cue_ids,
            "text": text,
            "role": "explanation",
            "summary": ""
        })

    return out


def build_output(path: str):
    cues = parse_srt(path)
    beats = group_beats(cues)
    return {"cues": cues, "beats": beats}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python srt_analyst.py <input.srt>")
        sys.exit(1)

    input_path = sys.argv[1]
    output = build_output(input_path)
    out_path = str(Path(input_path).with_suffix(".json"))
    Path(out_path).write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")
