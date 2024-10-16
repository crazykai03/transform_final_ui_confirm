# Import module
from tkinter import *
from PIL import ImageTk , Image
import threading
import time
lock_press_time =0
lock_hold= False
hold_time =0
hold_status= False
held_status = False
lock_state = True
pre_function_time =0
rf_tran_data = ""
command =[ord("B"),ord("E"),ord("3"),ord("1"),0]

os.system('sudo chmod 777 /dev/ttyS0')

def uppress(event):
    global pre_function_time
    pre_function_time = time.time()
    canvas1.itemconfig(up_btn, image = up_tap)



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
    canvas1.itemconfig(stop_btn, image = stop_tap)
    command[4] = 0x07

def stoprelease(event):
    global pre_function_time
    pre_function_time = time.time()
    canvas1.itemconfig(stop_btn, image=stop)



def lockpress(event):
    global  button1 ,lock_press_time , lock_hold , lock_state
    lock_hold = True
    canvas1.itemconfig(lock_btn, image = lock_tap)
    lock_state = True
    lock_press_time= time.time()
def lockrelease(event):
    global btn1 , lock_press_time , lock_hold ,lock_state
    lock_hold = False
    print(time.time()-lock_press_time)
    if (lock_state==True):
        canvas1.itemconfig(lock_btn, image=lock)
        setting_pop_up_release()
        unbind_btn()


def light1press(event):
    global pre_function_time,hold_status,hold_time
    pre_function_time = time.time()
    canvas1.itemconfig(light1_btn, image = light1_tap)
    hold_status = True
    command[4] = 0x80
    hold_time = time.time()


def light1release(event):
    global pre_function_time,hold_status,held_status
    pre_function_time = time.time()
    canvas1.itemconfig(light1_btn, image=light1)
    if held_status!=True:
        command[4] = 0xA8
    else:
        command[4] = 0x8A
    hold_status = False
    held_status = False


def light2press(event):
    global pre_function_time,hold_status,hold_time
    pre_function_time = time.time()
    canvas1.itemconfig(light2_btn, image = light2_tap)
    hold_status = True
    command[4] = 0x81
    hold_time = time.time()


def light2release(event):
    global pre_function_time,hold_status,held_status

    pre_function_time = time.time()
    canvas1.itemconfig(light2_btn, image=light2)
    if held_status != True:
        command[4] = 0xA9
    else:
        command[4] = 0x8B
    hold_status = False
    held_status = False

def light3press(event):
    global pre_function_time,hold_status,hold_time
    pre_function_time = time.time()
    canvas1.itemconfig(light3_btn, image = sofa_tap)




def light3release(event):
    global pre_function_time,hold_status,held_status

    pre_function_time = time.time()
    command[4] = 0x03

def alllightpress(event):
    global pre_function_time
    pre_function_time = time.time()
    canvas1.itemconfig(all_light_btn, image = all_light_tap)


def alllightrelease(event):
    global pre_function_time
    pre_function_time = time.time()
    canvas1.itemconfig(all_light_btn, image=all_light)
    command[4] = 0xD7



def settingpress(event):
    global pre_function_time
    pre_function_time = time.time()
    canvas1.itemconfig(setting_btn, image = setting_tap)
    setting_pop_up()






#---------canvas 2

def settingbackpress(event):
    global pre_function_time
    pre_function_time = time.time()
    canvas2.itemconfig(settingback_btn, image = settingback_tap)


def settingbackrelease(event):
    global pre_function_time
    pre_function_time = time.time()
    canvas2.itemconfig(settingback_btn, image = settingback)
    setting_pop_up_release()

def pairpress(event):
    global pre_function_time
    pre_function_time = time.time()
    canvas2.itemconfig(pair_btn, image=pair_tap)

def pairrelease(event):
    global pre_function_time
    pre_function_time = time.time()
    canvas2.itemconfig(pair_btn, image = pair)
    command[4] = 0x70


def resetpress(event):
    global pre_function_time
    pre_function_time = time.time()
    canvas2.itemconfig(reset_btn, image=reset_tap)


