# import libraries
import RPi.GPIO as GPIO

class button:
    """
    GPIO pulldown, input button class. 

    Parameter
    ---------------
    buttonPin : int
        default = 5.  pin number of button on RPi using BCM format.  The other pin setup is pin 6. 
    """

    def __init__(self,buttonPin=5):
        """ Initializes pulldown, input button. """
        self.buttonPin=buttonPin

        # setup GPIO pins
        GPIO.setmode(GPIO.BCM)

        # set buttons as input and with a pulldown resistor
        GPIO.setup([buttonPin], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def buttonStatus(self):
        """ Returns button status.   0 if the button is not pressed.  1 if the button is pressed"""
        return GPIO.input(self.buttonPin)
