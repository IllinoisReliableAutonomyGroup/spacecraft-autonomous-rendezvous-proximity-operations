#!/bin/bash
# Idempotent fixes applied to the Verse submodule working tree so the paper scripts run as the paper used them:
#  - enable the verification call that is commented out in three paper scripts, and define the timer they print;
#  - install the two switch-track variant scripts (initial estimation error 1.0 for every deputy).
set -e
cd "$(dirname "$0")"
V=verse/demo/aprod
for f in $V/paper/orbital_true_multi_switch_ver_gpa.py $V/paper/orbital_true_multi_switch_ver_gpa_3dep_fix.py; do
  sed -i.bak -e "s/^    # trace = scenario.verify(T, 1)/    start = time.perf_counter()\n    trace = scenario.verify(T, 1)/" \
             -e "s/^    # print(f'Simula\(t\)\{0,1\}ion time/    print(f'Simulation time/" \
             -e "s/^    # diam = time_step_diameter_rect(trace, T, 1)/    diam = time_step_diameter_rect(trace, T, 1)/" \
             -e "s/^    # diam_0, diam_f, diam_bar = \([0-9]*\), diam\[-1\]/    diam_0, diam_f, diam_bar = \1, diam[-1]/" \
             -e "s/^    # print(f'F\/I: {diam_f\/diam_0/    print(f'F\/I: {diam_f\/diam_0/" "$f" && rm -f "$f.bak"
done
f=$V/vis_dubins_rdvz/1c1n_ver_parser_3.py
sed -i.bak -e "s/^    # traces = scenario.verify(T, time_step)/    traces = scenario.verify(T, time_step)/" \
           -e "s/^    # print(f'Runtime for T={T}, ts={time_step}/    print(f'Runtime for T={T}, ts={time_step}/" \
           -e "s/^    # diam = time_step_diameter_rect(traces, T, time_step)/    diam = time_step_diameter_rect(traces, T, time_step)/" \
           -e "s/^    # diam_0, diam_f, diam_bar = 0.4, diam\[-1\]/    diam_0, diam_f, diam_bar = 0.4, diam[-1]/" \
           -e "s/^    # print(f'F\/I: {diam_f\/diam_0:.2f}/    print(f'F\/I: {diam_f\/diam_0:.2f}/" "$f" && rm -f "$f.bak"
cp scripts/var_switch2_ie10.py scripts/var_switch3_ie10.py $V/paper/
echo "prepare.sh: Verse submodule prepared"
