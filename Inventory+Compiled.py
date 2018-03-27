
# coding: utf-8

# In[ ]:


import numpy
import os
import pandas as pd

#LCD
import LCD2004 as lcd
display = lcd.LCD()
display.toggle_backlight(True)
#reload(lcd) command to update

#Reader
import m5e
read = m5e.M5e()

#Should find a way to access the RFID tags

os.chdir('D:\Academics\Spring 2018\Intro to Human Space Flight\Project')
#cd D:\Academics\Spring 2018\Intro to Human Space Flight\Project

#Place all files in one directory

stock = pd.read_csv("Stock.csv")
new_items=pd.read_csv("New Items.csv")

#stock_count = len(stock["Name"])
#new_items_count = len(new_items["Name"])

"""list = ["\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02", "0X4284r82r", "shjbvhsd", "sfsgfsg", "wsefdwf"]
j = 0
for i in list:
    stock.loc[j, "ID"] = i
    j += 1"""
    
"""for i in range(0, len(new_items["Name"])):
        stock.loc[stock_count + i]["Name"] = new_items.loc[i]["Name"]
        stock.loc[stock_count + i]["Quantity"] = new_items.loc[i]["Quantity"]
        stock.loc[stock_count + i]["Type"] = new_items.loc[i]["Type"]"""
    
stock = stock.append(new_items)
stock.to_csv("Stock.csv", index=False, encoding='utf8')
stock = pd.read_csv("Stock.csv")

stock_count = len(stock["Name"])
stock

flag = 0
while (flag == 0):
    option = input("Type\n'1' for Location tracking\n'2' for Availability Checking\n'3' to Exit")
# Temp CTB Update Code
#stock = pd.read_csv("Stock.csv")


    what = input("What do you want to update? Add or Remove (a/r): ")
    code = "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02"

    if what == 'a' | what == 'A':
        for i in range (0, len(stock["Name"])):
            if (stock.loc[i]["ID"]) == code:
                stock.loc[i, "Status"] = "Available"
         
            
    elif what == 'r' | what == 'R':
        for i in range (0, len(stock["Name"])):
            if (stock.loc[i]["ID"]) == code:
                stock.loc[i, "Status"] = "Not Available"
                

            
    stock.to_csv("Stock.csv", index=False, encoding='utf8')
    stock = pd.read_csv("Stock.csv")

    stock



# Finding location of the item using the terminal

    if option == 1:
        choice = input("Do you want to enter or Scan or Type? (s/t): ")
        mis = 0
        if choice == 't' | choice == 't':
            name = input("Enter the name of the product: ")
    
            for i in range (0, len(stock["Name"])):
                if stock.loc[i]["Name"].lower() == name.lower():
                    if stock.loc[i]["Status"] == "Not Available":
                        print ("\n\n", stock.loc[[i]])
                        mis = 1
                        
            if mis == 0:
                print ("Item already placed in Cargo Transfer Bag")
                
                
        elif choice == 's' | choice == 'S':
            code = read.ReadSingleTag()
    
            for i in range (0, len(stock["ID"])):
                if stock.loc[i]["ID"] == code:
                    print ("\n\n", stock.loc[[i]])
                    
        else:
            print ("Invalid Input")
        
        
#print ("\nQuantity Available: ", temp_count)



#Checking the availability of a product using the terminal
    elif option == 2:
        name = input("Enter the name of the product: ")
        tot_count = 0
        inv_count = 0
        for i in range (0, len(stock["Name"])):
                if stock.loc[i]["Name"].lower() == name.lower():
                    tot_count += 1
                    if stock.loc[i]["Status"] == "Available":
                        inv_count += 1
                    print (stock.loc[[i]])

        print ("\n\nTotal Quantity: ", tot_count)
        print ("Quantity in Inventory: ", inv_count)
    
    elif option == 3:
        print("Bye")
        flag = 1
        
    else:
        print ("Invalid Input")