def resetrelease(event):
    global pre_function_time
    pre_function_time = time.time()
    canvas2.itemconfig(reset_btn, image = reset)
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
    global  command
    ser.write(bytes(command))











def mylog():
    global  lock_press_time , lock_state , pre_function_time,held_status

    if (time.time() - lock_press_time >=2 and lock_hold==True):
        canvas1.itemconfig(lock_btn, image=unlock)
        bind_btn()
        lock_state = False
        pre_function_time = time.time()
    elif (time.time() - pre_function_time >=30  and lock_state == False ):
        canvas1.itemconfig(lock_btn, image=lock)
        lock_state = True
        setting_pop_up_release()
        unbind_btn()

    if hold_status==True and time.time() - hold_time >=0.5 :
        held_status = True
        serial_write()
    elif  command[4] !=0x00 and hold_status==False:
        serial_write()
        command[4]=0x00




    threading.Timer(0.3, mylog).start()

def unbind_btn():
    canvas1.tag_unbind(up_btn, '<Button-1>' )
    canvas1.tag_unbind(up_btn, '<ButtonRelease-1>' )

    canvas1.tag_unbind(down_btn, '<Button-1>', )
    canvas1.tag_unbind(down_btn, '<ButtonRelease-1>' )




    canvas1.tag_unbind(light1_btn, '<Button-1>' )
    canvas1.tag_unbind(light1_btn, '<ButtonRelease-1>' )

    canvas1.tag_unbind(light2_btn, '<Button-1>' )
    canvas1.tag_unbind(light2_btn, '<ButtonRelease-1>' )

    canvas1.tag_unbind(light3_btn, '<Button-1>' )
    canvas1.tag_unbind(light3_btn, '<ButtonRelease-1>')

    canvas1.tag_unbind(all_light_btn, '<Button-1>' )
    canvas1.tag_unbind(all_light_btn, '<ButtonRelease-1>' )






def bind_btn():
    canvas1.tag_bind(up_btn, '<Button-1>', uppress)
    canvas1.tag_bind(up_btn, '<ButtonRelease-1>', uprelease)

    canvas1.tag_bind(down_btn, '<Button-1>', downpress)
    canvas1.tag_bind(down_btn, '<ButtonRelease-1>', downrelease)

    canvas1.tag_bind(stop_btn, '<Button-1>', stoppress)
    canvas1.tag_bind(stop_btn, '<ButtonRelease-1>', stoprelease)

    canvas1.tag_bind(lock_btn, '<Button-1>', lockpress)
    canvas1.tag_bind(lock_btn, '<ButtonRelease-1>', lockrelease)

    canvas1.tag_bind(light1_btn, '<Button-1>', light1press)
    canvas1.tag_bind(light1_btn, '<ButtonRelease-1>', light1release)

    canvas1.tag_bind(light2_btn, '<Button-1>', light2press)
    canvas1.tag_bind(light2_btn, '<ButtonRelease-1>', light2release)

    canvas1.tag_bind(light3_btn, '<Button-1>', light3press)
    canvas1.tag_bind(light3_btn, '<ButtonRelease-1>', light3release)

    canvas1.tag_bind(all_light_btn, '<Button-1>', alllightpress)
    canvas1.tag_bind(all_light_btn, '<ButtonRelease-1>', alllightrelease)
    canvas1.tag_bind(setting_btn, '<Button-1>', settingpress)


# Create object
root = Tk()

# Adjust size
root.geometry("480x800")

# Add image file
bg = PhotoImage(file="Bg.png")
logo = PhotoImage(file="Logo.png")
up= PhotoImage(file="bed-default.png")
down= PhotoImage(file="party-default.png")
stop = PhotoImage(file="stop-default.png")
light1= PhotoImage(file="light1-default.png")
light2= PhotoImage(file="light2-default.png")
sofa= PhotoImage(file="sofa-default.png")
#dimming= PhotoImage(file="control-default.png")
all_light = PhotoImage(file="allLight-default.png")
#pop_up_bg = PhotoImage(file="Popup-Bg.png")
#change =  PhotoImage(file="change_btn.png")
#confirm =  PhotoImage(file="confirm_btn.png")
lock= PhotoImage(file="lock-default.png")
unlock = PhotoImage(file="unlock-default.png")

