import pyodbc

def get_db_connection():
    conn = pyodbc.connect(
        'Driver={ODBC Driver 18 for SQL Server};'
        'Server=localhost\\SQLEXPRESS;'
        'Database=GitActivityDB;'
        'Trusted_Connection=yes;'
        'Encrypt=no;'
        'TrustServerCertificate=yes;',
        timeout=5
    )
    return conn
