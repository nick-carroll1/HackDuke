import streamlit as st
import pandas as pd
import numpy as np
import altair

df=pd.read_excel("https://github.com/nick-carroll1/HackDuke/blob/main/raw_data/transactions_log.xlsx?raw=true")
df.head()

st.title("Vendor Analytics")


st.title("unique users")
