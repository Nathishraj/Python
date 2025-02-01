import mysql.connector
#Connecting MySQL Database
mycon = mysql.connector.connect(
    host="localhost", user="root", 
    password="Nathish", database="shopping_ms")
#Cursor used to send sql queries and retrieve results
mycur = mycon.cursor()

# To provide extra blank spaces in the output for readability
def space(): 
	for i in range(1):
		print()

def check():
	#query to select all customer IDs from the table
	qry = 'select cust_id from customer;'
	mycur.execute(qry)
	d = mycur.fetchall()
    #creating empty list to save the customer IDs
	list_of_ids = []
	for ids in d:
		list_of_ids.append(ids[0])
	return list_of_ids

def createCustAcc():
    listOfIds = check()
    #This is just for having an condition to the infinite loop
    ask = "Y"
    while ask in "yY":
        cust_id = int(input("Let's check whether you already have an account\nEnter your Customer Id..."))
        if cust_id in listOfIds:
             print("This Customer ID has been already existed./nTry creating a new ID for you!")
        else:
             #Empty Tuple to create new ID to add the new customer details 
             cust_details = ()
             cust_fname = input("Enter the First Name: ")
             cust_lname = input("Enter the Last Name: ")
             cust_mnum = input("Enter the Mobile Number: ")
             cust_adrs = input("Enter the Address: ")
             cust_details = (cust_id,cust_fname,cust_lname,cust_mnum,cust_adrs)
             #Writing SQL Query to add the details
             sql_query = 'insert into customer values(%s,%s,%s,%s,%s,NULL)'
             #value of the fields to be entered with the query
             val = cust_details
             mycur.execute(sql_query, val)
             mycon.commit()
             print('Customer details entered')
             ask = input('Do you want to continue (Y/N) ')
             if ask not in ('Yy'):
                space()
                break

def getBkdPro(cust_id):
    sql_query = "select bkd_pro from customer where cust_id=%s;"
    mycur.execute(sql_query,(cust_id,))
    bkdpro = mycur.fetchone()
    bkd_pros = bkdpro[0]
    return bkd_pros

