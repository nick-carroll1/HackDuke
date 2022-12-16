import streamlit as st
import streamlit.components.v1 as components
import os

import mysql.connector

# server = "localhost"
# username="root"
# password=""
# dbname="qrcodedb"


def add_record():

    text = str(st.session_state.textbox)

    cnx = mysql.connector.connect(
        host="cupadventure.cus96lnhsxap.us-east-1.rds.amazonaws.com",
        user="admin",
        password="NoahGift706-2",
        database="cup_adventure",
    )

    cur = cnx.cursor(buffered=True)

    # st.write("aaaaa")
    # try:
    #    text = st.experimental_get_query_params()["text"][0]
    #    #st.write("text is: " + text)
    # except:
    #    text = ""
    # st.write("no text submitted")
    cur.execute(
        "SELECT * FROM transactions WHERE STUDENTID = %s AND STATUS = '0'", (text,)
    )
    # date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    if cur.rowcount > 0:
        cur.execute(
            "UPDATE transactions SET STATUS = '1', RETURNS = NOW() WHERE STUDENTID = %s",
            (text,),
        )
        # st.success("New return record added successfully")
    else:
        cur.execute(
            "INSERT INTO transactions(STUDENTID,BORROW,RETURNS,STATUS) VALUES (%s, NOW(),'','0')",
            (text,),
        )
    # st.success("New borrow record added successfully")


cnx = mysql.connector.connect(
    host="cupadventure.cus96lnhsxap.us-east-1.rds.amazonaws.com",
    user="admin",
    password="NoahGift706-2",
    database="cup_adventure",
)

cur = cnx.cursor(buffered=True)
cur.execute("SELECT * FROM transactions")
result = cur.fetchall()

html = ""
for row in result:
    html += f"""
    <tr>
        <td>{row[0]}</td>
        <td>{row[1]}</td>
        <td>{row[2]}</td>
        <td>{row[3]}</td>
        <td>{row[4]}</td>
    </tr>
    """

st.write("hello222222222")
st.session_state["c"] = ""
st.write(st.session_state)

input = st.text_input("textbox", key="textbox", on_change=add_record)

a = components.html(
    """
<html>
    <head>  
    <script type = "text/javascript" src = "https://cdnjs.cloudflare.com/ajax/libs/webrtc-adapter/3.3.3/adapter.min.js"></script>
    <script type = "text/javascript" src = "https://cdnjs.cloudflare.com/ajax/libs/vue/2.1.10/vue.min.js"></script>
    <script type = "text/javascript" src = "https://rawgit.com/schmich/instascan-builds/master/instascan.min.js"></script>
    <link rel = "stylesheet" href = "https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    </head>
    <body>
        <div class = "container">
            <div class = "row">
                <div class = "col-md-6">
                    <video id = "preview" width = "100%"></video>
                </div>
                <div class = "col-md-6">"""
    + input
    + f"""
                <form action = "Scan" method = "get" name = "form1" id = "form1" class = "form-horizontal">"""
    + """
                    <label>SCAN QR CODE</label>
                    <input type = "text" name = "text222" id = "text222" readonyy = "" placeholder = "scan the QR Code" class = "form-control">
                </form>
                  <table class="table table-bordered">

                  <thead>
                        <tr>
                            <td>ID</td>
                            <td>Student ID</td>
                            <td>Borrow</td>
                            <td>Return</td>
                            <td>Status</td>
                        </tr>
                    </thead>
                    <tbody>"""
    + html
    + """
                    </tbody>
                </table>
            </div>
        </div>

        <script>
            let scanner = new Instascan.Scanner({ video: document.getElementById('preview') });
            Instascan.Camera.getCameras().then(function (cameras) {
                if (cameras.length > 0) {
                    scanner.start(cameras[0]);
                } else {
                    console.error('No cameras found.');
                }
            }).catch(function (e) {
                console.error(e);
            });

            scanner.addListener('scan', function (c) {
                document.getElementById('textbox').value = c;
                //document.forms["form1"].submit();
           
            });
        
        
        </script>
    </body>
</html>""",
    width=900,
    height=1500,
    scrolling=True,
)

st.write(st.session_state["c"])
st.write("hello")
st.write(st.session_state)
all_variables = dir()
html_variables = dir(a)
st.write(all_variables)
st.write(html_variables.text_input())
