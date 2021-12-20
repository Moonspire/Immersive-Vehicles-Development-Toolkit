# Developed by Aunuli Mansfield
# Immersive Vehicles Development Toolkit
# Run python file with Python 3.8.7 or newer

import os
import shutil
import json
import re
import string

clear = lambda: os.system('cls')

recent = {"files":[]}

# Project Handling

def main():
    global recent
    if os.path.isfile("./recent"):
        recent = getJSON("./recent")
    menuObj = []
    for path in recent["files"]:
        if os.path.isdir(path):
            menuObj.append({"name":os.path.split(path)[1],"function":"creativeTabs","args":[path + "/assets"]})
    menuObj.append({"name":"New Project","function":"newProject"})
    menuObj.append({"name":"Open Project","function":"openProject"})
    print("\n" + "Main Menu")
    menu(*menuObj)

def newProject():
    path = ""
    name = ""
    confirmed = False
    while (not confirmed):
        path = getDir("\n" + "Project Directory: ")
        name = getDirName("\n" + "Project Name: ")
        confirmed = confirmSettings({"value":path,"name":"Directory"}, {"value":name,"name":"Name"})
    assets = path + "/" + name + "/assets"
    makeDir(assets)
    creativeTabs(assets)

def openProject():
    path = (getDir("\n" + "Project Directory: ") + "/assets")
    if os.path.isdir(path):
        creativeTabs(path)
    else:
        print("ERROR: Path is not an IV pack")
        main()

# Creative Tabs

def creativeTabs(path):
    global recent
    recent["files"].insert(0, os.path.split(path)[0])
    recent["files"] = removeDuplicates(recent["files"])
    makeJSON("./recent", recent)
    print("\n" + "Main Menu > " + os.path.split(os.path.split(path)[0])[1])
    tabs = readDir(path)
    menuObj = []
    for tab in tabs:
        tabDetails = getJSON(path + "/" + tab + "/packdefinition.json")
        menuObj.append({"name":tabDetails["packName"],"function":"openTab","args":[path, tab, tabDetails["packName"]]})
    menuObj.append({"name":"Add Creative Tab","function":"addCreativeTab","args":[path]})
    menuObj.append({"name":"Back","function":"main"})
    menu(*menuObj)

def addCreativeTab(path):
    print("\n" + "Main Menu > " + os.path.split(os.path.split(path)[0])[1] + " > ADD A TAB")
    name = getName("\n" + "New Tab Name: ")
    dirName = (re.sub(r'[^a-zA-Z0-9]', '', name)).lower()
    data = {"packID":dirName,"packName":name}
    makeDir(path + "/" + dirName)
    makeJSON(path + "/" + dirName + "/packdefinition.json", data)
    creativeTabs(path)

def openTab(path, tab, name):
    print("\n" + "Main Menu > " + os.path.split(os.path.split(path)[0])[1] + " > " + name)
    menu({"name":"Poles","function":"openPoles","args":[path,tab,name]},
    {"name":"Fonts","function":"openFonts","args":[path,tab,name]},
    {"name":"Delete Tab","function":"deletePath","args":[path, path + "/" + tab]},
    {"name":"Back","function":"creativeTabs","args":[path]})

# Poles

def openPoles(path, tab, name):
    print("\n" + "Main Menu > " + os.path.split(os.path.split(path)[0])[1] + " > " + name + " > Poles")
    jsonDir = path + "/" + tab + "/jsondefs/poles"
    if not os.path.isdir(jsonDir):
        makeDir(jsonDir)
    poleJSONs = readDir(jsonDir)
    menuObj = []
    for poleJSON in poleJSONs:
        pole = getJSON(jsonDir + "/" + poleJSON)["general"]["name"]
        menuObj.append({"name":pole,"function":"openPole","args":[path, tab, name, pole]})
    menuObj.append({"name":"Add A Pole","function":"addPole","args":[path, tab, name]})
    menuObj.append({"name":"Back","function":"openTab","args":[path, tab, name]})
    menu(*menuObj)

