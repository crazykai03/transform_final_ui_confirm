import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import serial.tools.list_ports
from pathlib import Path
import serial
import json
import time
import requests

import numpy as np
import shutil
from tkinter import messagebox
import math
import threading


import pandas as pd

camera_base_url="http://192.168.1.2:8080/ccapi/ver100/"

uart_receive = []
angle_num_aj=""
height_num_aj=""
seperate_num_aj=""

auto_angle_num_aj=""
auto_height_num_aj=""
auto_seperate_num_aj=""

uart_receive=""

process_list=[]

circle_counter=0
total_circle=0

whole_circle_counter =0
total_whole_circle_counter=1
path=""
camera_path=""

auto_processing=False
camera_fixed = False

command =[]

processingc = False
processingr=False

excel_process =False
# --- functions ---
AV_value = ["f3.4","f4.0","f4.5","f5.0","f5.6","f6.3","f7.1","f8.0"]
ISO_value=["auto","100","125","160","200","250","320","400","500","640","800","1000","1250","1600","2000","2500","3200"]
TV_value=["15\"","13\"","10\"","8\"","6\"","5\"","4\"","3\"2","2\"5","2\"","1\"6","1\"3","1\"","0\"8","0\"6","0\"5","0\"4","0\"3","1/4","1/5",
          "1/6","1/8","1/10","1/13","1/15","1/20","1/25","1/30","1/40","1/50","1/60","1/80","1/100","1/125","1/160","1/200","1/250","1/320"
          ,"1/400","1/500","1/640","1/800","1/1000","1/1250","1/1600","1/2000"]

global ser
def insert_processing_list():
    global process_list,whole_circle_counter,total_whole_circle_counter
    auto_angle_num.config(state=NORMAL)
    auto_height_num.config(state=NORMAL)
    auto_angle_separate.config(state=NORMAL)
    image_name.config(state=NORMAL)
    print(whole_circle_counter)
    auto_angle_num.delete(0,tk.END)
    auto_height_num.delete(0, tk.END)


    auto_angle_num.insert(0,process_list[whole_circle_counter][0])
    auto_height_num.delete(0, tk.END)
    auto_height_num.insert(0,process_list[whole_circle_counter][1])
    auto_angle_separate.delete(0, tk.END)

    auto_angle_separate.insert(0,process_list[whole_circle_counter][2])

    image_name.delete(0, tk.END)

    image_name.insert(0, process_list[whole_circle_counter][3])




    auto_angle_num.config(state=DISABLED)
    auto_height_num.config(state=DISABLED)
    auto_angle_separate.config(state=DISABLED)
    image_name.config(state=DISABLED)





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
        command.clear()
        disable_wdiget()
        #process_rundown()
        #mylog()

    except:
        messagebox.showinfo("錯誤", "串口連接錯誤")
        auto_processing=False
        processing=False





def reset_rotate_transmit():
    global processingr
    command.append(ord("2"))
    command.append(ord("B"))
    command.append(ord("I"))
    command.append(ord("R"))

    command.append(ord("\n"))
    processingr=True

    serial_write()


def reset_camera_transmit():
    global processingc

    command.append(ord("1"))
    command.append(ord("R"))
    command.append(ord("E"))
    command.append(ord("S"))
    command.append(ord("E"))
    command.append(ord("T"))
    command.append(ord("C"))
    command.append(ord("\n"))
    processingc = True
    serial_write()




def start_auto_transmit():
    global auto_processing,camera_fixed,excel_process,ser

   # if excel_process==True:
        #insert_processing_list()

    if auto_angle_separate.get()=="":
        messagebox.showinfo("錯誤", "數值有誤,運行取消")
        auto_processing = False

    else:

        auto_processing_auto_fill()

        command.append(ord("2"))
        command.append(ord("A"))
        command.append(ord(auto_angle_num_aj[0]))
        command.append(ord(auto_angle_num_aj[1]))
        command.append(ord(auto_angle_num_aj[2]))
        command.append(ord("H"))
        command.append(ord(auto_height_num_aj[0]))
        command.append(ord(auto_height_num_aj[1]))
        command.append(ord(auto_height_num_aj[2]))
        command.append(ord(auto_height_num_aj[3]))
        command.append(ord("\n"))


        auto_processing=True
        camera_fixed=False
        print(command)
        serial_write()

