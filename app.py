import os
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILENAME = "aircrashesFullDataUpdated_2024.csv"

csv_path = None
for root, dirs, files in os.walk(BASE_DIR):
    if CSV_FILENAME in files:
        csv_path = os.path.join(root, CSV_FILENAME)
        break

if csv_path is None:
    st.error(f"CSV file '{CSV_FILENAME}' not found anywhere in project!")
    st.stop()

try:
    df = pd.read_csv(csv_path)
except Exception as e:
    st.error(f"Error loading CSV: {e}")
    st.stop()

st.title("Aircrashes Data Viewer")
st.write(f"CSV loaded from: `{csv_path}`")

st.subheader("First 10 rows of the dataset")
st.dataframe(df.head(10))

st.subheader("Dataset Summary")
st.write(df.describe(include='all'))


# Create Date column from Year, Month, Day
df["Date"] = pd.to_datetime(df[["Year", "Month", "Day"]], errors="coerce")

st.title("Air Crashes Dashboard")

# 1. Crashes per Year
st.subheader("Crashes per Year")
crashes_per_year = df.groupby("Year").size()
st.line_chart(crashes_per_year)

# 2. Top 10 Countries
st.subheader("Top 10 Countries with Most Crashes")
crashes_by_country = df["Country/Region"].value_counts().head(10)
st.bar_chart(crashes_by_country)

# 3. Top Aircraft Manufacturers
st.subheader("Top Aircraft Manufacturers")
top_manufacturers = df["Aircraft Manufacturer"].value_counts().head(10)
st.bar_chart(top_manufacturers)

# 4. Fatalities per Year
st.subheader("Fatalities per Year")
fatalities_per_year = df.groupby("Year")["Fatalities (air)"].sum()
st.line_chart(fatalities_per_year)

# 5.Survival Rate Distribution
st.subheader("Survival Rate Distribution")
df["Survivors"] = df["Aboard"] - df["Fatalities (air)"]
df["Survival Rate"] = df["Survivors"] / df["Aboard"]
st.bar_chart(df["Survival Rate"].dropna())
