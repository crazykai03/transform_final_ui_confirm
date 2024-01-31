# Import module
from tkinter import *
from PIL import ImageTk, Image
import threading
import time

import os
import serial

lock_press_time = 0
lock_hold = False
hold_time = 0
hold_status = False
held_status = False
lock_state = True
pre_function_time = 0
rf_tran_data = ""
command = [ord("B"), ord("E"), ord("7"), ord("1"), 0]

os.system('sudo chmod 777 /dev/ttyS0')

ser = serial.Serial("/dev/ttyS0", 19200, timeout=0.2)


def uppress(event):
    global pre_function_time
    pre_function_time = time.time()
    canvas1.itemconfig(up_btn, image=up_tap)


def uprelease(event):
    global pre_function_time
    pre_function_time = time.time()
    canvas1.itemconfig(up_btn, image=up)
    command[4] = 0x01


def downpress(event):
    global pre_function_time
    pre_function_time = time.time()
    canvas1.itemconfig(down_btn, image=down_tap)


def downrelease(event):
    global pre_function_time
    pre_function_time = time.time()
    canvas1.itemconfig(down_btn, image=down)
    command[4] = 0x02


def stoppress(event):
    global pre_function_time
    pre_function_time = time.time()
    canvas1.itemconfig(stop_btn, image=stop_tap)
    command[4] = 0x03


def stoprelease(event):
    global pre_function_time
    pre_function_time = time.time()
    canvas1.itemconfig(stop_btn, image=stop)


def lockpress(event):
    global button1, lock_press_time, lock_hold, lock_state
    lock_hold = True
    canvas1.itemconfig(lock_btn, image=lock_tap)
    lock_state = True
    lock_press_time = time.time()


def lockrelease(event):
    global btn1, lock_press_time, lock_hold, lock_state
    lock_hold = False
    print(time.time() - lock_press_time)
    if (lock_state == True):
        canvas1.itemconfig(lock_btn, image=lock)
        setting_pop_up_release()
        unbind_btn()







def rgbpress(event):
    global pre_function_time, hold_status, hold_time
    pre_function_time = time.time()
    canvas1.itemconfig(rgb1_btn, image=rgb1_tap)
    hold_status = True
    command[4] = 0xCB
    hold_time = time.time()


def rgbrelease(event):
    global pre_function_time, hold_status, held_status

    pre_function_time = time.time()
    canvas1.itemconfig(rgb1_btn, image=rgb1)
    if held_status != True:
        command[4] = 0xC6
    else:
        command[4] = 0xD0
    hold_status = False
    held_status = False


def dimmingpress(event):
    global pre_function_time, hold_status, hold_time
    pre_function_time = time.time()
    canvas1.itemconfig(control_btn, image=dimming_tap)


def dimmingrelease(event):
    global pre_function_time, hold_status, held_status

    pre_function_time = time.time()
    canvas1.itemconfig(control_btn, image=dimming)
    command[4] = 0xB7


def settingpress(event):
    global pre_function_time
    pre_function_time = time.time()
    canvas1.itemconfig(setting_btn, image=setting_tap)
    setting_pop_up()


# ---------canvas 2
def settingbackpress(event):
    global pre_function_time
    pre_function_time = time.time()
    canvas2.itemconfig(settingback_btn, image=settingback_tap)


def settingbackrelease(event):
    global pre_function_time
    pre_function_time = time.time()
    canvas2.itemconfig(settingback_btn, image=settingback)
    setting_pop_up_release()


def pairpress(event):
    global pre_function_time
    pre_function_time = time.time()
    canvas2.itemconfig(pair_btn, image=pair_tap)


def pairrelease(event):
    global pre_function_time
    pre_function_time = time.time()
    canvas2.itemconfig(pair_btn, image=pair)
    command[4] = 0x70


def resetpress(event):
    global pre_function_time
    pre_function_time = time.time()
    canvas2.itemconfig(reset_btn, image=reset_tap)


def resetrelease(event):
    global pre_function_time
    pre_function_time = time.time()
    canvas2.itemconfig(reset_btn, image=reset)
    command[4] = 0x71


