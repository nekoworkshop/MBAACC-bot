# direct inputs
# source to this solution and code:
# http://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
# http://www.gamespp.com/directx/directInputKeyboardScanCodes.html

import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

#scancodes
W = 0x11
A = 0x1E
S = 0x1F
D = 0x20
J = 0x24
U = 0x16
I = 0x17
O = 0x18
L = 0x26

#Mapped in-game key config
#numbers represent directions (look at your numpad)
Input_4 = A
Input_2 = S
Input_6 = D
Input_8 = W

#Light, medium, heavy attack, guard and throw/supercharge
Input_A = U
Input_B = I
Input_C = O
Input_D = J
Input_ABC = L

MINIMAL_INPUT_DELAY = 0.03

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

Input_command_array = [Input_4,Input_2,Input_6,Input_8,Input_A,Input_B,Input_C,Input_D,Input_ABC]
previous_movement = None
def SendCommand(command):

    #check if the new command is a continous movement state (walking,crouching,dashing).
    if command <= 6:
       if command == previous_movement:  #Continue current movement state
           return
       else: #A new movement state has been called
            Remove_movement_state()
            Enter_movement_state(command)
            return

    #The command is a skill move or instant movement(jump)
    Remove_movement_state()
    send_single_move(command)



def Enter_movement_state(state):
    assert state <= 6
    if state == 0:          #walk left
        PressKey(Input_4)
    elif state == 1:        #walk right
        PressKey(Input_6)
    elif state == 2:        #crouch
        PressKey(Input_2)
    elif state == 3:        #crouch defense
        PressKey(Input_4)
        PressKey(Input_2)
    elif state == 4:        #crouch defense
        PressKey(Input_6)
        PressKey(Input_2)
    elif state == 5:        #dash left
        PressKey(Input_4)
        time.sleep(MINIMAL_INPUT_DELAY)
        ReleaseKey(Input_4)
        time.sleep(MINIMAL_INPUT_DELAY)
        PressKey(Input_4)
    elif state == 6:        #dash right
        PressKey(Input_6)
        time.sleep(MINIMAL_INPUT_DELAY)
        ReleaseKey(Input_6)
        time.sleep(MINIMAL_INPUT_DELAY)
        PressKey(Input_6)

def Remove_movement_state():
    ReleaseKey(Input_4)
    ReleaseKey(Input_6)
    ReleaseKey(Input_2)

def send_single_move(command):
    #The command should start at 7
    if command == 7:        #jump upwards
        PressKey(Input_8)
        input_delay()
        ReleaseKey(Input_8)
    if command == 8:        #jump left
        PressKey(Input_8)
        PressKey(Input_4)
        input_delay()
        ReleaseKey(Input_8)
        ReleaseKey(Input_4)
    if command == 9:        #jump right
        PressKey(Input_8)
        PressKey(Input_6)
        input_delay()
        ReleaseKey(Input_8)
        ReleaseKey(Input_6)
    if command == 10:       #stand A attack
        PressKey(Input_A)
        input_delay()
        ReleaseKey(Input_A)
    if command == 11:       #stand B attack
        PressKey(Input_B)
        input_delay()
        ReleaseKey(Input_B)
    if command == 12:       #stand C attack
        PressKey(Input_C)
        input_delay()
        ReleaseKey(Input_C)
    if command == 13:       #crouch A attack
        PressKey(Input_2)
        input_delay()
        PressKey(Input_A)
        input_delay()
        ReleaseKey(Input_2)
        ReleaseKey(Input_A)
    if command == 14:       #236A
        PressKey(Input_2)
        input_delay()
        PressKey(Input_6)
        input_delay()
        ReleaseKey(Input_2)
        PressKey(Input_A)
        input_delay()
        ReleaseKey(Input_6)
        input_delay()
        ReleaseKey(Input_A)
    if command == 15:       #236B
        PressKey(Input_2)
        input_delay()
        PressKey(Input_6)
        input_delay()
        ReleaseKey(Input_2)
        PressKey(Input_B)
        input_delay()
        ReleaseKey(Input_6)
        input_delay()
        ReleaseKey(Input_B)
    if command == 16:       #236C
        PressKey(Input_2)
        input_delay()
        PressKey(Input_6)
        input_delay()
        ReleaseKey(Input_2)
        PressKey(Input_C)
        input_delay()
        ReleaseKey(Input_6)
        input_delay()
        ReleaseKey(Input_C)
    if command == 17:       #214A
        PressKey(Input_2)
        input_delay()
        PressKey(Input_4)
        input_delay()
        ReleaseKey(Input_2)
        PressKey(Input_A)
        input_delay()
        ReleaseKey(Input_4)
        input_delay()
        ReleaseKey(Input_A)

    if command == 18:       #214B
        PressKey(Input_2)
        input_delay()
        PressKey(Input_4)
        input_delay()
        ReleaseKey(Input_2)
        PressKey(Input_B)
        input_delay()
        ReleaseKey(Input_4)
        input_delay()
        ReleaseKey(Input_B)

    if command == 17:       #214C
        PressKey(Input_2)
        input_delay()
        PressKey(Input_4)
        input_delay()
        ReleaseKey(Input_2)
        PressKey(Input_C)
        input_delay()
        ReleaseKey(Input_4)
        input_delay()
        ReleaseKey(Input_C)

def input_delay(delay = MINIMAL_INPUT_DELAY):
    time.sleep(delay)

#contemplating if I should use more specific "moves" as output or go a more general way.
def Move_236A():
    PressKey(Input_2)
    time.sleep(0.03)
    PressKey(Input_6)
    time.sleep(0.03)
    ReleaseKey(Input_2)
    PressKey(Input_A)
    time.sleep(0.03)
    ReleaseKey(Input_6)
    time.sleep(0.03)
    ReleaseKey(Input_A)

if __name__ == '__main__':
    PressKey(W)
    time.sleep(1)
    ReleaseKey(W)
    time.sleep(1)