from user import User
from account import Account
from database import Database

class ATM:
    def __init__(self):
        self.db = Database()
        self.user = None
        self.account = None

    def main_menu(self):
        self.user = User.authenticate(self.db)
        if self.user:
            self.account = Account(self.db, self.user)
            while True:
                print("\n1. Balance Inquiry")
                print("2. Cash Withdrawal")
                print("3. Cash Deposit")
                print("4. Manat Transfer")
                print("5. Mini Statement")
                print("6. Change PIN")
                print("7. Exit")
                choice = input("Choose an option: ")

                if choice == '1':
                    self.account.balance_inquiry()
                elif choice == '2':
                    self.account.cash_withdrawal()
                elif choice == '3':
                    self.account.cash_deposit()
                elif choice == '4':
                    self.account.fund_transfer()
                elif choice == '5':
                    self.account.mini_statement()
                elif choice == '6':
                    self.user.change_pin()
                elif choice == '7':
                    break
                else:
                    print("Invalid choice, please try again.")
