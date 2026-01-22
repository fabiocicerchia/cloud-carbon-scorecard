# Cloud Region Carbon-Intensity Ratings

This repo provides a simple, auditable dataset to support carbon-aware region selection.

- **Input mapping**: `data/regions-map.yml` (provider region -> country)
- **Generator**: `scripts/generate_regions_score.py`
- **Output**: `data/regions-carbon-score.json`

## Quick start (local)

```bash
python3 -m venv .venv && source ./.venv/bin/activate
pip install pandas requests pyyaml
python scripts/generate_regions_score.py
```

## Notes

- The starter mapping includes common regions for AWS/GCP/Azure plus a more complete set for smaller providers.
- To truly cover **all** regions, extend `data/regions-map.yml` (PRs welcome).
