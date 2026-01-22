#!/usr/bin/env python3
"""Generate cloud region carbon-intensity ratings.

What it does
- Reads `data/regions-map.yml` (provider -> region -> country)
- Downloads OWID grapher dataset for lifecycle carbon intensity of electricity
  (`carbon-intensity-electricity`)
- Picks the latest available year per country
- Computes a rating band (A-F, or U for unknown)
- Writes `data/regions-carbon-score.json`

Why this design
- Mapping every cloud region to a specific grid zone is messy and changes over time.
  Keeping a simple, auditable mapping file makes updates straightforward.
- OWID/Ember is updated annually and is easy to fetch without credentials.

If you need real-time/subnational data
- Swap the OWID join for Electricity Maps (requires an API key and zone mapping).
"""

from __future__ import annotations

import json
import sys
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Any, Tuple, Optional

import pandas as pd
import requests
import yaml


OWID_CSV = "https://ourworldindata.org/grapher/carbon-intensity-electricity.csv"

RATING_BANDS = [
    ("A", 0, 100),
    ("B", 100, 200),
    ("C", 200, 350),
    ("D", 350, 500),
    ("E", 500, 650),
    ("F", 650, None),
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

RATING_COLORS = {
    "A": "#22c55e",  # Green
    "B": "#eab308",  # Yellow
    "C": "#f97316",  # Orange
    "D": "#92400e",  # Brown
    "E": "#dc2626",  # Red
    "F": "#9333ea",  # Purple
    "U": "#9ca3af",  # Gray (Unknown)
}


def rating_for(value: Optional[float]) -> str:
    if value is None or pd.isna(value):
        return "U"
    for label, lo, hi in RATING_BANDS:
        if value >= lo and (hi is None or value < hi):
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
        out[str(provider)] = {str(k): str(v) for k, v in regions.items()}
    return out


def load_owid_latest() -> Tuple[Dict[str, float], Dict[str, Any]]:
    df = pd.read_csv(OWID_CSV)
    # OWID grapher format: Entity, Code, Year, <metric>
    metric_col = [c for c in df.columns if c not in ("Entity", "Code", "Year")][0]
    df = df.dropna(subset=[metric_col])
    df["Year"] = df["Year"].astype(int)

    # Latest per Entity (country/region)
    latest_idx = df.groupby("Entity")["Year"].idxmax()
    latest = df.loc[latest_idx, ["Entity", "Year", metric_col]].copy()
    latest = latest.rename(columns={metric_col: "gco2e_per_kwh"})
    intensity_by_entity = dict(zip(latest["Entity"], latest["gco2e_per_kwh"]))

    meta = {
        "metric_col": metric_col,
        "years": {
            "min": int(df["Year"].min()),
            "max": int(df["Year"].max()),
        },
        "row_count": int(df.shape[0]),
    }
    return intensity_by_entity, meta


def resolve_country_to_entity(country: str, entities: Dict[str, float]) -> Optional[str]:
    """Resolve ISO2 like 'DE' or common country names to OWID Entity keys."""
    # Fast path: exact match
    if country in entities:
        return country

    iso2_map = {
        "US": "United States",
        "GB": "United Kingdom",
        "IE": "Ireland",
        "DE": "Germany",
        "NL": "Netherlands",
        "FR": "France",
        "PL": "Poland",
        "CA": "Canada",
        "SG": "Singapore",
        "IN": "India",
        "FI": "Finland",
        "AU": "Australia",
        "JP": "Japan",
        "KR": "South Korea",
        "AE": "United Arab Emirates",
        "ZA": "South Africa",
        "BR": "Brazil",
        "ES": "Spain",
        "IT": "Italy",
        "SE": "Sweden",
        "NO": "Norway",
        "CH": "Switzerland",
        "BE": "Belgium",
        "AT": "Austria",
        "PT": "Portugal",
        "DK": "Denmark",
        "CZ": "Czechia",
        "IL": "Israel",
        "MX": "Mexico",
    }
    if country in iso2_map and iso2_map[country] in entities:
        return iso2_map[country]

    # Try case-insensitive match
    c_low = country.strip().lower()
    for ent in entities.keys():
        if ent.lower() == c_low:
            return ent

    return None


def generate_markdown(data: Dict[str, Any], output_path: str) -> None:
    """Generate a markdown file with ratings and colored emojis."""
    lines = ["# Cloud Carbon Scorecard\n"]
    lines.append(f"_Generated: {data['generated_at_utc']}_\n")
    lines.append("\n## Rating Bands\n")
    lines.append("Carbon intensity in gCO₂e/kWh:\n")

    # Rating legend
    for label, lo, hi in RATING_BANDS:
        emoji = RATING_EMOJIS.get(label, "")
        range_str = f"{lo}-{hi}" if hi is not None else f"{lo}+"
        lines.append(f"- {emoji} **{label}**: {range_str} gCO₂e/kWh\n")
    lines.append(f"- {RATING_EMOJIS['U']} **U**: Unknown/No data\n")

    lines.append("\n## Ratings by Provider\n")

    rating_order = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "U": 6}

    for provider, prov_data in sorted(data["providers"].items()):
        lines.append(f"\n### {provider.upper()}\n")
        lines.append("\n| Region | Country | Rating | Carbon Intensity (gCO₂e/kWh) |\n")
        lines.append("|--------|---------|--------|------------------------------|\n")

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
            rating_order.get(x["rating"], 99),
            x["intensity"] if x["intensity"] is not None else 999999,
            x["region_id"]
        ))

        for region in regions:
            emoji = RATING_EMOJIS.get(region["rating"], "")
            intensity_str = f"{region['intensity']:.2f}" if region["intensity"] is not None else "N/A"
            lines.append(f"| `{region['region_id']}` | {region['country']} | {emoji} {region['rating']} | {intensity_str} |\n")

    # Add methodology section
    lines.append("\n## Methodology\n")
    source = data["methodology"]["grid_intensity_source"]
    lines.append(f"**Data Source:** {source['name']}\n")
    lines.append(f"- Dataset: `{source['dataset']}`\n")
    lines.append(f"- Metric: {source['metric']}\n")
    lines.append(f"- Latest year in dataset: {source['latest_year_in_dataset']}\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(lines)


def main() -> int:
    region_map = load_region_map("data/regions-map.yml")
    intensity_by_entity, owid_meta = load_owid_latest()

    out: Dict[str, Any] = {
        "schema_version": "1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "methodology": {
            "grid_intensity_source": {
                "name": "Our World in Data (Ember)",
                "dataset": "carbon-intensity-electricity",
                "metric": "lifecycle_carbon_intensity_gco2e_per_kwh",
                "owid_metric_column": owid_meta["metric_col"],
                "latest_year_in_dataset": owid_meta["years"]["max"],
            },
            "rating_bands_gco2e_per_kwh": {k: [lo, hi] for (k, lo, hi) in RATING_BANDS} | {"U": None},
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
                "owid_entity": ent,
                "grid_intensity_gco2e_per_kwh": None if intensity is None else float(intensity),
                "rating": rating,
            }
        out["providers"][provider] = prov_obj

    with open("data/regions-carbon-score.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=True)

    print("Wrote data/regions-carbon-score.json")

    # Generate markdown scorecard
    generate_markdown(out, "SCORECARD.md")
    print("Wrote SCORECARD.md")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
