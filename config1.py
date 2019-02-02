
"""
This code is just a test of the functions of this library.  
"""

# import libraries
#import LCD2004 as lcd
#import button
import time
import m5e
import RPi.GPIO as GPIO
import pandas as pd
#import numpy as np
from AIMS import aimsLib

# instruct the RPi to ignore warnings
GPIO.setwarnings(False)

# initialize the LCD screen
#lcd1=lcd.LCD()
#lcd1.write_to_LCD(["","Awaiting","a command",""])
#lcd1.toggle_backlight(True)

# initialize the buttons
#b1 = button.button(5)
#b2 = button.button(6)


# initialize the M5e rfid reader
reader = m5e.M5e()


	
# initialize the database
df=pd.read_csv('tagIDList.csv',index_col=0)

# code
aimsLib.investigateBox(df,reader,None,1)


## main loop
#while(True):
#	if b1.buttonStatus()==1:
#		data=reader.ReadSingleTag()
#		print(data)
#		item,loc=lookupTag(df,data)
#		if item!='NA':
#			lcd1.write_to_LCD(["Read Single Tag","ID: %s" % data[-17:-1],"Item: %s"%item,"SCTB Number: %d"%loc],justification='left')
#	if b2.buttonStatus()==1:
##        	data=reader.ReadMultiTag()
#		investigateBox(df,1)
#	time.sleep(0.3)