def fiexed_camera_auto_transmit():
    global circle_counter,auto_processing,excel_process

    #if excel_process==True:
        #insert_processing_list()
    auto_processing_auto_fill()

    command.append(ord("1"))
    command.append(ord("R"))
    command.append(ord(auto_seperate_num_aj[0]))
    command.append(ord(auto_seperate_num_aj[1]))
    command.append(ord(auto_seperate_num_aj[2]))
    command.append(ord("\n"))
    if auto_angle_separate.get()=="":
        messagebox.showinfo("錯誤", "數值有誤,運行取消")
        auto_processing = False
    else:
        serial_write()





def camera_transmit():
    global processingc, camera_fixed
    print("hello")
    value_auto_fill()


    command.append(ord("1"))
    command.append(ord("A"))
    command.append(ord(angle_num_aj[0]))
    command.append(ord(angle_num_aj[1]))
    command.append(ord(angle_num_aj[2]))
    command.append(ord("H"))
    command.append(ord(height_num_aj[0]))
    command.append(ord(height_num_aj[1]))
    command.append(ord(height_num_aj[2]))
    command.append(ord(height_num_aj[3]))
    command.append(ord("\n"))
    print(command)
    processingc=True
    camera_fixed = False
    serial_write()

def rotate_transmit():
    global processingr, camera_fixed
    value_auto_fill()


    command.append(ord("2"))
    command.append(ord("R"))
    command.append(ord(seperate_num_aj[0]))
    command.append(ord(seperate_num_aj[1]))
    command.append(ord(seperate_num_aj[2]))
    command.append(ord("\n"))

    camera_fixed=True
    processingr=True

    serial_write()

def response_OK():
    command.append(ord("1"))
    command.append(ord("O"))
    command.append(ord("K"))
    command.append(ord("\n"))
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
    try:
        ser = serial.Serial(COMPORT, 57600, timeout=0.5)
        threading.Timer(0.2, mylog).start()
    except:
        print("not allow")


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
    global workbook,total_whole_circle_counter,excel_process,whole_circle_counter,path,process_list

    filepath = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])

    print(filepath)
    remove_excel_file()
    try:
        path=Path(filepath)

        df = pd.read_excel(path)
        for index, row in df.iterrows():
            process_list.append(row.to_list())

        print(process_list)
        total_whole_circle_counter = len(process_list)
        print(total_whole_circle_counter)
        whole_circle_counter=0
        print(total_whole_circle_counter)

        canvas2.itemconfig(file_label, text=path.name, fill="white")
        excel_process=True
        insert_processing_list()

    except:
        print("no")

def reload_excel():
    global workbook,total_whole_circle_counter,excel_process,whole_circle_counter,path,process_list
    try:

        process_list=[]
        df = pd.read_excel(path)
        for index, row in df.iterrows():
            process_list.append(row.to_list())
        print(process_list)
        total_whole_circle_counter = len(process_list)
        whole_circle_counter = 0
        print(total_whole_circle_counter)
        insert_processing_list()

    except:
        print("no")

def remove_excel_file():
    global process_list,path,total_whole_circle_counter,circle_counter,total_circle,whole_circle_counter,auto_processing,processingc,processingr
    print("remove")
    path=""
    circle_counter = 0
    total_circle = 0
    whole_circle_counter = 1
    total_whole_circle_counter = 1
    process_list=[]
    auto_processing=False
    canvas2.itemconfig(file_label, text="", fill="white")
    processingc=False
    processingr=False
    enable_wdiget()



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
    auto_angle_num.config(state=DISABLED)

    height_num.config(state=DISABLED)
    auto_height_num.config(state=DISABLED)

    angle_separate.config(state=DISABLED)
    auto_angle_separate.config(state=DISABLED)

    transmit_btn.config(state=DISABLED)
    camera_btn.config(state=DISABLED)
    zero_btn.config(state=DISABLED)
    camera_zero_btn.config(state=DISABLED)
    auto_start_btn.config(state=DISABLED)

    auto_angle_num.config(state=DISABLED)
    auto_height_num.config(state=DISABLED)
    auto_angle_separate.config(state=NORMAL)
    image_name.config(state=DISABLED)

    if auto_processing==True:
        auto_angle_separate.config(state=NORMAL)
        canvas2.itemconfig(remain_speerate_circle, text=str(circle_counter)+"/"+str(int(auto_angle_separate.get())), fill="white")
        canvas2.itemconfig(auto_status_label, text="進行中", fill="red")
        canvas2.itemconfig(remain_circle, text=str(whole_circle_counter) + "/" + str(total_whole_circle_counter),
                           fill="white")
        auto_angle_separate.config(state=DISABLED)

