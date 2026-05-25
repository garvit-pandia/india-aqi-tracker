import numpy as np
import pandas as pd

from src.data_loader import _vectorized_fill_bucket, load_data


class TestVectorizedFillBucket:
    def test_fills_missing_buckets(self):
        df = pd.DataFrame(
            {
                "AQI": [45, 75, 150, 250, 350, 450],
                "AQI_Bucket": [None, None, None, None, None, None],
            }
        )
        result = _vectorized_fill_bucket(df)
        assert result["AQI_Bucket"].tolist() == [
            "Good",
            "Satisfactory",
            "Moderate",
            "Poor",
            "Very Poor",
            "Severe",
        ]

    def test_leaves_existing_buckets(self):
        df = pd.DataFrame(
            {
                "AQI": [45, 320],
                "AQI_Bucket": ["Good", "Severe"],
            }
        )
        result = _vectorized_fill_bucket(df)
        assert result["AQI_Bucket"].tolist() == ["Good", "Severe"]

    def test_fills_na_string_buckets(self):
        df = pd.DataFrame(
            {
                "AQI": [75, 150],
                "AQI_Bucket": ["N/A", "N/A"],
            }
        )
        result = _vectorized_fill_bucket(df)
        assert result["AQI_Bucket"].tolist() == ["Satisfactory", "Moderate"]

    def test_handles_nan_aqi(self):
        df = pd.DataFrame(
            {
                "AQI": [np.nan, 75],
                "AQI_Bucket": [None, None],
            }
        )
        result = _vectorized_fill_bucket(df)
        assert result.loc[0, "AQI_Bucket"] == "N/A"
        assert result.loc[1, "AQI_Bucket"] == "Satisfactory"

    def test_partial_missing(self):
        df = pd.DataFrame(
            {
                "AQI": [45, 320, 150],
                "AQI_Bucket": [None, "Severe", None],
            }
        )
        result = _vectorized_fill_bucket(df)
        assert result["AQI_Bucket"].tolist() == ["Good", "Severe", "Moderate"]


class TestLoadData:
    def test_loads_valid_csv(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        csv_path.write_text("City,Date,AQI,AQI_Bucket\nDelhi,2015-01-01,320,Severe\n")
        df = load_data(str(csv_path))
        assert df is not None
        assert len(df) == 1
        assert df.loc[0, "City"] == "Delhi"

    def test_missing_file(self, tmp_path):
        df = load_data(str(tmp_path / "missing.csv"))
        assert df is None

    def test_missing_columns(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        csv_path.write_text("Name,When,Reading\nA,2020,50\n")
        df = load_data(str(csv_path))
        assert df is None

    def test_adds_date_features(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        csv_path.write_text(
            "City,Date,AQI,AQI_Bucket\nDelhi,2015-06-15,200,Satisfactory\n"
        )
        df = load_data(str(csv_path))
        assert df is not None
        assert df.loc[0, "Year"] == 2015
        assert df.loc[0, "Month"] == 6
        assert df.loc[0, "Month_Name"] == "Jun"
