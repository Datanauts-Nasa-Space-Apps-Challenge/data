# Lunar Landing Site Navigator — Data Documentation

## Overview

This repository contains the structured geospatial and mission reference datasets used by **Lunar Landing Site Navigator**, a platform developed by Datanauts for exploring, evaluating, and comparing potential lunar landing locations.

The datasets provide a common information layer connecting:

- Historical, ongoing, and planned lunar missions.
- Named lunar geographical locations and candidate landing sites.
- Geographic coordinates (latitude and longitude).
- Lunar Grid Reference System (LGRS) identifiers.
- Relationships between missions and their associated lunar locations.
- Precomputed terrain horizon profiles for selected locations.

The objective is to establish a consistent spatial reference framework that allows the application to display lunar locations, associate them with missions, analyze their surrounding terrain, and support future landing-site evaluation workflows.

The repository separates mission information from geographical information, connecting both through unique identifiers.

---

# 1. Repository Data Architecture

The current data model consists of three main components:

| Dataset | Purpose | Main information |
|---|---|---|
| `missions.json` | Mission catalogue | Mission names, agencies, identifiers, and statuses |
| `sites.json` | Lunar geographical catalogue | Site names, coordinates, LGRS references, and mission relationships |
| `missions.schema.json` | Data validation | JSON structure and constraints for mission records |

The geographical dataset also contains optional precomputed horizon information for selected locations.

## 1.1. Data relationships

The data model follows a one-to-many relationship between missions and geographical sites, while allowing multiple missions to share the same geographical location.

For example:

- A mission is uniquely identified by its `id`.
- A geographical location is uniquely identified by its own `id`.
- The `mission_ids` property in a geographical record references one or more missions from the mission catalogue.

Conceptually:

```text
                 missions.json
                       |
                       |
                  Mission ID
                       |
                       |
                 sites.json
                       |
          +------------+------------+
          |            |            |
       Site 1       Site 2       Site 3
          |            |            |
       LGRS ID      LGRS ID      LGRS ID
          |            |            |
       Lat/Long     Lat/Long     Lat/Long
          |            |            |
       Horizon      Horizon      Horizon
       Profile      Profile      Profile
```

The relationship is implemented through identifiers rather than duplicated mission information.

This approach avoids unnecessary data duplication and allows mission information and geographical information to evolve independently.

---

# 2. Lunar Mission Dataset

## 2.1. Purpose

The mission dataset provides a structured catalogue of lunar exploration missions.

It includes historical missions, unsuccessful attempts, partially successful missions, and future planned missions.

Its purpose is to provide historical and operational context to the geographical locations represented in the application.

The dataset currently contains 49 mission records.

## 2.2. Data structure

Each mission is represented by the following properties:

| Field | Type | Description |
|---|---|---|
| `id` | Integer | Unique internal mission identifier |
| `name` | String | Official or commonly used mission name |
| `agency` | String | Responsible space agency or organization |
| `status` | String | Mission outcome or planning status |

Example:

```json
{
  "id": 1,
  "name": "Luna 9",
  "agency": "USSR",
  "status": "completed"
}
```

### Mission identifiers

The `id` property provides a stable internal reference for each mission.

These identifiers are used by the geographical dataset to associate missions with their corresponding lunar locations.

They are internal database identifiers, not official NASA mission identifiers.

### Space agencies

The `agency` field identifies the organization responsible for the mission.

The catalogue includes organizations such as:

- NASA (United States).
- USSR space program.
- CNSA (China).
- ISRO (India).
- JAXA (Japan).
- ESA (Europe).

Some records combine a national space agency with a commercial contractor or mission operator.

### Mission status classification

The dataset uses four possible status values:

| Status | Meaning |
|---|---|
| `completed` | Mission classified as successfully completed |
| `partial` | Mission achieved some objectives but experienced significant limitations |
| `failed` | Mission classified as unsuccessful |
| `planned` | Mission included in the future mission catalogue |

These categories provide a simplified classification for visualization and filtering.

They should not be interpreted as a complete technical assessment of mission success. In particular, the distinction between mission completion, landing success, and scientific objective completion may require more detailed mission-specific information.

---

# 3. Lunar Geographical Sites Dataset

## 3.1. Purpose

The geographical dataset contains named lunar locations and candidate landing areas.

It combines historical landing locations with scientifically relevant geographical features, particularly around the lunar south pole.

