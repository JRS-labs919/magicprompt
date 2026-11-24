---
name: gate-and-verify
description: Approve the compiled prompt first, then run it through the claim-verified answer pipeline with an independent Approver. For high-stakes research, reviews, extractions and summaries. Explicit invocation only.
disable-model-invocation: true
---

# Gate and Verify

Two failures, two controls. A well-formed prompt stops the wrong task from being run; the verified-answer pipeline stops a wrong answer from shipping. This skill does both: one approval of the prompt, then every claim in the result is tagged, sourced and re-checked before it reaches the user. After that the conversation is normal again.

## The flow

```
1. REFINE    — write the prompt (CLAIMS block always included); do none of the work
2. SHOW      — prompt + what was assumed
3. APPROVE   — once: Run / Edit / Cancel
4. RUN       — approved prompt as Stage 0 → Reviewer → Dispatcher → SME → Approver
5. FINISH    — Publisher output + the prompt's checks, one report
   then      — normal conversation; the gate stays closed
```

## What to read, and when

The steps, template, claim-tag rules and pipeline are in this file. Read what applies from the rest in one batch.

| When | Read |
|---|---|
| After picking the task type | `references/shared/variant-a.md` … `variant-f.md` — the one matching file |
| Unsure how to fill a block | `references/shared/levers.md` |
| Step 5 | `references/shared/gate-report.md` |
| A subagent tool exists | `references/shared/reviewer-agent.md` |

## Differences from plain prompt-gate

- The prompt is always FULL and **always** includes the CLAIMS block.
- CHECKS lists the Approver block by reference, plus any task-specific `[script]` checks.
- Follow-up questions after the run are answered normally — they go through the pipeline again only if the user asks for that.

{{include: gate-loop.md}}

{{include: template.md}}

## Step 4 — Run through the pipeline

Open with: `Running prompt v<n> through the verified-answer pipeline.` Run Stages 1–5 below using these bindings wherever the shared pipeline gives a different instruction. The approved prompt already settled most of Stages 0–2.

| Pipeline element | Bound to |
|---|---|
| Stage 0 / Gatekeeper | The approved prompt. No new GO/HOLD decision — the user already made it. |
| Assumptions carried | The prompt's Assumed list, as `A` rows |
| HOLD | Only the prompt's HARD STOPS. Anything else resolves to TBD or a bracketed answer and the run continues. |
| Reviewer block | Premises, Time-sensitive and Risk flags only. Scope comes from the prompt's SCOPE block — narrow it if needed, never widen. |
| Dispatcher block | SME, Research depth and Tool plan only. Done-when is the prompt's OUTPUT block. |
| Source authority | The prompt's SOURCES order first, then the tiers below |
| ESCALATE | Ship with the unresolved defects as Open items, leading the output |

{{include: claim-tags.md}}

{{include: pipeline.md}}

## Step 5 — Finish

One report, in this order:

1. The Publisher output (Answer, Verification, Open items, Trace)
2. The prompt's task-specific checks in the `references/shared/gate-report.md` format — `[script]` items with command and output
3. Calls made on the conservative path, if any

Nothing is withheld. A claim that did not survive the Approver ships as TBD; a check still failing after two fix attempts leads the report and that part is marked not safe to use.

## Failure modes

| Failure | What it looks like |
|---|---|
| Leaking the answer | The refine turn contains a finding or figure |
| Running on silence | Executing when the reply never said to |
| Re-gating | A follow-up after the run gets a new prompt and approval nobody asked for |
| Stopping to check in | The run halts for something not on the HARD STOPS list |
| Scope widened in-pipeline | Reviewer "in" list larger than the approved SCOPE |
| Second gatekeeping | Re-asking the user something the approved prompt already settled |
| Phantom source | A pointer to something not opened this session |
| Confident [U] | An unverified figure written as a plain sentence |
| Bare PASS | A gate or Approver test with no evidence or named judge |
| Self-review called independent | Same-context review labelled as independent |
| Budget creep | Research continuing past the depth budget instead of shipping TBD |