def existCustAcc():
    try:
        ask = int(input("Enter your Customer Id to sign-in: "))
        listOfIds = check()
        print("Successfully Logged!!")
        if ask in listOfIds:
            while True:
                print("\n\n1. View Bookings\n2. Book a Product\n3. Update your Id details\n4. Cancelling booked products\n\t\tEnter 'back' to get back")
                choi = input("Enter - ")
                if choi == "1":
                    bkdpro = getBkdPro(ask)
                    #if there is no products booked in that cust_id
                    if bkdpro is None or bkdpro == "":
                        print("You have not yet booked products")
                    else:
                        pros = bkdpro.strip("_").split("_")
                        print("Booked Products: ")
                        for bkditems in pros:
                            print("- " + bkditems)

                elif choi == "2":
                    sql_query = "select pro_id from products;"
                    mycur.execute(sql_query)
                    proslist = mycur.fetchall()
                    #Empty list to store product Id's
                    listOfProducts = []
                    for i in proslist:
                        listOfProducts.append(i[0])
                        print(listOfProducts)
                    pro_id = input("Enter the product id to get booked: ")
                    #Checking before if that entered product_id has a place in total product_ids
                    if pro_id in listOfProducts:
                        sql_query = "select bkd_pro from customer where cust_id=%s;"
                        mycur.execute(sql_query,(ask,))
                        pro = mycur.fetchone()
                        prl = pro[0]
                        #When the column is empty, New product will be stored
                        if prl is None or prl == "":
                            sql_query = "update customer set bkd_pro=%s where cust_id=%s;"
                            val = (pro_id+"_",ask)
                            mycur.execute(sql_query,val)
                            mycon.commit()
                            print("Your product is booked successfully!")
                        #If the product is alraedy booked, Adding one more quantity of that product
                        else:
                            prl1 = prl+pro_id+"_"
                            sql_query2 = "update customer set bkd_pro=%s where cust_id=%s;"
                            val2 = (prl1,ask)
                            mycur.execute(sql_query2,val2)
                            mycon.commit()
                            print("Your product is booked successfully!")
                    else:
                        print("This product doesn't exists.\nMake sure that you've entered correct product Id!")
                
                elif choi == "3":
                     sql_query = "select cust_id, c_fname, c_lname, c_mnum, c_adrs from customer where cust_id =%s;"
                     mycur.execute(sql_query,(ask,))
                     c_det = mycur.fetchone()
                     fields = ["First Name","Last Name","Mob Number","Address"]
                     dic = {}
                     #The loop prints existing details for the user.
                     print("Your existing record is: ")
                     for i in range(4):
                          dic[fields[i]] = c_det[i+1]
                          print(i+1,"",fields[i],":",c_det[i+1])
                     #Selecting which info to be changed
                     for i in range(len(c_det)):
                          updtchoi = int(input("Enter choice to update: "))
                          upval = input("Enter the new "+fields[updtchoi-1]+": ")
                          dic[fields[updtchoi-1]] = upval
                          cont = input("Do you want to update other details? Y or N : ")
                          if cont in "Nn":
                              break
                     sql_query = "update customer set c_fname=%s, c_lname=%s, c_mnum=%s, c_adrs=%s where cust_id=%s;"
                     updt1 = tuple(dic.values())+(ask)
                     val = updt1
                     mycur.execute(sql_query, val)
                     mycon.commit()
                     print("Your details were updated!")

                elif choi == "4":
                     try:
                          #To get the existed bookings from the table
                          bkd_pro = getBkdPro(ask)
                          print("Your Bookings are: \n",bkd_pro)
                          if bkd_pro is None or bkd_pro == "":
                               print("You have no bookings to get cancelled")
                          else:
                               cpro = input("To cancel all the products: Enter 'A'\n OR Enter a product code to cancel a specific one: ")
                               if cpro in "Aa":
                                    sql_query = "update customer set bkd_pro=NULL where cust_id=%s"
                                    mycur.execute(sql_query,(ask,))
                                    mycon.commit()
                                    print("All bookings have been cancelled")
                               elif cpro in bkd_pro:
                                    #The booked products are stored as a string (e.g., "P101_P102_P103_").
                                    #[0:-1] removes the trailing underscore (_) at the end.
                                    x = (bkd_pro[0:-1]).split("_")
                                    x.remove(cpro)
                                    updt_pro = ""
                                    #Again adding those "_" for further uses
                                    for item in x:
                                        updt_pro = updt_pro + item + '_'
                                    sql_query = "update customer set bkd_pro=%s where cust_id=%s;"
                                    val = (updt_pro,ask)
                                    mycur.execute(sql_query,val)
                                    mycon.commit()
                                    print("Booking Cancelled !")
                     except Exception:
                          print("Some problem in cancelling booking products.Try Again")
                elif choi.lower() == "back":
                     print("Successfully Logged Out")
                     space()
                     break
        else:
             print("This Account does not exist")
    except Exception:
         print("\nSome error Occured. Try Again! \nIf nothing disturbs you, you can continue on your way!")

def view_pro():
     sql_query = "select * from products;"
     mycur.execute(sql_query)
     d = mycur.fetchall()
     #[(101, "Product1", 50000, 10),(102, "Product2", 500, 25),(103, "Product3", 1500, 15)]          
     dic = {}
     #Key → Product ID (i[0])     
     #Value → Remaining details (name, price, stock) as a tuple (i[1:])
     for i in d:
          dic[i[0]] = i[1:]        
          #{101: ()"Product1", 50000, 10), 102: ("Product2", 500, 25), 103: ("Product3", 1500, 15)}
     print("_"*80)
     print("{:<17} {:<22} {:<23} {:<19}".format(
          "Product name","Product ID","Price","Stock"))
     print("_"*80)
     #Printing the dictionary in the form of a table
     for pid, pdet in dic.items():
          a, b, c = pdet
          print("{:<17} {:<22} {:<23} {:<19}".format(pid, a, b, c))
     print("_"*80)

def addpro():
     #Display the current list of products
     view_pro()
     n = int(input("Enter no of items to insert: "))
     for j in range(n):
          t = ()
          proname = input("Product Name: ")
          proid = input("Product ID: ")
          pprice = int(input("Price : "))
          pstk = int(input("Stock: "))
          t = (proname, proid, pprice, pstk)
          sql_query = "insert into products values(%s,%s,%s,%s);"
          val = t
          mycur.execute(sql_query, val)
          mycon.commit()
          print("Product Added")