The dataset currently contains 60 geographical records.

These records include:

- Historical landing locations.
- Lunar craters.
- Mountainous regions.
- Highlands.
- Maria and other geological formations.
- Potential future landing areas.
- Locations associated with planned lunar missions.

The dataset provides the geographical foundation for the application's map visualization and site comparison functionality.

## 3.2. Data structure

Each geographical record contains the following properties:

| Field | Type | Description |
|---|---|---|
| `id` | Integer | Unique internal site identifier |
| `name` | String | Name of the lunar geographical location |
| `cell_id` | String | Associated Lunar Grid Reference System coordinate |
| `lat` | Number | Lunar latitude in decimal degrees |
| `long` | Number | Lunar longitude in decimal degrees |
| `mission_ids` | Integer array | Identifiers of associated missions |
| `horizon_profile` | Number array | Optional precomputed terrain horizon measurements |

Example:

```json
{
  "id": 1,
  "name": "Shackleton",
  "cell_id": "B WV G64 T63",
  "lat": -89.67,
  "long": 129.78,
  "mission_ids": [42, 44]
}
```

Some records include a `horizon_profile` property containing an ordered sequence of numerical angular measurements.

## 3.3. Geographic coordinates

The `lat` and `long` fields represent the geographical position of each location.

Coordinates are expressed in decimal degrees.

- Latitude ranges from -90° to +90°.
- Longitude ranges from -180° to +180°.
- Negative latitude represents the lunar southern hemisphere.
- Positive latitude represents the lunar northern hemisphere.
- Longitude follows the convention used by the source geographical dataset.

For example:

```json
{
  "name": "Shackleton",
  "lat": -89.67,
  "long": 129.78
}
```

This indicates a location close to the lunar south pole.

These coordinates allow the application to position locations on a lunar map, associate them with topographic datasets, and calculate spatial relationships.

**Important:** Latitude and longitude alone do not define a complete spatial reference system. Coordinate datum, longitude convention, reference frame, and source metadata must also be consistent when combining external geospatial datasets.

---

# 4. Lunar Grid Reference System (LGRS)

## 4.1. Purpose

One of the central components of the project is the Lunar Grid Reference System (LGRS).

LGRS provides a hierarchical spatial reference system for identifying locations on the Moon.

It is inspired by Earth's Military Grid Reference System (MGRS) and provides a consistent way to identify lunar geographical areas at different spatial resolutions.

The system allows geographical information to be organized into standardized grid cells rather than relying exclusively on latitude and longitude.

This is particularly useful for:

- Identifying potential landing regions.
- Associating observations with specific geographical areas.
- Comparing neighboring locations.
- Organizing citizen-science annotations.
- Linking terrain features to imagery and scientific observations.
- Building a structured lunar geospatial knowledge base.

## 4.2. LGRS resolution hierarchy

The LGRS framework provides multiple spatial resolution levels:

| Resolution | Purpose |
|---|---|
| 25 km | Global geographical organization |
| 1 km | Regional subdivision |
| 100 m | Detailed local navigation |
| 10 m | Condensed coordinate representation |
| 1 m | Fine-grained spatial identification |

The system uses different projection approaches depending on the lunar geographical region.

These include:

- Lunar Transverse Mercator (LTM).
- Lunar Polar Stereographic (LPS).

The polar projection is particularly relevant to the south pole, where conventional transverse mapping approaches become less suitable.

## 4.3. Site grid references

Each geographical record includes a `cell_id` property.

Example:

```json
{
  "name": "Shackleton",
  "cell_id": "B WV G64 T63"
}
```

This property associates the geographical location with its corresponding LGRS reference.

The reference can be used to identify the location within the hierarchical lunar grid and to connect it with other geospatial information.

The grid identifier is stored as a string to preserve its alphanumeric structure.

It should be treated as an opaque spatial identifier by application components unless they explicitly implement the corresponding LGRS encoding and decoding rules.

The application can use this identifier as a common reference when organizing observations, terrain information, and other spatial datasets.

## 4.4. Relationship between coordinates and LGRS

Latitude and longitude and LGRS serve complementary purposes.

| Latitude / Longitude | LGRS |
|---|---|
| Represents a geographical position | Identifies a standardized grid location |
| Useful for map positioning | Useful for spatial indexing |
| Expressed in angular coordinates | Expressed as an alphanumeric reference |
| Suitable for coordinate transformations | Suitable for hierarchical spatial organization |

