# Worked example — full trace

A short calculation question with a premise check. Everything here is `[K]`/`[D]`, so no research was needed; it exists to show the block shapes and ledger format, not research depth. This run is in a chat surface with a code tool but no subagent tool, so review is same-context.

Inquirer:

```
/promptlvl9000 trace:full Our 480 V service — is the line-to-neutral 277 V, and what would it be on a 415 V system?
```

Response:

```
GATEKEEPER
Question: Confirm L-N voltage on a 480 V three-phase system (expected 277 V) and give the L-N value for a 415 V three-phase system.
Inputs present: none
Gaps: G1 — winding configuration of the inquirer's 480 V service not stated (blocking N — bracket: wye has a neutral, delta does not)
Decision: GO-WITH-ASSUMPTIONS
Assumptions carried: A1 — both systems are wye-connected with an accessible neutral; delta case stated in the answer

REVIEWER
Type: calculation
Complexity: 1
Premises: P1 — a 480 V three-phase system has a line-to-neutral voltage (true only for a wye / 4-wire system)
Time-sensitive: N
Scope — in: L-N for 480 V and 415 V nominal three-phase wye | out: tolerances, utilization vs service voltage, utility-specific standards
Risk flags: [figures/IDs]
Readings: single

DISPATCHER
SME: Electrical power distribution — LV three-phase systems
Research depth: 0 — formula is [K], values are [D]
Tool plan: code tool → re-run calc rows
Authority tiers in play: 6 only
Done-when: both L-N values with the calculation shown, and the wye/delta condition stated
Review mode: same-context (no subagent tool)

SME
Draft:
Yes — on a wye-connected 480 V system the line-to-neutral voltage is about 277 V (480Y/277 V). A 415 V wye system gives about 240 V line-to-neutral. Both figures assume a wye system with a neutral; a 480 V delta service has no line-to-neutral voltage at all.
Claim ledger:
C1 | In a balanced three-phase wye system, V(L-N) = V(L-L) / √3 | [K] | standard three-phase relationship (formula — exempt from knowledge check)
C2 | √3 ≈ 1.732 | [K] | mathematical constant
C3 | 480 V L-L → 277 V L-N | [D] | calc: 480 / √3 = 277.1
C4 | 415 V L-L → 240 V L-N | [D] | calc: 415 / √3 = 239.6
C5 | A delta-connected system has no neutral and therefore no L-N voltage | [K] | winding-configuration definition (exempt)
P1 | 480 V system has an L-N voltage | confirmed for wye, refuted for delta | C1, C5; configuration unknown → A1
A1 | Both systems wye with accessible neutral | [A] | Gatekeeper
Open items: inquirer's actual winding configuration (A1)

APPROVER  (review: same-context)
Pointer check    PASS — C1, C2, C5 are formula / constant / definition, not real-world figures — judged same-context
Figures/IDs      PASS — 277 and 240 are [D] with working shown
Calc re-run      PASS  `python3 -c "print(round(480/3**.5,1), round(415/3**.5,1))"` → 277.1 239.6
Knowledge check  PASS — no load-bearing [K] outside formulas, constants, definitions
Premises         PASS — P1 resolved, conditional on A1, stated in the draft
Freshness        PASS — not time-sensitive
Hedge            PASS — no [U]
Scope            PASS — Done-when met; nothing outside "in"
Tone/clarity     PASS
Discrepancies:   none
Verdict:         APPROVE

PUBLISHER — audience: inquirer, trace:full
```

**Answer**
Yes — on a wye-connected 480 V system the line-to-neutral voltage is about 277 V (480Y/277 V), and a 415 V wye system gives about 240 V line-to-neutral.
Both figures are V(L-L)/√3 and assume a wye system with a neutral. A 480 V delta service has no line-to-neutral voltage; if your service is delta, the 277 V figure does not apply.

**Verification** — 5 claims: 0 [S] · 3 [K] · 2 [D] · 1 assumption · 0 TBD
C1 [K] V(L-N) = V(L-L)/√3 for wye ← standard relationship
C2 [K] √3 ≈ 1.732 ← constant
C3 [D] 480 V → 277 V ← calc: 480 / √3 = 277.1 (re-run)
C4 [D] 415 V → 240 V ← calc: 415 / √3 = 239.6 (re-run)
C5 [K] delta has no neutral, no L-N ← winding-configuration definition
Assumptions: A1 both systems wye with accessible neutral
Premises: P1 confirmed for wye, refuted for delta (A1)
Discrepancies: none
Approver: APPROVE, reworks 0 — all tests PASS
Review: same-context (no subagent tool available)

**Open items** — A1: confirm the service is wye (4-wire); if delta, no L-N voltage exists

**Trace** — Gatekeeper GO-WA (A1) → Reviewer C1 [figures/IDs] → Dispatcher SME electrical distribution, depth 0, tools code → SME → Approver (same-context) → Publisher (inquirer)

---

# Shape of a "not verifiable" result

This is a template with placeholders, not a real run. It shows what ships when research comes up empty on a time-sensitive, figure-bearing question — a lead time, a current price, a part's status. The pipeline does not fail here; it reports honestly.

```
**Answer**
TBD — not verified: <the figure asked for> could not be confirmed from any source opened in this session.
Checked: <source 1 — what it did and did not contain>; <source 2 — same>; <connector / file — same>.
What would resolve it: <the specific document, contact, or query that would>.
<Any part of the question that WAS answerable, stated with its own ledger rows.>

**Verification** — <N> claims: <n> [S] · <n> [K] · <n> [D] · <n> assumptions · 1 TBD
C1 [U→TBD] <the figure> ← searched: <query>; fetched: <page>; result: not stated
<other rows>
Assumptions: <…> | none
Premises: <…>
Discrepancies: <e.g. source A dated X says one thing, source B dated Y says another — neither current enough> | none
Approver: APPROVE, reworks 1 — Hedge FAILED on first pass (C1 asserted "typically 14–16 weeks" with no source); resolved by converting to TBD
Review: independent (Opus 5.5, separate context)

**Open items** — C1

**Trace** — Gatekeeper GO → Reviewer C2 [figures/IDs] [current-status], time-sensitive → Dispatcher SME <domain>, depth 2, tools web_search ×2, web_fetch ×1 → SME → Approver (REWORK 1/2 → APPROVE) → Publisher (inquirer)
```

The Approver line in that template is the whole point of the skill: a plausible lead-time figure was drafted, caught by the Hedge test, and replaced with TBD before the inquirer ever saw it.
