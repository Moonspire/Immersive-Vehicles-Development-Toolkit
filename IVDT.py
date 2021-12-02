# Developed by Aunuli Mansfield
# Immersive Vehicles Development Toolkit
# Run python file with Python 3.8.7 or newer

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

programData = {"uuids":[],"recent":[]}

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'dearpygui']) # Download dearPyGui

def hyperlink(text, address):
    b = dpg.add_button(label=text, callback=lambda:webbrowser.open(address))
    dpg.bind_item_theme(b, "__demo_hyperlinkTheme")

def readDir(path, makeDir = False):
    if (os.path.isdir(path)):
        return os.listdir(path)
    elif makeDir:
        os.makedirs(path)
        return os.listdir(path)
    else:
        return []
    

def readJSON(path):
    if (os.path.isfile(path)):
        with open(path, "r") as file:
            return json.load(file)
    else:
        with dpg.window(label = "ERROR"):
            dpg.add_text("Could not find a JSON file at " + path)

import dearpygui.dearpygui as dpg
from dearpygui.demo import show_demo

def generateUUID():
    uuid = random.randrange(0, 999, 1)
    global programData
    if uuid in programData["uuids"]:
        return generateUUID()
    else:
        programData["uuids"].append(uuid)
        print(programData["uuids"])
        return uuid

def removeUUID(uuid):
    try:
        while True:
            programData["uuids"].remove(uuid)
    except ValueError:
        pass
    print(programData["uuids"])

def generateProject(name, path, uuid):
    readDir(path + "/" + name + "/assets", True)
    openProject(path + "/" + name)

def newProject():
    uuid = generateUUID()
    with dpg.window(label = "Make A IV Pack", tag = uuid, on_close = lambda s, a, u : updateWorkspace(projectUUID, root, uuid), width = 800, height = 200):
        with dpg.group():
            dpg.add_text("IV packs contain an assets folder with everything inside of it")
        with dpg.group(horizontal = True):
            dpg.add_text("Pack Name:")
            dpg.add_input_text(label = "", tag = str(uuid) + "_name", default_value = "My Pack", width = 600)
        with dpg.group(horizontal = True):
            dpg.add_text("Pack Location:")
            dpg.add_button(label = "File", tag = str(uuid) + "_updatable", callback = fileBrowser, user_data = {"title":"Select A Location To Make Project","fileTypes":["Folder{.}"],"uuid":uuid,"function":"updateButton"}, width = 600)
        dpg.add_button(label = "Make Project", callback = lambda s, a, u : generateProject(dpg.get_value(str(uuid) + "_name"), dpg.get_item_label(str(uuid) + "_updatable"), uuid))

def makeJSON(path, data):
    with open(path, "w") as file:
        json.dump(data, file, indent=4, sort_keys=True)

def openProject(file, unused = 0):
    file = os.path.abspath(file)
    projectBrowser(0, "", file)

def fileBrowser(sender, app_data, fileData):
    with dpg.file_dialog(label = fileData["title"], callback = lambda s, a, u : globals()[fileData["function"]](a["file_path_name"], fileData["uuid"])):
        for fileType in fileData["fileTypes"]:
            dpg.add_file_extension(fileType, color=(255, 255, 255, 255))

def updateWorkspace(uuid, root, rmUUID = 0):
    if (rmUUID != 0):
        removeUUID(rmUUID)
    dpg.delete_item(str(uuid) + "_contents")
    loadProjectContents(uuid, root)

def updateButton(file, uuid):
    dpg.set_item_label(str(uuid) + "_updatable", file)

def importFile(imageSrc, imageEnd):
    if os.path.isfile(imageSrc):
        shutil.copy2(imageSrc, imageEnd)

def generateFont(tab, name, src, uuid, projectUUID, root):
    fontDir = tab + "/textures/fonts/" + name
    readDir(fontDir, True)
    importFile(src, fontDir + "/unicode_page_00")
    dpg.delete_item(uuid)
    dpg.delete_item(uuid)
    updateWorkspace(projectUUID, root, uuid)