def enable_wdiget():
    canvas1.itemconfig(status_label, text="完成", fill="green")
    angle_num.config(state=NORMAL)
    auto_angle_num.config(state=NORMAL)

    auto_height_num.config(state=NORMAL)
    height_num.config(state=NORMAL)
    auto_height_num.config(state=NORMAL)

    angle_separate.config(state=NORMAL)
    auto_angle_separate.config(state=NORMAL)
    transmit_btn.config(state=NORMAL)
    camera_btn.config(state=NORMAL)
    zero_btn.config(state=NORMAL)
    camera_zero_btn.config(state=NORMAL)
    auto_start_btn.config(state=NORMAL)
    auto_angle_num.config(state=NORMAL)
    auto_height_num.config(state=NORMAL)
    auto_angle_separate.config(state=NORMAL)
    image_name.config(state=NORMAL)

    canvas2.itemconfig(remain_speerate_circle, text= "0/0" ,
                       fill="white")
    canvas2.itemconfig(auto_status_label, text="空置中", fill="green")
    try:
        canvas2.itemconfig(remain_speerate_circle, text=str(circle_counter) + "/" + str(int(auto_angle_separate.get())),
                       fill="white")
        canvas2.itemconfig(remain_circle, text=str(whole_circle_counter) + "/" + str(total_whole_circle_counter),
                       fill="white")
    except:
        print("OK")
def camera_setting_transmit():
    print("transmit")
    tv_data = json.dumps({"value":TV_combo.get()})
    iso_data = json.dumps({"value": ISO_combo.get()})
    av_data = json.dumps({"value": AV_combo.get()})
    zoom_data = json.dumps({"value": zoom_value.get()})

    responsetv = requests.put(camera_base_url+"shooting/settings/tv",data=tv_data)
    time.sleep(0.5)
    responseav = requests.put(camera_base_url + "shooting/settings/av", data=av_data)
    time.sleep(0.5)
    responseiso = requests.put(camera_base_url + "shooting/settings/iso", data=iso_data)
    time.sleep(0.5)
    responsezoom = requests.post(camera_base_url + "shooting/control/zoom", data=zoom_data)

    initial_camera_data()


def initial_camera_data():
    battery_level_text=""
    battery_level_color="blue"
    try:
        connect_response = requests.get("http://192.168.1.2:8080/ccapi")
        if connect_response.status_code==200:

            tv_get_data = requests.get(camera_base_url + "shooting/settings/tv")
            av_get_data = requests.get(camera_base_url + "shooting/settings/av")
            iso_get_data = requests.get(camera_base_url + "shooting/settings/iso")
            zoom_get_data = requests.get(camera_base_url + "shooting/control/zoom")

            canvas3.itemconfig(tv_label, text=tv_get_data.json()['value'], fill="red")
            canvas3.itemconfig(av_label, text=av_get_data.json()['value'], fill="red")
            canvas3.itemconfig(iso_label, text=iso_get_data.json()['value'], fill="red")
            zoom_value.set(int(zoom_get_data.json()['value']))

            battery_data = requests.get(camera_base_url + "devicestatus/battery")
            if battery_data.json()['level']=="full":
                battery_level_text="滿電量"
                battery_level_color="green"
            elif battery_data.json()['level']=="high":
                battery_level_text="高電量"
                battery_level_color="green"
            elif battery_data.json()['level']=="half":
                battery_level_text="中等電量"
                battery_level_color="blue"
            elif battery_data.json()['level']=="quarter":
                battery_level_text="低電量"
                battery_level_color="red"

            canvas3.itemconfig(battery_label, text=battery_level_text, fill=battery_level_color)
            print(battery_data.json())

        else:
            messagebox.showinfo("錯誤", "相機連接失敗")

    except:
        messagebox.showinfo("錯誤", "相機連接失敗")



