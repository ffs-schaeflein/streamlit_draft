import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit Konfiguration
st.set_page_config(page_title="Fachbelegungsanalyse", layout="wide")
st.title("Fachbelegungsanalyse")

# --- TEIL 1: Zone 02 ---
st.header("Auswertung Fachbelegung Zone 02")

try:
    df1 = pd.read_csv('Fachbelegung ohne Sperrplatz Zone 02_202602231127.csv', sep=';')
    df1.columns = df1.columns.str.strip()

    # Interaktives Balkendiagramm erstellen
    fig1 = px.bar(
        df1, 
        x="Fachbelegung", 
        y="Anzahl_Plaetze",
        title="Fachbelegung Zone 02",
        labels={'Fachbelegung': 'Belegungsgrad', 'Anzahl_Plaetze': 'Anzahl Plätze'},
        color_discrete_sequence=['#3498db'],
        text="Anzahl_Plaetze"
    )

    fig1.update_traces(textposition='outside', cliponaxis=False)
    fig1.update_layout(
        bargap=0.4,
        xaxis=dict(tickmode='linear', tick0=0, dtick=1, title="Belegungsgrad"),
        yaxis_title="Anzahl Plätze",
        template="plotly_white",
        hovermode="x unified"
    )

    # In Streamlit anzeigen
    st.plotly_chart(fig1, use_container_width=True)

    # NEU: Rohdaten zum Ausklappen für Zone 02
    with st.expander("Rohdaten Zone 02 anzeigen"):
        st.dataframe(df1, use_container_width=True)

except FileNotFoundError:
    st.error("Datei für Zone 02 nicht gefunden.")

# Optische Trennung
st.markdown("---")

# --- TEIL 2: Zone BLNM ---
st.header("Auswertung Fachbelegung Zone BLNM")

try:
    df2 = pd.read_csv('Fachbelegung ohne Sperrplatz Zone BLNM_202602231158.csv', sep=';')
    df2.columns = df2.columns.str.strip()

    # Daten filtern & formatieren
    df_filtered = df2[df2['Anzahl_Plaetze'] > 0].copy()
    df_filtered['Fachbelegung'] = df_filtered['Fachbelegung'].astype(str)

    # Interaktives Balkendiagramm erstellen
    fig2 = px.bar(
        df_filtered, 
        x="Fachbelegung", 
        y="Anzahl_Plaetze",
        title="Fachbelegung Zone BLNM",
        labels={'Fachbelegung': 'Belegungsgrad', 'Anzahl_Plaetze': 'Anzahl Plätze'},
        color_discrete_sequence=['#2ecc71'],
        text="Anzahl_Plaetze"
    )

    fig2.update_traces(textposition='outside')
    fig2.update_layout(
        bargap=0.2,
        xaxis=dict(title="Belegungsgrad (Kategorien mit Daten)", type='category'),
        yaxis_title="Anzahl Plätze",
        template="plotly_white"
    )

    # In Streamlit anzeigen
    st.plotly_chart(fig2, use_container_width=True)

    # NEU: Rohdaten zum Ausklappen für Zone BLNM
    with st.expander("Rohdaten Zone BLNM anzeigen"):
        st.dataframe(df_filtered, use_container_width=True)

except FileNotFoundError:
    st.error("Datei für Zone BLNM nicht gefunden.")