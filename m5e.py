"""
Thing Magic M5e and M5e-Compact Python Interface
Originally Written by Travis Deyle [tdeyle@gatech.edu] under the tutelage of 
Dr. Matt Reynolds (Duke University) and Dr. Charlie Kemp (Georgia Tech)
Please remember me if you become rich and/or famous, and please  
refer to our related work(s) when writing papers.  Thanks.

Latest version written by John Brooks [jwbrooks0@gmail.com]
"""

## Import libraries
import serial, time #,sys
#from threading import Thread
#from time import time
from time import sleep

## Main class
class M5e:
	"""Interface to Mercury M5e and M5e-Compact"""
	
	def __init__(self, portINT=-1, portSTR='/dev/ttyS0', baudrate=9600, 
		TXport=1, RXport=1, readPwr=2300, protocol='GEN2', compact=True, verbosity=True):
		""" Initialize m5e """
		if portINT != -1:
			self.port = portINT	# stores the serial port as 0-based integer
		else:
			self.port = portSTR	# stores it as a /dev-mapped string

		self.port=portSTR
		
		self.baudrate = baudrate	# should be 9600 for M5e by default.  May want to up the baud for faster reading (after bootup)
		self.TXport = TXport		# Initialized transmit antenna
		self.RXport = RXport		# Initialized receive antenna
		self.readPwr = readPwr	  # Initialized read TX power in centi-dBm
		self.protocol = protocol	# Initialized protocol
		self.compact = compact
		self.verbosity = verbosity
		self.ser = None
		
		if verbosity == True:
			print('Initializing M5e (or M5e-Compact)')
		
		# Setup Serial port  
		self._initSerialConnection()

		# Check if BootLoader is running by issuing "Get BootLoader/Firmware Version"		
		self._TransmitCommand('\x00\x03')
		self._ReceiveResponse()	  # automatically makes sure returned status = 0x0000
		
		# Boot into Firmware
		self._TransmitCommand('\x00\x04')
		try:
			self._ReceiveResponse()
		except M5e_CommandStatusError, inst:
			# Non-Zero Response will be received if the reader has already booted into firmware
			#   This occurs when you've already powered-up & previously configured the reader.  
			#   Can safely ignore this problem and continue initialization
				if inst[1] == '\x01\x01':	   # This actually means "invalid opcode"
					pass
				else:
					raise
		
		# setup antenna
		#self._ChangeAntennaPorts(self.TXport, self.RXport)
		self._ChangeTXReadPower(self.readPwr)
				
		# Set Tag Protocol to GEN2
		if self.protocol != 'GEN2':
			raise M5e_error('Sorry, GEN2 is only protocol supported at this time')
		self._TransmitCommand('\x02\x93\x00\x05')
		self._ReceiveResponse()
		
		# Set Region (we're only going to deal with North America)
		self._TransmitCommand('\x01\x97\x01')
		self._ReceiveResponse()
		
		
	def _initSerialConnection(self):
		"""
		Initializes serial port to m5e unit
		"""
		print('\tAttempting 9600 bps')
		try:
			self.ser = serial.Serial(self.port, 9600, timeout=2, writeTimeout=2)
			self._TransmitCommand('\x00\x03')
			self._ReceiveResponse()	  # automatically makes sure returned status = 0x0000
			print('\tSuccessful @ 9600 bps')
		except:
			print('\tFailed 9600 bps')
			self.ser = None
			raise M5e_SerialPortError('Could not open serial port %d at baudrate %d or %d.' % (self.port,230400,9600))
		
		if self.ser == None:
			raise M5e_SerialPortError('Could not open serial port %d at baudrate %d or %d.' % (self.port,230400,9600))
  
		
	def _countTagBufferSize(self):
		# Returns the number of tags stored in the buffer
		self._TransmitCommand('\x00\x29')
		(start, length, command, status, data, CRC) = self._ReceiveResponse()
		print("Num Tags in Buffer = %d" % ord(data[3]))
		return ord(data[3]) #i'm assuming here that only the last character contains a number, meaning there are less than 256 tags in the buffer


	def _readEntireTagBuffer(self):
		"""
		Returns all Tag IDs stored in the buffer
		"""
		# first, get the number of tags in the buffer
		count = self._countTagBufferSize()

		# init list for tag ID strings
		newIDS=[]
		#print "readbuffercommand = %s" % self.ReturnHexString('\x02\x29'+'\x00'+chr(count))

		# send command and receive response
		self._TransmitCommand('\x02\x29'+'\x00'+chr(count))
		(start, length, command, status, data, CRC) = self._ReceiveResponse()

		# this next bit of code pulls out multiple tag IDs from a long list of possible IDs.
		index=data.find('\x00\x80')
		while index != -1:
			newIDS.append(data[index+4:index+16])
			data=data[(index+1):]
			index=data.find('\x00\x80')

		# clear tag bugger after reading it.  
		self._clearTagBuffer()

		return newIDS


	def _clearTagBuffer(self):
		# clears tag buffer
		self._TransmitCommand('\x00\x2a')
		self._ReceiveResponse()
		

	def _serialClose(self):
		# close serial port
		self.ser.close()


	def ReadSingleTag(self):
		"""returns tag ID for first tag that responds"""
		self._TransmitCommand('\x02\x21\x03\xe8') # 03e8 in hex equals 1000 in decimal.  units in ms.  1000 ms = 1 s.  
		(start, length, command, status, data, CRC) = self._ReceiveResponse()
		if status == '\x04\x00':
			print("No tag found")
			return ""
		else:
			print("ReadID = %s" % self._ReturnHexString(data[0:12]))
			return self._ReturnHexString(data[0:12])


	def ReadMultiTag(self):
		"""read multiple tag IDs and places them in the tag buffer"""

		self._clearTagBuffer();

		self._TransmitCommand('\x02\x22\x03\xe8') # 03e8 in hex equals 1000 in decimal.  units in ms.  1000 ms = 1 s.  
		(start, length, command, status, data, CRC) = self._ReceiveResponse()

		sleep(.1)

		return self._readEntireTagBuffer();

 
	def _ChangeAntennaPorts(self, TXport, RXport):
		"""Changes TX and RX ports"""
		self.TXport = TXport
		self.RXport = RXport
		self._TransmitCommand('\x02\x91' + chr(self.TXport) + chr(self.RXport))
		self._ReceiveResponse()
		
		
	def _ChangeTXReadPower(self, readPwr):
		"""Sets the Read TX Power based on current value of readPwr (in centi-dBm)"""
		self.readPwr = readPwr
		readTXPwrHighByte = chr((self.readPwr & 0xFFFF) >> 8)
		readTXPwrLowByte = chr(self.readPwr & 0x00FF)
		self._TransmitCommand('\x02\x92'+ readTXPwrHighByte + readTXPwrLowByte)
		self._ReceiveResponse()
		
		
	def _CalculateCRC(self, msg):
		"""Implements CCITT CRC-16 defined in Mercury Embedded Module Dev Guide."""
		crcResult = 0xFFFF
		for x in range(len(msg)):
			currChar = ord(msg[x])
			v = 0x80
			for y in range(8):
				xor_flag = 0
				if (crcResult & 0x8000):
					xor_flag = 1
				crcResult = crcResult << 1
				if (currChar & v):
					crcResult = crcResult + 1
				if (xor_flag):
					crcResult = crcResult ^ 0x1021
				v = v >> 1
				crcResult = crcResult & 0xFFFF
			#print hex(currChar)
		return chr((crcResult >> 8) & 0xFF) + chr(crcResult & 0xFF)
		# return the 16-bit result in the form of 2 characters


	def _ReturnHexString(self, hexStr):
		"Helper function to visualize a hex string (such as a hexCommand)"
		result = ''
		for i in range(len(hexStr)):
			result = result + hex(ord(hexStr[i])) + ' '
		return result


	def _ConstructCommand(self, hexCommand):
		"Helper function to attach start byte and CRC to a command string"
		return '\xFF' + hexCommand + self._CalculateCRC(hexCommand)


	def _TransmitCommand(self, command):
		"Transmits a command.  Should call ReceiveResponse before calling again."
		try:
			self.ser.write(self._ConstructCommand(command))
		except:
			raise M5e_TransmitTimeoutExceeded('Something happened (probably power failure) to disable serial transmission')
		
	def _ReceiveResponse(self):
		if self.verbosity==True:
			printAll=True
		else:
			printAll=False
		"Receives a single command's response"
		# Get Start byte, disregard anything else...
		timeoutsToWait = 5
		timeoutsWaited = 0

		while timeoutsWaited < timeoutsToWait:
			start = self.ser.read()		# this is non-blocking.  Will wait for timeout duration, then return
			if start == '\xFF':
				break
			timeoutsWaited += 1
			
		if printAll==True:
			print("start = %s" % self._ReturnHexString(start))
		if start != '\xFF':
			time.sleep(5)
			self.ser.flushInput()
			raise M5e_ReceiveError('Error in receive stream (start byte).  Waited 5 seconds then flushed input.  Try reissueing command and receive response.')
			
		length = self.ser.read()		# non blocking, returns after timeout
		if printAll==True:
			print("length = %s" % self._ReturnHexString(length))
		if len(length) != 1:
			time.sleep(5)
			self.ser.flushInput()
			raise M5e_ReceiveError('Error in receive stream (length byte).  Waited 5 seconds then flushed input.  Try reissueing command and receive response.')

		command = self.ser.read()
		if printAll==True:
			print("command = %s" % self._ReturnHexString(command))
		if len(command) != 1:
			time.sleep(5)
			self.ser.flushInput()
			raise M5e_ReceiveError('Error in receive stream (command byte).  Waited 5 seconds then flushed input.  Try reissueing command and receive response.')

		status = self.ser.read(2)	   # non-blocking
		if printAll==True:
			print("status = %s" % self._ReturnHexString(status))
		if len(status) != 2:
			time.sleep(5)
			self.ser.flushInput()
			raise M5e_ReceiveError('Error in receive stream (status bytes).  Waited 5 seconds then flushed input.  Try reissueing command and receive response.')

		data = self.ser.read(ord(length))
		if printAll==True:
			print("data = %s" % self._ReturnHexString(data))
		if len(data) != ord(length):
			time.sleep(5)
			self.ser.flushInput()
			raise M5e_ReceiveError('Error in receive stream (data bytes).  Waited 5 seconds then flushed input.  Try reissueing command and receive response.')

		CRC = self.ser.read(2)
		if printAll==True:
			print("CRC = %s" % self._ReturnHexString(CRC))
		if len(CRC) != 2:
			time.sleep(5)
			self.ser.flushInput()
			raise M5e_ReceiveError('Error in receive stream (CRC bytes).  Waited 5 seconds then flushed input.  Try reissueing command and receive response.')
		
		# Validate the CRC
		validateCRC = length + command + status + data
		if self._CalculateCRC(validateCRC) != CRC:
			raise M5e_CRCError('Received response CRC failed')
		
		# Check if return status was OK (0x0000 is success)
		if status != '\x00\x00':
			# raise eror and halt code
			#raise M5e_CommandStatusError('Received response returned non-zero status',status)

			# print error but continue
			print('Received response returned non-zero status' + str(status))
			
		return (start, length, command, status, data, CRC)
	
		
	def _QueryEnvironment(self, timeout=50):
		# Read Tag ID Multiple
		timeoutHighByte = chr((timeout & 0xFFFF) >> 8)
		timeoutLowByte = chr(timeout & 0x00FF)
		try:
			self._TransmitCommand('\x04\x22\x00\x00'+timeoutHighByte+timeoutLowByte)
			self._ReceiveResponse()
		except M5e_CommandStatusError, inst:
			flag = False
			# Read & Get returns non-zero status when no tags found.  This is 
			#   an expected event... so ignore the exception.
			if inst[1] == '\x04\x00':   
				return []
			else:
				raise

		# Get Tag Buffer
		#   Get # Tags remaining
		self._TransmitCommand('\x00\x29')
		(start, length, command, status, data, CRC) = self._ReceiveResponse()
		
		readIndex = (ord(data[0]) << 8) + ord(data[1])
		writeIndex = (ord(data[2]) << 8) + ord(data[3])
		numTags = writeIndex - readIndex
		
