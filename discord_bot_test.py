def printRed(txt):
    print("\033[0;31m{}\033[00m".format(txt))

try:
    import pyautogui as pag
except Exception as e:
    print(e)
    print("\033[0;31mThere is an import error here! This is most likely caused by an incorrect installation process. Ensure that you have done the 'pip3 install...steps'\033[00m")
    quit()
import time, os, ctypes, tty
import tkinter
import tkinter as tk
from tkinter import ttk
import backpack, reset, loadsettings, move,update,updateexperiment
import multiprocessing, webbrowser, imagesearch, sys, discord, subprocess
from webhook import webhook
global savedata
global setdat
from tkinter import messagebox
import numpy as np
import asyncio
from logpy import log
import logging
import pynput
from pynput.keyboard import Key
from pynput.mouse import Button

try:
    import matplotlib.pyplot as plt
except Exception as e:
    print("\033[0;31mThere is an import error here! Enter pip3 install matplotlib in terminal'\033[00m")
from PIL import ImageGrab, Image

try:
    import cv2
except Exception as e:
    print(e)
    print("\033[0;31mThere is a import error here! Check out ImportError: dlopen in #common-fixes in the discord server or 'bugs and fixes' section in the github\033[00m")
    quit()


from ocrpy import imToString,customOCR
import sv_ttk
import math
import ast
import calibrate_hive
from datetime import datetime
import pyscreeze

setdat = loadsettings.load()
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!b'):
        args = message.content.split(" ")[1:]
        cmd = args[0].lower()
        if cmd == "rejoin":
            await message.channel.send("Now attempting to rejoin")
            await asyncRejoin()
        elif cmd == "screenshot":
            await message.channel.send("Sending a screenshot via webhook")
            webhook("User Requested: Screenshot","","light blue",1)
        elif cmd == "report":
            await message.channel.send("Sending Hourly Report")
            hourlyReport(0)
            
            #honeyHist = []
            #savehoney_history(honeyHist)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
client.run(setdat['discord_bot_token'], log_handler=handler)
