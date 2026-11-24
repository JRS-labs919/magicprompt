#!/usr/bin/env python3
"""Magicprompt release gate. Prints every check with its evidence; exits 1 on any FAIL."""
import json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "magicprompt"
SK = PLUGIN / "skills"
results = []
def check(name, ok, detail=""):
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))

# 1 plugin.json
pj = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text())
check("plugin.json name/version", pj.get("name") == "magicprompt" and re.fullmatch(r"\d+\.\d+\.\d+", pj.get("version", "")) is not None,
      f"name={pj.get('name')} version={pj.get('version')}")
check("CHANGELOG has this version", f"## {pj['version']}" in (ROOT / "CHANGELOG.md").read_text())
marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
entry, = marketplace["plugins"]
check("marketplace points to the packaged plugin",
      entry["name"] == pj["name"] and entry["source"] == "./plugins/magicprompt")

# 2 manifest / shared coverage
manifest = {k: v for k, v in json.loads((ROOT / "shared-manifest.json").read_text()).items() if not k.startswith("_")}
skills = sorted(p.name for p in (ROOT / "src").iterdir() if p.is_dir())
check("manifest covers all src skills", sorted(manifest) == skills, f"skills={skills}")
masters = {p.name for p in (ROOT / "shared").glob("*.md")}
used = {f for v in manifest.values() for f in v["lazy"]}
for s in skills:
    used |= set(re.findall(r"\{\{include: ([\w.-]+)\}\}", (ROOT / "src" / s / "SKILL.md").read_text()))
check("every used shared file exists", used <= masters, f"missing={sorted(used - masters)}")
check("no orphan shared file", masters <= used, f"orphans={sorted(masters - used)}")

# 3 generated skills match src + shared
r = subprocess.run([sys.executable, str(ROOT / "scripts/build.py"), "--check"], capture_output=True, text=True)
check("skills/ matches a fresh build", r.returncode == 0, r.stdout.strip().replace("\n", "; "))

# 4 frontmatter, size, leftovers
total_desc = 0
for s in skills:
    txt = (SK / s / "SKILL.md").read_text()
    m = re.match(r"---\n(.*?)\n---\n", txt, re.S)
    fm = dict(l.split(": ", 1) for l in m.group(1).splitlines() if ": " in l) if m else {}
    d = fm.get("description", ""); total_desc += len(d); lines = txt.count("\n")
    check(f"{s}: frontmatter", fm.get("name") == s and 0 < len(d) <= 1024 and "<" not in d and ">" not in d, f"desc={len(d)} chars")
    check(f"{s}: SKILL.md within 500 lines, no unresolved include", lines <= 500 and "{{include" not in txt, f"{lines} lines")

# 5 every referenced path resolves inside its own skill folder
for s in skills:
    refs = set()
    for md in (SK / s).rglob("*.md"):
        refs |= set(re.findall(r"references/[\w/.-]+\.md", md.read_text()))
    bad = sorted(x for x in refs if not (SK / s / x).exists())
    check(f"{s}: {len(refs)} referenced paths resolve", not bad, f"unresolved={bad}" if bad else "")
for s in ("prompt-gate", "gate-and-verify"):
    have = sorted(p.name for p in (SK / s / "references/shared").glob("variant-*.md"))
    check(f"{s}: six variant files", len(have) == 6, ",".join(have))

# 6 carry-over: rules from the originals + new behaviours present in each skill's effective text
corpus = lambda s: "\n".join(p.read_text() for p in (SK / s).rglob("*.md"))
required = {
    "prompt-gate": ["Do not do the work yet", "Silence is never approval", "the gate stays closed", "Decide, don't ask",
                    "the only gate", "Don't stop to check in", "HARD STOPS", "Calls I made", "Just the prompt",
                    "A failed check gets fixed, not parked", "Re-gating", "Stopping to check in", "Second approval",
                    "SHORT", "[inventoried]", "Could also", "disable-model-invocation: true", "Flag, do not resolve",
                    "PRE-EDIT INVENTORY", "STEP 0 — DISCOVERY", "SEARCH FIRST", "EXACT CHANGE LIST", "Drift signals",
                    "What does not work", "Bare PASS", "[script]", "reviewer-agent", "Over-reading"],
    "promptlvl9000": ["GO-WITH-ASSUMPTIONS", "HOLD", "Maximum two rework loops", "Real-world figures and identifiers",
                      "A pointer must be something opened this session", "Fast path", "trace:full", "Done-when",
                      "Hedge", "Premises", "audience:team", "Not for casual chat", "Gatekeeper interrupts", "Source authority",
                      "Knowledge check", "same-context", "Calc re-run", "Opus 5.5", "Role-played panel", "Assumptions:",
                      "Tool-call budget", "Budget creep", "tappable options"],
    "gate-and-verify": ["Do not do the work yet", "Silence is never approval", "the gate stays closed", "the only gate",
                        "HARD STOPS", "No new GO/HOLD decision", "Maximum two rework loops", "Real-world figures and identifiers",
                        "CLAIMS", "Stage 0", "Second gatekeeping", "Re-gating", "Nothing is withheld",
                        "disable-model-invocation: true", "Knowledge check", "[script]", "Tool-call budget"],
}
for s, phrases in required.items():
    c = corpus(s); miss = [p for p in phrases if p not in c]
    check(f"{s}: {len(phrases)} required rules present", not miss, f"missing={miss}" if miss else "")

