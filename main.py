import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

'''
# Wuhan nCov Coronavirus in Singapore
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
df = df.dropna()  # removes those rows that doesn't have data
df_exclude_hospitals = df[df['hospital'] == 0]

begin = df_patient_count.iloc[0]['date']
end = df_patient_count.iloc[-1]['date']
max_days = (end - begin).days + 1
st.write('Daily Updates of All Places ', total_confirmed_so_far,
         ' _Confirmed_ Patients Have Visited - http://www.sgwuhan.live, based on past ', max_days,
         ' days of updates obtained from MOH. https://www.moh.gov.sg/2019-ncov-wuhan')
days_to_filter = st.slider('Limit to Locations Reported X Days Ago', 1, max_days, max_days)
date_starting = datetime.now() - timedelta(days=days_to_filter)
date_starting = pd.Timestamp(date_starting)
df = df[df['reported_date'] >= date_starting]
df_exclude_hospitals = df_exclude_hospitals[df_exclude_hospitals['reported_date'] >= date_starting]

# st.map(df)
if st.checkbox("Include Hospitals", False):
    st.map(df)
else:
    st.map(df_exclude_hospitals)

st.write(df)

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
})  # , use_container_width=True)



# st.markdown("Written By Pier Lim")
