#########################################
# Immersive Vehicles Development Tookit #
#########################################

# Developers: Aunuli Mansfield (Moonspire)
# Debugging help from: Lemmy
# IV help from: Laura
# Run python file with Python 3
# Developed on Python 3.8.7
version = "D-1.0.0"

###############################
# Style Guide & Documentation #
###############################

# Functions:
#
# Function names should be camel case that describe the function's tasks.
# Example: getFile() #Returns a file path
#
# Functions should also be organized into categories from largest in scope to smallest in scope.
# Example: Main Menu > Projects > Tabs > Vehicles > Signs > Decors > Fonts > IO > General
#
# Required for most objects:
# def new[Object]()             - The creation window for the object
# def generate[Object]()        - Creates the object and is called by the new[Object] function
# def open[Object] ()           - This opens the [Object]Browser window for the object
# def [Object]Browser ()        - The window for viewing and editing the object
#
# Required for some objects:
# def update[Object]            - Called by other functions to refresh the [Object]Browser content. Calls load[Object]Contents
# def load[Object]Contents      - Used to populate the [Object]Browser on objects that need to update their content to match changes
#
# Other functions for the object go after all of the above
#
# Variables:
#
# Variables should also use camel case names that describe the variable's use.
# Example: enteredValue #To store a recently entered value
#
# Windows:
#
# Windows can be made by "with dpg.window():" with the window content below.
# Example:  with dpg.window():
#               [Window Content]
#
# Windows also can be named by adding "label = [Window Name]" to the arguments for the window creation
# Example:  with dpg.window(label = "Example Window")
#               [Window Content]
#
# This software tracks windows using Universal Window IDs aka UWIDs. Each window should have a UWID.
# You can add a UWID to a window by calling "generateUWID()" and adding its result to the window with "tag = [uwid]" where [uwid] is the generated UWID.
# Example:  uwid = generateUWID()
#           with dpg.window(label = "Example Window", tag = uwid):
#               [Window Content]
#
# UWIDs are registered in the software to ensure there aren't duplicates. Due to this any instance of a window being closed or removed must deallocate that window's UWID
# This is done by adding "on_close = lambda s, a, u : removeUWID([uwid])" to the window creation where [uwid] is the window's UWID
# Example:  uwid = generateUWID()
#           with dpg.window(label = "Example Window", tag = uwid, on_close = lambda s, a, u : removeUWID(uwid)):
#               [Window Content]
#
# Text:
#
# Windows are not very useful without having content. Text is some of the simplest window content to add.
# Text can be created by calling "dpg.add_text([text])" where [text] is a string.
# Example:  uwid = generateUWID()
#           with dpg.window(label = "Example Window", tag = uwid, on_close = lambda s, a, u : removeUWID(uwid)):
#               dpg.add_text("Sample Text")
#
# Aside from displaying text you can also get text from users with text input fields.
# Text input fields are made by calling "dpg.add_input_text()" and can have default values by passing them "default_value = [text]" where [text] is a string of the default value.
# Example:  uwid = generateUWID()
#           with dpg.window(label = "Example Window", tag = uwid, on_close = lambda s, a, u : removeUWID(uwid)):
#               dpg.add_input_text(default_value = "Type Here")
#
# Text input fields should be tagged with the UWID of the window and a name. This is done so other parts of the program can reference them and read their values.
# This can be done just like adding the UWID to the window with the "tag" arguments.
# Example:  uwid = generateUWID()
#           with dpg.window(label = "Example Window", tag = uwid, on_close = lambda s, a, u : removeUWID(uwid)):
#               dpg.add_input_text(default_value = "Type Here", tag = str(uwid) + "_textField")
#
# Buttons:
#
# Buttons operate very similar to text input fields but also allow for calling functions on their interaction.
# Buttons can be created with "dpg.add_button(label = [text])" where [text] is the text to display in the button.
# Example:  uwid = generateUWID()
#           with dpg.window(label = "Example Window", tag = uwid, on_close = lambda s, a, u : removeUWID(uwid)):
#               dpg.add_button(label = "Click Me!")
#
# The main purpose of buttons are to call functions on clicking them.
# This can be done by adding "callback = lambda s, a, u : [function]" where [function] is your function call.
# Example:  uwid = generateUWID()
#           with dpg.window(label = "Example Window", tag = uwid, on_close = lambda s, a, u : removeUWID(uwid)):
#               dpg.add_button(label = "Click Me!", callback = lambda s, a, u : myFunction())
#
# Drop Down Selections:
#
# Drop Down Selections or Combos are menus that drop down and provide a list that the user can select one option from.
# They can be created with "dpg.add_combo()" and populated with options from any list by passing the list as an argument.
# Example:  uwid = generateUWID()
#           with dpg.window(label = "Example Window", tag = uwid, on_close = lambda s, a, u : removeUWID(uwid)):
#               options = ["1","2","3"]
#               dpg.add_combo(options)
#
# Combos also should have a tag with the UWID and an identifier just like text input fields so other functions can read their data.
# Example:  uwid = generateUWID()
#           with dpg.window(label = "Example Window", tag = uwid, on_close = lambda s, a, u : removeUWID(uwid)):
#               options = ["1","2","3"]
#               dpg.add_combo(options, tag = str(uwid) + "_combo"
#
# File Browser:
#
# To get a file path, make a button and make the callback "callback = lambda s, a, u : fileBrowser([name],[param],[function],[files])" where [name] is the title of the window,
# [function] is the function to call after file selected, [param] is the second argument for the function, and [files] are the allowed file types.
# Example:  uwid = generateUWID()
#           with dpg.window(label = "Example Window", tag = uwid, on_close = lambda s, a, u : removeUWID(uwid)):
#               buttonTag = str(uwid) + "_button"
#               dpg.add_button(label = "Get File", callback = lambda s, a, u : fileBrowser("Get File", buttonTag, "updateButton", ["Any{.*}"]), tag = buttonTag)
#
# Notes:
#
# The Main Menu always has a UWID of 0, it is the only window with a hard coded UWID and the only window that can not exist multiple times. Never call "main()" in any function!
#
# Documentation on DearPyGui can be found here: https://dearpygui.readthedocs.io/en/latest/

