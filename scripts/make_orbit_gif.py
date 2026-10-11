#!/usr/bin/env python
"""Animation of the docking mission: left, the chief on a circular orbit around Earth with the ground station and its update
beam; right, the chief-centred LVLH frame with the deputy's true position (filled), its estimate (hollow), the angles-only line
of sight, the proximity zone, and the mode. Driven by one Verse simulation of the configuration in the current worktree.

usage: python make_orbit_gif.py <verse_repo_root> <out.gif> [--step 20] [--seed 0]
"""
import sys, os, argparse
import numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("repo"); ap.add_argument("out"); ap.add_argument("--step", type=int, default=20); ap.add_argument("--seed", type=int, default=0)
a = ap.parse_args()
repo = os.path.abspath(a.repo); os.chdir(repo); sys.path[:0] = [repo, os.path.join(repo, "demo", "aprod")]
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt; from matplotlib import animation, patches
import plotly.graph_objects as go; go.Figure.show = lambda *x, **k: None
import orbital_docking_demo_ver_gpa_parser_wrapper_freq as W
from orbital_docking_agent_gpa import OrbitalAgent, n as MEAN_MOTION
from orbital_docking_sensor_gpa_parser_wrapper_freq import OrbitalSensor
from parsed_wrap import clear_parse_cache
from verse import Scenario, ScenarioConfig
# ---------------- one simulation of the paper's docking configuration ----------------
if os.path.exists(W.filename): os.remove(W.filename)
clear_parse_cache(); np.random.seed(a.seed)
sc = Scenario(ScenarioConfig(init_seg_length=1, parallel=False))
sc.add_agent(OrbitalAgent("deputy", file_name="./demo/aprod/orbital_docking_controller_gpa_parser_freq.py")); sc.set_sensor(OrbitalSensor())
T, ry, nn = 3000, 75, W.n
base = [0, ry + 10, 0, nn / 2 * ry * .9, 0, 0]
sc.set_init([[base + [b - 2.5 for b in base] + [-2.5] * 3 + [0] * 7, base + [b + 2.5 for b in base] + [2.5] * 3 + [0] * 7]], [(W.GOMode.Passive, W.POMode.Passive, W.MoveMode.NMT)])
tree = sc.simulate(T, 1, seed=a.seed)
rows, ground, prox_on, dock_on = [], [], None, None
for nd in tree.nodes:
    tr = np.array(nd.trace.get("deputy", []), dtype=float)
    if len(tr) == 0: continue
    go_m, po_m, mv = nd.mode["deputy"]
    if go_m == "Active": ground.append(float(tr[0, 0]))
    if po_m == "Active" and prox_on is None: prox_on = float(tr[0, 0])
    if mv == "Docking" and dock_on is None: dock_on = float(tr[0, 0])
    for r in tr: rows.append((r[0], r[1], r[2], r[3], r[7], r[8], r[9], mv))
rows.sort(key=lambda r: r[0])
t = np.array([r[0] for r in rows]); X = np.array([[r[1], r[2], r[3]] for r in rows]); H = np.array([[r[4], r[5], r[6]] for r in rows]); MODE = [r[7] for r in rows]
def at(tt):
    i = int(np.searchsorted(t, tt, side="right")) - 1; return max(i, 0)
print(f"[sim] ground updates at {sorted(set(int(g) for g in ground))}; proximity active from {prox_on}; Docking from {dock_on}")
# ---------------- geometry ----------------
mu, R_E = 398600.4418, 6371.0
r_orb = (mu / MEAN_MOTION ** 2) ** (1 / 3)              # circular orbit radius consistent with the model's mean motion (146 km altitude)
R_DRAW = 1.35 * R_E                                      # radius at which the orbit is drawn, so it clears the globe's outline
inc = np.deg2rad(45.0); w_earth = 2 * np.pi / 86164.0
def chief_pos(tt):
    th = MEAN_MOTION * tt; p = np.array([np.cos(th), np.sin(th), 0.0]) * R_DRAW
    return np.array([p[0], p[1] * np.cos(inc), p[1] * np.sin(inc)])          # orbit plane inclined about the x-axis
def station_pos(tt):                                     # ground station on the rotating Earth, under the orbit at t = 0
    lat, lon0 = np.deg2rad(20.0), np.deg2rad(-10.0); lon = lon0 + w_earth * tt
    return R_E * np.array([np.cos(lat) * np.cos(lon), np.cos(lat) * np.sin(lon), np.sin(lat)])
