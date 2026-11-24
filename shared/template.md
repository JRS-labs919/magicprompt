## Universal template

Fill every block or mark it `n/a`. Silent omission is the gap this exists to close.

```
TASK
<one sentence, imperative>

SOURCES (authority order, highest first)
1. <file> — governs [inventoried]
2. <file> [inventoried]
3. <file> — background only, non-authoritative [user-stated, unverified]

SCOPE
Change only: <explicit list>
Leave unchanged: <explicit list> — verify by <method>
Out of scope: <plausible-looking things that are not included>

UNKNOWNS
Anything not stated in the sources → TBD, listed in open items.
No inference from similar projects. No typical values. No boilerplate carry-over.
Blank is not acceptable in place of TBD.

CONFLICTS
Flag, do not resolve. Numbered register: what each source says (cited),
why it matters, whether it blocks, who owns the resolution.
Blocking items lead the output.

STOP AND ASK IF
- <named condition>
- <named condition>

CLAIMS (when the output states real-world facts or figures)
Tag every factual claim per the claim-tag rules.
Figures and identifiers must be [S] or [D]. [U] ships as TBD, never as a value.

VERIFICATION GATE (report every item per references/shared/gate-report.md, pass or fail, before presenting)
- [script] <count in> == <count out>
- [script] <unchanged thing> hash match
- [judgment] <domain check>
Review: same-context | reviewer-agent (required at FULL depth when a subagent tool exists)

OUTPUT
<exact count, format, filename, location, presentation order>
Do not produce: <tempting extras>

DO NOT
- <negative constraint>
- <negative constraint>
```

Blocks that are genuinely inapplicable get `n/a` with a two-word reason: `SOURCES — n/a (no files)`.