def setting_pop_up():
    canvas1.pack_forget()
    canvas2.pack()
    canvas2.tag_bind(settingback_btn, '<Button-1>', settingbackpress)
    canvas2.tag_bind(settingback_btn, '<ButtonRelease-1>', settingbackrelease)
    canvas2.tag_bind(pair_btn, '<Button-1>', pairpress)
    canvas2.tag_bind(pair_btn, '<ButtonRelease-1>', pairrelease)
    canvas2.tag_bind(reset_btn, '<Button-1>', resetpress)
    canvas2.tag_bind(reset_btn, '<ButtonRelease-1>', resetrelease)


def setting_pop_up_release():
    canvas2.pack_forget()
    canvas1.pack()
    canvas2.tag_unbind(settingback_btn, '<Button-1>')
    canvas2.tag_unbind(settingback_btn, '<ButtonRelease-1>')
    canvas2.tag_unbind(pair_btn, '<Button-1>')
    canvas2.tag_unbind(reset_btn, '<Button-1>')
    canvas2.tag_unbind(pair_btn, '<ButtonRelease-1>')
    canvas2.tag_unbind(reset_btn, '<ButtonRelease-1>')


def serial_write():
    global command
    # print(command)
    #print(bytes(command))
    ser.write(bytes(command))


def mylog():
    global lock_press_time, lock_state, pre_function_time, held_status

    if (time.time() - lock_press_time >= 2 and lock_hold == True):
        canvas1.itemconfig(lock_btn, image=unlock)
        bind_btn()
        lock_state = False
        pre_function_time = time.time()
    elif (time.time() - pre_function_time >= 30 and lock_state == False):
        canvas1.itemconfig(lock_btn, image=lock)
        lock_state = True
        setting_pop_up_release()
        unbind_btn()

    if hold_status == True and time.time() - hold_time >= 0.5:
        held_status = True
        serial_write()
    elif command[4] != 0x00 and hold_status == False:
        serial_write()
        command[4] = 0x00

    threading.Timer(0.3, mylog).start()


def unbind_btn():
    canvas1.tag_unbind(up_btn, '<Button-1>')
    canvas1.tag_unbind(up_btn, '<ButtonRelease-1>')

    canvas1.tag_unbind(down_btn, '<Button-1>', )
    canvas1.tag_unbind(down_btn, '<ButtonRelease-1>')



    canvas1.tag_unbind(rgb1_btn, '<Button-1>')
    canvas1.tag_unbind(rgb1_btn, '<ButtonRelease-1>')

    canvas1.tag_unbind(control_btn, '<Button-1>')
    canvas1.tag_unbind(control_btn, '<ButtonRelease-1>')


def bind_btn():
    canvas1.tag_bind(up_btn, '<Button-1>', uppress)
    canvas1.tag_bind(up_btn, '<ButtonRelease-1>', uprelease)

    canvas1.tag_bind(down_btn, '<Button-1>', downpress)
    canvas1.tag_bind(down_btn, '<ButtonRelease-1>', downrelease)

    canvas1.tag_bind(stop_btn, '<Button-1>', stoppress)
    canvas1.tag_bind(stop_btn, '<ButtonRelease-1>', stoprelease)

    canvas1.tag_bind(lock_btn, '<Button-1>', lockpress)
    canvas1.tag_bind(lock_btn, '<ButtonRelease-1>', lockrelease)





    canvas1.tag_bind(rgb1_btn, '<Button-1>', rgbpress)
    canvas1.tag_bind(rgb1_btn, '<ButtonRelease-1>', rgbrelease)

    canvas1.tag_bind(control_btn, '<Button-1>', dimmingpress)
    canvas1.tag_bind(control_btn, '<ButtonRelease-1>', dimmingrelease)

    canvas1.tag_bind(setting_btn, '<Button-1>', settingpress)


# ------canvas 2 -----------------


# Create object
root = Tk()
pwd_path = "/home/pi/transform_final_ui_confirm/transformer_final_ui/VR/"

# Adjust size
root.geometry("800x480")

# Add image file
bg = PhotoImage(file=pwd_path + "Bg.png")
logo = PhotoImage(file=pwd_path + "Logo.png")
up = PhotoImage(file=pwd_path + "up-default.png")
down = PhotoImage(file=pwd_path + "down-default.png")
stop = PhotoImage(file=pwd_path + "stop-default.png")


