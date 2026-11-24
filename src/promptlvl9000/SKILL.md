---
name: promptlvl9000
description: Answer through a gated pipeline — Gatekeeper, Reviewer, Dispatcher, SME, Approver, Publisher — instead of directly. Every claim is tagged and tied to a source opened this session; anything unverifiable ships as TBD. Use on /promptlvl9000, "verified answer", "no-hallucination mode", "high-accuracy mode", "run this through the pipeline", or any question where being wrong is expensive — specs, ratings, part numbers, standards clauses, prices, lead times, dates, current status. Not for casual chat, brainstorming, creative writing, or tasks that build or change files.
---

# PromptLvL9000

A question comes in. Instead of answering it, run it through six roles with fixed inputs, outputs and authority. The answer the inquirer gets is whatever survives the Approver, and nothing reaches the Approver without a claim ledger tied to sources that were actually opened.

The point is not ceremony. Fabrication happens when a model fills a gap with the most plausible-sounding value and nobody checks. This pipeline makes every gap visible (Gatekeeper, Reviewer), makes every claim traceable (SME ledger), and makes every assertion survive a re-check against its source (Approver) before it ships (Publisher). A question that cannot be answered from sources gets an honest "not verifiable" with what was checked — that is a passing result, not a failure.

If the *ask itself* is fuzzy and a misread would be expensive, use `gate-and-verify` — the user approves a compiled prompt first, then this pipeline runs against it.

## Execution model

- Everything needed for a run is in this file. Two files load on demand: `references/shared/reviewer-agent.md` when a subagent tool exists, and `references/worked-example.md` when a block shape or the ledger format is unclear.
- Roles run in this context, sequentially, each writing its block before the next starts. A role may only use what prior blocks and tool results contain. The Approver is the exception — see Stage 4.
- No stage is skipped. On a trivial question each block is one line; it does not disappear.
- Normal safety rules sit above this skill; nothing here overrides them.

## Invocation

`/promptlvl9000 <question>` or `PromptLvL9000: <question>`. Options anywhere in the message, all optional:

| Option | Values | Default |
|---|---|---|
| `trace:` | `brief` / `full` / `off` | `brief` |
| `depth:` | `auto` / `0` / `1` / `2` / `3` | `auto` |
| `audience:` | `me` / `team` | `me` |

## Stage 0 — Gatekeeper

Oversees every stage, owns every halt, receives the question first.

```
GATEKEEPER
Question: <restated in one line — the inquirer's intent, not their wording>
Inputs present: <files / links / data> | none
Gaps: G1 … (blocking Y/N), G2 …
Decision: GO | GO-WITH-ASSUMPTIONS | HOLD
Assumptions carried: A1 … (GO-WITH-ASSUMPTIONS only)
```

- **GO** — complete enough to answer.
- **GO-WITH-ASSUMPTIONS** — gaps exist, but each can be bracketed (answer both branches) or closed with a stated assumption that would not materially change the answer if wrong. Every assumption carried becomes an `A` row in the ledger and prints in the final Verification block — never silently absorbed.
- **HOLD** — a blocking gap: the answer changes materially with the missing input and cannot be bracketed, or a referenced input (file, link, record) is missing or inaccessible and the answer depends on it. HOLD asks ONE batched set of questions — tappable options where the answers are enumerable — and ends the turn. On reply, resume at Stage 1 with the Gatekeeper block updated.

GO and GO-WITH-ASSUMPTIONS are the defaults. HOLD is the exception. Never ask permission to proceed.

**Gatekeeper interrupts** — any stage may raise one; the Gatekeeper rules on it:

- Premise refuted mid-pipeline and the corrected question has more than one plausible intent → bracket if cheap, else HOLD.
- A required source turns out inaccessible → bracket with TBD, or HOLD if the answer collapses without it.
- Approver returns ESCALATE → ship with Open items (default), or HOLD.

{{include: claim-tags.md}}

{{include: pipeline.md}}

## Fast path

Complexity 1, no risk flags: every block still gets written, one line each; depth 0 or 1; ledger of a few rows; Approver prints its tests. Total pipeline overhead on a simple question is about ten lines. Do not shortcut it — a gate that fires inconsistently is a gate nobody can rely on.

## Failure modes

Watch for these in your own output — each one is the hallucination this skill exists to prevent, wearing a different coat:

| Failure | What it looks like |
|---|---|
| Answering first | A finding appears before the Gatekeeper block |
| Narrated pipeline | "As the Reviewer, I would consider…" instead of a written block |
| Phantom source | A pointer to a page, file or record that was not opened this session |
| Confident [U] | An unverified claim rewritten as a plain sentence; "typically", "around", "generally" doing the work of a source |
| Ledger gap | A figure or name in the draft with no ledger row |
| Unchecked [K] | A load-bearing knowledge claim passed without the knowledge check or an `Unchecked [K]` listing |
| Rubber stamp | Approver prints PASS without re-opening pointers; all PASS on a draft with a TBD-worthy figure |
| Self-review called independent | Same-context Approver labelled as independent |
| Role-played panel | Domain/Skeptic/Scope seats written by one context and presented as a debate |
| Silent assumption | A GO-WITH-ASSUMPTIONS run whose assumptions don't appear in the Verification block |
| Premise dropped | A Reviewer premise with no resolution in the ledger |
| Scope creep | Answer covers things outside the Reviewer's "in" list, unmarked |
| Soft HOLD | Asking the inquirer something that could have been bracketed; or proceeding on a reading that should have been HOLD |
| Budget creep | Research continuing past the depth budget instead of shipping TBD |
| Loop without end | A third rework instead of ESCALATE |
