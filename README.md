# Cloud Region Carbon-Intensity Ratings

This repo provides a simple, auditable dataset to support carbon-aware region selection.

- **Input mapping**: `data/regions-map.yml` (provider region -> country)
- **Generator**: `scripts/generate_regions_score.py`
- **Output**: `data/regions-carbon-score.json`

<!-- SCORECARD_START -->

## Cloud Carbon Scorecard
_Generated: 2026-01-23T18:07:04.153968+00:00_

### Rating Bands
Carbon intensity in gCO₂e/kWh:
- 🟢 **A**: 0-100 gCO₂e/kWh
- 🟡 **B**: 100-200 gCO₂e/kWh
- 🟠 **C**: 200-350 gCO₂e/kWh
- 🟤 **D**: 350-500 gCO₂e/kWh
- 🔴 **E**: 500-650 gCO₂e/kWh
- 🟣 **F**: 650+ gCO₂e/kWh
- ⚪ **U**: Unknown/No data

### Ratings by Provider

#### ALIBABA

| Region | Country | Rating | Carbon Intensity (gCO₂e/kWh) |
|--------|---------|--------|------------------------------|
| `eu-central-1` | DE | 🟠 C | 331.60 |
| `me-east-1` | AE | 🟤 D | 467.51 |
| `ap-northeast-1` | JP | 🟤 D | 483.43 |
| `ap-southeast-1` | SG | 🟤 D | 498.74 |
| `ap-south-1` | IN | 🟣 F | 707.45 |
| `ap-southeast-3` | MY | ⚪ U | N/A |
| `ap-southeast-5` | ID | ⚪ U | N/A |
| `cn-beijing` | CN | ⚪ U | N/A |
| `cn-hangzhou` | CN | ⚪ U | N/A |
| `cn-hongkong` | HK | ⚪ U | N/A |
| `cn-huhehaote` | CN | ⚪ U | N/A |
| `cn-qingdao` | CN | ⚪ U | N/A |
| `cn-shanghai` | CN | ⚪ U | N/A |
| `cn-shenzhen` | CN | ⚪ U | N/A |
| `cn-zhangjiakou` | CN | ⚪ U | N/A |
| `us-east-1` | US | ⚪ U | N/A |
| `us-west-1` | US | ⚪ U | N/A |

#### AWS

| Region | Country | Rating | Carbon Intensity (gCO₂e/kWh) |
|--------|---------|--------|------------------------------|
| `eu-central-2` | CH | 🟢 A | 32.65 |
| `eu-north-1` | SE | 🟢 A | 35.33 |
| `eu-west-3` | FR | 🟢 A | 41.79 |
| `sa-east-1` | BR | 🟡 B | 106.06 |
| `eu-south-2` | ES | 🟡 B | 153.26 |
| `ca-central-1` | CA | 🟡 B | 185.35 |
| `ca-west-1` | CA | 🟡 B | 185.35 |
| `eu-west-2` | GB | 🟠 C | 217.09 |
| `eu-west-1` | IE | 🟠 C | 255.89 |
| `eu-south-1` | IT | 🟠 C | 285.26 |
| `eu-central-1` | DE | 🟠 C | 331.60 |
| `ap-northeast-2` | KR | 🟤 D | 415.51 |
| `me-central-1` | AE | 🟤 D | 467.51 |
| `mx-central-1` | MX | 🟤 D | 483.14 |
| `ap-northeast-1` | JP | 🟤 D | 483.43 |
| `ap-northeast-3` | JP | 🟤 D | 483.43 |
| `ap-southeast-1` | SG | 🟤 D | 498.74 |
| `ap-southeast-2` | AU | 🔴 E | 553.83 |
| `ap-southeast-4` | AU | 🔴 E | 553.83 |
| `il-central-1` | IL | 🔴 E | 567.26 |
| `ap-south-1` | IN | 🟣 F | 707.45 |
| `ap-south-2` | IN | 🟣 F | 707.45 |
| `af-south-1` | ZA | 🟣 F | 713.17 |
| `ap-east-1` | HK | ⚪ U | N/A |
| `ap-east-2` | TW | ⚪ U | N/A |
| `ap-southeast-3` | ID | ⚪ U | N/A |
| `ap-southeast-5` | MY | ⚪ U | N/A |
| `ap-southeast-6` | NZ | ⚪ U | N/A |
| `ap-southeast-7` | TH | ⚪ U | N/A |
| `me-south-1` | BH | ⚪ U | N/A |
| `us-east-1` | US | ⚪ U | N/A |
| `us-east-2` | US | ⚪ U | N/A |
| `us-west-1` | US | ⚪ U | N/A |
| `us-west-2` | US | ⚪ U | N/A |

