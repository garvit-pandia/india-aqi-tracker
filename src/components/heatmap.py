import pandas as pd
import plotly.express as px
import streamlit as st

from src.constants import HEATMAP_COLORSCALE, MONTH_NAMES


def render_seasonal_heatmap(filtered_df: pd.DataFrame, selected_city: str) -> None:
    heatmap_data = filtered_df.dropna(subset=["AQI"])

    if heatmap_data.empty:
        st.warning(f"No AQI data for {selected_city} to generate Heatmap.")
        return

    pivot = heatmap_data.pivot_table(
        index="Year", columns="Month_Name", values="AQI", aggfunc="mean"
    )
    pivot = pivot.reindex(columns=[m for m in MONTH_NAMES if m in pivot.columns])

    fig_heatmap = px.imshow(
        pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.astype(str).tolist(),
        labels=dict(x="Month", y="Year", color="Avg AQI"),
        color_continuous_scale=HEATMAP_COLORSCALE,
        aspect="auto",
    )
    fig_heatmap.update_layout(
        title=f"Seasonal AQI Heatmap - {selected_city}",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#e2e8f0", "family": "Outfit"},
        title_font={"size": 20},
        yaxis={"type": "category"},
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
    st.markdown(
        "<div style='text-align:center; color:#a0aec0; font-size:0.9rem;'>"
        "Nov-Dec spike caused by crop stubble burning and cold air trapping pollutants near ground level"
        "</div>",
        unsafe_allow_html=True,
    )
