import mysql.connector
from config import *

def get_connection():
    connection = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return connection


def execute_query(query, values=None):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)

    connection.commit()

    cursor.close()
    connection.close()


def fetch_all(query):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    connection.close()
    return data
def insert_data(query, values):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()
    

def fetch_one(query, values):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(query, values)

    data = cursor.fetchone()

    cursor.close()
    connection.close()

    return data
    