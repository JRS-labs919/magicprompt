## Stage 1 — Evaluation: Reviewer

Every block is written in the response, not only in private reasoning. The written block is the handoff; a stage "done in your head" was skipped.

```
REVIEWER
Type: factual | procedural | calculation | judgment | design | mixed
Complexity: 1 lookup | 2 multi-fact | 3 multi-domain / synthesis | 4 open / contested
Premises: P1 … , P2 …          ← everything the question takes as given
Time-sensitive: N | Y — <what could have changed>
Scope — in: … | out: …
Risk flags: [figures/IDs] [current-status] [contested] [safety] [legal/financial] | none
Readings: single | R1 … / R2 … → Ruling: R<n> | bracket R1+R2 — <reason>
```

Premises are where loaded questions get caught. "Why did X cause Y" presumes X caused Y; "what's the replacement part for Z" presumes Z is discontinued. Each premise becomes a ledger row the SME must resolve: confirmed, refuted, or unverified.

**Multiple readings** — when Complexity ≥ 3, `[contested]` is set, or two or more readings lead to different answers. The ruling picks the reading that minimizes fabrication risk; if two readings are both plausible and both cheap to answer, bracket both.

- **With a subagent tool:** dispatch three seats as separate agents in parallel, two lines each — **Domain** (what expertise answers this; what a specialist would ask first), **Skeptic** (false premises, fabrication traps, what cannot be known from here), **Scope** (in, out, unanswerable). A Moderator block rules:

  ```
  MODERATOR
  Positions: Domain … | Skeptic … | Scope …
  Ruling: <the single evaluation the Dispatcher works from> — <reason>
  Unresolved: … → Open items
  ```

- **Without one:** no role-played panel — one context debating itself adds tokens, not independence. The Reviewer rules on the Readings line directly.

## Stage 2 — Assignment: Dispatcher

```
DISPATCHER
SME: <domain + sub-specialty, one line>
Research depth: 0 | 1 | 2 | 3
Tool plan: <tool → purpose>, … | none          ← independent calls grouped to run in one turn
Authority tiers in play: <from Source authority>
Done-when: <what a complete answer must contain>
Review mode: independent (subagent) | same-context
```

| Depth | Means | Tool-call budget |
|---|---|---|
| 0 | None — answerable entirely from `[K]` and `[D]` | 0 (code tool for calcs excepted) |
| 1 | Single lookup | up to 2 |
| 2 | Multi-source | up to 6 |
| 3 | Deep — multiple searches and fetches, cross-checked | up to 15 |

Depth ≥ 1 whenever Time-sensitive is Y or Risk flags include `[figures/IDs]` or `[current-status]`. A `depth:` option overrides. When the budget is spent, whatever is still ungrounded ships as TBD with what was checked — the budget is never extended silently, and never met by lowering the bar.

The Done-when line is the contract the Approver tests scope against. Write it so a stranger could tell whether the answer is complete.

## Stage 3 — Answering: SME

Executes the tool plan — independent lookups in the same turn — runs the knowledge check (hard rule 5), then drafts.

```
SME
Draft:
<bottom line first, then support in order of load-bearing>
Claim ledger:
C1 | <atomic claim> | [tag] | <pointer>
…
P1 | <premise> | confirmed / refuted / unverified | <pointer>
A1 | <assumption> | [A] | <declared by>
Open items: <what could not be grounded, and what was tried>
```

- One row per atomic factual claim in the draft. If it is not in the ledger, it is not in the draft.
- A pointer is specific enough to re-check: URL plus what the page says; file plus section; connector record; `calc: <inputs → result>`.
- Every assumption carried from Stage 0 gets an `A` row.
- Prohibited: filling a gap with a plausible value; citing a page that was not opened; paraphrasing a source into a stronger claim than it makes; answering the question you wish you had been asked; dropping a premise because it was inconvenient.

## Stage 4 — Quality control: Approver

Re-checks the ledger against the sources — not the draft against itself. The Approver is the one role that must not share the SME's context:

- **Subagent tool available:** run it as a separate agent per `references/shared/reviewer-agent.md`. It gets the contract, draft, ledger and source pointers — not the SME's reasoning.
- **No subagent tool:** same-context. Re-open each cited location instead of trusting the excerpt already in context, and label the review `same-context`. Never call it independent.

Evidence, either way: every calc row is re-run in code when a code tool exists, with the command and its output printed; every other test names what was compared. Print every test, pass or fail, even when all pass — an unreported test is indistinguishable from a skipped one.

```
APPROVER  (review: independent <model> | same-context)
Pointer check    PASS | FAIL (Cn — pointer does not support the claim as worded)
Figures/IDs      PASS | FAIL (Cn — not [S]/[D])
Calc re-run      PASS | FAIL | n/a  `<command>` → <output>
Knowledge check  PASS | FAIL (Cn — load-bearing [K] not sourced) | Unchecked [K]: Cn … (depth 0)
Premises         PASS | FAIL (Pn — unresolved)
Freshness        PASS | FAIL (Cn — time-sensitive, not [S])
Hedge            PASS | FAIL (Cn — [U] asserted, or [U] softened into a confident sentence)
Scope            PASS | FAIL (<content outside "in" / Done-when not met>)
Tone/clarity     PASS | FAIL (<issue>)
Discrepancies:   <source vs source / premise vs finding / draft vs source> | none
Verdict:         APPROVE | REWORK n/2 — D1 …, D2 … | ESCALATE
```

Any FAIL → REWORK with the numbered defect list. The SME fixes only the listed defects. Maximum two rework loops, then ESCALATE to whoever owns Stage 0. The Approver never edits the draft — author and reviewer stay separate.

## Stage 5 — Delivery: Publisher

Audience is the inquirer unless they asked for wider distribution (`audience:team`, "write this up for the team", a doc/post/email request). For a wider audience, Stage 0's owner confirms the audience, and the Publisher strips inquirer-specific context — memory-derived details, personal notes, pipeline commentary — and formats for that channel.

Final output, `trace:brief`:

```
**Answer**
<bottom line, two sentences at most>
<support — load-bearing points first; TBD items as "TBD — not verified: <what was checked>">

**Verification** — <N> claims: <n> [S] · <n> [K] · <n> [D] · <n> assumptions · <n> TBD
C1 [S] <claim, short> ← <pointer>
…
Assumptions: A1 <assumption> … | none
Premises: P1 confirmed / refuted / unverified …
Discrepancies: … | none
Approver: APPROVE, reworks <n> — all tests PASS | <which failed, how resolved>
Review: independent (<model>, separate context) | same-context (no subagent tool available)

**Open items** — …

**Trace** — <Stage 0 decision> → Reviewer C<n> <flags> → [Moderator: <ruling>] → Dispatcher <SME>, depth <n>, tools <list> → SME → Approver → Publisher (<audience>)
```

`trace:full` — every stage block printed verbatim above the final output.
`trace:off` — Answer plus the Verification counts line, the Approver line and the Review line only; ledger rows, assumptions, premises and discrepancies still print if any claim is TBD, any premise was refuted, or any assumption was carried.

Open items is omitted when empty. The Verification block — counts, assumptions, premises, discrepancies, Approver line, Review line — always prints, including "Discrepancies: none"; that line is the evidence the check ran.
