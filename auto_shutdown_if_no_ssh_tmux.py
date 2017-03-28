import os
import commands
import string
import datetime

def ssh_connection_count():
    status, output = commands.getstatusoutput("netstat -t | grep ':ssh' | wc -l")
    if status == 0:
        return string.atoi(output)
    else:
        return 0

def exist_tmux_session():
    status, output = commands.getstatusoutput("tmux ls")
    return status == 0

def has_GPU_task():
    status, output = commands.getstatusoutput("nvidia-smi --query-compute-apps=name --format=csv,noheader | wc -l")
    return status == 0 and string.atoi(output) > 0

def has_started_for(seconds):
    status, output = commands.getstatusoutput("awk -F. '{print $1}' /proc/uptime")
    if status ==0 and string.atoi(output) > seconds:
        return True
    elif status != 0:
        return True
    else:
        return False

def main():
    have_ssh_connect = ssh_connection_count() > 0
    logfile = "/home/titan/log/auto_shutdown_check.log"
    os.system("echo check auto shutdown at " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " > " + logfile)
    if have_ssh_connect:
        os.system("echo there are ssh connection. >> " + logfile)
        return
    have_tmux_session = exist_tmux_session()
    if have_tmux_session:
        os.system("echo there are tmux sessions. >> " + logfile)
        return
    if has_GPU_task():
        os.system("echo there are GPU tasks. >> " + logfile)
        return
    if not has_started_for(60*10): # if only start less than 10 minutes, maybe we not ssh yet.
        os.system("echo jsut start, wait for ssh. >> " + logfile)
        return
    os.system("echo should shutdown now. >> " + logfile)
    os.system("sudo shutdown -P now")
    
if __name__ == '__main__':
    main()
