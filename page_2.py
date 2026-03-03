import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. KONFIGURATION ---
st.set_page_config(layout="wide", page_title="Kombiniertes ABC-Dashboard")
st.title("📊 Strategisches ABC-Analyse Dashboard")

# Dateipfade
DATEI_BASIS = 'ABC_Analyse_Langenau_202602171343.csv'
DATEI_ERWEITERT = 'Erweiterte_ABC_Analyse_Langenau_202602171404.csv'

# Hilfsfunktion für Gini
def calculate_gini(vals):
    x = np.asarray(vals, dtype=float).flatten()
    x = x[~np.isnan(x)]
    x = x[x >= 0]
    if x.size == 0 or x.sum() == 0:
        return 0.0
    x_sorted = np.sort(x)
    n = x_sorted.size
    s = x_sorted.sum()
    return (2.0 * np.sum((np.arange(1, n+1) * x_sorted)) / (n * s)) - (n + 1) / n

# --- 2. TEIL 1: BASIS-ANALYSE (Zwei Diagramme nebeneinander) ---
st.header("1. Basis-Auswertung (Zonen-Überblick)")

try:
    df_basis = pd.read_csv(DATEI_BASIS, sep=';')
    df_basis.columns = df_basis.columns.str.strip()
    
    # Datentypen
    for c in ['Haeufigkeit', 'kum_anteil_SKU', 'kum_anteil_OL']:
        if c in df_basis.columns:
            df_basis[c] = pd.to_numeric(df_basis[c], errors='coerce')

    order = ['A', 'B', 'C']
    counts = df_basis['ABC_Klasse'].value_counts().reindex(order).fillna(0)
    palette = {'A': '#4daf4a', 'B': '#377eb8', 'C': '#e41a1c'}

    fig1 = make_subplots(
        rows=1, cols=2, 
        subplot_titles=("Anzahl Artikel nach Klasse", "Pareto: SKU- vs. OL-Anteil"),
        horizontal_spacing=0.1
    )

    # Plot 1: Balken
    fig1.add_trace(go.Bar(
        x=counts.index, y=counts.values,
        marker_color=[palette.get(k, 'gray') for k in counts.index],
        text=counts.values, textposition='auto', name="SKUs", showlegend=False
    ), row=1, col=1)

    # Plot 2: Pareto
    for cls in order:
        sub = df_basis[df_basis['ABC_Klasse'] == cls]
        if not sub.empty:
            fig1.add_trace(go.Scatter(
                x=sub['kum_anteil_SKU'], y=sub['kum_anteil_OL'],
                mode='lines+markers', name=f'Klasse {cls}',
                fill='tozeroy', line=dict(color=palette[cls], width=2)
            ), row=1, col=2)

    fig1.update_layout(height=450, template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)
    
    with st.expander("Rohdaten Basis-Analyse"):
        st.dataframe(df_basis, use_container_width=True)

except FileNotFoundError:
    st.error(f"Basis-Datei '{DATEI_BASIS}' nicht gefunden.")

st.markdown("---")

# --- 3. TEIL 2: ERWEITERTE ANALYSE (Lorenz-Kurve untereinander) ---
st.header("2. Erweiterte Konzentrationsanalyse")

try:
    df_ext = pd.read_csv(DATEI_ERWEITERT, sep=';')
    df_ext.columns = df_ext.columns.str.strip()
    df_ext['Haeufigkeit'] = pd.to_numeric(df_ext['Haeufigkeit'], errors='coerce').fillna(0)

    # Lorenz-Berechnung
    vals = df_ext['Haeufigkeit'].values
    vals_sorted = np.sort(vals)
    cum_wealth = np.cumsum(vals_sorted) / vals_sorted.sum()
    cum_pop = np.arange(1, len(vals_sorted) + 1) / len(vals_sorted)
    gini_val = calculate_gini(vals)

    st.subheader(f"Lorenz-Kurve (Gini-Index: {gini_val:.3f})")
    
    fig_lorenz = go.Figure()
    fig_lorenz.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Gleichverteilung', line=dict(color='gray', dash='dash')))
    fig_lorenz.add_trace(go.Scatter(
        x=np.concatenate([[0], cum_pop]), y=np.concatenate([[0], cum_wealth]),
        mode='lines', name='Konzentrationskurve', fill='toself',
        fillcolor='rgba(228, 26, 28, 0.1)', line=dict(color='crimson', width=4)
    ))

    fig_lorenz.update_layout(
        height=600, template="plotly_white",
        xaxis_title="Kumulierter Anteil SKUs", yaxis_title="Kumulierter Anteil Häufigkeit"
    )
    st.plotly_chart(fig_lorenz, use_container_width=True)

    with st.expander("Rohdaten Erweiterte Analyse"):
        st.dataframe(df_ext, use_container_width=True)

except FileNotFoundError:
    st.error(f"Erweiterte Datei '{DATEI_ERWEITERT}' nicht gefunden.")