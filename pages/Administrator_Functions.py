import streamlit as st
import altair as alt
from datetime import date
from createdb import query, querydf, add_user, update_user, rent_cup, return_cup, purchase_cup


# make a sidebar with choice of different pages named "Read Data" and "Add New Data"
st.sidebar.title("Navigation")
selection = st.sidebar.radio(
    "Go to",
    [
        "Welcome Page",
        "Read All Data",
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
        st.write(userquery)
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
st.write(st.session_state)
if check_password():
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
    # User selects Pull Customer Data
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
            with st.form("rental"):
                cupquery = f"SELECT cup_id FROM cups_db WHERE sold = 'no' AND cup_status = 'Available' AND vendor_id = '{vendors['id'][vendor]}';"
                cupresults = query(cupquery)
                cups = [eachCup[0] for eachCup in cupresults]
                cup = st.selectbox("Please select a cup", cups)
                customerQuery = f"SELECT customer_id, customer_firstName, customer_lastName FROM customers_db WHERE cup_rental IS NULL;"
                customerResults = query(customerQuery)
                customer = st.selectbox("Please select a customer", customerResults)[0]
                # Every form must have a submit button.
                submitted = st.form_submit_button("Submit")
                if submitted:
                    try:
                        rent_cup(customer, vendors['id'][vendor], cup)
                        st.write("Thank you for renting this cup.")
                    except:
                        st.write("There was an error renting your cup.")
        # Return transaction
        elif transaction == "Return":
            st.write("Use the dropdown below to return a cup.")
            customerQuery = f"SELECT customer_id, customer_firstName, customer_lastName, cup_rental FROM customers_db WHERE cup_rental IS NOT NULL;"
            customerResults = query(customerQuery)
            customer = st.selectbox("Please select a customer", customerResults)
            customer_id = customer[0]
            cup = customer[3]
            with st.form("return"):
                # First run, show inputs for username + password.
                st.write(f"{customer[1]} {customer[2]} has cup {cup} to return.")
                vendorquery = f"SELECT DISTINCT vendor_id, vendor_name FROM vendors_db;"
                vendorresults = query(vendorquery)
                vendors = {'id': {eachVendor[1]: eachVendor[0] for eachVendor in vendorresults}, 'name': [eachVendor[1] for eachVendor in vendorresults]}
                vendor = st.selectbox("Please select a vendor to return the cup", vendors['name'])
                # Every form must have a submit button.
                submitted = st.form_submit_button("Submit")
                if submitted:
                    try:
                        return_cup(customer_id, vendors['id'][vendor], cup)
                        st.write("Thank you for returning the cup.  We hope you contine to use Cup Adventure.")
                    except:
                        st.write("There was an error renting your cup.")
        # Purchase transaction
        elif transaction == "Purchase":
            st.write("Use the dropdown below to purchase a cup.")
            customerQuery = f"SELECT customer_id, customer_firstName, customer_lastName, cup_rental FROM customers_db WHERE cup_rental IS NOT NULL;"
            customerResults = query(customerQuery)
            customer = st.selectbox("Please select a customer", customerResults)
            customer_id = customer[0]
            with st.form("purchase"):
                cupquery = f"SELECT cup_id FROM cups_db WHERE sold = 'no' AND cup_status = 'Available';"
                cupresults = query(cupquery)
                cups = [eachCup[0] for eachCup in cupresults]
                cups.append(customer[3])
                cup = st.selectbox("Please select a cup", cups)
                # Every form must have a submit button.
                submitted = st.form_submit_button("Submit")
                st.write(submitted)
                if submitted:
                    try:
                        cat = purchase_cup(customer_id, cup)
                        st.write("Thank you for purchasing this cup.")
                        st.write(cat)
                    except:
                        st.write("There has been an error in this purchase.")
        else:
            st.write("There has been an error.  Please contact us for help.")