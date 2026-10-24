# Video explainer production (Kok Bisa style)

## Activation

- Activate this skill when the user says the trigger phrase "mode explainer" or names the skill video_explainer_production. Load this file and run the whole production by this standard only.

- Keep this lane separate from other video work. The taugasih_production skill covers Tau Ga Sih Shorts in another chat and never applies here.

- Scope decision (user, 24 Oct 2026, after the full length maturity test): use this lane for shorts under 60 seconds. A full length production is proven to work but is not worth its wall-clock time and token cost, so do not propose longform unless the user explicitly asks for it.

- Maturity: v1.1, locked 24 Oct 2026. The first full length production (Dinasti Utsmaniyah, 600 seconds, 17 scenes, 89 beats) passed both audit points and is the battle test of this skill. Its findings are folded into the rules below.

## Golden standard and inputs

- Treat the locked golden sample as the quality benchmark for every production. Its files live in the reference project folder (see Environment notes) and its beat sheet BEAT-SHEET-SAMPEL.md v6 is the format contract.

- Start from two inputs only, the narration audio and the script. The audio duration is the absolute ruler for video duration and is never cut, sped up or replaced.

- Measure the real phrase timings from the audio before writing timestamps. Transcribe locally with faster-whisper using local_files_only and manual ffmpeg decoding to a float32 array, then write an SRT with one cue per phrase.

- Work in a fresh project folder per video with input/, aset/, scenes/, tools/ and preview/ subfolders. Keep the script, the beat sheet, the scene HTML and the render tools inside that folder.

## Beat sheet and confirmation

- Write the beat sheet before any building, one beat per narration phrase. Each beat carries its timestamp range, the exact narration text, the visual, the motion, the SFX and the transition.

- Group beats into scenes of roughly three phrases with one shared location or visual system. End the sheet with the continuous bed audio spec and the measured targets.

- Confirm understanding before executing any beat sheet revision the user sends. Restate what will change, wait for the go ahead, and apply extra corrections the user adds during that confirmation.

- Accept revisions only as beat sheet edits. Implement the edited sheet exactly as written and deliver the video and the updated sheet together.

## Assets

- Generate every background and character with the image generator in one locked style, flat storybook illustration with a warm muted palette. Never draw scenes with code, because code drawn visuals read as slides and the user rejects them.

- Produce transparent elements on a plain white background and key the white out with a border connected flood fill on near white pixels plus removal of enclosed pure white only when the enclosed component exceeds 0.4 percent of the image area, then feather the alpha edge. If rembg runs out of memory in your environment, the PIL and scipy keying route is the fallback this pipeline was validated with.

- Check each keyed element over a cream background before use. Pale interiors such as cream turbans and wool sit below the keying threshold and must stay opaque.

- Keep characters as separate elements on their own layers with soft ground shadows. Match character scale to doors, tents and animals in the background so the size reads natural.

- Recolor map regions by extracting a land mask from the painting itself with measured color rules per pixel, then save each region as its own overlay image. Never fake a region with a radial glow, because viewers see the coastline mismatch.

- Check your SFX bank folder (see Environment notes) before synthesizing or downloading anything. Download missing signature sounds such as animal calls from Wikimedia Commons or other clearly licensed sources and record the source in the bank SOURCES.md.

## Scene build

- Build all scenes as sections of one scenes/index.html at 1920x1080 with absolutely positioned elements. Drive the whole stage from one deterministic renderFrame(f) function so frame f always produces the same picture.

- Separate the layers in DOM order, background, world elements behind the character, the character, front elements that can occlude the character, then labels and screen text. A character walking behind a flock or crowd must sit in the layer behind it.

- Animate the camera per phrase with keyframed focus points and scale on the world wrapper. Zoom toward whatever the narration names, travel between subjects, and zoom back out before the scene climax.

- Show text only as elements integrated in the scene, running counters, year ranges, name plaques, region labels and in-world titles. Never add subtitles, lower thirds or caption bars.

- Trigger a visual change on every narration phrase and never leave the screen static for more than two seconds. Add small ambient life to supporting elements, grazing animals, flickering fire, drifting dust and rippling water, kept slow and subtle.

## Audio mix

- Build the mix with ffmpeg from the narration, a low continuous ambient bed and one SFX per element action placed at its beat timestamp. Synthesize the bed from sine pads and lowpassed noise when no licensed bed exists.

- Match SFX to actions, ticks for counting numbers, a hard pop for labels and counters landing, whoosh for zooms and transitions, thud for impacts, shimmer for color changes and footsteps that follow the walking rhythm.

- Normalize the final mix to between -14 and -16 LUFS integrated with true peak below -1 dB and no silence gap above 0.7 seconds.

## Render

- Render frame by frame with puppeteer-core and a full Chrome build in headless new mode. Headless shell builds can hang on complex pages, so use the full browser binary.

- Return undefined from every function passed to page.evaluate. Returning a timeline or element object hangs the browser connection.

- Capture JPEG screenshots at quality 90, mux the frames with ffmpeg and encode with pix_fmt yuv420p so Android players can play the file. Run renders as tracked background processes with `muse.exec`, never as detached nohup jobs.

- Time phrase cues in frames at 30 fps and keep a per scene frame map in the scene file header so later edits stay surgical.

- Segments rendered from JPEG frames come out as yuvj420p full range or as tv range per segment. Read each segment color_range metadata and normalize the range exactly once during final assembly, never inside the segment builds.

- Assemble long videos in lossless chunks with a frame count checkpoint per chunk, then join the chunks. A single long encode gets killed by runtime restarts on this VM and loses the whole run. Verify checkpoints from metadata nb_frames, because counting frames by fully decoding lossless 1080p is prohibitively slow.

