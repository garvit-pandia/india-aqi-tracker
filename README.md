# India AQI Tracker
> An interactive data science dashboard for tracking and analyzing the Air Quality Index (AQI) across Indian cities.

https://github.com/garvit-pandia/india-aqi-tracker/blob/main/2026-03-22_23-07.png


## Features
- **Historical Analysis:** Visualize yearly and daily AQI shifts from 2015 to 2020.
- **City Comparisons:** Instantly compare overall AQI averages and historical values between multiple Indian cities.
- **Seasonal Heatmaps:** Identify the most severe periods of the year for pollution intensity across specific location domains.
- **Categorical Breakdown:** Analyze the distribution of poor vs good air quality days utilizing distinct visualizations.

## Dashboard Screenshots
| Overview & KPI Dashboard | Heatmap & Yearly Charts |
|---|---|
| ![Overview](media/2026-03-22_23-06.png) | ![Heatmap](media/2026-03-22_23-07.png) |

| Distribution & Pollutant Analysis |
|---|
| ![Distribution](media/2026-03-22_23-07_1.png) |

## Tech Stack
- Python
- Pandas
- Streamlit
- Plotly

## Data Source
- [CPCB Air Quality Dataset via Kaggle](https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india)

## Run Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Start the application
streamlit run app.py
```

## Live Demo
Check out the fully hosted version on Hugging Face Spaces: [India AQI Tracker](https://huggingface.co/spaces/garvitpandia28/india-aqi-tracker)
