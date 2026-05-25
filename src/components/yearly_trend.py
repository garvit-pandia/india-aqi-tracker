import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.constants import LINE_COLOR, MARKER_COLOR


def render_yearly_trend(filtered_df: pd.DataFrame, selected_city: str) -> None:
    yearly_data = (
        filtered_df.dropna(subset=["AQI"])
        .groupby("Year")["AQI"]
        .mean()
        .reset_index()
    )

    if yearly_data.empty:
        st.warning(f"No AQI data for {selected_city} in selected range.")
        return

    yearly_data["Year_str"] = yearly_data["Year"].astype(str)

    fig_line = go.Figure()
    fig_line.add_trace(
        go.Scatter(
            x=yearly_data["Year_str"].tolist(),
            y=yearly_data["AQI"].tolist(),
            mode="lines+markers",
            line={"color": LINE_COLOR, "width": 4},
            marker={"size": 10, "color": MARKER_COLOR},
            name="AQI",
        )
    )
    fig_line.update_layout(
        title=f"Yearly Average AQI - {selected_city}",
        margin={"t": 50, "b": 30, "l": 10, "r": 10},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#e2e8f0", "family": "Outfit"},
        xaxis={"showgrid": False, "type": "category", "title": "Year"},
        yaxis={"gridcolor": "rgba(255,255,255,0.1)", "title": "AQI"},
        title_font={"size": 20},
    )
    st.plotly_chart(fig_line, use_container_width=True)
