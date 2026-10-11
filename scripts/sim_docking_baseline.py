#!/usr/bin/env python
"""Simulation baseline for a docking variant: N simulations of the configuration in the
current worktree (its freq sensor/controller constants), reporting A/I Sim and F/I Sim with
the paper's diam_0 = 45 (L1 diameter of the initial set).

usage: python sim_docking_baseline.py <verse_repo_root> <N> <out.json>
"""
import sys, os, json, time
import numpy as np
repo, N, out = os.path.abspath(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
os.chdir(repo); sys.path[:0] = [repo, os.path.join(repo, "demo", "aprod")]
import plotly.graph_objects as go; go.Figure.show = lambda *a, **k: None
import orbital_docking_demo_ver_gpa_parser_wrapper_freq as W
from orbital_docking_agent_gpa import OrbitalAgent
from orbital_docking_sensor_gpa_parser_wrapper_freq import OrbitalSensor
from parsed_wrap import clear_parse_cache
from verse import Scenario, ScenarioConfig
from verse.utils.star_diams import sim_traces_to_diameters
if os.path.exists(W.filename): os.remove(W.filename)
clear_parse_cache()
sc = Scenario(ScenarioConfig(init_seg_length=1, parallel=False))
sc.add_agent(OrbitalAgent("deputy", file_name="./demo/aprod/orbital_docking_controller_gpa_parser_freq.py")); sc.set_sensor(OrbitalSensor())
T, ts, ry, n = 3000, 1, 75, W.n
base = [0, ry + 10, 0, n / 2 * ry * .9, 0, 0]
sc.set_init([[base + [b - 2.5 for b in base] + [-2.5] * 3 + [0] * 7, base + [b + 2.5 for b in base] + [2.5] * 3 + [0] * 7]], [(W.GOMode.Passive, W.POMode.Passive, W.MoveMode.NMT)])
t0 = time.perf_counter(); trees = sc.simulate_multi(T, ts, num_sims=N); dt = time.perf_counter() - t0
d = sim_traces_to_diameters(trees); diam_0 = 45.0
res = {"N": N, "sim_runtime_s": dt, "F/I Sim": d[-1] / diam_0, "A/I Sim": (sum(d) / len(d)) / diam_0, "raw_final": d[-1], "raw_avg": sum(d) / len(d)}
json.dump(res, open(out, "w"), indent=1); print(f"[simbase] N={N} runtime {dt:.1f}s  A/I Sim {res['A/I Sim']:.3f}  F/I Sim {res['F/I Sim']:.3f}")
