"""A szöuli kerékpárkölcsönzés órai adatainak beolvasása és típusos előkészítése."""

from pathlib import Path

import pandas as pd

CSV_PATH = Path(__file__).resolve().parent / "data" / "SeoulBikeData.csv"

CSV_COLUMNS = {
    "Date": "date",
    "Rented Bike Count": "rentals",
    "Hour": "hour",
    "Temperature(°C)": "temperature_c",
    "Humidity(%)": "humidity_pct",
    "Wind speed (m/s)": "wind_speed_m_s",
    "Visibility (10m)": "visibility_10m",
    "Dew point temperature(°C)": "dew_point_c",
    "Solar Radiation (MJ/m2)": "solar_radiation_mj_m2",
    "Rainfall(mm)": "rainfall_mm",
    "Snowfall (cm)": "snowfall_cm",
    "Seasons": "season",
    "Holiday": "is_holiday",
    "Functioning Day": "is_operating",
}

WEEKDAYS = ["Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek", "Szombat", "Vasárnap"]
SEASONS = ["Winter", "Spring", "Summer", "Autumn"]
NUMERIC_COLUMNS = [
    "rentals",
    "hour",
    "temperature_c",
    "humidity_pct",
    "wind_speed_m_s",
    "visibility_10m",
    "dew_point_c",
    "solar_radiation_mj_m2",
    "rainfall_mm",
    "snowfall_cm",
]


def load_bike_data(path: str | Path = CSV_PATH) -> pd.DataFrame:
    """Minden CSV-sorból egy órai megfigyelést készít időrendben."""
    raw = pd.read_csv(path, encoding="cp1252")
    missing_columns = CSV_COLUMNS.keys() - raw.columns
    if len(missing_columns):
        raise ValueError("Hiányzó CSV-oszlopok: " + ", ".join(sorted(missing_columns)))

    data = raw[list(CSV_COLUMNS)].rename(columns=CSV_COLUMNS)
    missing_values = data.columns[data.isna().any()]
    if len(missing_values):
        raise ValueError("Hiányzó adatok ezekben az oszlopokban: " + ", ".join(missing_values))

    data[NUMERIC_COLUMNS] = data[NUMERIC_COLUMNS].apply(pd.to_numeric, errors="raise")
    if not (data["hour"].between(0, 23) & data["hour"].mod(1).eq(0)).all():
        raise ValueError("Az óra 0 és 23 közötti egész szám lehet.")
    if not (data["rentals"].ge(0) & data["rentals"].mod(1).eq(0)).all():
        raise ValueError("A kölcsönzések száma nemnegatív egész szám lehet.")
    data[["hour", "rentals"]] = data[["hour", "rentals"]].astype("int64")

    data["date"] = pd.to_datetime(data["date"], format="%d/%m/%Y", errors="raise")
    data.insert(0, "timestamp", data["date"] + pd.to_timedelta(data["hour"], unit="h"))
    if not data["timestamp"].is_unique:
        raise ValueError("Az adathalmazban ismétlődő órás időbélyegek vannak.")

    for column, values in {
        "is_holiday": {"Holiday": True, "No Holiday": False},
        "is_operating": {"Yes": True, "No": False},
    }.items():
        if not data[column].isin(values).all():
            raise ValueError(f"Ismeretlen kategória a(z) {column} oszlopban.")
        data[column] = data[column].map(values).astype(bool)

    if not data["season"].isin(SEASONS).all():
        raise ValueError("Ismeretlen évszak az adathalmazban.")
    data["season"] = pd.Categorical(data["season"], categories=SEASONS, ordered=True)

    weekday_number = data["timestamp"].dt.dayofweek
    data["weekday"] = pd.Categorical.from_codes(weekday_number, WEEKDAYS, ordered=True)
    data["is_weekend"] = weekday_number.ge(5)
    data["month"] = data["date"].dt.to_period("M").dt.to_timestamp()
    return data.sort_values("timestamp", ignore_index=True)
