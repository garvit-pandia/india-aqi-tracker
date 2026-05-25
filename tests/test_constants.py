from src.constants import (
    AQI_BUCKET_COLORS,
    AQI_BUCKET_THRESHOLDS,
    CSV_PATH,
    DEFAULT_CITY,
    HEATMAP_COLORSCALE,
    MONTH_NAMES,
    POLLUTANTS,
)


class TestConstants:
    def test_csv_path_is_string(self):
        assert isinstance(CSV_PATH, str)

    def test_aqi_buckets_cover_full_range(self):
        prev_high = -1
        for low, high, _label in AQI_BUCKET_THRESHOLDS:
            assert low == prev_high + 1 or prev_high == -1
            prev_high = high

    def test_all_buckets_have_colors(self):
        for _, _, label in AQI_BUCKET_THRESHOLDS:
            assert label in AQI_BUCKET_COLORS
        assert "N/A" in AQI_BUCKET_COLORS

    def test_month_names_count(self):
        assert len(MONTH_NAMES) == 12

    def test_pollutants_non_empty(self):
        assert len(POLLUTANTS) > 0

    def test_heatmap_colorscale_is_valid(self):
        assert len(HEATMAP_COLORSCALE) == 3
        for item in HEATMAP_COLORSCALE:
            assert len(item) == 2
            assert 0.0 <= item[0] <= 1.0

    def test_default_city_is_string(self):
        assert isinstance(DEFAULT_CITY, str)
