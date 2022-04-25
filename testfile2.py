# Automatically connects to arduino via name, can read data and insert data to txt file.
import webbrowser
from tkinter import *
from tkinter import messagebox
import serial.tools.list_ports
import threading
import datetime

root = Tk()
root.geometry('800x500')
new_file_name = None
list = []
# -------------------------<functions>-------------------------

def arduino_serial_data():
    def get_ports():
        ports = serial.tools.list_ports.comports()

        return ports

    def findArduino(portsFound):
        commPort = 'None'
        numConnection = len(portsFound)

        for i in range(0, numConnection):
            port = foundPorts[i]
            strPort = str(port)

            if "Arduino" in strPort:
                splitPort = strPort.split(' ')
                commPort = (splitPort[0])

        return commPort

    foundPorts = get_ports()
    connectPort = findArduino(foundPorts)

    if connectPort != 'None':
        ser = serial.Serial(connectPort, baudrate=9600, timeout=1)
        print('Connected to ' + connectPort)
    else:
        print('Connection Issue!, try reconnecting your device.')
    def loop_test():
        try:
            data = ser.readline()
            text = data.decode()
            print(text)
            list.append(text)
            print(list)
            root.after(900, loop_test)
        except serial.serialutil.SerialException:
            print("Arduino device disconnected")
    loop_test()


def save_data():
    data_file = open(str(new_file_name) + ".txt", 'w')
    data_file.writelines(list)
    data_file.close()

def exit_confirmation():
    confirmation = messagebox.askokcancel('message box', 'Are you sure you want to continue?')
    if confirmation == True:
        root.destroy()
    else:
        None


def createNewWindow():
    win = Toplevel(root)

    def clicked():
        Input = entry1.get()
        FileName = str(Input)
        TextFile = open(str(FileName) + ".txt", "x")
        global new_file_name
        new_file_name = entry1.get()
        print(new_file_name)

    entry1 = Entry(win)
    button1 = Button(win, text="Press to create text file", command=clicked)
    entry1.pack()
    button1.pack()


def new_file():
    pass


def web_site():
    webbrowser.open('example.com')


# -------------------------<functions>-------------------------

my_menu = Menu(root, tearoff=0)
root.config(menu=my_menu)

if new_file_name != None:
    print(new_file_name)
else:
    pass

file_menu = Menu(my_menu)
file_menu.add_command(label='open', command=new_file)
file_menu.add_command(label='new file', command=createNewWindow)
file_menu.add_command(label='Exit', command=exit_confirmation)
file_menu.add_command(label='Read arduino data', command=arduino_serial_data)
file_menu.add_command(label='Save file', command=save_data)
my_menu.add_cascade(label='File', menu=file_menu)

help_menu = Menu(my_menu)
help_menu.add_command(label='About our project', command=web_site)
my_menu.add_cascade(label='Help', menu=help_menu)

root.mainloop()