# 6b rules retired in 1.2.0 must not survive anywhere in the gate skills
retired = ["re-enters at Phase 1", "Stop triggers are real stops", "A failed gate item blocks the artifact", "STOP AND ASK IF",
           "Every re-present ends with a gate call", "MINIMAL", "STANDARD"]
for s_ in ("prompt-gate", "gate-and-verify"):
    hit = [p_ for p_ in retired if p_ in corpus(s_)]
    check(f"{s_}: {len(retired)} retired rules absent", not hit, f"still present={hit}" if hit else "")

# 7 load budgets — bytes actually read per run, against the pre-optimisation baselines
def load(s, *lazy):
    return (SK / s / "SKILL.md").stat().st_size + sum((SK / s / "references/shared" / f).stat().st_size for f in lazy)
BASE = {"prompt-gate original": 24732, "promptlvl9000 v1.0.0": 21960, "gate-and-verify v1.0.0": 41086}
paths = [
    ("prompt-gate SHORT",                    load("prompt-gate"), 1, "prompt-gate original"),
    ("prompt-gate FULL (variant B)",         load("prompt-gate", "variant-b.md", "gate-report.md"), 3, "prompt-gate original"),
    ("prompt-gate FULL research + reviewer", load("prompt-gate", "variant-d.md", "claim-tags.md", "gate-report.md", "reviewer-agent.md"), 5, None),
    ("promptlvl9000, chat",                  load("promptlvl9000"), 1, "promptlvl9000 v1.0.0"),
    ("promptlvl9000 + reviewer agent",       load("promptlvl9000", "reviewer-agent.md"), 2, "promptlvl9000 v1.0.0"),
    ("gate-and-verify (variant D, chat)",    load("gate-and-verify", "variant-d.md", "gate-report.md"), 3, "gate-and-verify v1.0.0"),
]
for name, size, files, base in paths:
    if base:
        b = BASE[base]
        check(f"load: {name}", size <= b, f"{size} bytes in {files} files vs {b} ({base}) → {100 * (size - b) / b:+.0f}%")
    else:
        print(f"INFO  load: {name} — {size} bytes in {files} files (no earlier equivalent)")
print(f"INFO  descriptions loaded every session — {total_desc} chars total (v1.0.0: 1652; standalone prompt-gate alone: 899)")

# 8 skill-creator quick_validate. Its key allowlist omits `disable-model-invocation`, which the runtime
# accepts (the installed standalone prompt-gate carries it), so validate a copy with only that key removed.
qv = Path("/mnt/skills/examples/skill-creator/scripts/quick_validate.py")
installed = Path("/mnt/skills/plugins/prompt-gate/SKILL.md")
if qv.exists():
    for s in skills:
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td) / s; shutil.copytree(SK / s, tmp)
            sk = tmp / "SKILL.md"; t = sk.read_text(); stripped = "disable-model-invocation: true\n" in t
            sk.write_text(t.replace("disable-model-invocation: true\n", ""))
            r = subprocess.run([sys.executable, str(qv), str(tmp)], capture_output=True, text=True, cwd=str(qv.parent.parent))
        check(f"{s}: quick_validate" + (" (disable-model-invocation exempted)" if stripped else ""), r.returncode == 0,
              (r.stdout + r.stderr).strip().splitlines()[-1])
    if installed.exists():
        check("disable-model-invocation accepted by runtime", "disable-model-invocation: true" in installed.read_text(), f"present in installed {installed}")
else:
    print("NOT RUN  quick_validate — skill-creator not present in this environment")

fails = results.count(False)
print(f"\nSummary: {len(results)} checks · {fails} fail")
sys.exit(1 if fails else 0)
