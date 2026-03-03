import streamlit as st
import pandas as pd
import plotly.express as px

# --- Konfiguration ---
st.set_page_config(page_title="Verweildaueranalyse Kombiniert", layout="wide")
st.title("Verweildaueranalyse: Vergleich der Zonen")

@st.cache_data
def load_and_clean_data(file_path):
    try:
        df = pd.read_csv(file_path, sep=';')
        # Bereinigung: " Tage" entfernen und zu numerisch konvertieren
        df['Verweildauer'] = pd.to_numeric(
            df['Verweildauer'].astype(str).str.replace(' Tage', '', case=False).str.strip(), 
            errors='coerce'
        )
        return df.dropna(subset=['Verweildauer'])
    except FileNotFoundError:
        return None

# --- Funktion zur Diagrammerstellung ---
def create_histogram(df, title, color):
    fig = px.histogram(
        df, 
        x="Verweildauer", 
        title=title,
        labels={'Verweildauer': 'Tage'},
        color_discrete_sequence=[color]
    )
    
    fig.update_traces(
        xbins=dict(start=0, end=df['Verweildauer'].max(), size=7),
        marker_line_width=1,
        marker_line_color="white"
    )
    
    fig.update_layout(
        bargap=0.1,
        xaxis=dict(title="Wochen (7-Tage Intervalle)", tick0=0, dtick=7),
        yaxis_title="Anzahl der Einträge",
        template="plotly_white",
        height=500
    )
    return fig

# --- Daten laden ---
df_zone_02 = load_and_clean_data('Verweildauer 02 ohne Mandant ohne WE_STRAT 01 neu_202602270919.csv')
df_zone_blnm = load_and_clean_data('Verweildauer Zone BLNM_202602200934.csv')

# --- Anzeige Diagramm 1 (Zone 02) ---
st.header("Analyse Zone 02")
if df_zone_02 is not None:
    fig1 = create_histogram(df_zone_02, "Verweildauer in Wochen (Zone 02)", '#3498db')
    st.plotly_chart(fig1, use_container_width=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Durchschnitt", f"{df_zone_02['Verweildauer'].mean():.1f} Tage")
    c2.metric("Median", f"{df_zone_02['Verweildauer'].median():.1f} Tage")
    c3.metric("Max", f"{df_zone_02['Verweildauer'].max():.0f} Tage")
    
    # NEU: Expander für Rohdaten Zone 02
    with st.expander("Rohdaten Zone 02 anzeigen"):
        st.dataframe(df_zone_02, use_container_width=True)
else:
    st.error("Datei für Zone 02 nicht gefunden.")

st.markdown("---") # Trennlinie

# --- Anzeige Diagramm 2 (BLNM) ---
st.header("Analyse Zone BLNM")
if df_zone_blnm is not None:
    fig2 = create_histogram(df_zone_blnm, "Verweildauer in Wochen (BLNM)", '#2ecc71')
    st.plotly_chart(fig2, use_container_width=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Durchschnitt", f"{df_zone_blnm['Verweildauer'].mean():.1f} Tage")
    c2.metric("Median", f"{df_zone_blnm['Verweildauer'].median():.1f} Tage")
    c3.metric("Max", f"{df_zone_blnm['Verweildauer'].max():.0f} Tage")
    
    # NEU: Expander für Rohdaten Zone BLNM
    with st.expander("Rohdaten Zone BLNM anzeigen"):
        st.dataframe(df_zone_blnm, use_container_width=True)
else:
    st.error("Datei für BLNM nicht gefunden.")