def addPole(path, tab, name):
    print("\n" + "Main Menu > " + os.path.split(os.path.split(path)[0])[1] + " > " + name + " > Poles > ADD A POLE")
    prompt = "\n" + """Pole Instructions:
Poles are OBJ models with a PNG texture file and a JSON describing how they should render in game
For this you will need an OBJ broken into sections to render and a PNG texture sheet
The JSON will be generated automatically for you"""
    print(prompt)
    if (getBool("\n" + "Do you have the OBJ and PNG ready | Y/N: ")):
        poleObj = getFile("\n" + "OBJ Source Path: ")
        polePng = getFile("\n" + "PNG Source Path: ")
        poleName = getName("\n" + "Pole Name: ")
        dirName = (re.sub(r'[^a-zA-Z0-9]', '', poleName)).lower()
        makeDir(path + "/" + tab + "/objmodels/poles")
        importFile(poleObj, path + "/" + tab + "/objmodels/poles/" + dirName + ".obj")
        makeDir(path + "/" + tab + "/textures/poles")
        importFile(poleObj, path + "/" + tab + "/textures/poles/" + dirName + ".png")
        makeDir(path + "/" + tab + "/jsondefs/poles")
        jsonOut = {}
        jsonOut["general"] = {}
        jsonOut["general"]["name"] = poleName
        jsonOut["general"]["stackSize"] = getInt("\n" + "Stack Size: ", False, [1,64])
        makeJSON(path + "/" + tab + "/jsondefs/poles/" + dirName + ".json", jsonOut)
        openPole(path, tab, name, poleName)
    else:
        openPoles(path, tab, name)

def openPole(path, tab, name, poleName):
    print("\n" + "Main Menu > " + os.path.split(os.path.split(path)[0])[1] + " > " + name + " > Poles > " + poleName)
    menu({"name":"Back","function":"openPoles","args":[path, tab, name]})

# Fonts

def openFonts(path, tab, name):
    print("\n" + "Main Menu > " + os.path.split(os.path.split(path)[0])[1] + " > " + name + " > Fonts")
    fontsDir = path + "/" + tab + "/textures/fonts"
    if not os.path.isdir(fontsDir):
        makeDir(fontsDir)
    fonts = readDir(fontsDir)
    menuObj = []
    for font in fonts:
        menuObj.append({"name":font,"function":"openFont","args":[path, tab, name, font]})
    menuObj.append({"name":"Add A Font","function":"addFont","args":[path, tab, name]})
    menuObj.append({"name":"Back","function":"openTab","args":[path, tab, name]})
    menu(*menuObj)

def openFont(path, tab, name, font):
    print("\n" + "Main Menu > " + os.path.split(os.path.split(path)[0])[1] + " > " + name + " > Fonts > " + font)
    menu({"name":"Delete Font","function":"deletePath","args":[path,path + "/" + tab + "/textures/fonts/" + font]},{"name":"Back","function":"openFonts","args":[path, tab, name]})

def addFont(path, tab, name):
    print("\n" + "Main Menu > " + os.path.split(os.path.split(path)[0])[1] + " > " + name + " > Fonts > ADD A FONT")
    prompt = "\n" + """Font Instructions:
Fonts are PNG texture sheets of sizes 128x128, 256x256, 512x512, etc
Characters are tiled across the texture sheet with 16 characters across and 16 down
Examples include https://media.discordapp.net/attachments/789711773132783636/915153427489767464/unicode_page_ff.png"""
    print(prompt)
    if (getBool("\n" + "Do you have a PNG formatted properly | Y/N: ")):
        fontDir = getFile("\n" + "Font Source Path: ")
        fontName = getDirName("\n" + "Font Name: ")
        makeDir(path + "/" + tab + "/textures/fonts/" + fontName)
        importFile(fontDir, path + "/" + tab + "/textures/fonts/" + fontName + "/unicode_page_oo.png")
    openFonts(path, tab, name)

