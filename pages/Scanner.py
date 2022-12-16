import streamlit as st
from PIL import Image


image = Image.open("images/bar_code.PNG")

# displaying the image on streamlit app
st.image(image, caption="Please Click the Button Below")


def get_st_button_a_tag(url_link, button_name):
    """
    generate html a tag
    :param url_link:
    :param button_name:
    :return:
    """
    return f"""
    <a href={url_link}><button style="
    fontWeight: 400;
    padding: 0.25rem 0.75rem;
    borderRadius: 0.25rem;
    margin: 0px;
    lineHeight: 1.6;
    width: auto;
    userSelect: none;
    backgroundColor: #abd5c5;
    border: 1px solid rgba(49, 51, 63, 0.2);">{button_name}</button></a>
    """


col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    pass
with col2:
    pass
with col4:
    pass
with col5:
    pass
with col3:
    st.markdown(
        get_st_button_a_tag("http://cupsadventure.tech/", "QR Code Scanner"),
        unsafe_allow_html=True,
    )