###########
# Imports #
###########

import sys
import subprocess
import os
import shutil
import json
import re
import string
import webbrowser
import pathlib
import random
import ctypes
import numpy as np
from PIL import Image

ctypes.windll.shcore.SetProcessDpiAwareness(2)

####################################
# Get OS and download dependancies #
####################################

from sys import platform
if platform == "linux" or platform == "linux2":
    if os.geteuid()==0:
        subprocess.check_call(['apt-get', 'install', '-y', 'python3-pip'])
    else:
        sys.exit("ERROR: IVDT does not have permission to download dependancies, try 'sudo python3 IVDT.py'")
elif platform == "darwin":
    sys.exit("ERROR: IVDT can't download dependancies on Mac OS, please use Linux or Windows")
elif platform == "win32":
    subprocess.check_call([sys.executable, '-m', 'ensurepip', '--default-pip'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'dearpygui'])

##################
# Program Memory #
##################

programData = {"uwids":[],"recent":[]}

#############################
# Import Downloaded Content #
#############################

import dearpygui.dearpygui as dpg
from dearpygui.demo import show_demo

#############
# Main Menu #
#############

def main():
    uwid = 0
    global programData
    global version
    programData["uwids"].append(uwid)
    with dpg.window(label = "Main Menu", width = 400, height = 800, pos = (0, 0)):
        if "D-" in version:
            with dpg.menu_bar():
                with dpg.menu(label = "Experimental"):
                    dpg.add_menu_item(label = "Texture Maker", callback = lambda s, a, u : textureEditor())
                    dpg.add_menu_item(label = "DearPyGui Demo", callback = show_demo)
        dpg.add_text("Immersive Vehicles Development Toolkit - " + version)
        recent = readJSON("recent")
        if "JSON_ERR" in recent:
            print("No Recent Files Found, Continuing Without Them")
        else:
            programData["recent"] = recent["files"]
        for path in programData["recent"]:
            if os.path.isdir(path + "/assets"):
                dpg.add_button(label = os.path.split(path)[1], callback = projectBrowser, user_data = path)
        dpg.add_button(label = "New Project", callback = newProject)
        dpg.add_button(label = "Open Project", callback = lambda s, a, u : fileBrowser("Select A Project",uwid,"openProject",["Archive (.jar .zip){.jar,.zip}","Folder{.}"]))

#####################
# Project Managment #
#####################

