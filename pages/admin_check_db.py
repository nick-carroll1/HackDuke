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
    query_vendor_1 = "SELECT * FROM vendors_db"
    df_metric_1 = pd.read_sql(query_vendor_1, connection)
    query_vendor_2 = "SELECT month(transaction_date) as Month, count(distinct vendor_id) as Active_Vendors FROM transactions_log WHERE transaction_status = 'Borrowed' GROUP BY month(transaction_date)"
    df_metric_2 = pd.read_sql(query_vendor_2, connection)
    month = st.selectbox("Select a month", df_metric_1["Month"].unique())
    df_metric_3 = df_metric_1.loc[df_metric_1["Month"] == month, :]
    # grou by vendor_id and count how many transaction_status == "Borrowed" for each vendor_id and make it a dataframe
    df_metric_3 = (
        df_metric_3.groupby("vendor_id")
        .agg({"transaction_status": "count"})
        .reset_index()
    )

    st.header("Vendor Data for 2022")

    # All the chart codes - not deployed yet
    stock_chart = (
        alt.Chart(df_metric_1)
        .mark_bar()
        .encode(
            x=alt.X(
                "vendor_name",
                sort="-y",
                axis=alt.Axis(labelAngle=-0),
                title="Vendor Name",
            ),
            y=alt.Y("cup_stock", title="Cup Stock"),
            color="vendor_name",
            tooltip=[
                alt.Tooltip("vendor_name", title="Vendor Name"),
                alt.Tooltip("cup_stock", title="Cup Stock"),
            ],
        )
        .interactive()
    )

    # create an altair chart to show x:month(transaction_date), y count(distinct vendor_id) from df_metric_2
    vendor_chart = (
        alt.Chart(df_metric_2)
        .mark_bar()
        .encode(
            x=alt.X("Month:N", title="Month", axis=alt.Axis(labelAngle=-0)),
            y=alt.Y("Active_Vendors:Q", title="Active Vendors"),
            tooltip=[
                alt.Tooltip("Month", title="Month"),
                alt.Tooltip("Active_Vendors:Q", title="Active Vendors"),
            ],
        )
        .interactive()
    )

    st.subheader("Cup Stock by Vendor")
    st.altair_chart(stock_chart, use_container_width=True)

    st.subheader("Active Vendors by Month")
    st.altair_chart(vendor_chart, use_container_width=True)

elif selection == "Customer Data":
    query_customer_1 = "SELECT month(join_date) as Month, COUNT(distinct customer_id) as new_user FROM customers_db GROUP BY month(join_date);"
    df_customer_1 = pd.read_sql(query_customer_1, connection)
    query_customer_2 = "SELECT month(transaction_date) as Month, count(distinct customer_id) as active_user FROM transactions_log WHERE transaction_status = 'Borrowed' GROUP BY month(transaction_date)"
    df_customer_2 = pd.read_sql(query_customer_2, connection)

    st.header("Customer Data for 2022")
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
        .mark_area()
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

# close connection
connection.close()
