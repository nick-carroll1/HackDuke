import mysql.connector
from mysql.connector import Error
import os
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import altair as alt
import datetime
from createdb import query, add_user, update_user


# def create_db_connection(host_name, user_name, user_password, user_port, db_name):
#     connection = None
#     try:
#         connection = mysql.connector.connect(
#             host=host_name,
#             user=user_name,
#             passwd=user_password,
#             port=user_port,
#             database=db_name,
#         )
#         print("MySQL Database connection successful")
#     except Error as err:
#         print(f"Error: '{err}'")

#     return connection


# connection = create_db_connection(
#     os.getenv("AWS_HOST"),
#     os.getenv("AWS_USER"),
#     os.getenv("AWS_PASSWORD"),
#     os.getenv("AWS_PORT"),
#     "cup_adventure",
# )

# # fetch the table names from the database
# cursor = connection.cursor()
# cursor.execute("SHOW TABLES")
# tables = cursor.fetchall()
# tables = [table[0] for table in tables]


# def rent_cup(
#     user,
#     vendor,
#     cup,
#     database="cup_adventure",
#     username=os.getenv("AWS_USER"),
#     passwd=os.getenv("AWS_PASSWORD"),
#     hostname=os.getenv("AWS_HOST"),
#     portnum=int(os.getenv("AWS_PORT")),
# ):
#     # Create Connection
#     connection = mysql.connector.connect(
#         user=username, password=passwd, host=hostname, port=portnum
#     )
#     cursor = connection.cursor()
#     cursor.execute(f"USE {database};")
#     columns = [
#         "order_id",
#         "transaction_date",
#         "customer_id",
#         "vendor_id",
#         "cup_id",
#         "transaction_status",
#         "Revenue",
#     ]
#     values = [None, date.today(), user, vendor, cup, "'Borrowed'", 0]
#     # execute query
#     try:
#         values[0] = cursor.execute(f"SELECT MAX(order_id) + 1 FROM transactions_log;")[
#             0
#         ][0]
#         values[2] = cursor.execute(
#             f"SELECT customer_id FROM customers_db WHERE user_name = '{user}';"
#         )[0][0]
#         values[3] = (
#             "'"
#             + cursor.execute(
#                 f"SELECT vendor_id FROM vendors_db WHERE vendor_name = '{vendor}';"
#             )[0][0]
#             + "'"
#         )
#         cursor.execute(f"INSERT INTO transactions_log ({columns}) VALUES ({values});")
#         cursor.execute(
#             f"UPDATE customers_db SET cup_rental = '{cup}' WHERE user_name = '{user}';"
#         )
#         cursor.execute(
#             f"UPDATE cups_db SET cup_status = 'Borrowed', vendor_id = 'Out' WHERE cup_id = {cup};"
#         )
#         cursor.execute(
#             f"UPDATE vendors_db SET cup_stock = (SELECT cup_stock FROM vendors_db WHERE vendor_name = {vendor} - 1) WHERE vendor_name = {vendor};"
#         )
#         connection.commit()
#     except:
#         connection.rollback()
#     connection.close()
#     pass


# make a sidebar with choice of different pages named "Read Data" and "Add New Data"
st.sidebar.title("Navigation")
selection = st.sidebar.radio(
    "Go to",
    [
        "Welcome Page",
        "Read All Data",
        "Vendor Data",
        "Customer Data",
        "Pull Customer Data",
        "Add New Customer Data",
    ],
)


def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        userquery = f"SELECT user_name, password FROM customers_db where user_name = '{st.session_state['username']}';"
        results = query(userquery)
        passwords = {eachLine[0]: eachLine[1] for eachLine in results}
        if (
            (st.session_state["username"] in passwords.keys())
            and (st.session_state["password"]
                 == passwords[st.session_state["username"]])
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            # del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        with st.form("sign-in1"):
            # First run, show inputs for username + password.
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")

            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if submitted:
                password_entered()
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        with st.form("sign-in2"):
            # First run, show inputs for username + password.
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")

            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if submitted:
                password_entered()
    else:
        # Password correct.
        return True


st.title("Cup Adventure")
if check_password():
    # if the user selects "Read Data" then show the table
    if selection == "Welcome Page":
        st.write("Welcome to Cup Adventure Admin Page")
        st.write("Please select a page from the sidebar")

        st.write('test')
        myquery = "SHOW TABLES;"
        results = db.query(myquery)
        st.write(results)

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
                x=alt.X("Month:N", title="Month",
                        axis=alt.Axis(labelAngle=-0)),
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
                x=alt.X("Month:N", title="Month",
                        axis=alt.Axis(labelAngle=-0)),
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
                y=alt.Y("active_user:Q", title="Active Users",
                        scale=alt.Scale(zero=False)),
                tooltip=[
                    alt.Tooltip("Month", title="Month"),
                    alt.Tooltip("active_user:Q", title="Active Users"),
                ],
            )
            .interactive()
        )
        st.altair_chart(customer_line_chart, use_container_width=True)
        connection.close()
    elif selection == "Pull Customer Data":
        st.header("Pull User Data")
        st.write("Please enter the user ID below to pull the user data")
        # user_id = st.text_input("User ID", "")
        # if st.button("Pull Data"):
        #     query = "SELECT * FROM customers_db WHERE customer_id = " + user_id
        #     df = pd.read_sql(query, connection)
        #     st.write(df)
        # # give a choice of using user_name
        username = st.text_input("User Name", "")
        try:
            if st.button("Pull Data"):
                query = (
                    "SELECT customer_id, customer_lastName, customer_firstName, join_date, cup_rental, deposit, cups_bought, account_value, user_name FROM customers_db WHERE user_name = "
                    + str(username)
                )
                df = pd.read_sql(query, connection)
                st.write(df)
                connection.close()
        except Exception as e:
            st.write("User not found")
            connection.close()

    elif selection == "Add/Update Customer Data":
        # Add/Update Customer Data Page
        # Use a form to update customer data
        with st.form("Customer Sign-up"):
            # Collect customer data inputs
            st.header("Add New Customer Data or Update Existing Customer Data")
            st.write("Please enter the new customer data below")
            customer_id = st.text_input("Customer ID")
            customer_lastName = st.text_input("Customer Last Name")
            customer_firstName = st.text_input("Customer First Name")
            customer_join_date = st.date_input("Join Date", today)
            deposit = st.text_input("Deposit", 5)
            account_value = st.text_input("Account Value", 0)
            submitted = st.form_submit_button("Submit")
            # Submit inputs with form button
            if submitted:
                # Consolidate user data
                user = {
                    "customer_id": customer_id,
                    "customer_firstName": first_name,
                    "customer_lastName": last_name,
                    "join_date": date.today(),
                    "deposit": deposit,
                    "account_value": account_value
                }
                # Run query
                try:
                    # check if customer_id already exists in customers_db
                    customerQuery = f"SELECT * FROM customers_db WHERE customer_id = {customer_id};"
                    customerResults = query(customerQuery)
                    # Add new user
                    if len(customerResults) == 0:
                        add_user(user)
                        st.write(
                            f"Congratulations {first_name} {last_name}!  You have signed-up for Cup Adventure!"
                        )
                        st.write(
                            "Thank you for joining us in reducing Cup Waste!")
                    # Update existing user
                    else:
                        update_user(user)
                        st.write(
                            f"{first_name} {last_name}'s information has been updated in the database.")
                except:
                    st.write(
                        "There was an error signing you up.  Please ensure no fields are blank."
                    )
