import streamlit as st
import streamlit.components.v1 as components

st.title("Cup Adventure")
from PIL import Image
image = Image.open(r"images\banner.jpg")

st.image(image)
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