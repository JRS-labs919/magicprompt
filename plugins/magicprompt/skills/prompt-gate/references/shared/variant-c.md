# Variant C — Build / code / tooling

Add to the template:

```
STEP 0 — DISCOVERY
Map the relevant code and state the entry point before changing anything.
If <component> cannot be located, that is a hard stop — do not build around
it or reimplement it.

CHANGE DISCIPLINE
No features beyond the stated list. No refactoring of adjacent code.
No renaming. No reformatting of untouched regions.

VERIFICATION
Run <test/validation> and print the command and its output
(references/shared/gate-report.md).
State explicitly which behaviors were verified and which were not.
If a check fails in the test environment but would pass in the real one,
say so and say why — do not call it working.

PERSISTENCE
State whether the change takes effect immediately or requires an install,
commit, or deploy step by the user.
```

**Why Step 0:** when the entry point is unknown, the reliable move is discovery, not assumption. A prompt that asks for a fix without naming where the code lives produces a plausible fix in the wrong place.

**Why the environment caveat:** test-harness artifacts get reported as real failures and real failures get dismissed as harness artifacts. Naming which one it is, with the reason, keeps that honest.

**Why persistence:** an edit that never reaches the user's repo or profile leaves every other session running the old version, and the resulting "it didn't work" is unexplainable without this line.
