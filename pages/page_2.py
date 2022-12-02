import streamlit as st
import createdb
from datetime import date

st.title("Customer Sign-up")

st.subhead("Welcome to Cup Adventure!")

first_name = st.text_input("Add your first name")
last_name = st.text_input("Add your last name")
user = {"customer_firstName": first_name, "customer_lastName": last_name, "join_date": date.today().__str__()}
createdb.add_user(user)