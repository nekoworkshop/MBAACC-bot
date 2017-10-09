from MBAACC_Bot.pyvjoy.vjoydevice import *
from MBAACC_Bot.pyvjoy._sdk import *
from MBAACC_Bot.pyvjoy.constants import *

import time

BUTTON_1 = 1
BUTTON_2 = 2
BUTTON_3 = 4
BUTTON_4 = 8
BUTTON_5 = 16
BUTTON_6 = 32
BUTTON_7 = 64
BUTTON_8 = 128

j = VJoyDevice(1,None)

'''
0--------0x8000> X+
|
|
|     N(0x4000,0x4000)
|
|
0x8000
v Y+
'''

def stick_input(direction):


    if direction == 1:
        j.data.wAxisX = 0x1
        j.data.wAxisY = 0x8000
    elif direction == 2:
        j.data.wAxisX = 0x4000
        j.data.wAxisY = 0x8000
    elif direction == 3:
        j.data.wAxisX = 0x8000
        j.data.wAxisY = 0x8000
    elif direction == 4:
        j.data.wAxisX = 0x1
        j.data.wAxisY = 0x4000
    elif direction == 5:
        j.data.wAxisX = 0x4000
        j.data.wAxisY = 0x4000
    elif direction == 6:
        j.data.wAxisX = 0x8000
        j.data.wAxisY = 0x4000
    elif direction == 7:
        j.data.wAxisX = 0x1
        j.data.wAxisY = 0x1
    elif direction == 8:
        j.data.wAxisX = 0x4000
        j.data.wAxisY = 0x1
    elif direction == 9:
        j.data.wAxisX = 0x8000
        j.data.wAxisY = 0x1
    j.update()

def button_input(button_id):
    if button_id == "A":
        j.data.lButtons = BUTTON_1
    elif button_id == "B":
        j.data.lButtons = BUTTON_2
    elif button_id == "C":
        j.data.lButtons = BUTTON_3
    elif button_id == "D":
        j.data.lButtons = BUTTON_4
    elif button_id == "QA":
        j.data.lButtons = BUTTON_5
    elif button_id == "FN2":
        j.data.lButtons = BUTTON_6
    j.update()
    time.sleep(0.1)
    j.data.lButtons = 0
    j.update()

def reset_buttons():
    j.reset_buttons()

def buttonTest():

    j.data.lButtons = BUTTON_1
    time.sleep(0.5)
    j.update()
    j.data.lButtons = BUTTON_2
    time.sleep(0.5)
    j.update()
    j.data.lButtons = BUTTON_3
    time.sleep(0.5)
    j.update()
    j.data.lButtons = BUTTON_4
    time.sleep(0.5)
    j.update()
    j.data.lButtons = BUTTON_5
    time.sleep(0.5)
    j.update()
    j.data.lButtons = BUTTON_6
    time.sleep(0.5)
    j.update()
    j.data.lButtons = BUTTON_7
    time.sleep(0.5)
    j.update()
    j.data.lButtons = BUTTON_8
    time.sleep(0.5)
    j.update()

if __name__ =="__main__":
    while True:
        print("resetting input")
        j.reset_buttons()
        j.data.wAxisX = 0x4000
        j.data.wAxisY = 0x4000
        j.update()
        time.sleep(3)
        buttonTest()
        print("nya")
