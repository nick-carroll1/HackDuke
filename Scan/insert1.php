
 <?php
    ini_set("display_errors", "1");
    ini_set("display_startup_errors", "1");
    error_reporting(E_ALL);

    SESSION_START();
    $server = "cupadventure.cus96lnhsxap.us-east-1.rds.amazonaws.com";
    $username="admin";
    $password="NoahGift706";
    $dbname="cup_adventure";

    $conn = mysqli_connect($server,$username,$password,$dbname);

    if(mysqli_connect_errno()){
       echo "Failed to connect to MySQL";
    }
    echo "Connected to MySQL successfully";

    if (isset($_POST['text'])) {
        $text = $_POST['text'];
        // $sql = "INSERT INTO transactions(STUDENTID,BORROW) VALUES ('$text',NOW())";
        // if ($conn->query($sql) === TRUE) {
        //     $_SESSION["success"] = "New record added successfully";
        // } else {
        //     $_SESSION["error"] = $conn->error;
        // }
        $date = date("Y-m-d H:i:s");
        $sql = "SELECT * FROM transactions WHERE STUDENTID = '$text' AND STATUS = '0'";
        $query = $conn->query($sql);
        if ($query->num_rows > 0) {
            $sql = "UPDATE transactions SET STATUS = '1', RETURNS = NOW() WHERE STUDENTID = '$text'";
            $query = $conn->query($sql);
            $_SESSION["success"] = "New return record added successfully";
        } else {
            $sql = "INSERT INTO transactions(STUDENTID,BORROW,RETURNS,STATUS) VALUES ('$text', NOW(),'','0')";
            if ($conn->query($sql) === TRUE){
                $_SESSION["success"] = "New borrow record added successfully";
            } else {
                $_SESSION["error"] = $conn->error;
            }
        }
    } else {
        $_SESSION["error"] = "Please scan your QR Code";
    }

        header("Location: index.php");
    
    $conn->close();
?>