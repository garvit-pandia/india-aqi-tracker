import pandas as pd
import pytest


@pytest.fixture
def sample_df() -> pd.DataFrame:
    data = {
        "City": ["Delhi", "Delhi", "Mumbai", "Mumbai", "Udaipur", "Udaipur"],
        "Date": [
            "2015-01-01",
            "2015-02-01",
            "2015-01-01",
            "2015-02-01",
            "2015-01-01",
            "2015-02-01",
        ],
        "PM2.5": [150.0, 200.0, 80.0, 90.0, 45.0, 55.0],
        "PM10": [250.0, 300.0, 120.0, 130.0, 70.0, 80.0],
        "NO2": [60.0, 70.0, 30.0, 35.0, 20.0, 25.0],
        "CO": [1.5, 2.0, 0.8, 0.9, 0.4, 0.5],
        "SO2": [15.0, 18.0, 8.0, 9.0, 5.0, 6.0],
        "O3": [40.0, 45.0, 25.0, 30.0, 35.0, 40.0],
        "AQI": [320, 380, 150, 165, 75, 90],
        "AQI_Bucket": [None, None, "Moderate", "Moderate", "Satisfactory", "Satisfactory"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def loaded_df(sample_df: pd.DataFrame) -> pd.DataFrame:
    df = sample_df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Month_Name"] = df["Date"].dt.strftime("%b")
    df["YearMonth"] = df["Date"].dt.to_period("M").astype(str)

    from src.data_loader import _vectorized_fill_bucket

    return _vectorized_fill_bucket(df)


@pytest.fixture
def small_df() -> pd.DataFrame:
    data = {
        "City": ["Udaipur"],
        "Date": ["2015-03-01"],
        "AQI": [75],
        "AQI_Bucket": ["Satisfactory"],
    }
    return pd.DataFrame(data)
