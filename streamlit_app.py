import streamlit as st
import json

import requests  # pip install requests
import streamlit as st  # pip install streamlit
from streamlit_lottie import st_lottie  # pip install streamlit-lottie


st.title("Cup Adventure")
st.write("Welcome to Cup Adventure.  Thank you for helping us to reduce cup waste.")

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_hello = load_lottieurl(
    "https://assets7.lottiefiles.com/packages/lf20_7njcjc4q.json"
)

st_lottie(
    lottie_hello,
    speed=1,
    reverse=False,
    loop=True,
    quality="low",  # medium ; high
    height=None,
    width=None,
    key=None,
)

    