#		 tagEPCs = []
#		 while numTags > 0:
#			 numFetch = min([numTags, 13])
#			 numFetchHighByte = chr((numFetch & 0xFFFF) >> 8)
#			 numFetchLowByte = chr(numFetch & 0x00FF)
#			 self.TransmitCommand('\x02\x29' + numFetchHighByte + numFetchLowByte)
#			 (start, length, command, status, data, CRC) = self.ReceiveResponse()
			
#			 # each tag occupies 18 bytes in the response, regardless of tag size
#			 for i in range(numFetch): # NOTE: first 4 bytes in GEN2 are size & protocol.  Last 2 are CRC
#				 tagEPCs.append(data[i*18+4:(i+1)*18-2])
#				 #tagEPCs.append(data[i*18:(i+1)*18])
			
#			 numTags = numTags - numFetch

		results = []   # stored as (ID, RSSI)
		while numTags > 0:
			self._TransmitCommand('\x03\x29\x00\x02\x00')
			(start, length, command, status, data, CRC) = self._ReceiveResponse()

			tagsRetrieved = ord(data[3])
			for i in xrange(tagsRetrieved):
				rssi = ord(data[4 + i*19])
				tagID = data[4 + i*19 + 5 : 4 + i*19 + 5 + 12]
				results.append( (tagID, rssi) )
			
			numTags = numTags - tagsRetrieved
			
		# Reset/Clear the Tag ID Buffer for next Read Tag ID Multiple
		self._TransmitCommand('\x00\x2A')
		self._ReceiveResponse()
			
		return results
	
	def _TrackSingleTag(self, tagID, timeout=50):
		# Make sure TagID is 60-bits
		if len(tagID) != 12:
			raise M5e_Error('Only 96-bit tags supported by TrackSingleTag')
		
		timeoutHighByte = chr((timeout & 0xFFFF) >> 8)
		timeoutLowByte = chr(timeout & 0x00FF)
		try:
			self._TransmitCommand('\x12\x21'+timeoutHighByte+timeoutLowByte+'\x11\x00\x02\x60'+tagID)
			(start, length, command, status, data, CRC) = self._ReceiveResponse()
			# data is in form OptionsFlags (1 byte) MetaFlags (2 bytes) RSSI (1 byte), EPC (12 bytes data[-14:-2]) TAG CRC (2 bytes)
		except M5e_CommandStatusError, inst:
			flag = False
			# Read & Get returns non-zero status when no tags found.  This is 
			#   an expected event... so ignore the exception.
			if inst[1] == '\x04\x00':   
				return -1   # Requested tag not found
			else:
				raise
			
		return ord(data[3])

	def ChangeTagID(self, newTagID=b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01', timeout=50):
		# Note: This will rewrite the EPC on the first tag detected!
		# newTagID can be a string of 12 hex bytes or it can be an integer (which the code will then convert to a 12 hex byte string)
		
		# if newTagID is an int, convert it to a 12 hex byte string
		if type(newTagID) is int:
			newTagID=chr(newTagID)
			
			while(len(newTagID) < 12):
				newTagID='\x00'+newTagID

		# Make sure TagID is 12 hex bytes
		if len(newTagID) != 12:
			raise M5e_Error('Only 96-bit tags supported by TrackSingleTag')
		
		timeoutHighByte = chr((timeout & 0xFFFF) >> 8)
		timeoutLowByte = chr(timeout & 0x00FF)
		try:
			cmdLen = chr(len(newTagID)+4)
			self._TransmitCommand(cmdLen+'\x23'+timeoutHighByte+timeoutLowByte+'\x00\x00'+newTagID)
			(start, length, command, status, data, CRC) = self._ReceiveResponse()
		except M5e_CommandStatusError, inst:
			return False
			
		return True 
	
	def _QuickQuery(self):
		#prints data to a log file once
		while True:
			try:
				logname = str(raw_input("Please enter the name of the target log file: "))
				break
			except IOError:
				print("The log file name must be valid.")
		
		path = '/home/createbrain/Desktop/hospirfidbot/logs/' + logname
		f = file(path, 'w')	 #this line and the next generate the log file
		f.close()
		t = str(time())
		data = self._QueryEnvironment()
		print(t)
		print(data)
		f = open(path, 'r+')	 # this method does not handle exceptions
		f.seek(0, 2)
		f.write(t)
		for i in data:
			a1, a2 = i
			f.write(' ' + a1.encode("hex") + ' ' + str(a2))
		f.write('\n')
		f.close()
		del data
		
	def _LoopQuery(self):
		#indefinitely prints data to a log file
		while True:
			try:
				logname = str(raw_input("Please enter the name of a new log file: "))
				break
			except IOError:
				print("The logfile name must be valid.")
		while True:
			try:
				timeout = str(raw_input("Timeout (default is 50 in ms): "))
				break
			except IOError:
				print("The timer must be valid.")
		
		path = '/home/createbrain/Desktop/hospirfidbot/logs/' + logname
		#remove(path)		 #delete current log file
		f = file(path, 'w')	 #this line and the next generate the log file
		f.close()
		tin = int(timeout)
		while 1:
			t = str(time())
			data = self._QueryEnvironment(tin)
			print(t)
			print(data)
			with open(path, 'r+') as f:	# this method handles exceptions (supposedly)
				f.seek(0, 2)
				f.write(t + ' ' + str(len(data)))
				for i in data:
				   a1, a2 = i
				   f.write(' ' + a1.encode("hex") + ' ' + str(a2))
				f.write('\n')
				f.close()
		 #   f = open(path, 'r+')	 # this method does not handle exceptions
		 #   f.seek(0, 2)
		 #   f.write(t)
		 #   for i in data:
		 #	   a1, a2 = i
		 #	   f.write(' ' + str(a1) + ' ' + str(a2))
		 #   f.write('\n')
		 #   f.close()
			del data
		return

class M5e_error(Exception):
	"General Exception"
	pass

class M5e_SerialPortError(M5e_error):
	"If pyserial throws error"
	pass
	
class M5e_CRCError(M5e_error):
	"If CRC check from Mercury packet is incorrect (data corruption)"
	pass
	
class M5e_CommandStatusError(M5e_error):
	"If return response from Mercury is non-zero (error status)"
	pass

class M5e_TransmitTimeoutExceeded(M5e_error):
	"Something happened (probably power failure) to disable serial transmission"
	pass

class M5e_ReceiveError(M5e_error):
	"Serial input out of synch.  Try waiting a few seconds, flush input stream, and reissue command"
	pass


## THIS IS THE "DIRECT" METHOD...
##if __name__ == '__main__':
##	import time
##	import numpy as np
##	
##	read = M5e(portSTR='/dev/ttyUSB0', baudrate=230400)   
##
##	# Demonstrate Querying the environment
##	for i in range(5):
##		print read._QueryEnvironment()
##		time.sleep(1)
##		
##	# To track tags' RSSI
##	tags = read._QueryEnvironment()
##	for tag in tags:
##		print [tag], read.TrackSingleTag(tag)

