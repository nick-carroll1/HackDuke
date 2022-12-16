import streamlit as st
from createdb import add_user
from datetime import date
import json
import requests  
from streamlit_lottie import st_lottie  

st.title("Customer Sign-up")

st.subheader("Welcome to Cup Adventure!")

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_hello = load_lottieurl(
    "https://assets7.lottiefiles.com/packages/lf20_jcikwtux.json"
)

st_lottie(
    lottie_hello,
    speed=1,
    reverse=False,
    loop=True,
    quality="medium",  # low ; high
    height=450,
    width=400,
    key=None,
)
with st.form("Customer Sign-up"):
    customer_id = st.text_input("Customer ID")
    first_name = st.text_input("Add your first name")
    last_name = st.text_input("Add your last name")

    submitted = st.form_submit_button("Submit")
    if submitted:
        user = {"customer_id": customer_id,
                "customer_firstName": first_name,
                "customer_lastName": last_name,
                "join_date": date.today()
                }
        try:
            add_user(user)
            st.write(
                f"Congratulations {first_name} {last_name}!  You have signed-up for Cup Adventure!"
            )
            st.write("Thank you for joining us in reducing Cup Waste!")
        except Exception as err:
            st.write(
                "There was an error signing you up.  Please ensure no fields are blank."
            )
            
