import streamlit as st
import pandas as pd
import numpy as np
import altair

st.title("Vendor Analytics")


st.title("unique users")

df=pd.read_excel("https://github.com/nick-carroll1/HackDuke/blob/main/raw_data/transactions_log.xlsx?raw=true")
d=df.groupby('transaction_date')['cup_id'].nunique()
d1 = d.to_frame().reset_index()

altair.Chart(d1).mark_line().encode(x='transaction_date',y='cup_id')


