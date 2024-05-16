from decimal import Decimal, getcontext
from user import User

class Account:
    def __init__(self, db, user):
        self.db = db
        self.user = user
        self.balance = self.get_balance()
    
    def get_balance(self):
        query = "SELECT balance FROM Accounts WHERE user_id = ?"
        self.db.cursor.execute(query, (self.user.user_id,))
        result = self.db.cursor.fetchone()

        if result is not None:
            return Decimal(result[0])  # Convert balance to Decimal
        else:
            raise Exception("User data not found in Accounts table")

    def update_balance(self, new_balance):
        query = "UPDATE Accounts SET balance = ? WHERE user_id = ?"
        self.db.cursor.execute(query, (new_balance, self.user.user_id))
        self.db.conn.commit()
        self.balance = Decimal(new_balance)  # Update balance as Decimal

    def balance_inquiry(self):
        print(f"Your balance is: ${self.balance:.2f}")

    def cash_withdrawal(self):
        amount = Decimal(input("Enter amount to withdraw: "))  # Convert input to Decimal
        if amount > self.balance:
            print("Insufficient manats")
        else:
            new_balance = self.balance - amount
            self.update_balance(new_balance)
            self.record_transaction('withdrawal', amount)
            print(f"Withdrawal successful. New balance: ${new_balance:.2f}")


    def cash_deposit(self):
        amount = Decimal(input("Enter amount to deposit: "))  # Convert input to Decimal
        new_balance = self.balance + amount  # Perform arithmetic with Decimal objects
        self.update_balance(new_balance)
        self.record_transaction('deposit', amount)
        print(f"Deposit successful. New balance: ${new_balance:.2f}")

    def fund_transfer(self):
        recipient_username = input("Enter recipient username: ")
        amount = Decimal(input("Enter amount to transfer: "))  # Convert input to Decimal

        # Check if the transfer amount is valid (positive and within balance)
        if amount <= 0:
            print("Invalid transfer amount. Please enter a positive value.")
            return

        if amount > self.balance:
            print("Insufficient funds to transfer.")
            return

        recipient_account = self.find_user_account(recipient_username)

        if recipient_account is not None:
            recipient_new_balance = recipient_account.balance + amount
            recipient_account.update_balance(recipient_new_balance)

            sender_new_balance = self.balance - amount
            self.update_balance(sender_new_balance)

            self.record_transaction('transfer_out', amount)
            recipient_account.record_transaction('transfer_in', amount)

            print(f"Transfer successful. New balance: ${sender_new_balance:.2f}")
        else:
            print(f"Recipient '{recipient_username}' not found.")

    def find_user_account(self, username):
        query = "SELECT id FROM Users WHERE username = ?"
        print(f"Debug: SQL Query - {query} with username {username}")  # Debug statement
        self.db.cursor.execute(query, (username,))
        result = self.db.cursor.fetchone()

        if result is not None:
            recipient_user_id = result[0]  # Extract user_id from the result tuple
            print(f"Debug: Found user_id - {recipient_user_id}")  # Debug statement
            return Account(self.db, self.user)  # Create Account instance for recipient
        else:
            print("Debug: User not found")  # Debug statement
            return None
        
    def mini_statement(self):
        query = "SELECT transaction_type, amount, timestamp FROM Transactions WHERE user_id = ? ORDER BY timestamp DESC LIMIT 10"
        self.db.cursor.execute(query, (self.user.user_id,))
        transactions = self.db.cursor.fetchall()
        
        if transactions:
            print("Recent Transactions:")
            for trans in transactions:
                transaction_type = trans[0]
                amount = Decimal(trans[1])  # Convert amount to Decimal
                timestamp = trans[2]
                print(f"{timestamp} - {transaction_type}: ${amount:.2f}")
        else:
            print("No transactions found.")

    def record_transaction(self, transaction_type, amount):
        amount_decimal = Decimal(amount)  # Convert amount to Decimal
        query = "INSERT INTO Transactions (user_id, transaction_type, amount) VALUES (?, ?, ?)"
        self.db.cursor.execute(query, (self.user.user_id, transaction_type, amount_decimal))
        self.db.conn.commit()