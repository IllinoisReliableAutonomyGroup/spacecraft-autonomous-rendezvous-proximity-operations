#!/usr/bin/env python
"""Minimum separation between agents over a saved Verse tree (true positions,
columns 1..3 after the time column). For each node and time step the reach
boxes of two agents give a lower bound (box-to-box gap) and an upper bound on
their distance; the minimum over the run of the lower bound certifies that the
separation never drops below it.

usage: python pair_separation.py <verse_repo_root> <tree.json> [--pos 1 2 3]
"""
import sys, os, argparse, itertools
import numpy as np

ap = argparse.ArgumentParser(); ap.add_argument("repo"); ap.add_argument("tree"); ap.add_argument("--pos", type=int, nargs=3, default=[1, 2, 3])
a = ap.parse_args()
sys.path.insert(0, os.path.abspath(a.repo))
from verse.analysis.analysis_tree import AnalysisTree
tree = AnalysisTree.load(a.tree)
agents = list(tree.nodes[0].trace.keys())
idx = a.pos
best = {}
for p, q in itertools.combinations(agents, 2):
    lo_min, hi_min, t_at, node_at = np.inf, np.inf, None, None
    for k, nd in enumerate(tree.nodes):
        A, B = np.array(nd.trace.get(p, []), dtype=float), np.array(nd.trace.get(q, []), dtype=float)
        if len(A) < 2 or len(B) < 2 or len(A) != len(B):
            continue
        la, ha = np.minimum(A[0::2, idx], A[1::2, idx]), np.maximum(A[0::2, idx], A[1::2, idx])
        lb, hb = np.minimum(B[0::2, idx], B[1::2, idx]), np.maximum(B[0::2, idx], B[1::2, idx])
        gap = np.maximum(0, np.maximum(lb - ha, la - hb))          # per-coordinate gap between boxes
        dmin = np.linalg.norm(gap, axis=1)                          # lower bound on separation
        far = np.maximum(np.abs(hb - la), np.abs(ha - lb)); dmax = np.linalg.norm(far, axis=1)
        j = int(dmin.argmin())
        if dmin[j] < lo_min:
            lo_min, hi_min, t_at, node_at = float(dmin[j]), float(dmax[j]), float(A[2 * j, 0]), k
    best[(p, q)] = (lo_min, hi_min, t_at, node_at)
    print(f"{p} vs {q}: min lower-bound separation {lo_min:.3f} km (upper bound there {hi_min:.3f} km) at t={t_at:.0f} s, node {node_at}")