def newProject():
    uwid = generateUWID()
    with dpg.window(label = "Make A IV Pack", tag = uwid, on_close = lambda s, a, u : removeUWID(uwid), width = 800, height = 200):
        buttonTag = str(uwid) + "_packLocation"
        with dpg.group():
            dpg.add_text("IV packs contain an assets folder with everything inside of it")
        with dpg.group(horizontal = True):
            dpg.add_text("Pack Name:")
            dpg.add_input_text(tag = str(uwid) + "_name", default_value = "My Pack", width = 600)
        with dpg.group(horizontal = True):
            dpg.add_text("Pack Location:")
            dpg.add_button(label = "File", tag = buttonTag, callback = lambda s, a, u : fileBrowser("Select A Location To Make Project", buttonTag, "updateButton", ["Folder{.}"]), width = 600)
        dpg.add_button(label = "Make Project", callback = lambda s, a, u : generateProject(dpg.get_value(str(uwid) + "_name"), dpg.get_item_label(buttonTag), uwid))

def generateProject(name, path, uwid):
    readDir(path + "/" + name + "/assets", True)
    openProject(path + "/" + name)
    deleteItem(uwid)
    removeUWID(uwid)

def openProject(file, unused = 0):
    file = os.path.abspath(file)
    if os.path.isfile(file):
        extract_dir = "./projects/" + os.path.split(file)[1]
        readDir(extract_dir, True)
        shutil.unpack_archive(file, extract_dir, "zip")
        file = extract_dir
    projectBrowser(0, "", file)

def projectBrowser(sender, app_data, root):
    if root in programData["recent"]:
        programData["recent"].remove(root)
    programData["recent"].insert(0, root)
    makeJSON("./recent", {"files":programData["recent"]})
    projectName = os.path.split(root)[1]
    uwid = generateUWID()
    with dpg.window(label = projectName, width = 400, height = 800, pos = (100, 100), tag = uwid, on_close = removeUWID, user_data = uwid):
        with dpg.menu_bar():
            with dpg.menu(label = "File"):
                dpg.add_menu_item(label = "Export Jar", callback = lambda s, a, u : fileBrowser("Export Project",root,"makeJar",["Archive (.jar .zip){.jar,.zip}"]))
            with dpg.menu(label = "Create"):
                dpg.add_menu_item(label = "Creative Tab", callback = lambda s, a, u : makeTab(root, uwid))
                dpg.add_menu_item(label = "Font", callback = lambda s, a, u : makeFont(root, uwid))
                dpg.add_menu_item(label = "Pole")
                dpg.add_menu_item(label = "Sign")
                dpg.add_menu_item(label = "From Clipboard")
        loadProjectContents(uwid, root)

def updateProject(uwid, root, rmUWID = 0):
    if (rmUWID != 0):
        removeUWID(rmUWID)
    deleteItem(str(uwid) + "_contents")
    loadProjectContents(uwid, root)

def loadProjectContents(uwid, root):
    assets = root + "/assets"
    with dpg.group(tag = str(uwid) + "_contents", parent = uwid):
        tabsList = readDir(assets, True)
        print(tabsList)
        for tab in tabsList:
            tab = assets + "/" + tab
            tabJSON = readJSON(tab + "/packdefinition.json")
            tabName = tabJSON["packName"]
            with dpg.collapsing_header(label = tabName):
                with dpg.tree_node(label = "Fonts"):
                    fonts = tab + "/textures/fonts"
                    fontsList = readDir(fonts)
                    for font in fontsList:
                        dpg.add_button(label = font, callback = lambda s, a, u : openFont(font, uwid, root, tab))

#################
# Creative Tabs #
#################

def makeTab(root, projectUWID):
    uwid = generateUWID()
    projectName = os.path.split(root)[1]
    assets = root + "/assets"
    with dpg.window(label = "Make A Font", tag = uwid, on_close = lambda s, a, u : updateProject(projectUWID, root, uwid), width = 800, height = 200):
        with dpg.group(horizontal = True):
            dpg.add_text("IV creative tabs contain all of the IV items, models, and files.")
        with dpg.group(horizontal = True):
            dpg.add_text("Tab Name:")
            dpg.add_input_text(label = "", tag = str(uwid) + "_name", default_value = "My Tab", width = 600)
        dpg.add_button(label = "Make Tab", callback = lambda s, a, u : generateTab(dpg.get_value(str(uwid) + "_name"), uwid, projectUWID, root))

def generateTab(name, uwid, projectUWID, root):
    tabDir = (re.sub(r'[^a-zA-Z0-9]', '', name)).lower()
    readDir(root + "/assets/" + tabDir, True)
    packDef = {}
    packDef["packID"] = tabDir
    packDef["packName"] = name
    makeJSON(root + "/assets/" + tabDir + "/packdefinition.json", packDef)
    deleteItem(uwid)
    updateProject(projectUWID, root, uwid)

