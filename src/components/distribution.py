import pandas as pd
import plotly.express as px
import streamlit as st

from src.constants import AQI_BUCKET_COLORS


def render_aqi_distribution(filtered_df: pd.DataFrame, selected_city: str) -> None:
    dist = (
        filtered_df["AQI_Bucket"]
        .value_counts()
        .rename_axis("Category")
        .reset_index(name="Days")
    )

    if dist.empty:
        return

    fig_donut = px.pie(
        values=dist["Days"].tolist(),
        names=dist["Category"].tolist(),
        hole=0.5,
        title=f"AQI Days Distribution - {selected_city}",
        color=dist["Category"].tolist(),
        color_discrete_map=AQI_BUCKET_COLORS,
    )
    fig_donut.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#e2e8f0", "family": "Outfit"},
        title_font={"size": 20},
        annotations=[
            {
                "text": "AQI",
                "x": 0.5,
                "y": 0.5,
                "font_size": 20,
                "showarrow": False,
                "font_color": "#e2e8f0",
            }
        ],
    )
    fig_donut.update_traces(
        hoverinfo="label+percent",
        textinfo="value",
        textfont_size=14,
        marker={"line": {"color": "#16213e", "width": 2}},
    )
    st.plotly_chart(fig_donut, use_container_width=True)
