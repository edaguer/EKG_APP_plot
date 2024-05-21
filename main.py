import streamlit as st
from analyze_activity import (
    load_data, calculate_mean_max, interactive_plot, 
    calculate_zones, calculate_time_in_zones, calculate_avg_power_in_zones
)

# Registerkarten erstellen
tab1, tab2 = st.tabs(["EKG-Data", "Power-Data"])

with tab1:
    st.header("EKG-Data")
    st.write("# My Plot")

    
with tab2:
    st.header("Power-Data")

    # Daten laden
    df = load_data()

    # Maximale Herzfrequenz eingeben
    max_hr = st.number_input("Bitte geben Sie die maximale Herzfrequenz ein:", min_value=100, max_value=220, value=190, step=1)

    # Mittelwert und Maximalwert der Leistung berechnen
    mean_power, max_power = calculate_mean_max(df)
    st.write(f"Mittelwert der Leistung: {mean_power:.2f} Watt")
    st.write(f"Maximalwert der Leistung: {max_power:.2f} Watt")


  
   # if st.button("Analyse durchführen"):
    df, zones = calculate_zones(df, max_hr)
  # Interaktiven Plot erstellen
    fig = interactive_plot(df,zones)
    st.plotly_chart(fig)

    time_in_zones = calculate_time_in_zones(df, zones)
    avg_power_in_zones = calculate_avg_power_in_zones(df, zones)

    st.subheader("Zeit in Herzfrequenzzonen (in Sekunden)")
    for zone, time in time_in_zones.items():
        st.write(f"{zone}: {time} Sekunden")

    st.subheader("Durchschnittliche Leistung in Herzfrequenzzonen (in Watt)")
    for zone, avg_power in avg_power_in_zones.items():
        st.write(f"{zone}: {avg_power} Watt")
