## Phase 1 — Compile

### Do not do the work

This is the load-bearing rule. During the compile turn, produce no part of the answer — no partial finding, no "the answer is likely X", no preliminary read of the actual content, no hedged preview. A leaked answer anchors the review and defeats the entire purpose: the user stops reviewing the prompt and starts reacting to the result.

If the request is trivial enough that compiling feels like overhead, compile a short prompt anyway. A consistent gate the user can rely on beats a fuzzy escape hatch that fires inconsistently.

The one exception: a conversational question *about* this skill or about a prompt already compiled ("what does authority hierarchy mean?", "why did you put that in scope?") is not a work request. Answer it directly and stay in the gate.

A new work request later in the same thread re-enters at Phase 1 and gets its own prompt. Only questions about output already delivered stay ungated.

### Classify the task

Pick the closest variant and read only its file — `references/shared/variant-a.md` through `variant-f.md`:

- **A — Document / spec / RFQ review or extraction**
- **B — File transformation** (an existing file in, a modified file out)
- **C — Build / code / tooling**
- **D — Research / market / supplier**
- **E — Skill, prompt, or instruction editing**
- **F — General** (none of the above; use the universal template only)

Some requests span two. Compile against the primary one and pull the extra blocks that matter from the second. Variants A and D always carry the CLAIMS block (the claim-tag rules).

### Inventory the sources — read-only, no analysis

If files are attached or referenced, run a bounded inventory so the SOURCES block is accurate rather than guessed. Batch the inventory calls in one turn:

- names, types, sizes; directory listings
- spreadsheets: sheet names, row/column counts, table ranges
- documents: page count, section headings
- JSON: top-level keys
- code: entry points and file structure

Stop there. Do not read content to answer anything, do not open linked or downstream files, do not start reconciling. If the inventory raises a question, that question belongs in the compiled prompt, not in a resolution you perform now.

Mark each SOURCES entry as `[inventoried]` or `[user-stated, unverified]`. If the user referenced a file that isn't actually present, say so in the open questions — do not compile a prompt around a file that may not exist.

If there are no sources, skip this step entirely.

Then mark each source reachable / size-limited / auth-walled / unverified, and each planned gate item `[script]` or `[judgment]` and runnable-here or not. A gate item that cannot run in this environment is not a gate — say so before the gate, not after. Note whether a subagent tool exists; that decides whether review will be independent or same-context (`references/shared/reviewer-agent.md`).

### Pick the depth

- **MINIMAL** — no sources, no artifact produced, nothing irreversible, one factual answer. Six lines is plenty: task, unknown rule, output shape.
- **STANDARD** — one source or one artifact, bounded work. Every block present, each terse.
- **FULL** — multiple sources, transformation of existing data, anything irreversible, or anything feeding a downstream system of record. Review by reviewer-agent when a subagent tool exists.

Default to STANDARD. Move to FULL whenever existing data could be degraded.

### Build the prompt

Use the Universal template section below and the blocks from the one variant file. At STANDARD and FULL, read `references/shared/levers.md` first — it says what each block defends against. At MINIMAL, skip it. Every block gets filled or explicitly marked `n/a` — a silently omitted block is exactly the gap this skill exists to close.

At MINIMAL this reverses — keep TASK, UNKNOWNS, OUTPUT, drop the rest outright rather than printing `n/a`. Dropping blocks is a failure at STANDARD/FULL only.

Two rules govern what goes in:

**Nothing enters the prompt that the user didn't say without being logged.** Every inferred line gets an entry in the assumption ledger. If it isn't worth logging, it isn't worth putting in the prompt.

**Scope never expands silently.** If the request should plausibly be wider — an obvious adjacent check, a related sheet, a second failure mode — that goes in a separate `PROPOSED ADDITIONS` block the user can strike wholesale. Never fold it into the main scope.

## Phase 2 — Present

Exact structure:

```
**Compiled prompt — v1** (variant X, depth Y)

<the prompt, in a fenced block, copy-ready>

**Assumptions** — strike anything wrong
1. ...
2. ...

**Proposed additions** — not in your ask; say the word to drop them
- ...

**Open questions** — I can't assume these
1. ...
```

Then call the gate.

Keep the assumption ledger to what actually changes the output. "I assumed you want this in a file" matters. "I assumed you want it written in English" does not. A padded ledger stops getting read, which is the same as having no ledger.

Omit empty sections rather than printing them with "none".

## Phase 3 — Gate

Ask for approval with tappable options where possible — `ask_user_input_v0` — since this is often reviewed on a phone. Fall back to a plain question if unavailable.

- Options: Approve / Edit / Cancel. When proposed additions exist: Approve with additions / Approve without additions / Edit / Cancel — an approval never leaves the additions' status ambiguous.
- Open questions that have a short list of possible answers go in the same call as the gate (three questions maximum, gate included), so one reply can answer and approve. Open-ended questions are asked in prose above it.

Reading the reply:

- **Gate words** — "yes", "go", "run it", "approved", "ship it", "do it" → execute.
- **Any edit, correction, or struck assumption** → apply it, increment the version, re-present. On a re-present, show only the changed lines plus the new version number, not the whole prompt again — unless the changes are extensive enough that a full reprint is clearer.
- **Answers to open questions with no gate word** → fold them in, show the delta, ask once more. Do not treat an answer as approval.
- **Answers plus a gate word in the same reply** → fold the answers in, increment the version, and execute — opening with the changed lines so the user sees exactly what ran. If an answer changes scope, sources or output rather than filling a blank, re-present instead.
- **Ambiguous reply** → treat as an edit, not as approval. Silence is never approval.
- **Every re-present ends with a gate call.** A delta shown without one is a soft gate.

The version number matters in a long thread. Reference prompts as v1/v2/v3 so there is never doubt about which one is in force.

If the user asks for the prompt as a file to route to someone else, write it to `/mnt/user-data/outputs/` and present it. Not the default — inline is lower friction.

The exported file carries the ledger, the version, and any open questions, marked unapproved — a fenced prompt alone reads as settled instruction.
