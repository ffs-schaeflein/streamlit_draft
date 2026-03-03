import streamlit as st

# --- Konfiguration der Seite ---
st.set_page_config(
    page_title="Automatisierungsprojekt Langenau",
    layout="centered"
)

# --- Titel ---
st.title("Startseite")

# --- Projekt-Informationen ---
st.header("Automatisierungsprojekt Langenau")

# Textblock für die Beschreibung
st.write("Dieses Dashboard dient der Visualisierung und Analyse der Projektdaten.")

# --- Bereich: Datenbewertungen ---
st.subheader("Datenauswertungen")

# Eine einfache Liste der Auswertungspunkte
st.markdown("""
* ABC-Analyse
* Zonenpenetrationsanalyse
* Verweildaueranalyse
* Fachbelegungsanalyse
* Reichweitenanalyse
""")

# Optional: Button für Interaktion
if st.button("Auswertung aktualisieren"):
    st.success("Daten wurden aktualisiert!")
