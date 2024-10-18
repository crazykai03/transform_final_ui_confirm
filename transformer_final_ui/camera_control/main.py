import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import serial.tools.list_ports
from pathlib import Path
import serial
import threading
from tkinter import messagebox
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk

global ser , uart_receive
import pandas as pd

angle_num_aj=""
height_num_aj=""
seperate_num_aj=""

auto_angle_num_aj=""
auto_height_num_aj=""
auto_seperate_num_aj=""

process_list=[]

circle_counter=0
total_circle=0

whole_circle_counter =0
total_whole_circle_counter=0

auto_processing=False
camera_fixed = False

command =[0x00] * 11

processingc = False
processingr=False

excel_process =False
# --- functions ---


def insert_processing_list():
    global process_list,whole_circle_counter,total_whole_circle_counter
    print(whole_circle_counter)
    auto_angle_num.delete(0,tk.END)
    auto_height_num.delete(0, tk.END)


    auto_angle_num.insert(0,process_list[whole_circle_counter][0])
    auto_height_num.delete(0, tk.END)
    auto_height_num.insert(0,process_list[whole_circle_counter][1])
    auto_angle_separate.delete(0, tk.END)

    auto_angle_separate.insert(0,process_list[whole_circle_counter][2])

    canvas2.itemconfig(remain_circle, text=str(whole_circle_counter)+"/"+str(total_whole_circle_counter), fill="white")




def value_auto_fill():
    global angle_num_aj , height_num_aj , seperate_num_aj
    angle_num_aj = angle_num.get()
    height_num_aj = height_num.get()
    if angle_separate.get()=="":
        angle_separate.insert(0,"0")
    seperate_num_aj = angle_separate.get()

    if len(angle_num_aj)==1:
        angle_num_aj = "00"+angle_num_aj
    elif len(angle_num_aj)==2:
        angle_num_aj = "0" + angle_num_aj
    elif len(angle_num_aj)==0:
        angle_num_aj = "000"


    if len(height_num_aj)==1:
        height_num_aj = "000"+height_num_aj
    elif len(height_num_aj)==2:
        height_num_aj = "00" + height_num_aj
    elif len(height_num_aj) == 3:
        height_num_aj = "0" + height_num_aj
    elif len(height_num_aj)==0:
        height_num_aj = "0000"

    if len(seperate_num_aj)==1:
        seperate_num_aj = "00"+seperate_num_aj
    elif len(seperate_num_aj)==2:
        seperate_num_aj = "0" + seperate_num_aj
    elif len(seperate_num_aj)==0:
        seperate_num_aj = "000"






def auto_processing_auto_fill():

    global auto_angle_num_aj , auto_height_num_aj , auto_seperate_num_aj,circle_counter,excel_process

    auto_angle_num_aj = auto_angle_num.get()
    auto_height_num_aj = auto_height_num.get()
    auto_seperate_num_aj = str(int(360/int(auto_angle_separate.get()))*circle_counter)


    if len(auto_angle_num_aj)==1:
        auto_angle_num_aj = "00"+auto_angle_num_aj
    elif len(auto_angle_num_aj)==2:
        auto_angle_num_aj = "0" + auto_angle_num_aj
    elif len(auto_angle_num_aj)==0:
        auto_angle_num_aj = "000"


    if len(auto_height_num_aj)==1:
        auto_height_num_aj = "000"+auto_height_num_aj
    elif len(auto_height_num_aj)==2:
        auto_height_num_aj = "00" + auto_height_num_aj
    elif len(auto_height_num_aj) == 3:
        auto_height_num_aj = "0" + auto_height_num_aj
    elif len(auto_height_num_aj)==0:
        auto_height_num_aj = "0000"

    if len(auto_seperate_num_aj)==1:
        auto_seperate_num_aj = "00"+auto_seperate_num_aj
    elif len(auto_seperate_num_aj)==2:
        auto_seperate_num_aj = "0" + auto_seperate_num_aj
    elif len(auto_seperate_num_aj)==0:
        auto_seperate_num_aj = "000"

def serial_write():
    global command ,ser , processing,auto_processing
    try:
        print(command)
        ser.write(bytes(command))
        command = [0x00] * 11
        threading.Timer(0.3, mylog).start()

    except:
        messagebox.showinfo("錯誤", "串口連接錯誤")
        auto_processing=False
        processing=False