def delpro():
     view_pro()
     delpr = input("Enter Id of a Product to be deleted")
     sql_query = "delete from products where pro_id=%s;"
     mycur.execute(sql_query,delpr)
     mycon.commit()
     print("Product is deleted")

def employee():
     try:
          ask = input("Enter your employee id to sign in: ")
          sql_query = "select emp_id from employee;"
          mycur.execute(sql_query)
          eids = mycur.fetchall()
          ListofEmpID = []
          for i in eids:
               ListofEmpID.append(i[0])
          if ask not in ListofEmpID:
               print("Enter the correct ID")
          else:
               while True:
                    space()
                    cho = input(" 1.Update deliver records\n 2.Add a new product\n 3.Delete a product\n\t\tEnter 'back' to logout: ")
                    if cho == "1":
                         cust_id = input("Enter customer ID: ")
                         bkd_pro = getBkdPro(cust_id)       #Before Split "P101_P102_P103_"
                         if bkd_pro is None or bkd_pro == "":
                              print("This customer has no bookings")
                         else:
                              print("All Bookings: ",bkd_pro)
                              pro_id = input("Enter product code to remove the delievered product ")
                              if pro_id in bkd_pro:
                                   x = (bkd_pro[0:-1]).split("_")     #After Split x = ["P101","P102","P103"]
                                   #Removing the entered product id
                                   x.remove(pro_id)
                                   updt_pro = ""
                                   #Again Updating Products with "_" for further uses
                                   for i in x:
                                        updt_pro = updt_pro+i+"_"
                                   sql_query = "update customer set bkd_pro=%s where cust_id=%s;"
                                   val = (updt_pro, cust_id)
                                   mycur.execute(sql_query,val)
                                   mycon.commit()
                                   print("Delievered products is removed from the database")
                              else:
                                   print("Enter the correct code")
                    elif cho == "2":
                         addpro()
                    elif cho == "3":
                         delpro()
                    elif cho.lower() == "back":
                         print("Successfully Logged out ")
                         break
     except Exception:
          print("Give the correct input")

def addemp():
     sql_query = "select * from employee;"
     mycur.execute(sql_query)
     emp_list = mycur.fetchall()
     print("List of Current Employees:")
     for emp in emp_list:
          print("Emp Id: ", emp[0], "First Name: ", emp[1], "Last Name: ", emp[2], "Phone No: ", emp[3])
     newemp = []
     new = int(input("Enter the number of employees to add : "))
     for i in range(1,new+1):
          newone = ()
          neid = int(input(str(i) + ') Employee Id(==3 digits): '))
          nefname = input(str(i) + ') First Name: ')
          nelname = input(str(i) + ') Last Name: ')
          nemnum = int(input(str(i) + ') Contact No: '))
          neadrs = input(str(i) + ') Address: ')
          #Saving details in a tuple format
          newone = (neid, nefname, nelname, nemnum, neadrs)
          newemp = newemp + [newone,]
     sql_query = "insert into employee values(%s,%s,%s,%s,%s);"
     for i in range(len(newemp)):
          val = newemp[i]
          mycur.execute(sql_query,val)
          mycon.commit()
     print("Employee details has been added")
     space()

def employer():
     while True:
          print()
          print("Enter the Option:\n1.View Product Details\n2.Add a New Employee\n\t\tEnter 'back' to get back")
          ch = input("Enter - ")
          if ch == "1":
               view_pro()
          elif ch == "2":
               addemp()
          elif ch.lower() == "back":
               break

print("\t\t\tWelcome to Our Boutique Shop!")
#Running an Infinite Loop
while True:
    print("Who are you : \na)Customer\nb)Employee\nc)Employer\n\t\tEnter e to EXIT")
    choice=input("Enter - ")
    try:
        if choice in "aA":
            print("1.Create Account\n2.Sign into the Existing Account\n")
            choic=input("Enter - ")
            if choic == "1":
                createCustAcc()
            elif choic == "2":
                existCustAcc()
            else:
                print("Enter the correct option!")
        elif choice in "bB":
            employee()
        elif choice in "cC":
            employer()
        elif choice.lower() == "e":
            print("ThankYou for visiting our Boutique Shop")
            break
    except Exception:
        print("Give the right input")
    space()
        