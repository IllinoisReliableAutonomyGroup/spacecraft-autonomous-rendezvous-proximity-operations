# Sensor programs for spacecraft rendezvous and docking: artifact

Companion artifact for *Verifying Autonomous Spacecraft Rendezvous and Docking with Sensor Programs* (Alex Yuan, Kristina Miller,
Sayan Mitra; submitted to TACAS 2027). It pins the exact code that produced the paper's results and lets every row of the results
table be re-run with one command.

Reliable Autonomy Group, University of Illinois Urbana-Champaign. Code of the Verse library and of this artifact is under the
University of Illinois/NCSA Open Source License (see `LICENSE`).

## What is pinned

| component | where | pinned at |
|---|---|---|
| Verse (hybrid-system reachability library with the sensor-program parser and `verify_partitioned`) | submodule `verse/` → [AutoVerse-ai/Verse-library](https://github.com/AutoVerse-ai/Verse-library) | tag `tacas27-sensor-programs` (commit 6a6c87a, branch `satellite_models`) |
| auto_LiRPA (CROWN bound propagation), Alex Yuan's fork with the Verse bridge | submodule `auto_LiRPA/` → [IllinoisReliableAutonomyGroup/auto_LiRPA](https://github.com/IllinoisReliableAutonomyGroup/auto_LiRPA) | commit 711153a |
| Python packages | `requirements-pinned.txt` | versions of the run environment (torch 2.3.1 CPU, cvxpy 1.6.6, highspy 1.11.0, numpy 1.26.4, …) |

The spacecraft models (dynamics, controllers, sensor programs, run scripts) live in `verse/demo/aprod/`; the four paper runs are in
`verse/demo/aprod/paper/`. `prepare.sh` applies two small fixes to the submodule's working tree (see "Known quirks").

## Quick start

Docker (Linux x86-64 or arm64; ~10 minutes to build, CPU only):

```sh
git clone --recursive https://github.com/IllinoisReliableAutonomyGroup/sensor-programs-tacas27.git
cd sensor-programs-tacas27
docker build -t sensor-programs .
docker run --rm -it -v "$PWD/out:/workspace/out" sensor-programs bash run_row.sh rdv-2        # 10 s smoke test
docker run --rm -it -v "$PWD/out:/workspace/out" sensor-programs bash run_row.sh apo-avoid    # ~2 min
docker run --rm -it -v "$PWD/out:/workspace/out" sensor-programs bash run_row.sh apo-dock     # ~20 min on a laptop
```

Native (macOS or Linux, Python 3.10 or 3.11):

```sh
git clone --recursive https://github.com/IllinoisReliableAutonomyGroup/sensor-programs-tacas27.git
cd sensor-programs-tacas27
bash env/native.sh python3.10            # creates ./venv and prepares the submodule
VENV=./venv bash run_row.sh rdv-2
```

`run_row.sh <row>` sets the scenario's constants for that row, runs the verification headlessly (no plot windows), saves the
reachable-set tree to `out/<row>/tree_0.json`, and evaluates the row's property. Row ids and expected numbers: `expected_results.md`.
Full table reproduction, sequentially on a laptop, takes about 2.5 hours; the docking rows dominate.

## Layout

```
run_row.sh            one table row or sensitivity configuration, end to end
prepare.sh            fixes applied to the Verse submodule working tree (idempotent)
scripts/
  run_verse_headless.py   runs a Verse demo script without plot windows and saves every verified AnalysisTree
  verdicts.py             docking checks: goal containment on every leaf; entry box vs the mode-entry box B
  pair_separation.py      certified minimum separation between two agents over a tree
  sim_docking_terminal.py 20-run simulation probe (terminal states, entry estimates; the witnesses of Section 5.3)
  sim_docking_baseline.py / sim_ra_baseline.py   A/I Sim and F/I Sim baselines (N = 25)
  var_switch2_ie10.py / var_switch3_ie10.py      switch-track variants with initial estimation error 1.0
  variant_rows.py         turns variant outputs into table rows
results/              trees (gzipped JSON), runtimes, diameters, verdict and simulation JSON from the runs behind the paper
expected_results.md   per-row expected values, verdict rules, tolerances
env/native.sh         native environment setup
Dockerfile            reproduction image
```

## Properties checked (Section 3.4 and 5.1 of the paper)

* `apo-dock`: goal containment, every leaf of the execution tree (branch ended by the 100 m stop rule or by the horizon) lies
  within ε_G = 10 km of the chief; mode-entry condition, the estimated position at the Docking transition lies in
  B = [6, 11] × [−75, −71] km. Verified if both hold on the computed sets; violated if a simulated run witnesses an entry outside B;
  inconclusive otherwise.
* `apo-avoid`: the deputy never comes within 2.5 km of the obstacle (certified minimum box-to-box separation ≥ 2.5 km).
* `apo-track`: deputies never come within 5 km of each other.
* `rdv`: every agent reaches `Complete` by the horizon within 3.1 m of its partner, and no two agents come within 1 m.

## Known quirks (handled by `prepare.sh` and `run_row.sh`)

* Three paper scripts have `scenario.verify` commented out in the committed branch (the authors last ran them for simulation
  plots); `prepare.sh` re-enables the call and defines the timer the following print uses.
* The 3-agent rendezvous script prints A/I and F/I with `diam_0 = 0.4`; the paper's row uses the initial width of that script,
  `0.04`, hence 286.40 / 1248.03 in the paper versus 28.64 / 124.8 printed.
* The MPC in the docking and reach-avoid agents solves with HiGHS (`cvxpy` + `highspy`). Without `highspy` the docking agent
  silently falls back to LQR and prints "MPC was unable to find a solution" on every step; the numbers then do not reproduce.
  Both packages are in `requirements-pinned.txt`.
* Scripts must run from the Verse root with `demo/aprod` on `sys.path` and the script's own directory first, which the runner does.
* Parallel runs need separate checkouts: the parser cache (`demo/aprod/parsed_wrap/parse_cache/`) and the MPC reference file
  (`demo/aprod/refs.pkl`) are repo-relative and cleared at the start of every script.
* The CORA and JuliaReach models of the cross-tool comparison (Section 5.4) are not part of this artifact; only the Verse side
  (`tools-baseline`) is.

## Citation

```
@inproceedings{yuan2027sensorprograms,
  author    = {Alex Yuan and Kristina Miller and Sayan Mitra},
  title     = {Verifying Autonomous Spacecraft Rendezvous and Docking with Sensor Programs},
  booktitle = {Tools and Algorithms for the Construction and Analysis of Systems (TACAS 2027)},
  year      = {2027},
  note      = {Submitted}
}
```