# openTab and tabBrowser are handled by the projectBrowser

#########
# Fonts #
#########

def makeFont(root, projectUWID):
    uwid = generateUWID()
    projectName = os.path.split(root)[1]
    assets = root + "/assets"
    with dpg.window(label = "Make A Font", tag = uwid, on_close = lambda s, a, u : updateProject(projectUWID, root, uwid), width = 800, height = 200):
        buttonTag = str(uwid) + "_fontSrc"
        with dpg.group():
            dpg.add_text("IV fonts must be formatted in a 128x128, 256x256, 512x512, etc resolution PNG with 16 characters vertically and horrizontally.")
            hyperlink("Example IV font PNG", "https://images-ext-1.discordapp.net/external/R0JdwE7QbBZGccgg3SY3gXDPVGexLbLw8KmUTMJ14dE/https/media.discordapp.net/attachments/789711773132783636/915153427489767464/unicode_page_ff.png")
        with dpg.group(horizontal = True):
            dpg.add_text("Font Name:")
            dpg.add_input_text(label = "", tag = str(uwid) + "_name", default_value = "myfont", width = 600)
        with dpg.group(horizontal = True):
            dpg.add_text("Creative Tab: ")
            tabsList = readDir(assets, True)
            tabs = {"names":[],"dirs":{}}
            for tab in tabsList:
                tab = assets + "/" + tab
                tabJSON = readJSON(tab + "/packdefinition.json")
                tabName = tabJSON["packName"]
                tabs["names"].append(tabName)
                tabs["dirs"][tabName] = tab
            dpg.add_combo(tabs["names"], tag = str(uwid) + "_combo", width = 600)
        with dpg.group(horizontal = True):
            dpg.add_text("PNG Source:")
            dpg.add_button(label = "File", tag = buttonTag, callback = lambda s, a, u : fileBrowser("Select A Project", buttonTag, "updateButton", ["Image (.png){.png}"]), width = 600)
        dpg.add_button(label = "Make Font", callback = lambda s, a, u : generateFont(tabs["dirs"][dpg.get_value(str(uwid) + "_combo")], dpg.get_value(str(uwid) + "_name"), dpg.get_item_label(buttonTag), uwid, projectUWID, root))

def generateFont(tab, name, src, uwid, projectUWID, root):
    fontDir = tab + "/textures/fonts/" + name
    print(readDir(fontDir, True))
    importFile(src, fontDir + "/unicode_page_00")
    deleteItem(uwid)
    updateProject(projectUWID, root, uwid)

def openFont(fontName, projectUWID, root, tab):
    fontBrowser(fontName, projectUWID, root, tab)

def fontBrowser(fontName, projectUWID, root, tab):
    font = tab + "/textures/fonts/" + fontName
    uwid = generateUWID()
    with dpg.window(label = fontName, tag = uwid, on_close = lambda s, a, u : updateProject(projectUWID, root, uwid), width = 400, height = 400):
        with dpg.menu_bar():
            with dpg.menu(label = "File"):
                dpg.add_menu_item(label = "Copy Font To Clipboard")
                dpg.add_menu_item(label = "Duplicate Font")
                dpg.add_menu_item(label = "Delete Font")
            with dpg.menu(label = "Edit"):
                dpg.add_menu_item(label = "Change Name")
                dpg.add_menu_item(label = "Change Texture")
        dpg.add_text("Font Name: " + fontName)
        fontSrc = os.path.abspath(font + "/unicode_page_00.png")
        print(fontSrc)
        dpg.add_text("Font Sheet:")
        width, height, channels, data = dpg.load_image(fontSrc)
        with dpg.texture_registry():
            texture_id = dpg.add_static_texture(width, height, data)
        with dpg.drawlist(width=300, height=300):
            dpg.draw_image(texture_id, (0, 0), (300, 300), uv_min=(0, 0), uv_max=(1, 1))

##################
# Texture Editor #
##################

