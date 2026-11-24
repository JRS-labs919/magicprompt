# Changelog

## 1.2.0 — 2026-11-24
prompt-gate simplified: its job is a better prompt, approved once — not a checkpoint on everything after it.

- **One gate.** Refine → Show → Approve → Run → Finish. Routine edits and answers are applied and run, opening with the changed lines. A request to review the revised prompt or a change to the task itself calls for review before running.
- **The gate stays closed after the run.** Follow-ups in the same chat are handled normally. The old rule that every new request re-entered the gate is removed. Refine again only on a new invocation.
- **No mid-run check-ins.** STOP AND ASK IF is replaced by HARD STOPS — a missing input the work cannot proceed without, or an overwrite outside scope. Everything else takes the conservative path (TBD, register the conflict, leave it alone) and is listed under "Calls I made".
- **Failed checks get fixed, not parked.** Fix inside scope and re-check, twice at most; still failing → it leads the output and that part is marked not safe to use. The deliverable is no longer withheld.
- **Decide, don't ask.** Assume and list; questions only for what changes the result and cannot be guessed — two at most.
- **Simpler shape.** Short and full prompts omit unused blocks. Optional additions stay in one "Could also" line. The approval options are Run / Edit / Cancel.
- **"Just the prompt".** Ask for the prompt alone and it is handed over to run elsewhere.
- gate-and-verify follows the same flow; nothing is withheld — unverified claims ship as TBD.
- promptlvl9000 unchanged.

## 1.1.1 — 2026-11-24

- Package the plugin in a dedicated directory for Claude marketplace sync.
- Document marketplace installation from claude.ai and Claude Code.

## 1.1.0 — 2026-11-24
Optimisation pass on all three skills.

Loading
- Everything a run always needs is now inside each SKILL.md (built from `src/` + `shared/` by `scripts/build.py`). promptlvl9000 reads no reference files in chat; v1.0.0 read four on every run.
- `variants.md` split into one file per variant; only the matching one loads.
- `contract.md` split: the template is inline, the levers load at STANDARD/FULL only, the drift signals moved to the gate report (read at close).
- Each skill has a load table: what to read, when, in one batch.
- Descriptions shortened — they load in every session.

Behaviour
- Gate: when proposed additions exist, the options are Approve with additions / Approve without additions / Edit / Cancel.
- Gate: open questions with enumerable answers are asked in the same tappable call as the gate; answers plus a gate word execute in one reply, opening with the changed lines. Scope-changing answers still re-present.
- prompt-gate MINIMAL skips the levers file.
- promptlvl9000: tool-call budget per research depth (0 / 2 / 6 / 15); past the budget, ungrounded claims ship as TBD.
- promptlvl9000: independent lookups run in the same turn; HOLD uses tappable options where answers are enumerable.
- gate-and-verify: Reviewer and Dispatcher blocks reduced to what the approved prompt has not already settled.
- New failure modes: Over-reading, Budget creep.

Tooling
- `scripts/sync_shared.py` replaced by `scripts/build.py` (`--check` detects hand-edited generated files).
- Release gate now measures bytes loaded per run against the pre-optimisation baselines.

## 1.0.0 — 2026-11-24
- Plugin created from standalone `prompt-gate` and `promptlvl9000` (2026-10-02 build).
- Shared rules extracted to `shared/`.
- prompt-gate: evidence-based gate report, reviewer agent at FULL depth, claim tags for variants A/D.
- promptlvl9000: Approver in a separate agent, Calc re-run and Knowledge check tests, panel only as real agents, assumptions always printed.
- New skill: gate-and-verify.
