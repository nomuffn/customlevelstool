from variables import *
from utils import *

def loadFolders():
    print()
    print("> Loading & checking for broken folders")
    allFolders.clear()
    brokenFolders.clear()
    invalidFormatFolders.clear()
    for folder in os.listdir(WORKINGDIR):
        if folder != recycleBin and folder != ".idea":
            broken = folderBroken(folder)
            if broken == BROKENNT:
                allFolders.append(folder)
            elif broken == ERROR_MAPFILES:
                brokenFolders.append(folder)
            elif broken == ERROR_FORMAT:
                invalidFormatFolders.append(folder)
    print("Finished loading all folders")


def convertToPlaylist():
    print()
    print("Converting CustomLevels folder to playlist")
    print()

    songs = []
    for folder in allFolders + invalidFormatFolders:
        #Open info.dat
        if "CustomLevelsToPlaylist_Converter.exe" in folder:
            continue

        try:
            infoDatPath = WORKINGDIR + "\\" + folder + "\\" + "info.dat"
            if not os.path.isfile(infoDatPath):
                print(folder + "\\" + "info.dat" + " doesnt exist, skipping folder")
                continue

            with open(infoDatPath, "rb") as f:
                infoFile = json.loads(f.read())
                songName = infoFile["_songName"]

                infoDat = open(infoDatPath, "rb")
                allFiles = infoDat.read()
                infoDat.close()

                #Iterate through all sets & maps
                for beatmapSets in infoFile["_difficultyBeatmapSets"]:
                    for diff in beatmapSets["_difficultyBeatmaps"]:

                        try:
                            #print(diff["_beatmapFilename"])
                            #Get content of each file and append
                            in_file = open(WORKINGDIR + "\\" + folder + "\\" + diff["_beatmapFilename"], "rb")
                            allFiles = allFiles + in_file.read()
                            in_file.close()

                        except IOError:
                            print("(beatmap) Invalid file: "+diff["_beatmapFilename"])
                            input("press enter to continue")

                hash_object = hashlib.sha1(allFiles)
                hashh = hash_object.hexdigest()
                songs.append((songName, hashh))
                #print("Song with hash added: "+songName, hashh)
                #print("---------------------------------")


        except IOError:
            print("(infoDat) Invalid folder: "+ folder)
            print("---------------------------------")
            input("press enter to continue")

    print("Added", len(songs), "songs")
    name = input("Enter your epic gamer name: ")
    newJson = {"playlistTitle": "CustomLevels Folder (" + str(len(songs)) + ") by " + name + " from " + str(date.today()),
               "playlistAuthor": "muffns customlevels to playlist script thingy",
               "playlistDescription": "Hopefully all custom levels put together in a playlist",
               "image": image}

    songsForJson = []
    for song in songs:
        item = { "hash": song[1], "songName": song[0] }
        songsForJson.append(item)
    newJson["songs"] = songsForJson

    print("Hopefully successfull yay")
    file = open("CustomLevels ("+str(len(songs))+" Songs) By "+name+" from "+str(date.today())+" .json", "w+")
    file.write(json.dumps(newJson))
    file.close()
    print("File saved to " + WORKINGDIR + "\\" + "CustomLevels ("+str(len(songs))+" Songs) By "+name+" from "+str(date.today())+".json")



def moveOldVersions():
    global allFolders
    print()
    print("Moving all old versions of a map to CustomLevels/#Recycle Bin")
    print()
    time.sleep(3)

    # sorted by names and has ids as list, ids will be checked
    sortedFolders = defaultdict(list)
    for folder in allFolders:
        sortedFolders[getFolderName(folder)]\
            .append(getFolderId(folder))

    #Remove older versions, checked by their ids
    for folderName in sortedFolders:

        ids = sortedFolders[folderName]

        #getHighestId
        highestId = sortedFolders[folderName][0]
        for folderId in ids:
            if folderId > highestId:
                highestId = folderId

        #delete all folders with lower id
        for folderId in ids:
            if folderId < highestId:
                fullFolderName = str(getHexString(folderId)) + " " + folderName
                try:
                    moveToRecycleBin(getFolderPath(fullFolderName))
                    print("> Moved to recycle bin: "+ fullFolderName)
                except FileNotFoundError:
                    print("X ERROR, Folder does not exist? skipping:", fullFolderName)

    print("done hahaball")



