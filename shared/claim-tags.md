## Claim tags

Every factual claim in a draft or deliverable carries one tag.

| Tag | Meaning | In the final output |
|---|---|---|
| `[S]` | Sourced — from a tool result opened this session: fetched page, search result read, connector record, attached file, memory file. Pointer required. | Yes. Resting on one secondary source only → `[S] single-source`. |
| `[K]` | Established knowledge — stable, textbook/standard, low drift. | Yes, subject to the knowledge check |
| `[D]` | Derived — computed or reasoned from `[S]`/`[K]` inputs; working shown. | Yes |
| `[A]` | Assumption — declared at Stage 0 or in an approved prompt's assumption ledger. | Yes, labelled as an assumption |
| `[U]` | Unverified — could not be grounded. | Never as an assertion. Ships as `TBD — not verified: <what was checked>` or is omitted. |

### Hard rules

1. Real-world figures and identifiers — ratings, specs, prices, lead times, dates, counts, part numbers, standards clause numbers, names, quotations, URLs — must be `[S]` or `[D]`. `[K]` is not enough. Formulas and mathematical constants may be `[K]`.
2. A pointer must be something opened this session. A source remembered from training is `[U]`, however confident it feels.
3. Anything flagged time-sensitive needs `[S]`. `[K]` on a time-sensitive item is downgraded to `[U]`.
4. "Not findable" is a valid answer. Say what was checked and what would resolve it.
5. **Knowledge check.** A `[K]` claim is *load-bearing* if removing it changes the bottom line. At research depth ≥ 1, every load-bearing `[K]` that is not a formula, constant or definition is checked against a source: it becomes `[S]`, or `[U]` if the source contradicts it or cannot be found. At depth 0, load-bearing `[K]` claims are listed as `Unchecked [K]` in the verification output — never silently passed.

### Source authority

When sources conflict, the higher tier wins and the conflict goes in the discrepancy register. Never resolve a conflict silently. An approved prompt's SOURCES order, when one exists, ranks above this list.

1. Inputs the user supplied this session — files, pasted data, stated facts
2. Connected systems the user controls — SharePoint, Asana, mail, CRM, etc.
3. Memory files
4. Primary external sources — manufacturer, standards body, government, vendor documentation
5. Secondary external sources — reputable press, reference sites
6. Established knowledge `[K]`

Nothing outside this list is a source.

### Ledger rows

```
C<n> | <atomic claim> | [tag] | <pointer: URL + what it says / file + section / record / calc: inputs → result>
P<n> | <premise> | confirmed / refuted / unverified | <pointer>
A<n> | <assumption> | [A] | <who declared it>
```

One row per atomic claim. A figure or name in a deliverable with no ledger row is a defect.
