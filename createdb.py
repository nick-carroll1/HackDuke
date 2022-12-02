"""Create a database for Cup Adventure"""

import os
import mysql.connector
from datetime import date


def createdb(
    database,
    username=os.getenv("AWS_CUPADVENTURE_USERNAME"),
    passwd=os.getenv("AWS_CUPADVENTURE_PASSWORD"),
    hostname=os.getenv("AWS_CUPADVENTURE_HOSTNAME"),
    portnum=int(os.getenv("AWS_CUPADVENTURE_PORT")),
):
    connection = mysql.connector.connect(
        user=username, password=passwd, host=hostname, port=portnum
    )
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    connection.close()
    pass


def createTable(
    table,
    parameters,
    database="cup_adventure",
    username=os.getenv("AWS_CUPADVENTURE_USERNAME"),
    passwd=os.getenv("AWS_CUPADVENTURE_PASSWORD"),
    hostname=os.getenv("AWS_CUPADVENTURE_HOSTNAME"),
    portnum=int(os.getenv("AWS_CUPADVENTURE_PORT")),
):
    connection = mysql.connector.connect(
        user=username, password=passwd, host=hostname, port=portnum
    )
    tableParameters = "( " + parameters[0]
    if len(parameters) > 1:
        for eachParameter in parameters[1:]:
            tableParameters += ", " + eachParameter
            pass
        pass
    tableParameters += " )"
    cursor = connection.cursor()
    cursor.execute(f"USE {database}")
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} {parameters}")
    connection.close()
    pass


def query(query, database, username, passwd, hostname, portnum):
    connection = mysql.connector.connect(
        user=username, password=passwd, host=hostname, port=portnum
    )
    cursor = connection.cursor()
    cursor.execute(f"USE {database}")
    cursor.execute(query)
    for x in cursor:
        print(x)
    connection.close()
    pass


def add_user(
    user,
    database="cup_adventure",
    username=os.getenv("AWS_CUPADVENTURE_USERNAME"),
    passwd=os.getenv("AWS_CUPADVENTURE_PASSWORD"),
    hostname=os.getenv("AWS_CUPADVENTURE_HOSTNAME"),
    portnum=int(os.getenv("AWS_CUPADVENTURE_PORT")),
):
    connection = mysql.connector.connect(
        user=username, password=passwd, host=hostname, port=portnum
    )
    cursor = connection.cursor()
    cursor.execute(f"USE {database};")
    userKeys = list(user.keys())
    columns = userKeys[0]
    if type(user[userKeys[0]]) == str:
        values = "'" + user[userKeys[0]] + "'"
        pass
    else:
        values = user[userKeys[0]]
    if len(userKeys) > 1:
        for eachKey in userKeys[1:]:
            columns += ", " + eachKey
            eachValue = user[eachKey]
            if type(eachValue) == str:
                values += ", '" + eachValue + "'"
                pass
            else:
                values += ", " + eachValue
                pass
            pass
        pass
    try:
        cursor.execute(f"INSERT INTO customers ({columns}) VALUES ({values});")
        connection.commit()
    except:
        connection.rollback()
    # print(f"INSERT INTO customers ({columns}) VALUES ({values});")
    connection.close()
    pass


if __name__ == "__main__":
    myuser = os.getenv("AWS_CUPADVENTURE_USERNAME")
    mypassword = os.getenv("AWS_CUPADVENTURE_PASSWORD")
    myhost = os.getenv("AWS_CUPADVENTURE_HOSTNAME")
    myport = int(os.getenv("AWS_CUPADVENTURE_PORT"))
    mydatabase = "cup_adventure"
    mytable = "customers"
    myparameters = [
        "customer_id INT NOT NULL AUTO_INCREMENT",
        "customer_lastName varchar(255) NOT NULL",
        "customer_firstName varchar(255)",
        "customer_status varchar(15)",
        "join_date date",
        "buy_cup bool",
        "deposit float",
        "primary key (customer_id)",
    ]
    myquery = "INSERT INTO customers (customer_firstName, customer_lastName, join_date) VALUES ('Jenny', 'Shen', '2022-12-02');"
    newUser = {"customer_firstName": "Jenny", "customer_lastName": "Shen", "join_date": date.today().__str__()}
    # createdb(mydatabase, myuser, mypassword, myhost, myport)
    # createTable(mytable, myparameters, mydatabase, myuser, mypassword, myhost, myport)
    # query(myquery, mydatabase, myuser, mypassword, myhost, myport)
    add_user(newUser)
