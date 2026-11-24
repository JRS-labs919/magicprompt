---
name: prompt-gate
description: Compile a casual request into a reviewable prompt — sources, unknowns, scope, stop triggers, evidence gate — show it with assumptions flagged, and execute only after approval. Explicit invocation only.
disable-model-invocation: true
---

# Prompt Gate

The user asks for something the way they'd ask in normal conversation. Instead of doing it, compile that request into an explicit prompt, show it, and wait. Only after approval does any work happen.

The point is not ceremony. Most bad output traces back to a gap that was invisible at request time — an unstated source hierarchy, an unstated unknown-handling rule, an unbounded change surface. Surfacing those *before* work starts is far cheaper than catching them in the deliverable, and it puts the user in position to correct the framing rather than the output.

When the main risk is a wrong *answer* rather than a misread *ask* — research, supplier facts, exec summaries — use `gate-and-verify`: same gate, plus the claim-verified answer pipeline.

## The loop

```
1. COMPILE   — classify, inventory sources, build the prompt
2. PRESENT   — prompt + assumption ledger + open questions
3. GATE      — wait for approval; edits recompile and re-present
4. EXECUTE   — run against the approved prompt, verbatim
5. CLOSE     — report every verification-gate item with its evidence
```

## What to read, and when

Phases 1–3 and the template are in this file. Everything else loads only when it applies — read what applies in one batch.

| When | Read |
|---|---|
| After classifying | `references/shared/variant-a.md` … `variant-f.md` — the one matching file |
| STANDARD or FULL, before building the prompt | `references/shared/levers.md` |
| Variant A or D, or the output will state real-world figures | `references/shared/claim-tags.md` — the claim-tag rules |
| Phase 5 | `references/shared/gate-report.md` |
| FULL depth and a subagent tool exists | `references/shared/reviewer-agent.md` |
| Depth or shape unclear | `references/examples.md` |

{{include: gate-loop.md}}

{{include: template.md}}

## Phase 4 — Execute

Open with one line naming what's running: `Executing approved prompt v2.` Then follow it literally. Group independent tool calls in the same turn.

**The approved prompt governs.** Where it conflicts with the original casual phrasing, the prompt wins — that's what the review was for. Where it conflicts with a general habit or a nicer-looking alternative, the prompt still wins.

**Stop triggers are real stops.** When one fires, stop and report. Do not improvise a resolution, do not proceed on the most plausible reading, do not note it at the bottom and continue. The user approved a prompt that said to stop.

**If the approved prompt turns out to be wrong** — a source doesn't contain what the inventory implied, the scope boundary makes the task impossible — stop, say what's wrong, propose the amendment, and wait. Do not silently amend and continue.

## Phase 5 — Close

Report the verification gate in the `references/shared/gate-report.md` format: every item, pass or fail; each `[script]` item with its command and actual output; each `[judgment]` item with what was compared and who judged it. Where a code tool exists, put the `[script]` checks in one script and run it once. Print the gate even when everything passes.

At FULL depth with a subagent tool, a separate reviewer agent grades the gate — it receives the approved prompt, the deliverable and the source pointers, not your reasoning. Otherwise review is same-context and labelled so.

**A failed gate item blocks the artifact.** Report what failed; do not hand over the deliverable until it passes or the user explicitly waives it.

Then list anything in the approved prompt that was not satisfied, and why. A partially-satisfied prompt reported honestly is useful; a partially-satisfied prompt presented as complete is the failure this whole skill is built to prevent.

## Failure modes

Watch for these in your own output — each has happened:

| Failure | What it looks like |
|---|---|
| Leaking the answer | The compile turn contains a finding, a number, or "it looks like X" |
| Padding the ledger | Twelve assumptions, none of which change anything |
| Silent scope growth | The prompt asks for more than the user did, unmarked |
| Fake inventory | SOURCES lists a file that was never checked for existence |
| Soft gate | Executing on an ambiguous reply, or on answered questions alone |
| Skipped gate report | Output presented without printing the verification results |
| Bare PASS | A gate item marked PASS with no command, output, or named judge |
| Self-graded FULL | A FULL-depth deliverable graded in the same context while a subagent tool was available |
| Version drift | Executing against v1 after v2 was approved |
| Blocks dropped | A template block omitted because it "didn't seem relevant" |
| Over-reading | Loading every variant file, or the levers at MINIMAL |