def take_photo():
    global camera_path,auto_seperate_num_aj,whole_circle_counter,auto_processing
    photo_response=""

    print("take")

    if auto_processing == True:
        photo_name = image_name.get()+"_"+str(angle_num.get())+"_"+str(height_num.get())+".jpg"

    else:
        photo_name=image_name.get() if image_name.get()!="" else "testing_photo"

    print(photo_name)

    try:
        if camera_path=="":
            messagebox.showinfo("錯誤", "沒有選擇相機路徑")
            auto_processing = False
        else:
            af_data= {"af":True}
            jsondata = json.dumps(af_data)
            print (camera_base_url+"shooting/control/shutterbutton")
            taking_response =requests.post(camera_base_url+"shooting/control/shutterbutton",data=jsondata)

            if(taking_response.status_code==200):

                while True:
                    photo_response=requests.get(camera_base_url+"contents/sd/100CANON")

                    time.sleep(0.5)
                    print("waiting")
                    if photo_response.status_code==200 and len(photo_response.json()['url'])!=0:
                        break



            download_photo = requests.get(photo_response.json()['url'][0], stream=True)
            if (photo_response.status_code==200):

                with open(str(camera_path)+"\\"+str(photo_name)+'.jpg','wb') as out_file:
                    shutil.copyfileobj(download_photo.raw,out_file)
                print(photo_response.json()['url'][0])
            del_response =  requests.delete(photo_response.json()['url'][0])
    except:
        messagebox.showinfo("錯誤", "相機未連接")

def check_camera_storage_empty():
    camera_file_response = requests.get(camera_base_url + "contents/sd")
    len_of_file = len(camera_file_response.json()['url'])
    for i in range (len_of_file):
        photo_response = requests.delete(camera_file_response.json['url'][i])







def load_photo_path():
    global camera_path , camera_label
    try:
        temp_camera_path = filedialog.askdirectory()

        camera_path = Path(temp_camera_path)
        print(camera_path.name)
        canvas3.itemconfig(camera_label, text=camera_path, fill="black")
    except:
        print("no")


def process_rundown():
    global ser, uart_receive, processingc, processingr, circle_counter, camera_fixed, auto_processing, whole_circle_counter, total_whole_circle_counter, excel_process
    if True:
        print("waiting")
        if uart_receive != "":
            if uart_receive == 'c' and camera_fixed==False:
                uart_receive=""
                response_OK()

                if auto_processing==True:
                    print("auto_start")
                    camera_fixed=True
                    fiexed_camera_auto_transmit()

                elif processingc==True:
                    processingc=False
                    print("finish")

            if uart_receive=="r" and camera_fixed==True:
                uart_receive = ""
                response_OK()



                if auto_processing==True :
                    print("111111111");
                    if circle_counter < int(auto_angle_separate.get()):
                        circle_counter = circle_counter + 1
                        take_photo()
                        print("take photo")
                        if circle_counter< int(auto_angle_separate.get()):
                            fiexed_camera_auto_transmit()


                        elif whole_circle_counter<total_whole_circle_counter:

                                print("whole counter = ")
                                print(whole_circle_counter)
                                circle_counter=0
                                whole_circle_counter=whole_circle_counter+1
                                if whole_circle_counter <total_whole_circle_counter:
                                    insert_processing_list()
                                    start_auto_transmit()
                                else:
                                    print("3333333");
                                    auto_processing = False
                                    whole_circle_counter = 0
                                    circle_counter = 0
                                    reload_excel()




                elif processingr==True:
                    processingr=False






    if processingc == False and processingr==False and auto_processing==False:

        enable_wdiget()
        print("enable")
    else:
        #threading.Timer(0.2, mylog).start()
        None

def mylog():
    global ser ,uart_receive , processingc,processingr ,circle_counter,camera_fixed,auto_processing,whole_circle_counter,total_whole_circle_counter,excel_process
    #print("reading")

    while ser.inWaiting():  # Or: while ser.inWaiting():

        uart_receive = ser.readline()
        uart_receive=uart_receive.decode('UTF-8').strip()
        print(uart_receive)
        if uart_receive!="":
            process_rundown()


    threading.Timer(0.2, mylog).start()













# --- main ---

# Create object
root = Tk()

button1 = PhotoImage(file = r"button1.png")

# Adjust size
root.geometry("800x680")
root.configure(bg='dimgray')
bg = PhotoImage(file="Bg.png")

style = ttk.Style(root)
style.theme_use('classic')
style.configure('Test.TLabel', background= 'dimgray')


canvas1 = Canvas(root, width=400,
                 height=480,bd=0, highlightthickness=0 , bg="#2B2E35")
