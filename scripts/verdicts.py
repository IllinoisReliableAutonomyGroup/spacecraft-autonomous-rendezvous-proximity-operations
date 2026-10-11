#!/usr/bin/env python
"""Compute the two docking verdicts from a saved Verse AnalysisTree.

usage: python verdicts.py <verse_repo_root> <tree.json|tree.pkl> [--agent deputy]
                          [--eps-g KM] [--v-g M_PER_S] [--box X0 Y0 HALF_X HALF_Y]
                          [--pos 1 2 3] [--vel 4 5 6] [--est 7 8 9] [--mode-name Docking]

Mission goal (containment, sound as a sufficient condition):
  every leaf box L_j (branch ended by the Docked assert or by the horizon)
  must satisfy max_{x in L_j} ||r|| <= eps_g and max ||v|| <= v_g.
Mode-entry condition (intersection, sound as a necessary condition):
  at every node where the mode first becomes <mode-name>, the box of the
  estimated position must lie inside the box B = [x0 +- hx] x [y0 +- hy].
Trace rows of a verified tree alternate lower/upper bounds: [t, lo...], [t, hi...].
"""
import sys, os, argparse, pickle, json
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("repo"); ap.add_argument("tree")
ap.add_argument("--agent", default="deputy")
ap.add_argument("--eps-g", type=float, default=5.0)      # km
ap.add_argument("--v-g", type=float, default=10.0)       # m/s
ap.add_argument("--box", type=float, nargs=4, default=None)  # x0 y0 half_x half_y (km), estimate frame
ap.add_argument("--pos", type=int, nargs=3, default=[1, 2, 3])
ap.add_argument("--vel", type=int, nargs=3, default=[4, 5, 6])
ap.add_argument("--est", type=int, nargs=3, default=[7, 8, 9])
ap.add_argument("--mode-name", default="Docking")
ap.add_argument("--json", default=None, help="write a machine-readable summary here")
a = ap.parse_args()

sys.path.insert(0, os.path.abspath(a.repo))
from verse.analysis.analysis_tree import AnalysisTree
tree = pickle.load(open(a.tree, "rb")) if a.tree.endswith(".pkl") else AnalysisTree.load(a.tree)

def box_at(node, which):
    """(lo, hi) arrays without the time column; which = 0 first step, -1 last step."""
    tr = np.array(node.trace[a.agent], dtype=float)
    if which == 0:
        lo, hi = tr[0, 1:], tr[1, 1:]
    else:
        lo, hi = tr[-2, 1:], tr[-1, 1:]
    return np.minimum(lo, hi), np.maximum(lo, hi), tr[0, 0], tr[-1, 0]

def norm_range(lo, hi, idx):
    lo, hi = lo[[i - 1 for i in idx]], hi[[i - 1 for i in idx]]   # idx counts from 1 after t
    far = np.maximum(np.abs(lo), np.abs(hi))
    near = np.where((lo <= 0) & (hi >= 0), 0.0, np.minimum(np.abs(lo), np.abs(hi)))
    return float(np.linalg.norm(near)), float(np.linalg.norm(far))

leaves = [nd for nd in tree.nodes if not nd.child]
rows, ok_all = [], True
for nd in leaves:
    lo, hi, t0, t1 = box_at(nd, -1)
    rmin, rmax = norm_range(lo, hi, a.pos); vmin, vmax = norm_range(lo, hi, a.vel); emin, emax = norm_range(lo, hi, a.est)
    hits = nd.assert_hits.get(a.agent) if nd.assert_hits else None
    ok = (rmax <= a.eps_g) and (1e3 * vmax <= a.v_g)
    ok_all &= ok
    rows.append(dict(t_end=t1, modes=list(nd.mode[a.agent]), assert_hits=hits, r_true_km=[rmin, rmax],
                     v_true_mps=[1e3 * vmin, 1e3 * vmax], r_est_km=[emin, emax], in_goal=bool(ok)))
    print(f"leaf t_end={t1:7.1f}  modes={'/'.join(nd.mode[a.agent]):28s} assert={hits}  |r| in [{rmin:.4f},{rmax:.4f}] km  |v| in [{1e3*vmin:.3f},{1e3*vmax:.3f}] m/s  |r_hat| in [{emin:.4f},{emax:.4f}] km  -> {'in G' if ok else 'NOT in G'}")
print(f"\nMISSION GOAL (eps_G={a.eps_g} km, v_G={a.v_g} m/s): {'VERIFIED' if ok_all else 'NOT VERIFIED'} over {len(leaves)} leaves "
      f"({sum(1 for r in rows if r['assert_hits'])} stopped by assert, {sum(1 for r in rows if not r['assert_hits'])} at the horizon)")

entries = []
for nd in tree.nodes:
    if a.mode_name in nd.mode[a.agent]:
        parent = next((p for p in tree.nodes if nd in p.child), None)
        if parent is None or a.mode_name not in parent.mode[a.agent]:
            lo, hi, t0, t1 = box_at(nd, 0)
            e = [i - 1 for i in a.est]; p = [i - 1 for i in a.pos]
            entries.append(dict(t=t0, est_lo=lo[e].tolist(), est_hi=hi[e].tolist(), true_lo=lo[p].tolist(), true_hi=hi[p].tolist()))
            print(f"entry into {a.mode_name} at t={t0:.0f}: estimate box x[{lo[e[0]]:.3f},{hi[e[0]]:.3f}] y[{lo[e[1]]:.3f},{hi[e[1]]:.3f}] km; true x[{lo[p[0]]:.3f},{hi[p[0]]:.3f}] y[{lo[p[1]]:.3f},{hi[p[1]]:.3f}] km")
mode_ok = None
if a.box and entries:
    x0, y0, hx, hy = a.box
    mode_ok = all(x0 - hx <= e["est_lo"][0] and e["est_hi"][0] <= x0 + hx and y0 - hy <= e["est_lo"][1] and e["est_hi"][1] <= y0 + hy for e in entries)
    print(f"MODE-ENTRY CONDITION (B = [{x0}+-{hx}] x [{y0}+-{hy}] km on the estimate): {'VERIFIED (estimate box inside B at every entry)' if mode_ok else 'INCONCLUSIVE (estimate box leaves B at some entry; over-approximation meets U)'}")
if a.json:
    json.dump(dict(tree=a.tree, eps_g=a.eps_g, v_g=a.v_g, box=a.box, leaves=rows, goal_verified=bool(ok_all), entries=entries, mode_entry_verified=mode_ok), open(a.json, "w"), indent=1)
