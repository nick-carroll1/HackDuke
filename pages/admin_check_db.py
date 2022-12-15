import mysql.connector
from mysql.connector import Error
import os
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import altair as alt


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
    os.getenv("AWS_HOST"),
    os.getenv("AWS_USER"),
    os.getenv("AWS_PASSWORD"),
    os.getenv("AWS_PORT"),
    "cup_adventure",
)

# fetch the table names from the database
cursor = connection.cursor()
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
tables = [table[0] for table in tables]

# make a sidebar with choice of different pages named "Read Data" and "Add New Data"
st.sidebar.title("Navigation")
selection = st.sidebar.radio(
    "Go to",
    [
        "Welcome Page",
        "Read All Data",
        "Vendor Data",
        "Customer Data",
        "Order Data",
        "Product Data",
        "Order Details Data",
    ],
)

# if the user selects "Read Data" then show the table
if selection == "Welcome Page":
    st.write("Welcome to Cup Adventure Admin Page")
    st.write("Please select a page from the sidebar")

elif selection == "Read All Data":
    # create a streamlit selectbox to select the table
    table_name = st.selectbox("Select a table", tables)

    # query the database based on table_name selected and preserve the column names
    query = "SELECT * FROM " + table_name
    df = pd.read_sql(query, connection)
    st.write(df)

    # create a streamlit selectbox to select the column
    column_name = st.selectbox("Select a column", df.columns)

    # make a summary statistics table of the selected column in horizontal format and integer format
    st.write(df[column_name].describe().to_frame().T)

# if the user selects "Add New Data" then show the form
elif selection == "Vendor Data":
    query_metric_1 = "SELECT * FROM vendors_db"
    df_metric_1 = pd.read_sql(query_metric_1, connection)
    query_metric_2 = "SELECT month(transaction_date) as Month, count(distinct vendor_id) as Active_Vendors FROM transactions_log WHERE transaction_status = 'Borrowed' GROUP BY month(transaction_date)"
    df_metric_2 = pd.read_sql(query_metric_2, connection)

    st.header("Vendor Data for 2022")
    # create an altair chart to show vendor_name and cup_stock
    stock_chart = (
        alt.Chart(df_metric_1)
        .mark_bar()
        .encode(
            x=alt.X(
                "vendor_name",
                sort="-y",
                axis=alt.Axis(labelAngle=-90),
                title="Vendor Name",
            ),
            y=alt.Y("cup_stock", title="Cup Stock"),
            color="vendor_name",
            tooltip=["vendor_name", "cup_stock"],
        )
        .interactive()
    )
    st.altair_chart(stock_chart, use_container_width=True)

    # create an altair chart to show x:month(transaction_date), y count(distinct vendor_id) from df_metric_2
    vendor_chart = (
        alt.Chart(df_metric_2)
        .mark_bar()
        .encode(
            x=alt.X("Month:N", title="Month", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("Active_Vendors:Q", title="Active Vendors"),
            tooltip=[
                alt.Tooltip("Month", title="Month"),
                alt.Tooltip("Active_Vendors:Q", title="Active Vendors"),
            ],
        )
        .interactive()
    )
    st.altair_chart(vendor_chart, use_container_width=True)

# close connection
connection.close()