Using both systems provides flexibility when integrating different sources of lunar geographical information.

**Note:** An LGRS coordinate must be generated or validated using the official LGRS implementation. It should not be constructed by simply converting latitude and longitude into an arbitrary alphanumeric string.

---

# 5. Mission-to-Site Relationships

## 5.1. Purpose

The geographical dataset uses the `mission_ids` array to associate geographical locations with lunar missions.

This relationship makes it possible to connect historical exploration activities with the geographical features represented in the application.

Example:

```json
{
  "id": 34,
  "name": "Mare Tranquillitatis",
  "cell_id": "26N TF J03 V41",
  "lat": 0.674,
  "long": 23.473,
  "mission_ids": [5, 8, 30]
}
```

The application can resolve these identifiers against `missions.json` to retrieve the corresponding mission information.

Conceptually:

```typescript
const siteMissions = site.mission_ids.map((missionId) =>
  missions.find((mission) => mission.id === missionId)
);
```

This allows the interface to display the missions associated with a selected geographical location.

## 5.2. Multiple missions per location

A geographical location can be associated with multiple missions.

This is important because different missions may explore, land, impact, or operate within the same geographical region.

For example, multiple historical missions have been associated with Mare Tranquillitatis.

The dataset can therefore represent geographical locations as shared spatial references rather than creating an independent geographical record for every mission.

## 5.3. Locations without associated missions

An empty `mission_ids` array indicates that no mission association is currently recorded.

For example:

```json
{
  "id": 2,
  "name": "Spudis",
  "mission_ids": []
}
```

This does not indicate that the geographical location is unsuitable for exploration.

Many records represent candidate landing areas or scientifically interesting regions without a corresponding mission association in the current catalogue.

## 5.4. Referential integrity

The following relationship must be maintained:

```text
sites[].mission_ids[] -> missions[].id
```

Every mission identifier referenced by a geographical record should correspond to an existing mission record.

This can be validated programmatically to prevent broken relationships.

Additionally, mission-to-site associations should be interpreted as geographical associations, not necessarily proof of a successful landing at the exact coordinates represented by the site.

---

# 6. Terrain Horizon Profiles

## 6.1. Purpose

The `horizon_profile` property provides precomputed angular information about the surrounding terrain of selected geographical locations.

This information is particularly relevant to the lunar south pole, where the combination of extreme latitude and irregular terrain produces complex illumination conditions.

Unlike Earth, the Moon has an extremely small axial tilt relative to its orbital plane.

Consequently, the Sun remains close to the lunar horizon in polar regions.

Small differences in terrain elevation can therefore have a significant impact on whether a location receives direct sunlight.

A mountain ridge can block sunlight even when the Sun is geometrically above the local horizontal plane.

Horizon profiles help characterize this obstruction.

## 6.2. Data structure

The horizon profile is represented as an ordered array of numerical values.

Example:

```json
{
  "id": 1,
  "name": "Shackleton",
  "horizon_profile": [
    21.8,
    21.735,
    21.725,
    21.689,
    21.599
  ]
}
```

Each value represents an angular horizon measurement.

The values are expressed in degrees and describe the apparent elevation of the surrounding terrain relative to the local horizontal reference.

A larger positive value indicates that the surrounding terrain reaches a higher angular elevation in the corresponding direction.

A smaller value indicates a lower apparent terrain horizon.

Negative values can represent directions where the apparent horizon lies below the local horizontal reference, depending on the adopted horizon convention.

## 6.3. Physical interpretation

The horizon profile represents the terrain obstruction surrounding a particular location.

For a given direction, the terrain horizon defines the minimum solar elevation required for the Sun to become directly visible above the terrain.

Let:

- \(A\) represent the solar azimuth.
- \(h_{\odot}\) represent the apparent solar elevation.
- \(H(A)\) represent the terrain horizon elevation in the corresponding direction.

Direct sunlight is geometrically possible when:

\[
h_{\odot} > H(A)
\]

If:

\[
h_{\odot} \leq H(A)
\]

the surrounding terrain blocks the direct solar line of sight.

This relationship is fundamental for evaluating illumination at lunar polar locations.

It explains why two nearby locations can experience significantly different lighting conditions despite having similar geographical coordinates.

