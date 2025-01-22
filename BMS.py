import pathlib
import pickle
import os

class Account():
    def __init__(self):
        self.accNo = 0
        self.name = ""
        self.type = ""
        self.deposit = 0

    def createAcc(self):
        self.accNo=int(input("Enter the Acccount Number: "))
        self.name=input("Enter the Account Holder Name: ")
        self.type=input("Enter Account Type [S/C]: ").upper()       #small case to upper case
        self.deposit=int(input("Enter the intial Amount\n[(>=500 for Savings Account)\n(>=1000 for Current Account)]: "))
        print("\nYour Account has been created!\n")

    def showAccount(self):
        print("Account Number:", self.accNo)
        print("Account Holder Name:", self.name)
        print("Type of Account:", self.type)
        print("Balance:", self.deposit)

    def modifyAccount(self):
        print("Account Number: ", self.accNo)
        self.name = input("Modify Account Holder Name: ")
        self.type = input("Modify Type of Account [C/S]: ").upper()
        self.deposit = int(input("Modify Balance: "))

    def depositAmount(self,amt):
        self.deposit += amt

    def withdrawAmount(self,amt):
        if amt <= self.deposit:
            self.deposit -= amt
        else:
            print("Insufficient balance")

def intro():
    #while True helps to run infinite loop, Only when the user choose 8 program will exit
    while True:
        print("\t\tMAIN MENU")
        print("\t1.NEW ACCOUNT")
        print("\t2.DEPOSIT AMOUNT")
        print("\t3.WITHDRAW AMOUNT")
        print("\t4.BALANCE ENQUIRY")
        print("\t5.ALL ACCOUNT HOLDERS LIST")
        print("\t6.DELETE AN ACCOUNT")
        print("\t7.MODIFY AN ACCOUNT")
        print("\t8.EXIT")

        option=input("Select an Option (1-8): ")
        if option=="1":
            createNewAcc()
        elif option=="2":
            num=int(input("Enter the Account Number: "))
            depositAndWithdraw(num,1)
        elif option=="3":
            num=int(input("Enter the Account Number: "))
            depositAndWithdraw(num,2)
        elif option=="4":
            num=int(input("Enter the Account Number: "))
            balanceEnq(num)
        elif option=="5":
            allAcc()
        elif option=="6":
            num=int(input("Enter the Account Number: "))
            closeAcc(num)
        elif option=="7":
            num=int(input("Enter the Account Number: "))
            modifyAcc(num)
        elif option=="8":
            print("\t\t\tThankYou for using Bank Management System")
            break
        else:
            print("\t!!! INVALID OPTION !!!")

def createNewAcc():
    account = Account()     #Object created for ACCOUNT class
    account.createAcc()
    writeAccountsFile(account)

def writeAccountsFile(account):
    #data extension is used in terms to set data in structured format
    file = pathlib.Path("accounts.data")    
    #checking whether the file already have or not
    if file.exists():       
        infile = open("accounts.data", "rb")     
        oldlist = pickle.load(infile)       #deserializing the datas in the file
        oldlist.append(account)
        infile.close()
        #Deletes the old file to allow the updated list to be saved.
        os.remove("accounts.data")      
    else:
        #The file will create and add the new account as a LIST
        oldlist = [account]
    outfile = open("accounts.data", "wb")
    pickle.dump(oldlist, outfile)       #serializing the datas in the file
    outfile.close()

def depositAndWithdraw(num, opt):
    file = pathlib.Path("accounts.data")
    if file.exists():
        with open("accounts.data", "rb") as infile:
            mylist = pickle.load(infile)
        os.remove("accounts.data")
        found = False
        for item in mylist:
            if item.accNo == num:  
                if opt == 1:  # Deposit
                    amt = int(input("Enter the amount to deposit: "))
                    item.depositAmount(amt)
                    print("Your account balance has been updated")
                elif opt == 2:  # Withdraw
                    amt = int(input("Enter the amount to withdraw: "))
                    item.withdrawAmount(amt)
                    print("Your account balance has been updated")
                found = True
                break
        if not found:
            print("No matching account found.")
        with open("accounts.data", "wb") as outfile:
            pickle.dump(mylist, outfile)
    else:
        print("No records found.")


def balanceEnq(num):
    file=pathlib.Path("accounts.data")
    if file.exists():
        infile=open("accounts.data","rb")
        mylist=pickle.load(infile)
        infile.close()
        found = False
        for item in mylist:
            if item.accNo == num:
                print("Your Account Balance is: ", item.deposit)
                found = True
        if not found:
            print("No existing record with this number")
    else:
        print("no records to search")

def allAcc():
    file=pathlib.Path("accounts.data")
    if file.exists():
        infile=open("accounts.data","rb")
        mylist=pickle.load(infile)
        for item in mylist:
            item.showAccount()
        infile.close()
    else:
        print("No records to display")

def closeAcc(num):
    file = pathlib.Path("accounts.data")
    if file.exists():
        infile=open("accounts.data","rb")
        oldlist=pickle.load(infile)
        infile.close()
        newList=[item for item in oldlist if item.accNo != num]
        os.remove("accounts.data")
        outfile=open("accounts.data","wb")
        pickle.dump(newList,outfile)
        outfile.close()
        print("Account deleted")
    else:
        print("No records to delete")

def modifyAcc(num):
    file=pathlib.Path("accounts.data")
    if file.exists():
        infile=open("accounts.data","rb")
        oldlist=pickle.load(infile)
        infile.close()
        os.remove("accounts.data")
        for item in oldlist:
            if item.accNo == num:
                item.modifyAccount()
                break
        outfile=open("accounts.data","wb")
        pickle.dump(oldlist,outfile)
        outfile.close()
    else:
        print("No records Found")

print("\t\t\t****************************")
print("\t\t\t   BANK MANAGEMENT SYSTEM")
print("\t\t\t****************************")
input("Please Enter to continue.........")      #input used to press the ENTER key to continue
intro()     

#It is used to be an Standalone program, We cannot use this file as an module
if __name__ == "__main__":
    intro()