import streamlit as st
import createdb
from datetime import date


st.title("Customer Sign-up")

st.subheader("Welcome to Cup Adventure!")

with st.form("Customer Sign-up"):
    customer_id = st.text_input("Customer ID")
    first_name = st.text_input("Add your first name")
    last_name = st.text_input("Add your last name")

    submitted = st.form_submit_button("Submit")
    if submitted:
        user = {"customer id" = customer_id,
                "customer_firstName": first_name,
                "customer_lastName": last_name,
                "join_date": date.today()
                }
        try:
            createdb.add_user(user)
            st.write(
                f"Congratulations {first_name} {last_name}!  You have signed-up for Cup Adventure!"
            )
            st.write("Thank you for joining us in reducing Cup Waste!")
        except:
            st.write(
                "There was an error signing you up.  Please ensure no fields are blank."
            )
