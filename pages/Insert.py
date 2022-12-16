import streamlit as st
import streamlit.components.v1 as components
import os
import datetime

import mysql.connector

# server = "localhost"
# username="root"
# password=""
# dbname="qrcodedb"

cnx = mysql.connector.connect(
    host="cupadventure.cus96lnhsxap.us-east-1.rds.amazonaws.com",
    user="admin",
    password="NoahGift706-2",
    database="cup_adventure",
)

cur = cnx.cursor(buffered=True)


st.write('{"jenny": 1, "jenny2": 2}')
