import mysql.connector

DB_USER = 'root'
DB_HOST = '127.0.0.1'
DB_PASS = 'pass'
DB_PORT = 3306
DB_DATABASE = 'food-truck'

cnx = mysql.connector.connect(
    user = DB_USER,
    host = DB_HOST,
    password = DB_PASS,
    port = DB_PORT,
    database = DB_DATABASE
)

cursor = cnx.cursor(dictionary=True)

def query_(query, data, cursor, cnx):
    if data:
        cursor.execute(query, data)
        cnx.commit()

def query_return(query, data, cursor, cnx):
    cursor.execute(query, data)
    result = list(cursor.fetchall())
    return result

def query_no_data(query, cursor, cnx):
    cursor.execute(query)
    result = list(cursor.fetchall())
    return result
