#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 12:51:52 2019

@author: john
"""
import numpy as _np

# initialize database and database functions
def lookupTag(df,lcd,tagID='0xe2 0x0 0x51 0x80 0x0 0xe 0x1 0x40 0x12 0x60 0x97 0x57 '):
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
		lcd.write_to_LCD(output)
		return 'NA',0
	
	
# investigate the contents of a SCTB and display findings
def investigateBox(df,reader,lcd,boxNum=1):
	
	tagIDs=reader.ReadMultiTag()
	
	if type(reader)!=type(None):
		lcd.write_to_LCD(["Read all tags","total count: %d"%len(tagIDs),"",""],justification='left')
		
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
	boxList=_np.array(df.loc[df['Location']==1].index)
	for i in range(0,len(boxList)):
		result=boxList[i] in tagIDs
		if result==False:
			t1,t2=lookupTag(df,boxList[i])
			print("%s \t %d" % (t1,t2))