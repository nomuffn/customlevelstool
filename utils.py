import os
import hashlib
import time
import zipfile
from datetime import date
from collections import defaultdict
import shutil
import json
import os.path
import urllib.request
import traceback
import logging
from variables import *
from ratelimit import limits, sleep_and_retry

def prompt(errorMessage):
    yesno = ""
    while yesno != "y" and yesno != "n":
        yesno = input(errorMessage)

    if yesno == "y":
        return True
    else:
        return False

def promptYYNN(errorMessage):
    yesno = ""
    while yesno != "y" and yesno != "n" and yesno != "yy" and yesno != "nn":
        yesno = input(errorMessage)

    return yesno

def getFolderPath(folder):
    return WORKINGDIR + "\\" + folder

def divider():
    print("--------------------------------")

def moveToRecycleBin(folderPath):
    try:
        if not os.path.exists(recycleBin):
            os.makedirs(recycleBin)

        folderName = folderPath.split(os.sep)[-1]
        newFolderPath = os.path.join(recycleBin, folderName)
        if os.path.exists(newFolderPath):
            #in case the dir already exists, rename & move
            count = 1
            target = newFolderPath
            while os.path.exists(target):
                count += 1
                target = os.path.join(recycleBin, os.path.splitext(folderName)[0] + " (%d)" % count)

            newFolderPath = folderPath + " ("+str(count)+")"
            os.rename(
                folderPath,
                newFolderPath)
            shutil.move(newFolderPath, getFolderPath(recycleBin))
        else:
            shutil.move(folderPath, getFolderPath(recycleBin))
    except FileNotFoundError:
        print("ERROR, Folder not found for some very odd reasons, most likely a small bug:", folderPath)

def getFolderId(folder):
    return int(folder.split(" ", 1)[0], 16)

def getHexString(id):
    return str(hex(id))[2:]

def getFolderName(folder):
    return folder.split(" ", 1)[1]

def formatBroken(folder):
    try:
        getFolderId(folder)
        getFolderName(folder)
        return False
    except (ValueError, IndexError):
        #not a song folder or broken format
        return True

def mapFilesBroken(folder):
    infoDatPath = WORKINGDIR + "\\" + folder + "\\" + "info.dat"
    if not os.path.isfile(infoDatPath):
        return True

    try:
        with open(infoDatPath, "rb") as f:
            infoFile = json.loads(f.read())
            for beatmapSets in infoFile["_difficultyBeatmapSets"]:
                for diff in beatmapSets["_difficultyBeatmaps"]:
                        in_file = open(WORKINGDIR + "\\" + folder + "\\" + diff["_beatmapFilename"], "rb")
                        in_file.close()
    except:
        return True

    return False


def folderBroken(folder):
    #print("> Checking:", folder)
    if mapFilesBroken(folder):
        #print("- Skipping folder, map files are broken")
        return ERROR_MAPFILES

    if formatBroken(folder):
        #print("- Skipping folder, broken format, right format would be: id (Songname - Mapper)")
        return ERROR_FORMAT

    return BROKENNT


@sleep_and_retry
@limits(calls=7, period=10)
def isUploaded(folder):
    url = "https://beatsaver.com/api/maps/detail/" + getHexString(getFolderId(folder))
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = {'User-Agent': user_agent}
    req = urllib.request.Request(url, headers=headers)

    try:
        contents = urllib.request.urlopen(req)
        response = contents.read()
        if response == "Not Found":
            return BEATSAVER_NOTFOUND
    except (urllib.error.HTTPError, urllib.error.URLError) as e: #cannot resolve error? TODO
        return BEATSAVER_NOTFOUND

    return BEATSAVER_UPLOADED


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))
def zipit(dir_list, zip_name):
    zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for dir in dir_list:
        zipdir(dir, zipf)
    zipf.close()

def moveFoldersToRecycleBin(list):
    for folder in list:
        moveToRecycleBin(getFolderPath(folder))

def getResponseFromUrl(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = {'User-Agent': user_agent}
    req = urllib.request.Request(url, headers=headers)
    try:
        contents = urllib.request.urlopen(req)
        response = contents.read()
        return response
    except (urllib.error.HTTPError, urllib.error.URLError):
        return -1


# def loadValuesIntoList(json, list):
#     if json == -1:
#         return

#     for value in json:
#         list.append(value)

# def downloadSongsFromList():
#     if not mappers:
#         loadValuesIntoList(
#             getResponseFromUrl(urlMappers), mappers)
#     if not artists:
#         loadValuesIntoList(
#             getResponseFromUrl(urlArtists), artists)

#     exit()


@sleep_and_retry
@limits(calls=7, period=10)
def callBeatsaverApi(endpoint):
    req = Request("https://api.beatsaver.com/" + endpoint, headers={'User-Agent': 'Mozilla/5.0'})
    return json.loads(urlopen(req).read())
