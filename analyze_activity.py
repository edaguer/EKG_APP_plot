import pandas as pd
import plotly.express as px #Leistung über die Zeit in Plot, welcher Leistung und Herzfrequenz über die Zeit anzeigt


def load_data():
    df = pd.read_csv("activity.csv")
    return df

def calculate_mean_max(df):
    mean_power = df["PowerOriginal"].mean()
    max_power = df["PowerOriginal"].max()
    return mean_power, max_power

def interactive_plot(df):
    df["Time_in_Seconds"] = df.index
    fig = px.line(df, x="Time_in_Seconds", y=["PowerOriginal", "HeartRate"], title="Power and Heart Rate over Time")
    return fig

def calculate_zones(df, max_hr):
    zones = {
        "Zone 1": (0.5 * max_hr, 0.6 * max_hr),
        "Zone 2": (0.6 * max_hr, 0.7 * max_hr),
        "Zone 3": (0.7 * max_hr, 0.8 * max_hr),
        "Zone 4": (0.8 * max_hr, 0.9 * max_hr),
        "Zone 5": (0.9 * max_hr, 1.0 * max_hr)
    }
    
    for zone, (lower, upper) in zones.items():
        df[zone] = df["HeartRate"].apply(lambda x: 1 if lower <= x <= upper else 0)
    
    return df, zones

def calculate_time_in_zones(df, zones):
    time_in_zones = {}
    for zone in zones:
        time_in_zone = df[zone].sum() * df["Duration"].mean() #/ 60  # in Minuten
        time_in_zones[zone] = round(time_in_zone, 2)
    return time_in_zones

def calculate_avg_power_in_zones(df, zones):
    avg_power_in_zones = {}
    for zone in zones:
        avg_power_in_zone = df[df[zone] == 1]["PowerOriginal"].mean()
        avg_power_in_zones[zone] = round(avg_power_in_zone, 2)
    return avg_power_in_zones