- Never probe or extract frames from a segment MP4 while its renderer is still writing it. A file read mid mux looks corrupt and proves nothing either way.

- When a scene builder ends without a final report, verify its deliverables on disk directly. A missing report does not mean a missing segment.

## Universal technical rules

- Apply these rules to every production in this pipeline. Each one generalizes a failure that cost a revision round in the golden sample, restated as a technical property to verify rather than an incident to remember.

- Separate asset production from compositing. All scene visuals are raster images from the generator, and code only moves, composites and writes text, because code drawn scenes read as flat slides.

- Bind every narration phrase to at least one visual state change. Measure motion density with one fixed reproducible method, full resolution luma mean absolute difference between frames sampled every second frame, and require the finished video to meet or exceed the golden sample measured with the identical method (golden sample 1.16, first full production 4.41). A scene with no bound change produces a static interval, and static intervals above two seconds fail.

- Derive every recolor or highlight from a mask of the source image geometry, measured per pixel. Verify the result on a still against the real shapes, because a radial glow passes code review and fails the eye.

- Keep one finish level across all composited elements in a scene, full color illustration with the shared palette and line treatment. Mixed finishes such as a flat silhouette over a painted background read as pasted on.

- Model every entity that must move as an independent layer with its own animation loop. Anything baked into the background image is static by definition, so crowds, animals and water need sprites or overlays of their own.

- Use real recordings for recognizable sounds such as animal calls and reserve synthesis for abstract sounds such as ticks, pops and whooshes. Record the source and license of every downloaded sound.

- Calibrate character scale against reference objects in the same frame, such as door height and animal size. Match periodic SFX rates to the animated cycle they accompany, so footstep frequency equals the walk cycle frequency.

- Define labels once in the style bible as a measured spec of font, size, padding and border weight, then reuse it for every plaque and name tag. Per instance eyeballing drifts.

- Animate actions as cause, contact and result. A tool enters, acts on the scene and leaves, and only its effect persists, because an end state that teleports in reads as fake.

- Back up the scene file before any structural edit and diff the element inventory after it. Silent element loss is the default failure of large HTML surgery.

- Run renders as tracked, resumable, per frame jobs with JPEG capture. A render that cannot resume from its missing frames loses the whole run to any interruption.

- Treat the beat sheet as part of the deliverable and verify it against the finished video before delivery. A spec that describes an older version is a defect of the same weight as a visual one.

## Quality gates

- Audit every production against the Universal technical rules at two fixed points, before the first full render on stills and the plan, and after the render on the finished file. Report the audit result per rule to the user with the delivery, and treat any failed rule as a defect to fix before approval.

- Inspect stills at the key frame of every beat before the full render. Check layer order, keying leftovers, label readability and natural character scale, and fix failures in the scene file rather than in post.

- Measure motion density on the finished file with the fixed method in the Universal rules and compare it against the golden sample measured the same way. Absolute density numbers inherited from builder self reports are not a gate, because they proved irreproducible across methods.

- Verify the final file with ffprobe, exact frame count equal to duration times 30, duration equal to the narration audio and pix_fmt yuv420p.

- Deliver the MP4 into your deliverables folder with the version in its file name and report the measured numbers with it. Keep producing versions until the user approves, and treat the approved version plus its beat sheet as the new golden standard when the user says so.

## When an audit fails

- Classify every failed rule by severity. Fatal defects such as broken sync, wrong facts, missing elements or an unplayable file, and quality defects such as density or label spec failures, block delivery until fixed.

- Localize the defect to its scenes and beats and repair only those segments. Reassemble and remeasure the whole file afterwards, but never re-render unaffected scenes for a local defect.

- Fix the defect at the layer where it originates, the asset, the scene code, the mix or the timing map. Never patch the rendered output, because a post patch desyncs the scene from its beat sheet.

- Re-audit the repaired segments, their immediate neighbours and the global measurements after every fix. A repair that breaks a transition or a sync point is a new defect, not a finished one.

- Allow at most two internal fix cycles for the same defect. On a third failure, stop and report to the user with the defect, its cause and the options, which are a design change through the beat sheet or an explicit waiver.

- Ship a failed item only on the user explicit waiver, and record the waiver in the delivery report next to the failed rule. A waived defect is documented, never hidden.

- Generalize every new failure type the audit catches into the Universal technical rules before the production closes. The rule list grows from audits, not from memory.

## Voice over

- Generate short narration with your local TTS tool (the reference setup uses a speak command with --language id and --output). One call handles at least 2000 characters, and roughly 950 characters equal one minute of speech.

- Generate per phrase rather than in one call when the beat sheet needs exact per phrase timings.

- Send long scripts to the user for ElevenLabs when the user prefers it, and rebuild the beat sheet timings from the returned audio instead of stretching the old ones.

## Environment notes

This skill was developed and battle-tested in one specific agent environment. Before your first production, map these pieces to your own setup and record your equivalents next to this file:

- A reference project folder holding the golden sample (the approved 30 second sample video, its beat sheet v6 and its style measurements). The whole quality system calibrates against it, so produce and approve your own golden sample first if you adopt this skill fresh.
- An image generator for all scene art, plus the PIL and scipy keying tools described under Assets.
- A local faster-whisper install for phrase timing, run with local_files_only and manual ffmpeg decoding to a float32 array (passing a file path straight to transcribe can break on some PyAV versions).
- An SFX bank folder with a SOURCES.md recording the source and license of every sound.
- puppeteer-core with a full Chrome build for the frame renderer.
- ffmpeg for the mix, assembly and measurement commands.
- A deliverables folder where finished MP4 files are handed to the user.
- Enough CPU patience: frame rendering and chunked assembly are resumable by design, because long single encodes are fragile on small machines.