def textureEditor(xRes = 128, yRes = 128):
    with dpg.window(label = "Texture Maker", width = 1020, height = 820):
        global programData
        programData["lastMousePos"] = [-1, -1]
        with dpg.menu_bar():
            with dpg.menu(label = "File"):
                dpg.add_menu_item(label = "Save Image")
        with dpg.group():
            dpg.add_text("Primary Color")
            dpg.add_color_picker((0, 0, 0, 255), no_side_preview=True, alpha_bar=True, width=200, callback = colorChanged, tag = "colorPicker")
            dpg.add_button(label = "Swap Primary & Secondary", callback = lambda s, a, u: swapColors())
            dpg.add_text("Secondary Color")
            dpg.add_color_picker((0, 0, 0, 0), no_side_preview=True, alpha_bar=True, width=200, callback = colorChanged, tag = "colorPicker2")
            dpg.add_drag_int(label="Brush Size", default_value = 1, width = 100, tag = "texEdit_brushSize")
        with dpg.group(tag = "textureViewPort"):
            channels = 4
            data = imageScaler(createTextureData(xRes, yRes), [xRes, yRes], [800, 800])
            with dpg.texture_registry():
                dpg.add_static_texture(800, 800, createTransparency(), tag = "transparency")
                dpg.add_dynamic_texture(800, 800, data, tag = "testTexture")
            with dpg.group(tag = "imageFrame"):
                with dpg.drawlist(width=800, height=800):
                    dpg.draw_image("transparency", (0, 0), (800, 800), uv_min=(0, 0), uv_max=(1, 1))
                    dpg.draw_image("testTexture", (0, 0), (800, 800), uv_min=(0, 0), uv_max=(1, 1))
                dpg.set_item_pos("imageFrame", (220, 19))
                print(dpg.get_item_pos("textureViewPort"))
                with dpg.item_handler_registry(tag = "texEdit"):
                    dpg.add_item_hover_handler(callback = lambda s, a, u : textureMouse(data, [xRes, yRes]))
                dpg.bind_item_handler_registry("imageFrame", "texEdit")

def swapColors():
    primary = dpg.get_value("colorPicker")
    secondary = dpg.get_value("colorPicker2")
    dpg.set_value("colorPicker", secondary)
    dpg.set_value("colorPicker2", primary)

def colorChanged(s, a, u):
    print(a)

def createTransparency(resolution = [800, 800]):
    textureData = []
    for i in range(51*51):
        if (i % 2) == 0:
            textureData.append(0.5)
            textureData.append(0.5)
            textureData.append(0.5)
        else:
            textureData.append(0.6)
            textureData.append(0.6)
            textureData.append(0.6)
        textureData.append(1)
    return imageScaler(textureData, [51, 51], resolution)

def textureMouse(data, resolution = [128, 128]):
    if dpg.is_mouse_button_down(0):
        textureDraw(data, "L", resolution)
    elif dpg.is_mouse_button_down(1):
        textureDraw(data, "R", resolution)
    else:
        global programData
        programData["lastMousePos"] = [-1, -1]

def textureDraw(data, button = "L", resolution = [128, 128]):
    global programData
    lastPos = programData["lastMousePos"]
    pos = dpg.get_mouse_pos()
    pos = [int(pos[0]-220), int(pos[1])]
    programData["lastMousePos"] = pos
    color = []
    colorSelected = "colorPicker"
    if button == "R":
        colorSelected = "colorPicker2"
    for channel in dpg.get_value(colorSelected):
        color.append(channel/255)
    if lastPos != [-1, -1]:
        areaX = range(lastPos[0], pos[0])
        if pos[0] <= lastPos[0]:
            areaX = range(pos[0], lastPos[0])
        areaY = range(lastPos[1], pos[1])
        if pos[1] <= lastPos[1]:
            areaY = range(pos[1], lastPos[1])
        slope = 0
        if lastPos[0] != pos[0]:
            slope = float(lastPos[1] - pos[1]) / float(lastPos[0] - pos[0])
        print(slope, "Pos:", pos, "Last Pos:", lastPos)
        for x in areaX:
            y = int((x * slope) - (lastPos[0] * slope) + lastPos[1])
            data = drawWithBrush([x, y], data, color, resolution, dpg.get_value("texEdit_brushSize"))
        for y in areaY:
            x = pos[0]
            if slope != 0:
                x = int((y + (lastPos[0] * slope) - lastPos[1]) / slope)
            data = drawWithBrush([x, y], data, color, resolution, dpg.get_value("texEdit_brushSize"))
    data = drawWithBrush(pos, data, color, resolution, dpg.get_value("texEdit_brushSize"))
    dpg.set_value("testTexture", data)

