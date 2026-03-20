import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def main():
    st.set_page_config(layout="wide", page_title="India AQI Tracker", page_icon="🌫️", initial_sidebar_state="expanded")

    # Premium Frontend Design injected via CSS
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Main Background & Gradient */
    .stApp {
        background: radial-gradient(circle at top right, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #e2e8f0;
    }
    
    /* Hide Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}
    
    /* Cards and Metrics */
    div[data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 1.1rem;
        font-weight: 400;
        color: #a0aec0;
    }
    
    /* Glassmorphism for containers */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(0, 242, 254, 0.15);
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    .stSelectbox label, .stSlider label, .stMultiSelect label {
        font-weight: 600;
        color: #e2e8f0;
    }
    
    /* Title Animation */
    .title-glow {
        text-align: center;
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(to right, #4facfe, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-shift 3s ease infinite;
        background-size: 200% 200%;
        margin-bottom: 2rem;
    }
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    </style>
    """, unsafe_allow_html=True)

    @st.cache_data
    def load_data():
        df = pd.read_csv('city_day.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        df['Month_Name'] = df['Date'].dt.strftime('%b')
        df['YearMonth'] = df['Date'].dt.to_period('M').astype(str)
        
        # Calculate/Fix AQI_Bucket based on custom logic requirements if missing or inconsistent
        def get_bucket(v):
            if pd.isna(v): return "N/A"
            if v <= 50: return "Good"
            if v <= 100: return "Satisfactory"
            if v <= 200: return "Moderate"
            if v <= 300: return "Poor"
            if v <= 400: return "Very Poor"
            return "Severe"
            
        # Prioritize filling NA buckets if AQI exists
        df['AQI_Bucket'] = df.apply(lambda row: get_bucket(row['AQI']) if pd.isna(row['AQI_Bucket']) or row['AQI_Bucket'] == "N/A" else row['AQI_Bucket'], axis=1)
        return df

    df = load_data()

    st.sidebar.markdown("<h3 style='text-align: center; color: #4facfe;'>🌫️ Settings</h3>", unsafe_allow_html=True)
    st.sidebar.caption("<div style='text-align: center;'>Built by Garvit Pandia | LPU Final Year | Data Science</div>", unsafe_allow_html=True)
    st.sidebar.markdown("---")

    st.markdown("<div class='title-glow'>India AQI Tracker</div>", unsafe_allow_html=True)

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
    
    # Calculate worst month gracefully
    monthly_avg = filtered_df.dropna(subset=['AQI']).groupby(['Year', 'Month', 'Month_Name'])['AQI'].mean().reset_index()
    if not monthly_avg.empty:
        worst_idx = monthly_avg['AQI'].idxmax()
        worst_row = monthly_avg.loc[worst_idx]
        worst_month_display = f"{worst_row['Month_Name']} {int(worst_row['Year'])}"
    else:
        worst_month_display = "N/A"

    col1.metric("Avg AQI", f"{avg_aqi:.1f}" if pd.notna(avg_aqi) else "N/A")
    col2.metric("Worst AQI", f"{worst_aqi:.1f}" if pd.notna(worst_aqi) else "N/A")
    col3.metric("Best AQI", f"{best_aqi:.1f}" if pd.notna(best_aqi) else "N/A")
    col4.metric("Worst Month", worst_month_display)

    # Row 1 Charts
    st.markdown("<br>", unsafe_allow_html=True)
    r1_col1, r1_col2 = st.columns(2)

    # Seasonal Heatmap
    month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    heatmap_data = filtered_df.dropna(subset=['AQI']).groupby(['Year', 'Month', 'Month_Name'])['AQI'].mean().reset_index()
    if not heatmap_data.empty:
        # Pivot by internal integer month and explicit index for years
        heatmap_pivot = heatmap_data.pivot(index="Year", columns="Month", values="AQI")
        # Ensure all 12 months exist as columns
        for m in range(1, 13):
            if m not in heatmap_pivot.columns:
                heatmap_pivot[m] = np.nan
        heatmap_pivot = heatmap_pivot[sorted(heatmap_pivot.columns)]

        y_labels = [str(int(y)) for y in heatmap_pivot.index]
        x_labels = [month_names[m-1] for m in heatmap_pivot.columns]

        fig_heatmap = go.Figure(data=go.Heatmap(
            z=heatmap_pivot.values,
            x=x_labels,
            y=y_labels,
            colorscale=[[0, "#00B050"], [0.5, "#FFC000"], [1, "#FF0000"]],
            colorbar=dict(title="Avg AQI"),
            hoverongaps=False
        ))
        fig_heatmap.update_layout(
            title=f"Seasonal AQI Heatmap - {selected_city}",
            xaxis_title="Month", yaxis_title="Year",
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', family='Outfit'), title_font=dict(size=20),
            yaxis=dict(type='category')
        )
        r1_col1.plotly_chart(fig_heatmap, use_container_width=True)
        r1_col1.markdown("<div style='text-align:center; color:#a0aec0; font-size:0.9rem;'>Nov-Dec spike caused by crop stubble burning and cold air trapping pollutants near ground level</div>", unsafe_allow_html=True)
    else:
        r1_col1.warning(f"No AQI data for {selected_city} to generate Heatmap.")

    # Yearly average line chart
    yearly_data = filtered_df.dropna(subset=['AQI']).groupby('Year')['AQI'].mean().reset_index()
    if not yearly_data.empty:
        yearly_data['Year_str'] = yearly_data['Year'].astype(str)
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=yearly_data['Year_str'], y=yearly_data['AQI'], mode='lines+markers',
                                      line=dict(color='#00f2fe', width=4), marker=dict(size=10, color='#4facfe'), name='AQI'))
        fig_line.update_layout(title=f"Yearly Average AQI - {selected_city}", 
                               margin=dict(t=50, b=30, l=10, r=10),
                               paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0', family='Outfit'),
                               xaxis=dict(showgrid=False, type='category', title='Year'),
                               yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title='AQI'), title_font=dict(size=20))
        r1_col2.plotly_chart(fig_line, use_container_width=True)
    else:
        r1_col2.warning(f"No AQI data for {selected_city} in selected range.")

    # Row 2 Charts
    st.markdown("<br>", unsafe_allow_html=True)
    r2_col1, r2_col2 = st.columns(2)

    # City comparison bar chart
    comparison_df = df[(df['City'].isin(selected_comparison_cities)) & (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    if not comparison_df.dropna(subset=['AQI']).empty:
        city_avg = comparison_df.dropna(subset=['AQI']).groupby('City')['AQI'].mean().reset_index().sort_values('AQI')
        colors = ['#ff4b4b' if city == selected_city else '#2d3748' for city in city_avg['City']]
        fig_bar = go.Figure(go.Bar(
            x=city_avg['AQI'], 
            y=city_avg['City'], 
            orientation='h', 
            marker_color=colors,
            marker_line_width=0, opacity=0.85
        ))
        fig_bar.update_layout(title="City Comparison (Avg AQI)", xaxis_title="Average AQI", yaxis_title="",
                              margin=dict(t=50, b=30, l=10, r=10),
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0', family='Outfit'), 
                              xaxis=dict(gridcolor='rgba(255,255,255,0.1)'), title_font=dict(size=20))
        r2_col1.plotly_chart(fig_bar, use_container_width=True)
    else:
        r2_col1.warning("Comparison data unavailable.")

    # Selected pollutant monthly area chart
    monthly_pollutant = filtered_df.dropna(subset=[selected_pollutant]).groupby('YearMonth')[selected_pollutant].mean().reset_index()
    if not monthly_pollutant.empty:
        fig_area = go.Figure()
        fig_area.add_trace(go.Scatter(x=monthly_pollutant['YearMonth'], y=monthly_pollutant[selected_pollutant], fill='tozeroy',
                                      line=dict(color='#f22f46'), fillcolor='rgba(242, 47, 70, 0.3)', name=selected_pollutant))
        fig_area.update_layout(title=f"Monthly Average {selected_pollutant} - {selected_city}",
                               margin=dict(t=50, b=30, l=10, r=10),
                               paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0', family='Outfit'),
                               xaxis=dict(showgrid=False), yaxis=dict(gridcolor='rgba(255,255,255,0.1)'), title_font=dict(size=20))
        r2_col2.plotly_chart(fig_area, use_container_width=True)
    else:
        r2_col2.warning(f"No {selected_pollutant} records for {selected_city}.")

    # AQI Bucket Donut
    st.markdown("<br>", unsafe_allow_html=True)
    r3_col1, r3_col2 = st.columns(2)
    bucket_counts = filtered_df['AQI_Bucket'].value_counts().reset_index()
    bucket_counts.columns = ['Bucket', 'Count']
    color_map = {
        'Good': '#00B050',
        'Satisfactory': '#92D050',
        'Moderate': '#FFC000',
        'Poor': '#FF7000',
        'Very Poor': '#FF0000',
        'Severe': '#C00000'
    }
    if not bucket_counts.empty:
        fig_donut = px.pie(bucket_counts, values='Count', names='Bucket', hole=0.5, title=f"AQI Days Distribution - {selected_city}", color='Bucket', color_discrete_map=color_map)
        fig_donut.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0', family='Outfit'), title_font=dict(size=20),
                                annotations=[dict(text='AQI', x=0.5, y=0.5, font_size=20, showarrow=False, font_color='#e2e8f0')])
        fig_donut.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=14, marker=dict(line=dict(color='#16213e', width=2)))
        r3_col1.plotly_chart(fig_donut, use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='background: rgba(255,255,255,0.03); border-radius: 12px; padding: 20px; text-align: center; color: #a0aec0; font-family: Outfit; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.05);'>
            Built by <strong>Garvit Pandia</strong> · LPU · 
            <a href='https://github.com/garvit-pandia/india-aqi-tracker' target='_blank' style='color: #4facfe; text-decoration: none;'>GitHub Repo</a> · 
            <a href='https://huggingface.co/spaces/garvitpandia28/india-aqi-tracker' target='_blank' style='color: #00f2fe; text-decoration: none;'>Hugging Face Space</a>
        </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
