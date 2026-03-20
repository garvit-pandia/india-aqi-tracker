import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def main():
    st.set_page_config(layout="wide", page_title="India AQI Tracker", page_icon="🌫️")

    @st.cache_data
    def load_data():
        df = pd.read_csv('city_day.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        df['Month_Name'] = df['Date'].dt.strftime('%b')
        df['YearMonth'] = df['Date'].dt.to_period('M').astype(str)
        return df

    df = load_data()

    st.sidebar.caption("Built by Garvit Pandia | LPU Final Year | Data Science")

    st.title("India AQI Tracker 🌫️")

    # Filter Controls
    cities = sorted(df['City'].dropna().unique())
    default_city = "Udaipur" if "Udaipur" in cities else (cities[0] if len(cities)>0 else "")
    selected_city = st.sidebar.selectbox("Select City", cities, index=cities.index(default_city) if default_city in cities else 0)
    
    year_range = st.sidebar.slider("Select Year Range", 2015, 2020, (2015, 2020))
    
    default_compare = [selected_city, "Delhi", "Bengaluru"]
    default_compare = [c for c in default_compare if c in cities]
    selected_comparison_cities = st.sidebar.multiselect("Select Cities for Comparison", cities, default=default_compare)
    
    pollutants = ['PM2.5', 'PM10', 'NO2', 'CO', 'SO2', 'O3']
    selected_pollutant = st.sidebar.selectbox("Select Pollutant", pollutants)

    # Filtered Data
    filtered_df = df[(df['City'] == selected_city) & (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]

    # 4 Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    avg_aqi = filtered_df['AQI'].mean()
    worst_aqi = filtered_df['AQI'].max()
    best_aqi = filtered_df['AQI'].min()
    
    monthly_avg = filtered_df.groupby('YearMonth')['AQI'].mean()
    worst_month = monthly_avg.idxmax() if len(monthly_avg) > 0 else "N/A"

    col1.metric("Avg AQI", f"{avg_aqi:.1f}" if pd.notna(avg_aqi) else "N/A")
    col2.metric("Worst AQI", f"{worst_aqi:.1f}" if pd.notna(worst_aqi) else "N/A")
    col3.metric("Best AQI", f"{best_aqi:.1f}" if pd.notna(best_aqi) else "N/A")
    col4.metric("Worst Month", worst_month)

    # Row 1 Charts
    st.markdown("<br>", unsafe_allow_html=True)
    r1_col1, r1_col2 = st.columns(2)

    # Seasonal Heatmap
    heatmap_data = filtered_df.groupby(['Year', 'Month'])['AQI'].mean().reset_index()
    if not heatmap_data.empty:
        heatmap_pivot = heatmap_data.pivot(index="Year", columns="Month", values="AQI")
        fig_heatmap = px.imshow(heatmap_pivot, color_continuous_scale=["green", "yellow", "red"], 
                                labels=dict(x="Month", y="Year", color="Avg AQI"),
                                title=f"Seasonal AQI Heatmap - {selected_city}")
        fig_heatmap.update_layout(xaxis=dict(tickmode='array', tickvals=list(range(1,13)), ticktext=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']))
        r1_col1.plotly_chart(fig_heatmap, use_container_width=True)
        r1_col1.caption("Nov-Dec spike caused by crop stubble burning and cold air trapping pollutants near ground level")

    # Yearly average line chart
    yearly_data = filtered_df.groupby('Year')['AQI'].mean().reset_index()
    if not yearly_data.empty:
        fig_line = px.line(yearly_data, x='Year', y='AQI', title=f"Yearly Average AQI - {selected_city}", markers=True)
        r1_col2.plotly_chart(fig_line, use_container_width=True)

    # Row 2 Charts
    st.markdown("<br>", unsafe_allow_html=True)
    r2_col1, r2_col2 = st.columns(2)

    # City comparison bar chart
    comparison_df = df[(df['City'].isin(selected_comparison_cities)) & (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    if not comparison_df.empty:
        city_avg = comparison_df.groupby('City')['AQI'].mean().reset_index().sort_values('AQI')
        colors = ['red' if city == selected_city else 'gray' for city in city_avg['City']]
        fig_bar = go.Figure(go.Bar(
            x=city_avg['AQI'], 
            y=city_avg['City'], 
            orientation='h', 
            marker_color=colors
        ))
        fig_bar.update_layout(title="City Comparison (Avg AQI)", xaxis_title="Average AQI", yaxis_title="")
        r2_col1.plotly_chart(fig_bar, use_container_width=True)

    # Selected pollutant monthly area chart
    monthly_pollutant = filtered_df.groupby('YearMonth')[selected_pollutant].mean().reset_index()
    if not monthly_pollutant.empty:
        fig_area = px.area(monthly_pollutant, x='YearMonth', y=selected_pollutant, title=f"Monthly Average {selected_pollutant} - {selected_city}")
        r2_col2.plotly_chart(fig_area, use_container_width=True)

    # AQI Bucket Donut
    st.markdown("<br>", unsafe_allow_html=True)
    r3_col1, r3_col2 = st.columns(2)
    bucket_counts = filtered_df['AQI_Bucket'].value_counts().reset_index()
    bucket_counts.columns = ['Bucket', 'Count']
    color_map = {
        'Good': 'green',
        'Satisfactory': 'lightgreen',
        'Moderate': 'yellow',
        'Poor': 'orange',
        'Very Poor': 'red',
        'Severe': 'darkred'
    }
    if not bucket_counts.empty:
        fig_donut = px.pie(bucket_counts, values='Count', names='Bucket', hole=0.4, title=f"AQI Days Distribution - {selected_city}", color='Bucket', color_discrete_map=color_map)
        r3_col1.plotly_chart(fig_donut, use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: gray;'>Built by Garvit Pandia · LPU · <a href='https://github.com/garvit-pandia/india-aqi-tracker' target='_blank'>github.com/garvit-pandia/india-aqi-tracker</a> · <a href='https://huggingface.co/spaces/garvitpandia28/india-aqi-tracker' target='_blank'>huggingface.co/spaces/garvitpandia28/india-aqi-tracker</a></div>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
