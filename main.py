# import windows_toasts
import sys
from windows_toasts import WindowsToaster, ToastImageAndText1, ToastDisplayImage, ToastDuration, ToastAudio
from pathlib import Path
import os
import time
from datetime import datetime, timedelta


cwd = os.path.abspath(__file__)
parentDir = os.path.dirname(cwd)
DEFAULT_ICON_PATH = parentDir + "/bell.ico"

class WinToast:
    def __init__(self):
        pass
    
    def __init__(self, title : str, body : str, duration : str, iconPath : str = ""):
        self.title = title
        self.body = body
        self.duration = duration

        if not Path(iconPath).is_file(): # if the icon is not exists
            self.iconPath = DEFAULT_ICON_PATH
        else: self.iconPath = iconPath

    def GenerateToast(self):
        self.toaster = WindowsToaster(self.title)
        self.newToast = ToastImageAndText1()
        self.newToast.SetBody(self.body)
        self.newToast.SetDuration(ToastDuration(self.duration))
        self.audio = ToastAudio(silent = True)
        self.newToast.SetAudio(self.audio)
        self.newToast.AddImage(ToastDisplayImage.fromPath(self.iconPath))

    def ShowToast(self):
        self.toaster.show_toast(self.newToast)

def GoToast(title, body, duration, iconPath):
    toaster = WinToast(title, body, duration, iconPath)
    toaster.GenerateToast()
    toaster.ShowToast()

def Input():
    print("Toast generating program on windows.")
    title = input("Enter the toast title: ")
    body = input("Enter the toast body: ")
    try:
        duration = int(input("Enter the toast duration (Default : 0, Short : 1, Long : 2): "))
        if duration == 1:
            duration = "short"
        elif duration == 2:
            duration = "long"
        else:
            duration = "Default"
    except e:
        print("--Duration invalid, default duration selected")
        duration = "Default"
        
   
    iconPath = input("Enter icon path: ")
    return (title, body, duration, iconPath)

#First Param: Title
#Second Param: Body
#Third Param: Duration (short, default, long)
#Fourth Param: Repeat time interval (in minutes)
#Fifth Param: Icon Path
if __name__ == "__main__":
    print("Program starts.")
    if len(sys.argv) > 1 : #command line arguments passed in - called by another program
        title = sys.argv[1]
        body = sys.argv[2]
        duration = sys.argv[3]
        repeatInterval = sys.argv[4]
        iconPath = sys.argv[5]

        if len(sys.argv) >= 6 and issubclass(type(sys.argv[5]), str): # use icon
            iconPath = sys.argv[5]
    else : # taking user input from command line
        title, body, duration, iconPath = Input()
        repeatInterval = int(input("Enter the time you want the toast to repeat (minutes): "))
        

    print("Program processing...")
    # Repeated toasting
    while True:
        GoToast(title, body, duration, iconPath)
        currentTime = datetime.now()
        nextTime = currentTime + timedelta(seconds = repeatInterval * 60)
        print("Next time to toast: " + '{:%H:%M:%S}'.format(nextTime))
        time.sleep(repeatInterval * 60)

    
    print("Program ends.")
