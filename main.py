import pandas as pd
import streamlit as st

'''
# Wuhan Coronavirus in Singapore
'''


@st.cache
def load_data():
    df = pd.read_csv("./data/wuhan_patient_trace.csv")
    df['reported_date'] = pd.to_datetime(df['reported_date'], dayfirst=True)
    df_subset = df[['patient', 'reported_date']].drop_duplicates()
    df_subset = df_subset.groupby('reported_date').count()
    df_subset['date'] = df_subset.index
    df_subset = df_subset.sort_values(by='date')
    df_subset = df_subset.reset_index(drop=True)
    df_subset = df_subset.rename(columns={'patient': 'patient_counts'})
    return df, df_subset


df, df_patient_count = load_data()
df_raw = df
total_confirmed_so_far = df['patient'].max()
df = df.dropna()
df_exclude_hospitals = df[df['hospital'] == 0]

st.write('Daily Updates of All Places ', total_confirmed_so_far,
         ' _Confirmed_ Patients Have Visited - http://www.sgwuhan.live')

if st.checkbox("Include Hospitals", False):
    st.map(df)
else:
    st.map(df_exclude_hospitals)


st.vega_lite_chart(df_patient_count, {
    "mark": {"type": "bar", "color": "maroon"},
    "selection": {
        "grid": {
            "type": "interval", "bind": "scales"
        }
    },
    'encoding': {
        "tooltip": [
            {"field": "date", "type": "temporal"},
            {'field': 'patient_counts', 'type': 'quantitative'}
        ],
        'x': {'field': 'date', 'type': 'temporal'},
        'y': {'field': 'patient_counts', 'type': 'quantitative'},
    },
})#, use_container_width=True)

'''
Based on updates obtained from MOH. https://www.moh.gov.sg/2019-ncov-wuhan
'''
if st.checkbox("Show raw data", False):
    st.write(df_raw)

# st.markdown("Written By Pier Lim")
