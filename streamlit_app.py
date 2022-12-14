import streamlit as st
import streamlit.components.v1 as components
from createdb import query, rent_cup, return_cup


def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        userquery = f"SELECT user_name, password FROM customers_db where user_name = '{st.session_state['username']}';"
        results = query(userquery)
        passwords = {eachLine[0]: eachLine[1] for eachLine in results}
        st.write(passwords)
        st.write((st.session_state["username"] in passwords.keys())
            and (st.session_state["password"]
            == passwords[st.session_state["username"]]))
        if (
            (st.session_state["username"] in passwords.keys())
            and (st.session_state["password"]
            == passwords[st.session_state["username"]])
        ):
            st.write("I am Here")
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
    if "user info" not in st.session_state:
        userquery = f"SELECT customer_firstName, user_name, cup_rental FROM customers_db where user_name = '{st.session_state['username']}';"
        results = query(userquery)
        userInfo = {'firstName': results[0][0], 'username': results[0][1], 'status': results[0][2]}
        st.session_state['user info'] = userInfo
    if "user info" in st.session_state:
        st.write(f"Welcome {st.session_state['user info']['firstName']}")
        if st.session_state['user info']['status'] == "Available":
            st.write("If you would like to rent a cup, please use the dropdown below.")
            with st.form("rental"):
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
                    rent_cup(st.session_state['user info']['username'], cup)
                    st.write("Thank you for renting your cup.")
                    st.session_state['user info']['status'] = cup
        elif st.session_state['user info']['status'] == None:
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
                    rent_cup(st.session_state['user info']['username'], cup)
                    st.write("Thank you for renting your cup.")
                    st.session_state['user info']['status'] = cup
        elif st.session_state['user info']['status'] != "Available":
            st.write("You currently have a cup borrowed.  Please return your cup when you are finished with it.")
            with st.form("return"):
                # First run, show inputs for username + password.
                vendorquery = f"SELECT vendor_name FROM vendors_db;"
                vendorresults = query(vendorquery)
                vendors = [eachVendor[0] for eachVendor in vendorresults]
                st.selectbox("Please select a vendor", vendors)
                st.selectbox("Please select a cup", [st.session_state['user info']['status']])
                # Every form must have a submit button.
                submitted = st.form_submit_button("Submit")
                st.write(submitted)
                if submitted:
                    return_cup(st.session_state['user info']['username'], cup)
                    st.write("Thank you for returning your cup.")
                    st.session_state['user info']['status'] = "Available"
        else:
            st.write("There has been an error tracking your last cup.  Please contact us for help.")
        

def cup_rental():
    st.write("Thank you for renting your cup.")



