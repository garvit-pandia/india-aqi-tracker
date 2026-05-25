import logging
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

from src.constants import (
    AQI_BUCKET_THRESHOLDS,
    CSV_PATH,
    REQUIRED_COLUMNS,
)

logger = logging.getLogger(__name__)


def _vectorized_fill_bucket(df: pd.DataFrame) -> pd.DataFrame:
    conditions = []
    choices = []
    for low, high, label in AQI_BUCKET_THRESHOLDS:
        conditions.append((df["AQI"] >= low) & (df["AQI"] <= high))
        choices.append(label)

    needs_fill = df["AQI_Bucket"].isna() | (df["AQI_Bucket"] == "N/A")
    has_aqi = df["AQI"].notna()

    mask = needs_fill & has_aqi
    if mask.any():
        df.loc[mask, "AQI_Bucket"] = np.select(conditions, choices, default="N/A")[mask]

    df.loc[df["AQI"].isna() & df["AQI_Bucket"].isna(), "AQI_Bucket"] = "N/A"
    return df


@st.cache_data
def load_data(csv_path: str | Path | None = None) -> pd.DataFrame | None:
    path = Path(csv_path) if csv_path else Path(CSV_PATH)

    if not path.exists():
        st.error(f"Data file not found: {path.resolve()}")
        st.stop()
        return None

    try:
        df = pd.read_csv(path)
    except Exception as e:
        st.error(f"Failed to read data file: {e}")
        st.stop()
        return None

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        st.error(f"Missing required columns: {', '.join(missing)}")
        st.stop()
        return None

    logger.info("Loaded %d rows from %s", len(df), path.name)

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Month_Name"] = df["Date"].dt.strftime("%b")
    df["YearMonth"] = df["Date"].dt.to_period("M").astype(str)

    df = _vectorized_fill_bucket(df)

    return df
