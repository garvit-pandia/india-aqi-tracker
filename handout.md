# India AQI Tracker Debugging Handout

## Current State
I have investigated the Hugging Face Space for `india-aqi-tracker-live` using the Antigravity browser agent and local debugging scripts. All the data aggregation logic works correctly in Pandas, but the bugs are rendering issues caused by how Plotly interprets the Pandas objects.

## Issues Identified & Root Causes

1. **Yearly Average AQI (Straight Line 0 to 5):**
   - **Bug:** The line chart plots `0, 1, 2, 3, 4, 5` on the Y-axis instead of the actual AQI averages.
   - **Root Cause:** In the line `fig_line.add_trace(go.Scatter(x=yearly_data['Year_str'], y=yearly_data['AQI']))`, Plotly is incorrectly inferring the Pandas Series values. Sometimes when crossing minor library version changes, Plotly treats Series indices or falls back to standard enumeration.
   - **Fix:** Convert the Panda Series directly to Python lists: `y=yearly_data['AQI'].tolist()`.

2. **Seasonal AQI Heatmap (Blank/Empty):**
   - **Bug:** The Heatmap has correctly labeled axes but shows no colored tiles. The X-axis defaults to integer indices (0, 2, 4...) instead of month names.
   - **Root Cause:** Plotly Express's `imshow` is rendering the `pivot` Pandas DataFrame, but failing to map the DataFrame's string `.columns` to the X-axis and integer `.index` to the Y-axis automatically.
   - **Fix:** Explicitly pass the dataframe values and both axes to Plotly: `fig_heatmap = px.imshow(pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(), ...)`

3. **AQI Days Distribution (Donut Chart Slices Equal 1):**
   - **Bug:** The Donut chart maps `Category` but assigns each exactly `1` slice value instead of the counted days.
   - **Root Cause:** The `value_counts().reset_index()` behavior combined with `.columns = ['Category', 'Days']` works perfectly in local Pandas 2.x, but in different deployment environments (or with Plotly's strict typing), `px.pie` may misinterpret it if not strictly typed or explicitly renamed. 
   - **Fix:** Guarantee robust grouping with `dist = filtered_df['AQI_Bucket'].value_counts().rename_axis('Category').reset_index(name='Days')` and robust plotting with `.tolist()`.

4. **Monthly Average Area Chart (Incorrect Shape) / City Comparison (Missing Bars)**
   - **Bug:** `px.bar` fails to render elements if the data is a single row with specific typings or if X vs Y mapping behaves weirdly without standard types.
   - **Fix:** Convert to lists for the Area trace `go.Scatter` and explicitly define `y=city_avg['City'].tolist()` and `x=city_avg['AQI'].tolist()` for the `px.bar`.

## Next Steps
To continue where you left off, simply provide this file back to me. Let me know if you would like me to apply these fixes to `app.py`, test them out, and create the subsequent updates. I'll automatically adhere to the `Agent.md` guidelines during the implementation.