def reset_rotate_transmit():
    global processingr
    command[0] = ord("R")
    command[1] = ord("E")
    command[2] = ord("E")
    command[3] = ord("S")
    command[4] = ord("E")
    command[5] = ord("T")
    command[6] = ord("R")
    processingr=True

    serial_write()


def reset_camera_transmit():
    global processingc
    command[0]=ord("3")
    command[1]=ord("0")
    command[1]=ord("R")
    command[2] = ord("E")
    command[3] = ord("E")
    command[4] = ord("S")
    command[5] = ord("E")
    command[6] = ord("T")
    command[7] = ord("C")
    processingc = True
    serial_write()



def start_auto_transmit():
    global auto_processing,camera_fixed,excel_process
    if excel_process==True:
        insert_processing_list()

    if auto_angle_separate.get()=="":
        messagebox.showinfo("錯誤", "數值有誤,運行取消")
        auto_processing = False
    if 360% int(auto_angle_separate.get()) != 0 :
        messagebox.showinfo("錯誤", "次數必順被整除")
        auto_processing = False
    else:

        auto_processing_auto_fill()
        command[0] = ord("3")
        command[1] = ord("0")
        command[2] = ord("A")
        command[3] = ord(auto_angle_num_aj[0])
        command[4] = ord(auto_angle_num_aj[1])
        command[5] = ord(auto_angle_num_aj[2])
        command[6] = ord("H")
        command[7] = ord(auto_height_num_aj[0])
        command[8] = ord(auto_height_num_aj[1])
        command[9] = ord(auto_height_num_aj[2])
        command[10] = ord(auto_height_num_aj[3])


        auto_processing=True
        camera_fixed=False
        print(command)
        serial_write()

def fiexed_camera_auto_transmit():
    global circle_counter,auto_processing,excel_process
    if excel_process==True:
        insert_processing_list()
    auto_processing_auto_fill()
    command[0]=ord("3")
    command[1] = ord("1")
    command[2] = ord("R")
    command[3] = ord(auto_seperate_num_aj[0])
    command[4] = ord(auto_seperate_num_aj[1])
    command[5] = ord(auto_seperate_num_aj[2])
    if auto_angle_separate.get()=="":
        messagebox.showinfo("錯誤", "數值有誤,運行取消")
        auto_processing = False
    else:
        serial_write()





def camera_transmit():
    global processingc, camera_fixed
    print("hello")
    value_auto_fill()

    command[0]=ord("3")
    command[1]=ord("0")
    command[2]=ord("A")
    command[3] = ord(angle_num_aj[0])
    command[4] = ord(angle_num_aj[1])
    command[5] = ord(angle_num_aj[2])
    command[6] = ord("H")
    command[7] = ord(height_num_aj[0])
    command[8] = ord(height_num_aj[1])
    command[9] = ord(height_num_aj[2])
    command[10] = ord(height_num_aj[3])
    print(command)
    processingc=True
    camera_fixed = False
    serial_write()

def rotate_transmit():
    global processingr, camera_fixed
    value_auto_fill()

    command[0]=ord("3")
    command[1]=ord("1")
    command[2]=ord("R")
    command[3] = ord(seperate_num_aj[0])
    command[4] = ord(seperate_num_aj[1])
    command[5] = ord(seperate_num_aj[2])


    processingr=True

    serial_write()



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
    global workbook,total_whole_circle_counter,excel_process,whole_circle_counter

    filepath = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])

    print(filepath)
    try:
        path=Path(filepath)

        df = pd.read_excel(path)
        for index, row in df.iterrows():
            process_list.append(row.to_list())
        print(process_list)
        total_whole_circle_counter = len(process_list[0])
        whole_circle_counter=0
        print(total_whole_circle_counter)
        canvas2.create_text(60, 85, text="檔案名稱 :", fill="white", font=('Helvetica 15 bold'))
        canvas2.create_text(120, 85, text=path.name, fill="white",anchor="w", font=('Helvetica 12 bold'))
        excel_process=True
    except:
        print("no")



def callback(input):

    if input.isdigit() and int(input)<=90  or input =="" :

        return True
    elif input[0]=="-":
        if len(input)==1:
            return True
        elif len(input)>1 and int(input)>=-90 :
            return True
        else:
            return False
    else:
        return False

