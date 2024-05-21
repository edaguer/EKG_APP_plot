"""import streamlit as st
from read_pandas import read_my_csv
from read_pandas import make_plot


# Wo startet sie Zeitreihe

# Wo endet sich
# Was ist die Maximale und Minimale Spannung
# Grafik
tab1, tab2 = st.tabs(["EKG-Data", "Power-Data"])

with tab1:
    st.header("EKG-Data")
    st.write("# My Plot")

    df = read_my_csv()
    fig = make_plot(df)

    st.plotly_chart(fig)

with tab2:
    st.header("Power-Data")

# Hilfsfunktionen
def load_data():
    df = pd.read_csv("activity.csv")
    return df

def calculate_statistics(df):
    mean_power = df["PowerOriginal"].mean()
    max_power = df["PowerOriginal"].max()
    return mean_power, max_power

def create_interactive_plot(df):
    df["Time_in_Seconds"] = df.index
    fig = px.line(df, x="Time_in_Seconds", y=["PowerOriginal", "HeartRate"], labels={'value':'Measurement', 'variable':'Metric'})
    return fig

def calculate_time_in_zones(df, max_hr):
    zones = {
        "Zone 1": (0.5 * max_hr, 0.6 * max_hr),
        "Zone 2": (0.6 * max_hr, 0.7 * max_hr),
        "Zone 3": (0.7 * max_hr, 0.8 * max_hr),
        "Zone 4": (0.8 * max_hr, 0.9 * max_hr),
        "Zone 5": (0.9 * max_hr, 1.0 * max_hr)
    }
    for zone, (lower, upper) in zones.items():
        df[zone] = df["HeartRate"].apply(lambda x: lower <= x < upper).astype(int)
    time_in_zones = {zone: (df[zone].sum() * df["Duration"].mean() / 60) for zone in zones}
    return time_in_zones

def calculate_avg_power_in_zones(df, zones):
    avg_power_in_zones = {zone: df[df[zone] == 1]["PowerOriginal"].mean() for zone in zones}
    return avg_power_in_zones
sg

"""

import streamlit as st
import pandas as pd
import plotly.express as px
from analyze_activity import load_data, calculate_mean_max, interactive_plot, calculate_zones, calculate_avg_power_in_zones

"""# Hilfsfunktionen aus analyze_activity
def load_data():
    df = pd.read_csv("activity.csv")
    return df

def calculate_statistics(df):
    mean_power = df["PowerOriginal"].mean()
    max_power = df["PowerOriginal"].max()
    return mean_power, max_power

def create_interactive_plot(df):
    df["Time_in_Seconds"] = df.index
    fig = px.line(df, x="Time_in_Seconds", y=["PowerOriginal", "HeartRate"], labels={'value':'Measurement', 'variable':'Metric'})
    return fig

def calculate_time_in_zones(df, max_hr):
    zones = {
        "Zone 1": (0.5 * max_hr, 0.6 * max_hr),
        "Zone 2": (0.6 * max_hr, 0.7 * max_hr),
        "Zone 3": (0.7 * max_hr, 0.8 * max_hr),
        "Zone 4": (0.8 * max_hr, 0.9 * max_hr),
        "Zone 5": (0.9 * max_hr, 1.0 * max_hr)
    }
    for zone, (lower, upper) in zones.items():
        df[zone] = df["HeartRate"].apply(lambda x: lower <= x < upper).astype(int)
    time_in_zones = {zone: (df[zone].sum() * df["Duration"].mean() / 60) for zone in zones}
    return time_in_zones

def calculate_avg_power_in_zones(df, zones):
    avg_power_in_zones = {zone: df[df[zone] == 1]["PowerOriginal"].mean() for zone in zones}
    return avg_power_in_zones
"""
st.title("Leistungstest Analyse")

tab1, tab2 = st.tabs(["EKG-Data", "Power-Data"])

with tab1:
    st.header("EKG-Data")
    df = load_data()
    mean_power, max_power = calculate_statistics(df)
    
    st.write(f"Mittelwert der Leistung: {mean_power:.2f} Watt")
    st.write(f"Maximalwert der Leistung: {max_power:.2f} Watt")
    
    fig = create_interactive_plot(df)
    st.plotly_chart(fig)

with tab2:
    st.header("Power-Data")
    df = load_data()
    max_hr = st.number_input("Bitte geben Sie die maximale Herzfrequenz ein:", min_value=100, max_value=220, value=190)
    
    time_in_zones = calculate_time_in_zones(df, max_hr)
    st.write("Zeit in den Herzfrequenzzonen (in Minuten):")
    for zone, time in time_in_zones.items():
        st.write(f"{zone}: {time:.2f} Minuten")
    
    avg_power_in_zones = calculate_avg_power_in_zones(df, time_in_zones.keys())
    st.write("Durchschnittliche Leistung in den Zonen (in Watt):")
    for zone, avg_power in avg_power_in_zones.items():
        st.write(f"{zone}: {avg_power:.2f} Watt")
