import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import re

# 1. SEITENKONFIGURATION
st.set_page_config(page_title="Zonenpenetrationsanalyse", layout="wide")

# Hauptüberschrift mit HTML für größere Schrift und Abstand nach unten
st.markdown("<h1 style='font-size: 45px; margin-bottom: 30px;'>📊 Zonenpenetrationsanalyse</h1>", unsafe_allow_html=True)

# --- 2. DATEN DIREKT LADEN ---
DATEI_PFAD = 'Zonenpenetration Basis TPA 02 Zielplatz ausgeschlossen_202602181422.csv'

try:
    df = pd.read_csv(DATEI_PFAD, sep=';')

    # Fächer in Häuser einteilen
    df['Haus'] = (df['Fach'] - 1) // 3 + 1
    df = df.rename(columns={'Anzahl_Fahrpositionen': 'Anzahl_TPAs'})

    # Numerische Konvertierung
    cols_to_fix = ['Anzahl_TPAs', 'A', 'B', 'C']
    for c in cols_to_fix:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

    # REGAL numerisch aufbereiten
    df['REGAL_num'] = df['REGAL'].astype(str).str.lstrip('0').replace('', '0')
    df['REGAL_num'] = pd.to_numeric(df['REGAL_num'], errors='coerce').fillna(0).astype(int)

    # Filterung
    df_subset = df[df['REGAL_num'] >= 2].copy()

    if df_subset.empty:
        st.warning('Keine Daten für REGAL >= 2 gefunden.')
    else:
        # --- 3. METRIKEN ---
        col1, col2, col3 = st.columns(3)
        col1.metric("Max Fächer", int(df['Fach'].max()))
        col2.metric("Anzahl Häuser", int(df['Haus'].max()))
        col3.metric("Gesamt TPAs", int(df['Anzahl_TPAs'].sum()))

        # Abstand zwischen Metriken und Plot
        st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)

        # --- 4. PIVOTIERUNG ---
        pivot = df_subset.pivot_table(
            index='Haus',
            columns='REGAL_num',
            values='Anzahl_TPAs',
            aggfunc='sum',
            fill_value=0
        )

        # Sortierung
        def extract_number(s):
            nums = re.findall(r'\d+', str(s))
            return int(nums[0]) if nums else 0

        new_index = sorted(pivot.index, key=extract_number)
        pivot = pivot.reindex(index=new_index)

        # Achsen vervollständigen
        max_regal = int(pivot.columns.max())
        pivot = pivot.reindex(columns=np.arange(2, max_regal + 1), fill_value=0)

        # --- 5. PLOTTING (Heatmap) ---
        flat = pivot.values.flatten()
        vmax = np.percentile(flat, 99) if flat.size > 0 and flat.max() > 0 else 1
        
        fig_heat = px.imshow(
            pivot.values,
            x=[str(c) for c in pivot.columns],
            y=[str(i) for i in pivot.index],
            color_continuous_scale='Blues',
            aspect="auto",
            labels=dict(x='REGAL', y='Haus', color='Anzahl_TPAs'),
            title=f'Heatmap: Haus × REGAL (2..{max_regal})'
        )

        # Anpassung der Abstände und Schriftgrößen im Plot
        fig_heat.update_layout(
            height=800,
            margin=dict(t=150, b=50, l=50, r=50), # t=top erhöht für Abstand zur Überschrift
            title_font_size=28,
            font=dict(size=14)
        )

        fig_heat.update_traces(
            zmin=0, 
            zmax=vmax,
            hovertemplate='Haus: %{y}<br>REGAL: %{x}<br>Anzahl: %{z}<extra></extra>'
        )
        
        fig_heat.update_xaxes(side='top', tickangle=0, title_font=dict(size=20))
        fig_heat.update_yaxes(title_font=dict(size=20))
        
        st.plotly_chart(fig_heat, use_container_width=True)

        with st.expander("Rohdaten anzeigen"):
            st.dataframe(df, use_container_width=True)

except FileNotFoundError:
    st.error(f"Die Datei '{DATEI_PFAD}' wurde nicht gefunden.")