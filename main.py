# import windows_toasts
import sys
from windows_toasts import WindowsToaster, ToastImageAndText1, ToastDisplayImage, ToastDuration, ToastAudio
from pathlib import Path
import os
import time
from datetime import datetime, timedelta


# Lấy đường dẫn của file đang thực thi
current_file_path = os.path.abspath(__file__)

# Lấy đường dẫn tới thư mục chứa file đang thực thi
parent_directory = os.path.dirname(current_file_path)

# Đường dẫn mặc định tới file icon
DEFAULT_ICON_PATH = parent_directory + "/bell.ico"

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
    print("Chuong trinh tao toast tren windows.")
    title = input("Nhap title cua toast: ")
    body = input("Nhap body cua toast: ")
    duration = int(input("Nhap duration (Default : 0, Short : 1, Long : 2): "))
        
    if duration == 1:
        duration = "short"
    elif duration == 2:
        duration = "long"
    else:
        duration = "Default"
    iconPath = input("Nhap icon path: ")
    return (title, body, duration, iconPath)

#First Param: Title
#Second Param: Body
#Third Param: Duration (short, default, long)
#Fourth Param: Icon Path
#Fifth Param: Repeat time interval (in minutes)
if __name__ == "__main__":
    print("Program starts.")
    if len(sys.argv) > 1 : #command line arguments passed in - called by another program
        title = sys.argv[1]
        body = sys.argv[2]
        duration = sys.argv[3]
        iconPath = ""
        repeatInterval = sys.argv[4]

        if len(sys.argv) >= 6 and issubclass(type(sys.argv[4]), str): # use icon
            iconPath = sys.argv[4]
    else : # taking user input from command line
        title, body, duration, iconPath = Input()
        repeatInterval = int(input("Nhap thoi gian ban muon thong bao lap lai (phut): "))
        

    print("Program processing...")
    stop = False
    while not stop:
        GoToast(title, body, duration, iconPath)
        currentTime = datetime.now()
        nextTime = currentTime + timedelta(seconds = repeatInterval * 60)
        print("Next time to toast: " + '{:%H:%M:%S}'.format(nextTime))
        time.sleep(repeatInterval * 60)

    
    print("Program ends.")