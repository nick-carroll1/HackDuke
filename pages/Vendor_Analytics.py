import streamlit as st
import pandas as pd
import numpy as np
import altair

st.title("Vendor Analytics")


st.title("Unique Cups")

df=pd.read_excel("https://github.com/nick-carroll1/HackDuke/blob/main/raw_data/transactions_log.xlsx?raw=true")
d=df.groupby('transaction_date')['cup_id'].nunique()
d1 = d.to_frame().reset_index()

unique=altair.Chart(d1).mark_line().encode(x='transaction_date',y='cup_id')


st.altair_chart(unique)
st.write(d1)


q1 = """
SELECT *
FROM transactions_log;
"""

l=reatedb.query(   q1,
    database,
    username,
    passwd,
    hostname,
    portnum)

st.write(l)
