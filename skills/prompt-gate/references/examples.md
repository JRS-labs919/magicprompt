# Worked Examples

Read when the right depth or shape is unclear. Three examples: MINIMAL, STANDARD, FULL.

---

## Example 1 — MINIMAL

**The ask:** "what's the standard date format for a sortable filename"

No sources, no artifact, nothing irreversible. Do not compile a thirty-line contract for this.

```
**Compiled prompt — v1** (variant F, MINIMAL)

TASK
Give a standard date format that sorts chronologically in filenames.

UNKNOWNS
If the files include dates and times, explain what changes for timestamps.

OUTPUT
Inline. Give one example filename.
```

**Assumptions** — strike anything wrong
1. Use whole calendar dates in filenames.

**Open questions** — none.

*Note the ledger has one entry, not five. Only things that change the answer.*

---

## Example 2 — STANDARD

**The ask:** "check whether the links on the Orders tab point to the right invoices"

One source, bounded, read-only, produces a finding rather than an artifact.

```
**Compiled prompt — v1** (variant B/A, STANDARD)

TASK
Audit the hyperlinks on the Orders tab of <workbook> against the
row data they sit on, and report mismatches.

SOURCES (authority order)
1. <workbook>, Orders tab — the rows under audit [inventoried: 41 data rows, 38 hyperlinks]
2. The linked invoices — ground truth for what each link points at [user-stated, unverified]

SCOPE
Change only: nothing. Read-only audit.
Out of scope: fixing anything found; the other seven tabs.

UNKNOWNS
A row whose correct target cannot be determined from the sheet data →
report as UNDETERMINED with what is known. Do not guess the intended target.

VERIFICATION GATE (report each, pass or fail)
- every one of the 41 rows accounted for: correct / mismatched / no link / undetermined
- counts sum to 41
- for each mismatch, name both the linked file and the file the row data implies

OUTPUT
Inline. Mismatches first, numbered, with row numbers. Then a one-line
pattern statement if the mismatches are systematic rather than random.
Do not produce: a corrected workbook.

DO NOT
- open invoice files beyond those needed to establish the mismatch pattern
- comment on pricing or spec content
```

**Assumptions** — strike anything wrong
1. Read-only — you want the finding before any fix.
2. Mismatch is judged against the row's invoice number and billing date.
3. Three linked files sampled is enough to establish a pattern; more only if it's not systematic.

**Proposed additions** — not in your ask; say the word to drop them
- Flag rows with no hyperlink at all, not just wrong ones.

**Open questions**
1. If the offset turns out to be systematic, do you want the fix in the same pass or as a separate approved step?

*Note the OUTPUT block bans the corrected workbook. Without that line, a helpful fix arrives unrequested and the audit becomes unreviewable.*

---

## Example 3 — FULL

**The ask:** "clean up this workbook so it's readable, don't lose anything"

Existing artifact in, modified artifact out, feeding a downstream system of record. Highest risk. Every block earns its place.

```
**Compiled prompt — v1** (variant B, FULL)

TASK
Improve the readability and layout of <workbook> and emit <workbook v-next>.

SOURCES (authority order)
1. <workbook> — the only source; its data is ground truth [inventoried: 8 tabs, 234 records, 39 cell notes, 1 embedded image, 229 formulas]

SCOPE
Change only: column widths, wrap, number formats, banding, gridline display,
header placement, outline grouping, navigation links.
Leave unchanged: every cell VALUE, every note, every hyperlink target, the
embedded image, every formula result — verify by cell-level diff and hash.
Out of scope: correcting data errors; consolidating duplicates; changing
formulas; renaming columns; touching the FX rate basis.

UNKNOWNS
Ambiguity about whether something is data or presentation → treat as data,
leave it alone, and list it. Do not decide.

PRE-EDIT INVENTORY (print it)
Per tab: record count, cell notes, embedded images, hyperlinks, data
validations, defined names, external links, hidden rows, macros, table ranges.

POST-EDIT INVENTORY (print side-by-side)
Same list. Any delta is a failure — stop and report, do not present.

SOURCE-DEFECT CHECK
Flag anything structurally wrong in the SOURCE — links offset from their
rows, data stranded outside a table boundary, hidden rows masking live
records, a table range short of the last column. Flag only; do not fix.
Preserving a defect faithfully still ships the defect.

STOP AND ASK IF
- a formatting change would require moving a cell value
- two tabs disagree on a shared value
- an element cannot be carried over by the available library

VERIFICATION GATE (report each, pass or fail)
- 234 records in / 234 out, cell values identical
- 39 notes in / 39 out, each landed on the same record matched by part number
- embedded image byte-identical
- formula count and results unchanged
- hyperlink targets unchanged, count unchanged
- zero macros, zero external links introduced

OUTPUT
One .xlsx in outputs, version-incremented filename. Changelog tab documenting
every change made. Present the workbook first.
Do not produce: a summary document, a PDF, or a second variant.

DO NOT
- silently drop anything the library cannot round-trip
- reformat in a way that changes how a value parses
- present output without printing the gate results
```

**Assumptions** — strike anything wrong
1. "Don't lose anything" covers notes, images, and hyperlinks — not just cell values.
2. Presentation-only means formulas are untouched, including the duplicated FX rate.
3. New file, version-incremented; the original stays intact.

**Proposed additions** — not in your ask; say the word to drop them
- A changelog tab.
- Flagging (not fixing) source defects found during the pass.

**Open questions**
1. Which spreadsheet apps need to display the workbook correctly?

*Note the two independent halves of the gate: the inventory diff catches loss, the source-defect check catches inherited errors. A workbook can pass the first perfectly while shipping a broken link block.*

---

## Calibration notes

- **Ledger length tracks risk, not prompt length.** The FULL example has three assumptions. Three that matter beat twelve that don't.
- **`Do not produce` is doing real work** in examples 2 and 3. The unrequested helpful extra is a frequent failure and one line prevents it.
- **Proposed additions stay outside the prompt block.** They are struck by a word, not edited out of a fenced block on a phone.
- **Open questions are things that cannot be assumed** — not things that could be assumed and logged. If it can go in the ledger, it goes in the ledger; a long question list stalls the gate.
