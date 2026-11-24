# Reviewer agent — independent review

Read when a subagent / task tool exists. The author of a deliverable is the worst judge of it: the context that drafted a claim will re-read it and agree. Separation is the control.

## Dispatch

- **Model:** Opus 5.5 (`claude-opus-5-5`). If unavailable, the strongest model available — and name it in the Review line.
- **Give it exactly:**
  1. The contract — the approved prompt, or the Reviewer scope + Dispatcher Done-when
  2. The deliverable or draft
  3. The claim ledger, if one exists
  4. The source pointers — paths, URLs, record IDs — so it can open them itself
  5. The claim-tag rules and the review block it must return (the Approver block or the gate-report format), pasted as text
- **Do not give it:** the author's reasoning, earlier drafts, rework history, or the conversation. It judges the work, not the story behind it.
- **It must:** open each pointer itself rather than trust quoted excerpts; re-run every calc row in code where it can; return the review block with every test and its evidence. It never edits the deliverable — it returns numbered defects.

```
You are an independent reviewer. You did not write this and have no stake in it passing.
Contract: <contract>
Deliverable: <deliverable>
Ledger: <ledger or "none">
Sources: <pointers>
Rules: <claim-tag rules, pasted>
Return format: <review block, pasted>
Open every pointer yourself. Re-run every calc in code. For each claim, decide whether the
source supports it AS WORDED. Return every test PASS/FAIL with its evidence, a numbered
defect list, and a verdict. Do not rewrite the deliverable.
```

## After it returns

Label the output `Review: independent (<model>, separate context)`. Defects go back to the author, who fixes only the listed defects. Maximum two rework loops, then escalate to whoever owns halts (the Gatekeeper, or the user when an approved prompt governs).

## No subagent tool

Review runs in the same context under the same-context rules stated in the skill, and is labelled `Review: same-context`. Never call it independent.