def height_callback(input):

    if input.isdigit() and int(input)<=3000 or input =="" :
        return True
    else:
        return False


def ang_callback(input):
    if input.isdigit() and int(input) <=360 or input =="":
        return True
    else:
        return False
def disable_wdiget():
    global circle_counter
    canvas1.itemconfig(status_label, text="進行中", fill="red")
    angle_num.config(state=DISABLED)
    height_num.config(state=DISABLED)
    angle_separate.config(state=DISABLED)
    transmit_btn.config(state=DISABLED)
    camera_btn.config(state=DISABLED)
    zero_btn.config(state=DISABLED)
    camera_zero_btn.config(state=DISABLED)
    auto_start_btn.config(state=DISABLED)

    #auto_angle_num.config(state=DISABLED)
    #auto_height_num.config(state=DISABLED)
    #auto_angle_separate.config(state=DISABLED)

    if auto_processing==True:
        canvas2.itemconfig(remain_speerate_circle, text=str(circle_counter)+"/"+str(int(auto_angle_separate.get())), fill="white")
        canvas2.itemconfig(auto_status_label, text="進行中", fill="red")
def enable_wdiget():
    canvas1.itemconfig(status_label, text="完成", fill="green")
    angle_num.config(state=NORMAL)
    height_num.config(state=NORMAL)
    angle_separate.config(state=NORMAL)
    transmit_btn.config(state=NORMAL)
    camera_btn.config(state=NORMAL)
    zero_btn.config(state=NORMAL)
    camera_zero_btn.config(state=NORMAL)
    auto_start_btn.config(state=NORMAL)
    auto_angle_num.config(state=NORMAL)
    auto_height_num.config(state=NORMAL)
    auto_angle_separate.config(state=NORMAL)
    canvas2.itemconfig(remain_speerate_circle, text= "0/0" ,
                       fill="white")
    canvas2.itemconfig(auto_status_label, text="空置中", fill="green")

def mylog():
    global ser ,uart_receive , processingc,processingr ,circle_counter,camera_fixed,auto_processing,whole_circle_counter,total_whole_circle_counter,excel_process
    #print("reading")
    disable_wdiget()

    while ser.in_waiting:  # Or: while ser.inWaiting():
        uart_receive = ser.readline().decode('ascii').strip()
        #print(uart_receive)
        if uart_receive == 'c' and camera_fixed==False:
            if auto_processing==True:

                camera_fixed=True
                fiexed_camera_auto_transmit()

            elif processingc==True:
                processingc=False
                print("finish")
        if uart_receive=="r" and camera_fixed==True:
            if auto_processing==True:
                circle_counter = circle_counter + 1
                fiexed_camera_auto_transmit()

            elif processingr==True:
                processingr=False
        if auto_processing == True:
            if circle_counter >=  int(auto_angle_separate.get()):
                print("plus one")
                if excel_process == True and whole_circle_counter <total_whole_circle_counter-1:
                    circle_counter = 0
                    whole_circle_counter=whole_circle_counter+1
                    start_auto_transmit()

                else:
                    auto_processing=False
                    circle_counter=0

    if processingc == False and processingr==False and auto_processing==False:

        enable_wdiget()
    else:
        threading.Timer(0.01, mylog).start()








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
ang_reg = root.register(ang_callback)

angle_num = Entry(canvas1, fg="black", bd=5,justify='center')
height_num = Entry(canvas1, fg="black", bd=5,justify='center')
angle_separate = Entry(canvas1,fg="black",bd=5,justify='center')

auto_angle_num = Entry(canvas2, fg="black", bd=5,justify='center')
auto_height_num = Entry(canvas2, fg="black", bd=5,justify='center')
auto_angle_separate = Entry(canvas2,fg="black",bd=5,justify='center')


angle_num.config(validate ="key",
         validatecommand =(reg, '%P'))
height_num.config(validate ="key",
         validatecommand =(height_reg, '%P'))
angle_separate.config(validate ="key",
         validatecommand =(ang_reg, '%P'))


auto_angle_num.config(validate ="key",
         validatecommand =(reg, '%P'))
auto_height_num.config(validate ="key",
         validatecommand =(height_reg, '%P'))
