# Two cost-saving skills for Claude

Two skills for Claude (Claude Code and the Claude apps) that cut the cost of long sessions on large projects without lowering the quality of the answers.

| Skill | What it does |
|---|---|
| [`project-map`](skills/project-map) | Keeps a one-page map of a project (`PROJECT-MAP.md`) that a small script refreshes from the files on disk. Claude reads the map in one call instead of exploring the folder again every session. |
| [`smart-delegation`](skills/smart-delegation) | Splits each request into mechanical and thinking parts, hands the bulky mechanical parts (transcription, extraction, test runs, click-through checks) to cheaper helper models, and keeps the reasoning, the checking and the final answer on the main model. |

They work well together: `smart-delegation` tells helpers to start from the map, so they do not explore either.

## Install

**Claude Code:** copy the skill folders into `~/.claude/skills/` (all projects) or `.claude/skills/` inside one project.

```
git clone https://github.com/albaniandoktor-coder/claude-cost-saving-skills.git
cp -r claude-cost-saving-skills/skills/project-map claude-cost-saving-skills/skills/smart-delegation ~/.claude/skills/
```

**Claude apps:** zip a skill's folder and add it as a skill in your settings.

## Using project-map

Copy `skills/project-map/scripts/make_project_map.py` into your project's top folder and run it:

```
python3 make_project_map.py --log NOTES.md
```

It needs only Python 3.8+ and reads only file names, sizes and dates. It creates `PROJECT-MAP.md` with a hand-kept "Standing notes" half and a generated "Snapshot" half. Fill in the standing notes once (how to run, how to test, what must not be touched) and add a line to your `CLAUDE.md` telling Claude to run the command first.

## Using smart-delegation

Nothing to set up. It applies when the session has a helper (subagent) tool; without one, its three habits (script before model, loops go to helpers, output goes to files) still reduce cost. The model tiers it names are Anthropic's Haiku, Sonnet and the session model.

## License

MIT. See [LICENSE](LICENSE).
