import mysql.connector
from config import *

# Get Connection
def get_connection():
    connection = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return connection

# Execute Query
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

# View All
def fetch_all(query):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    connection.close()
    return data
# Insert Data
def insert_data(query, values):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()
    
# View One
def fetch_one(query, values):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(query, values)

    data = cursor.fetchone()

    cursor.close()
    connection.close()

    return data
# Update
def update_data(query, values):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query, values)
    connection.commit()

    affected_rows = cursor.rowcount

    cursor.close()
    connection.close()

    return affected_rows

# Delete
def delete_data(query, values):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query, values)
    connection.commit()

    affected_rows = cursor.rowcount

    cursor.close()
    connection.close()

    return affected_rows
# Transaction
def execute_transaction(queries):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        for query, values in queries:
            cursor.execute(query, values)

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()  

