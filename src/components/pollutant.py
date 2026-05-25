import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.constants import AREA_FILL_COLOR, AREA_LINE_COLOR


def render_pollutant_area(
    filtered_df: pd.DataFrame,
    selected_pollutant: str,
    selected_city: str,
) -> None:
    monthly_pollutant = (
        filtered_df.dropna(subset=[selected_pollutant])
        .groupby("YearMonth")[selected_pollutant]
        .mean()
        .reset_index()
    )

    if monthly_pollutant.empty:
        st.warning(f"No {selected_pollutant} records for {selected_city}.")
        return

    fig_area = go.Figure()
    fig_area.add_trace(
        go.Scatter(
            x=monthly_pollutant["YearMonth"].astype(str).tolist(),
            y=monthly_pollutant[selected_pollutant].tolist(),
            fill="tozeroy",
            line={"color": AREA_LINE_COLOR},
            fillcolor=AREA_FILL_COLOR,
            name=selected_pollutant,
        )
    )
    fig_area.update_layout(
        title=f"Monthly Average {selected_pollutant} - {selected_city}",
        margin={"t": 50, "b": 30, "l": 10, "r": 10},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#e2e8f0", "family": "Outfit"},
        xaxis={"showgrid": False},
        yaxis={"gridcolor": "rgba(255,255,255,0.1)"},
        title_font={"size": 20},
    )
    st.plotly_chart(fig_area, use_container_width=True)
