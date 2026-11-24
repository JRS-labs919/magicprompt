# Levers — what each block of the compiled prompt defends against

Background for writing a FULL prompt. Read when unsure what a block is for or how to fill it.

## The levers

Ranked by observed effect on output quality. The first four cover most of it.

### Authority hierarchy

When sources conflict, an unranked set gets silently reconciled — one value gets picked and the disagreement disappears. The disagreement is usually the finding.

Compile it as an ordered list with the governing source first, plus a rule for what to do on conflict (flag, never resolve). If the user didn't state an order, propose one from document type and log it as an assumption — drawings over spec, spec over narrative, issued-for-construction over preliminary, later revision over earlier.

Non-authoritative sources get labeled as such. "Background only" is a real and useful designation.

### Unknown-handling rule

This is the literal hallucination control. Without it, a missing value gets filled with the plausible one — the typical rating, the value from a similar project, the spec's boilerplate.

The rule has three parts, and all three are needed:

- Not in the source → explicit `TBD`, never a value.
- No inference from similar projects, no rounding to typical, no boilerplate carry-over.
- Every TBD surfaces in an open-items list in the deliverable. Absent is not the same as flagged — a blank field reads as "not applicable" to whoever gets it next.

### Verification gate

"Double-check it" changes nothing. A countable check does. Write actual comparisons with a stated pass criterion:

- counts in versus counts out, per category
- hashes on anything meant to be unchanged
- domain checks that have caught real defects: feeder positions versus named loads, campus totals divided by blocks, BOM against drawing, N-1 capacity
- the result gets printed whether it passes or fails

A gate that only reports on failure is indistinguishable from no gate.

Mark every item `[script]` (countable — runs as code, prints its command and output) or `[judgment]` (needs reading — names who judged it). A bare PASS is a self-report, not a gate. Format and rules: `references/shared/gate-report.md`.

### Change-scope boundary

Unbounded scope produces unrequested behavior that looks requested. Compile three lists: change only, leave unchanged and verify, out of scope. The third catches the things that look in-scope but aren't.

For anything touching an existing artifact, "leave unchanged" needs a verification method attached, not just an instruction.

### Negative constraints

Negatives are load-bearing and get followed. Compile them explicitly rather than assuming an absence of instruction means absence of behavior. Common ones: no commentary, no alternatives offered, no adjacent refactoring, no extra deliverable formats, no cross-references to other work.

### Artifact contract

Exact count, format, filename, location, and order of presentation. Ambiguity here produces extra deliverables, wrong formats, and content in a file that should have been inline.

State what *not* to produce too, when there's an obvious tempting extra.

### Provenance requirement

Every rating, quantity, price, and date cites its source file and cell or page. This makes fabrication expensive and visible — and in review, the unsourced numbers are exactly the ones to distrust.

### Extraction split from decision

Two passes beat one. Extract to a reviewable intermediate, stop, then build after approval. This is why round-trip workflows outperform one-shot builds on the same input.

Write it as two passes with the intermediate shown in the output. Put a stop between them only when the user asks for one — the default is to keep going.

### Hard stops

A run that halts for every doubt is a run nobody wants to start. Name the few conditions that genuinely cannot be worked around, and let everything else resolve to the conservative path with a logged note:

- an input the work cannot proceed without is missing or unreadable → hard stop
- the next step would overwrite or delete something outside scope → hard stop
- two sources conflict → register both, do not pick, keep going
- a value is missing → TBD, keep going
- unclear whether something is in scope → leave it alone, note it, keep going

Generic instructions to "ask if unsure" don't fire anyway, because the whole problem is not knowing you're unsure. A short named list does.

### Ground-truth restatement

Long threads degrade — reasoning starts running against an earlier state of a file. When continuing work on a revised artifact, the prompt should restate what supersedes what.

---

## What does not work

Do not compile these — they consume space and change nothing:

- "Be accurate", "don't hallucinate", "double-check your work" — non-operational.
- "Use your best judgment" on a factual gap — an explicit invitation to fill it.
- More attached sources with no authority order — more material, more silent reconciliation.
- Analysis and deliverable requested in one shot when the analysis has open questions.
- Politeness padding. Every line in a compiled prompt should change the output or come out.

One more, worth its own line because it is counterintuitive:

**"Preserved exactly" is not "correct."** A faithful copy propagates a structural defect perfectly. When the task is preservation, the prompt still needs a check on whether the preserved thing is right in the source.
