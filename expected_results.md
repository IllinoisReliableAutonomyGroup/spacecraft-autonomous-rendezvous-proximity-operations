# Expected results

Numbers the paper reports (Table 2 and Section 5.3) and what a reproduction run should give. Verification in Verse uses
DryVR-style sampled bloating, so A/I and F/I vary by a few percent between runs; verdicts and certified separations were stable
across every repetition we made. Runtimes are wall-clock on an Apple M2 (CPU-only CROWN); Alex Yuan's original runs on a
CUDA workstation were 1.5–4× slower in wall-clock for the docking rows and comparable elsewhere. "Paper" = values printed in
the submission; "Repro" = this artifact on 2026-10-08/09 (`results/`).

| row (`run_row.sh` id) | n | Runtime paper / repro | A/I paper / repro | F/I paper / repro | A/I Sim, F/I Sim (paper) | Verdict and check |
|---|---|---|---|---|---|---|
| `apo-dock` | 18 | 4455 s / 1040 s | 0.70 / 0.70 | 0.73 / 0.73 | 0.30, 0.04 | verified: goal containment at ε_G = 10 km (leaf max ‖r‖ 8.92 km) and entry box [6.45,10.15]×[−74.36,−71.98] km ⊂ B = [6,11]×[−75,−71] |
| `apo-dock-T10` | 18 | – / 665 s | – / 0.63 | – / 0.81 | 0.22, 0.00 (repro) | verified: entry box [6.88,8.93]×[−74.35,−72.34] ⊂ B |
| `apo-avoid` | 24 | 125 s / 103 s | 0.66 / 0.66 | 0.58 / 0.58 | 0.53, 0.11 | verified: certified deputy–obstacle separation 2.75 km ≥ 2.5 |
| `apo-avoid-eps025` | 24 | – / 101 s | – / 0.60 | – / 0.50 | 0.39, 0.05 (repro) | verified: 3.87 km |
| `apo-avoid-T10` | 24 | – / 101 s | – / 0.59 | – / 0.62 | 0.43, 0.00 (repro) | verified: 3.82 km |
| `apo-track-2` | 36 | 279 s / 147 s | 0.75 / 0.68 | 0.79 / 0.55 | 0.35, 0.15 | inconclusive: certified separation 0.94 km < 5 km (boxes of the two leading deputies nearly meet at t = 241 s) |
| `apo-track-2-e1` | 36 | – / 159 s | – / 0.47 | – / 0.55 | 0.23, 0.14 (repro) | verified: 5.40 km |
| `apo-track-3` | 54 | 670 s / 459 s | 0.87 / 0.87 | 0.82 / 0.82 | 0.43, 0.14 | inconclusive: 0.94 km (first pair); other pairs ≥ 31.7 km |
| `apo-track-3-e1` | 54 | – / 490 s | – / 0.75 | – / 0.82 | 0.32, 0.14 (repro) | verified: 5.40 km |
| `rdv-2` | 8 | 4.57 s / 6 s | 4.76 / 4.76 | 24.12 / 24.12 | 1.76, 1.31 | verified: all 8 leaves Complete at t = 7.3 s; separation at leaves 1.05–3.05 m (ε_R = 3.1 m, d_min = 1 m) |
| `rdv-3` | 12 | 215.9 s / 144 s | 286.40 / 28.64* | 1248.03 / 124.8* | 1.039, 0.00 | inconclusive: 4 of 25 leaves not all Complete; car1/car2 boxes overlap at t = 13.65 s. *The script prints with diam_0 = 0.4; the paper's row uses diam_0 = 0.04 (raw final 49.92, raw average 11.46 are identical). |
| `tools-baseline` | 18 | 26.74 s / 12.5 s | – / 1.32 | 1.18 / 1.18 | – | Verse side of the CORA/JuliaReach comparison (simplified docking, time-based guards). JuliaReach (43.71 s) and CORA (716.49 s) models are not in this artifact. |

Sensitivity configurations (Section 5.3), docking unless noted:

| id | change | result |
|---|---|---|
| `apo-dock-degraded` | ε_g,max = 1.25 km and T_g = 20 min | goal still verified (leaf max ‖r‖ 8.49 km); entry boxes up to x ∈ [0.6, 20.4], y ∈ [−80.6, −63.8] km leave B; 5 of 20 simulated runs (`scripts/sim_docking_terminal.py`) enter Docking outside B → violated with witness |
| `apo-dock-eps075` | ε = 0.75 km | entry box x up to 11.47 km leaves B by < 0.5 km; 0/20 simulated witnesses → inconclusive |
| `apo-dock-eps100` | ε = 1.0 km | entry box x up to 12.75 km; 5/20 simulated witnesses → violated |
| `apo-dock-T20` | T_g = 20 min | entry box x up to 11.32, y up to −70.76 km; 0/20 witnesses → inconclusive |
| `apo-avoid-eps075` / `apo-avoid-eps100` | ε = 0.75 / 1.0 km | certified separation 1.62 km / 0.37 km < 2.5 → inconclusive |

Leaf and entry checks: `scripts/verdicts.py` (docking: goal containment on every leaf, entry box vs B), `scripts/pair_separation.py`
(minimum over time of the box-to-box distance between two agents). Simulation baselines: `scripts/sim_docking_baseline.py`,
`scripts/sim_ra_baseline.py` (N = 25), and the switch-track scripts' own simulation blocks.
