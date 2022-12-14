import streamlit as st
import streamlit.components.v1 as components
import os

components.html(
    """<?php SESSION_START(); ?>
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
                    <?php
                        if(isset($_SESSION['error'])){
                        echo "
                            <div class='alert alert-danger'>
                            <h4>Error!</h4>
                            ".$_SESSION['error']."
                            </div>
                        ";
                        }

                        if(isset($_SESSION['success'])){
                        echo "
                            <div class='alert alert-success alert-dismissible' style='background:green;color:#fff'>
                            <h4>Success!</h4>
                            ".$_SESSION['success']."
                            </div>
                        ";
                        unset($_SESSION['success']);
                        }
				  ?>
                </div>
                <div class = "col-md-6">
                <form action = "../Scan/insert1.php" method = "post" name = "form1" id = "form1" class = "form-horizontal">
                    <label>SCAN QR CODE</label>
                    <input type = "text" name = "text" id = "text" readonyy = "" placeholder = "scan the QR Code" class = "form-control">
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
                    <tbody>"""+f"""
                        <?php
                        $server = {os.getenv("AWS_CUPADVENTURE_HOSTNAME")};
                        $username={os.getenv("AWS_CUPADVENTURE_USERNAME")};
                        $password={os.getenv("AWS_CUPADVENTURE_PASSWORD")};
                        $dbname="cup_adventure";"""+"""
                    
                        $conn = new mysqli($server,$username,$password,$dbname);
						$date = date("Y-m-d H:i:s");
                        if($conn->connect_error){
                            die("Connection failed" .$conn->connect_error);
                        }
                           $sql ="SELECT * FROM transactions";
                           $query = $conn->query($sql);
                           while ($row = $query->fetch_assoc()){
                        ?>
                            <tr>
                                <td><?php echo $row['ID'];?></td>
                                <td><?php echo $row['STUDENTID'];?></td>
                                <td><?php echo $row['BORROW'];?></td>
                                <td><?php echo $row['RETURNS'];?></td>
                                <td><?php echo $row['STATUS'];?></td>
                            </tr>
                        <?php
                        }
                        ?>
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
                document.getElementById('text').value = c;
                document.forms["form1"].submit();
            });
        
        
        </script>
    </body>
</html>""", width = 900, height = 900, scrolling= True
)