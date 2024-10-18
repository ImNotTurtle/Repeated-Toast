import sys
from windows_toasts import WindowsToaster, Toast, ToastDisplayImage, ToastDuration, ToastAudio
from pathlib import Path
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
import ctypes
import winreg as reg  # Windows Registry access

CWD = os.path.abspath(__file__)
PARENT_DIR = os.path.dirname(CWD)
DEFAULT_ICON_LIGHT = PARENT_DIR + "/bell_light.ico"
DEFAULT_ICON_DARK = PARENT_DIR + "/bell_dark.ico"

def IsDarkMode():
    """Check windows background mode (light / dark mode)"""
    try:
        registry = reg.OpenKey(reg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize')
        value, _ = reg.QueryValueEx(registry, 'AppsUseLightTheme')
        reg.CloseKey(registry)
        # value == 0 is dark mode, != 0 is light mode
        return value == 0
    except Exception as e:
        print(f"Error reading theme setting: {e}")
        return False  # default to light mode


class WinToast:
    def __init__(self, title: str, body: str, duration: str, iconPath: str = ""):
        self.title = title
        self.body = body
        self.duration = duration
        if iconPath == "" or not Path(iconPath).is_file(): # empty icon path or icon path does not exist
            # use default icon
            if IsDarkMode():
                self.iconPath = DEFAULT_ICON_LIGHT
            else: 
                self.iconPath = DEFAULT_ICON_DARK
        else:
            self.iconPath = iconPath

    def GenerateToast(self):
        self.toaster = WindowsToaster(self.title)
        self.newToast = Toast([self.title, self.body])  # Set title and body in the constructor
        self.newToast.duration = ToastDuration(self.duration)  # Set the duration
        self.newToast.audio = ToastAudio(silent=True)  # Set silent audio
        
        # Check icon path before toasting
        if iconPath != "" or Path(self.iconPath).is_file():
            self.newToast.AddImage(ToastDisplayImage.fromPath(self.iconPath))  # Add image from the icon path
        else:
            pass

    def ShowToast(self):
        self.toaster.show_toast(self.newToast)

def GoToast(title, body, duration, iconPath):
    toaster = WinToast(title, body, duration, iconPath)
    toaster.GenerateToast()
    toaster.ShowToast()

def Input():
    print("Toast generating program on Windows.")
    title = input("Enter the toast title: ")
    body = input("Enter the toast body: ")
    try:
        duration = int(input("Enter the toast duration (Short: 1, Long: 2): "))
        if duration == 1:
            duration = "short"
        elif duration == 2:
            duration = "long"
        else:
            print("--Invalid duration, defaulting to 'short'")
            duration = "short"  # Set default to "short"
    except Exception as e:
        print("--Duration invalid, defaulting to 'short'")
        duration = "short"  # Set default to "short"

    iconPath = input("Enter icon path: ")
    return (title, body, duration, iconPath)

# First Param: Title
# Second Param: Body
# Third Param: Duration (short, default, long)
# Fourth Param: Repeat time interval (in minutes)
# Fifth Param: Icon Path
if __name__ == "__main__":
    print("Program starts.")
    if len(sys.argv) > 1:  # command line arguments passed in - called by another program
        title = sys.argv[1]
        body = sys.argv[2]
        duration = sys.argv[3]
        repeatInterval = sys.argv[4]
        iconPath = sys.argv[5]

        if len(sys.argv) >= 6 and isinstance(sys.argv[5], str):  # use icon
            iconPath = sys.argv[5]
    else:  # taking user input from command line
        title, body, duration, iconPath = Input()
        repeatInterval = int(input("Enter the time you want the toast to repeat (minutes): "))

    print("Program processing...")
    while True:
        GoToast(title, body, duration, iconPath)
        currentTime = datetime.now()
        nextTime = currentTime + timedelta(seconds=repeatInterval * 60)
        print("Next time to toast: " + '{:%H:%M:%S}'.format(nextTime))
        time.sleep(repeatInterval * 60)

    print("Program ends.")
