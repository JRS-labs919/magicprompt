# Gate report — evidence format

Shared by every Magicprompt skill. A verification gate is only as good as its evidence. "PASS" with nothing behind it is a self-report, and self-reports are what the gate exists to replace.

## Two kinds of check

- **[script]** — anything countable or comparable: record counts, hashes, arithmetic, schema checks, required-field presence, row-by-row reconciliation. Where a code environment exists, write these checks into one script (e.g. `gate_checks.py`), run it once, and print its output verbatim. Arithmetic claims (`[D]` calc rows) are re-run in code, not re-read.
- **[judgment]** — anything that needs reading: does the pointer support the claim as worded, is the tone right, is the scope met. Name who judged it: `reviewer-agent` (separate context) or `same-context`.

Declare each planned gate item as [script] or [judgment] when the prompt or plan is written, and mark any item that cannot run in this environment. An item that cannot run is not a gate — say so before execution, not after.

## Format

```
**Gate — <skill> <prompt version or run id>**
G1 [script]   <check> — PASS | FAIL | NOT RUN
     `<command or script line>` → <actual output, verbatim or trimmed to the relevant line>
G2 [judgment] <check> — PASS | FAIL
     <what was compared against what> — judged by reviewer-agent | same-context
G3 [script]   <check> — NOT RUN — <why it cannot run here; declared before execution>
Summary: <n> script · <n> judgment · <n> not run · <n> fail
Review: independent (<model>, separate context) | same-context (no subagent tool available)
```

## Rules

1. Print every item, pass or fail. An unreported gate is indistinguishable from a skipped one.
2. No bare PASS. A [script] item without its command and output is a FAIL of the gate itself.
3. A failed item blocks the artifact. Report what failed; do not hand over the deliverable until it passes or the user explicitly waives it.
4. Never call a same-context review independent.
5. After the gate, list anything in the governing prompt that was not satisfied, and why.

## Who reviews

- **Subagent tool available, FULL depth or any verified-answer run:** a separate reviewer agent grades the gate — `references/shared/reviewer-agent.md`.
- **Otherwise, same-context:** re-open each cited location (re-read the file section, re-fetch the page) instead of trusting the excerpt already in context; re-run calcs in code if a code tool exists; label the report `Review: same-context`.

## Drift signals — scan the deliverable before reporting the gate

Check the deliverable against these before presenting. Each indicates a gap was filled instead of flagged.

| Signal | Usually means |
|---|---|
| A number with no citation, beside numbers that have one | Filled from pattern, not source |
| A round or typical value in a field the sources didn't cover | Plausible-value substitution |
| A conflict resolved in a sentence rather than registered | One source was picked silently |
| A product or model name asserted without a link | Recall — possibly stale or invented |
| A blank field instead of an explicit TBD | Dropped, not flagged; reads as N/A downstream |
| "Should work" or "functionally correct" with no test output | Untested |
| PASS with no command, output, or named judge behind it | Self-reported gate |
| A section nobody asked for | Scope drift — check what else moved |
| Reference to a file state the user has since replaced | Context degradation; restart the thread |

Cheapest audit: pick two numbers at random and ask where each came from, file and cell. If both can't be answered, distrust the set.
