
# coding: utf-8

# In[1]:


import pandas as pd

#LCD
import LCD2004 as lcd
display = lcd.LCD()
display.toggle_backlight(True)
#reload(lcd) command to update



#import button library
import button
b1 = button.button(5)
b2 = button.button(6)
    
#Reader
import m5e
read = m5e.M5e()

stock = pd.read_csv("Stock.csv")

flag = 0
while (flag == 0):
    if b1.buttonStatus() == 1:
        
        print ("\n\nShow the RFID tag to the Scanner\n\n")
        code = read.ReadSingleTag()
        quantity = 0
    
        #for i in range (0, len(stock["ID"])):
        if code == "\xe2\x00Q\x80\x00\x0e\x01@\x16pl\xa3":
            print ("\n\nItem:    " + str(stock.loc[0]["Name"]))
            print ("\nRoom No. " + str(stock.loc[0]["Room Location"]))
            print ("\nCTB No.  " + str(stock.loc[0]["CTB Location"]))
            i = 0
            
        elif code == "\xe2\x00Q\x80\x00\x0e\x01@\x17@a\x87":
            print ("\n\nItem:    " + str(stock.loc[1]["Name"]))
            print ("\nRoom No. " + str(stock.loc[1]["Room Location"]))
            print ("\nCTB No.  " + str(stock.loc[1]["CTB Location"]))
            i = 1
            
        elif code == "\xe2\x00Q\x80\x00\x0e\x01@\x15\x00|`":
            print ("\n\nItem:    " + str(stock.loc[2]["Name"]))
            print ("\nRoom No. " + str(stock.loc[2]["Room Location"]))
            print ("\nCTB No.  " + str(stock.loc[2]["CTB Location"]))
            i = 2
            
        elif code == "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04":
            print ("\n\nItem:    " + str(stock.loc[3]["Name"]))
            print ("\nRoom No. " + str(stock.loc[3]["Room Location"]))
            print ("\nCTB No.  " + str(stock.loc[3]["CTB Location"]))
            i = 3
            
        elif code == "\xe2\x00\x00\x17E\x18\x011%\x10\x16\xed":
            print ("\n\nItem:    " + str(stock.loc[4]["Name"]))
            print ("\nRoom No. " + str(stock.loc[4]["Room Location"]))
            print ("\nCTB No.  " + str(stock.loc[4]["CTB Location"]))
            i = 4
            
        elif code == "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05":
            print ("\n\nItem:    " + str(stock.loc[5]["Name"]))
            print ("\nRoom No. " + str(stock.loc[5]["Room Location"]))
            print ("\nCTB No.  " + str(stock.loc[5]["CTB Location"]))
            i = 5
            
        elif code == "\xe2\x00\x00\x17E\x18\x013%\x10\x16\xee":
            print ("\n\nItem:    " + str(stock.loc[6]["Name"]))
            print ("\nRoom No. " + str(stock.loc[6]["Room Location"]))
            print ("\nCTB No.  " + str(stock.loc[6]["CTB Location"]))
            i = 6
            
        elif code == "\xe2\x00\x00\x17E\x18\x012%\x10\x16\xe6":
            print ("\n\nItem:    " + str(stock.loc[7]["Name"]))
            print ("\nRoom No. " + str(stock.loc[7]["Room Location"]))
            print ("\nCTB No.  " + str(stock.loc[7]["CTB Location"]))
            i = 7
            
        elif code == "\xe2\x00Q\x80\x00\x0e\x01@\x16\x10q":
            print ("\n\nItem:    " + str(stock.loc[8]["Name"]))
            print ("\nRoom No. " + str(stock.loc[8]["Room Location"]))
            print ("\nCTB No.  " + str(stock.loc[8]["CTB Location"]))
            i = 8
            
        elif code == "\xe2\x00Q\x80\x00\x0e\x01@\x15\x10~\x9c":
            print ("\n\nItem:    " + str(stock.loc[9]["Name"]))
            print ("\nRoom No. " + str(stock.loc[9]["Room Location"]))
            print ("\nCTB No.  " + str(stock.loc[9]["CTB Location"]))
            i = 9
            
        elif code == "\xe2\x00Q\x80\x00\x0e\x01@\x19\x00P\x1d":
            print ("\n\nItem:    " + str(stock.loc[10]["Name"]))
            print ("\nRoom No. " + str(stock.loc[10]["Room Location"]))
            print ("\nCTB No.  " + str(stock.loc[10]["CTB Location"]))
            i = 10
            
        elif code == "\xe2\x00Q\x80\x00\x0e\x01@\x18PV\x96":
            print ("\n\nItem:    " + str(stock.loc[11]["Name"]))
            print ("\nRoom No. " + str(stock.loc[11]["Room Location"]))
            print ("\nCTB No.  " + str(stock.loc[11]["CTB Location"]))
            i = 11
            
        elif code == "\xe2\x00\x00\x17E\x18\x01(%\x10\x16\xd8":
            print ("\n\nItem:    " + str(stock.loc[12]["Name"]))
            print ("\nRoom No. " + str(stock.loc[12]["Room Location"]))
            print ("\nCTB No.  " + str(stock.loc[12]["CTB Location"]))
            i = 12
            
        elif code == "\xe2\x00\x00\x17E\x18\x01'%\x10\x16\xdf":
            print ("\n\nItem:    " + str(stock.loc[13]["Name"]))
            print ("\nRoom No. " + str(stock.loc[13]["Room Location"]))
            print ("\nCTB No.  " + str(stock.loc[13]["CTB Location"]))
            i = 13
            
        elif code == "e2\x00\x00\x17E\x18\x01)%\x90\x16\xe0":
            print ("\n\nItem:    " + str(stock.loc[14]["Name"]))
            print ("\nRoom No. " + str(stock.loc[14]["Room Location"]))
            print ("\nCTB No.  " + str(stock.loc[14]["CTB Location"]))
            i = 14
            
        elif code == "\xe2\x00\x00\x17E\x18\x01&%\x10\x16\xd7":
            print ("\n\nItem:    " + str(stock.loc[15]["Name"]))
            print ("\nRoom No. " + str(stock.loc[15]["Room Location"]))
            print ("\nCTB No.  " + str(stock.loc[15]["CTB Location"]))
            i = 15
            
        elif code == "\xe2\x00Q\x80\x00\x0e\x01@\x19\x10RA":
            print ("\n\nItem:    " + str(stock.loc[16]["Name"]))
            print ("\nRoom No. " + str(stock.loc[16]["Room Location"]))
            print ("\nCTB No.  " + str(stock.loc[16]["CTB Location"]))
            i = 16
            
        elif code == "\xe2\x00\x00\x17E\x18\x010%\x10\x16\xe5":
            print ("\n\nItem:    " + str(stock.loc[17]["Name"]))
            print ("\nRoom No. " + str(stock.loc[17]["Room Location"]))
            print ("\nCTB No.  " + str(stock.loc[17]["CTB Location"]))
            i = 17
            
        elif code == "\xe2\x00Q\x80\x00\x0e\x01@\x10\x10\xb3h":
            print ("\n\nItem:    " + str(stock.loc[18]["Name"]))
            print ("\nRoom No. " + str(stock.loc[18]["Room Location"]))
            print ("\nCTB No.  " + str(stock.loc[18]["CTB Location"]))
            i = 18
            
        elif code == "\xe2\x00Q\x80\x00\x0e\x01@\x14\x10\x87\xa0":
            print ("\n\nItem:    " + str(stock.loc[19]["Name"]))
            print ("\nRoom No. " + str(stock.loc[19]["Room Location"]))
            print ("\nCTB No.  " + str(stock.loc[19]["CTB Location"]))
            i = 19
            
        elif code == "\xe2\x00Q\x80\x00\x0e\x01@\x19\x10RA":
            print ("\n\nItem:    " + str(stock.loc[20]["Name"]))
            print ("\nRoom No. " + str(stock.loc[20]["Room Location"]))
            print ("\nCTB No.  " + str(stock.loc[20]["CTB Location"]))
            i = 20
            
        elif code == "\xe2\x00Q\x80\x00\x0e\x01@\x11 \xa8\xd1":
            print ("\n\nItem:    " + str(stock.loc[21]["Name"]))
            print ("\nRoom No. " + str(stock.loc[21]["Room Location"]))
            print ("\nCTB No.  " + str(stock.loc[21]["CTB Location"]))
            i = 21
            
        elif code == "\xe2\x00Q\x80\x00\x0e\x01@\x11\x80\xa0\x1e":
            print ("\n\nItem:    " + str(stock.loc[22]["Name"]))
            print ("\nRoom No. " + str(stock.loc[22]["Room Location"]))
            print ("\nCTB No.  " + str(stock.loc[22]["CTB Location"]))
            i = 22
            
        elif code == "\xe2\x00Q\x80\x00\x0e\x01@\x16\x10q ":
            print ("\n\nItem:    " + str(stock.loc[23]["Name"]))
            print ("\nRoom No. " + str(stock.loc[23]["Room Location"]))
            print ("\nCTB No.  " + str(stock.loc[23]["CTB Location"]))
            i = 23
            
        else:
            print ("\n\nUnable to Scan Item\n\n")
            continue
            
        for j in range (0, len(stock["ID"])):
            if i != j:
                    
                if stock.loc[j]["Name"].lower == stock.loc[i]["Name"].lower:
                    if stock.loc[j]["Status"] == "Available":
                        quantity += 1
                                
        if quantity == 0:
            print ("\nYou have nothing left in the stock!\n\n")
        else:
            print ("\nYou have " + str(quantity) + " more left in the stock!\n\n")
                    
        display.write_to_LCD([str(stock.loc[i]["Name"]), "Room No. " + str(stock.loc[i]["Room Location"]), "CTB No." + str(stock.loc[i]["CTB Location"]), "Quantity: " + str(quantity)])
            
    elif b2.buttonStatus() == 1:
        print ("\n\nBye\n\n")
        flag = 1
                    

