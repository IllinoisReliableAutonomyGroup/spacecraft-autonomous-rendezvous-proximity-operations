#!/usr/bin/env python
"""Run a Verse demo script headlessly from the repository root and save every
AnalysisTree returned by Scenario.verify / verify_partitioned.

usage: python run_verse_headless.py <verse_repo_root> <demo_script> <dump_prefix>

Figures are never shown. Each verified tree is written to <dump_prefix>_<k>.json
(or .pkl if JSON serialization fails) and a line per run goes to
<dump_prefix>_runs.jsonl with the wall-clock runtime and node count.
"""
import sys, os, runpy, time, builtins, json, pickle

repo, script, prefix = sys.argv[1:4]
repo, script = os.path.abspath(repo), os.path.abspath(script)
os.chdir(repo)
sys.path[:0] = [os.path.dirname(script), repo, os.path.join(repo, "demo", "aprod")]  # script dir first: sibling modules shadow older copies under demo/aprod

import plotly.graph_objects as go, webbrowser
go.Figure.show = lambda self, *a, **k: None
webbrowser.open = webbrowser.open_new = webbrowser.open_new_tab = lambda *a, **k: True
builtins.display_figure = lambda *a, **k: None

from verse.scenario import scenario as _sc
_count = {"n": 0}

def _wrap(name):
    orig = getattr(_sc.Scenario, name)
    def wrapped(self, *a, **kw):
        t0 = time.perf_counter()
        tree = orig(self, *a, **kw)
        dt = time.perf_counter() - t0
        fn = f"{prefix}_{_count['n']}.json"; _count["n"] += 1
        try:
            tree.dump(fn)
        except Exception as e:  # fall back to pickle
            fn = fn[:-5] + ".pkl"
            with open(fn, "wb") as fh:
                pickle.dump(tree, fh)
        with open(prefix + "_runs.jsonl", "a") as fh:
            fh.write(json.dumps({"script": script, "method": name, "args": [repr(x) for x in a],
                                 "kwargs": {k: repr(v) for k, v in kw.items()},
                                 "runtime_s": dt, "nodes": len(tree.nodes), "dump": fn}) + "\n")
        print(f"[runner] {name} finished in {dt:.2f} s, {len(tree.nodes)} nodes, saved {fn}", flush=True)
        return tree
    setattr(_sc.Scenario, name, wrapped)

for _name in ("verify", "verify_partitioned"):
    _wrap(_name)

sys.argv = [script]
runpy.run_path(script, run_name="__main__")
