# Variant B — File transformation

The highest-risk variant. An existing artifact goes in and a modified one comes out, and losses are silent.

Add to the template:

```
PRE-EDIT INVENTORY (print it)
Record count per sheet or section, cell notes, embedded images, hyperlinks,
data validations, defined names, external links, hidden rows, macros.

POST-EDIT INVENTORY (print side-by-side against pre-edit)
Same list. Any delta is a failure — restore what was lost and re-run the
inventory. If it cannot be restored, report it first and mark the file not safe to use.

EXPLICITLY CONFIRM CARRIED OVER
Cell notes, embedded images, hyperlinks.
These are dropped silently by common libraries; absence produces no error.

SOURCE-DEFECT CHECK
Preserved exactly is not the same as correct. If a preserved element looks
structurally wrong in the SOURCE — offset links, orphaned references,
stranded data outside a table boundary — flag it. Do not propagate it cleanly.
```

**Why both halves matter:** a rebuild can drop dozens of cell notes and an embedded image without a single error message, and a hyperlink block can be offset by a fixed number of rows across half a tab — and survive a faithful rebuild *because* the rebuild was faithful. The first half catches loss. The second catches inherited defects. Neither catches the other.

**On row remapping:** when records move, verify each carried-over annotation landed on the same record by matching a stable key, not by position.
