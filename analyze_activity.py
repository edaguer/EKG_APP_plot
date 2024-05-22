import pandas as pd
import plotly.express as px #Leistung über die Zeit in Plot, welcher Leistung und Herzfrequenz über die Zeit anzeigt
import plotly.graph_objects as go

#Daten aus der CSV-Datei laden
def load_data():
    df = pd.read_csv("activity.csv")
    return df 

#Berechnungen für Mittelwert & maximale Leistung
def calculate_mean_max(df):
    mean_power = df["PowerOriginal"].mean()
    max_power = df["PowerOriginal"].max()
    return mean_power, max_power

#interaktiven Plot erstellen
def interactive_plot(df, zones):
    df["Time_in_Seconds"] = df.index
    fig = go.Figure() #leeren Figure erstellen

    #Leistungsdaten zur Figure hinzufügen
    fig.add_trace(go.Scatter(x=df["Time_in_Seconds"], y=df["PowerOriginal"],
                             mode='lines', name='Power (Watts)',
                             yaxis='y1'))

    #Herzfrequenzdaten zur Figure hinzufügen
    fig.add_trace(go.Scatter(x=df["Time_in_Seconds"], y=df["HeartRate"],
                             mode='lines', name='Heart Rate (BPM)',
                             yaxis='y2'))

   #Layout: Achsen, Legende, Skala auf beiden Seiten
    fig.update_layout(
        title="Power and Heart Rate over Time",
        xaxis=dict(title='Time (seconds)'),
        yaxis=dict(title='Power (Watts)', titlefont=dict(color='darkblue'),
                   tickfont=dict(color='darkblue'),range=[0,400]),
        yaxis2=dict(title='Heart Rate (BPM)', titlefont=dict(color='lightblue'),
                    tickfont=dict(color='lightblue'),range=[0,400],
                    anchor='x', overlaying='y', side='right'),
        legend=dict(x = 1.1, y = 1) #Legende weiter rechts positionieren
    )
    #Leistungszonen gefärbt hinzufügen
    #zone 1
    fig.add_shape(type="rect", x0=0, x1=df["Time_in_Seconds"].max(), y0=zones["Zone 1"][0], y1=zones["Zone 1"][1], line=dict(color="red", width=1), fillcolor="red", opacity=0.3, layer="below") #opacity für Farbenstärke
    #zone 2
    fig.add_shape(type="rect", x0=0, x1=df["Time_in_Seconds"].max(), y0=zones["Zone 2"][0], y1=zones["Zone 2"][1], line=dict(color="blue", width=1), fillcolor="blue", opacity=0.3, layer="below")
    #zone 3
    fig.add_shape(type="rect", x0=0, x1=df["Time_in_Seconds"].max(), y0=zones["Zone 3"][0], y1=zones["Zone 3"][1], line=dict(color="green", width=1), fillcolor="green", opacity=0.3, layer="below")
    #zone 4
    fig.add_shape(type="rect", x0=0, x1=df["Time_in_Seconds"].max(), y0=zones["Zone 4"][0], y1=zones["Zone 4"][1], line=dict(color="yellow", width=1), fillcolor="yellow", opacity=0.3, layer="below")
    #zone 5
    fig.add_shape(type="rect", x0=0, x1=df["Time_in_Seconds"].max(), y0=zones["Zone 5"][0], y1=zones["Zone 5"][1], line=dict(color="purple", width=1), fillcolor="purple", opacity=0.3, layer="below")
    
    fig.update_layout(legend_title="Legend") #Titel für Legende
    
    return fig
#Berechnung der Herzfrequenzzonen basierend auf dem macimalen Herzfrequenzwert
def calculate_zones(df, max_hr):
    zones = {
        "Zone 1": (0.5 * max_hr, 0.6 * max_hr),
        "Zone 2": (0.6 * max_hr, 0.7 * max_hr),
        "Zone 3": (0.7 * max_hr, 0.8 * max_hr),
        "Zone 4": (0.8 * max_hr, 0.9 * max_hr),
        "Zone 5": (0.9 * max_hr, 1.0 * max_hr)
    }
    #Herzfrequenzwerte zu den jeweiligen Zonen zuordnen    
    for zone, (lower, upper) in zones.items():
        df[zone] = df["HeartRate"].apply(lambda x: 1 if lower <= x <= upper else 0)
    
    return df, zones

#Berechnung der Zeit in den jeweiligen Zonen
def calculate_time_in_zones(df, zones):
    time_in_zones = {}
    for zone in zones:
        time_in_zone = df[zone].sum() * df["Duration"].mean() #/ 60  # in Minuten
        time_in_zones[zone] = round(time_in_zone, 2)
    return time_in_zones

#Berechnung der Durchschnittsleistung in den jeweiligen Zonen
def calculate_avg_power_in_zones(df, zones):
    avg_power_in_zones = {}
    for zone in zones:
        avg_power_in_zone = df[df[zone] == 1]["PowerOriginal"].mean()
        avg_power_in_zones[zone] = round(avg_power_in_zone, 2)
    return avg_power_in_zones