rgb1 = PhotoImage(file=pwd_path + "light-default.png")


dimming = PhotoImage(file=pwd_path + "control-default.png")

lock = PhotoImage(file=pwd_path + "lock-default.png")
unlock = PhotoImage(file=pwd_path + "unlock-default.png")
setting = PhotoImage(file=pwd_path + "Setting-default.png")

settingbg = PhotoImage(file=pwd_path + "settingbg.png")
settingback = PhotoImage(file=pwd_path + "back-default.png")

pair = PhotoImage(file=pwd_path + "pair-default.png")
reset = PhotoImage(file=pwd_path + "reset-default.png")

# pop_up_bg = PhotoImage(file="Popup-Bg.png")
# change =  PhotoImage(file="change_btn.png")
# confirm =  PhotoImage(file="confirm_btn.png")

# option = PhotoImage(file="option.png")
# ------------for tap button--------------------------------

up_tap = PhotoImage(file=pwd_path + "up-tap.png")
down_tap = PhotoImage(file=pwd_path + "down-tap.png")

stop_tap = PhotoImage(file=pwd_path + "stop-tap.png")

rgb1_tap = PhotoImage(file=pwd_path + "light-tap.png")

dimming_tap = PhotoImage(file=pwd_path + "control-tap.png")


lock_tap = PhotoImage(file=pwd_path + "lock-tap.png")
unlock_tap = PhotoImage(file=pwd_path + "unlock-tap.png")

setting_tap = PhotoImage(file=pwd_path + "Setting-tap.png")
settingback_tap = PhotoImage(file=pwd_path + "back-tap.png")
pair_tap = PhotoImage(file=pwd_path + "pair-tap.png")
reset_tap = PhotoImage(file=pwd_path + "reset-tap.png")

# change_tap =  PhotoImage(file="change_tap.png")
# confirm_tap =  PhotoImage(file="confirm_tap.png")
# all_dark = PhotoImage(file = "all_dark_bg.png")


# Create Canvas
canvas1 = Canvas(root, width=800,
                 height=480, bd=0, highlightthickness=0, bg="#2B2E35")
canvas2 = Canvas(root, width=800,
                 height=480, bd=0, highlightthickness=0, bg="#2B2E35")
canvas1.pack(fill="both", expand=True)

# Display image
# canvas1.create_image(0, 0, image=bg,anchor="nw")


offset_x = 72
offset_y = 87

# Display Buttons
bg_img_all = canvas1.create_image(400, 240, image=bg)
logo_btn = canvas1.create_image(24 + 186, 24 + 28, image=logo)


up_btn = canvas1.create_image(328 + 72, 100 + 87, image=up)
down_btn = canvas1.create_image(328 + 72, 282 + 87, image=down)

stop_btn = canvas1.create_image(480 + 148, 282 + 87, image=stop)
lock_btn = canvas1.create_image(480 + 148, 100 + 87, image=lock)

rgb1_btn = canvas1.create_image(24 + 148, 100 + 87, image=rgb1)
control_btn = canvas1.create_image(24 + 148, 282 + 87, image=dimming)


setting_btn = canvas1.create_image(14 + 748, 14 + 52, image=setting)
# option_btn =  canvas1.create_image(480+offset_y,185+offset_y,image=option)


# ------canvas 2 -----------------
settingbg_pop = canvas2.create_image(324 + 76, 170 + 70, image=settingbg)
settingback_btn = canvas2.create_image(324 + 76, 290 + 70, image=settingback)
pair_btn = canvas2.create_image(172 + 76, 154 + 70, image=pair)
reset_btn = canvas2.create_image(476 + 76, 154 + 70, image=reset)
# pop_up_background =  canvas2.create_image(176+224,16+224,image=pop_up_bg)
# change_btn =  canvas2.create_image(400,220,image=change)
# confirm_btn =  canvas2.create_image(400,220+170,image=confirm)


bind_btn()
unbind_btn()

# canvas1.itemconfig(lock,state='hidden')


mylog()

# Execute tkinter

root.overrideredirect(True)

root.mainloop()
