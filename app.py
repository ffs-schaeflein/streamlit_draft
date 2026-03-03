import streamlit as st

main_page = st.Page("page_1.py", title="Startseite")
page_2 = st.Page("page_2.py", title="ABC-Analyse")
page_3 = st.Page("page_3.py", title="Zonenpenetrationsanalyse")
page_4 = st.Page("page_4.py", title="Verweildaueranalyse")
page_5 = st.Page("page_5.py", title="Fachbelegungsanalyse")
page_6 = st.Page("page_6.py", title="Reichweitenanalyse")

pg = st.navigation([main_page, page_2, page_3, page_4, page_5, page_6])

pg.run()