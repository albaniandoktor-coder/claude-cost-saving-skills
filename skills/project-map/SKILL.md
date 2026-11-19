---
name: project-map
description: Start work on a large or long-lived project folder by reading its saved map (PROJECT-MAP.md) instead of exploring the folder again. Use whenever a request touches a project that has, or should have, a map: testing, fixing, auditing, adding content, changing how it looks, or a bare "continue" about earlier work, even if the project is not named. Also use to set a map up the first time a project turns out to be expensive to explore.
---

# Project map: read the map first

Some projects are expensive to find your way around: hundreds of files, a few of them many megabytes, and a long technical log. Listing folders and opening files to get oriented can cost tens of thousands of tokens, and without a map every session pays that again. A map file beside the project, kept current by a small script, replaces that with one tool call and a few thousand tokens.

The map is `PROJECT-MAP.md` in the project's top folder. The script is `scripts/make_project_map.py` in this skill; copy it into the project's top folder the first time, so later sessions can run it without this skill being loaded.

## Step 1: get the map (one call)

From the project's top folder, run:

```
python3 make_project_map.py
```

Useful options: `--log NOTES.md` indexes the `## ` headings of a long notes or change-log file with their line numbers, and `--entry path/to/index.html` checks a web entry page for scripts and stylesheets that point at missing files. Put the options the project needs in its `CLAUDE.md` or in the map's standing notes, so every session runs the same command.

The script rewrites the snapshot half of the map from the files on disk (well under a second for most projects, and no model tokens) and prints the whole map. Always run the script rather than reading the file, so the snapshot is never stale. Skip the command only if a section headed "Snapshot (generated ...)" from this session is already in your context.

The map has two halves:

- **Standing notes** (kept by hand): what the project is, where things are, how it runs, which files must not be touched, how changes are made, the test commands, and what to watch out for.
- **Snapshot** (rewritten on every run): free disk space, file counts by type, top-level folders, file families by name, the largest files, what changed most recently, and the log index.

## Step 2: work from the map, not from exploration

The map exists so that these are no longer needed. Skip them:

- Listing the project folder or its subfolders to get oriented. The folder, family and recent-changes lists say where to look; list a folder only to find one specific file.
- Reading the README or the log from top to bottom. Pick the section from the index and read only those lines: `sed -n 'START,ENDp' NOTES.md`.
- Printing any file named under "Largest files". Search it with `grep -n` piped through `head`, or load it with a short script and print only the items needed.
- Rediscovering the test commands, the port, or the backup conventions. They are in the standing notes; follow them.

If the map does not answer something, look that one thing up, then add it to the map (Step 3) so it is only ever looked up once.

When handing work to a helper agent, paste the few standing-note lines it needs into its brief, or tell it to run the same command first. A helper that explores on its own pays the cost this skill exists to remove.

## Step 3: leave the map better than you found it

Before finishing a session that changed the project:

1. If something durable changed or was learned (a new convention, a folder moved, a new gotcha, a new test command), edit the standing notes in `PROJECT-MAP.md`, above the line that begins `<!-- AUTO SNAPSHOT BELOW`. Correct or replace lines rather than adding to the end, and keep the notes under about 60 lines. One-off details of today's job belong in the project's log as a dated section, not in the map.
2. Run the script once more so the snapshot and the log index reflect your changes.

Never edit below the marker; the script overwrites it.

## Setting up a map for the first time

1. Copy `scripts/make_project_map.py` into the project's top folder and run it. It creates `PROJECT-MAP.md` with an empty standing-notes section and a first snapshot.
2. Write the standing notes from what the project already documents (README, contributor notes, the log). Cover: what the project is, how to run it, how to test it, the files that hold the user's own data and must never be overwritten or tested against, how changes are made and backed up, and known pitfalls. Ask the user about anything that cannot be found.
3. Add one line to the project's `CLAUDE.md` (or equivalent instructions file) telling future sessions to run the command first.
4. If the project has needs the generic snapshot does not cover (for example a manifest of modules, or an external drive), extend the script's `snapshot()` function. Keep it to file names, sizes and dates so it stays fast and safe.
