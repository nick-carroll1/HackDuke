import mysql.connector
from mysql.connector import Error
import os
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st


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

# create a streamlit selectbox to select the table
table_name = st.selectbox("Select a table", tables)

# query the database based on table_name selected and preserve the column names
query = "SELECT * FROM " + table_name
df = pd.read_sql(query, connection)
st.write(df)

# create a streamlit selectbox to select the column
column_name = st.selectbox("Select a column", df.columns)

# close connection
connection.close()
