#!/usr/bin/python
#--------------------------------------
#
#  lcd2004.py
#  20x4 LCD Test Script with
#  backlight control and text justification
#
# https://www.sunfounder.com/
#
#--------------------------------------
 
# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND

#import
import RPi.GPIO as _GPIO
import time as _time

class LCD:
	"""
	Allows user to establish a connection and control of an attached LCD2004 panel using a raspberry pi.  

	Inputs
	---------
	LCD_RS : int
		R.Pi pin mapping to LCD2004 pin.  register pin that controls where in the LCD's memory you are writing data to.  
	LCD_E : int
		R.Pi pin mapping to LCD2004 pin.  enabling pin that reads the information when High level (1) is received.  The instructions are run when the signal changes from High level to Low level.
	LCD_D4 : int
		R.Pi pin mapping to LCD2004 pin.  read/write digital pin 4
	LCD_D5 : int
		R.Pi pin mapping to LCD2004 pin.  read/write digital pin 5
	LCD_D6 : int
		R.Pi pin mapping to LCD2004 pin.  read/write digital pin 6
	LCD_D7 : int
		R.Pi pin mapping to LCD2004 pin.  read/write digital pin 7
	LCD_D7 : int
		R.Pi pin mapping to LCD2004 pin.  Turns backlight on and off.  		

	Notes
	--------
	This code is based HEAVILY on lcd2004.py code provided by sunfounder.  

	References
	----------------
	https://www.sunfounder.com/
	http://wiki.sunfounder.cc/index.php?title=LCD2004_Module#The_Experiment_for_Raspberry_Pi
	"""


	# Define some device constants
	LCD_WIDTH = 20    # Maximum characters per line
	LCD_CHR = True
	LCD_CMD = False
	 
	LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
	LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
	LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
	LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line
	 
	# Timing constants
	E_PULSE = 0.0005
	E_DELAY = 0.0005
 

	def __init__(self,	LCD_RS = 16,
					LCD_E  = 1 , 
					LCD_D4 = 7,
					LCD_D5 = 8,
					LCD_D6 = 25,
					LCD_D7 = 24,
					LCD_ON = 23): 

		# Define GPIO to LCD mapping
		self.LCD_RS = LCD_RS
		self.LCD_E  = LCD_E
		self.LCD_D4 = LCD_D4
		self.LCD_D5 = LCD_D5
		self.LCD_D6 = LCD_D6
		self.LCD_D7 = LCD_D7
		self.LCD_ON = LCD_ON

		# setup GPIO pins
		_GPIO.setmode(_GPIO.BCM)       # Use BCM GPIO numbers
		_GPIO.setup(self.LCD_E, _GPIO.OUT)  # E
		_GPIO.setup(self.LCD_RS, _GPIO.OUT) # RS
		_GPIO.setup(self.LCD_D4, _GPIO.OUT) # DB4
		_GPIO.setup(self.LCD_D5, _GPIO.OUT) # DB5
		_GPIO.setup(self.LCD_D6, _GPIO.OUT) # DB6
		_GPIO.setup(self.LCD_D7, _GPIO.OUT) # DB7
		_GPIO.setup(self.LCD_ON, _GPIO.OUT) # Backlight enable

		# Initialise display
		self._lcd_init()

		# Toggle backlight on-off-on
		self.toggle_backlight(True)
		_time.sleep(0.5)
		self.toggle_backlight(False)
		_time.sleep(0.5)
		self.toggle_backlight(True)
		
		# display ready message
		self.write_to_LCD(['%%%%%%%%%%%%%%%%%%%%','LCD Panel','ready','%%%%%%%%%%%%%%%%%%%%'])
		_time.sleep(1)
		self.write_to_LCD(['','','',''])

	def _lcd_init(self):
		# Initialise display
		self._lcd_byte(0x33,self.LCD_CMD) # 110011 Initialise
		self._lcd_byte(0x32,self.LCD_CMD) # 110010 Initialise
		self._lcd_byte(0x06,self.LCD_CMD) # 000110 Cursor move direction
		self._lcd_byte(0x0C,self.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
		self._lcd_byte(0x28,self.LCD_CMD) # 101000 Data length, number of lines, font size
		self._lcd_byte(0x01,self.LCD_CMD) # 000001 Clear display
		_time.sleep(self.E_DELAY)
 
	def _lcd_byte(self,bits, mode):
		# Send byte to data pins
		# bits = data
		# mode = True  for character
		#        False for command

		_GPIO.output(self.LCD_RS, mode) # RS

		# High bits
		_GPIO.output(self.LCD_D4, False)
		_GPIO.output(self.LCD_D5, False)
		_GPIO.output(self.LCD_D6, False)
		_GPIO.output(self.LCD_D7, False)
		if bits&0x10==0x10:
			_GPIO.output(self.LCD_D4, True)
		if bits&0x20==0x20:
			_GPIO.output(self.LCD_D5, True)
		if bits&0x40==0x40:
			_GPIO.output(self.LCD_D6, True)
		if bits&0x80==0x80:
			_GPIO.output(self.LCD_D7, True)

		# Toggle 'Enable' pin
		self._lcd_toggle_enable()

		# Low bits
		_GPIO.output(self.LCD_D4, False)
		_GPIO.output(self.LCD_D5, False)
		_GPIO.output(self.LCD_D6, False)
		_GPIO.output(self.LCD_D7, False)
		if bits&0x01==0x01:
			_GPIO.output(self.LCD_D4, True)
		if bits&0x02==0x02:
			_GPIO.output(self.LCD_D5, True)
		if bits&0x04==0x04:
			_GPIO.output(self.LCD_D6, True)
		if bits&0x08==0x08:
			_GPIO.output(self.LCD_D7, True)

		# Toggle 'Enable' pin
		self._lcd_toggle_enable()
 
	def _lcd_toggle_enable(self):
		# Toggle enable
		_time.sleep(self.E_DELAY)
		_GPIO.output(self.LCD_E, True)
		_time.sleep(self.E_PULSE)
		_GPIO.output(self.LCD_E, False)
		_time.sleep(self.E_DELAY)
 
	def _lcd_string(self,message,line,style):
		# Send string to display
		# style=1 Left justified
		# style=2 Centred
		# style=3 Right justified

		if style==1:
			message = message.ljust(self.LCD_WIDTH," ")
		elif style==2:
			message = message.center(self.LCD_WIDTH," ")
		elif style==3:
			message = message.rjust(self.LCD_WIDTH," ")

		self._lcd_byte(line, self.LCD_CMD)

		for i in range(self.LCD_WIDTH):
			self._lcd_byte(ord(message[i]),self.LCD_CHR)
 
	def toggle_backlight(self,flag=True):
		"""
		True = On
		False = Off
		"""
		# Toggle backlight on-off-on
		_GPIO.output(self.LCD_ON, flag)

	def write_to_LCD(self,text=["this","is","a","test"]):
		# Send some centred test
		
		self._lcd_string(text[0],self.LCD_LINE_1,1)
		self._lcd_string(text[1],self.LCD_LINE_2,1)
		self._lcd_string(text[2],self.LCD_LINE_3,1)
		self._lcd_string(text[3],self.LCD_LINE_4,1)
		_time.sleep(0.5) # 3 second delay
 
