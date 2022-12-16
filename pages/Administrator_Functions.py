import streamlit as st
import altair as alt
from datetime import date
from createdb import query, querydf, add_user, update_user, rent_cup, return_cup


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
        "Add/Update Customer Data",
        "Transactions"
    ],
)


def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        userquery = f"SELECT user_name, password FROM admin_db where user_name = '{st.session_state['username']}';"
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
# if check_password():
# if the user selects "Read Data" then show the table
if selection == "Welcome Page":
    st.write("Welcome to Cup Adventure Admin Page")
    st.write("Please select a page from the sidebar")

elif selection == "Read All Data":
    tableResults = query("SHOW TABLES")
    tables = [table[0] for table in tableResults]
    # create a streamlit selectbox to select the table
    table_name = st.selectbox("Select a table", tables)

    # query the database based on table_name selected and preserve the column names
    query = "SELECT * FROM " + table_name
    df = querydf(query)
    st.table(df)

    # create a streamlit selectbox to select the column
    column_name = st.selectbox("Select a column", df.columns)

    # make a summary statistics table of the selected column in horizontal format and integer format
    st.table(df[column_name].describe().to_frame().T)

# if the user selects "Add New Data" then show the form
elif selection == "Vendor Data":
    query_vendor_1 = "SELECT * FROM vendors_db"
    df_metric_1 = querydf(query_vendor_1)
    query_vendor_2 = "SELECT month(transaction_date) as Month, count(distinct vendor_id) as Active_Vendors FROM transactions_log WHERE transaction_status = 'Borrowed' GROUP BY month(transaction_date)"
    df_metric_2 = querydf(query_vendor_2)

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
    df_customer_1 = querydf(query_customer_1)
    query_customer_2 = "SELECT month(transaction_date) as Month, count(distinct customer_id) as active_user FROM transactions_log WHERE transaction_status = 'Borrowed' GROUP BY month(transaction_date)"
    df_customer_2 = querydf(query_customer_2)

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
elif selection == "Pull Customer Data":
    st.header("Pull User Data")
    st.write("Please enter the Customer ID below to pull the user data")
    # user_id = st.text_input("User ID", "")
    # if st.button("Pull Data"):
    #     query = "SELECT * FROM customers_db WHERE customer_id = " + user_id
    #     df = pd.read_sql(query, connection)
    #     st.write(df)
    # # give a choice of using user_name
    customer_id = st.text_input("Customer ID")
    try:
        if st.button("Pull Data"):
            customerQuery = (
                f"SELECT customer_id, customer_lastName, customer_firstName, join_date, cup_rental, deposit, cups_bought, account_value FROM customers_db WHERE customer_id = '{customer_id}'"
            )
            st.table(querydf(customerQuery))
    except Exception as err:
        st.write("Error searching for User.")
        st.write(err)

elif selection == "Add/Update Customer Data":
    # Add/Update Customer Data Page
    # Use a form to update customer data
    with st.form("Customer Sign-up2"):
        # Collect customer data inputs
        st.header("Add New Customer Data or Update Existing Customer Data")
        st.write("Please enter the new customer data below")
        customer_id = st.text_input("Customer ID")
        customer_lastName = st.text_input("Customer Last Name")
        customer_firstName = st.text_input("Customer First Name")
        customer_join_date = st.date_input("Join Date", date.today())
        deposit = st.text_input("Deposit", 5)
        account_value = st.text_input("Account Value", 0)
        submitted = st.form_submit_button("Submit")
        # Submit inputs with form button
        if submitted:
            # Consolidate user data
            user = {
                "customer_id": customer_id,
                "customer_firstName": customer_firstName,
                "customer_lastName": customer_lastName,
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
                        f"Congratulations {customer_firstName} {customer_lastName}!  You have signed-up for Cup Adventure!"
                    )
                    st.write(
                        "Thank you for joining us in reducing Cup Waste!")
                # Update existing user
                else:
                    update_user(user)
                    st.write(
                        f"{customer_firstName} {customer_lastName}'s information has been updated in the database.")
            except:
                st.write(
                    "There was an error signing you up.  Please ensure no fields are blank."
                )

#
elif selection == "Transactions":
    # Choose a transaction
    options = ["Rental", "Return", "Purchase"]
    transaction = st.selectbox("Please select a transaction", options)
    # Rental transaction
    if transaction == "Rental":
        vendorquery = f"SELECT DISTINCT vendor_id, vendor_name FROM vendors_db;"
        vendorresults = query(vendorquery)
        vendors = {'id': {eachVendor[1]: eachVendor[0] for eachVendor in vendorresults}, 'name': [eachVendor[1] for eachVendor in vendorresults]}
        vendor = st.selectbox("Please select a vendor", vendors['name'])
        with st.form("transactions"):
            cupquery = f"SELECT cup_id FROM cups_db WHERE sold = 'no' AND cup_status = 'Available' AND vendor_id = '{vendors['id'][vendor]}';"
            cupresults = query(cupquery)
            cups = [eachCup[0] for eachCup in cupresults]
            cup = st.selectbox("Please select a cup", cups)
            customerQuery = f"SELECT customer_id, customer_firstName, customer_lastName FROM customers_db WHERE cup_rental IS NULL;"
            customerResults = query(customerQuery)
            customer = st.selectbox("Please select a customer", customerResults)[0]
            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            st.write(submitted)
            if submitted:
                rent_cup(customer, vendor, cup)
                st.write("Thank you for renting your cup.")
    # Return transaction
    elif transaction == "Return":
        st.write("Use the dropdown below to rent your first cup.")
        with st.form("first_rental"):
            # First run, show inputs for username + password.
            vendorquery = f"SELECT DISTINCT vendor_id, vendor_name FROM vendors_db;"
            vendorresults = query(vendorquery)
            vendors = {'id': [eachVendor[0] for eachVendor in vendorresults], 'name': [eachVendor[1] for eachVendor in vendorresults]}
            vendor = st.selectbox("Please select a vendor", vendors['name'])
            cupquery = f"SELECT cup_id FROM cups_db WHERE sold = 'no' AND cup_status = 'Available';"
            cupresults = query(cupquery)
            cups = [eachCup[0] for eachCup in cupresults]
            cup = st.selectbox("Please select a cup", cups)
            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            st.write(submitted)
            if submitted:
                rent_cup(st.session_state['user info']['username'], vendor, cup)
                st.write("Thank you for renting your cup.")
                st.session_state['user info']['status'] = cup
    # Purchase transaction
    elif transaction == "Purchase":
        st.write("You currently have a cup borrowed.  Please return your cup when you are finished with it.")
        with st.form("return"):
            # First run, show inputs for username + password.
            vendorquery = f"SELECT DISTINCT vendor_name FROM vendors_db;"
            vendorresults = query(vendorquery)
            vendors = [eachVendor[0] for eachVendor in vendorresults]
            vendor = st.selectbox("Please select a vendor", vendors)
            cup = int(st.selectbox("Please select a cup", [st.session_state['user info']['status']]))
            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            st.write(submitted)
            if submitted:
                return_cup(st.session_state['user info']['username'], vendor, cup)
                st.write("Thank you for returning your cup.")
                st.session_state['user info']['status'] = "Available"
    else:
        st.write("There has been an error.  Please contact us for help.")