#### AZURE

| Region | Country | Rating | Carbon Intensity (gCO₂e/kWh) |
|--------|---------|--------|------------------------------|
| `switzerlandnorth` | CH | 🟢 A | 32.65 |
| `switzerlandwest` | CH | 🟢 A | 32.65 |
| `swedencentral` | SE | 🟢 A | 35.33 |
| `francecentral` | FR | 🟢 A | 41.79 |
| `francesouth` | FR | 🟢 A | 41.79 |
| `brazilsouth` | BR | 🟡 B | 106.06 |
| `brazilsoutheast` | BR | 🟡 B | 106.06 |
| `austriaeast` | AT | 🟡 B | 113.91 |
| `denmarkeast` | DK | 🟡 B | 114.30 |
| `belgiumcentral` | BE | 🟡 B | 149.77 |
| `spaincentral` | ES | 🟡 B | 153.26 |
| `canadacentral` | CA | 🟡 B | 185.35 |
| `canadaeast` | CA | 🟡 B | 185.35 |
| `uksouth` | GB | 🟠 C | 217.09 |
| `ukwest` | GB | 🟠 C | 217.09 |
| `westeurope` | NL | 🟠 C | 253.22 |
| `northeurope` | IE | 🟠 C | 255.89 |
| `italynorth` | IT | 🟠 C | 285.26 |
| `germanynorth` | DE | 🟠 C | 331.60 |
| `germanywestcentral` | DE | 🟠 C | 331.60 |
| `koreacentral` | KR | 🟤 D | 415.51 |
| `koreasouth` | KR | 🟤 D | 415.51 |
| `uaecentral` | AE | 🟤 D | 467.51 |
| `uaenorth` | AE | 🟤 D | 467.51 |
| `mexicocentral` | MX | 🟤 D | 483.14 |
| `japaneast` | JP | 🟤 D | 483.43 |
| `japanwest` | JP | 🟤 D | 483.43 |
| `southeastasia` | SG | 🟤 D | 498.74 |
| `australiacentral` | AU | 🔴 E | 553.83 |
| `australiacentral2` | AU | 🔴 E | 553.83 |
| `australiaeast` | AU | 🔴 E | 553.83 |
| `australiasoutheast` | AU | 🔴 E | 553.83 |
| `israelcentral` | IL | 🔴 E | 567.26 |
| `polandcentral` | PL | 🔴 E | 592.20 |
| `centralindia` | IN | 🟣 F | 707.45 |
| `southindia` | IN | 🟣 F | 707.45 |
| `westindia` | IN | 🟣 F | 707.45 |
| `southafricanorth` | ZA | 🟣 F | 713.17 |
| `southafricawest` | ZA | 🟣 F | 713.17 |
| `centralus` | US | ⚪ U | N/A |
| `chilecentral` | CL | ⚪ U | N/A |
| `eastasia` | HK | ⚪ U | N/A |
| `eastus` | US | ⚪ U | N/A |
| `eastus2` | US | ⚪ U | N/A |
| `indonesiacentral` | ID | ⚪ U | N/A |
| `malaysiawest` | MY | ⚪ U | N/A |
| `newzealandnorth` | NZ | ⚪ U | N/A |
| `northcentralus` | US | ⚪ U | N/A |
| `norwayeast` | False | ⚪ U | N/A |
| `norwaywest` | False | ⚪ U | N/A |
| `qatarcentral` | QA | ⚪ U | N/A |
| `southcentralus` | US | ⚪ U | N/A |
| `westcentralus` | US | ⚪ U | N/A |
| `westus` | US | ⚪ U | N/A |
| `westus2` | US | ⚪ U | N/A |
| `westus3` | US | ⚪ U | N/A |

#### DIGITALOCEAN

| Region | Country | Rating | Carbon Intensity (gCO₂e/kWh) |
|--------|---------|--------|------------------------------|
| `tor1` | CA | 🟡 B | 185.35 |
| `lon1` | GB | 🟠 C | 217.09 |
| `ams3` | NL | 🟠 C | 253.22 |
| `fra1` | DE | 🟠 C | 331.60 |
| `sgp1` | SG | 🟤 D | 498.74 |
| `syd1` | AU | 🔴 E | 553.83 |
| `blr1` | IN | 🟣 F | 707.45 |
| `atl1` | US | ⚪ U | N/A |
| `nyc1` | US | ⚪ U | N/A |
| `nyc2` | US | ⚪ U | N/A |
| `nyc3` | US | ⚪ U | N/A |
| `sfo2` | US | ⚪ U | N/A |
| `sfo3` | US | ⚪ U | N/A |

#### GCP

