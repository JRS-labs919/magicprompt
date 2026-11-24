# Variant E — Skill, prompt, or instruction editing

Add to the template:

```
EXACT CHANGE LIST
<numbered, each one a single change>

CROSS-REFERENCES
Do not reference other skills, projects, or prompts inside this one
unless explicitly listed above.

NO ADDED BEHAVIOR
No steps, gates, examples, or behavior beyond the numbered list.

REVIEW BEFORE PACKAGING
Show the diff of the instruction file before packaging or finalizing.

PERSISTENCE
State whether the edit is live immediately or requires the user to
install the package first.
```

**Why the cross-reference line:** a helpfully-added pointer to a sibling skill is invisible in a diff-free review and changes runtime behavior in every future invocation. It has to be opt-in.