canvas2 = Canvas(root, width=400,
                 height=480,bd=0, highlightthickness=0 , bg="#2B2E35")

canvas3 = Canvas(root, width=800,
                 height=200,bd=0, highlightthickness=0 , bg="#dcc6f0")



comlable = ttk.Label(root, text="COM", style="Test.TLabel")
comlable.place(x=275,y=1)



box = ttk.Combobox(root, values=serial.tools.list_ports.comports())

box.pack()

box.bind('<<ComboboxSelected>>', on_select)
canvas3.pack(fill='both',side="bottom")
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

image_name =  Entry(canvas3,fg="black",bd=5,justify='center')


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



transmit_btn = Button(root, width=10, height=2, bg='gray',fg='white', text='發送', command=rotate_transmit)
camera_btn = Button(root, width=10, height=2, bg='gray',fg='white', text='相機角度發送', command=camera_transmit)
zero_btn = Button(root, width=10, height=2, bg='red',fg='white', text='轉盤零位重置', command=reset_rotate_transmit)
camera_zero_btn = Button(root, width=10, height=2, bg='red',fg='white', text='相機零位重置', command=reset_camera_transmit)
excel_btn = Button(root, width=10, height=2, bg='gray',fg='white', text='加載進程', command=load_excel_file)
remove_excel_btn = Button(root, width=10, height=2, bg='red',fg='white', text='刪除加載/重置', command=remove_excel_file)
auto_start_btn = Button(root, width=10, height=2, bg='gray',fg='white', text='啟動自動拍攝', command=start_auto_transmit)

photo_path = Button(root, width=10, height=2, bg='gray',fg='white', text='路徑選擇', command=load_photo_path)
photo_btn = Button(root, width=10, height=2, bg='gray',fg='white', text='進行拍攝', command=take_photo)

camera_setting_btn = Button(root, width=10, height=2, bg='gray',fg='white', text='相機參數發送', command=camera_setting_transmit)
get_camera_setting = Button(root, width=10, height=2, bg='gray',fg='white', text='相機連接', command=initial_camera_data)

AV_combo = ttk.Combobox(root,width=8,value=AV_value,state="readonly")
AV_combo.current(1)

ISO_combo = ttk.Combobox(root,width=8,value=ISO_value,state="readonly")
ISO_combo.current(0)

TV_combo = ttk.Combobox(root,width=8,value=TV_value,state="readonly")
TV_combo.current(18)

zoom_value = tk.Scale(root,from_=0,to=150 , orient='horizontal',background='#dcc6f0',highlightthickness=0)


canvas1.create_window(220,230, anchor='nw', window=transmit_btn)
canvas1.create_window(220,70, anchor='nw', window=camera_btn)
canvas1.create_window(310,230, anchor='nw', window=zero_btn)
canvas1.create_window(310,70, anchor='nw', window=camera_zero_btn)
canvas2.create_window(120,20, anchor='nw', window=excel_btn)
canvas2.create_window(210,20, anchor='nw', window=remove_excel_btn)
canvas2.create_window(120,350, anchor='nw', window=auto_start_btn)



canvas3.create_window(140,10, anchor='nw', window=photo_path)
canvas3.create_window(230,10, anchor='nw', window=photo_btn)
canvas3.create_window(70,110, anchor='nw', window=AV_combo)
canvas3.create_window(210,110, anchor='nw', window=ISO_combo)
canvas3.create_window(350,110, anchor='nw', window=TV_combo)
canvas3.create_window(70,150, anchor='nw', window=zoom_value)

canvas3.create_window(200,150, anchor='nw', window=camera_setting_btn)
canvas3.create_window(300,150, anchor='nw', window=get_camera_setting)
canvas1.create_text(50,50,text="角度 :",fill="white" ,font=('Helvetica 15 bold'))
canvas1.create_text(88,90,text="度",fill="white" ,font=('Helvetica 15 bold'))
canvas1.create_text(120,50,text="高度 :",fill="white" ,font=('Helvetica 15 bold'))
canvas1.create_text(180,90,text="毫米",fill="white" ,font=('Helvetica 15 bold'))

