import streamlit as st
import pandas as pd
import time
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Auto-refresh counter setup
count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")

# Get the current timestamp and date
ts = time.time()
date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")

# Display the current timestamp in the app
st.write(f"Current time: {timestamp}")

# FizzBuzz logic
if count == 0:
    st.write("Count is zero")
elif count % 3 == 0 and count % 5 == 0:
    st.write("FizzBuzz")
elif count % 3 == 0:
    st.write("Fizz")
elif count % 5 == 0:
    st.write("Buzz")
else:
    st.write(f"Count: {count}")

# Attempt to load and display the CSV file
csv_file_path = f"Attendance/Attendance_{date}.csv"

try:
    df = pd.read_csv(csv_file_path)
    st.dataframe(df.style.highlight_max(axis=0))
except FileNotFoundError:
    st.error(f"CSV file not found: {csv_file_path}")
except Exception as e:
    st.error(f"An error occurred: {e}")
