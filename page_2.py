import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Seite auf Breitbild stellen
st.set_page_config(layout="wide", page_title="ABC-Analyse Dashbord")

st.title("📊 ABC-Analyse Dashbord")

# --- 1. DATEN DIREKT LADEN ---
# Hier wird die Datei ohne Nutzerinteraktion eingelesen
DATEI_PFAD = 'ABC_Analyse_Langenau_202602171343.csv'

try:
    df = pd.read_csv(DATEI_PFAD, sep=';')

    # Datentypen sicherstellen
    for c in ['Haeufigkeit', 'kum_anteil_SKU', 'kum_anteil_OL']:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')

    # Ordnung und Farben definieren
    order = ['A', 'B', 'C']
    counts = df['ABC_Klasse'].value_counts().reindex(order).fillna(0)
    palette = {'A': '#4daf4a', 'B': '#377eb8', 'C': '#e41a1c'}

    # --- 2. LAYOUT ERSTELLEN ---
    fig = make_subplots(
        rows=1, cols=2, 
        subplot_titles=("Anzahl Artikel nach ABC-Klasse", "Pareto: Kum. OL-Anteil vs SKU-Anteil"),
        horizontal_spacing=0.1
    )

    # --- Plot 1: Balkendiagramm ---
    fig.add_trace(
        go.Bar(
            x=counts.index,
            y=counts.values,
            marker_color=[palette.get(k, 'gray') for k in counts.index],
            text=counts.values,
            textposition='auto',
            name="Anzahl SKUs",
            showlegend=False
        ),
        row=1, col=1
    )

    # --- Plot 2: Pareto / Lorenz-Kurve ---
    for cls in order:
        sub = df[df['ABC_Klasse'] == cls]
        if not sub.empty:
            fig.add_trace(
                go.Scatter(
                    x=sub['kum_anteil_SKU'],
                    y=sub['kum_anteil_OL'],
                    mode='lines+markers',
                    name=f'Klasse {cls}',
                    fill='tozeroy', 
                    line=dict(color=palette[cls], width=2),
                    marker=dict(size=4),
                    opacity=0.7,
                    hovertemplate="<b>Klasse %{text}</b><br>" +
                                  "SKU Anteil: %{x}%<br>" +
                                  "OL Anteil: %{y}%<extra></extra>",
                    text=[cls] * len(sub)
                ),
                row=1, col=2
            )

    # --- 3. DESIGN & ANZEIGE ---
    fig.update_layout(
        height=600,
        template="plotly_white",
        title_text=f"Analyse: {DATEI_PFAD}",
        hovermode="closest",
        legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="right", x=1)
    )

    fig.update_xaxes(title_text="ABC-Klasse", row=1, col=1)
    fig.update_yaxes(title_text="Anzahl Artikel", row=1, col=1)
    fig.update_xaxes(title_text="kumulierte SKU-Anteile (%)", row=1, col=2)
    fig.update_yaxes(title_text="kumulierte OL-Anteile (%)", row=1, col=2)

    # Anzeige in der App
    st.plotly_chart(fig, use_container_width=True)

    # Rohdaten einklappbar machen
    with st.expander("Tabelle mit Rohdaten einblenden"):
        st.dataframe(df, use_container_width=True)

except FileNotFoundError:
    st.error(f"Die Datei '{DATEI_PFAD}' wurde nicht gefunden. Bitte prüfe, ob sie im richtigen Ordner liegt.")