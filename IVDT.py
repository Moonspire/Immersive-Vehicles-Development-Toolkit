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

makeFiles = {}

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'dearpygui']) # Download dearPyGui

def hyperlink(text, address):
    b = dpg.add_button(label=text, callback=lambda:webbrowser.open(address))
    dpg.bind_item_theme(b, "__demo_hyperlinkTheme")

def readDir(path):
    if not (os.path.isdir(path)):
        os.makedirs(path)
    return os.listdir(path)

def readJSON(path):
    if (os.path.isfile(path)):
        with open(path, "r") as file:
            return json.load(file)
    else:
        with dpg.window(label = "ERROR"):
            dpg.add_text("Could not find a JSON file at " + path)

import dearpygui.dearpygui as dpg
from dearpygui.demo import show_demo

def newProject():
    print("Save Clicked")

def logData(sender, app_data, source = []):
    global makeFiles
    if source[0] not in makeFiles.keys():
        makeFiles[source[0]] = {}
    if source[1] not in makeFiles[source[0]].keys():
        makeFiles[source[0]][source[1]] = {}
    makeFiles[source[0]][source[1]][source[2]] = app_data
    print(makeFiles[source[0]][source[1]][source[2]])

def makeFont(sender, app_data, projectName):
    with dpg.window(label = "Make A Font"):
        with dpg.group(horizontal=True):
            dpg.add_text("IV fonts must be formatted in a 128x128, 256x256, 512x512, etc resolution PNG with 16 characters vertically and horrizontally.")
            hyperlink("Example IV font PNG", "https://images-ext-1.discordapp.net/external/R0JdwE7QbBZGccgg3SY3gXDPVGexLbLw8KmUTMJ14dE/https/media.discordapp.net/attachments/789711773132783636/915153427489767464/unicode_page_ff.png")
        with dpg.group(horizontal=True):
            dpg.add_text("Font Name:")
            dpg.add_input_text(label = "", default_value = "myfont", callback = logData, user_data = [projectName, "makeFont", "name"])
        with dpg.group(horizontal=True):
            dpg.add_text("PNG Source:")
            dpg.add_button(label = "File")

def projectBrowser(sender, app_data, root):
    projectName = os.path.split(root)[1]
    with dpg.window(label = projectName):
        with dpg.menu_bar():
            with dpg.menu(label = "Create"):
                dpg.add_menu_item(label = "Font", callback = makeFont, user_data = projectName)
                dpg.add_menu_item(label = "Pole")
                dpg.add_menu_item(label = "Sign")
                dpg.add_menu_item(label = "From Clipboard")
        assets = root + "/assets"
        tabsList = readDir(assets)
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

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

with dpg.window(label = "Main Menu"):
    dpg.add_text("Immersive Vehicles Development Toolkit")
    recent = readJSON("recent")
    for path in recent["files"]:
        if os.path.isdir(path + "/assets"):
            dpg.add_button(label = os.path.split(path)[1], callback = projectBrowser, user_data = path)
    dpg.add_button(label = "New Project", callback = newProject)
    dpg.add_button(label = "Open Project", callback = newProject)
    #dpg.add_input_text(label="string")
    #dpg.add_slider_float(label="float")

show_demo()

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()