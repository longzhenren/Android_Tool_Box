# coding:utf-8
'''
Target: Python AndroidToolBox FileTransfer Module
Author: LZR@BUAA
Date:   08/30/2020
'''

from ftplib import FTP
import locale
import subprocess
from Methods import *


Update = Tk()
Update.withdraw()
FTPlist = []
ADBlist = []
Selectlist = []

IP = ""
path = os.getcwd()
ftp = FTP()
rmpath = "/AndroidToolBox/"
t1st = 0
t2st = 0

# def cmd1(command):
#     return os.popen(command).read()

# class mThread (threading.Thread):
#     global t1st,t2st
#     t1st=t2st=0
#     def __init__(self, threadID, name, op):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.op = op

#     def run(self):
#         # print("开始线程:" + self.name)
#         UPlist(self.op)


def downloadfile(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'wb')
    ftp.encoding = "utf-8"
    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
    ftp.set_debuglevel(0)
    fp.close()


def uploadfile(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'rb')
    ftp.encoding = "utf-8"
    ftp.storbinary('STOR ' + remotepath, fp, bufsize)
    ftp.set_debuglevel(0)
    fp.close()
    # return 1


def divide(list):
    ADBlist.clear()
    FTPlist.clear()
    lenl = len(list)
    if lenl == 0:
        print("列表空!")
        exitProgram(2)
    for i in range(lenl // 2):
        FTPlist.append(list[i])
    for i in range((lenl // 2) + 1, lenl):
        ADBlist.append(list[i])
    # print(ADBlist)
    # print(FTPlist)


def ADBUP():
    # global t1st
    # t1st = 0
    # os.popen("chcp 65001")
    for i in ADBlist:
        command = "adb push \""+i+"\" /sdcard"+rmpath+i.split("/")[-1]
        os.popen(command)
        # t1st = 1


def FTPUP():
    # global t2st
    # t2st = 0
    global ftp
    for i in FTPlist:
        uploadfile(ftp, i.split("/")[-1], i)
    # t2st = 1


def Upload():
    global ftp
    global t1st, t2st
    os.system("cls")
    print("+--------------文件上传--------------+")
    print("[1]文件上传\n[2]文件夹上传\n[3]退出程序")
    print("请选择-> ", end='')
    op = InputJudge(3)
    if op == 1:
        cur = filedialog.askopenfilenames(title="请选择文件")
        divide(cur)
        Thread1 = threading.Thread(target=ADBUP)
        Thread2 = threading.Thread(target=FTPUP)
        Thread1.start()
        Thread2.start()
        # exitProgram(0)
        # print("文件将保存到/sdcard/AndroidToolBox/下,\n完成传输后程序自动退出")
        input("文件将保存到/sdcard/AndroidToolBox/下,\n请按Enter键开始传输,完成后程序将自动退出")

    elif op == 2:
        dirl = filedialog.askdirectory(title="请选择文件夹,不支持递归")
        print("正在启动传输……")
        list_short = os.listdir(dirl)
        list_long = [dirl+"/"+x for x in list_short]
        divide(list_long)
        Thread1 = threading.Thread(target=ADBUP)
        Thread2 = threading.Thread(target=FTPUP)
        Thread1.start()
        Thread2.start()
        input("文件将保存到/sdcard/AndroidToolBox/下,\n请按Enter键开始传输,完成后程序将自动退出")
        # exitProgram(0)
    elif op == 3:
        # os.system("chcp 936")
        exitProgram(1)


# def singleUpload():
#     global ftp
#     print("[1]打开文件对话框选择文件(适用于少量文件上传)\n[2]打开文件夹添加文件(适用于大量文件上传)\n[3]退出程序")
#     print("请选择-> ",end = '')
#     op = InputJudge(3)
#     if op == 1:
#         cur = filedialog.askopenfilenames()
#         print(cur)
#         for i in cur:
#             # print("/AndroidToolBox/"+i)
#             uploadfile(ftp, i.split("/")[-1], i)
#     elif op == 2:
#         os.startfile(localpath)
#         input("复制完成后请按Enter继续")
#         print("正在启动传输……")
#         list_dir = os.listdir(localpath)
#         for i in list_dir:
#             print("正在传输文件:" + i)
#             uploadfile(ftp, i, localpath+i)
#         print("传输完成!")
#         exitProgram(0)
#     elif op == 3:
#         exitProgram(1)


def Download():
    messagebox.showinfo("映射成功!", "请在打开的窗口中直接进行文件操作")
    os.system("explorer ftp://LZR:BUAA21@192.168.2.106:1921")


def StartFTP(IP, Port, User, Pass):
    print("启动FTP服务中……")
    ftp.set_debuglevel(0)
    ftp.connect(IP, Port)
    ftp.login(User, Pass)
    ftp.set_pasv(False)
    ftp.encoding = "utf-8"
    print(ftp.getwelcome())
    if "AndroidToolBox" not in ftp.nlst():
        ftp.mkd("/AndroidToolBox/")
    ftppath = "AndroidToolBox"
    ftp.cwd(ftppath)


def FileTransmain():
    fport = 1921
    fuser = "LZR"
    fpass = "BUAA21"
    os.popen("chcp 65001")
    os.system("cls")
    print("#######################################")
    print("")
    print("              高速文件传输")
    print("              By:LZR@BUAA")
    print("")
    print("#######################################")
    cmd("adb disconnect")
    # print("*************实验性功能提醒*************")
    # input("请知悉:由于Windows系统命令行的编码问题\n以高速模式传输路径含有中文的文件可能会使程序崩溃\n按Enter继续……")
    print("程序采用FTP+ADB突破USB速率进行文件传输\n请保持USB连接稳定,且与设备在同一局域网")
    while True:
        if USBConnected():
            if powerStatus():
                MobileInfo = getInfo()
                IP = getIPaddress()
                getInfo()
                print("手机连接成功!当前设备: " +
                      MobileInfo['brand'] + " " + MobileInfo['model'])
                break
            else:
                print("手机开机状态异常,是否重新开机?(Y/N)")
                if InputJudge(2):
                    cmd("adb reboot")
        # time.sleep(2)
    if cmd("adb shell pm list package").find("com.my.ftpdemo") == -1:
        print("正在安装FTP客户端 请稍候……")
        r = cmd("adb install FtpClient.apk")
        if r.find("Success"):
            print("安装成功!")
    print("正在启动FTP客户端……请在手机端授予权限")
    cmd("adb shell am start com.my.ftpdemo/.MainActivity")
    StartFTP(IP, fport, fuser, fpass)
    print("FTP连接成功,是否在资源管理器中打开?(Y/N)")
    if InputJudge(2):
        cmd("explorer ftp://"+fuser+":"+fpass+"@"+IP+":"+str(fport))
        # messagebox.showinfo("登录信息", "服务器:" + IP + "\n端口号:" +
        #                     str(fport)+"\n账号:"+fuser+"\n密码:"+fpass)
        # print("登录信息\n服务器:" + IP + "\n端口号:" +
        #   str(fport)+"\n账号:"+fuser+"\n密码:"+fpass)
        # os.system("explorer "+"ftp://"+fuser+":"+fpass+"@"+IP+":"+str(fport))
    os.system("cls")
    print("+--------------文件传输--------------+")
    print("[1]批量上传文件\n[2]批量下载文件\n[3]退出程序")
    print("请选择-> ", end='')
    op = InputJudge(3)
    if op == 1:
        Upload()
    elif op == 2:
        Download()
    elif op == 3:
        exitProgram(1)


if __name__ == "__main__":
    FileTransmain()