canvas1.create_text(190,250,text="度",fill="white" ,font=('Helvetica 15 bold'))
canvas1.create_text(160,280,text="範圍(0~359)",fill="red" ,font=('Helvetica 10 bold'))
canvas1.create_text(40,120,text="範圍(-90~90)",fill="red" ,font=('Helvetica 10 bold'))
canvas1.create_text(140,120,text="範圍(0~3000)",fill="red" ,font=('Helvetica 10 bold'))
canvas1.create_text(65,250,text="旋轉角度:",fill="white" ,font=('Helvetica 12 bold'))

canvas1.create_text(50,390,text="狀態:",fill="white" ,font=('Helvetica 12 bold'))
status_label = canvas1.create_text(100,390,text="完成",fill="green" ,font=('Helvetica 12 bold'))

canvas2.create_text(50,250,text="角度",fill="white" ,font=('Helvetica 15 bold'))
canvas2.create_text(150,250,text="高度",fill="white" ,font=('Helvetica 15 bold'))
canvas2.create_text(280,250,text="一圈攝影次數",fill="white" ,font=('Helvetica 15 bold'))


canvas2.create_text(50,410,text="自動化狀態:",fill="white" ,font=('Helvetica 12 bold'))
auto_status_label = canvas2.create_text(130,410,text="空置中",fill="green" ,font=('Helvetica 12 bold'))

canvas2.create_text(50,180,text="圈數進度:",fill="white" ,font=('Helvetica 12 bold'))
remain_circle = canvas2.create_text(160,180,text="0/0",fill="white" ,font=('Helvetica 15 bold'))

canvas2.create_text(65,210,text="當前單圈次數:",fill="white" ,font=('Helvetica 12 bold'))
remain_speerate_circle = canvas2.create_text(160,210,text="0/0",fill="white",font=('Helvetica 15 bold'))

canvas2.create_text(60, 85, text="檔案名稱 :", fill="white", font=('Helvetica 15 bold'))
file_label=canvas2.create_text(120, 85, text="", fill="white",anchor="w", font=('Helvetica 12 bold'))

camera_label=canvas3.create_text(120, 75, text="", fill="black",anchor="w", font=('Helvetica 12 bold'))

auto_angle_value = canvas2.create_window((50, 300), window=auto_angle_num,height=30, width=50)
auto_height_value= canvas2.create_window((150, 300), window=auto_height_num,height=30, width=50)
auto_seperate_value= canvas2.create_window((240, 300), window=auto_angle_separate,height=30, width=50)
image_name_value= canvas3.create_window((650, 40), window=image_name,height=30, width=150)



canvas2.create_text(60,40,text="檔案 :",fill="white" ,font=('Helvetica 15 bold'))

angle_value = canvas1.create_window((45, 90), window=angle_num,height=30, width=50)
height_value= canvas1.create_window((130, 90), window=height_num,height=30, width=50)
seperate_value= canvas1.create_window((150, 250), window=angle_separate,height=30, width=50)

canvas3.create_text(60,30,text="相片存放 :",fill="black" ,font=('Helvetica 15 bold'))
canvas3.create_text(60, 75, text="路徑名稱 :", fill="black", font=('Helvetica 15 bold'))

canvas3.create_text(40, 120, text="光圈:", fill="black", font=('Helvetica 15 bold'))
canvas3.create_text(180, 120, text="曝光:", fill="black", font=('Helvetica 15 bold'))
canvas3.create_text(320, 120, text="快門:", fill="black", font=('Helvetica 15 bold'))
canvas3.create_text(500, 120, text="電量:", fill="black", font=('Helvetica 15 bold'))
canvas3.create_text(40, 177, text="ZOOM:", fill="black", font=('Helvetica 12 bold'))
canvas3.create_text(520, 40, text="照片名稱:", fill="black", font=('Helvetica 12 bold'))
canvas3.create_text(35, 140, text="實際數值:", fill="RED", font=('Helvetica 10 bold'))
av_label=canvas3.create_text(83, 140, text="f4.0", fill="RED", font=('Helvetica 10 bold'))
iso_label=canvas3.create_text(225, 140, text="auto", fill="RED", font=('Helvetica 10 bold'))
tv_label=canvas3.create_text(361, 140, text="1/4", fill="RED", font=('Helvetica 10 bold'))
battery_label=canvas3.create_text(540, 120, text="", fill="black", anchor="w",font=('Helvetica 15 bold'))
#cap = cv2.VideoCapture(0)
#capture_video()
#root.overrideredirect(True)


#threading.Timer(0.2, mylog()).start()
root.resizable(width=0, height=0)
root.mainloop()
