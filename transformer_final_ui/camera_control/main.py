import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import serial.tools.list_ports
from pathlib import Path
import serial
import threading
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk

global ser
angle_num_aj=""
height_num_aj=""
seperate_num_aj=""

command =[0x00] * 8

from tkinter import messagebox
# --- functions ---
def value_auto_fill():
    global angle_num_aj , height_num_aj , seperate_num_aj
    angle_num_aj = angle_num.get()
    height_num_aj = height_num.get()
    seperate_num_aj = angle_separate.get()

    if len(angle_num_aj)==1:
        angle_num_aj = "00"+angle_num_aj
    elif len(angle_num_aj)==2:
        angle_num_aj = "0" + angle_num_aj
    elif len(angle_num_aj)==0:
        angle_num_aj = "000"


    if len(height_num_aj)==1:
        height_num_aj = "00"+height_num_aj
    elif len(height_num_aj)==2:
        height_num_aj = "0" + height_num_aj
    elif len(height_num_aj)==0:
        height_num_aj = "000"

    if len(seperate_num_aj)==1:
        seperate_num_aj = "00"+seperate_num_aj
    elif len(seperate_num_aj)==2:
        seperate_num_aj = "0" + seperate_num_aj
    elif len(seperate_num_aj)==0:
        seperate_num_aj = "000"


    print(angle_num_aj)
    print(height_num_aj)

def serial_write():
    global command ,ser
    try:
        ser.write(bytes(command))
        threading.Timer(0.3, mylog).start()
    except:
        messagebox.showinfo("錯誤", "串口連接錯誤")



def data_transmit():
    value_auto_fill()
    serial_write()


def camera_transmit():
    value_auto_fill()
    command[0]=ord("A")
    command[1] = ord(angle_num_aj[0])
    command[2] = ord(angle_num_aj[1])
    command[3] = ord(angle_num_aj[2])
    command[4] = ord("H")
    command[5] = ord(height_num_aj[0])
    command[6] = ord(height_num_aj[1])
    command[7] = ord(height_num_aj[2])
    print(command)
    serial_write()
    angle_num.config(state=DISABLED)



def serial_ports():
    return serial.tools.list_ports.comports()

def on_select(event=None):

    # get selection from event
    global ser
    print("event.widget:", box.get())
    COMPORT = box.get().split(" ")[0]
    #print (COMPORT.split(" ")[0])
    print(COMPORT)
    ser = serial.Serial(COMPORT, 19200, timeout=0.2)


#def capture_video():
#    ret, frame = cap.read()
#    if ret:
#        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
#        img = Image.fromarray(cv2image)
#        imgtk = ImageTk.PhotoImage(image=img)
#        camlabel.imgtk = imgtk
#        camlabel.configure(image=imgtk)
#        camlabel.after(10, capture_video)


def load_excel_file():
    global workbook
    filepath = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    print(filepath)
    path=Path(filepath)
    canvas2.create_text(60, 85, text="檔案名稱 :", fill="white", font=('Helvetica 15 bold'))
    canvas2.create_text(120, 85, text=path.name, fill="white",anchor="w", font=('Helvetica 12 bold'))


def callback(input):

    if input.isdigit() and int(input)<=180 or input =="":
        return True
    else:
        return False

def height_callback(input):

    if input.isdigit() and int(input)<=400 or input =="":
        return True
    else:
        return False




def mylog():
    global ser
    print("reading")
    canvas1.itemconfig(status_label,text="進行中",fill="red")
    while ser.in_waiting:  # Or: while ser.inWaiting():
        print(ser.readline())
    threading.Timer(0.3, mylog).start()


# --- main ---

# Create object
root = Tk()



# Adjust size
root.geometry("800x480")
root.configure(bg='dimgray')
bg = PhotoImage(file="Bg.png")

style = ttk.Style(root)
style.theme_use('classic')
style.configure('Test.TLabel', background= 'dimgray')


canvas1 = Canvas(root, width=400,
                 height=480,bd=0, highlightthickness=0 , bg="#2B2E35")
canvas2 = Canvas(root, width=400,
                 height=480,bd=0, highlightthickness=0 , bg="#2B2E35")





comlable = ttk.Label(root, text="COM", style="Test.TLabel")
comlable.place(x=275,y=1)

camlabel = ttk.Label(root,)
camlabel.place(x=400,y=20)

box = ttk.Combobox(root, values=serial.tools.list_ports.comports())

box.pack()

box.bind('<<ComboboxSelected>>', on_select)

canvas1.pack(side="left")

canvas2.pack(side="right")


reg = root.register(callback)
height_reg = root.register(height_callback)

angle_num = Entry(canvas1, fg="black", bd=5,justify='center')
height_num = Entry(canvas1, fg="black", bd=5,justify='center')
angle_separate = Entry(canvas1,fg="black",bd=5,justify='center')

angle_num.config(validate ="key",
         validatecommand =(reg, '%P'))
height_num.config(validate ="key",
         validatecommand =(height_reg, '%P'))
angle_separate.config(validate ="key",
         validatecommand =(reg, '%P'))

bg_img_all = canvas1.create_image(400,240,image=bg)



transmit_btn = Button(root, width=10, height=1, bg='gray',fg='white', text='發送', command=data_transmit)
camera_btn = Button(root, width=10, height=2, bg='gray',fg='white', text='相機角度發送', command=camera_transmit)
zero_btn = Button(root, width=10, height=2, bg='gray',fg='white', text='轉盤零位重置', command=data_transmit)
camera_zero_btn = Button(root, width=10, height=2, bg='gray',fg='white', text='相機零位重置', command=data_transmit)
excel_btn = Button(root, width=10, height=2, bg='gray',fg='white', text='LOAD', command=load_excel_file)




canvas1.create_window(25,320, anchor='nw', window=transmit_btn)
canvas1.create_window(220,70, anchor='nw', window=camera_btn)
canvas1.create_window(180,150, anchor='nw', window=zero_btn)
canvas1.create_window(280,150, anchor='nw', window=camera_zero_btn)
canvas2.create_window(120,20, anchor='nw', window=excel_btn)


canvas1.create_text(50,50,text="角度 :",fill="white" ,font=('Helvetica 15 bold'))
canvas1.create_text(88,90,text="度",fill="white" ,font=('Helvetica 15 bold'))
canvas1.create_text(120,50,text="高度 :",fill="white" ,font=('Helvetica 15 bold'))
canvas1.create_text(180,90,text="厘米",fill="white" ,font=('Helvetica 15 bold'))

canvas1.create_text(80,170,text="轉盤零位校正:",fill="white" ,font=('Helvetica 12 bold'))
canvas1.create_text(80,240,text="一圈攝影次數:",fill="white" ,font=('Helvetica 12 bold'))

canvas1.create_text(50,390,text="狀態:",fill="white" ,font=('Helvetica 12 bold'))
status_label = canvas1.create_text(100,390,text="完成",fill="green" ,font=('Helvetica 12 bold'))


canvas2.create_text(60,40,text="檔案 :",fill="white" ,font=('Helvetica 15 bold'))

angle_value = canvas1.create_window((50, 90), window=angle_num,height=30, width=50)
height_value= canvas1.create_window((130, 90), window=height_num,height=30, width=50)
seperate_value= canvas1.create_window((170, 240), window=angle_separate,height=30, width=50)



#cap = cv2.VideoCapture(0)
#capture_video()
#root.overrideredirect(True)

root.mainloop()