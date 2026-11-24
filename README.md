# Magicprompt

Magicprompt is a plugin for confirming task scope and verifying factual claims in Claude.

| Skill | Use when | Guards against |
|---|---|---|
| `prompt-gate` | Builds, file transformations, skill edits, anything irreversible or feeding a system of record | Misreading the ask |
| `promptlvl9000` | Factual questions, specs, prices, lead times, standards, current status | Fabricated answers |
| `gate-and-verify` | High-stakes research, reviews, exec summaries where the ask is fuzzy too | Both |

`prompt-gate` and `gate-and-verify` run only when invoked explicitly. `promptlvl9000` can also trigger on its own for high-accuracy questions.

## Install in Claude

On claude.ai, open **Customize → Plugins → Add marketplace**. Enter `JRS-labs919/magicprompt`, select **Sync**, then install **magicprompt** from the marketplace.

### Claude Code

Run these commands in a Claude Code session, then choose an installation scope.

```text
/plugin marketplace add JRS-labs919/magicprompt
/plugin install magicprompt@magicprompt
```

Try `/magicprompt:prompt-gate Review this README for clarity` to see the scope approval step.

## What changed

See `CHANGELOG.md`. v1.0.0 merged the two standalone skills and added the evidence gate, the independent reviewer and the claim checks. v1.1.0 is the optimisation pass: fewer files read per run, one-reply approvals, research budgets.

promptlvl9000 was rebuilt from the 2026-10-02 version. If you changed your installed copy after that, merge those changes into `src/promptlvl9000/SKILL.md`.

## Layout

```
src/<skill>/SKILL.md     skill source, with {{include: file.md}} markers
src/<skill>/references/  files owned by one skill
shared/                  rules used by more than one skill — single copy
shared-manifest.json     which shared files each skill loads on demand
plugins/magicprompt/     plugin manifest and generated skills
scripts/build.py         builds plugin skills (--check verifies they are current)
scripts/validate_plugin.py  release gate
```

Material every run needs is built into each SKILL.md, so a run starts without reading reference files. Material that applies only sometimes (one variant, the levers, the gate report, the reviewer agent) is copied into the skill's own `references/shared/` and read on demand. Every skill folder is self-contained.

## Editing

1. Edit `src/<skill>/SKILL.md` or `shared/*.md`. Never edit generated skills in `plugins/magicprompt/skills/`.
2. `python3 scripts/build.py`
3. `python3 scripts/validate_plugin.py` — must end `0 fail`.
4. Bump `version` in `plugins/magicprompt/.claude-plugin/plugin.json` and add a CHANGELOG entry.

## Install notes

Clone or download and unzip this repository. From the repository root, start Claude Code with the plugin loaded for the current session.

```sh
claude --plugin-dir ./plugins/magicprompt
```

- Remove the standalone `prompt-gate` and `promptlvl9000` skills after installing, or both copies will compete.
- In Claude Code, plugin skills are namespaced: `/magicprompt:prompt-gate`, `/magicprompt:promptlvl9000`, `/magicprompt:gate-and-verify`.
- Independent review needs a subagent tool (Claude Code, Cowork). In plain chat, review runs same-context and says so.