## 6.4. Horizon profile interpretation

The horizon profile can be used to:

1. Reconstruct the surrounding terrain horizon.
2. Identify directions with elevated terrain obstruction.
3. Evaluate whether the Sun can become visible above the local terrain.
4. Estimate potential sunlight windows when combined with solar position calculations.
5. Compare terrain obstruction between candidate landing sites.
6. Support the visualization of local illumination conditions.

The profile is especially useful when combined with astronomical calculations that determine the Sun's position at a particular time.

## 6.5. Relationship with solar visibility

The horizon profile does not independently determine whether a location is illuminated.

Solar visibility depends on both the terrain geometry and the Sun's position.

A simplified evaluation can be expressed as:

\[
V(A,t)=
\begin{cases}
1 & h_{\odot}(A,t)>H(A)\\
0 & h_{\odot}(A,t)\leq H(A)
\end{cases}
\]

Where:

- \(V\) represents direct solar visibility.
- \(A\) represents solar azimuth.
- \(t\) represents time.
- \(h_{\odot}(A,t)\) represents solar elevation.
- \(H(A)\) represents terrain horizon elevation.

This simplified model assumes a consistent angular reference and does not account for additional effects such as atmospheric refraction, which is negligible for most practical lunar surface calculations.

A more complete illumination model should also account for local surface slope, the orientation of the receiving terrain, and the finite angular size of the Sun.

## 6.6. Important implementation consideration

The current dataset contains numerical horizon profiles, but the JSON records do not explicitly document:

- The azimuth of the first sample.
- The angular interval between samples.
- The total number of samples.
- The reference direction and orientation convention.
- The exact elevation model used to generate the profiles.
- The observer height above the reference terrain.
- The algorithm used to calculate the apparent horizon.

These parameters must be documented alongside the generation process before the arrays can be interpreted as a fully specified directional horizon dataset.

In particular, an array index should not automatically be interpreted as an azimuth in degrees without confirming the sampling convention.

The profiles should therefore be treated as precomputed terrain measurements whose precise sampling metadata belongs to the calculation pipeline.

---

# 7. How the Dataset Supports Landing Site Evaluation

The datasets provide complementary information that can be combined to evaluate candidate lunar landing locations.

The main workflow consists of four stages.

## 7.1. Stage 1 — Geographical identification

The application retrieves the geographical record associated with a selected location.

It obtains:

- Site name.
- Geographic coordinates.
- LGRS reference.
- Associated mission identifiers.
- Available horizon information.

This provides the initial geographical context.

## 7.2. Stage 2 — Spatial integration

The coordinates are used to associate the selected location with external lunar datasets.

These include:

- LOLA elevation data.
- LROC orbital imagery.
- NASA Moon Trek geographical layers.
- LGRS spatial references.

This makes it possible to combine the site catalogue with detailed topographic and visual information.

## 7.3. Stage 3 — Terrain and illumination analysis

Where a horizon profile is available, it can be combined with solar positioning calculations to estimate periods of direct solar visibility.

The application can evaluate:

- Solar elevation.
- Solar azimuth.
- Terrain horizon obstruction.
- Potential sunlight windows.
- Local illumination variability.

These calculations help identify geographical areas with potentially favorable illumination characteristics.

## 7.4. Stage 4 — Mission comparison

The mission catalogue allows geographical locations to be placed within the broader context of lunar exploration.

Users can compare:

- Historical landing locations.
- Previously explored geographical regions.
- Proposed landing areas.
- Locations associated with planned missions.

By combining geographical information with terrain and illumination data, the application provides a unified environment for exploring alternative landing scenarios.

---

# 8. Data Processing and Validation

The datasets are structured as JSON to facilitate integration with the application's TypeScript-based architecture.

## 8.1. Mission schema validation

The mission catalogue includes a JSON Schema based on JSON Schema Draft 2020-12.

The schema defines:

- The root object structure.
- The `missions` array.
- Required mission properties.
- Data types.
- Minimum identifier values.
- Allowed mission status values.
- Restrictions on additional properties.

The schema ensures that mission records follow a consistent structure.

The allowed status values are:

```json
[
  "planned",
  "completed",
  "partial",
  "failed"
]
```

Each mission must include:

```json
[
  "id",
  "name",
  "agency",
  "status"
]
```

Additional properties are not permitted by the current mission schema.

