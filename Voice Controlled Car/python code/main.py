import pyttsx3
import speech_recognition as sr
import time
import serial

control_string = ""
control_string += str(0)+"," + str(0) +","+ str(0) +"," + str(0) + "\n"
speed = 50
ser = serial.Serial(port='COM8',baudrate=115200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)

print("Jarvis Initializing...")
time.sleep(1)

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Jarvis waiting for command...")
        audio=r.listen(source)
        try:
            print("processing...")
            query=r.recognize_google(audio, language='en-in')
        except Exception as e:
            print("Try Again...")
            return "None"
        return query
    
def send_serial(go):
        control_string = "<"+str(go) +","+ str(0)  +","+str(0)  +","+str(0)+">"+"\n"
        print(control_string)
        ser.write(str.encode(control_string))
        time.sleep(0.1)

def main_call():
    go = 0
    while True:
        query=takeCommand().lower()
        if 'move forward' in query:
            print("move forward...")
            speak("moving forward...")
            go = -1*speed
            send_serial(go)
            
        elif 'move backward' in query:
            print("moving backward...")
            speak("moving backward...")
            go = speed
            send_serial(go)
            
        elif 'stop' in query:
            print("stop...")
            speak("stopping the robot...")
            go = 0
            send_serial(go)

        elif 'shutdown' in query:
            print("program shutdown...")
            speak("I am shutting down the program...")
            break

if __name__=="__main__":
    main_call()

"""

"""