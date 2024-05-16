from getpass import getpass

class User:
    def __init__(self, db, user_id, username, pin):
        self.db = db
        self.user_id = user_id
        self.username = username
        self.pin = pin
    
    @staticmethod
    def authenticate(db):
        username = input("Enter username: ")
        pin = getpass("Enter PIN: ")

        print(f"Debug: Entered username - {username}")
        print(f"Debug: Entered PIN - {pin}")

        query = "SELECT * FROM Users WHERE username = ? AND pin = ?"
        print(f"Debug: SQL Query - {query}")

        db.cursor.execute(query, (username, pin))
        user_data = db.cursor.fetchone()

        if user_data:
            print("Authentication successful")
            return User(db, user_data[0], user_data[1], user_data[2])
        else:
            print("Authentication failed")
            return None

    def change_pin(self):
        new_pin = getpass("Enter new PIN: ")
        query = "UPDATE Users SET pin = ? WHERE id = ?"
        self.db.cursor.execute(query, (new_pin, self.user_id))
        self.db.conn.commit()
        print("PIN changed successfully.")
