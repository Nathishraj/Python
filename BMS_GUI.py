import tkinter
from tkinter import *
from tkinter import messagebox
import pathlib
import pickle 

class BMS:
    def __init__(self):
        self.accNo = 0
        self.name = ""
        self.type = ""
        self.deposit = 0
        self.window=tkinter.Tk()
        self.window.geometry("800x500")
        self.window.title("BMS")
        self.window.resizable(0,0)
        self.entry()

    #Using this to clean the data in the files
    def reset_data_file(self):
        with open("accounts.data", "wb") as outfile:
            pickle.dump([], outfile)  # Save an empty list to clear the file
        messagebox.showinfo("Success", "Data file has been reset!")

    def entry(self):
        self.f1=Frame(self.window,width=800,height=500)
        self.f1.place(x=0,y=0)
        l1=Label(self.f1,text="Bank Management System",font=("Algerian",36,"bold"))
        l1.place(x=60,y=60)
        b1=Button(self.f1,text="NEW ACCOUNT",font=("Lato",17,"bold"),width=18,bg="#3399ff",command=self.createNewAcc)
        b1.place(x=120,y=160)
        b2=Button(self.f1,text="DEPOSIT AMOUNT",font=("Lato",17,"bold"),width=18,bg="#3399ff",command=self.deposit_amount)
        b2.place(x=120,y=230)
        b3=Button(self.f1,text="WITHDRAW AMOUNT",font=("Lato",17,"bold"),width=18,bg="#3399ff",command=self.withdraw_amount)
        b3.place(x=120,y=300)
        b4=Button(self.f1,text="BALANCE ENQUIRY",font=("Lato",17,"bold"),width=18,bg="#3399ff",command=self.balance_enquiry)
        b4.place(x=120,y=370)
        b5=Button(self.f1,text="ALL ACCOUNTS",font=("Lato",17,"bold"),width=18,bg="#3399ff",command=self.allAcc)
        b5.place(x=450,y=160)
        b6=Button(self.f1,text="DELETE ACCOUNT",font=("Lato",17,"bold"),width=18,bg="#3399ff",command=self.delete_account)
        b6.place(x=450,y=230)
        b7=Button(self.f1,text="MODIFY ACCOUNT",font=("Lato",17,"bold"),width=18,bg="#3399ff",command=self.modify_account)
        b7.place(x=450,y=300)
        b8=Button(self.f1,text="EXIT",font=("Lato",17,"bold"),width=18,bg="red",command=self.window.destroy)
        b8.place(x=450,y=370)

        self.window.mainloop()

    def createNewAcc(self):
        self.accNo = IntVar()
        self.name = StringVar()
        self.type = StringVar()
        self.deposit = IntVar()
        self.f2 = Frame(self.f1, width=800, height=500)
        self.f2.place(x=0, y=0)
        # Labels and entry fields
        Label(self.f2, text="Enter the Account Number:", font=("Lato", 12, "bold")).place(x=120, y=140)
        Entry(self.f2, width=30, textvariable=self.accNo).place(x=450, y=150)
        Label(self.f2, text="Enter the Account Holder Name:", font=("Lato", 12, "bold")).place(x=120, y=200)
        Entry(self.f2, width=30, textvariable=self.name).place(x=450, y=200)
        Label(self.f2, text="Select Account Type:", font=("Lato", 12, "bold")).place(x=120, y=260)
        Radiobutton(self.f2, text="Savings Account", variable=self.type, value="Savings Account").place(x=420, y=260)
        Radiobutton(self.f2, text="Current Account", variable=self.type, value="Current Account").place(x=600, y=260)
        Label(self.f2, text="Enter the Initial Amount: ", font=("Lato", 12, "bold")).place(x=120, y=320)
        Entry(self.f2, width=30, textvariable=self.deposit).place(x=420, y=320)
        # Save Account button with command linked to save_account method
        save_button = Button(self.f2, text="Save Account", font=("Lato", 14, "bold"), command=self.save_account)
        save_button.place(x=350, y=400)


    def save_account(self):
        # Retrieve user input values
        acc_no = self.accNo.get()
        name = self.name.get()
        acc_type = self.type.get()
        deposit = self.deposit.get()
        # Validate inputs
        if not acc_no or not name or not acc_type or deposit <= 0:
            messagebox.showerror("Error", "All fields are required, and deposit must be greater than zero!")
            return
        # Prepare account data
        account_data = {
            "Account No": acc_no,
            "Name": name,
            "Type": acc_type,
            "Deposit": deposit,
        }
        # Write data to file
        file = pathlib.Path("accounts.data")
        if file.exists():
            with open("accounts.data", "rb") as infile:
                try:
                    accounts = pickle.load(infile)
                except EOFError:  # File exists but is empty
                    accounts = []
        else:
            accounts = []
        accounts.append(account_data)
        with open("accounts.data", "wb") as outfile:
            pickle.dump(accounts, outfile)
        messagebox.showinfo("Success", "Account Created Successfully!")
        self.entry()  # Return to the main menu

    def deposit_amount(self):
        self.accNo = IntVar()
        self.amount = IntVar()
        self.f3 = Frame(self.f1, width=800, height=500)
        self.f3.place(x=0, y=0)
        Label(self.f3, text="Deposit Amount", font=("Algerian", 24, "bold")).place(x=260, y=60)
        Label(self.f3, text="Enter Account Number:", font=("Lato", 12, "bold")).place(x=120, y=160)
        Entry(self.f3, width=30, textvariable=self.accNo).place(x=450, y=160)
        Label(self.f3, text="Enter Deposit Amount:", font=("Lato", 12, "bold")).place(x=120, y=220)
        Entry(self.f3, width=30, textvariable=self.amount).place(x=450, y=220)
        deposit_button = Button(self.f3, text="Deposit", font=("Lato", 14, "bold"), command=self.perform_deposit)
        deposit_button.place(x=350, y=300)
        back_button = Button(self.f3, text="Back", font=("Lato", 14, "bold"), command=self.entry)
        back_button.place(x=350, y=360)

    def perform_deposit(self):
        acc_no = self.accNo.get()
        amount = self.amount.get()
        if not acc_no or not amount:
            messagebox.showerror("Error", "All fields are required!")
            return
        file = pathlib.Path("accounts.data")
        if file.exists():
            with open("accounts.data", "rb") as infile:
                accounts = pickle.load(infile)
            for account in accounts:
                if account['Account No'] == acc_no:
                    account['Deposit'] += amount
                    with open("accounts.data", "wb") as outfile:
                        pickle.dump(accounts, outfile)
                    messagebox.showinfo("Success", "Amount Deposited Successfully!")
                    self.entry()
                    return
            messagebox.showerror("Error", "Account not found!")
        else:
            messagebox.showerror("Error", "No accounts found!")

    def withdraw_amount(self):
        self.accNo = IntVar()
        self.amount = IntVar()
        self.f4 = Frame(self.f1, width=800, height=500)
        self.f4.place(x=0, y=0)
        Label(self.f4, text="Withdraw Amount", font=("Algerian", 24, "bold")).place(x=260, y=60)
        Label(self.f4, text="Enter Account Number:", font=("Lato", 12, "bold")).place(x=120, y=160)
        Entry(self.f4, width=30, textvariable=self.accNo).place(x=450, y=160)
        Label(self.f4, text="Enter Withdraw Amount:", font=("Lato", 12, "bold")).place(x=120, y=220)
        Entry(self.f4, width=30, textvariable=self.amount).place(x=450, y=220)
        withdraw_button = Button(self.f4, text="Withdraw", font=("Lato", 14, "bold"), command=self.perform_withdraw)
        withdraw_button.place(x=350, y=300)
        back_button = Button(self.f4, text="Back", font=("Lato", 14, "bold"), command=self.entry)
        back_button.place(x=350, y=360)

    def perform_withdraw(self):
        acc_no = self.accNo.get()
        amount = self.amount.get()
        if not acc_no or not amount:
            messagebox.showerror("Error", "All fields are required!")
            return
        file = pathlib.Path("accounts.data")
        if file.exists():
            with open("accounts.data", "rb") as infile:
                accounts = pickle.load(infile)
            for account in accounts:
                if account['Account No'] == acc_no:
                    if account['Deposit'] < amount:
                        messagebox.showerror("Error", "Insufficient balance!")
                    else:
                        account['Deposit'] -= amount
                        with open("accounts.data", "wb") as outfile:
                            pickle.dump(accounts, outfile)
                        messagebox.showinfo("Success", "Amount Withdrawn Successfully!")
                        self.entry()
                        return
            messagebox.showerror("Error", "Account not found!")
        else:
            messagebox.showerror("Error", "No accounts found!")

    def balance_enquiry(self):
        self.accNo = IntVar()
        self.f7 = Frame(self.f1, width=800, height=500)
        self.f7.place(x=0, y=0)
        Label(self.f7, text="Balance Enquiry", font=("Algerian", 24, "bold")).place(x=260, y=60)
        Label(self.f7, text="Enter Account Number:", font=("Lato", 12, "bold")).place(x=120, y=160)
        Entry(self.f7, width=30, textvariable=self.accNo).place(x=450, y=160)
        check_button = Button(self.f7, text="Check Balance", font=("Lato", 14, "bold"), command=self.perform_balance_enquiry)
        check_button.place(x=350, y=300)
        back_button = Button(self.f7, text="Back", font=("Lato", 14, "bold"), command=self.entry)
        back_button.place(x=350, y=360)

    def perform_balance_enquiry(self):
        acc_no = self.accNo.get()
        if not acc_no:
            messagebox.showerror("Error", "Account number is required!")
            return
        file = pathlib.Path("accounts.data")
        if file.exists():
            with open("accounts.data", "rb") as infile:
                accounts = pickle.load(infile)
            for account in accounts:
                if account['Account No'] == acc_no:
                    balance = account['Deposit']
                    messagebox.showinfo("Balance Enquiry", f"Account Number: {acc_no}\nBalance: {balance}")
                    return
            messagebox.showerror("Error", "Account not found!")
        else:
            messagebox.showerror("Error", "No accounts found!")


    def allAcc(self):
        file = pathlib.Path("accounts.data")
        if file.exists() and file.stat().st_size > 0:  # Check if file exists and is not empty
            with open("accounts.data", "rb") as infile:
                try:
                    accounts = pickle.load(infile)
                    if accounts:  # Ensure there are records to display
                        account_info = "\n".join(
                            [f"Account No: {acc['Account No']}, Name: {acc['Name']}, "
                            f"Type: {acc['Type']}, Balance: {acc['Deposit']}" for acc in accounts]
                        )
                        messagebox.showinfo("All Accounts", account_info)
                    else:
                        messagebox.showinfo("Info", "No accounts to display!")
                except (EOFError, pickle.UnpicklingError) as e:
                    messagebox.showerror("Error", f"Unable to read file: {e}")
        else:
            messagebox.showerror("Error", "No records to display!")
            
    def showAccount(self, acc_no):
        file = pathlib.Path("accounts.data")
        if file.exists():
            with open("accounts.data", "rb") as infile:
                accounts = pickle.load(infile)
            for acc in accounts:
                if acc["Account No"] == acc_no:
                    messagebox.showinfo(
                        "Account Details",
                        f"Account No: {acc['Account No']}\n"
                        f"Name: {acc['Name']}\n"
                        f"Type: {acc['Type']}\n"
                        f"Balance: {acc['Deposit']}"
                    )
                    return
            messagebox.showerror("Error", "Account not found!")
        else:
            messagebox.showerror("Error", "No records available!")
    
    def delete_account(self):
        self.accNo = IntVar()
        self.f5 = Frame(self.f1, width=800, height=500)
        self.f5.place(x=0, y=0)
        Label(self.f5, text="Delete Account", font=("Algerian", 24, "bold")).place(x=260, y=60)
        Label(self.f5, text="Enter Account Number:", font=("Lato", 12, "bold")).place(x=120, y=160)
        Entry(self.f5, width=30, textvariable=self.accNo).place(x=450, y=160)
        delete_button = Button(self.f5, text="Delete", font=("Lato", 14, "bold"), command=self.perform_delete)
        delete_button.place(x=350, y=300)
        back_button = Button(self.f5, text="Back", font=("Lato", 14, "bold"), command=self.entry)
        back_button.place(x=350, y=360)

    def perform_delete(self):
        acc_no = self.accNo.get()
        if not acc_no:
            messagebox.showerror("Error", "Account number is required!")
            return
        file = pathlib.Path("accounts.data")
        if file.exists():
            with open("accounts.data", "rb") as infile:
                accounts = pickle.load(infile)
            updated_accounts = [account for account in accounts if account['Account No'] != acc_no]
            if len(updated_accounts) == len(accounts):
                messagebox.showerror("Error", "Account not found!")
            else:
                with open("accounts.data", "wb") as outfile:
                    pickle.dump(updated_accounts, outfile)
                messagebox.showinfo("Success", "Account deleted successfully!")
                self.entry()
        else:
            messagebox.showerror("Error", "No accounts found!")

    def modify_account(self):
        self.accNo = IntVar()
        self.new_name = StringVar()
        self.new_type = StringVar()
        self.f6 = Frame(self.f1, width=800, height=500)
        self.f6.place(x=0, y=0)
        Label(self.f6, text="Modify Account", font=("Algerian", 24, "bold")).place(x=260, y=60)
        Label(self.f6, text="Enter Account Number:", font=("Lato", 12, "bold")).place(x=120, y=160)
        Entry(self.f6, width=30, textvariable=self.accNo).place(x=450, y=160)
        Label(self.f6, text="Enter New Name:", font=("Lato", 12, "bold")).place(x=120, y=220)
        Entry(self.f6, width=30, textvariable=self.new_name).place(x=450, y=220)
        Label(self.f6, text="Select New Account Type:", font=("Lato", 12, "bold")).place(x=120, y=280)
        Radiobutton(self.f6, text="Savings Account", variable=self.new_type, value="Savings Account").place(x=450, y=280)
        Radiobutton(self.f6, text="Current Account", variable=self.new_type, value="Current Account").place(x=600, y=280)
        modify_button = Button(self.f6, text="Modify", font=("Lato", 14, "bold"), command=self.perform_modify)
        modify_button.place(x=350, y=360)
        back_button = Button(self.f6, text="Back", font=("Lato", 14, "bold"), command=self.entry)
        back_button.place(x=350, y=420)

    def perform_modify(self):
        acc_no = self.accNo.get()
        new_name = self.new_name.get()
        new_type = self.new_type.get()
        if not acc_no or not new_name or not new_type:
            messagebox.showerror("Error", "All fields are required!")
            return
        file = pathlib.Path("accounts.data")
        if file.exists():
            with open("accounts.data", "rb") as infile:
                accounts = pickle.load(infile)
            for account in accounts:
                if account['Account No'] == acc_no:
                    account['Name'] = new_name
                    account['Type'] = new_type
                    with open("accounts.data", "wb") as outfile:
                        pickle.dump(accounts, outfile)
                    messagebox.showinfo("Success", "Account modified successfully!")
                    self.entry()
                    return
            messagebox.showerror("Error", "Account not found!")
        else:
            messagebox.showerror("Error", "No accounts found!")

begin=BMS()