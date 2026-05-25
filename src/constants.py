CSV_PATH = "city_day.csv"

DEFAULT_CITY = "Udaipur"

YEAR_RANGE = (2015, 2020)

DEFAULT_COMPARISON_CITIES = ["Delhi", "Bengaluru"]

POLLUTANTS = ["PM2.5", "PM10", "NO2", "CO", "SO2", "O3"]

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

AQI_BUCKET_COLORS = {
    "Good": "#2ecc71",
    "Satisfactory": "#a8d08d",
    "Moderate": "#f1c40f",
    "Poor": "#e67e22",
    "Very Poor": "#e74c3c",
    "Severe": "#c0392b",
    "N/A": "#95a5a6",
}

AQI_BUCKET_THRESHOLDS = [
    (0, 50, "Good"),
    (51, 100, "Satisfactory"),
    (101, 200, "Moderate"),
    (201, 300, "Poor"),
    (301, 400, "Very Poor"),
    (401, float("inf"), "Severe"),
]

REQUIRED_COLUMNS = ["City", "Date", "AQI", "AQI_Bucket"]

HEATMAP_COLORSCALE = [[0, "#00B050"], [0.5, "#FFC000"], [1, "#FF0000"]]

LINE_COLOR = "#00f2fe"
MARKER_COLOR = "#4facfe"
HIGHLIGHT_COLOR = "#ff4b4b"
DEFAULT_BAR_COLOR = "#2d3748"
AREA_LINE_COLOR = "#f22f46"
AREA_FILL_COLOR = "rgba(242, 47, 70, 0.3)"

PAGE_TITLE = "India AQI Tracker"
PAGE_ICON = "🌫️"
