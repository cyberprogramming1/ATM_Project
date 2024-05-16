import pyodbc

class Database:
    def __init__(self):
        self.conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=DESKTOP-VIKK52P;'
            'DATABASE=ATMDB;'
            'Trusted_Connection=yes;'
        )
        self.cursor = self.conn.cursor()
