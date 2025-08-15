import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

st.set_page_config(page_title="IoT Temperature Capture", layout="wide")

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["timestamp", "temperature"])
if "running" not in st.session_state:
    st.session_state.running = False

def generate_temperature():
    base_temp = 22
    variation = np.random.normal(0, 0.5)
    return round(base_temp + variation, 2)

st.title("IoT Temperature Data Capture Unit")

col1, col2 = st.columns(2)
if col1.button("Start Capture"):
    st.session_state.running = True
if col2.button("Stop Capture"):
    st.session_state.running = False

if st.session_state.running:
    new_row = {
        "timestamp": datetime.now(),
        "temperature": generate_temperature()
    }
    st.session_state.data = pd.concat(
        [st.session_state.data, pd.DataFrame([new_row])],
        ignore_index=True
    )
    # Save to CSV so other repo can access it
    st.session_state.data.to_csv("temperature_data.csv", index=False)
    time.sleep(1)
    st.rerun()

# Show latest reading
if not st.session_state.data.empty:
    st.metric("Latest Temperature (°C)", st.session_state.data.iloc[-1]["temperature"])

# Show table
st.dataframe(st.session_state.data.tail(20))

# Download CSV
csv = st.session_state.data.to_csv(index=False)
st.download_button("Download Data as CSV", data=csv, file_name="temperature_data.csv", mime="text/csv")