| Region | Country | Rating | Carbon Intensity (gCO₂e/kWh) |
|--------|---------|--------|------------------------------|
| `europe-west6` | CH | 🟢 A | 32.65 |
| `europe-north2` | SE | 🟢 A | 35.33 |
| `europe-west9` | FR | 🟢 A | 41.79 |
| `europe-north1` | FI | 🟢 A | 56.81 |
| `southamerica-east1` | BR | 🟡 B | 106.06 |
| `europe-west1` | BE | 🟡 B | 149.77 |
| `europe-southwest1` | ES | 🟡 B | 153.26 |
| `northamerica-northeast1` | CA | 🟡 B | 185.35 |
| `northamerica-northeast2` | CA | 🟡 B | 185.35 |
| `europe-west2` | GB | 🟠 C | 217.09 |
| `europe-west4` | NL | 🟠 C | 253.22 |
| `europe-west12` | IT | 🟠 C | 285.26 |
| `europe-west8` | IT | 🟠 C | 285.26 |
| `europe-west10` | DE | 🟠 C | 331.60 |
| `europe-west3` | DE | 🟠 C | 331.60 |
| `asia-northeast3` | KR | 🟤 D | 415.51 |
| `northamerica-south1` | MX | 🟤 D | 483.14 |
| `asia-northeast1` | JP | 🟤 D | 483.43 |
| `asia-northeast2` | JP | 🟤 D | 483.43 |
| `asia-southeast1` | SG | 🟤 D | 498.74 |
| `australia-southeast1` | AU | 🔴 E | 553.83 |
| `australia-southeast2` | AU | 🔴 E | 553.83 |
| `me-west1` | IL | 🔴 E | 567.26 |
| `europe-central2` | PL | 🔴 E | 592.20 |
| `asia-south1` | IN | 🟣 F | 707.45 |
| `asia-south2` | IN | 🟣 F | 707.45 |
| `africa-south1` | ZA | 🟣 F | 713.17 |
| `asia-east1` | TW | ⚪ U | N/A |
| `asia-east2` | HK | ⚪ U | N/A |
| `asia-southeast2` | ID | ⚪ U | N/A |
| `asia-southeast3` | TH | ⚪ U | N/A |
| `me-central1` | QA | ⚪ U | N/A |
| `me-central2` | SA | ⚪ U | N/A |
| `southamerica-west1` | CL | ⚪ U | N/A |
| `us-central1` | US | ⚪ U | N/A |
| `us-east1` | US | ⚪ U | N/A |
| `us-east4` | US | ⚪ U | N/A |
| `us-east5` | US | ⚪ U | N/A |
| `us-south1` | US | ⚪ U | N/A |
| `us-west1` | US | ⚪ U | N/A |
| `us-west2` | US | ⚪ U | N/A |
| `us-west3` | US | ⚪ U | N/A |
| `us-west4` | US | ⚪ U | N/A |

#### HETZNER

| Region | Country | Rating | Carbon Intensity (gCO₂e/kWh) |
|--------|---------|--------|------------------------------|
| `hel1` | FI | 🟢 A | 56.81 |
| `fsn1` | DE | 🟠 C | 331.60 |
| `nbg1` | DE | 🟠 C | 331.60 |
| `sin` | SG | 🟤 D | 498.74 |
| `ash` | US | ⚪ U | N/A |
| `hil` | US | ⚪ U | N/A |

#### ORACLE

