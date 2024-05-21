# %%
import pandas as pd
import plotly.express as px #Leistung über die Zeit in Plot, welcher Leistung und Herzfrequenz über die Zeit anzeigt


def load_data():
    df = pd.read_csv("activity.csv")
    print(df.head()) #return df

# %%
#Mittelwert und Maximalwert der Leistung
def calculate_mean_max(df):
    mean_power = df["PowerOriginal"].mean()
    max_power = df["PowerOriginal"].max()
    return mean_power, max_power

# %%
def interactive_plot(df):
    df["Time_in_Seconds"] = df.index
    fig = px.line(df, x= "Time_in_Seconds", y= "PowerOriginal")
    fig.show() #return fig

# %%
#5 Zonen mittels Herzfrequenz einteilen
def calculate_zones(df,max_hr):
    max_hr = int(input("Bitte geben Sie die maximale Herzfrequenz ein: "))
    #Definition der 5 HR-Zonen
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


# %%
# Durchschnittliche Leistung in jeder Zone berechnen
def calculate_avg_power_in_zones(df, zones):
    for zone in zones:
    avg_power_in_zones = {zone: df[df[zone] == 1]["PowerOriginal"].mean() for zone in zones}
    return avg_power_in_zones

