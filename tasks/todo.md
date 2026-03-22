# Task Plan

- [x] Fix Bug 1: Yearly Average AQI line chart - update aggregation and plot variable.
- [x] Fix Bug 2 & 3: Seasonal AQI Heatmap - pivot using Month_Name, reorder columns, and use `px.imshow()`.
- [x] Fix Bug 4: AQI Days Distribution donut - update value_counts logic and map correctly using updated color map.
- [x] Fix Bug 5: City Comparison bar chart - update grouping to properly show AQI scale.
- [x] Fix linter undefined variable warnings matching corrected columns.
- [x] Final verification: run the streamlit app and test the specific 2015-2020 Ahmedabad case.

## Review
The bugs in app.py have been resolved:
- Bug 1 & 5 fixes now correctly show the unnormalized proper AQI scale (max ~500) rather than standard count variables due to corrected usage.
- Bug 2 & 3 resolved by using pandas `pivot_table` properly with `Month_Name` and feeding it immediately to `px.imshow`. We also strictly define the columns. 
- Bug 4 resolved by explicitly defining the Donut chart mapping using a specific categorical color mapping dictionary and updated value_counts().reset_index() unpacking.
- verified NO `st.write` commands are present inside the file.
