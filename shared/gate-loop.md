## Step 1 — Refine

### Do not do the work yet

While refining, produce no part of the answer — no partial finding, no "it looks like X", no preview. A leaked answer anchors the review: the user stops reading the prompt and starts reacting to the result.

A question *about* the prompt ("why is that in scope?") is not a work request. Answer it directly.

### Size it

- **SHORT** — a question, no files, nothing produced. TASK, UNKNOWNS, OUTPUT. Five or six lines.
- **FULL** — files, a deliverable, or a change to existing work. Every template block that applies.

Use only the blocks that apply. Leave the rest out — no `n/a` lines.

### Task type (FULL only)

Read the one matching file, `references/shared/variant-a.md` through `variant-f.md`, and add its blocks:

- **A** — Document / spec / RFQ review or extraction
- **B** — File transformation (an existing file in, a modified file out)
- **C** — Build / code / tooling
- **D** — Research / market / supplier
- **E** — Skill, prompt, or instruction editing
- **F** — General

A and D always carry the CLAIMS block (the claim-tag rules).

### Check the sources (only when files or links are referenced)

A bounded, read-only inventory so SOURCES is accurate rather than guessed — names, sizes, sheet names and row counts, page counts and headings, top-level keys, entry points. Batch the calls in one turn. Do not read content to answer anything.

Mark each source `[inventoried]` or `[user-stated, unverified]`. A referenced file that isn't there goes under "Need from you" — never write a prompt around a file that may not exist.

### Write the prompt

Use the Universal template below. `references/shared/levers.md` explains what each block defends against — read it when unsure how to fill one.

- **Decide, don't ask.** If a gap can be closed with a reasonable assumption, assume it and list it. A question is only for something that changes the result and cannot be guessed — two at most.
- **Everything inferred is listed.** If it isn't worth listing under Assumed, it isn't worth putting in the prompt. List only what changes the output; a padded list stops getting read.
- **Don't widen the ask.** A useful extra goes in one "Could also" line. It is out unless the user says to add it.

## Step 2 — Show

```
**Prompt — v1**

<the prompt, in a fenced block, copy-ready>

**Assumed** — tell me if any are wrong
1. ...

**Could also** — <one line> (say "add it")

**Need from you**
1. ...
```

Omit empty sections.

## Step 3 — Approve — the only gate

One approval, once. Use tappable options where possible — `ask_user_input_v0` with Run / Edit / Cancel — since this is often reviewed on a phone. Anything under "Need from you" that has a short list of answers goes in the same call, so one reply answers and approves.

- **Run, go, yes, do it** → run.
- **Cancel** → end the run without executing the prompt.
- **Edit without changes specified** → ask what to change.
- **Corrections, answers, struck assumptions, "add it"** → apply them and run, opening with the changed lines as v2. If the user asks to see the revision first or changes the task itself, show the revised prompt and wait for approval.
- **Can't tell whether to run** → ask once, plainly. Silence is never approval.
- **"Just the prompt"**, or a request for it as a file → hand over the prompt with its assumptions and stop. It is theirs to run elsewhere.

## After the run — the gate stays closed

Once the prompt has run, the conversation is normal again. Follow-ups, tweaks, "now do the same for the other tab", new questions — handle them directly. No new prompt, no approval, no closing report.

The approved prompt's rules — source order, unknowns as TBD, scope, the do-nots — keep applying to follow-up work on the same thing. Refine again only when the user invokes the skill again.
