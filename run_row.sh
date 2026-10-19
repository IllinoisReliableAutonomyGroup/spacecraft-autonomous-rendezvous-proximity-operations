#!/bin/bash
# Run one row of Table 2 (or a sensitivity configuration) end to end: configure the scenario's constants, verify, save the
# reachable-set tree under out/<row>/, and evaluate the row's property.
#   usage: VENV=./venv bash run_row.sh <row>      (inside the Docker image VENV is unset and the system python is used)
#   rows:  apo-dock apo-dock-T10 apo-dock-eps075 apo-dock-eps100 apo-dock-T20 apo-dock-degraded
#          apo-avoid apo-avoid-eps025 apo-avoid-T10 apo-avoid-eps075 apo-avoid-eps100
#          apo-track-2 apo-track-2-e1 apo-track-3 apo-track-3-e1  rdv-2 rdv-3  tools-baseline
set -e
cd "$(dirname "$0")"; ROOT=$PWD; V=$ROOT/verse; A=$V/demo/aprod
if [ -n "$VENV" ]; then VENV=$(cd "$VENV" && pwd) || { echo "VENV=$VENV not found"; exit 1; }; PY=$VENV/bin/python; else PY=python; fi   # absolute: the run below changes directory
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-2} MKL_NUM_THREADS=${MKL_NUM_THREADS:-2} PYTHONWARNINGS=ignore
row=$1; [ -n "$row" ] || { sed -n 2,7p "$0"; exit 1; }
OUT=$ROOT/out/$row; mkdir -p "$OUT"
DOCK_S=$A/orbital_docking_sensor_gpa_parser_wrapper_freq.py; DOCK_C=$A/orbital_docking_controller_gpa_parser_freq.py
RA_S=$A/orbital_ra_sensor_gpa.py; RA_C=$A/orbital_ra_controller_gpa.py
restore() { git -C "$V" checkout -q -- demo/aprod/orbital_docking_sensor_gpa_parser_wrapper_freq.py demo/aprod/orbital_docking_controller_gpa_parser_freq.py demo/aprod/orbital_ra_sensor_gpa.py demo/aprod/orbital_ra_controller_gpa.py 2>/dev/null || true; }
trap restore EXIT; restore
case $row in
  apo-dock)          script=$A/orbital_docking_demo_ver_gpa_parser_wrapper_freq.py ;;
  apo-dock-T10)      script=$A/orbital_docking_demo_ver_gpa_parser_wrapper_freq.py; sed -i.bak 's/if ego.timer >= 900 and ego.go_mode/if ego.timer >= 600 and ego.go_mode/' $DOCK_C ;;
  apo-dock-T20)      script=$A/orbital_docking_demo_ver_gpa_parser_wrapper_freq.py; sed -i.bak 's/if ego.timer >= 900 and ego.go_mode/if ego.timer >= 1200 and ego.go_mode/' $DOCK_C ;;
  apo-dock-eps075)   script=$A/orbital_docking_demo_ver_gpa_parser_wrapper_freq.py; sed -i.bak 's/^epsilon = 0.5$/epsilon = 0.75/' $DOCK_S ;;
  apo-dock-eps100)   script=$A/orbital_docking_demo_ver_gpa_parser_wrapper_freq.py; sed -i.bak 's/^epsilon = 0.5$/epsilon = 1.0/' $DOCK_S ;;
  apo-dock-degraded) script=$A/orbital_docking_demo_ver_gpa_parser_wrapper_freq.py; sed -i.bak 's/^epsilon = 0.5$/epsilon = 1.25/' $DOCK_S; sed -i.bak 's/if ego.timer >= 900 and ego.go_mode/if ego.timer >= 1200 and ego.go_mode/' $DOCK_C ;;
  apo-avoid)         script=$A/paper/orbital_ra_demo_ver_gpa.py ;;
  apo-avoid-eps025)  script=$A/paper/orbital_ra_demo_ver_gpa.py; sed -i.bak 's/^epsilon = 0.5$/epsilon = 0.25/' $RA_S ;;
  apo-avoid-eps075)  script=$A/paper/orbital_ra_demo_ver_gpa.py; sed -i.bak 's/^epsilon = 0.5$/epsilon = 0.75/' $RA_S ;;
  apo-avoid-eps100)  script=$A/paper/orbital_ra_demo_ver_gpa.py; sed -i.bak 's/^epsilon = 0.5$/epsilon = 1.0/' $RA_S ;;
  apo-avoid-T10)     script=$A/paper/orbital_ra_demo_ver_gpa.py; sed -i.bak 's/if ego.timer >= 900:/if ego.timer >= 600:/' $RA_C ;;
  apo-track-2)       script=$A/paper/orbital_true_multi_switch_ver_gpa.py ;;
  apo-track-2-e1)    script=$A/paper/var_switch2_ie10.py ;;
  apo-track-3)       script=$A/paper/orbital_true_multi_switch_ver_gpa_3dep_fix.py ;;
  apo-track-3-e1)    script=$A/paper/var_switch3_ie10.py ;;
  rdv-2)             script=$A/vis_dubins_rdvz/1c1n_ver_parser.py ;;
  rdv-3)             script=$A/vis_dubins_rdvz/1c1n_ver_parser_3.py ;;
  tools-baseline)    script=$A/orbital_docking_demo_ver_simple_same_real.py ;;
  *) echo "unknown row $row"; exit 1 ;;
esac
rm -f $A/*.bak
echo "== $row: verifying ($script) =="
( cd "$V" && PYTHONPATH="$V:$A" "$PY" "$ROOT/scripts/run_verse_headless.py" "$V" "$script" "$OUT/tree" ) > "$OUT/run.log" 2>&1 || true
grep -v 'ImportWarning\|_SixMeta\|^$\|polytope\|linprog' "$OUT/run.log" | grep '\[runner\]\|F/I\|Sim results\|Traceback\|Error\|No such file\|not found' || true
tree=$(ls "$OUT"/tree_0.json 2>/dev/null || ls "$OUT"/tree_0.pkl 2>/dev/null) || { echo "!! no tree produced; see $OUT/run.log (last lines follow)"; tail -5 "$OUT/run.log"; exit 1; }
echo "== $row: property check =="
case $row in
  apo-dock*)   $PY scripts/verdicts.py "$V" "$tree" --eps-g 10 --v-g 1e9 --box 8.5 -73 2.5 2 --json "$OUT/verdict.json" | grep 'MISSION\|MODE-ENTRY\|entry into' ;;
  apo-avoid*)  $PY scripts/pair_separation.py "$V" "$tree" | tee "$OUT/separation.txt"; echo "property: deputy stays >= 2.5 km from the obstacle (verified iff the certified separation above is >= 2.5)" ;;
  apo-track*)  $PY scripts/pair_separation.py "$V" "$tree" | tee "$OUT/separation.txt"; echo "property: deputies stay >= 5 km apart (verified iff every certified separation above is >= 5)" ;;
  rdv-*)       $PY scripts/pair_separation.py "$V" "$tree" --unit m | tee "$OUT/separation.txt"; echo "property: every agent Complete by the horizon within 3.1 m of its partner, no two agents within 1 m (see expected_results.md for the leaf check)" ;;
  tools-baseline) echo "cross-tool baseline: compare runtime and F/I with expected_results.md" ;;
esac
echo "== $row: outputs in $OUT =="