u, v = np.mgrid[0:2 * np.pi:40j, 0:np.pi:20j]; EX, EY, EZ = R_E * np.cos(u) * np.sin(v), R_E * np.sin(u) * np.sin(v), R_E * np.cos(v)
orb = np.array([chief_pos(tt) for tt in np.linspace(0, 2 * np.pi / MEAN_MOTION, 200)])
# ---------------- figure ----------------
fig = plt.figure(figsize=(11, 6.0), dpi=110); fig.subplots_adjust(bottom=0.16, wspace=0.05)
ax3 = fig.add_subplot(1, 2, 1, projection="3d"); ax2 = fig.add_subplot(1, 2, 2)
times = list(range(0, T + 1, a.step)); L = 9200
def draw(i):
    tt = times[i]; k = at(tt); ax3.clear(); ax2.clear()
    # --- Earth view ---
    ax3.plot_surface(EX, EY, EZ, color="#8fbde6", linewidth=0, shade=True, antialiased=False)
    ax3.plot_wireframe(EX, EY, EZ, rstride=5, cstride=4, color="#4a78a8", lw=.35)
    ax3.plot(orb[:, 0], orb[:, 1], orb[:, 2], color="#3b2a80", lw=1.3)
    c = chief_pos(tt); s = station_pos(tt)
    ax3.plot(*s, marker="^", color="#1f6f2e", ms=7); ax3.text(s[0] * 1.02, s[1] * 1.02, s[2] - 900, "ground station", fontsize=7, color="#1f6f2e")
    ax3.plot(*c, marker="*", color="k", ms=11); ax3.text(c[0], c[1], c[2] + 450, "chief + deputy", fontsize=7)
    flash = any(abs(tt - g) < 1.5 * a.step for g in ground)
    if flash:
        ax3.plot([s[0], c[0]], [s[1], c[1]], [s[2], c[2]], color="#1f6f2e", lw=2.2)
        ax3.text(*((s + c) / 2 + np.array([0, 0, 600])), "ground update", fontsize=8, color="#1f6f2e", weight="bold")
    ax3.set_xlim(-L, L); ax3.set_ylim(-L, L); ax3.set_zlim(-L, L); ax3.set_box_aspect((1, 1, 1))
    ax3.view_init(elev=24, azim=np.degrees(MEAN_MOTION * tt) - 70)          # camera follows the chief
    ax3.set_axis_off(); ax3.set_title(f"Chief on a circular orbit, η = {MEAN_MOTION} rad/s (orbit drawn at 1.35 R_E; true altitude 146 km)\nt = {tt:4d} s", fontsize=8.5)
    # --- LVLH view ---
    mv = MODE[k]; prox_active = prox_on is not None and tt >= prox_on
    ax2.set_xlim(-50, 50); ax2.set_ylim(-100, 100); ax2.set_aspect("equal"); ax2.grid(alpha=.3)
    ax2.set_xlabel("x, radial (km)"); ax2.set_ylabel("y, along-track (km)")
    ax2.add_patch(patches.Circle((0, 0), 5, fc="#b9a6e6" if prox_active else "#e6e0f5", ec="#6a4fc4" if prox_active else "none", lw=1.2, alpha=.8))
    if prox_active:
        for rr in (2 + 3 * (((tt - prox_on) / a.step) % 1.0),):
            ax2.add_patch(patches.Circle((0, 0), rr, fc="none", ec="#6a4fc4", lw=.8, alpha=.6))
    ax2.plot(0, 0, "k*", ms=11)
    ax2.plot(X[:k + 1, 0], X[:k + 1, 1], color="#d02020", lw=.9, alpha=.7)
    ax2.plot(X[k, 0], X[k, 1], "o", color="#d02020", ms=6)                                   # true position
    ax2.plot(H[k, 0], H[k, 1], "o", mfc="none", mec="#d02020", mew=1.4, ms=9)                # estimate
    ax2.plot([X[k, 0], 0], [X[k, 1], 0], color="#e08a00", lw=1.2)                           # angles-only line of sight
    th = np.degrees(np.arctan2(-X[k, 1], -X[k, 0]))
    ax2.text(X[k, 0] / 2 + 2, X[k, 1] / 2, f"bearing {th:5.1f}°", fontsize=7, color="#e08a00")
    if flash: ax2.text(-48, 92, "GROUND UPDATE: estimate reset", fontsize=8, color="#1f6f2e", weight="bold")
    err = np.linalg.norm(H[k, :2] - X[k, :2])
    ax2.text(0.0, -0.13, f"mode {mv}  |  angles-only on  |  ground fix every 15 min\nproximity {'ON, every 1 s' if prox_active else 'off (> 5 km)'}  |  estimate error {err:4.2f} km  (filled: true, hollow: estimate)", transform=ax2.transAxes, fontsize=7.5, va="top")
    ax2.set_title("Chief-centred LVLH frame", fontsize=9)
anim = animation.FuncAnimation(fig, draw, frames=len(times), interval=70)
anim.save(a.out, writer=animation.PillowWriter(fps=14))
print(f"[gif] {a.out}: {len(times)} frames, {os.path.getsize(a.out)/1e6:.1f} MB")
