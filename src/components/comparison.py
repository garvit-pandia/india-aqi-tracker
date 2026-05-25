import pandas as pd
import plotly.express as px
import streamlit as st

from src.constants import DEFAULT_BAR_COLOR, HIGHLIGHT_COLOR


def render_city_comparison(
    df: pd.DataFrame,
    selected_comparison_cities: list[str],
    year_range: tuple[int, int],
    selected_city: str,
) -> None:
    comparison_df = df[
        (df["City"].isin(selected_comparison_cities))
        & (df["Year"] >= year_range[0])
        & (df["Year"] <= year_range[1])
    ]

    if comparison_df.empty:
        st.warning("Comparison data unavailable.")
        return

    city_avg = (
        comparison_df.dropna(subset=["AQI"])
        .groupby("City")["AQI"]
        .mean()
        .reset_index()
        .sort_values("AQI")
    )
    city_avg["Color"] = city_avg["City"].apply(
        lambda c: HIGHLIGHT_COLOR if c == selected_city else DEFAULT_BAR_COLOR
    )

    fig_bar = px.bar(
        x=city_avg["AQI"].tolist(),
        y=city_avg["City"].tolist(),
        orientation="h",
        title="City Comparison (Avg AQI)",
    )
    fig_bar.update_traces(marker_color=city_avg["Color"].tolist())
    fig_bar.update_layout(
        margin={"t": 50, "b": 30, "l": 10, "r": 10},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#e2e8f0", "family": "Outfit"},
        xaxis={"gridcolor": "rgba(255,255,255,0.1)", "title": "Average AQI"},
        yaxis={"title": ""},
        title_font={"size": 20},
    )
    st.plotly_chart(fig_bar, use_container_width=True)
