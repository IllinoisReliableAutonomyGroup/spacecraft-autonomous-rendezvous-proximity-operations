#!/usr/bin/env python
"""Simulation baseline for a reach-avoid variant (configuration of the current worktree):
A/I Sim and F/I Sim over N simulations with the paper's diam_0 = 45.
usage: python sim_ra_baseline.py <verse_repo_root> <N> <out.json>
"""
import sys, os, json, time
import numpy as np
repo, N, out = os.path.abspath(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
os.chdir(repo); sys.path[:0] = [repo, os.path.join(repo, "demo", "aprod", "paper"), os.path.join(repo, "demo", "aprod")]
import plotly.graph_objects as go; go.Figure.show = lambda *a, **k: None
import orbital_ra_demo_ver_gpa as W
from orbital_ra_agent_gpa import OrbitalAgent, SimpleOrbtialAgent
from orbital_ra_sensor_gpa import OrbitalSensor
from verse import Scenario, ScenarioConfig
from verse.utils.star_diams import sim_traces_to_diameters
sc = Scenario(ScenarioConfig(init_seg_length=1, parallel=False))
dep = OrbitalAgent("deputy", file_name="./demo/aprod/orbital_ra_controller_gpa.py"); obs = SimpleOrbtialAgent("obs")
sc.add_agent(dep); sc.add_agent(obs); sc.set_sensor(OrbitalSensor())
T, ry, n = 3000, 75, W.n
base = [0, ry + 10, 0, n / 2 * ry * .9, 0, 0]
x0_l = base + [b - 2.5 for b in base] + [-2.5] * 3 + [0] * 9; x0_u = base + [b + 2.5 for b in base] + [2.5] * 3 + [0] * 9
obs_base = [0, -ry, 0, 0, 0, 0]
try:
    GOMode, POMode, TrajMode = W.GOMode, W.POMode, W.TrajMode
except AttributeError:
    from orbital_ra_controller_gpa import GOMode, POMode, TrajMode
mode_list = [(GOMode.Passive, POMode.Passive, TrajMode.Normal), (GOMode.Passive,)]  # as in the paper script's set_init
sc.set_init([[x0_l, x0_u], [obs_base, obs_base]], mode_list)
t0 = time.perf_counter(); trees = sc.simulate_multi(T, 1, num_sims=N); dt = time.perf_counter() - t0
d = sim_traces_to_diameters(trees); diam_0 = 45.0
res = {"N": N, "sim_runtime_s": dt, "F/I Sim": d[-1] / diam_0, "A/I Sim": (sum(d) / len(d)) / diam_0, "raw_final": d[-1], "raw_avg": sum(d) / len(d)}
json.dump(res, open(out, "w"), indent=1); print(f"[simbase] N={N} runtime {dt:.1f}s  A/I Sim {res['A/I Sim']:.3f}  F/I Sim {res['F/I Sim']:.3f}")
