#!/usr/bin/env python
"""Simulate the docking scenario (parser + 1 s proximity updates, the Table 2
configuration) N times and report where and how fast the deputy is when it
stops, plus the estimate at the moment it enters Docking.

usage: python sim_docking_terminal.py <verse_repo_root> <N> <out.json>
"""
import sys, os, json
import numpy as np

repo, N, out = os.path.abspath(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
os.chdir(repo)
sys.path[:0] = [repo, os.path.join(repo, "demo", "aprod")]
import plotly.graph_objects as go
go.Figure.show = lambda *a, **k: None

import orbital_docking_demo_ver_gpa_parser_wrapper_freq as W
from orbital_docking_agent_gpa import OrbitalAgent
from orbital_docking_sensor_gpa_parser_wrapper_freq import OrbitalSensor
from parsed_wrap import clear_parse_cache
from verse import Scenario, ScenarioConfig

if os.path.exists(W.filename):
    os.remove(W.filename)
clear_parse_cache()
scenario = Scenario(ScenarioConfig(init_seg_length=1, parallel=False))
scenario.add_agent(OrbitalAgent("deputy", file_name="./demo/aprod/orbital_docking_controller_gpa_parser_freq.py"))
scenario.set_sensor(OrbitalSensor())
T, ts, ry, n = 3000, 1, 75, W.n
base = [0, ry + 10, 0, n / 2 * ry * .9, 0, 0]
x0_l = base + [b - 2.5 for b in base] + [-2.5] * 3 + [0] * 7
x0_u = base + [b + 2.5 for b in base] + [2.5] * 3 + [0] * 7
scenario.set_init([[x0_l, x0_u]], [(W.GOMode.Passive, W.POMode.Passive, W.MoveMode.NMT)])

trees = scenario.simulate_multi(T, ts, num_sims=N)
if hasattr(trees, "nodes"):
    trees = [trees]

def parent_of(tree, nd):
    return next((p for p in tree.nodes if nd in p.child), None)

rows = []
for i, tree in enumerate(trees):
    leaves = [nd for nd in tree.nodes if not nd.child]
    entry = next((nd for nd in tree.nodes if "Docking" in nd.mode["deputy"] and len(nd.trace.get("deputy", [])) > 0), None)
    # closest approach over the whole run
    allrows = np.array([r for nd in tree.nodes for r in nd.trace.get("deputy", [])], dtype=float)
    rn = np.linalg.norm(allrows[:, 1:4], axis=1); k = int(rn.argmin())
    for nd in leaves:
        hits = nd.assert_hits.get("deputy") if nd.assert_hits else None
        while nd is not None and len(nd.trace.get("deputy", [])) == 0:   # a node created after an assert has no trace
            nd = parent_of(tree, nd)
        s = np.array(nd.trace["deputy"][-1], dtype=float)  # t, x,y,z, vx,vy,vz, hx..., ex..., timer, po_timer, a-, a+
        rows.append({
            "sim": i, "t_end": s[0], "modes": list(nd.mode["deputy"]),
            "assert_hits": hits,
            "closest_r_km": float(rn[k]), "closest_t": float(allrows[k, 0]), "closest_v_kms": float(np.linalg.norm(allrows[k, 4:7])),
            "r_true_km": float(np.linalg.norm(s[1:4])), "v_true_kms": float(np.linalg.norm(s[4:7])),
            "r_est_km": float(np.linalg.norm(s[7:10])), "err_pos_km": float(np.linalg.norm(s[13:16])),
            # first trace row of the Docking node: [t, x, y, z, vx, vy, vz, hx, hy, ...]
            "entry_t": float(entry.trace["deputy"][0][0]) if entry is not None else None,
            "entry_true_xy": [float(v) for v in entry.trace["deputy"][0][1:3]] if entry is not None else None,
            "entry_est_xy": [float(v) for v in entry.trace["deputy"][0][7:9]] if entry is not None else None,
        })

json.dump(rows, open(out, "w"), indent=1)
r = np.array([x["r_true_km"] for x in rows]); v = np.array([x["v_true_kms"] for x in rows]); te = np.array([x["t_end"] for x in rows])
docked = sum(1 for x in rows if x["assert_hits"])
print(f"[sim] {len(rows)} terminal states from {len(trees)} sims; {docked} stopped by the Docked assert, {len(rows)-docked} ran to the horizon")
print(f"[sim] terminal |r| km: min {r.min():.4f} max {r.max():.4f} | terminal |v| m/s: min {1e3*v.min():.3f} max {1e3*v.max():.3f} | t_end: min {te.min():.0f} max {te.max():.0f}")
cr = np.array([x["closest_r_km"] for x in rows]); ct = np.array([x["closest_t"] for x in rows]); cv = np.array([x["closest_v_kms"] for x in rows])
print(f"[sim] closest approach |r| km: min {cr.min():.4f} max {cr.max():.4f} at t in [{ct.min():.0f}, {ct.max():.0f}] s, |v| there m/s: min {1e3*cv.min():.3f} max {1e3*cv.max():.3f}")
ex = [x for x in rows if x["entry_est_xy"]]
if ex:
    d = np.array([[a - b for a, b in zip(x["entry_est_xy"], x["entry_true_xy"])] for x in ex])
    print(f"[sim] Docking entry: t in [{min(x['entry_t'] for x in ex):.0f}, {max(x['entry_t'] for x in ex):.0f}] s; est-true offset km: x in [{d[:,0].min():.3f}, {d[:,0].max():.3f}], y in [{d[:,1].min():.3f}, {d[:,1].max():.3f}]; true xy range x [{min(x['entry_true_xy'][0] for x in ex):.2f}, {max(x['entry_true_xy'][0] for x in ex):.2f}] y [{min(x['entry_true_xy'][1] for x in ex):.2f}, {max(x['entry_true_xy'][1] for x in ex):.2f}]")
