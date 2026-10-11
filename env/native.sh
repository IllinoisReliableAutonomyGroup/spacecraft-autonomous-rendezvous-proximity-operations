#!/bin/bash
# Native setup (Linux or macOS). Usage: bash env/native.sh [python3-executable]
# Creates ./venv, installs CPU torch, the pinned requirements, the auto_LiRPA fork, and Verse (editable) from the submodules.
set -e
PY=${1:-python3}
cd "$(dirname "$0")/.."
git submodule update --init
$PY -m venv venv
./venv/bin/pip install --upgrade pip setuptools wheel
./venv/bin/pip install --index-url https://download.pytorch.org/whl/cpu torch==2.3.1 torchvision==0.18.1
./venv/bin/pip install -r requirements.txt
./venv/bin/pip install ./auto_LiRPA
./venv/bin/pip install --no-deps -e ./verse
bash prepare.sh
echo "OK. Now: VENV=./venv bash run_row.sh rdv-2"
