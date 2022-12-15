import mysql.connector
from mysql.connector import Error
import os
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import altair as alt
import datetime


def create_db_connection(host_name, user_name, user_password, user_port, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            port=user_port,
            database=db_name,
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


connection = create_db_connection(
    os.getenv("AWS_CUPADVENTURE_HOSTNAME"),
    os.getenv("AWS_CUPADVENTURE_USERNAME"),
    os.getenv("AWS_CUPADVENTURE_PASSWORD"),
    os.getenv("AWS_CUPADVENTURE_PORT"),
    "cup_adventure",
)

# fetch the table names from the database
cursor = connection.cursor()
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
tables = [table[0] for table in tables]




st.header("Customer Analytics for 2022")
st.subheader("Unique Users by Month")
st.subheader("Current User Growth Rate")
st.subheader("Unique Users per Cup")
st.subheader("Number of Active Cafe Distributing the Cups")
st.subheader("Cups Sold")
st.subheader("Cups Circulation Amount Per Period?")

st.subheader("Unique Cups by Month")

query_customer_1 = "SELECT month(join_date) as Month, COUNT(distinct customer_id) as new_user FROM customers_db GROUP BY month(join_date);"
df_customer_1 = pd.read_sql(query_customer_1, connection)
query_customer_2 = "SELECT month(transaction_date) as Month, count(distinct customer_id) as active_user FROM transactions_log WHERE transaction_status = 'Borrowed' GROUP BY month(transaction_date)"
df_customer_2 = pd.read_sql(query_customer_2, connection)
query_customer_3="SELECT month(transaction_date) as Month, count(distinct cup_id) as unique_cup FROM transactions_log GROUP BY month(transaction_date)"
df_customer_3=pd.read_sql(query_customer_3, connection)



unique=alt.Chart(df_customer_3).mark_line().encode(x='Month:N',y='unique_cup:Q')


st.altair_chart(unique)


st.subheader("New Users by Month")
# create an altair chart to show x:Month, y:new_user from df_metric_3
customer_chart = (
    alt.Chart(df_customer_1)
    .mark_bar()
    .encode(
        x=alt.X("Month:N", title="Month", axis=alt.Axis(labelAngle=-0)),
        y=alt.Y("new_user:Q", title="New Users"),
        tooltip=[
            alt.Tooltip("Month", title="Month"),
            alt.Tooltip("new_user:Q", title="New Users"),
        ],
)
    .interactive()
)
st.altair_chart(customer_chart, use_container_width=True)

st.subheader("Active Users by Month")
# create an altair line chart to show x:Month, y:Active_Users from df_metric_4
customer_line_chart = (
    alt.Chart(df_customer_2)
    .mark_bar()
    .encode(
        x=alt.X(
            "Month:N",
            title="Month",
            axis=alt.Axis(labelAngle=-0),
            scale=alt.Scale(zero=False),
        ),
        y=alt.Y("active_user:Q", title="Active Users", scale=alt.Scale(zero=False)),
        tooltip=[
            alt.Tooltip("Month", title="Month"),
            alt.Tooltip("active_user:Q", title="Active Users"),
        ],
    )
    .interactive()
)
st.altair_chart(customer_line_chart, use_container_width=True)
connection.close()
