import streamlit as st
import pandas as pd
import plotly.express as px

# --- Konfiguration ---
st.set_page_config(page_title="Verweildaueranalyse Kombiniert", layout="wide")
st.title("Verweildaueranalyse: Vergleich der Zonen")

# --- FUNKTION ZUR DATENAUFBEREITUNG (um Code-Duplikate zu vermeiden) ---
def prepare_data(file_path, color_hex, title_label):
    try:
        df = pd.read_csv(file_path, sep=';')
        
        # Numerische Konvertierung & Bereinigung
        df['Verweildauer'] = pd.to_numeric(
            df['Verweildauer'].astype(str).str.replace(' Tage', '', case=False).str.strip(), 
            errors='coerce'
        )
        df = df.dropna(subset=['Verweildauer'])
        df = df[df['Verweildauer'] >= 0] # Nur positive Werte

        # Gruppierung in 7-Tage-Wochen
        df['Woche_Start'] = (df['Verweildauer'] // 7).astype(int)
        
        # Aggregation
        df_counts = df.groupby('Woche_Start').size().reset_index(name='Anzahl')
        df_counts = df_counts.sort_values('Woche_Start')
        
        # Label erstellen (z.B. "Woche 2 (14-20 Tage)")
        df_counts['Woche_Label'] = df_counts['Woche_Start'].apply(
            lambda x: f"Woche {x} ({x*7}-{x*7+6} d)"
        )
        
        # Diagramm erstellen
        fig = px.bar(
            df_counts, 
            x="Woche_Label", 
            y="Anzahl",
            title=f"Verweildauer {title_label} - Nur belegte Zeiträume",
            color_discrete_sequence=[color_hex],
            template="plotly_white",
            text_auto=True
        )

        fig.update_layout(
            xaxis_title="Zeitintervalle (Wochen)",
            yaxis_title="Anzahl der Einträge",
            xaxis={'type': 'category'},
            bargap=0.2
        )
        
        return fig
    except Exception as e:
        st.error(f"Fehler beim Laden von {file_path}: {e}")
        return None

# --- ZONE 02 (OBEN) ---
st.header("Zone 02")
fig1 = prepare_data(
    'Verweildauer 020 ohne Eingrenzung des WE_DATUM_ohne AS_202603031623.csv', 
    '#3498db', 
    "Zone 02"
)
if fig1:
    st.plotly_chart(fig1, use_container_width=True)

st.markdown("---") # Trennlinie

# --- ZONE BLNM (UNTEN) ---
st.header("Zone BLNM")
fig2 = prepare_data(
    'Verweildauer BLNM ohne Eingrenzung des WE_DATUM_ohne AS_202603031629.csv', 
    '#2ecc71', 
    "Zone BLNM"
)
if fig2:
    st.plotly_chart(fig2, use_container_width=True)