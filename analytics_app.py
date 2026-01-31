import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
from sklearn.linear_model import LinearRegression
import time

st.set_page_config(page_title="Senior Data Scientist - Drone Analytics", layout="wide")

st.title("🚁 Senior Data Scientist - Drone Analytics")
st.markdown("Real-time telemetry analysis and predictive modeling for autonomous drones.")

# Configuration
BACKEND_URL = "http://localhost:8000/api/history"

def fetch_data():
    try:
        response = requests.get(BACKEND_URL)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            return df
        else:
            st.error(f"Failed to fetch data: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
        return None

def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in km
    R = 6371.0

    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)

    a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    return R * c

# Fetch data
df = fetch_data()

if df is not None and not df.empty:
    # Sidebar for refresh
    if st.sidebar.button('Refresh Data'):
        st.rerun()

    # Calculate Distance
    df['prev_lat'] = df['latitude'].shift(1)
    df['prev_lon'] = df['longitude'].shift(1)
    df['distance'] = df.apply(lambda row: haversine(row['prev_lat'], row['prev_lon'], row['latitude'], row['longitude']) if not pd.isna(row['prev_lat']) else 0, axis=1)
    total_distance = df['distance'].sum()

    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Data Points", len(df))
    col2.metric("Total Distance (km)", f"{total_distance:.4f}")
    col3.metric("Last Latitude", f"{df['latitude'].iloc[-1]:.4f}")

    # Visualization
    st.write("### Trajectory Map")
    fig = px.scatter_map(df, lat="latitude", lon="longitude", zoom=12, height=500)
    fig.update_layout(map_style="open-street-map")
    fig.update_traces(marker=dict(size=10, color='red'))
    st.plotly_chart(fig, width='stretch')

    # Prediction
    st.write("### 🔮 Predictive Modeling (Next Location)")
    if len(df) >= 5:
        # Prepare data for simple linear regression
        X = np.array(range(len(df))).reshape(-1, 1)
        y_lat = df['latitude'].values
        y_lon = df['longitude'].values

        # Fit models
        model_lat = LinearRegression().fit(X[-10:], y_lat[-10:])
        model_lon = LinearRegression().fit(X[-10:], y_lon[-10:])

        # Predict next point
        next_index = np.array([[len(df)]])
        next_lat = model_lat.predict(next_index)[0]
        next_lon = model_lon.predict(next_index)[0]

        st.success(f"Predicted Next Location: **Lat: {next_lat:.6f}, Lon: {next_lon:.6f}**")

        # Show comparison
        st.write(f"Trend (Last 10 points):")
        trend_df = pd.DataFrame({
            'Actual Lat': y_lat[-10:],
            'Actual Lon': y_lon[-10:]
        })
        st.line_chart(trend_df)
    else:
        st.info("Need at least 5 data points for predictive modeling.")

    st.write("### Data Preview")
    st.dataframe(df.tail())
else:
    st.warning("No data available. Make sure the backend is running and has data.")
