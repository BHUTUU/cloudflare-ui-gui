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
#<<<-----Definig Functions----->>>
def localCmd(command):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out.decode().split('\n'), err
def cloudflare(lhost,lport):
    if os.name == 'nt':
        commandToRun = 'cloudflared -url '+lhost+':'+str(lport)+' >null 2>&1'
        # print('bash <('+commandToRun+')')
        with open(cloudflare_log, 'w') as logbook:
            cloudflareRun = subprocess.Popen(commandToRun, stdout=logbook, stderr=logbook)
        # run = localCmd(commandToRun)
        return cloudflareRun
winRoot = Tk()
# Title bar and Icon
getCache()
iconPhoto = PhotoImage(file='.cloudIcon.png')
winRoot.iconphoto(False, iconPhoto)
winRoot.title('cloudflare-ui')
# Box size
winRoot.geometry('600x400')
#<<---Frames--->>
mainFrame = Frame(winRoot, bg='pink').pack(fill="both")
#introFrame
introFrame = Frame(mainFrame,bg="white", height=100, highlightbackground="pink", highlightthickness=5)
introFrame.pack(side=TOP, fill=X, padx=20, pady=[20,0])
#Introduction text
introText = '''Welcome to cloudflare GUI
Author: Suman Kumar ~BHUTUU'''
introLabel = Label(introFrame, text=introText, bg="white", font="arial 9 bold")
introLabel.pack()
#Cloudflare Image
cloudImage = Image.open(".cloudIcon.png")
resizedCloudImage= cloudImage.resize((50,50), Image.LANCZOS)
plugCloudImage = ImageTk.PhotoImage(resizedCloudImage)
cloudImageLable = Label(introFrame, image=plugCloudImage, bg="white")
cloudImageLable.pack(side=LEFT, padx=[50,0])
#Bhutuu Image
bhutuuImage = Image.open(".bhutuuIcon.png")
resizedBhutuuImage = bhutuuImage.resize((50,50), Image.LANCZOS)
plugBhutuuImage = ImageTk.PhotoImage(resizedBhutuuImage)
bhutuuImageLable = Label(introFrame, image=plugBhutuuImage, bg="white")
bhutuuImageLable.pack(side=RIGHT, padx=[0,50])
#Program and fields frame:
programHead = Label(mainFrame,text="<<<---Connect your localhost to the Internet--->>>", font='arial 12 bold').pack()
#field frame>>>
localHostInput = StringVar()
localPortInput = IntVar()
localHostInput.set("127.0.0.1")
localPortInput.set(8080)
forwardedUrl = StringVar()
inputFrame = Frame(mainFrame,highlightbackground='black', highlightthickness=2)
hostFrame = Frame(inputFrame)
localHostLabel = Label(hostFrame, text="Enter your localhost: ")
localHostLabel.pack(side=LEFT)
localHostInputBox = Entry(hostFrame,textvariable=localHostInput)
localHostInputBox.pack(side=RIGHT)
hostFrame.pack()
portFrame = Frame(inputFrame)
localPortLabel = Label(portFrame, text="Enter your localport: ")
localPortLabel.pack(side=LEFT)
localPortInputBox = Entry(portFrame, textvariable=localPortInput)
localPortInputBox.pack(side=RIGHT)
portFrame.pack()
inputFrame.pack(side=LEFT, padx=[20,0])
def linkGenerator():
    while True:
        try:
            link = localCmd("grep -o 'https://[-0-9a-z]*\.trycloudflare.com' "+cloudflare_log)
        except SyntaxError:
            pass
        if not link[0]:
            time.sleep(1)
        else:
            break
    forwardedUrl.set(link) 

def onClickForward():
    # forwardButton['state'] = DISABLED
    if not localHostInput.get() or not localPortInput.get():
        messagebox.showerror(title="Error!", message="Both fields are mandatory!", icon='error')
    else:
        runner = threading.Thread(target=cloudflare(str(localHostInput.get()), str(localPortInput.get()))).start()
        threading.Thread(target=linkGenerator).start()


def onClickCancel():
    try:
        pidOfCloudflared = localCmd("tasklist | grep cloudflared |awk '{print $2}'")
        if not pidOfCloudflared[0][0]:
            pass
        else:
            pidList = pidOfCloudflared[0]
            print(pidOfCloudflared[0])
            for i in pidList:
                if not i:
                    continue
                os.kill(int(i), 2)
    except SyntaxError:
        pass 
    try:
        if os.path.exists(cloudflare_log):
            os.remove(cloudflare_log)
    except:
        pass
    winRoot.destroy()
    SystemExit(0)
def copyToClipboard(message):
    winRoot.clipboard_clear()
    winRoot.clipboard_append(message)
urlFrame = Frame(mainFrame)
url = Label(urlFrame, textvariable=forwardedUrl, bg='orange').pack()
urlFrame.pack()
buttonFrame = Frame(mainFrame)
forwardButton = Button(buttonFrame, text='Forward', state=NORMAL, command=onClickForward).pack(side=LEFT, padx=50)
cancelButton = Button(buttonFrame, text='Cancel', command=onClickCancel).pack(side=RIGHT)
buttonFrame.pack(side=BOTTOM)
cleanCache()
winRoot.mainloop()