from mss import mss
import cv2
from PIL import Image
import numpy as np
from time import time
import pyautogui
import time as delays
import ctypes

SendInput = ctypes.windll.user32.SendInput

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




mon = {'top': 290, 'left':0, 'width':960, 'height':540}
#               X                               Y
sct = mss()
delays.sleep(1)
print(pyautogui.position())
# pyautogui.click(480, 120, duration=0.2)
# pyautogui.click(button='right', duration=0.2)  # right-click the 
while 1:
    # begin_time = time()
    # sct_img = sct.grab(mon)
    # img = Image.frombytes('RGB', (sct_img.size.width, sct_img.size.height), sct_img.rgb)
    # img_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    # cv2.imshow('test', np.array(img_bgr))

    # pyautogui.click(480, 120, duration=0.1)
    # # pyautogui.click(button='right', duration=0.1)  # right-click the 
    # print('This frame takes {} seconds.'.format(time()-begin_time))
    # if cv2.waitKey(25) & 0xFF == ord('q'):
    #     cv2.destroyAllWindows()
    #     break
    
    position = pyautogui.position()
    print(position)

    pyautogui.moveTo(455, 755, duration=1)

    a = 36
    PressKey(a)
    delays.sleep(1)
    ReleaseKey(a)

    delays.sleep(1)
    