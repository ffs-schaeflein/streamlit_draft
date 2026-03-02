import streamlit as st

def page_2():
    st.title("Page 2")

pg = st.navigation(["page_1.py", page_2,"page_3.py"])  
pg.run()