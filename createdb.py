"""Create a database for Cup Adventure"""

import os
import mysql.connector
from datetime import date
import pandas as pd
from sqlalchemy import create_engine
import numpy as np


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

# mySQL Query
def query(
    myQuery,
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
    cursor.execute(myQuery)
    results = []
    for line in cursor:
        results.append(line)
    connection.close()
    return results


# Query Dataframe
def querydf(
    myquery,
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
        return pd.read_sql(
            myquery, connection
        )
    except:
        return (f"Error: Query could not be executed")


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
    assert len({"customer_id", "customer_firstName", "customer_lastName", "join_date"}.difference(set(userKeys))) == 0
    # Confirm customer_id is unique
    cursor.execute(f"SELECT customer_id FROM customers_db WHERE customer_id = '{user['customer_id']}';")
    users = {x[0] for x in cursor}
    assert users == set()
    # Convert user information to a query
    columns = userKeys[0]
    if (type(user[userKeys[0]]) == type(str())) or (type(user[userKeys[0]]) == type(date.today())):
        values = "'" + user[userKeys[0]] + "'"
        pass
    else:
        values = str(user[userKeys[0]])
    if len(userKeys) > 1:
        for eachKey in userKeys[1:]:
            columns += ", " + eachKey
            eachValue = user[eachKey]
            if (type(eachValue) == type(str())) or (type(eachValue) == type(date.today())):
                values += ", '" + str(eachValue) + "'"
                pass
            else:
                values += ", " + str(eachValue)
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

# Update User Information
def update_user(
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
    assert set(userKeys) == {"customer_id", "customer_firstName", "customer_lastName", "join_date", "deposit", "account_value"}
    # Convert user information to a query
    iterator =  list(set(userKeys).difference({"customer_id"}))
    if (type(user[iterator[0]]) == type(str())) or (type(user[iterator[0]]) == type(date.today())):
        updateQuery = f"{iterator[0]} = '{user[iterator[0]]}'"
    else:
        updateQuery = f"{iterator[0]} = {user[iterator[0]]}"
    for eachKey in iterator[1:]:
        if (type(user[eachKey]) == type(str())) or (type(user[eachKey]) == type(date.today())):
            updateQuery += (f", {eachKey} = '{user[eachKey]}'")
        else:
            updateQuery += (f", {eachKey} = {user[eachKey]}")
    # execute query
    try:
        cursor.execute(f"UPDATE customers_db SET {updateQuery} WHERE customer_id = '{user['customer_id']}';")
        connection.commit()
    except:
        connection.rollback()
    connection.close()
    pass


# Rent a cup
def rent_cup(
    user,
    vendor,
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
    columnValues = ['order_id', 'transaction_date', 'customer_id', 'vendor_id', 'cup_id', 'transaction_status', 'Revenue']
    valueValues = [None, date.today().__str__(), user, vendor, cup, "Borrowed", 0]
    # Prepare and execute queries
    try:
        cursor.execute(f"SELECT MAX(order_id) + 1 FROM transactions_log;")
        valueValues[0] = [order_id for order_id in cursor][0][0]
        # Convert transaction information to a query
        columns = columnValues[0]
        for eachColumn in columnValues[1:]:
            columns += ", " + eachColumn
        if (type(valueValues[0]) == type(str())):
            values = "'" + valueValues[0] + "'"
            pass
        elif (type(valueValues[0]) == type(date.today())):
            values = "'" + str(valueValues[0]) + "'"
            pass
        else:
            values = str(valueValues[0])
        for eachValue in valueValues[1:]:
            if (type(eachValue) == type(str())):
                values += ", '" + eachValue + "'"
                pass
            elif (type(eachValue) == type(date.today())):
                values += ", '" + eachValue + "'"
                pass
            else:
                values += ", " + str(eachValue)
                pass
            pass
        cursor.execute(f"INSERT INTO transactions_log ({columns}) VALUES ({values});")
        cursor.execute(f"UPDATE customers_db SET cup_rental = '{cup}' WHERE customer_id = '{user}';")
        cursor.execute(f"UPDATE cups_db SET cup_status = 'Borrowed', vendor_id = 'Out' WHERE cup_id = {cup};")
        cursor.execute(f"UPDATE vendors_db SET cup_stock = cup_stock - 1 WHERE vendor_id = '{vendor}';")
        connection.commit()
    except Exception as err:
        connection.rollback()
        return err
    connection.close()
    pass


# Return a cup
def return_cup(
    user,
    vendor,
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
    columnValues = ['order_id', 'transaction_date', 'customer_id', 'vendor_id', 'cup_id', 'transaction_status', 'Revenue']
    valueValues = [None, date.today().__str__(), user, vendor, cup, "Returned", 0]
    # Prepare and execute queries
    try:
        cursor.execute(f"SELECT MAX(order_id) + 1 FROM transactions_log;")
        valueValues[0] = [order_id for order_id in cursor][0][0]
        # Convert transaction information to a query
        columns = columnValues[0]
        for eachColumn in columnValues[1:]:
            columns += ", " + eachColumn
        if (type(valueValues[0]) == type(str())):
            values = "'" + valueValues[0] + "'"
            pass
        elif (type(valueValues[0]) == type(date.today())):
            values = "'" + str(valueValues[0]) + "'"
            pass
        else:
            values = str(valueValues[0])
        for eachValue in valueValues[1:]:
            if (type(eachValue) == type(str())):
                values += ", '" + eachValue + "'"
                pass
            elif (type(eachValue) == type(date.today())):
                values += ", '" + eachValue + "'"
                pass
            else:
                values += ", " + str(eachValue)
                pass
            pass
        cursor.execute(f"INSERT INTO transactions_log ({columns}) VALUES ({values});")
        cursor.execute(f"UPDATE customers_db SET cup_rental = NULL WHERE customer_id = '{user}';")
        cursor.execute(f"UPDATE cups_db SET cup_status = 'Available', vendor_id = 'Out' WHERE cup_id = {cup};")
        cursor.execute(f"UPDATE vendors_db SET cup_stock = cup_stock + 1 WHERE vendor_id = '{vendor}';")
        connection.commit()
    except Exception as err:
        connection.rollback()
        return err
    connection.close()
    pass


# Purchase a cup
def purchase_cup(
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
    columnValues = ['order_id', 'transaction_date', 'customer_id', 'vendor_id', 'cup_id', 'transaction_status', 'Revenue']
    valueValues = [None, date.today().__str__(), user, 'CA1', cup, "Purchased", 5]
    # Prepare and execute queries
    try:
        cursor.execute(f"SELECT MAX(order_id) + 1 FROM transactions_log;")
        valueValues[0] = [order_id for order_id in cursor][0][0]
        # Convert transaction information to a query
        columns = columnValues[0]
        for eachColumn in columnValues[1:]:
            columns += ", " + eachColumn
        if (type(valueValues[0]) == type(str())):
            values = "'" + valueValues[0] + "'"
            pass
        elif (type(valueValues[0]) == type(date.today())):
            values = "'" + str(valueValues[0]) + "'"
            pass
        else:
            values = str(valueValues[0])
        for eachValue in valueValues[1:]:
            if (type(eachValue) == type(str())):
                values += ", '" + eachValue + "'"
                pass
            elif (type(eachValue) == type(date.today())):
                values += ", '" + eachValue + "'"
                pass
            else:
                values += ", " + str(eachValue)
                pass
            pass
        cursor.execute(f"INSERT INTO transactions_log ({columns}) VALUES ({values});")
        cursor.execute(f"UPDATE customers_db SET cups_bought = cups_bought + 1, account_value = account_value - 5 WHERE customer_id = '{user}';")
        cursor.execute(f"UPDATE vendors_db SET cup_stock = cup_stock - 1 WHERE vendor_id = (SELECT vendor_id FROM cups_db WHERE cup_id = {cup});")
        cursor.execute(f"UPDATE cups_db SET cup_status = 'Sold', vendor_id = 'Out', sold = 'Yes' WHERE cup_id = {cup};")
        connection.commit()
    except Exception as err:
        connection.rollback()
        return err
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
    myquery = f"SELECT * FROM vendors_db;"
    # myquery = f"SELECT MAX(order_id) + 1 FROM transactions_log;"
    # myquery = f"SELECT customer_id FROM customers_db WHERE user_name = '{user}';"
    # myquery = "SHOW TABLES;"
    # newUser = {"customer_id": 14050, "customer_firstName": "Noah", "customer_lastName": "Gift", "join_date": date.today()}
    # createdb(mydatabase, myuser, mypassword, myhost, myport)
    # createTable(mytable, myparameters, mydatabase, myuser, mypassword, myhost, myport)
    # print(query(myquery, mydatabase, myuser, mypassword, myhost, myport))
    print(querydf(myquery, mydatabase, myuser, mypassword, myhost, myport))
    # add_user(newUser)
    # updatedTable = pd.read_excel('raw_data/customers_db.xlsx')
    # update_table(updatedTable, mytable)
    # user1 = {"customer_id": 1, "customer_firstName": "Fred", "customer_lastName": "Astaire", "join_date": date.today(), "deposit": 5, "account_value": 0}
    # print(update_user(user1))
    
