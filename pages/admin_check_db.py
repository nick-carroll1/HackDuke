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
        "Read All Data",
        "Vendor Data",
        "Customer Data",
        "Order Data",
        "Product Data",
        "Order Details Data",
    ],
)

# if the user selects "Read Data" then show the table
if selection == "Read All Data":
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
    st.write("Vendor Data")
    query_metric_1 = "SELECT * FROM vendors_db"
    df_metric_1 = pd.read_sql(query_metric_1, connection)

    # create an altair chart to show vendor_name and cup_stock
    chart = (
        alt.Chart(df_metric_1)
        .mark_bar()
        .encode(
            x="vendor_name",
            y="cup_stock",
            color="vendor_name",
            tooltip=["vendor_name", "cup_stock"],
        )
        .interactive()
    )
    st.altair_chart(chart, height=500, width=500)


# close connection
connection.close()
