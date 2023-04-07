#Program: cloudfalreGui :: Program to forward localhost http port on internet with a beautiful user interface.
#Author: Suman Kumar ~BHUTUU
#Date: 19-02-2023 (initiation)
#Licence: --(to be implemented)
#<<<------Import section------>>>
import os, re, time, subprocess, platform, base64,sys
from tkinter import *
from tkinter import messagebox
import threading
import ImageRequired
try:
    from PIL import Image, ImageTk
except ImportError:
    os.system('pip install pillow')
    from PIL import Image, ImageTk
try:
    import requests
except ImportError:
    os.system('pip install requests')
    import requests
#<<<-----Internal variables------>>>
OS = str(os.name)
if OS.upper() == 'NT':
    architecture = platform.machine()
    realName = 'windows'
    downloadFolder = os.path.expanduser('~')+'/Downloads'
    programDir = 'C:/Program Files'
    gitDir = programDir+'/Git/usr/bin'
    cloudflare_log = os.path.expanduser('~')+'/AppData/Local/Temp/cloudflare.log'
elif OS.upper() == 'GNU/LINUX':
    architecture = platform.machine()
    realName = "GNU/Linux"
    downloadFolder = os.path.expanduser('~')+'/Downloads'
    programDir = '/usr/bin'
    gitDir = programDir
    cloudflare_log = '/usr/tmp/cloudflare.log'
else:
    with open('cloudflare.log', 'w') as file:
        file.write("sorry but this cloudflare user interface doesn't supports your operating system!")
        file.close()
    SystemExit(0)
#<<<---------------RunTime cache---------->>>
def cleanCache():
    for i in ['.cloudIcon.png', '.bhutuuIcon.png']:
        if os.path.exists(i):
            os.remove(i)
cleanCache()
def getCache():
    bytes_data1 = base64.b64decode(ImageRequired.cloudImageBytes)
    bytes_data2 = base64.b64decode(ImageRequired.bhutuuImageBytes)
    cloudImageFile = open('.cloudIcon.png', 'wb')
    bhutuuImageFile = open('.bhutuuIcon.png', 'wb')
    cloudImageFile.write(bytes_data1)
    bhutuuImageFile.write(bytes_data2)
    cloudImageFile.close()
    bhutuuImageFile.close()
#<<<--------Function-------->>>
def cloudflare(lhost, lport):
    if realName == 'windows':
        cloudflare_command = 'cloudflared -url '+str(lhost)+':'+str(lport)+' --logfile '+cloudflare_log+' >'+os.devnull+' 2>&1'
        # subprocess.Popen(cloudflare_command)
        with open(os.devnull, 'wb') as log:
            running = subprocess.Popen(cloudflare_command, stdout=log, stderr=log)
def getLink():
    link = ''
    while not link:
        if os.path.exists(cloudflare_log):
            with open(cloudflare_log) as cloudlog:
                for line in cloudlog:
                    url = re.findall('https://[-0-9a-z]*\.trycloudflare.com', line)
                    if not url:
                        pass
                    else:
                        print(url[0])
                        link = url[0]
                cloudlog.close()
        else:
            continue
    return link

# threading.Thread(target=cloudflare('127.0.0.1', 8080)).start()
# threading.Thread(target=getLink).start()

#<<<<-------Graphical design------>>>
winRoot = Tk()
getCache()
iconPhoto = PhotoImage(file='.cloudIcon.png')
winRoot.iconphoto(False, iconPhoto)
winRoot.title('cloudflare-ui')
# Box size
winRoot.geometry('600x400')
#<<<----Frames----->>>
mainFrame = Frame(winRoot, bg='pink').pack(fill='both')
#introFrame
introFrame = Frame(mainFrame, bg='white', height=100, highlightbackground='pink', highlightthickness=5)
#intoduction text
introText = '''Welcome to cloudflare GUI
Author: Suman Kumar ~BHUTUU'''
introLabel = Label(introFrame, text=introText, bg='white', font=("Arial", 9, "bold")).pack()
#cloudflare Image
cloudImage = Image.open('.cloudIcon.png')
resizedCloudImage = cloudImage.resize((50,50), Image.LANCZOS)
plugCloudImage = ImageTk.PhotoImage(resizedCloudImage)
cloudImageLabel = Label(introFrame, image=plugCloudImage, bg="white").pack(side=LEFT, padx=[100,0])
#bhutuu Image
bhutuuImage = Image.open('.bhutuuIcon.png')
resizedBhutuuImage = bhutuuImage.resize((50, 50), Image.LANCZOS)
plugBhutuuImage = ImageTk.PhotoImage(resizedBhutuuImage)
bhutuuImageLabel = Label(introFrame, image=plugBhutuuImage, bg='white').pack(side=RIGHT, padx=[0,100])
introFrame.pack(side=TOP, fill=X, padx=20, pady=[20,0])
#Program and Field frame:
programHead = Label(mainFrame,text="<<<---Connect your localhost to the Internet--->>>", font='chiller 20 bold').pack()
#fields:
localHostInput = StringVar()
localPortInput = IntVar()
localHostInput.set("127.0.0.1")
localPortInput.set(8080)
forwardedUrl = StringVar()
forwardedUrl.set("Link will be here :)")
fieldFrame = Frame(mainFrame)
hostFrame = Frame(fieldFrame)
hostLabel = Label(hostFrame, text="Local Host:> ", font=('Comic Sans MS', '15', 'bold')).pack(side=LEFT)
hostEntry = Entry(hostFrame, textvariable=localHostInput, font=('Consolas', '12', 'bold')).pack(side=RIGHT)
hostFrame.pack()
portFrame = Frame(fieldFrame)
portLabel = Label(portFrame, text='Local Port:> ', font=('Comic Sans MS', '15', 'bold')).pack(side=LEFT)
portEntry = Entry(portFrame, textvariable=localPortInput, font=('Consolas', '12', 'bold')).pack(side=RIGHT)
portFrame.pack()
fieldFrame.pack(anchor='nw', padx=[20, 0], pady=[10,0])
#link Frame
linkFrame = Frame(mainFrame)
linkHeadLabel = Label(linkFrame, text="Forwarded on URL: ").pack(side=LEFT)
linkLable = Label(linkFrame, textvariable=forwardedUrl, font=('Arial', '10', 'bold')).pack(side=RIGHT)
copyButton = Button(linkFrame, text="COPY", command=copyLink).pack
linkFrame.pack(side=LEFT, padx=[20])
cleanCache()
winRoot.mainloop()