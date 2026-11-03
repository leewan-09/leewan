# Chart assets

The files in `src/assets/chart` are generated from OpenStreetMap data (© OpenStreetMap contributors, ODbL).
They're committed, so you only need this to refresh the map or change how it looks.

```bash
mkdir -p scripts/chart/.data
curl -L -o scripts/chart/.data/maldives.osm.pbf https://download.geofabrik.de/asia/maldives-latest.osm.pbf
python3 -I scripts/chart/extract_osm.py scripts/chart/.data/maldives.osm.pbf scripts/chart/.data/parsed.json
python3 -I scripts/chart/build_chart.py scripts/chart/.data/parsed.json src/assets/chart
```

The scripts use only the Python standard library.

`build_chart.py` also draws one chart for each project card. Each must show something true about where that project works, so check the stop lists in the script against the operators' timetables when a route changes.
