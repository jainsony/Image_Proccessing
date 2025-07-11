# https://wiki.nexusmods.com/index.php/DirectX_Scancodes_And_How_To_Use_Them

import ctypes
import time

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

# directx scan codes http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
while (True):
    a = 17
    PressKey(a)
    time.sleep(1)
    ReleaseKey(a)
    time.sleep(1)
    a = 36
    PressKey(a)
    time.sleep(1)
    ReleaseKey(a)

    time.sleep(1)



wda


###################################

# import ctypes
# import time

# SendInput = ctypes.windll.user32.SendInput

# # C struct redefinitions 
# PUL = ctypes.POINTER(ctypes.c_ulong)
# class KeyBdInput(ctypes.Structure):
#     _fields_ = [("wVk", ctypes.c_ushort),
#                 ("wScan", ctypes.c_ushort),
#                 ("dwFlags", ctypes.c_ulong),
#                 ("time", ctypes.c_ulong),
#                 ("dwExtraInfo", PUL)]

# class HardwareInput(ctypes.Structure):
#     _fields_ = [("uMsg", ctypes.c_ulong),
#                 ("wParamL", ctypes.c_short),
#                 ("wParamH", ctypes.c_ushort)]

# class MouseInput(ctypes.Structure):
#     _fields_ = [("dx", ctypes.c_long),
#                 ("dy", ctypes.c_long),
#                 ("mouseData", ctypes.c_ulong),
#                 ("dwFlags", ctypes.c_ulong),
#                 ("time",ctypes.c_ulong),
#                 ("dwExtraInfo", PUL)]

# class Input_I(ctypes.Union):
#     _fields_ = [("ki", KeyBdInput),
#                  ("mi", MouseInput),
#                  ("hi", HardwareInput)]

# class Input(ctypes.Structure):
#     _fields_ = [("type", ctypes.c_ulong),
#                 ("ii", Input_I)]

# # Actuals Functions

# def PressMouseLeftButton():
#     # Set mouse left button down
#     extra = ctypes.c_ulong(0)
#     ii_ = Input_I()
#     ii_.mi = MouseInput(0, 0, 0, 0x0002, 0, ctypes.pointer(extra))
#     x = Input(ctypes.c_ulong(0), ii_)
#     ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# def ReleaseMouseLeftButton():
#     # Set mouse left button up
#     extra = ctypes.c_ulong(0)
#     ii_ = Input_I()
#     ii_.mi = MouseInput(0, 0, 0, 0x0004, 0, ctypes.pointer(extra))
#     x = Input(ctypes.c_ulong(0), ii_)
#     ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# # Simulate left mouse click
# while 1:
#     PressMouseLeftButton()
#     time.sleep(1)
#     ReleaseMouseLeftButton()
#     time.sleep(1)
