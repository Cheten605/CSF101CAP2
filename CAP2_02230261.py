#####################################################################################
#NAME: CHETEN DORJI
#DEPARTMENT: 1 MECHANICAL
#STUDENT NUMBER: 02230261
####################################################################################
#REFERENCES:
#ocs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files 
#https://www.youtube.com/watch?v=q2SGW2VgwAM
#https://youtu.be/wfcWRAxRVBA?si=oq_ByGWa4hACzP0G
#https://youtu.be/2TrDIbwasw8?si=PdxT23wQ99c4FvU8
######################################################################################
import random

class Account:
    def __init__(self, account_number, account_type, balance=0.0):
        self.account_number = account_number
        self.account_type = account_type
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def WITHDRAW(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        return self.balance

    def TRANSFER(self, amount, recipient_account):
        self.WITHDRAW(amount)
        recipient_account.deposit(amount)

class BUSINESSACC(Account):
    def __init__(self, account_number, balance=0.0):
        super().__init__(account_number, "Business", balance)

class PERSONALACC(Account):
    def __init__(self, account_number, balance=0.0):
        super().__init__(account_number, "Personal", balance)

class BANKINGSYSTEM:
    def __init__(self):
        self.accounts = {}
        self.load_accounts()

    def CREATE_ACC(self, account_type):
        account_number = self.GENERATE_ACC_NO()
        if account_type == "Business":
            account = BUSINESSACC(account_number)
        elif account_type == "Personal":
            account = PERSONALACC(account_number)
        else:
            raise ValueError("Invalid account type")

        password = self.GENERATE_PASSWORD()
        self.accounts[account_number] = {
            "account": account,
            "password": password
        }
        self.SAVE_ACC()
        return account_number, password

    def login(self, account_number, password):
        account_info = self.accounts.get(account_number)
        if account_info and account_info["password"] == password:
            return account_info["account"]
        else:
            raise ValueError("Invalid account number or password")

    def GENERATE_ACC_NO(self):
        return str(random.randint(100000, 999999))

    def GENERATE_PASSWORD(self):
        return str(random.randint(1000, 9999))

    def load_accounts(self):
        try:
            with open("accounts.txt", "r") as file:
                for line in file:
                    account_number, password, account_type, balance = line.strip().split(',')
                    balance = float(balance)
                    if account_type == "Business":
                        account = BUSINESSACC(account_number, balance)
                    elif account_type == "Personal":
                        account = PERSONALACC(account_number, balance)
                    else:
                        continue
                    self.accounts[account_number] = {
                        "account": account,
                        "password": password
                    }
        except FileNotFoundError:
            self.accounts = {}

    def SAVE_ACC(self):
        with open("accounts.txt", "w") as file:
            for account_number, account_info in self.accounts.items():
                account = account_info["account"]
                password = account_info["password"]
                file.write(f"{account_number},{password},{account.account_type},{account.balance}\n")

    def delete_account(self, account_number):
        if account_number in self.accounts:
            del self.accounts[account_number]
            self.SAVE_ACC()
        else:
            raise ValueError("Account does not exist")

def main():
    bank = BANKINGSYSTEM()

    while True:
        print("\nBanking System Menu")
        print("1. Open Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            account_type = input("Enter account type (Business/Personal): ")
            account_number, password = bank.CREATE_ACC(account_type)
            print(f"Account created. Account Number: {account_number}, Password: {password}")

        elif choice == "2":
            account_number = input("Enter account number: ")
            password = input("Enter password: ")
            try:
                account = bank.login(account_number, password)
                print(f"Logged in to account {account_number}.")

                while True:
                    print("\nAccount Menu")
                    print("1. Check Balance")
                    print("2. Deposit")
                    print("3. WITHDRAW")
                    print("4. TRANSFER")
                    print("5. Delete Account")
                    print("6. Logout")
                    sub_choice = input("Enter choice: ")

                    if sub_choice == "1":
                        print(f"Balance: {account.balance}")

                    elif sub_choice == "2":
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)
                        print(f"Deposited {amount}. New balance: {account.balance}")

                    elif sub_choice == "3":
                        amount = float(input("Enter amount to WITHDRAW: "))
                        try:
                            account.WITHDRAW(amount)
                            print(f"Withdrew {amount}. New balance: {account.balance}")
                        except ValueError as e:
                            print(e)

                    elif sub_choice == "4":
                        recipient_account_number = input("Enter recipient account number: ")
                        amount = float(input("Enter amount to TRANSFER: "))
                        try:
                            recipient_account = bank.accounts.get(recipient_account_number)["account"]
                            account.TRANSFER(amount, recipient_account)
                            print(f"TRANSFERred {amount} to account {recipient_account_number}. New balance: {account.balance}")
                        except ValueError as e:
                            print(e)
                        except TypeError:
                            print("Recipient account does not exist.")

                    elif sub_choice == "5":
                        bank.delete_account(account_number)
                        print(f"Account {account_number} deleted.")
                        break

                    elif sub_choice == "6":
                        print("Logged out.")
                        break

                    else:
                        print("Invalid choice. Try again.")

            except ValueError as e:
                print(e)

        elif choice == "3":
            print("Exiting the banking system.")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()


