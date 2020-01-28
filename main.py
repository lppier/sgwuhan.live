import pandas as pd
import streamlit as st

'''
# Wuhan Coronavirus in Singapore

Daily Updates of All Places _Confirmed_ Patients Have Visited, including hospitals - www.sgwuhan.live
'''

@st.cache
def load_data():
    df = pd.read_csv("./data/wuhan_patient_trace.csv")
    return df


df = load_data()
df_exclude_hospitals = df[df['hospital'] == 0]

if st.checkbox("Include Hospitals", True):
    st.map(df)
else:
    st.map(df_exclude_hospitals)

'''
Based on updates obtained from MOH. https://www.moh.gov.sg/2019-ncov-wuhan
'''
if st.checkbox("Show raw data", False):
    st.write(df)

#st.markdown("Written By Pier Lim")