setting = PhotoImage(file="Setting-default.png")


settingbg = PhotoImage(file="settingbg.png")
settingback = PhotoImage(file="back-default.png")

pair = PhotoImage(file="pair-default.png")
reset =PhotoImage(file="reset-default.png")


#option = PhotoImage(file="option.png")
#------------for tap button--------------------------------

up_tap= PhotoImage(file="bed-tap.png")
down_tap= PhotoImage(file="party-tap.png")
stop_tap = PhotoImage(file="stop-tap.png")
light1_tap= PhotoImage(file="light1-tap.png")
light2_tap= PhotoImage(file="light2-tap.png")
sofa_tap= PhotoImage(file="sofa-tap.png")
#dimming_tap= PhotoImage(file="control-tap.png")
all_light_tap = PhotoImage(file="allLight-tap.png")
lock_tap= PhotoImage(file="lock-tap.png")
unlock_tap= PhotoImage(file = "unlock-default.png")
#change_tap =  PhotoImage(file="change_tap.png")
#confirm_tap =  PhotoImage(file="confirm_tap.png")
#all_dark = PhotoImage(file = "all_dark_bg.png")

setting_tap= PhotoImage(file = "Setting-tap.png")
settingback_tap = PhotoImage(file="back-tap.png")
pair_tap = PhotoImage(file="pair-tap.png")
reset_tap = PhotoImage(file="reset-tap.png")







# Create Canvas
canvas1 = Canvas(root, width=480,
                 height=800,bd=0, highlightthickness=0 , bg="#2B2E35")
canvas2 = Canvas(root, width=480,
                 height=800,bd=0, highlightthickness=0 , bg="#2B2E35")
canvas1.pack(fill="both", expand=True)


# Display image
#canvas1.create_image(0, 0, image=bg,anchor="nw")






offset_x = 106
offset_y = 83



# Display Buttons
bg_img_all = canvas1.create_image(240,400,image=bg)
logo_btn = canvas1.create_image(24+186,24+28,image=logo)
up_btn = canvas1.create_image(24+offset_x,100+offset_y,image=up)
down_btn = canvas1.create_image(244+offset_x,100+offset_y,image=down)
stop_btn =  canvas1.create_image(24+offset_x,613+offset_y,image=stop)
lock_btn =  canvas1.create_image(244+offset_x,613+offset_y,image=lock)

light1_btn =  canvas1.create_image(24+offset_x,442+offset_y,image=light1)
light2_btn =  canvas1.create_image(244+offset_x,442+offset_y,image=light2)
light3_btn =  canvas1.create_image(24+offset_x,272+offset_y,image=sofa)
#rgb1_btn =  canvas1.create_image(616+offset_y,100+offset_y,image=dimming)
all_light_btn =  canvas1.create_image(244+offset_x,271+offset_y,image=all_light)
setting_btn =  canvas1.create_image(14+428,14+52,image=setting)
#option_btn =  canvas1.create_image(480+offset_y,185+offset_y,image=option)




#------canvas 2 -----------------
#bg_img_dark = canvas2.create_image(400,240,image=all_dark)
#pop_up_background =  canvas2.create_image(176+224,16+224,image=pop_up_bg)
#change_btn =  canvas2.create_image(400,220,image=change)
#confirm_btn =  canvas2.create_image(400,220+170,image=confirm)

settingbg_pop = canvas2.create_image(240,400,image=settingbg)
settingback_btn = canvas2.create_image(240,513,image=settingback)
pair_btn = canvas2.create_image(143,384,image=pair)
reset_btn = canvas2.create_image(338,384,image=reset)




bind_btn()
unbind_btn()










#canvas1.itemconfig(lock,state='hidden')






mylog()


# Execute tkinter

root.overrideredirect(True)

root.mainloop()