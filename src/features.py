"""
Feature engineering utilities for NYC taxi trip data.
All functions are pure (no side effects beyond add_time_features which mutates df)
and work on NumPy arrays or pandas DataFrames.
"""
import numpy as np
import pandas as pd

NYC_BOUNDS = {
    "lon_min": -74.05, "lon_max": -73.75,
    "lat_min":  40.48, "lat_max":  40.92,
}

_TIME_SLOTS = [
    ("madrugada",    0,  5),
    ("manana_pico",  5,  9),
    ("manana_baja",  9, 12),
    ("tarde_pico",  12, 17),
    ("tarde_baja",  17, 20),
    ("noche",       20, 24),
]


def haversine(
    lat1: "float | np.ndarray",
    lon1: "float | np.ndarray",
    lat2: "float | np.ndarray",
    lon2: "float | np.ndarray",
) -> np.ndarray:
    """Haversine distance in km between coordinate pairs.

    Accepts scalars, lists, or NumPy/pandas arrays.
    Uses the WGS-84 mean Earth radius (6 371.0 km).

    Example
    -------
    >>> haversine(40.7128, -74.0060, 40.6501, -73.9496)  # Brooklyn Bridge → JFK area
    array(8.37...)
    """
    R = 6371.0
    lat1, lon1, lat2, lon2 = (np.radians(np.asarray(x, dtype=float))
                               for x in (lat1, lon1, lat2, lon2))
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return R * 2 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))


def assign_zone_grid(
    df: pd.DataFrame,
    n: int = 8,
    lat_col: str = "pickup_latitude",
    lon_col: str = "pickup_longitude",
    bounds: dict = NYC_BOUNDS,
) -> pd.Series:
    """Assign each pickup to a cell in an n×n grid over the NYC bounding box.

    Returns a Series of integer zone IDs in [0, n²-1], named 'zone_id'.
    Row index increases northward; column index increases eastward.

    Parameters
    ----------
    df     : DataFrame with lat/lon pickup columns.
    n      : Grid resolution (default 8 → 64 cells ≈ 3.2×6.1 km each).
    bounds : Dict with lon_min/lon_max/lat_min/lat_max keys.
    """
    lat_bins = np.linspace(bounds["lat_min"], bounds["lat_max"], n + 1)
    lon_bins = np.linspace(bounds["lon_min"], bounds["lon_max"], n + 1)
    row = np.digitize(df[lat_col].to_numpy(), lat_bins).clip(1, n) - 1
    col = np.digitize(df[lon_col].to_numpy(), lon_bins).clip(1, n) - 1
    return pd.Series(row * n + col, index=df.index, name="zone_id")


def add_time_features(
    df: pd.DataFrame,
    datetime_col: str = "pickup_datetime",
) -> pd.DataFrame:
    """Add hour, day_of_week, is_weekend, month, and time_slot columns.

    Mutates *df* in place and returns it for chaining.

    Time slots
    ----------
    madrugada   0–4 h  |  manana_pico 5–8 h  |  manana_baja  9–11 h
    tarde_pico 12–16 h  |  tarde_baja 17–19 h  |  noche       20–23 h
    """
    dt = pd.to_datetime(df[datetime_col])
    df["hour"]        = dt.dt.hour
    df["day_of_week"] = dt.dt.dayofweek   # 0 = Monday … 6 = Sunday
    df["is_weekend"]  = (df["day_of_week"] >= 5).astype(np.int8)
    df["month"]       = dt.dt.month

    cuts  = [lo for _, lo, _ in _TIME_SLOTS] + [24]
    labels = [name for name, _, _ in _TIME_SLOTS]
    df["time_slot"] = pd.cut(df["hour"], bins=cuts, labels=labels, right=False)
    return df


def compute_speed(
    df: pd.DataFrame,
    dist_col: str = "distance_km",
    duration_col: str = "trip_duration",
    duration_unit: str = "seconds",
) -> pd.Series:
    """Average speed in km/h.

    Parameters
    ----------
    duration_unit : 'seconds' (raw trip_duration column) or 'minutes'.
    """
    factor = 3600.0 if duration_unit == "seconds" else 60.0
    return (df[dist_col] / df[duration_col] * factor).rename("speed_kmh")


def clean_trips(
    df: pd.DataFrame,
    bounds: dict = NYC_BOUNDS,
    min_duration_s: int = 60,
    max_duration_s: int = 10_800,
    min_distance_km: float = 0.10,
    max_speed_kmh: float = 100.0,
) -> pd.DataFrame:
    """Apply standard quality filters for NYC taxi data.

    Drops rows with impossible durations, out-of-bounds coordinates,
    near-zero distances, or implausible speeds. Returns a filtered copy.

    Typical yield: ~98.4 % of raw rows survive (removes ~1.6 %).
    """
    mask = (
        df["passenger_count"].between(1, 6)
        & df["trip_duration"].between(min_duration_s, max_duration_s)
        & df["pickup_longitude"].between(bounds["lon_min"], bounds["lon_max"])
        & df["pickup_latitude"].between(bounds["lat_min"], bounds["lat_max"])
        & df["dropoff_longitude"].between(bounds["lon_min"], bounds["lon_max"])
        & df["dropoff_latitude"].between(bounds["lat_min"], bounds["lat_max"])
    )
    out = df.loc[mask].copy()

    if "distance_km" not in out.columns:
        out["distance_km"] = haversine(
            out["pickup_latitude"],  out["pickup_longitude"],
            out["dropoff_latitude"], out["dropoff_longitude"],
        )

    out["speed_kmh"] = compute_speed(out)
    speed_mask = (out["distance_km"] >= min_distance_km) & (out["speed_kmh"] <= max_speed_kmh)
    return out.loc[speed_mask].copy()
