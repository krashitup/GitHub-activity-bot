import pyodbc

def get_connection.py():
    """
    Establishes and returns a connection to the SQL Server database.
    """
    connection_string = (
        "Driver={ODBC Driver 17 for SQL Server};"
        'localhost\SQLEXPRESS'
        "Database=GitActivityDB;"
        "Trusted_Connection=yes;"
    )
    
    connection = pyodbc.connect(connection_string)
    
    return connection