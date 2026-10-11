# Saved verification results (2026-10-08, Apple M2, Verse branch `satellite_models` @ 6a6c87a)

Produced with `scripts/run_verse_headless.py`; see `HANDOFF.md` §3 for the script of each row and §6 for the numbers.

* `<run>_runs.jsonl`: method, arguments, wall-clock runtime, node count, dump file.
* `<run>_tree.json.gz`: the `AnalysisTree.dump` of the verified run (gunzip, then `AnalysisTree.load`).
* `<run>.diameters.txt`: A/I and F/I as printed by the demo script (or recomputed from the tree).
* `docking_nominal_verdict.json`: output of `scripts/verdicts.py` (goal radius 10 km; entry box B = [6, 11] x [-75, -71] km).
* `docking_sim_terminal.json`: 10 simulations of the docking configuration, terminal and closest-approach states (`scripts/sim_docking_terminal.py`).
* `docking_degraded_*`: the same for the degraded configuration (ground error 1.25 km, update period 1200 s); the simulation JSON holds 20 runs,
  5 of which enter Docking with the estimate outside B (the witness quoted in the paper is sim 13).
* `rdvz2_*`, `rdvz3_*`: the robot rendezvous rows (`demo/aprod/vis_dubins_rdvz/1c1n_ver_parser.py`, `..._3.py` with verify uncommented).

## Parameter variants (2026-10-09, `results/variants/`)
One constant changed at a time from the base scenario; `<name>.patch` is the exact `git diff` of the Verse worktree that ran it,
`var_switch*_ie10.py` (in `scripts/`) are the switch-track variant scripts (initial estimate error 1.0 for every deputy, verify enabled).
`retime_*` are the uncontended re-runs whose runtimes the table reports; the un-prefixed docking/ra variant runs were measured under
8-way CPU contention (runtimes not comparable, verdicts identical). `*_sim_terminal.json`: 20-run witness probes (entry estimate vs B).
