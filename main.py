import pandas as pd
import streamlit as st

'''
# Wuhan Coronavirus in Singapore

Daily Updates of All Places _Confirmed_ Patients Have Visited, including hospitals
'''

@st.cache
def load_data():
    df = pd.read_csv("./data/wuhan_patient_trace.csv")
    return df


df = load_data()
st.map(df)
'''
Based on updates obtained from MOH. https://www.moh.gov.sg/2019-ncov-wuhan
'''
if st.checkbox("Show raw data", False):
    st.write(df)

#st.markdown("Written By Pier Lim")
