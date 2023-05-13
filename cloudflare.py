#Program: cloudfalreGui :: Program to forward localhost http port on internet with a beautiful user interface.
#Author: Suman Kumar ~BHUTUU
#Date: 19-02-2023 (initiation)
#Licence: --(to be implemented)
#<<<------Import section------>>>
import os, re, time, subprocess, platform, base64
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
elif OS.upper() == 'GNU/LINUX' or OS.upper() == 'POSIX':
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
            running = subprocess.Popen(cloudflare_command, stdout=log, stderr=log, shell=True)
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
                        # print(url[0])
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
winRoot.geometry('800x400')
winRoot.minsize(800, 400)
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
localPortInput = StringVar()
count = IntVar()
localHostInput.set("127.0.0.1")
localPortInput.set("8080")
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
def copyLink():
    winRoot.clipboard_clear()
    winRoot.clipboard_append(forwardedUrl.get())
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
                        # print(url[0])
                        link = url[len(url)-1]
                cloudlog.close()
        else:
            continue
    forwardedUrl.set(link)
def killCloudflare():
    if realName == 'windows':
        try:
            pidOfCloudflared = localCmd("tasklist | grep cloudflared |awk '{print $2}'")
            if not pidOfCloudflared[0][0]:
                pass
            else:
                pidList = pidOfCloudflared[0]
                for i in pidList:
                    if not i:
                        continue
                    os.kill(int(i), 2)
        except SyntaxError:
            pass
    elif realName == 'GNU/Linux':
        try:
            os.system("killall -2 cloudflared")
        except SyntaxError:
            pass
def delCloudLogFile():
    try:
        if os.path.exists(cloudflare_log):
            os.remove(cloudflare_log)
    except:
        pass
def doForward():
    if not localHostInput.get() or not localPortInput.get():
        messagebox.showerror(title='Error',message="Both fields are mandatory!")
    else:
        killCloudflare()
        try:
            if os.path.exists(cloudflare_log):
                os.remove(cloudflare_log)
        except:
            pass
        winRoot.update_idletasks()
        forwardedUrl.set("Please wait....!")
        threading.Thread(target=cloudflare('127.0.0.1', 8080)).start()
        threading.Thread(target=getLink).start()
def onClickForward():
    count.set(count.get()+1)
    if count.get() == 1:
        doForward()
    else:
        messagebox.showinfo(title='Error!', message="Restart cloudflare to forward again!", icon='error')

def localCmd(command):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out.decode().split('\n'), err
def onClickCancel():
    killCloudflare()
    winRoot.destroy()
    delCloudLogFile()
    SystemExit(0)
linkFrame = Frame(mainFrame).pack(padx=[20,0])
linkHeadLabel = Label(linkFrame, text="<---Forwarded on URL--->", font=('Roman', 15, 'bold')).pack()
linkLable = Label(linkFrame,bg='skyblue',height=2, highlightbackground='black', highlightthickness=3, textvariable=forwardedUrl, font=('Arial', '10', 'bold')).pack(fill=X, padx=30)
copyButton = Button(linkFrame, text="copy", width=10,highlightbackground='black', highlightthickness=2,state=NORMAL, command=copyLink).pack(pady=10)
controlFrame = Frame(winRoot)
forwardButton = Button(controlFrame, text='Forward', state=NORMAL, command=onClickForward).pack(side=LEFT, padx=[0,20])
cancelButton = Button(controlFrame, text='Cancel',state=NORMAL, command=onClickCancel).pack(side=RIGHT, padx=[90,0])
controlFrame.pack(side=BOTTOM, anchor='s', pady=[0,10])
cleanCache()
winRoot.mainloop()