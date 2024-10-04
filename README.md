# strava-summary

Steps:

1. Get data from Strava with [Bulk Export](https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export#h_01GG58HC4F1BGQ9PQZZVANN6WF)
2. Update `STRAVA_DIR` inside `Makefile`
3. Setup Python venv and install dependencies: `make`
3. Uncompress the files: `make unpack`
4. Convert TCX to GPX to simplify parsing: `make tcx2gpx`
5. Create summary: `make summary`

View summary from `data/strava.csv`
