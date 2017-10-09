from MBAACC_Bot.controllerInputInjector import *

def singleCommand(key):
    button_input(key)


# 0 1 2 3 4 5 6 7 8  9 10 11 12 13 14   15 16 17 18 19 20    21 22 23 24 25 26   27   28 29    30
# |<--pure stick-->| A with directions| B with directions | C with directions  | QA | Throw | Block
def sendCommand(input):

    # Check if the input is a pure stick movement
    if input <= 8:

        #compensate the 1 offset between index and actual stick input value
        stick_input(input+1)

    # If the input contains button (direction + button)
    else:

        if input == 27:
            stick_input(5)
            button_input("QA")
            return
        elif input == 28:
            stick_input(4)
            button_input("QA")
            return
        elif input == 29:
            stick_input(6)
            button_input("QA")
            return
        elif input == 30:
            stick_input(5)
            button_input("D")
            return

        direction = (input-9) % 6
        button = (input-9) // 6

        if direction == 0:
            stick_input(1)
        elif direction == 1:
            stick_input(2)
        elif direction == 2:
            stick_input(3)
        elif direction == 3:
            stick_input(4)
        elif direction == 4:
            stick_input(5)
        elif direction == 5:
            stick_input(6)

        time.sleep(0.1)

        if button == 0:
            button_input("A")
        if button == 1:
            button_input("B")
        if button == 2:
            button_input("C")


if __name__ == "__main__":
    for x in range(0,32):
        time.sleep(1)
        sendCommand(x)