# IO

def importFile(imageSrc, imageEnd):
    if os.path.isfile(imageSrc):
        shutil.copy2(imageSrc, imageEnd)
    else:
        print("FATAL: Failed to find image")
        main()

def makeJar(path, name):
    if (os.path.isfile(path + name)):
        os.remove(path + name)
    shutil.make_archive(name, 'zip', path)

def makeJSON(path, data):
    with open(path, "w") as file:
        json.dump(data, file, indent=4, sort_keys=True)

def makeDir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def getJSON(path):
    if (os.path.isfile(path)):
        with open(path, "r") as file:
            return json.load(file)
    else:
        print("FATAL: JSON file not found, double check that " + path + " exists")
        main()

def getName(prompt):
    return input(prompt)

def getDirName(prompt):
    name = input(prompt)
    if (name.isalnum()):
        return name
    else:
        print("ERROR: Folder name must be alphanumeric")
        return getDirName(prompt)

def getDir(prompt):
    path = input(prompt)
    if (os.path.isdir(path)):
        return path
    else:
        print("ERROR: Input is not a valid path")
        return getDir(prompt)

def getFile(prompt):
    path = input(prompt)
    if (os.path.isfile(path)):
        return path
    else:
        print("ERROR: Input is not a valid path")
        return getFile(prompt)

def getInt(prompt, allowNegative, allowedRange = []):
    isNegative = 1
    selection = input(prompt)
    if (selection[0] == "-"):
        if (allowNegative):
            selection = selection[1:]
            isNegative = -1
        else:
            print("ERROR: Input is negative")
            return getInt(prompt, allowNegative, allowedRange)
        return genInt(prompt, allowNegative)
    if (selection.isdecimal()):
        number = int(selection) * isNegative
        if (number <= allowedRange[1] and number >= allowedRange[0]):
            return number
        else:
            print("ERROR: Input is not in range")
            return getInt(prompt, allowNegative, allowedRange)
    else:
        print("ERROR: Input is not an int")
        return getInt(prompt, allowNegative, allowedRange)

def getBool(prompt):
    selection = input(prompt)
    if (selection == "Y" or selection == "y"):
        return True
    elif (selection == "N" or selection == "n"):
        return False
    else:
        print("\n" + "ERROR: Input is not Y or N")
        return getBool(prompt)

# Generic functions

def removeDuplicates(inList = []):
    retList = []
    for val in inList:
        if val not in retList:
            retList.append(val)
    return retList

def menu(*options):
    options = list(options)
    options.append({"name":"Quit","function":"quitProgram"})
    x = 0
    print("\n" + "Select One Of The Following" + "\n")
    for option in options:
        x = x + 1
        print(str(x)+": "+str(option["name"]))
    selection = getInt("\n" + "Selection: ", False, [1,x])
    args = []
    if "args" in options[selection-1]:
        args = options[selection-1]["args"]
    globals()[options[selection-1]["function"]](*args)

def confirmSettings(*args):
    for arg in args:
        if (not getBool(str("\n" + "Confirm " + arg["name"] + ' as "' + arg["value"] + '" | Y/N: '))):
            return False
    return True

def readDir(path):
    if (os.path.isdir(path)):
        return os.listdir(path)
    else:
        print("FATAL: Can not read path, please provide the console output to Aunuli")
        main()

def deletePath(path, delete):
    print("\n" + "! WARNING ! Deleting can not be undone and may break references to this object")
    if getBool("\n" + "Are you sure you want to continue | Y/N: "):
        shutil.rmtree(delete)
        creativeTabs(path)
    else:
        creativeTabs(path)

def quitProgram():
    if (not getBool("\n" + "Close the program? | Y/N: ")):
        main()

main()