## 8.2. Geographical data validation

The geographical dataset should also be validated to ensure consistency.

Recommended validation rules include:

| Field | Validation |
|---|---|
| `id` | Unique positive integer |
| `name` | Non-empty string |
| `cell_id` | Valid LGRS reference |
| `lat` | Numeric value between -90 and +90 |
| `long` | Numeric value between -180 and +180 |
| `mission_ids` | Array of valid mission identifiers |
| `horizon_profile` | Optional array of finite numerical values |

Additional validation should ensure that:

- Site identifiers are unique.
- Mission references exist.
- Coordinates are valid.
- LGRS references correspond to the provided coordinates.
- Horizon profiles follow a consistent sampling convention.
- Missing optional data does not break application rendering.

## 8.3. Missing and optional information

Not every geographical record contains a horizon profile.

Similarly, not every geographical location is associated with a mission.

These cases should be handled as valid data conditions rather than errors.

The application should distinguish between:

- Information that is unavailable.
- Information that has not been calculated.
- Information that is not applicable.

This is especially important when presenting comparative analyses.

A missing horizon profile must not be interpreted as a completely unobstructed horizon.

## 8.4. Schemas and validation

Both catalogues ship with a JSON Schema (draft 2020-12). They can be validated with:

```bash
python -m pip install jsonschema

python - <<'EOF'
import json, jsonschema
for data, schema in [("missions.json", "missions.schema.json"),
                     ("sites.json", "sites.schema.json")]:
    jsonschema.validate(json.load(open(data)), json.load(open(schema)))
    print(f"{data}: valid")
EOF
``` 

## 8.5. Horizon profile precomputation (`src/precompute.py`)

For every site in `sites.json`, the script computes the maximum terrain
elevation angle along 360 azimuth rays cast over the LRO-LOLA lunar digital
elevation model `LDEM_80S_20MPP_ADJ.TIF` (80°S region, 20 m/pixel). The DEM is
not part of this repository: download it from NASA and place it next to the
script before running.

### Method

1. Convert each site's selenographic latitude/longitude to the DEM's projected
   coordinates.
2. Load the raster once into memory for fast vectorized slicing.
3. For each azimuth 0°…359°, cast a ray from the site, sampling the terrain
   every `STEP_M` meters out to `MAX_DIST_M`.
4. For each sample, compute the apparent elevation angle, correcting for lunar
   spherical curvature:

   `θ = atan2(h_terrain − h_observer − d² / (2·R_Moon), d)`

5. Keep the maximum angle per azimuth and round it to 3 decimals.

### Configuration (top of `precompute.py`)

| Parameter             | Value        | Meaning                                   |
| --------------------- | ------------ | ----------------------------------------- |
| `R_MOON`              | 1737400.0 m  | Official lunar mean radius                |
| `MAX_DIST_M`          | 100000.0 m   | Maximum ray-casting search distance       |
| `STEP_M`              | 20.0 m       | Sampling step along each ray (matches DEM resolution) |
| `OBSERVER_HEIGHT_M`   | 2.0 m        | Antenna / sensor height above local ground |

### Requirements and usage

```bash
python -m pip install numpy rasterio pyproj
cd src
python precompute.py
```

The script must be run from `src/`, because the input/output paths are relative
(`../sites.json`, `../sites_with_horizon.json`). It prints one `[OK]` line per
computed site (with the min/max profile angles) and an `[OUT OF BOUNDS]` line
for sites outside the DEM, then writes `../sites_with_horizon.json`.


---

# 9. Data Sources and Scientific References

The project combines reference information and geospatial datasets from several scientific and institutional sources.

The main sources include:

### NASA — Lunar and Planetary Data

