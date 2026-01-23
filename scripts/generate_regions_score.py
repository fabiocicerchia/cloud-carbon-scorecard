#!/usr/bin/env python3
"""Generate cloud region carbon-intensity ratings.

What it does
- Reads `data/regions-map.yml` (provider -> region -> country)
- Downloads Ember yearly electricity dataset for carbon intensity of electricity
- Picks the latest available year per country
- Computes a rating band (A-F, or U for unknown)
- Writes `data/regions-carbon-score.json`

Why this design
- Mapping every cloud region to a specific grid zone is messy and changes over time.
  Keeping a simple, auditable mapping file makes updates straightforward.
- Ember data is updated monthly and is easy to fetch without credentials.

If you need real-time/subnational data
- Swap the Ember join for Electricity Maps (requires an API key and zone mapping).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Dict, Any, Tuple, Optional

import pandas as pd
import yaml
from jinja2 import Environment, FileSystemLoader


EMBER_CSV = "https://files.ember-energy.org/public-downloads/yearly_full_release_long_format.csv"

# File paths
REGIONS_MAP_FILE = "data/regions-map.yml"
ISO2_COUNTRY_MAP_FILE = "data/iso2-country-map.yml"
REGIONS_SCORE_FILE = "data/regions-carbon-score.json"
README_FILE = "README.md"
TEMPLATE_FILE = "scripts/templates/scorecard.md.template"

RATING_BANDS = [
    ("A", 0, 100),
    ("B", 100, 200),
    ("C", 200, 350),
    ("D", 350, 500),
    ("E", 500, 650),
    ("F", 650, float('inf')),
]

RATING_EMOJIS = {
    "A": "🟢",  # Green circle
    "B": "🟡",  # Yellow circle
    "C": "🟠",  # Orange circle
    "D": "🟤",  # Brown circle
    "E": "🔴",  # Red circle
    "F": "🟣",  # Purple circle
    "U": "⚪",  # White circle (Unknown)
}

# Derive rating order from RATING_BANDS
RATING_ORDER = {label: idx for idx, (label, _, _) in enumerate(RATING_BANDS)}
RATING_ORDER["U"] = len(RATING_BANDS)

# Load ISO2 to country name mapping
def _load_iso2_map() -> Dict[str, str]:
    with open(ISO2_COUNTRY_MAP_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

ISO2_COUNTRY_MAP = _load_iso2_map()


def rating_for(value: Optional[float]) -> str:
    if value is None or pd.isna(value):
        return "U"
    for label, lo, hi in RATING_BANDS:
        if value >= lo and value < hi:
            return label
    return "U"


def load_region_map(path: str) -> Dict[str, Dict[str, str]]:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    # Normalize keys
    out: Dict[str, Dict[str, str]] = {}
    for provider, regions in data.items():
        if not isinstance(regions, dict):
            continue
        provider_key = str(provider)
        out[provider_key] = {}
        for region_id, country in regions.items():
            out[provider_key][str(region_id)] = str(country)
    return out


def load_ember_latest() -> Tuple[Dict[str, float], Dict[str, Any]]:
    df = pd.read_csv(EMBER_CSV)
    # Ember long format: Area, Year, Variable, Unit, Value
    # Filter for CO2 intensity variable
    df = df[df["Variable"] == "CO2 intensity"].copy()
    df = df.dropna(subset=["Value", "Year"])
    df["Year"] = df["Year"].astype(int)

    if df.empty:
        raise ValueError("No CO2 intensity data found in Ember dataset")

    # Latest per Area (country/region)
    latest_idx = df.groupby("Area")["Year"].idxmax()
    latest = df.loc[latest_idx, ["Area", "Year", "Value"]].copy()
    latest = latest.rename(columns={"Value": "gco2e_per_kwh"})
    intensity_by_entity = dict(zip(latest["Area"], latest["gco2e_per_kwh"]))

    meta = {
        "metric_col": "CO2 intensity",
        "years": {
            "min": int(df["Year"].min()),
            "max": int(df["Year"].max()),
        },
        "row_count": int(df.shape[0]),
    }
    return intensity_by_entity, meta


def resolve_country_to_entity(country: str, entities: Dict[str, float]) -> Optional[str]:
    """Resolve ISO2 like 'DE' or common country names to Ember Area keys."""
    # Fast path: exact match
    if country in entities:
        return country

    if country in ISO2_COUNTRY_MAP and ISO2_COUNTRY_MAP[country] in entities:
        return ISO2_COUNTRY_MAP[country]

    # Try case-insensitive match
    c_low = country.strip().lower()
    for ent in entities.keys():
        if ent.lower() == c_low:
            return ent

    return None


def generate_markdown(data: Dict[str, Any]) -> str:
    """Generate markdown content from template with ratings and colored emojis."""
    # Prepare provider data with sorted regions
    providers_data = {}
    for provider, prov_data in data["providers"].items():
        # Collect regions for this provider
        regions = []
        for region_id, region_data in prov_data["regions"].items():
            regions.append({
                "region_id": region_id,
                "rating": region_data["rating"],
                "country": region_data.get("country_input", ""),
                "intensity": region_data.get("grid_intensity_gco2e_per_kwh"),
            })

        # Sort by rating (A->F->U), then by intensity (low to high), then by region_id
        regions.sort(key=lambda x: (
            RATING_ORDER.get(x["rating"], 99),
            x["intensity"] if x["intensity"] is not None else 999999,
            x["region_id"]
        ))

        providers_data[provider] = {
            "regions": prov_data["regions"],
            "regions_sorted": regions
        }

    # Get methodology data
    source = data["methodology"]["grid_intensity_source"]

    # Setup Jinja2 environment
    template_dir = "scripts/templates"
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("scorecard.md.template")

    # Render template with data
    content = template.render(
        generated_at_utc=data["generated_at_utc"],
        rating_bands=RATING_BANDS,
        rating_emojis=RATING_EMOJIS,
        providers=providers_data,
        data_source_name=source["name"],
        dataset_url=source["dataset_url"],
        metric=source["metric"],
        latest_year=source["latest_year_in_dataset"],
        inf=float('inf')
    )

    return content


def update_readme_with_scorecard(scorecard_content: str, readme_path: str) -> None:
    """Update README.md with the scorecard content."""
    # Read the current README
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()

    # Define markers for the scorecard section
    start_marker = "<!-- SCORECARD_START -->"
    end_marker = "<!-- SCORECARD_END -->"

    # Check if markers exist
    if start_marker in readme_content and end_marker in readme_content:
        # Replace content between markers
        start_idx = readme_content.find(start_marker)
        end_idx = readme_content.find(end_marker) + len(end_marker)
        new_readme = (
            readme_content[:start_idx] +
            f"{start_marker}\n\n{scorecard_content}\n\n{end_marker}" +
            readme_content[end_idx:]
        )
    else:
        # Append scorecard to the end with markers
        new_readme = readme_content.rstrip() + f"\n\n{start_marker}\n\n{scorecard_content}\n\n{end_marker}\n"

    # Write updated README
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_readme)


def main() -> int:
    region_map = load_region_map(REGIONS_MAP_FILE)
    intensity_by_entity, ember_meta = load_ember_latest()

    out: Dict[str, Any] = {
        "schema_version": "1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "methodology": {
            "grid_intensity_source": {
                "name": "Ember",
                "dataset_url": EMBER_CSV,
                "metric": ember_meta["metric_col"],
                "latest_year_in_dataset": ember_meta["years"]["max"],
            },
            "rating_bands_gco2e_per_kwh": {k: [lo, hi if hi != float('inf') else None] for (k, lo, hi) in RATING_BANDS} | {"U": None},
        },
        "providers": {},
    }

    for provider, regions in sorted(region_map.items()):
        prov_obj: Dict[str, Any] = {"regions": {}}
        for region_id, country in sorted(regions.items()):
            ent = resolve_country_to_entity(country, intensity_by_entity)
            intensity = intensity_by_entity.get(ent) if ent else None
            rating = rating_for(intensity)
            prov_obj["regions"][region_id] = {
                "country_input": country,
                "ember_area": ent,
                "grid_intensity_gco2e_per_kwh": None if intensity is None else float(intensity),
                "rating": rating,
            }
        out["providers"][provider] = prov_obj

    with open(REGIONS_SCORE_FILE, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=True)

    print(f"Wrote {REGIONS_SCORE_FILE}")

    # Generate markdown scorecard content and inject directly into README
    scorecard_content = generate_markdown(out)
    update_readme_with_scorecard(scorecard_content, README_FILE)
    print(f"Updated {README_FILE} with scorecard")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
