---
name: gate-and-verify
description: Approve the compiled prompt first, then run it through the claim-verified answer pipeline with an independent Approver. For high-stakes research, reviews, extractions and summaries. Explicit invocation only.
disable-model-invocation: true
---

# Gate and Verify

Two failures, two controls. The gate stops the wrong task from being run; the verified-answer pipeline stops a wrong answer from shipping. This skill runs both in sequence: the user approves the prompt, then every claim in the result is tagged, sourced and re-checked before it reaches them.

## The loop

```
1. COMPILE   — classify, inventory sources, build the prompt (CLAIMS block always included)
2. PRESENT   — prompt + assumption ledger + open questions
3. GATE      — wait for approval; edits recompile and re-present
4. EXECUTE   — approved prompt as Stage 0 → Reviewer → Dispatcher → SME → Approver
5. CLOSE     — Publisher output + the prompt's verification gate, one report
```

## What to read, and when

The gate loop, template, claim-tag rules and pipeline are in this file. Read what applies from the rest in one batch.

| When | Read |
|---|---|
| After classifying | `references/shared/variant-a.md` … `variant-f.md` — the one matching file |
| Before building the prompt | `references/shared/levers.md` |
| Phase 5 | `references/shared/gate-report.md` |
| A subagent tool exists | `references/shared/reviewer-agent.md` |

## Differences from a plain gate

- The compiled prompt **always** includes the CLAIMS block, whatever the variant.
- The VERIFICATION GATE lists the Approver block by reference, plus any task-specific `[script]` checks.
- Depth is STANDARD at minimum.
- The prompt states whether review will be independent (subagent tool present) or same-context.

{{include: gate-loop.md}}

{{include: template.md}}

## Phase 4 — Execute through the pipeline

Open with: `Executing approved prompt v<n> through the verified-answer pipeline.` Run Stages 1–5 below with these bindings — the approved prompt already settled most of Stages 0–2, so do not redo or re-ask them:

| Pipeline element | Bound to |
|---|---|
| Stage 0 / Gatekeeper | The approved prompt. No new GO/HOLD decision — the user already made it. |
| Assumptions carried | The approved prompt's assumption ledger, as `A` rows |
| HOLD triggers | The prompt's STOP AND ASK IF list. A fired trigger stops the run and reports. |
| Reviewer block | Premises, Time-sensitive and Risk flags only. Scope comes from the prompt's SCOPE block — narrow it if needed, never widen. |
| Dispatcher block | SME, Research depth and Tool plan only. Done-when is the prompt's OUTPUT block. |
| Source authority | The prompt's SOURCES order first, then the tiers below |
| ESCALATE | Goes to the user, with the defect list and a proposed amendment |

If the approved prompt turns out to be wrong mid-run — a source lacks what the inventory implied, the scope makes the task impossible — stop, say what's wrong, propose the amendment as v<n+1>, and wait.

{{include: claim-tags.md}}

{{include: pipeline.md}}

## Phase 5 — Close

One report, in this order:

1. The Publisher output (Answer, Verification, Open items, Trace)
2. The prompt's task-specific gate items in the `references/shared/gate-report.md` format — `[script]` items with command and output
3. Anything in the approved prompt that was not satisfied, and why

The Approver verdict and the gate are both blocking. If either still fails after two rework loops, deliver the report without the deliverable and say what would clear it.

## Failure modes

| Failure | What it looks like |
|---|---|
| Leaking the answer | The compile turn contains a finding or figure |
| Soft gate | Executing on an ambiguous reply |
| Scope widened in-pipeline | Reviewer "in" list larger than the approved SCOPE |
| Second gatekeeping | Re-asking the user something the approved prompt already settled |
| Phantom source | A pointer to something not opened this session |
| Confident [U] | An unverified figure written as a plain sentence |
| Bare PASS | A gate or Approver test with no evidence or named judge |
| Self-review called independent | Same-context review labelled as independent |
| Budget creep | Research continuing past the depth budget instead of shipping TBD |
