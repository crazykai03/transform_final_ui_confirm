import os
import RPi.GPIO as GPIO
import time

killpython_cmd = 'pkill -9 -f main.py'
ui_cmd =['python3 /home/pi/transform_final_ui_confirm/transformer_final_ui/lift_kitchen/main.py', 'python3 /home/pi/transform_final_ui_confirm/transformer_final_ui/lift_sofa/main.py','python3 /home/pi/transform_final_ui_confirm/transformer_final_ui/scissor/main.py','python3 /home/pi/transform_final_ui_confirm/transformer_final_ui/wifi_input/main.py']



ui_index = 0








def button_handler(pin):
    global ui_index
    ui_index=ui_index+1
    if ui_index >3:
        ui_index=0
    f = open("/home/pi/transform_final_ui_confirm/transformer_final_ui/switchui/store.txt", "w")
    f.write(str(ui_index))
    f.close()    
    os.system(killpython_cmd)
    

def hell():
    global ui_index
    print("run cmd")
    f = open("/home/pi/transform_final_ui_confirm/transformer_final_ui/switchui/store.txt", "r")
    ui_index = int(f.read())
    f.close()
    print(ui_index)
    print(ui_cmd[ui_index]) 
    os.system(ui_cmd[ui_index])
  

button_pin = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin,GPIO.IN, pull_up_down = GPIO.PUD_UP)

    # events can be GPIO.RISING, GPIO.FALLING, or GPIO.BOTH
GPIO.add_event_detect(button_pin, GPIO.FALLING,
                              callback=button_handler,
                              bouncetime=800)

   



while True:
    print("start")
    hell()        
   
