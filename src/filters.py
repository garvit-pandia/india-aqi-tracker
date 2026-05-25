import streamlit as st

from src.constants import (
    DEFAULT_CITY,
    DEFAULT_COMPARISON_CITIES,
    POLLUTANTS,
    YEAR_RANGE,
)


def render_sidebar(df, key_prefix: str = "") -> dict:
    st.sidebar.markdown(
        "<h3 style='text-align: center; color: #4facfe;'>🌫️ Settings</h3>",
        unsafe_allow_html=True,
    )
    st.sidebar.caption(
        "<div style='text-align: center;'>Built by Garvit Pandia | LPU Final Year | Data Science</div>",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("---")

    cities = sorted(df["City"].dropna().unique())

    if not cities:
        st.error("No cities found in dataset.")
        st.stop()

    default_city = DEFAULT_CITY if DEFAULT_CITY in cities else cities[0]
    default_idx = cities.index(default_city)

    selected_city = st.sidebar.selectbox(
        "Select City",
        cities,
        index=default_idx,
        key=f"{key_prefix}city_select",
    )

    year_range = st.sidebar.slider(
        "Select Year Range",
        int(df["Year"].min()),
        int(df["Year"].max()),
        YEAR_RANGE,
        key=f"{key_prefix}year_slider",
    )

    default_compare = [selected_city] + [
        c for c in DEFAULT_COMPARISON_CITIES if c in cities
    ]
    selected_comparison = st.sidebar.multiselect(
        "Select Cities for Comparison",
        cities,
        default=default_compare,
        key=f"{key_prefix}compare_multiselect",
    )

    selected_pollutant = st.sidebar.selectbox(
        "Select Pollutant",
        POLLUTANTS,
        key=f"{key_prefix}pollutant_select",
    )

    st.sidebar.markdown("---")

    return {
        "selected_city": selected_city,
        "year_range": year_range,
        "selected_comparison_cities": selected_comparison,
        "selected_pollutant": selected_pollutant,
    }
