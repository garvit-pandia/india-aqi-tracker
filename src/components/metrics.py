import pandas as pd
import streamlit as st


def render_metric_cards(filtered_df: pd.DataFrame) -> None:
    col1, col2, col3, col4 = st.columns(4)

    avg_aqi = filtered_df["AQI"].mean()
    worst_aqi = filtered_df["AQI"].max()
    best_aqi = filtered_df["AQI"].min()

    monthly_avg = (
        filtered_df.dropna(subset=["AQI"])
        .groupby(["Year", "Month", "Month_Name"])["AQI"]
        .mean()
        .reset_index()
    )

    if not monthly_avg.empty:
        worst_idx = monthly_avg["AQI"].idxmax()
        worst_row = monthly_avg.loc[worst_idx]
        worst_month_display = f"{worst_row['Month_Name']} {int(worst_row['Year'])}"
    else:
        worst_month_display = "N/A"

    col1.metric("Avg AQI", f"{avg_aqi:.1f}" if pd.notna(avg_aqi) else "N/A")
    col2.metric("Worst AQI", f"{worst_aqi:.1f}" if pd.notna(worst_aqi) else "N/A")
    col3.metric("Best AQI", f"{best_aqi:.1f}" if pd.notna(best_aqi) else "N/A")
    col4.metric("Worst Month", worst_month_display)
