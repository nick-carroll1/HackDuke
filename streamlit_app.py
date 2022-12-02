import streamlit as st
import streamlit.components.v1 as components
# import streamlit_authenticator as stauth
import subprocess

st.write(subprocess.check_output(['pip', 'freeze']))

# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['preauthorized']
# )

# with open('../config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)

# name, authentication_status, username = authenticator.login('Login', 'main')

# if authentication_status:
#     authenticator.logout('Logout', 'main')
#     st.title("Cup Adventure")
#     st.write(f'Welcome *{name}*')
#     st.write(config['credentials'])
# elif authentication_status == False:
#     st.error('Username/password is incorrect')
# elif authentication_status == None:
#     st.warning('Please enter your username and password')

# from PIL import Image
# image = Image.open(r"images\banner.jpg")

# st.image(image)
# st.image("images\logo.jpg")
# st.image(r"images\banner.jpg")

# st.subheader("Previous Code")
# HTMLFile = open('hack.html', 'r', encoding='utf-8')
# sourceCode = HTMLFile.read()
# components.html(sourceCode)

# st.subheader("Website Code")
# HTMLFile = open('final_form_website.html', 'r', encoding='utf-8')
# sourceCode = HTMLFile.read()
# components.html(sourceCode)