
from spnav import *
import uinput

# In KSP set to 1 sensitivity and 0.05 of deadzone for each axis

# Button mapping on the spacepilot pro
# For other controllers, use the log output of this program to figure out which button has which id
butmap = [0,1,2,4,5,8,10,12,13,14,15,16,22,23,24,25,26,27,28,29,30] # 21 buttons w/ long press
# The uinput button that is triggered by the mouse buttons
buts = [
    uinput.BTN_SELECT, # Menu
    uinput.BTN_START, # Fit
    uinput.BTN_Y, # TopView
    uinput.BTN_B, # RightView
    uinput.BTN_C, # FrontView
    uinput.BTN_X, # Rotate View
    uinput.BTN_A, # ISO1
    uinput.BTN_Z, # 1
    uinput.BTN_TR, # 2
    uinput.BTN_TL, # 3
    uinput.BTN_TL2, # 4
    uinput.BTN_TR2, # 5
    uinput.BTN_NORTH, # ESC
    uinput.BTN_SOUTH, # ALT
    uinput.BTN_EAST, # SHIFT
    uinput.BTN_WEST, # CTRL
    uinput.BTN_BASE, # Lock rot
    uinput.BTN_BASE2, # Lock trans
    uinput.BTN_BASE3, # Lock dominant
    uinput.BTN_BASE4, # +
    uinput.BTN_BASE5, # -
    # uinput.BTN_THUMB, # uinput.BTN_0, # X 1
    # uinput.BTN_TRIGGER, # uinput.BTN_7,
    # uinput.BTN_BASE6, # 22 # OK
    # uinput.BTN_TOP, # ----
    # uinput.BTN_TOP2, # ---- OK
    # uinput.BTN_THUMB2, # OK
]

axis = [uinput.ABS_X, uinput.ABS_Y, uinput.ABS_Z, uinput.ABS_RX, uinput.ABS_RY, uinput.ABS_RZ]

# May depend on mouse
axeMax = 500
def factor(n):
    return int(32767 * n / 500)


####################################################################3

print("Connecting to spacenav")
spnav_open()
print("Connecting uinput device")
with uinput.Device(axis + buts) as device:
    try:
        while True:
            event = spnav_wait_event()
            print(event)
            if event.ev_type == 1: # Motion
                trans = event.translation
                rot = event.rotation
                device.emit(axis[0], factor(trans[0])) # Side (0)
                device.emit(axis[1], factor(trans[1])) # Up down (1)
                device.emit(axis[2], factor(trans[2])) # Forward (2)
                device.emit(axis[3], factor(rot[0]))# Rot Pitch (3)
                device.emit(axis[4], factor(rot[1]))# Roll (inverted) (4)
                device.emit(axis[5], factor(rot[2]))# Yaw  (5)
            elif event.ev_type == 2: # Button
                bnum = event.bnum
                state = event.press
                try:
                    device.emit(buts[butmap.index(bnum)], state)
                except ValueError:
                    pass
    except KeyboardInterrupt:
        print("Closing...")