def moveNotUploadedMaps():
    global allFolders, uploadedMapsCache
    print()
    print("Moving all maps that arent uploaded anymore to CustomLevels/#Recycle Bin")
    print()

    for folder in allFolders:

        print("Checking:", folder)
        move = False

        if folder in uploadedMapsCache:
            print("- Using cached status")
            if not uploadedMapsCache[folder]:
                move = True
        else:
            uploaded = isUploaded(folder)
            if uploaded == BEATSAVER_UPLOADED:
                move = False
            elif uploaded == BEATSAVER_NOTFOUND:
                move = True

        if move:
            moveToRecycleBin(getFolderPath(folder))
            print("> Not uploaded, moved folder to CustomLevels/#Recycle Bin:")

            uploadedMapsCache[folder] = False
        else:
            uploadedMapsCache[folder] = True
            print("- Still uploaded")
    print("done hahaball")
    

def zipNotUploadedMaps():
    global allFolders, uploadedMapsCache
    print()
    print("Zipping all maps that arent uploaded anymore")
    print()

    foldersToZip = []
    for folder in allFolders:

        print("Checking:", folder)

        notUploaded = False

        if folder in uploadedMapsCache:
            print("- Using cached status")
            if not uploadedMapsCache[folder]:
                notUploaded = True

        else:
            uploaded = isUploaded(folder)
            if uploaded == BEATSAVER_UPLOADED:
                notUploaded = False
            elif uploaded == BEATSAVER_NOTFOUND:
                notUploaded = True
            else:
                print("ERROR, HTTPError:", uploaded)
                continue

        if notUploaded:
            print("- Not uploaded anymore")
            foldersToZip.append(folder)

            uploadedMapsCache[folder] = False
        else:
            uploadedMapsCache[folder] = True
            print("- Still uploaded")

    if len(foldersToZip) == 0:
        print("All maps are still uploaded poggers :o")
        input("press enter to continue")
    else:
        zipit(foldersToZip, "not uploaded maps anymore from "+str(date.today())+".zip")
        print("All maps zipped to: not uploaded maps anymore from "+str(date.today())+".zip")
        print("done hahaball")

def handleBrokenFolders():
    divider()
    print()
    print("Broken folders found, want to handle them or ignore them?")

    if prompt("y to handle, n to ignore them: "):

        print("Want to list all broken folders?")
        if prompt("Enter y/n: "):
            divider()
            print("Broken Folders: ")
            for folder in brokenFolders:
                print("-", folder)

        print("Do you want to move all broken folders to the recycle bin?")
        if prompt("Enter y/n: "):
            for folder in brokenFolders:
                moveToRecycleBin(getFolderPath(folder))
                print("> Moved to CustomLevels/#Recycle Bin:", folder)
        else:
            print("Folders will be skipped")

    else:
        print("Folders will be skipped")

def moveBrokenFolders():
    for folder in brokenFolders:
        print("> Moving to CustomLevels/#Recycle Bin:", folder)
        moveToRecycleBin(getFolderPath(folder))
    brokenFolders.clear()
    print("> Done")

def handleInvalidFormatFolders():
    for folder in invalidFormatFolders:
        print(">", folder)
    print("Wanna move all those folders to", recycleBinString, "?")
    if prompt("Enter y/n: "):
        for folder in invalidFormatFolders:
            print("> Moving to CustomLevels/#Recycle Bin:", folder)
            moveToRecycleBin(getFolderPath(folder)  )
        invalidFormatFolders.clear()
        print("> Done")