| Region | Country | Rating | Carbon Intensity (gCO₂e/kWh) |
|--------|---------|--------|------------------------------|
| `switzerland-north-zurich` | CH | 🟢 A | 32.65 |
| `sweden-central-stockholm` | SE | 🟢 A | 35.33 |
| `france-central-paris` | FR | 🟢 A | 41.79 |
| `france-south-marseille` | FR | 🟢 A | 41.79 |
| `brazil-east-sao-paulo` | BR | 🟡 B | 106.06 |
| `brazil-southeast-vinhedo` | BR | 🟡 B | 106.06 |
| `spain-central-madrid` | ES | 🟡 B | 153.26 |
| `canada-southeast-montreal` | CA | 🟡 B | 185.35 |
| `canada-southeast-toronto` | CA | 🟡 B | 185.35 |
| `uk-south-london` | GB | 🟠 C | 217.09 |
| `uk-west-newport` | GB | 🟠 C | 217.09 |
| `netherlands-northwest-amsterdam` | NL | 🟠 C | 253.22 |
| `italy-northwest-milan` | IT | 🟠 C | 285.26 |
| `germany-central-frankfurt` | DE | 🟠 C | 331.60 |
| `south-korea-central-seoul` | KR | 🟤 D | 415.51 |
| `south-korea-north-chuncheon` | KR | 🟤 D | 415.51 |
| `uae-central-abu-dhabi` | AE | 🟤 D | 467.51 |
| `uae-east-dubai` | AE | 🟤 D | 467.51 |
| `mexico-central-queretaro` | MX | 🟤 D | 483.14 |
| `mexico-northeast-monterrey` | MX | 🟤 D | 483.14 |
| `japan-central-osaka` | JP | 🟤 D | 483.43 |
| `japan-east-tokyo` | JP | 🟤 D | 483.43 |
| `singapore-singapore` | SG | 🟤 D | 498.74 |
| `singapore-west-singapore` | SG | 🟤 D | 498.74 |
| `australia-east-sydney` | AU | 🔴 E | 553.83 |
| `australia-southeast-melbourne` | AU | 🔴 E | 553.83 |
| `israel-central-jerusalem` | IL | 🔴 E | 567.26 |
| `india-south-hyderabad` | IN | 🟣 F | 707.45 |
| `india-west-mumbai` | IN | 🟣 F | 707.45 |
| `south-africa-central-johannesburg` | ZA | 🟣 F | 713.17 |
| `chile-central-santiago` | CL | ⚪ U | N/A |
| `chile-west-valparaiso` | CL | ⚪ U | N/A |
| `colombia-central-bogota` | CO | ⚪ U | N/A |
| `indonesia-north-batam` | ID | ⚪ U | N/A |
| `saudi-arabia-central-riyadh` | SA | ⚪ U | N/A |
| `saudi-arabia-west-jeddah` | SA | ⚪ U | N/A |
| `serbia-central-jovanovac` | RS | ⚪ U | N/A |
| `us-east-ashburn` | US | ⚪ U | N/A |
| `us-midwest-chicago` | US | ⚪ U | N/A |
| `us-west-phoenix` | US | ⚪ U | N/A |
| `us-west-san-jose` | US | ⚪ U | N/A |

#### OVH

| Region | Country | Rating | Carbon Intensity (gCO₂e/kWh) |
|--------|---------|--------|------------------------------|
| `GRA` | FR | 🟢 A | 41.79 |
| `GRA-SNC` | FR | 🟢 A | 41.79 |
| `PAR` | FR | 🟢 A | 41.79 |
| `RBX` | FR | 🟢 A | 41.79 |
| `RBX-SNC` | FR | 🟢 A | 41.79 |
| `SBG` | FR | 🟢 A | 41.79 |
| `SBG-SNC` | FR | 🟢 A | 41.79 |
| `BHS` | CA | 🟡 B | 185.35 |
| `YYZ` | CA | 🟡 B | 185.35 |
| `ERI` | GB | 🟠 C | 217.09 |
| `LIM` | DE | 🟠 C | 331.60 |
| `SGP` | SG | 🟤 D | 498.74 |
| `SYD` | AU | 🔴 E | 553.83 |
| `WAW` | PL | 🔴 E | 592.20 |
| `YNM` | IN | 🟣 F | 707.45 |
| `HIL` | US | ⚪ U | N/A |
| `VIN` | US | ⚪ U | N/A |

#### SCALEWAY

| Region | Country | Rating | Carbon Intensity (gCO₂e/kWh) |
|--------|---------|--------|------------------------------|
| `fr-par` | FR | 🟢 A | 41.79 |
| `fr-par-1` | FR | 🟢 A | 41.79 |
| `fr-par-2` | FR | 🟢 A | 41.79 |
| `fr-par-3` | FR | 🟢 A | 41.79 |
| `nl-ams` | NL | 🟠 C | 253.22 |
| `nl-ams-1` | NL | 🟠 C | 253.22 |
| `nl-ams-2` | NL | 🟠 C | 253.22 |
| `nl-ams-3` | NL | 🟠 C | 253.22 |
| `pl-waw` | PL | 🔴 E | 592.20 |
| `pl-waw-1` | PL | 🔴 E | 592.20 |
| `pl-waw-2` | PL | 🔴 E | 592.20 |
| `pl-waw-3` | PL | 🔴 E | 592.20 |

### Methodology
**Data Source:** Ember
- Dataset URL: https://files.ember-energy.org/public-downloads/yearly_full_release_long_format.csv
- Metric: CO2 intensity
- Latest year in dataset: 2025


<!-- SCORECARD_END -->

## Quick start (local)

```bash
python3 -m venv .venv && source ./.venv/bin/activate
pip install pandas requests pyyaml
python scripts/generate_regions_score.py
```

## Notes

- The starter mapping includes common regions for AWS/GCP/Azure plus a more complete set for smaller providers.
- To truly cover **all** regions, extend `data/regions-map.yml` (PRs welcome).
