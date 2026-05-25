import streamlit as st

from src.components.comparison import render_city_comparison
from src.components.distribution import render_aqi_distribution
from src.components.heatmap import render_seasonal_heatmap
from src.components.metrics import render_metric_cards
from src.components.pollutant import render_pollutant_area
from src.components.yearly_trend import render_yearly_trend
from src.data_loader import load_data
from src.filters import render_sidebar
from src.styles import get_custom_css


def main():
    st.set_page_config(
        layout="wide",
        page_title="India AQI Tracker",
        page_icon="🌫️",
        initial_sidebar_state="expanded",
    )

    st.markdown(f"<style>{get_custom_css()}</style>", unsafe_allow_html=True)

    df = load_data()
    if df is None:
        st.stop()

    filters = render_sidebar(df)
    selected_city = filters["selected_city"]
    year_range = filters["year_range"]
    selected_comparison_cities = filters["selected_comparison_cities"]
    selected_pollutant = filters["selected_pollutant"]

    st.markdown("<div class='title-glow'>India AQI Tracker</div>", unsafe_allow_html=True)

    filtered_df = df[
        (df["City"] == selected_city)
        & (df["Year"] >= year_range[0])
        & (df["Year"] <= year_range[1])
    ]

    with st.spinner("Loading dashboard..."):
        render_metric_cards(filtered_df)

        st.markdown("<br>", unsafe_allow_html=True)
        r1_col1, r1_col2 = st.columns(2)

        with r1_col1:
            render_seasonal_heatmap(filtered_df, selected_city)
        with r1_col2:
            render_yearly_trend(filtered_df, selected_city)

        st.markdown("<br>", unsafe_allow_html=True)
        r2_col1, r2_col2 = st.columns(2)

        with r2_col1:
            render_city_comparison(df, selected_comparison_cities, year_range, selected_city)
        with r2_col2:
            render_pollutant_area(filtered_df, selected_pollutant, selected_city)

        st.markdown("<br>", unsafe_allow_html=True)
        r3_col1, _ = st.columns(2)

        with r3_col1:
            render_aqi_distribution(filtered_df, selected_city)

    st.markdown("---")
    st.markdown(
        """
        <div style='background: rgba(255,255,255,0.03); border-radius: 12px; padding: 20px;
                    text-align: center; color: #a0aec0; font-family: Outfit;
                    backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.05);'>
            Built by <strong>Garvit Pandia</strong> · LPU ·
            <a href='https://github.com/garvit-pandia/india-aqi-tracker' target='_blank'
               style='color: #4facfe; text-decoration: none;'>GitHub Repo</a> ·
            <a href='https://huggingface.co/spaces/garvitpandia28/india-aqi-tracker' target='_blank'
               style='color: #00f2fe; text-decoration: none;'>Hugging Face Space</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
