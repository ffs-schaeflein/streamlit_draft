import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import re

# 1. SEITENKONFIGURATION
st.set_page_config(page_title="Zonenpenetrationsanalyse", layout="wide")

st.markdown("<h1 style='font-size: 45px; margin-bottom: 30px;'>📊 Zonenpenetrationsanalyse</h1>", unsafe_allow_html=True)

# --- DATEIPFAD ---
PFAD_HEATMAP = 'Zonenpenetration Basis TPA 02 Zielplatz ausgeschlossen_202602181422.csv'

# Hilfsfunktion zum Sortieren der Haus-Nummern (falls diese Strings sind)
def extract_number(text):
    nums = re.findall(r'\d+', str(text))
    return int(nums[0]) if nums else 0

if os.path.exists(PFAD_HEATMAP):
    try:
        # Daten laden
        df = pd.read_csv(PFAD_HEATMAP, sep=';')
        df.columns = df.columns.str.strip()

        # Validierung der Pflichtspalten
        if 'Fach' in df.columns and 'REGAL' in df.columns:
            
            # --- DATENAUFBEREITUNG ---
            # Berechnung der Häuser (Fächer in 3er Gruppen)
            df['Haus'] = (df['Fach'] - 1) // 3 + 1
            
            # Regal-Nummer extrahieren
            df['REGAL_num'] = df['REGAL'].astype(str).str.extract(r'(\d+)').astype(float).fillna(0).astype(int)
            
            # Filterung: Regale ab Nummer 2
            df_subset = df[df['REGAL_num'] >= 2].copy()

            # Metriken anzeigen
            total_tpas = df['Anzahl_Fahrpositionen'].sum() if 'Anzahl_Fahrpositionen' in df.columns else 0
            col1, col2, col3 = st.columns(3)
            col1.metric("Max Fächer", int(df['Fach'].max()))
            col2.metric("Anzahl Häuser", int(df['Haus'].max()))
            col3.metric("Gesamt Einheiten", int(total_tpas))

            st.divider()

            # --- SCHLEIFE FÜR HEATMAPS (Gesamt + Kategorien) ---
            # Wir definieren, welche Werte wir als Heatmap sehen wollen
            # Falls deine CSV Spalten wie 'A', 'B', 'C' für Kategorien hat:
            kategorien = []
            for k in ['Anzahl_Fahrpositionen', 'A', 'B', 'C']:
                if k in df_subset.columns:
                    kategorien.append(k)

            for kat in kategorien:
                st.subheader(f"Analyse: {kat}")
                
                # Pivot-Tabelle erstellen
                pivot = df_subset.pivot_table(
                    index='Haus', 
                    columns='REGAL_num', 
                    values=kat, 
                    aggfunc='sum', 
                    fill_value=0
                )

                if not pivot.empty:
                    # Index (Häuser) numerisch sortieren
                    try:
                        new_index = sorted(pivot.index, key=extract_number)
                        pivot = pivot.reindex(index=new_index)
                    except:
                        pivot = pivot.sort_index()

                    # Regal-Achse vervollständigen (Lücken füllen)
                    max_regal = int(pivot.columns.max())
                    all_regale = np.arange(2, max_regal + 1)
                    pivot = pivot.reindex(columns=all_regale, fill_value=0)

                    # Heatmap Erstellung
                    # Skalierung: Bei Kategorien A,B,C fix 0-100, bei Gesamt flexibel oder nach Bedarf
                    color_range = [0, 100] if kat in ['A', 'B', 'C'] else None

                    fig = px.imshow(
                        pivot.values,
                        x=[f"R{c}" for c in pivot.columns],
                        y=[str(i) for i in pivot.index],
                        color_continuous_scale='Blues',
                        range_color=color_range,
                        aspect="auto",
                        labels=dict(x="Regal", y="Haus", color=f"Summe {kat}"),
                        title=f"Heatmap {kat} (Haus × Regal)"
                    )

                    fig.update_layout(
                        height=600,
                        margin=dict(t=50, b=50, l=50, r=50),
                        xaxis=dict(side='top')
                    )
                    
                    fig.update_traces(
                        hovertemplate="Haus: %{y}<br>Regal: %{x}<br>Wert: %{z}<extra></extra>"
                    )

                    # In Streamlit anzeigen
                    st.plotly_chart(fig, use_container_width=True)
                    
                    with st.expander(f"Datenquelle: {kat}"):
                        st.dataframe(pivot, use_container_width=True)
                    
                    st.markdown("---") # Trennlinie zwischen den Heatmaps

        else:
            st.error(f"Pflichtspalten fehlen. Vorhanden: {list(df.columns)}")

    except Exception as e:
        st.error(f"Ein Fehler ist aufgetreten: {e}")
else:
    st.error(f"Die Datei '{PFAD_HEATMAP}' wurde nicht gefunden.")