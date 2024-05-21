import pandas as pd
import plotly.express as px #Leistung über die Zeit in Plot, welcher Leistung und Herzfrequenz über die Zeit anzeigt
import plotly.graph_objects as go

def load_data():
    df = pd.read_csv("activity.csv")
    return df 

def calculate_mean_max(df):
    mean_power = df["PowerOriginal"].mean()
    max_power = df["PowerOriginal"].max()
    return mean_power, max_power

def interactive_plot(df, zones):
    df["Time_in_Seconds"] = df.index
    fig = px.line(df, x="Time_in_Seconds", y=["PowerOriginal", "HeartRate"], title="Power and Heart Rate over Time")
    # Add Power trace
    fig.add_trace(go.Scatter(x=df["Time_in_Seconds"], y=df["PowerOriginal"],
                             mode='lines', name='Power (Watts)',
                             yaxis='y1'))

    # Add Heart Rate trace
    fig.add_trace(go.Scatter(x=df["Time_in_Seconds"], y=df["HeartRate"],
                             mode='lines', name='Heart Rate (BPM)',
                             yaxis='y2'))

    # Add shaded areas for zones
    zone_colors = {
        "Zone 1": "rgba(0, 255, 0, 0.2)",  # Green
        "Zone 2": "rgba(255, 255, 0, 0.2)",  # Yellow
        "Zone 3": "rgba(255, 165, 0, 0.2)",  # Orange
        "Zone 4": "rgba(255, 69, 0, 0.2)",  # Red-Orange
        "Zone 5": "rgba(255, 0, 0, 0.2)"   # Red
    }
    
    for zone, (lower, upper) in zones.items():
        fig.add_shape(type="rect",
                      xref="paper", x0=0, x1=1,
                      yref="y2", y0=lower, y1=upper,
                      fillcolor=zone_colors[zone],
                      opacity=0.3,
                      line_width=0,
                      layer="below")

    # Create axis objects
    fig.update_layout(
        title="Power and Heart Rate over Time",
        xaxis=dict(title='Time (seconds)'),
        yaxis=dict(title='Power (Watts)', titlefont=dict(color='#1f77b4'),
                   tickfont=dict(color='#1f77b4')),
        yaxis2=dict(title='Heart Rate (BPM)', titlefont=dict(color='#ff7f0e'),
                    tickfont=dict(color='#ff7f0e'),
                    anchor='x', overlaying='y', side='right')
    )
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

#Fünf Zonen der Heart-Rates in Farben darstellen
