#read.ReadMultiTag()

import numpy
import os
import pandas as pd

#LCD
import LCD2004 as lcd
display = lcd.LCD()
display.toggle_backlight(False)
#reload(lcd) command to update


    
#Reader
import m5e
read = m5e.M5e()

os.chdir('.')

#Place all files in one directory

stock = pd.read_csv("Stock.csv")

flag = 0
while (flag == 0):
    option1 = input("\n\nEnter an Option\n'1' - Dispay Inventory Items \n'2' - Check the Availability of an Item\n'3' - Exit\n\n")
    option = int(option1)
    


    
    #Option 1
    if option == 1:
        
        
        list1 = read.ReadMultiTag()
    
        for i in range(0, len(stock["Name"])):
            stock.loc[i, "Status"] = "Unavailable"
    
        for i in range(0, len(list1)):
            if list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x16pl\xa3":
                stock.loc[0, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x17@a\x87":
                stock.loc[1, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x15\x00|`":
                stock.loc[2, "Status"] = "Available"
            
            elif list1[i] == "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04":
                stock.loc[3, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00\x00\x17E\x18\x011%\x10\x16\xed":
                stock.loc[4, "Status"] = "Available"
            
            elif list1[i] == "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05":
                stock.loc[5, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00\x00\x17E\x18\x013%\x10\x16\xee":
                stock.loc[6, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00\x00\x17E\x18\x012%\x10\x16\xe6":
                stock.loc[7, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x16\x10q":
                stock.loc[8, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x15\x10~\x9c":
                stock.loc[9, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x19\x00P\x1d":
                stock.loc[10, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x18PV\x96":
                stock.loc[11, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00\x00\x17E\x18\x01(%\x10\x16\xd8":
                stock.loc[12, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00\x00\x17E\x18\x01'%\x10\x16\xdf":
                stock.loc[13, "Status"] = "Available"
            
            elif list1[i] == "e2\x00\x00\x17E\x18\x01)%\x90\x16\xe0":
                stock.loc[14, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00\x00\x17E\x18\x01&%\x10\x16\xd7":
                stock.loc[15, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x19\x10RA":
                stock.loc[16, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00\x00\x17E\x18\x010%\x10\x16\xe5":
                stock.loc[17, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x10\x10\xb3h":
                stock.loc[18, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x14\x10\x87\xa0":
                stock.loc[19, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x19\x10RA":
                stock.loc[20, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x11 \xa8\xd1":
                stock.loc[21, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x11\x80\xa0\x1e":
                stock.loc[22, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x16\x10q ":
                stock.loc[23, "Status"] = "Available"
            
            
        stock.to_csv("Stock.csv", index=False, encoding='utf8')
        stock = pd.read_csv("Stock.csv")
        
        
        for i in range (0, len(stock["Name"])):
            if stock.loc[i]["Status"] == "Available":
                #print (stock.loc[[i]])
                #print ("\n--------------------------------------------------------")
                print ("\nName:    " + str(stock.loc[i]["Name"]))
                #print ("\nType:    " + str(stock.loc[i]["Type"]))
                #print ("\nRoom No. " + str(stock.loc[i]["Room Location"]))
                #print ("\nCTB No.  " + str(stock.loc[i]["CTB Location"]))
                #print ("\nType:    " + str(stock.loc[i]["Type"]))
                #print ("\nStatus:  " + str(stock.loc[i]["Status"]))
                #print ("\n--------------------------------------------------------")


    #Option 2
    elif option == 2:
        
        
        list1 = read.ReadMultiTag()
    
        for i in range(0, len(stock["Name"])):
            stock.loc[i, "Status"] = "Unavailable"
    
        for i in range(0, len(list1)):
            if list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x16pl\xa3":
                stock.loc[0, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x17@a\x87":
                stock.loc[1, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x15\x00|`":
                stock.loc[2, "Status"] = "Available"
            
            elif list1[i] == "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04":
                stock.loc[3, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00\x00\x17E\x18\x011%\x10\x16\xed":
                stock.loc[4, "Status"] = "Available"
            
            elif list1[i] == "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05":
                stock.loc[5, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00\x00\x17E\x18\x013%\x10\x16\xee":
                stock.loc[6, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00\x00\x17E\x18\x012%\x10\x16\xe6":
                stock.loc[7, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x16\x10q":
                stock.loc[8, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x15\x10~\x9c":
                stock.loc[9, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x19\x00P\x1d":
                stock.loc[10, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x18PV\x96":
                stock.loc[11, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00\x00\x17E\x18\x01(%\x10\x16\xd8":
                stock.loc[12, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00\x00\x17E\x18\x01'%\x10\x16\xdf":
                stock.loc[13, "Status"] = "Available"
            
            elif list1[i] == "e2\x00\x00\x17E\x18\x01)%\x90\x16\xe0":
                stock.loc[14, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00\x00\x17E\x18\x01&%\x10\x16\xd7":
                stock.loc[15, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x19\x10RA":
                stock.loc[16, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00\x00\x17E\x18\x010%\x10\x16\xe5":
                stock.loc[17, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x10\x10\xb3h":
                stock.loc[18, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x14\x10\x87\xa0":
                stock.loc[19, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x19\x10RA":
                stock.loc[20, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x11 \xa8\xd1":
                stock.loc[21, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x11\x80\xa0\x1e":
                stock.loc[22, "Status"] = "Available"
            
            elif list1[i] == "\xe2\x00Q\x80\x00\x0e\x01@\x16\x10q ":
                stock.loc[23, "Status"] = "Available"
            
            
        stock.to_csv("Stock.csv", index=False, encoding='utf8')
        stock = pd.read_csv("Stock.csv")
        
        name = raw_input("\n\nEnter the name of the product: ")
        tot_count = 0
        inv_count = 0
        for i in range (0, len(stock["Name"])):
                if stock.loc[i]["Name"].lower() == name.lower():
                    tot_count += 1
                    if stock.loc[i]["Status"] == "Available":
                        inv_count += 1
                    #print (stock.loc[[i]])
                    print ("\n--------------------------------------------------------")
                    print ("\nName:    " + str(stock.loc[i]["Name"]))
                    print ("\nType:    " + str(stock.loc[i]["Type"]))
                    print ("\nRoom No. " + str(stock.loc[i]["Room Location"]))
                    print ("\nCTB No.  " + str(stock.loc[i]["CTB Location"]))
                    print ("\nType:    " + str(stock.loc[i]["Type"]))
                    print ("\nStatus:  " + str(stock.loc[i]["Status"]))
                    print ("\n--------------------------------------------------------")



        print ("\n\nTotal Quantity: " + str(tot_count))
        print ("\nQuantity in Inventory: " + str(inv_count))
    
    
    #Option 3
    elif option == 3:
        print("\n\nBye\n\n")
        flag = 1
        break
    
    else:
        print ("\n\nInvalid Input\n\n")



