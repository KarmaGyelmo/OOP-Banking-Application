class BankAccount:
    def __init__(self, accountNumber, accountType, balance=0.0):
        self.accountNumber = accountNumber                          #This is like a unique ID for your account, kind of like your fingerprint in the bank's system.
        self.balance = balance                                      
        self.accountType = accountType                              

    def deposit(self, amount):                                     # Like adding more flour to the dough, this lets you add money to your account.
        self.balance += amount                                      

    def withdraw(self, amount):                                     #This is like taking some dough out. You can take money out, but only if you have enough (flour) in the account.
        if self.balance >= amount:                                  
            self.balance -= amount
            return True
        else:
            print("Insufficient Funds")
            return False

    def transfer(self, recipient, amount):                          #This is like sharing your dough with a friend's recipe (another account). You can send money to someone else's account, but again, only if you have enough.
        if self.withdraw(amount):
            recipient.deposit(amount)
            return True
        else:
            return False

class SavingsAccount(BankAccount):
    def __init__(self, accountNumber, balance=0.0):                 
        super().__init__(accountNumber, "Savings", balance)

class BusinessAccount(BankAccount):
    def __init__(self, accountNumber, balance=0.0):
        super().__init__(accountNumber, "Business", balance)

def create_account():
    accountNumber = generate_account_number()
    accountType = input("Enter Account Type (Savings/Business): ").lower()  # Convert input to lowercase
    balance = float(input("Enter Initial Balance: "))
    if accountType == "savings":
        account = SavingsAccount(accountNumber, balance)
    elif accountType == "business":
        account = BusinessAccount(accountNumber, balance)
    else:
        print("Invalid Account Type")
        return None
    save_account_details(account)
    print(f"Account Created Successfully! Account Number: {accountNumber}")
    return account

def generate_account_number():
    # Implement logic to generate a unique account number (e.g., random string)
    return "1234567890"  # Placeholder for actual generation

def save_account_details(account):
    with open("accounts.txt", "a") as file:
        file.write(f"{account.accountNumber},{account.accountType},{account.balance}\n")

def load_accounts():
    accounts = []
    try:
        with open("accounts.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                accountNumber, accountType, balance = data
                if accountType == "Savings":
                    account = SavingsAccount(accountNumber, float(balance))
                elif accountType == "Business":
                    account = BusinessAccount(accountNumber, float(balance))
                accounts.append(account)
    except FileNotFoundError:
        open("accounts.txt", "w").close()  # Create file if not found
    except ValueError:
        print("Error loading accounts. Data format is incorrect.")
    return accounts

def login():
    accountNumber = input("Enter Account Number: ")
    accounts = load_accounts()
    for account in accounts:
        if account.accountNumber == accountNumber:
            return account
    print("Invalid Account Number")
    return None

def manage_account(account):
    while True:
        print("\nMenu:")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer Money")
        print("5. Delete Account")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            print(f"Your Balance: ${account.balance}")

        elif choice == "2":
            amount = float(input("Enter Deposit Amount: "))
            account.deposit(amount)
            print(f"Deposit Successful! New Balance: ${account.balance}")
            save_account_details(account)

        elif choice == "3":
            amount = float(input("Enter Withdrawal Amount: "))
            if account.withdraw(amount):
                print(f"Withdrawal Successful! New Balance: ${account.balance}")
                save_account_details(account)

        elif choice == "4":
            recipientAccountNumber = input("Enter Recipient Account Number: ")
            recipientAccount = find_account(recipientAccountNumber)
            if recipientAccount:
                amount = float(input("Enter Transfer Amount: "))
                if account.transfer(recipientAccount, amount):
                    print(f"Transfer Successful! New Balance: ${account.balance}")
                    save_account_details(account)
                else:
                    print("Transfer Failed")
            else:
                print("Recipient Account Not Found")

        elif choice == "5":
            confirm = input("Are you sure you want to delete your account? (yes/no): ")
            if confirm.lower() == "yes":
                delete_account(account)
                break

        elif choice == "6":
            break

        else:
            print("Invalid choice. Please try again.")

def delete_account(account):
    try:
        with open("accounts.txt", "r") as file:
            lines = file.readlines()
        with open("accounts.txt", "w") as file:
            for line in lines:
                if line.split(",")[0] != account.accountNumber:
                    file.write(line)
        print("Account deleted successfully")
    except FileNotFoundError:
        print("Error deleting account. File not found.")

def find_account(accountNumber):
    accounts = load_accounts()
    for account in accounts:
        if account.accountNumber == accountNumber:
            return account
    return None

def main():
    while True:
        print("\nWelcome to the Banking App")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_account()

        elif choice == "2":
            account = login()
            if account:
                print("Login successful.")
                manage_account(account)

        elif choice == "3":
            print("Exiting the Banking App")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
