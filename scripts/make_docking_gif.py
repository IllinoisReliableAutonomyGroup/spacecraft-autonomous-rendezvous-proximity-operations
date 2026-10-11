#!/usr/bin/env python
"""Animated GIF of the docking scenario: the verified reachable box (true position, x-y plane) advancing in time with
simulated deputies inside it. Runs N simulations of the configuration in the current worktree and reads the saved tree.

usage: python make_docking_gif.py <verse_repo_root> <tree.json|.json.gz> <out.gif> [--sims N] [--step S] [--box X0 Y0 HX HY] [--title T]
"""
import sys, os, gzip, json, argparse, tempfile
import numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("repo"); ap.add_argument("tree"); ap.add_argument("out")
ap.add_argument("--sims", type=int, default=8); ap.add_argument("--step", type=int, default=20)
ap.add_argument("--box", type=float, nargs=4, default=None, help="mode-entry box on the estimate: x0 y0 half_x half_y (km)")
ap.add_argument("--title", default="apo-dock: verified reachable set and simulations")
a = ap.parse_args()
repo = os.path.abspath(a.repo); os.chdir(repo); sys.path[:0] = [repo, os.path.join(repo, "demo", "aprod")]
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt; from matplotlib import animation, patches
import plotly.graph_objects as go; go.Figure.show = lambda *x, **k: None
from verse.analysis.analysis_tree import AnalysisTree
# --- tree: boxes per time step (true x, y = columns 1, 2) ---
fn = a.tree
if fn.endswith(".gz"):
    tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False); tmp.write(gzip.open(fn, "rt").read()); tmp.close(); fn = tmp.name
tree = AnalysisTree.load(fn)
boxes = {}
for nd in tree.nodes:
    tr = np.array(nd.trace.get("deputy", []), dtype=float)
    for k in range(0, len(tr) - 1, 2):
        t = int(round(tr[k, 0])); lo, hi = np.minimum(tr[k, 1:3], tr[k+1, 1:3]), np.maximum(tr[k, 1:3], tr[k+1, 1:3])
        boxes.setdefault(t, []).append((lo, hi))
# --- simulations ---
import orbital_docking_demo_ver_gpa_parser_wrapper_freq as W
from orbital_docking_agent_gpa import OrbitalAgent
from orbital_docking_sensor_gpa_parser_wrapper_freq import OrbitalSensor
from parsed_wrap import clear_parse_cache
from verse import Scenario, ScenarioConfig
if os.path.exists(W.filename): os.remove(W.filename)
clear_parse_cache()
sc = Scenario(ScenarioConfig(init_seg_length=1, parallel=False))
sc.add_agent(OrbitalAgent("deputy", file_name="./demo/aprod/orbital_docking_controller_gpa_parser_freq.py")); sc.set_sensor(OrbitalSensor())
T, ry, n = 3000, 75, W.n
base = [0, ry + 10, 0, n / 2 * ry * .9, 0, 0]
sc.set_init([[base + [b - 2.5 for b in base] + [-2.5] * 3 + [0] * 7, base + [b + 2.5 for b in base] + [2.5] * 3 + [0] * 7]], [(W.GOMode.Passive, W.POMode.Passive, W.MoveMode.NMT)])
sims = []
for st in sc.simulate_multi(T, 1, num_sims=a.sims):
    rows = np.array([r for nd in st.nodes for r in nd.trace.get("deputy", [])], dtype=float)
    rows = rows[np.argsort(rows[:, 0], kind="stable")]
    entry = next((nd for nd in st.nodes if "Docking" in nd.mode["deputy"] and len(nd.trace.get("deputy", []))), None)
    sims.append({"t": rows[:, 0], "x": rows[:, 1], "y": rows[:, 2], "hx": rows[:, 7], "hy": rows[:, 8],
                 "entry": None if entry is None else np.array(entry.trace["deputy"][0], dtype=float)})
witness = None
if a.box:
    x0, y0, hx, hy = a.box
    for i, s in enumerate(sims):
        e = s["entry"]
        if e is not None and not (x0 - hx <= e[7] <= x0 + hx and y0 - hy <= e[8] <= y0 + hy): witness = i; break
# --- render ---
fig, ax = plt.subplots(figsize=(5.2, 7.4), dpi=125)
times = list(range(0, T + 1, a.step))
def draw(i):
    t = times[i]; ax.clear()
    ax.set_xlim(-50, 50); ax.set_ylim(-100, 100); ax.set_aspect("equal"); ax.grid(alpha=.3)
    ax.set_xlabel("x (km)"); ax.set_ylabel("y (km)"); ax.set_title(f"{a.title}\nt = {t:4d} s", fontsize=10)
    ax.add_patch(patches.Circle((0, 0), 5, fc="#dcd0f0", ec="none", alpha=.7)); ax.plot(0, 0, "k*", ms=9)
    if a.box:
        ax.add_patch(patches.Rectangle((x0 - hx, y0 - hy), 2 * hx, 2 * hy, fc="none", ec="green", lw=1.2, ls="--"))
    for lo, hi in boxes.get(t, []):
        ax.add_patch(patches.Rectangle(lo, hi[0] - lo[0], hi[1] - lo[1], fc="#2040ff", ec="#2040ff", alpha=.35, lw=.8))
    for j, s in enumerate(sims):
        m = s["t"] <= t; col = "#8800cc" if j == witness else "#d02020"
        ax.plot(s["x"][m], s["y"][m], color=col, lw=0.9 if j == witness else 0.6, alpha=.9 if j == witness else .6)
        if m.any(): ax.plot(s["x"][m][-1], s["y"][m][-1], "o", color=col, ms=3)
        if j == witness and s["entry"] is not None and s["entry"][0] <= t:
            ax.plot(s["entry"][7], s["entry"][8], "s", color=col, ms=6, mfc="none"); ax.plot(s["entry"][1], s["entry"][2], "s", color=col, ms=6)
    ax.text(-48, -96, "blue: verified reachable box (true position)\nred: simulations" + ("\npurple: enters Docking with estimate (hollow) outside B" if witness is not None else ""), fontsize=8)
anim = animation.FuncAnimation(fig, draw, frames=len(times), interval=60)
anim.save(a.out, writer=animation.PillowWriter(fps=16))
print(f"[gif] {a.out}: {len(times)} frames, {len(sims)} sims, witness={'sim %d' % witness if witness is not None else 'none'}, size {os.path.getsize(a.out)/1e6:.1f} MB")
