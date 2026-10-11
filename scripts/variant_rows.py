#!/usr/bin/env python
"""Summarize docking parameter variants into table rows.

usage: python variant_rows.py <verse_repo_root> <results_dir> <name:label> [<name:label> ...]
For each variant <name>: reads <name>_runs.jsonl (runtime), <name>.log (A/I, F/I as printed),
<name>_simbase.json (A/I Sim, F/I Sim), and evaluates the two docking verdicts on <name>_0.json
with scripts/verdicts.py (eps_G = 10 km, B = [6,11]x[-75,-71] km). Prints LaTeX rows in \revb.
"""
import sys, os, json, re, subprocess
repo, rdir = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
here = os.path.dirname(os.path.abspath(__file__))
for spec in sys.argv[3:]:
    name, label = spec.split(":", 1)
    runs = [json.loads(l) for l in open(f"{rdir}/{name}_runs.jsonl")]
    rt = runs[0]["runtime_s"]
    log = open(f"{rdir}/{name}.log").read()
    m = re.search(r"F/I: ([0-9.]+), A/I: ([0-9.]+)", log); fi, ai = float(m.group(1)), float(m.group(2))
    sb = json.load(open(f"{rdir}/{name}_simbase.json"))
    out = subprocess.run([sys.executable, f"{here}/verdicts.py", repo, runs[0]["dump"], "--eps-g", "10", "--v-g", "1e9",
                          "--box", "8.5", "-73", "2.5", "2", "--json", f"{rdir}/{name}_verdict.json"],
                         capture_output=True, text=True, env={**os.environ, "PYTHONWARNINGS": "ignore"}).stdout
    goal = "VERIFIED" in out.split("MISSION GOAL")[1].split("\n")[0]
    mode = ("VERIFIED" in out.split("MODE-ENTRY")[1].split("\n")[0]) if "MODE-ENTRY" in out else None
    entries = re.findall(r"entry into Docking at t=(\d+): estimate box x\[([-0-9.]+),([-0-9.]+)\] y\[([-0-9.]+),([-0-9.]+)\]", out)
    verdict = "verified" if (goal and mode) else ("inconclusive" if goal else "not verified (goal)")
    print(f"% {name}: runtime {rt:.1f} s, A/I {ai:.2f}, F/I {fi:.2f}, A/I Sim {sb['A/I Sim']:.2f}, F/I Sim {sb['F/I Sim']:.2f}; goal {'ok' if goal else 'FAIL'}; mode-entry {'ok' if mode else 'FAIL'}; entries {entries}")
    print(f"\\revb{{{label}}} & \\revb{{18}} & \\revb{{{rt:.2f}}} & \\revb{{{ai:.2f}}} & \\revb{{{fi:.2f}}} & \\revb{{{sb['A/I Sim']:.2f}}} & \\revb{{{sb['F/I Sim']:.2f}}} & \\revb{{{verdict}}} \\\\ \\hline")
