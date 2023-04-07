import subprocess, os
cloudflare_log = os.path.expanduser('~')+"/AppData/Local/Temp/cloudflare.log"
# print(cloudflare_log)
# if (os.path.exists(cloudflare_log)):
#     os.remove(cloudflare_log)
# else:
#     with open(cloudflare_log,'w') as file:
#         file.write("heloo")
#         file.close()
# print(os.path.exists(cloudflare_log))
if not os.path.exists(cloudflare_log):
    with open(cloudflare_log, 'w') as f:
        f.write("<<<---------cloudflare-Log---------->>>")
        f.close()
def localCmd(command):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out.decode().split('\n'), err
lhost = '127.0.0.1'
lport = 8080
commadToRun = 'cloudflared -url '+lhost+':'+str(lport)+' --logfile '+cloudflare_log+'>/dev/null 2>&1 &'
localCmd(commadToRun)
link = localCmd("tasklist | grep cloudflared |awk '{print $2}'")
print(link[0])