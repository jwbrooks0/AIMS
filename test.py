
"""
This code is just a test of the functions of this library.  
"""

# import libraries
import LCD2004 as lcd
import button
import time
import m5e
import RPi.GPIO as GPIO
import pandas as pd
import numpy as np

# instruct the RPi to ignore warnings
GPIO.setwarnings(False)

# initialize the LCD screen
lcd1=lcd.LCD()
lcd1.write_to_LCD(["","Awaiting","a command",""])
lcd1.toggle_backlight(True)

# initialize the buttons
b1 = button.button(5)
b2 = button.button(6)

# initialize database and database functions
def lookupTag(df,tagID='0xe2 0x0 0x51 0x80 0x0 0xe 0x1 0x40 0x12 0x60 0x97 0x57 '):
	try:
		return df.loc[tagID]['Item'],df.loc[tagID]['Location']
	except:
        	output=[]
		output.append('Tag not recognized')
		count=0
		while(len(tagID)>0):
			if len(tagID)>=20:
				output.append(tagID[0:20])
				tagID=tagID[20:]
			else:
				output.append(tagID[0:len(tagID)])
				tagID=[]
			count+=1
			if count==3:
				tagID=[]
		lcd1.write_to_LCD(output)
		return 'NA',0
	
def investigateBox(df,boxNum=1):
	
	tagIDs=reader.ReadMultiTag()
	lcd1.write_to_LCD(["Read all tags","total count: %d"%len(tagIDs),"",""],justification='left')
		
	
	print("")
	print("Tags found in SCTB #%d"%boxNum)
	print("")
	print("Item \t \t Location")
	print("----             --------")
	
	for i in range(0,len(tagIDs)):
		data=tagIDs[i]
		item,loc=lookupTag(df,data)
		print("%s \t %d"%(item,loc))
		
	print("")
	print("In the wrong SCTB")
	print("")
	print("Item \t \t Location")
	print("----             --------")
	for i in range(0,len(tagIDs)):
		result=tagIDs[i] in df.loc[df['Location']==1].index
		
		# if in the wrong box
		if result==False:
			t1,t2=lookupTag(df,tagIDs[i])
			print("%s \t %d" % (t1,t2))
			
	print("")
	print("Missing fron SCTB #%d" % boxNum)
	print("")
	print("Item \t \t Location")
	print("----             --------")
	boxList=np.array(df.loc[df['Location']==1].index)
	for i in range(0,len(boxList)):
		result=boxList[i] in tagIDs
		if result==False:
			t1,t2=lookupTag(df,boxList[i])
			print("%s \t %d" % (t1,t2))
	
            
df=pd.read_csv('tagIDList.csv',index_col=0)


# initialize the M5e rfid reader
reader = m5e.M5e()

# main loop
while(True):
	if b1.buttonStatus()==1:
		data=reader.ReadSingleTag()
		print(data)
		item,loc=lookupTag(df,data)
		if item!='NA':
			lcd1.write_to_LCD(["Read Single Tag","ID: %s" % data[-17:-1],"Item: %s"%item,"SCTB Number: %d"%loc],justification='left')
	if b2.buttonStatus()==1:
#        	data=reader.ReadMultiTag()
		investigateBox(df,1)
	time.sleep(0.3)
