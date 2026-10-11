# Convenience targets. VENV defaults to ./venv (created by `make setup`); unset it inside the Docker image.
VENV ?= ./venv
ROWS_SMOKE = rdv-2 apo-avoid
ROWS_ALL   = apo-dock apo-dock-T10 apo-avoid apo-avoid-eps025 apo-avoid-T10 apo-track-2 apo-track-2-e1 apo-track-3 apo-track-3-e1 rdv-2 rdv-3 tools-baseline
ROWS_SENS  = apo-dock-degraded apo-dock-eps075 apo-dock-eps100 apo-dock-T20 apo-avoid-eps075 apo-avoid-eps100

.PHONY: setup smoke all sensitivity docker clean
setup:          ## native environment in ./venv and the prepared submodule
	bash env/native.sh python3
smoke:          ## two fast rows (~3 min): rdv-2, apo-avoid
	for r in $(ROWS_SMOKE); do VENV=$(VENV) bash run_row.sh $$r || exit 1; done
all:            ## every row of Table 2 (~2.5 h on a laptop)
	for r in $(ROWS_ALL); do VENV=$(VENV) bash run_row.sh $$r || exit 1; done
sensitivity:    ## the Section 5.3 configurations (~2 h)
	for r in $(ROWS_SENS); do VENV=$(VENV) bash run_row.sh $$r || exit 1; done
docker:         ## build the reproduction image
	docker build -t sensor-programs .
clean:
	rm -rf out
