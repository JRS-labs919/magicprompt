---
name: prompt-gate
description: Turn a rough ask into a well-formed prompt, show it once with assumptions flagged, run it on approval, then get out of the way — no re-gating of follow-ups. Explicit invocation only.
disable-model-invocation: true
---

# Prompt Gate

The user asks for something the way they'd say it out loud. Turn that into a well-formed prompt, show it, get one approval, run it. After that the conversation is normal again.

Most bad output traces back to a gap that was invisible in the rough ask — which source governs, what to do with a missing value, what must not be touched. A good prompt closes those gaps before work starts. That is the whole job: a better prompt, approved once. It is not a checkpoint on everything that follows.

When the main risk is a wrong *answer* rather than a rough *ask* — research, supplier facts, exec summaries — use `gate-and-verify`: same single approval, then the claim-verified answer pipeline.

## The flow

```
1. REFINE    — write the prompt; do none of the work
2. SHOW      — prompt + what was assumed
3. APPROVE   — once: Run / Edit / Cancel
4. RUN       — follow the prompt without stopping to check in
5. FINISH    — deliverable, then checks and the calls that were made
   then      — normal conversation; the gate stays closed
```

## What to read, and when

Steps 1–3 and the template are in this file. The rest loads only when it applies — in one batch.

| When | Read |
|---|---|
| FULL prompt, after picking the task type | `references/shared/variant-a.md` … `variant-f.md` — the one matching file |
| Variant A or D, or the output will state real-world figures | `references/shared/claim-tags.md` — the claim-tag rules |
| Unsure how to fill a block | `references/shared/levers.md` |
| Step 5, FULL prompt | `references/shared/gate-report.md` |
| Step 5, FULL prompt, and a subagent tool exists | `references/shared/reviewer-agent.md` |
| Size or shape unclear | `references/examples.md` |

{{include: gate-loop.md}}

{{include: template.md}}

## Step 4 — Run

Open with one line: `Running prompt v1.` Then follow it. Group independent tool calls in the same turn.

**The approved prompt governs** — over the original rough phrasing, and over a nicer-looking alternative.

**Don't stop to check in.** Only the prompt's HARD STOPS halt the run. For everything else take the conservative path, keep going, and note it for the end:

- a value is missing → `TBD`
- two sources conflict → register both, pick neither
- unclear whether something is in scope → leave it alone
- a choice with no stated preference → the option that changes least

If the prompt itself turns out to be unworkable — a source doesn't contain what it was said to, the scope makes the task impossible — that is a hard stop: say what's wrong and what the corrected prompt would be.

## Step 5 — Finish

Deliverable first. Then, for a FULL prompt, a short close:

```
**Checks** — each with its evidence: command → output, or what was compared and who judged it
**Calls I made** — the conservative-path choices from the run
**Still TBD** — what the sources didn't give
```

Format and rules for Checks: `references/shared/gate-report.md`. Where a code tool exists, run the `[script]` checks as one script and print its output. When a subagent tool exists, a separate reviewer agent grades the checks; otherwise review is same-context and labelled so.

**A failed check gets fixed, not parked.** Fix it if the fix is inside scope and re-run the checks — twice at most. Still failing → say so first, above the deliverable, and mark that part not safe to use.

A SHORT prompt gets no close unless something was assumed or is TBD — then one line.

## Failure modes

| Failure | What it looks like |
|---|---|
| Leaking the answer | The refine turn contains a finding, a number, or "it looks like X" |
| Re-gating | A follow-up after the run gets a new prompt and a new approval nobody asked for |
| Stopping to check in | The run halts for something not on the HARD STOPS list |
| Second approval | Edits come back for another sign-off instead of being applied and run |
| Question dump | "Need from you" lists things that could have been assumed |
| Padded assumptions | Twelve assumptions, none of which change anything |
| Silent scope growth | The prompt asks for more than the user did, unmarked |
| Fake inventory | SOURCES lists a file that was never checked for existence |
| Running on silence | Executing when the reply never said to |
| Bare PASS | A check marked PASS with no command, output, or named judge |
| Buried failure | A failed check reported below the deliverable |
| Over-reading | Loading every variant file, or the levers for a SHORT prompt |
