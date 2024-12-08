import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='swoldier.cv0qs42yqp2y.us-east-2.rds.amazonaws.com',
        user='cyberdudes',
        password='Cybi123!',
        port='3306',
        database='swoldier'
    )
