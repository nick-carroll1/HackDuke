import streamlit as st
import streamlit.components.v1 as components
import os

import mysql.connector

# server = "localhost"
# username="root"
# password=""
# dbname="qrcodedb"


# def add_record():

try:
    text = st.experimental_get_query_params()["text"][0]
except:
    text = ""

if text:

    cnx = mysql.connector.connect(
        host="AWS_CUPADVENTURE_HOSTNAME",
        user="AWS_CUPADVENTURE_USERNAME",
        password="AWS_CUPADVENTURE_PASSWORD",
        database="cup_adventure",
        autocommit=True,
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

    cnx.close()
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


# input = st.text_input("textbox", key="textbox", on_change=add_record)

a = components.html(
    """
    <script type = "text/javascript" src = "https://cdnjs.cloudflare.com/ajax/libs/webrtc-adapter/3.3.3/adapter.min.js"></script>
    <script type = "text/javascript" src = "https://cdnjs.cloudflare.com/ajax/libs/vue/2.1.10/vue.min.js"></script>
    <script type = "text/javascript" src = "https://rawgit.com/schmich/instascan-builds/master/instascan.min.js"></script>
    <link rel = "stylesheet" href = "https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">

        <div class = "container">
            <div class = "row">
                <div class = "col-md-6">
                    <video id = "preview" width = "100%"></video>
                </div>
                <div class = "col-md-6">
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

        <form name="form1" action="Scan" method="get" style="display:none;">
            <input id="text" type="text" name="text" />
        </form>
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
                document.getElementById('text').value = c;
                document.forms["form1"].submit();
           
            });
        
        
        </script>
""",
    width=900,
    height=1500,
    scrolling=True,
)
