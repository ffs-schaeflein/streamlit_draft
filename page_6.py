import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- 1. Streamlit Seite konfigurieren ---
st.set_page_config(page_title="Reichweitenanalyse", layout="wide")
st.title("📊 Reichweitenanalyse: Zone 02")

# --- 2. Daten direkt laden ---
FILE_PATH = 'Reichweite Paletten in Tagen immer abrunden ohne 0000000000_202603021122.csv'

@st.cache_data # Beschleunigt das Laden beim Neuladen der Seite
def load_data(path):
    return pd.read_csv(path, sep=';')

try:
    df = load_data(FILE_PATH)

    # --- 3. Spalten bereinigen ---
    target_col = 'Reichweite_Tage'

    if target_col in df.columns:
        # Konvertierung zu Numerisch
        if df[target_col].dtype == 'object':
            df[target_col] = pd.to_numeric(df[target_col].astype(str).str.replace(',', '.'), errors='coerce')
        
        # Filtern: Ausreißer und Nullwerte entfernen
        df_02 = df[[target_col]].dropna().copy()
        df_02 = df_02[(df_02[target_col] > 0) & (df_02[target_col] < 999)]

        # Tage runden für saubere Gruppierung
        df_02['Tag'] = df_02[target_col].round(0).astype(int)

        # Aggregation
        df_counts = df_02.groupby('Tag').size().reset_index(name='Anzahl_Paletten')
        df_counts = df_counts.sort_values('Tag')

        # --- 4. Kennzahlen (Key Metrics) ---
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Gesamtanzahl Paletten (Zone 02)", f"{df_counts['Anzahl_Paletten'].sum():,}")
        with col2:
            st.metric("Durchschnittliche Reichweite", f"{df_02['Tag'].mean():.2f} Tage")

        # --- 5. Interaktives Balkendiagramm ---
        fig = px.bar(
            df_counts, 
            x='Tag', 
            y='Anzahl_Paletten',
            text_auto=True,
            title='Reichweitenanalyse: Nur Zone 02 (Tagesgenau)',
            labels={'Tag': 'Reichweite in Tagen', 'Anzahl_Paletten': 'Anzahl der Paletten'},
            template='plotly_white',
            color_discrete_sequence=['#e67e22'] # Orange für Zone 02
        )

        fig.update_layout(
            xaxis_title="Reichweite (Tage)",
            yaxis_title="Anzahl Paletten",
            bargap=0.1,
            hovermode='x'
        )

        # X-Achse als Kategorie setzen (zeigt nur vorhandene Tage)
        fig.update_xaxes(type='category', tickangle=-45)
        fig.update_traces(textposition='outside')

        # Diagramm in Streamlit anzeigen
        st.plotly_chart(fig, use_container_width=True)

        # --- 6. Ergebniskontrolle (Optional: Rohdaten) ---
        with st.expander("Tabellarische Übersicht"):
            st.dataframe(df_counts, use_container_width=True)

    else:
        st.error(f"Die Spalte '{target_col}' wurde in der CSV nicht gefunden.")

except FileNotFoundError:
    st.error(f"Die Datei '{FILE_PATH}' wurde nicht im Verzeichnis gefunden.")