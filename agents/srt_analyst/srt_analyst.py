#!/usr/bin/env python3
"""SRT Analyst for short_ai_agents.

Purpose:
  - validate SRT files
  - preserve original cue timing and text
  - group subtitle cues into beats for Storyboard Director handoff

Output:
  beat_map JSON file next to the source SRT
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

TIME_RE = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2},\d{3})")


def srt_to_ms(ts: str) -> int:
    h, m, rest = ts.split(":")
    s, ms = rest.split(",")
    return int(h) * 3600000 + int(m) * 60000 + int(s) * 1000 + int(ms)


def parse_srt(path: str):
    source = Path(path)
    text = source.read_text(encoding="utf-8-sig")
    blocks = [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]

    cues = []
    warnings = []

    for idx, block in enumerate(blocks, start=1):
        time_match = TIME_RE.search(block)
        if not time_match:
            raise ValueError(f"Cue #{idx}: no valid SRT time range found")

        start_ts, end_ts = time_match.groups()
        start_ms = srt_to_ms(start_ts)
        end_ms = srt_to_ms(end_ts)

        if end_ms < start_ms:
            raise ValueError(f"Cue #{idx}: end time occurs before start time")

        after_time = block[time_match.end():].strip()
        text_lines = [line.strip() for line in after_time.splitlines() if line.strip()]
        text_value = "\n".join(text_lines)

        if not text_value:
            warnings.append(f"Cue #{idx}: empty subtitle text")

        cues.append({
            "cue_id": idx,
            "start": round(start_ms / 1000.0, 3),
            "end": round(end_ms / 1000.0, 3),
            "duration": round((end_ms - start_ms) / 1000.0, 3),
            "text": text_value,
        })

    for i in range(1, len(cues)):
        prev = cues[i - 1]
        curr = cues[i]
        if curr["start"] < prev["end"]:
            warnings.append(
                f"Cue #{curr['cue_id']} overlaps with Cue #{prev['cue_id']} "
                f"({curr['start']} < {prev['end']})"
            )

    return {"cues": cues, "warnings": warnings}


def assign_role(beat_text: str, idx: int, total: int) -> str:
    text = beat_text.lower()

    if idx == 0 and any(word in text for word in ["mau", "lihat", "siapa", "tahu", "apakah", "mengapa", "kamu"])):
        return "hook"
    if any(word in text for word in ["tapi", "namun", "justru", "salah", "berbeda", "sebaliknya"]):
        return "contrast"
    if any(word in text for word in ["jadi", "kesimpulan", "jadi", "maka", "sebelum", "kalau kamu", "jawabanmu", "commentar"]):
        return "cta"
    if idx == total - 1 or any(word in text for word in ["akhirnya", "begitu", "ternyata", "lalu", "maka", "sempurna"]):
        return "climax"
    return "explanation"


def group_beats(cues, max_gap_sec=1.5, max_chars_per_beat=220):
    if not cues:
        return []

    beats = []
    current = {
        "cue_ids": [cues[0]["cue_id"]],
        "starts": [cues[0]["start"]],
        "ends": [cues[0]["end"]],
        "texts": [cues[0]["text"].strip()],
    }

    for cue in cues[1:]:
        text = cue["text"].strip()
        merged_text = " ".join(part for part in current["texts"] + [text] if part)
        gap = cue["start"] - max(current["ends"])
        should_merge = (
            gap <= max_gap_sec
            and len(merged_text) <= max_chars_per_beat
            and len(merged_text.split()) <= 28
        )

        if should_merge:
            current["cue_ids"].append(cue["cue_id"])
            current["starts"].append(cue["start"])
            current["ends"].append(cue["end"])
            current["texts"].append(text)
        else:
            beats.append(current)
            current = {
                "cue_ids": [cue["cue_id"]],
                "starts": [cue["start"]],
                "ends": [cue["end"]],
                "texts": [text],
            }

    beats.append(current)

    result = []
    for idx, beat in enumerate(beats):
        full_text = " ".join(part for part in beat["texts"] if part)
        start = min(beat["starts"])
        end = max(beat["ends"])
        result.append({
            "beat_id": f"beat_{idx + 1}",
            "start": round(start, 3),
            "end": round(end, 3),
            "duration": round(end - start, 3),
            "cue_ids": beat["cue_ids"],
            "role": assign_role(full_text, idx, len(beats)),
            "summary": full_text[:180],
            "text": full_text,
        })

    return result


def build_beat_map(path: str):
    parsed = parse_srt(path)
    cues = parsed["cues"]
    beats = group_beats(cues)

    return {
        "project": "short_ai_agents",
        "stage": "srt_analyst",
        "version": "0.2.0",
        "source_file": str(Path(path).name),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "validation": {
            "warning_count": len(parsed["warnings"]),
            "warnings": parsed["warnings"],
            "cue_count": len(cues),
        },
        "cues": cues,
        "beats": beats,
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python srt_analyst.py <input.srt>")
        sys.exit(1)

    input_path = sys.argv[1]
    result = build_beat_map(input_path)
    out_path = Path(input_path).with_suffix(".beat_map.json")
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Beat map written: {out_path}")
    if result["validation"]["warning_count"]:
        print("Warnings:")
        for warning in result["validation"]["warnings"]:
            print(f" - {warning}")
