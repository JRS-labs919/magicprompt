## Universal template

Use the blocks that apply and drop the ones that don't. SHORT prompts keep TASK, UNKNOWNS and OUTPUT only.

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
Anything not stated in the sources → TBD, listed at the end.
No inference from similar projects. No typical values. No boilerplate carry-over.
Blank is not acceptable in place of TBD.

CONFLICTS
Flag, do not resolve. Numbered register: what each source says (cited),
why it matters, who owns the resolution. Register it and keep going.

CLAIMS (when the output states real-world facts or figures)
Tag every factual claim per the claim-tag rules.
Figures and identifiers must be [S] or [D]. [U] ships as TBD, never as a value.

HARD STOPS (only these halt the run)
- <an input the work cannot proceed without is missing or unreadable>
- <the next step would overwrite or delete something outside SCOPE>
Anything else unclear → take the conservative path, keep going, list it under "Calls I made".

CHECKS (reported at the end, pass or fail, with evidence)
- [script] <count in> == <count out>
- [script] <unchanged thing> hash match
- [judgment] <domain check>

OUTPUT
<exact count, format, filename, location, presentation order>
Do not produce: <tempting extras>

DO NOT
- <negative constraint>
- <negative constraint>
```
