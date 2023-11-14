import os
import RPi.GPIO as GPIO
import time

killpython_cmd = 'killall python3'
ui_1_cmd =''
ui_2_cmd = ''
ui_3_cmd = ''


ui_index = '0'




f = open("store.txt", "a")
f.write(ui_index)
f.close()

f = open("store.txt", "r")

def button_handler(pin):
    print("button is clicked")

if __name__ == '__main__':
    button_pin = 18

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(button_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    # events can be GPIO.RISING, GPIO.FALLING, or GPIO.BOTH
    GPIO.add_event_detect(button_pin, GPIO.RISING,
                          callback=button_handler,
                          bouncetime=300)

   