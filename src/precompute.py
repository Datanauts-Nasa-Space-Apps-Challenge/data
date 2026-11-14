import json
import numpy as np
import rasterio
from pyproj import CRS, Transformer

# --- CONFIGURATION PARAMETERS ---
R_MOON = 1737400.0        # Official lunar mean radius in meters (1,737.4 km)
MAX_DIST_M = 100000.0     # Maximum ray-casting search distance for obstacles (100 km)
STEP_M = 20.0             # Sampling step along each ray (20 m, matching DEM resolution)
OBSERVER_HEIGHT_M = 2.0   # Antenna / sensor height above local ground (in meters)

DEM_PATH = "LDEM_80S_20MPP_ADJ.TIF"       # LRO-LOLA GeoTIFF file downloaded from NASA
SITES_INPUT = "../sites.json"          # Input sites JSON file
SITES_OUTPUT = "../sites_with_horizon.json"


def compute_360_horizon(dataset, dem_array, x0, y0, scale_factor, nodata):
    """
    Computes the maximum terrain elevation angle (in degrees) for each azimuth
    from 0° to 359°, accounting for lunar spherical curvature.
    """
    rows, cols = dem_array.shape

    # Retrieve the elevation of the site itself
    r0, c0 = dataset.index(x0, y0)
    if not (0 <= r0 < rows and 0 <= c0 < cols):
        return None  # Site falls outside the geographic bounds of this GeoTIFF

    h0 = float(dem_array[r0, c0]) * scale_factor + OBSERVER_HEIGHT_M

    # Distance vector from the site (start at STEP_M to avoid division by zero)
    dists = np.arange(STEP_M, MAX_DIST_M + STEP_M, STEP_M)

    # Precompute the lunar curvature drop for each distance: d^2 / (2 * R)
    curvature_drop = (dists ** 2) / (2.0 * R_MOON)

    horizon_profile = []

    for az_deg in range(360):
        # Azimuth in radians: 0° = North (+Y in South Polar projection), 90° = East (+X)
        az_rad = np.radians(az_deg)

        # Projected (X, Y) coordinates for all sample points along this ray
        xs = x0 + dists * np.sin(az_rad)
        ys = y0 + dists * np.cos(az_rad)

        # Convert projected (X, Y) coordinates to raster row and column indices
        rs, cs = rasterio.transform.rowcol(dataset.transform, xs, ys)
        rs = np.array(rs)
        cs = np.array(cs)

        # Keep only sample points that fall within the raster boundaries
        valid = (rs >= 0) & (rs < rows) & (cs >= 0) & (cs < cols)
        if not np.any(valid):
            horizon_profile.append(0.0)
            continue

        rs_v = rs[valid]
        cs_v = cs[valid]
        d_v = dists[valid]
        curv_v = curvature_drop[valid]

        # Extract terrain elevations along the ray and apply raster scale factor
        elevs = dem_array[rs_v, cs_v].astype(np.float64) * scale_factor

        # Filter out nodata pixels if defined in the GeoTIFF metadata
        if nodata is not None:
            not_na = elevs != (nodata * scale_factor)
            elevs = elevs[not_na]
            d_v = d_v[not_na]
            curv_v = curv_v[not_na]

        if len(elevs) == 0:
            horizon_profile.append(0.0)
            continue

        # Compute apparent elevation angles including lunar curvature drop:
        # tan(theta) = (h_terrain - h_observer - curvature_drop) / distance
        angles_rad = np.arctan2(elevs - h0 - curv_v, d_v)
        max_angle_deg = float(np.degrees(np.max(angles_rad)))

        horizon_profile.append(round(max_angle_deg, 3))

    return horizon_profile


def main():
    with open(SITES_INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Open the GeoTIFF and load the raster into RAM for fast vectorized slicing
    with rasterio.open(DEM_PATH) as dataset:
        dem_array = dataset.read(1)
        scale_factor = dataset.scales[0] if dataset.scales else 1.0
        nodata = dataset.nodata

        # Define coordinate transformer from lunar geographic (Lat/Lon) to GeoTIFF CRS
        lunar_geog = CRS.from_proj4(f"+proj=longlat +R={R_MOON} +no_defs")
        transformer = Transformer.from_crs(lunar_geog, dataset.crs, always_xy=True)

        computed_count = 0
        for site in data["sites"]:
            # Note: always_xy=True expects (longitude, latitude)
            x0, y0 = transformer.transform(site["long"], site["lat"])

            profile = compute_360_horizon(
                dataset, dem_array, x0, y0, scale_factor, nodata
            )

            if profile is not None:
                site["horizon_profile"] = profile
                computed_count += 1
                print(
                    f"[OK] {site['name']} (ID {site['id']}): "
                    f"min={min(profile)}°, max={max(profile)}°"
                )
            else:
                print(
                    f"[OUT OF BOUNDS] {site['name']} (lat={site['lat']}) "
                    f"is outside the coverage of this DEM."
                )

    with open(SITES_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(
        f"\nProcess complete: computed {computed_count} horizon profiles "
        f"into '{SITES_OUTPUT}'."
    )


if __name__ == "__main__":
    main()
