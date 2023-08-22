
import os
from variables import *
from menu import *
from actions import *

if DEBUG:
    print("debug, workingdir:", WORKINGDIR)
elif WORKINGDIR.split(os.sep)[-1] != "CustomLevels":
    input("Run this program in your CustomLevels folder >:(")
    exit()

input("Press enter to start loading folders")
loadFolders()

while(True): 
    menu()

