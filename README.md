---
title: India AQI Tracker
emoji: 🌫️
colorFrom: green
colorTo: red
sdk: streamlit
sdk_version: 1.32.0
python_version: "3.10"
app_file: app.py
pinned: false
---
# India AQI Tracker 🌫️

An interactive Streamlit data science dashboard for tracking and analyzing the Air Quality Index (AQI) across Indian cities.

[![Live Demo](https://img.shields.io/badge/Live_Demo-Hugging_Face-FFD21E?style=for-the-badge&logo=huggingface)](https://huggingface.co/spaces/garvitpandia28/india-aqi-tracker)

## 🖼️ Demo Screenshots

| Dashboard Overview | Heatmap & Yearly Trends |
|---|---|
| ![Dashboard Overview](demo/dashboard_overview.png) | ![Heatmap & Yearly](demo/heatmap_and_yearly.png) |

| City Comparison & Pollutant Analysis | AQI Distribution & Footer |
|---|---|
| ![City Comparison](demo/city_comparison_pollutant.png) | ![Donut Chart](demo/donut_chart_footer.png) |

## 📊 What It Shows
* **Historical Air Quality Trends**: Visualize yearly and daily AQI shifts from 2015 to 2020.
* **Pollutant Breakdowns**: Track specific pollutants like PM2.5, PM10, NO2, SO2, CO, and O3 over time.
* **City Comparisons**: Instantly compare AQI levels between multiple Indian cities.
* **Seasonal Heatmaps**: Identify the most severe periods of the year for pollution intensity.

## 💡 Key Insight
While the typical North Indian pollution narrative focuses heavily on Nov-Dec crop stubble burning and cold air inversion, cities like Udaipur present a **unique pollution pattern**. The data showcases how desert dust, localized industrial activity, and seasonal factors create an entirely different AQI fingerprint compared to the rest of the country.

## 🛠 Tech Stack
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging_Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)

## 🚀 How to Run Locally

```bash
# Clone the repository
git clone https://github.com/garvit-pandia/india-aqi-tracker.git
cd india-aqi-tracker

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit application
streamlit run app.py
```

## 📂 Dataset
* **Source**: CPCB (Central Pollution Control Board) via Kaggle.
* **Scope**: 26 Indian cities from 2015 through 2020. Contains daily records of key pollutants and aggregate AQI.

## 👤 Author
**Garvit Pandia**
* [GitHub Profile: @garvit-pandia](https://github.com/garvit-pandia)
* LPU Final Year Computer Science Student specializing in Data Science.
