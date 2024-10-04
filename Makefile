PROJECT_NAME := $(shell basename $(PWD))
VENV_PATH = ~/.venv/$(PROJECT_NAME)

STRAVA_DIR := $(shell echo ~/Downloads/export_43239612\ \(1\)/activities)
STRAVA_SUMMARY := data/strava.csv

all: venv install

venv:
	@python3 -m venv $(VENV_PATH)

install: venv
	@source $(VENV_PATH)/bin/activate && \
	pip install --disable-pip-version-check -q -r requirements.txt

unpack:
	@for file in '$(STRAVA_DIR)'/*.gz; do \
        gunzip -fk "$$file"; \
    done

tcx2gpx:
	@source $(VENV_PATH)/bin/activate && \
	python3 scripts/tcx2gpx.py '$(STRAVA_DIR)';

summary:
	@source $(VENV_PATH)/bin/activate && \
	python3 scripts/summary.py '$(STRAVA_DIR)' $(STRAVA_SUMMARY);

.PHONY: all venv install unpack tcx2gpx summary