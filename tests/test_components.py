import pandas as pd

from src.components.comparison import render_city_comparison
from src.components.distribution import render_aqi_distribution
from src.components.heatmap import render_seasonal_heatmap
from src.components.metrics import render_metric_cards
from src.components.pollutant import render_pollutant_area
from src.components.yearly_trend import render_yearly_trend


class TestMetricCards:
    def test_renders_with_data(self, loaded_df):
        render_metric_cards(loaded_df)

    def test_renders_empty_dataframe(self):
        df = pd.DataFrame(columns=["City", "Date", "AQI", "Year", "Month", "Month_Name", "AQI_Bucket"])
        render_metric_cards(df)


class TestSeasonalHeatmap:
    def test_renders_with_data(self, loaded_df):
        filtered = loaded_df[loaded_df["City"] == "Delhi"]
        render_seasonal_heatmap(filtered, "Delhi")

    def test_renders_empty_data(self, loaded_df):
        filtered = loaded_df[loaded_df["AQI"].isna()]
        render_seasonal_heatmap(filtered, "N/A City")


class TestYearlyTrend:
    def test_renders_with_data(self, loaded_df):
        filtered = loaded_df[loaded_df["City"] == "Delhi"]
        render_yearly_trend(filtered, "Delhi")

    def test_renders_empty_data(self, loaded_df):
        filtered = loaded_df[loaded_df["AQI"].isna()]
        render_yearly_trend(filtered, "N/A City")


class TestCityComparison:
    def test_renders_with_data(self, loaded_df):
        render_city_comparison(loaded_df, ["Delhi", "Mumbai"], (2015, 2020), "Delhi")

    def test_renders_no_matching_cities(self, loaded_df):
        render_city_comparison(loaded_df, ["NonExistent"], (2015, 2020), "Delhi")


class TestPollutantArea:
    def test_renders_with_data(self, loaded_df):
        filtered = loaded_df[loaded_df["City"] == "Delhi"]
        render_pollutant_area(filtered, "PM2.5", "Delhi")

    def test_renders_empty_data(self, loaded_df):
        filtered = loaded_df[loaded_df["PM2.5"].isna()]
        render_pollutant_area(filtered, "PM2.5", "No Data")


class TestAQIDistribution:
    def test_renders_with_data(self, loaded_df):
        filtered = loaded_df[loaded_df["City"] == "Delhi"]
        render_aqi_distribution(filtered, "Delhi")

    def test_renders_empty_data(self, loaded_df):
        df = pd.DataFrame(columns=["AQI_Bucket"])
        render_aqi_distribution(df, "Empty")
