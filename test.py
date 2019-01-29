
"""
This code is just a test of the functions of this library.  
"""

# import libraries
import LCD2004 as lcd
import button
import time
import m5e
import RPi.GPIO as GPIO

# instruct the RPi to ignore warnings
GPIO.setwarnings(False)

# initialize the LCD screen
lcd1=lcd.LCD()
lcd1.write_to_LCD(["Hello","how","are","you?"])
lcd1.toggle_backlight(False)

# initialize the buttons
b1 = button.button(5)
b2 = button.button(6)

# initialize the M5e rfid reader
reader = m5e.M5e()

# main loop
while(True):
    if b1.buttonStatus()==1:
        lcd1.write_to_LCD(["Button 1","has been","pressed",""])
        print(reader.ReadSingleTag())
    if b2.buttonStatus()==1:
        lcd1.write_to_LCD(["Button 2","has been","pressed",""])
        print(reader.ReadMultiTag())
    time.sleep(0.3)