def makeFont(root, projectUUID):
    uuid = generateUUID()
    projectName = os.path.split(root)[1]
    assets = root + "/assets"
    with dpg.window(label = "Make A Font", tag = uuid, on_close = lambda s, a, u : updateWorkspace(projectUUID, root, uuid), width = 800, height = 200):
        with dpg.group():
            dpg.add_text("IV fonts must be formatted in a 128x128, 256x256, 512x512, etc resolution PNG with 16 characters vertically and horrizontally.")
            hyperlink("Example IV font PNG", "https://images-ext-1.discordapp.net/external/R0JdwE7QbBZGccgg3SY3gXDPVGexLbLw8KmUTMJ14dE/https/media.discordapp.net/attachments/789711773132783636/915153427489767464/unicode_page_ff.png")
        with dpg.group(horizontal = True):
            dpg.add_text("Font Name:")
            dpg.add_input_text(label = "", tag = str(uuid) + "_name", default_value = "myfont", width = 600)
        with dpg.group(horizontal = True):
            dpg.add_text("Creative Tab: ")
            tabsList = readDir(assets, True)
            tabs = []
            for tab in tabsList:
                tab = assets + "/" + tab
                tabJSON = readJSON(tab + "/packdefinition.json")
                tabName = tabJSON["packName"]
                tabs.append(tabName)
            dpg.add_combo(tabs, label = "", width = 600)
        with dpg.group(horizontal = True):
            dpg.add_text("PNG Source:")
            dpg.add_button(label = "File", tag = str(uuid) + "_updatable", callback = fileBrowser, user_data = {"title":"Select A Project","fileTypes":["Image (.png){.png}"],"uuid":uuid,"function":"updateButton"}, width = 600)
        dpg.add_button(label = "Make Font", callback = lambda s, a, u : generateFont(tab, dpg.get_value(str(uuid) + "_name"), dpg.get_item_label(str(uuid) + "_updatable"), uuid, projectUUID, root))

def generateTab(name, uuid, projectUUID, root):
    tabDir = (re.sub(r'[^a-zA-Z0-9]', '', name)).lower()
    readDir(root + "/assets/" + tabDir, True)
    packDef = {}
    packDef["packID"] = tabDir
    packDef["packName"] = name
    makeJSON(root + "/assets/" + tabDir + "/packdefinition.json", packDef)
    dpg.delete_item(uuid)
    dpg.delete_item(uuid)
    updateWorkspace(projectUUID, root, uuid)

def makeTab(root, projectUUID):
    uuid = generateUUID()
    projectName = os.path.split(root)[1]
    assets = root + "/assets"
    with dpg.window(label = "Make A Font", tag = uuid, on_close = lambda s, a, u : updateWorkspace(projectUUID, root, uuid), width = 800, height = 200):
        with dpg.group(horizontal = True):
            dpg.add_text("IV creative tabs contain all of the IV items, models, and files.")
        with dpg.group(horizontal = True):
            dpg.add_text("Tab Name:")
            dpg.add_input_text(label = "", tag = str(uuid) + "_name", default_value = "My Tab", width = 600)
        dpg.add_button(label = "Make Tab", callback = lambda s, a, u : generateTab(dpg.get_value(str(uuid) + "_name"), uuid, projectUUID, root))

def projectBrowser(sender, app_data, root):
    if root in programData["recent"]:
        programData["recent"].remove(root)
    programData["recent"].insert(0, root)
    makeJSON("./recent", {"files":programData["recent"]})
    projectName = os.path.split(root)[1]
    uuid = generateUUID()
    with dpg.window(label = projectName, width = 400, height = 800, pos = (100, 100), tag = uuid, on_close = removeUUID, user_data = uuid):
        with dpg.menu_bar():
            with dpg.menu(label = "Create"):
                dpg.add_menu_item(label = "Creative Tab", callback = lambda s, a, u : makeTab(root, uuid))
                dpg.add_menu_item(label = "Font", callback = lambda s, a, u : makeFont(root, uuid))
                dpg.add_menu_item(label = "Pole")
                dpg.add_menu_item(label = "Sign")
                dpg.add_menu_item(label = "From Clipboard")
        loadProjectContents(uuid, root)

def loadProjectContents(uuid, root):
    assets = root + "/assets"
    with dpg.group(tag = str(uuid) + "_contents", parent = uuid):
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
                        dpg.add_button(label = font)

def main():
    uuid = 0
    global programData
    programData["uuids"].append(uuid)
    with dpg.window(label = "Main Menu", width = 400, height = 800, pos = (0, 0)):
        dpg.add_text("Immersive Vehicles Development Toolkit")
        recent = readJSON("recent")
        programData["recent"] = recent["files"]
        for path in recent["files"]:
            if os.path.isdir(path + "/assets"):
                dpg.add_button(label = os.path.split(path)[1], callback = projectBrowser, user_data = path)
        dpg.add_button(label = "New Project", callback = newProject)
        dpg.add_button(label = "Open Project", callback = fileBrowser, user_data = {"title":"Select A Project","fileTypes":["Archive (.jar .zip){.jar,.zip}","Folder{.}"],"uuid":uuid,"function":"openProject"})

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

#show_demo()

main()

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()