auto_angle_separate.config(validate ="key",
         validatecommand =(ang_reg, '%P'))

bg_img_all = canvas1.create_image(400,240,image=bg)



transmit_btn = Button(root, width=10, height=1, bg='gray',fg='white', text='發送', command=rotate_transmit)
camera_btn = Button(root, width=10, height=2, bg='gray',fg='white', text='相機角度發送', command=camera_transmit)
zero_btn = Button(root, width=10, height=2, bg='gray',fg='white', text='轉盤零位重置', command=reset_rotate_transmit)
camera_zero_btn = Button(root, width=10, height=2, bg='gray',fg='white', text='相機零位重置', command=reset_camera_transmit)
excel_btn = Button(root, width=10, height=2, bg='gray',fg='white', text='加載進程', command=load_excel_file)
remove_excel_btn = Button(root, width=10, height=2, bg='gray',fg='white', text='刪除加載', command=load_excel_file)
auto_start_btn = Button(root, width=10, height=2, bg='gray',fg='white', text='啟動自動拍攝', command=start_auto_transmit)



canvas1.create_window(25,320, anchor='nw', window=transmit_btn)
canvas1.create_window(220,70, anchor='nw', window=camera_btn)
canvas1.create_window(180,150, anchor='nw', window=zero_btn)
canvas1.create_window(280,150, anchor='nw', window=camera_zero_btn)
canvas2.create_window(120,20, anchor='nw', window=excel_btn)
canvas2.create_window(210,20, anchor='nw', window=remove_excel_btn)
canvas2.create_window(120,350, anchor='nw', window=auto_start_btn)


canvas1.create_text(50,50,text="角度 :",fill="white" ,font=('Helvetica 15 bold'))
canvas1.create_text(88,90,text="度",fill="white" ,font=('Helvetica 15 bold'))
canvas1.create_text(120,50,text="高度 :",fill="white" ,font=('Helvetica 15 bold'))
canvas1.create_text(180,90,text="毫米",fill="white" ,font=('Helvetica 15 bold'))

canvas1.create_text(80,170,text="轉盤零位校正:",fill="white" ,font=('Helvetica 12 bold'))
canvas1.create_text(65,250,text="旋轉角度:",fill="white" ,font=('Helvetica 12 bold'))

canvas1.create_text(50,390,text="狀態:",fill="white" ,font=('Helvetica 12 bold'))
status_label = canvas1.create_text(100,390,text="完成",fill="green" ,font=('Helvetica 12 bold'))

canvas2.create_text(50,250,text="角度",fill="white" ,font=('Helvetica 15 bold'))
canvas2.create_text(150,250,text="高度",fill="white" ,font=('Helvetica 15 bold'))
canvas2.create_text(280,250,text="一圈攝影次數",fill="white" ,font=('Helvetica 15 bold'))


canvas2.create_text(50,410,text="自動化狀態:",fill="white" ,font=('Helvetica 12 bold'))
auto_status_label = canvas2.create_text(130,410,text="空置中",fill="green" ,font=('Helvetica 12 bold'))

canvas2.create_text(50,180,text="圈數進度:",fill="white" ,font=('Helvetica 12 bold'))
remain_circle = canvas2.create_text(140,180,text="0/0",fill="white" ,font=('Helvetica 15 bold'))

canvas2.create_text(65,210,text="當前單圈次數:",fill="white" ,font=('Helvetica 12 bold'))
remain_speerate_circle = canvas2.create_text(140,210,text="0/0",fill="white" ,font=('Helvetica 15 bold'))

auto_angle_value = canvas2.create_window((50, 300), window=auto_angle_num,height=30, width=50)
auto_height_value= canvas2.create_window((150, 300), window=auto_height_num,height=30, width=50)
auto_seperate_value= canvas2.create_window((240, 300), window=auto_angle_separate,height=30, width=50)


canvas2.create_text(60,40,text="檔案 :",fill="white" ,font=('Helvetica 15 bold'))

angle_value = canvas1.create_window((45, 90), window=angle_num,height=30, width=50)
height_value= canvas1.create_window((130, 90), window=height_num,height=30, width=50)
seperate_value= canvas1.create_window((150, 250), window=angle_separate,height=30, width=50)



#cap = cv2.VideoCapture(0)
#capture_video()
#root.overrideredirect(True)

root.mainloop()