- [NASA Lunar Exploration](https://nssdc.gsfc.nasa.gov/planetary/planets/moonpage.html)
- [NASA Planetary Geology and Geophysics Data Archive — LOLA](https://pgda.gsfc.nasa.gov/products/90)
- [NASA Moon Trek](https://trek.nasa.gov/moon/)
- [NASA Scientific Visualization Studio — Lunar 3D Models](https://svs.gsfc.nasa.gov/14959)

### JPL — Astronomical and Planetary Data

- [JPL NAIF Generic Kernels](https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/)

These kernels provide planetary constants and reference information used in astronomical and planetary calculations.

### USGS — Lunar Geographical References

- [USGS Gazetteer of Planetary Nomenclature](https://planetarynames.wr.usgs.gov/)
- [USGS Lunar Grid Reference System Technical Memorandum](https://pubs.usgs.gov/publication/tm11E1)

### LGRS Implementation

- [LGRS Implementation — rbeyer/lgrs](https://github.com/rbeyer/lgrs)

The implementation provides a technical reference for working with lunar grid coordinates.

---

# 10. Future Data Development

The current datasets establish the foundation for a more comprehensive lunar geospatial information system.

Several extensions are planned.

## 10.1. Extended illumination datasets

Future versions could include:

- Time-dependent solar visibility.
- Illumination percentage.
- Continuous sunlight duration.
- Shadow duration.
- Seasonal illumination variability.
- Solar elevation and azimuth time series.

This would allow more detailed comparisons between landing locations and mission dates.

## 10.2. Landing suitability datasets

A future suitability layer could combine several environmental parameters:

- Terrain slope.
- Surface roughness.
- Crater density.
- Boulder distribution.
- Local horizon obstruction.
- Solar illumination.
- Earth visibility.
- Communication constraints.

The resulting information could be used to classify geographical regions according to operational suitability.

Such a classification would require explicitly defined criteria and appropriate scientific validation.

## 10.3. Citizen Science annotations

The geographical catalogue can also serve as a spatial foundation for community-generated observations.

Users could contribute annotations identifying:

- Potential landing hazards.
- Boulders.
- Craters.
- Terrain boundaries.
- Illumination regions.
- Shadow boundaries.
- Potentially suitable landing areas.

Each annotation could be associated with:

```json
{
  "id": "observation-001",
  "site_id": 1,
  "cell_id": "B WV G64 T63",
  "category": "surface_hazard",
  "confidence": 0.85,
  "source": "LROC",
  "timestamp": "2026-01-01T12:00:00Z"
}
```

This is an illustrative future data structure, not part of the current datasets.

## 10.4. Lunar Geospatial Knowledge Base

The long-term objective is to connect geographical locations, missions, imagery, terrain characteristics, and human observations into a unified spatio-temporal knowledge base.

The LGRS would provide the common spatial reference.

This would make it possible to organize observations consistently, compare neighboring regions, validate community contributions, and build reusable datasets for scientific research and machine learning.

Potential applications include:

- Lunar object detection.
- Surface hazard identification.
- Terrain classification.
- Shadow segmentation.
- Temporal change detection.
- AI-assisted landing site assessment.

Community-generated annotations would require quality control and expert validation before being used as scientific ground truth.

---

# 11. Technical Summary

The current repository datasets can be summarized as follows:

| Component | Current implementation |
|---|---|
| Mission catalogue | 49 records |
| Geographical catalogue | 60 records |
| Mission identifiers | Internal integer IDs |
| Site identifiers | Internal integer IDs |
| Mission relationships | `mission_ids` |
| Geographic positioning | Latitude / Longitude |
| Spatial reference | Lunar Grid Reference System |
| Terrain information | Optional horizon profiles |
| Mission validation | JSON Schema Draft 2020-12 |
| Data format | JSON |
| Application integration | React / TypeScript |

## Core design principles

The data architecture follows five principles:

1. **Separation of concerns:** Mission information and geographical information are stored independently.

2. **Referential integrity:** Mission-to-site relationships are maintained through unique identifiers.

3. **Spatial consistency:** LGRS provides a common reference for organizing geographical information.

4. **Extensibility:** Optional terrain and environmental datasets can be added without changing the fundamental mission-to-site relationship.

5. **Scientific traceability:** External data sources and calculation methodologies should be documented so that derived information can be reproduced and validated.

---

# 12. Conclusion

The repository provides the initial structured geographical and historical foundation of Lunar Landing Site Navigator.

By combining lunar mission information, geographical coordinates, LGRS references, and precomputed terrain horizon profiles, it establishes a common framework for exploring lunar locations and evaluating their environmental characteristics.

The main value of this architecture is not simply the storage of geographical information, but the ability to connect different types of lunar data through consistent spatial references.

This approach creates the foundations for integrating topographic analysis, astronomical calculations, mission planning, and citizen-science observations into a collaborative lunar geospatial platform.

**From geographical exploration to structured lunar knowledge: every location becomes a reference point for understanding and evaluating the lunar surface.**
