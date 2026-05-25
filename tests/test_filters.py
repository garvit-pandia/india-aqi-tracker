from src.filters import render_sidebar


class TestRenderSidebar:
    def test_returns_expected_keys(self, loaded_df):
        result = render_sidebar(loaded_df, key_prefix="test_")
        assert "selected_city" in result
        assert "year_range" in result
        assert "selected_comparison_cities" in result
        assert "selected_pollutant" in result
        assert result["selected_pollutant"] in [
            "PM2.5",
            "PM10",
            "NO2",
            "CO",
            "SO2",
            "O3",
        ]
