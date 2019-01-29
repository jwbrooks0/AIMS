import LCD2004 as lcd
import button
import time
import m5e
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

lcd1=lcd.LCD()
lcd1.write_to_LCD(["Hello","how","are","you?"])
lcd1.toggle_backlight(False)

b1 = button.button(5)
b2 = button.button(6)

reader = m5e.M5e()



while(True):
    if b1.buttonStatus()==1:
        lcd1.write_to_LCD(["Button 1","has been","pressed",""])
        print(reader.ReadSingleTag())
    if b2.buttonStatus()==1:
        lcd1.write_to_LCD(["Button 2","has been","pressed",""])
        print(reader.ReadMultiTag())
    time.sleep(0.3)
