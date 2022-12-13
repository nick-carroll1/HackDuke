"""Create a database for Cup Adventure"""

import os
import mysql.connector
from datetime import date
import pandas as pd
from sqlalchemy import create_engine


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


def query(
    query,
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
    cursor.execute(f"USE {database}")
    cursor.execute(query)
    results = []
    for line in cursor:
        results.append(line)
    connection.close()
    return results


def add_user(
    user,
    database="cup_adventure",
    username=os.getenv("AWS_CUPADVENTURE_USERNAME"),
    passwd=os.getenv("AWS_CUPADVENTURE_PASSWORD"),
    hostname=os.getenv("AWS_CUPADVENTURE_HOSTNAME"),
    portnum=int(os.getenv("AWS_CUPADVENTURE_PORT")),
):
    # Create Connection
    connection = mysql.connector.connect(
        user=username, password=passwd, host=hostname, port=portnum
    )
    cursor = connection.cursor()
    cursor.execute(f"USE {database};")
    # Confirm user information is complete to create a new user
    userKeys = list(user.keys())
    assert set(userKeys) == {"customer_firstName", "customer_lastName", "join_date", "user_name", "password"}
    # Confirm username is unique
    cursor.execute(f"SELECT user_name FROM customers_db WHERE user_name = '{user['user_name']}';")
    users = set()
    for x in cursor:
        users.add(x[0])
    assert users == set()
    # Convert user information to a query
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
    # execute query
    try:
        cursor.execute(f"INSERT INTO customers_db ({columns}) VALUES ({values});")
        connection.commit()
    except:
        connection.rollback()
    connection.close()
    pass

# Rent a cup
def rent_cup(
    user,
    cup,
    database="cup_adventure",
    username=os.getenv("AWS_CUPADVENTURE_USERNAME"),
    passwd=os.getenv("AWS_CUPADVENTURE_PASSWORD"),
    hostname=os.getenv("AWS_CUPADVENTURE_HOSTNAME"),
    portnum=int(os.getenv("AWS_CUPADVENTURE_PORT")),
):
    # Create Connection
    connection = mysql.connector.connect(
        user=username, password=passwd, host=hostname, port=portnum
    )
    cursor = connection.cursor()
    cursor.execute(f"USE {database};")
    # execute query
    try:
        cursor.execute(f"UPDATE customers_db SET customer_status = '{cup}' WHERE user_name = '{user}';")
        cursor.execute(f"UPDATE cups_db SET cup_status = 'Borrowed' WHERE cup_id = {cup};")
        connection.commit()
    except:
        connection.rollback()
    connection.close()
    pass

# Return a cup
def return_cup(
    user,
    cup,
    database="cup_adventure",
    username=os.getenv("AWS_CUPADVENTURE_USERNAME"),
    passwd=os.getenv("AWS_CUPADVENTURE_PASSWORD"),
    hostname=os.getenv("AWS_CUPADVENTURE_HOSTNAME"),
    portnum=int(os.getenv("AWS_CUPADVENTURE_PORT")),
):
    # Create Connection
    connection = mysql.connector.connect(
        user=username, password=passwd, host=hostname, port=portnum
    )
    cursor = connection.cursor()
    cursor.execute(f"USE {database};")
    # execute query
    try:
        cursor.execute(f"UPDATE customers_db SET customer_status = 'Available' WHERE user_name = '{user}';")
        cursor.execute(f"UPDATE cups_db SET cup_status = 'Available' WHERE cup_id = {cup};")
        connection.commit()
    except:
        connection.rollback()
    connection.close()
    pass


# Update table
def update_table(
    dataframe,
    table,
    database="cup_adventure",
    username=os.getenv("AWS_CUPADVENTURE_USERNAME"),
    passwd=os.getenv("AWS_CUPADVENTURE_PASSWORD"),
    hostname=os.getenv("AWS_CUPADVENTURE_HOSTNAME"),
    portnum=int(os.getenv("AWS_CUPADVENTURE_PORT")),
):
    # Create Connection
    engine = create_engine(f"mysql://{username}:{passwd}@{hostname}:{portnum}/{database}")
    connection = engine.connect()
    # Update table
    try:
        dataframe.to_sql(
            table, connection, if_exists="replace", index=False
        )
        pass
    except:
        print(f"Error: {table} could not be updated in database")
    pass


if __name__ == "__main__":
    myuser = os.getenv("AWS_CUPADVENTURE_USERNAME")
    mypassword = os.getenv("AWS_CUPADVENTURE_PASSWORD")
    myhost = os.getenv("AWS_CUPADVENTURE_HOSTNAME")
    myport = int(os.getenv("AWS_CUPADVENTURE_PORT"))
    mydatabase = "cup_adventure"
    mytable = "customers_db"
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
    # myquery = "INSERT INTO customers (customer_firstName, customer_lastName, join_date) VALUES ('Jenny', 'Shen', '2022-12-02');"
    # myquery = "SELECT password FROM customers_db where user_name = 'ngift1';"
    # myquery = f"SELECT DISTINCT vendor_id, vendor_name FROM vendors_db;"
    # myquery = "SHOW TABLES;"
    # newUser = {"customer_firstName": "Noah", "customer_lastName": "Gift", "join_date": date.today().__str__(), "user_name": "ngift1", "password": "password7"}
    # createdb(mydatabase, myuser, mypassword, myhost, myport)
    # createTable(mytable, myparameters, mydatabase, myuser, mypassword, myhost, myport)
    # print(query(myquery, mydatabase, myuser, mypassword, myhost, myport))
    # add_user(newUser)
    updatedTable = pd.read_excel('customers_db.xlsx')
    update_table(updatedTable, mytable)
    
