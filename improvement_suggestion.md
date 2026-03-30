# 🚀 India AQI Tracker: Improvement Suggestions

While testing each visual component and diving deep into the data mechanics of the `india-aqi-tracker`, I have noticed a few exciting opportunities. Here are 5 data science/frontend additions you could implement:

### 1. 🗺️ Interactive Scatter Maps (Folium or Pydeck)
Right now, you evaluate cities strictly via an isolated dropdown sidebar.
* **The Idea:** Provide latitude and longitude estimates for major Indian states and render an interactive bubble map (`st.map` or `st.pydeck_chart`) on the dashboard where larger bubbles signify higher historic/average pollution.
* **Why:** Maps bring spatial context directly to real-world issues. Users could immediately see differences between the Northern belt and Southern coastal states.

### 2. 🤖 Predictive Index Projection (SARIMA / Prophet)
Take this portfolio piece beyond analytical reporting into **prescriptive data science**.
* **The Idea:** Use a simple univariate model (via `statsmodels.tsa.seasonal.SARIMAX` or Facebook's `Prophet`) to train on the city’s historical curve and project an estimation line into 2021+. 
* **Why:** Demonstrating forecasting skills is an exceptional addition to any ML or Data Science portfolio project.

### 3. 🤔 Detailed Actionable Tooltips on Graphs
Plotly offers rich custom hovering that isn't fully utilized yet.
* **The Idea:** On the **Seasonal Heatmap**, you can inject custom tooltip text (`hover_data={'Month': True, 'Avg AQI': ':.1f', 'Main Pollutant': ...}`) so hovering over a "Severe" tile states specifically "Driven by PM2.5 spikes".
* **Why:** Rather than making the user hunt through the Dropdowns to find which pollutant spiked, immediately expose the dominant feature.

### 4. 🎛️ Dynamic Data Smoothing
The initial charts for smaller cities can sometimes be wildly noisy.
* **The Idea:** Add a simple toggle switch using `st.checkbox("Apply 3-Month Moving Average")` that utilizes `df['AQI'].rolling(window=3).mean()`.
* **Why:** This makes seasonal trends far easier to track visually over time, smoothing out chaotic, unreadable day-to-day data.

### 5. ⚠️ Historical Event Correlational Indicators
* **The Idea:** Add vertical event lines (`fig.add_vline`) to charts or scatter plots around explicitly significant dates like **Diwali celebrations** or the **March 2020 COVID-19 Lockdown**.
* **Why:** Visualizing massive systemic drops (COVID) provides immediate recognizable stories to the user.

*Let me know if any of these catch your eye! I can start wiring these up today!*