def getPixel(pos, resolution, data):
    r = ((pos[1]*resolution[1])+pos[0])*4
    g = r + 1
    b = g + 1
    a = b + 1
    return [data[r], data[g], data[b], data[a]]

def drawWithBrush(pos, data, rgba = [0, 0, 0, 0], resolution = [128, 128], brushSize = 1):
    scale = [800 / resolution[0], 800 / resolution[1]]
    fillRange = [
        [
            int((int(pos[0] / scale[0]) - brushSize + 1) * scale[0]),
            int((int(pos[0] / scale[0]) + brushSize) * scale[0])
        ],
        [
            int((int(pos[1] / scale[1]) - brushSize + 1) * scale[1]),
            int((int(pos[1] / scale[1]) + brushSize) * scale[1])
        ]
    ]
    for x in range(*fillRange[0]):
        for y in range(*fillRange[1]):
            data = editPixel([x, y], [800, 800], data, rgba)
    return data

def editPixel(pos, resolution, data, rgba = [0,0,0,0]):
    r = ((pos[1]*resolution[1])+pos[0])*4
    g = r + 1
    b = g + 1
    a = b + 1
    data[r] = rgba[0]
    data[g] = rgba[1]
    data[b] = rgba[2]
    data[a] = rgba[3]
    return data

def createTextureData(xRes = 128, yRes = 128):
    textureData = []
    for i in range(xRes*yRes):
        textureData.append(0)
        textureData.append(0)
        textureData.append(0)
        textureData.append(0)
    return textureData

#########
# Input #
#########

def fileBrowser(name, uwid, function, types = []):
    with dpg.file_dialog(label = name, callback = lambda s, a, u : globals()[function](a["file_path_name"], uwid)):
        for fileType in types:
            dpg.add_file_extension(fileType, color=(255, 255, 255, 255))

def readDir(path, makeDir = False):
    if (os.path.isdir(path)):
        return os.listdir(path)
    elif makeDir:
        print(os.makedirs(path))
        return os.listdir(path)
    else:
        return []

def readJSON(path):
    if (os.path.isfile(path)):
        with open(path, "r") as file:
            return json.load(file)
    else:
        return {"JSON_ERR":"No File"}

def importFile(imageSrc, imageEnd):
    if os.path.isfile(imageSrc):
        shutil.copy2(imageSrc, imageEnd)

##########
# Output #
##########

def makeJSON(path, data):
    with open(path, "w") as file:
        json.dump(data, file, indent=4, sort_keys=True)

def makeJar(path, root):
    name = os.path.split(path)[1]
    path = os.path.split(path)[0]
    print(root, path)
    zip_name = shutil.make_archive(path, "zip", root)
    os.rename(zip_name, name)

###########
# Generic #
###########

def imageScaler(data, srcRes, retRes):
    temp = []
    for x in range(srcRes[0]*srcRes[1]):
        r = x * 4
        g = r + 1
        b = g + 1
        a = b + 1
        temp.append((int(data[r]*255), int(data[g]*255), int(data[b]*255), int(data[a]*255)))
    im = Image.new("RGBA", srcRes)
    im.putdata(temp)
    im = im.resize(retRes, resample = Image.NEAREST)
    temp2 = list(im.getdata())
    retImg = []
    for x in temp2:
        retImg.append(float(x[0])/255)
        retImg.append(float(x[1])/255)
        retImg.append(float(x[2])/255)
        retImg.append(float(x[3])/255)
    print(len(data), len(retImg))
    return retImg

def hyperlink(text, address):
    b = dpg.add_button(label=text, callback=lambda:webbrowser.open(address))
    dpg.bind_item_theme(b, "__demo_hyperlinkTheme")

def generateUWID():
    uwid = random.randrange(0, 999, 1)
    global programData
    if uwid in programData["uwids"]:
        return generateUWID()
    else:
        programData["uwids"].append(uwid)
        print(programData["uwids"])
        return uwid

def removeUWID(uwid):
    try:
        while True:
            programData["uwids"].remove(uwid)
    except ValueError:
        pass
    print(programData["uwids"])

def updateButton(file, uwid):
    dpg.set_item_label(uwid, file)

def deleteItem(uwid):
    dpg.delete_item(uwid)

#########
# Debug #
#########

def printData(s, a, u):
    print(s)
    print(a)
    print(u)

##################################
# Create Window & Open Main Menu #
##################################

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

dpg.set_viewport_large_icon("ivdt_icon.ico")

main()

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()