#Program: cloudfalreGui :: Program to forward localhost http port on internet with a beautiful user interface.
#Author: Suman Kumar ~BHUTUU
#Date: 19-02-2023 (initiation)
#Licence: --(to be implemented)

#<<<------Import section------>>>

import os, re, time, subprocess, requests
from PIL import Image, ImageTk
from tkinter import *
import threading

#<<<-----Definig Functions----->>>
def localCmd(command):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out.decode(), err
def cloudfare(lhost,lport):
    if os.name == 'nt':
        run = threading.Thread(target=localCmd("cloudflared -url "))
        return run[0]
print(cloudfare("127.0.0.1", 8080))