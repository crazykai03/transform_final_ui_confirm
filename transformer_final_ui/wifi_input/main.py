from tkinter import *
from PIL import ImageTk , Image
import threading
import time
from tkinter import ttk
from tkinter.messagebox import askokcancel,showinfo,WARNING
import tkinter.font as font
import os

reboot_cmd = 'sudo reboot now'


focus_index = 0
button_list_index =0







root = Tk()

# Adjust size
root.geometry("800x480")

# Add image file
path = "/home/pi/transform_final_ui_confirm/transformer_final_ui/wifi_input/"
bg = PhotoImage(file=path+"Bg.png")
logo = PhotoImage(file=path+"Logo.png")
def reboot_pi():
    os.system(reboot_cmd)
def write_command():
    f=open('/home/pi/transform_final_ui_confirm/transformer_final_ui/wifi_input/wpa_supplicat.conf','w')
    f.write("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n")
    f.write("network={\n")
    f.write("	ssid=\""+ssid_text.get('1.0','end').strip()+"\""+"\n")
    f.write("	psk=\""+password_text.get('1.0','end').strip()+"\""+"\n")
    f.write("}")
    f.close()
    password_text.delete(1.0, END)
    ssid_text.delete(1.0, END)

    #os.system(reboot_cmd)

def create_current_button(display_index):
    x_position_index = 1
    y_position_index = 0
    for button in buttonlist[display_index]:
        command = lambda x=button: select(x)
        if button == 'Space':
            button = Button(root, text=button,font=("Helvetica", 8),bg='black',fg='white', height=2, width=85, command=command)
            x_position_index = 8
        elif button == 'Enter':
            button = Button(root, text=button, font=("Helvetica", 8), bg='red', fg='white', height=2, width=3,
                            command=command)
        else:
            button = Button(root, text=button,font=("Helvetica", 8), bg='black',fg='white',height=2, width=3, command=command)

        canvas_widget = canvas1.create_window(45 * x_position_index, 270 + y_position_index, window=button)
        x_position_index = x_position_index + 1
        if x_position_index > 15:
            y_position_index = y_position_index + 45
            x_position_index = 1





def ssid_focus_in(event):
    global focus_index
    focus_index=1
    ssid_text.focus_set()
    ssid_text.configure(bg='yellow')
    password_text.configure(bg='white')
def pass_focus_in(event):
    global focus_index
    focus_index=2
    password_text.focus_set()
    password_text.configure(bg='yellow')
    ssid_text.configure(bg='white')

def select(value):
    global button_list_index
    print(value)
    value_operate = value
    if value == 'Space':
        value_operate=" "

    elif value == 'Enter':
        write_command()
        return

    elif value == 'Tab':
        value_operate='\t'
    elif value == 'Caps':
        button_list_index=1
        create_current_button(button_list_index)
        return
    elif value == 'CAPS':
        button_list_index=0
        create_current_button(button_list_index)
        return
    elif value == 'ShiftL':
        button_list_index=2
        create_current_button(button_list_index)
        return
    elif value == 'ShiftR':
        button_list_index=0
        create_current_button(button_list_index)
        return










    if focus_index==1:
        if(value_operate=='Del'):
            ssid_text.delete(1.0, END)
        elif value_operate == 'Backs':
            i = ssid_text.get(1.0, END)
            newtext = i[:-2]
            ssid_text.delete(1.0, END)
            ssid_text.insert(INSERT, newtext)
        else:
            ssid_text.insert(INSERT,value_operate)
    if focus_index == 2:
        if (value_operate == 'Del'):
            password_text.delete(1.0, END)
        elif value_operate == 'Backs':
            i = password_text.get(1.0, END)
            newtext = i[:-2]
            password_text.delete(1.0, END)
            password_text.insert(INSERT, newtext)
        else:
            password_text.insert(INSERT, value_operate)






canvas1 = Canvas(root, width=800,
                 height=480,bd=0, highlightthickness=0 , bg="#2B2E35")


canvas1.pack(fill="both", expand=True)


#bg_img_all = canvas1.create_image(400,240,)
logo_btn = canvas1.create_image(24+186,24+28,image=logo)

ssid_text = Text(canvas1,width = 15, height=1, font=("Helvetica", 20))
ssid_text.place(x=200,y=120)
password_text = Text(canvas1,width = 15, height=1, font=("Helvetica", 20))
password_text.place(x=200,y=180)
canvas1.create_text((120, 140), text="SSID        :", font=("Helvetica", 20),fill='white')
canvas1.create_text((100, 200), text="PASSWORD :", font=("Helvetica", 20),fill='white')




ssid_text.bind("<Button-1>", ssid_focus_in)
password_text.bind("<Button-1>", pass_focus_in)





buttons = ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backs', 'Del',
           'Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', '7', '8', '9',
           'Caps', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', 'Enter', '4', '5', '6',
           'ShiftL', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'ShiftR', '1', '2', '3',
           'Space']


capsButtons = ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backs', 'Del',
               'Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', '7', '8', '9',
               'CAPS', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', 'Enter', '4', '5', '6',
               'ShiftL', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'ShiftR', '1', '2', '3',
               'Space']

leftShiftButtons = ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', 'Backs', 'Del',
                    'Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', ']', '7', '8', '9',
                    'Caps', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ':', 'Enter', '4', '5', '6',
                    'ShiftL', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '<', '>', '?', 'ShiftR', '1', '2', '3',
                    'Space'

                    ]

buttonlist = [buttons,capsButtons,leftShiftButtons]

create_current_button(button_list_index)




boot_button = Button(root, text="REBOOT",font=("Helvetica", 8), bg='black',fg='white',height=3, width=5, command=reboot_pi)
canvas1.create_window(700, 30, window=boot_button)


root.overrideredirect(True)

root.mainloop()
