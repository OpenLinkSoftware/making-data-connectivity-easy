import pyodbc

DSN_NAME = "VirtuosoODBC"
USERNAME = "dba"
PASSWORD = "dba"

connection_string = (
    f"DSN={DSN_NAME};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
)

try:
    conn = pyodbc.connect(connection_string, autocommit=True)
    cursor = conn.cursor()

    cursor.execute("SELECT 1")
    row = cursor.fetchone()

    print("Connected successfully. Test query returned:", row[0])

except pyodbc.Error as e:
    print("ODBC connection failed")
    print(e)

finally:
    try:
        cursor.close()
        conn.close()
    except Exception:
        pass