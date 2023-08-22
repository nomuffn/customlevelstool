from variables import *
from utils import *
from actions import *

def menu():
    input("Enter to go to menu")
    
    inputValues = ["e", "r", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    divider()
    print("Menu")
    print()
    print("Maps will never be deleted, they will always be moved to", recycleBinString)
    print("Feel free to delete all the maps in there or the entire folder")
    print()
    print("Only loaded folders will be handled in any option you choose")
    print()
    print("> Folders loaded:", len(allFolders))
    print("> Broken folders:", len(brokenFolders), "(wont work ingame anymore)")
    print("> Skipped folders with invalid folder name format:", len(invalidFormatFolders), "(still work in-game)")
    print()
    print("--- Options ---")
    if len(brokenFolders) > 0:
        print("[1] Move broken folders to CustomLevels/#Recycle Bin")
    if len(invalidFormatFolders) > 0:
        print("[2] List folders with invalid folder names")
    print("[3] Convert CustomLevels folder to playlist (invalid format folders included if possible)")
    print("[4] Move old versions of a map to", recycleBinString)
    print("    - for example have multiple battle sirens mapsets, only the one with the highest id will stay")
    print("[5] List all maps that arent uploaded anymore")

    print("[6] Zip all maps that arent uploaded anymore")
    print("[7] Download & create playlist from all maps of a mapper")
    print("[8] Check for reuploads")
    print("[9] Download all refugee camp covers lohl")

    print()
    print("[r] Reload folders")
    print("[e] Exit")

    divider()
    inputValue = 0
    while inputValue not in inputValues:
        inputValue = input("Choose an option:")

    divider()
    if inputValue == "1":
        moveBrokenFolders()
    elif inputValue == "2":
        handleInvalidFormatFolders()
    elif inputValue == "3":
        convertToPlaylist()
    elif inputValue == "4":
        moveOldVersions()
    elif inputValue == "5":
        moveNotUploadedMaps()

    elif inputValue == "6":
        zipNotUploadedMaps()
    elif inputValue == "7":
        downloadSongsFromMapper()

    elif inputValue == "r":
        loadFolders()
    elif inputValue == "e":
        exit()