# coding:utf-8
'''
Target: Python AndroidToolBox FileTransfer Module
Author: LZR@BUAA
Date:   08/30/2020
'''

from ftplib import FTP
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


class mThread (threading.Thread):
    def __init__(self, threadID, name, op):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.op = op

    def run(self):
        print("开始线程：" + self.name)
        UPlist(self.op)


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


def divide(list):
    '''
    Test Passed
    '''
    ADBlist.clear()
    FTPlist.clear()
    lenl = len(list)
    if lenl == 0:
        print("列表空！")
        exitProgram(2)
    for i in range(lenl // 2):
        FTPlist.append(list[i])
    for i in range((lenl // 2) + 1, lenl):
        ADBlist.append(list[i])


def UPlist(op):
    if op == 1:
        global ftp
        for i in FTPlist:
            uploadfile(ftp, i.split("/")[-1], i)
    else:
        for i in ADBlist:
            cmd("adb push \""+i+"\" /sdcard"+rmpath)
            # pushFile(i, "/sdcard"+rmpath)


def Upload():
    global ftp
    print("请选择：\n[1]文件上传\n[2]文件夹上传\n[3]退出程序")
    op = InputJudge(3)
    if op == 1:
        cur = filedialog.askopenfilenames(title="请选择文件")
        divide(cur)
        Thread1 = mThread(1, "FTPUP", 1)
        Thread2 = mThread(2, "ADBUP", 0)
        Thread1.start()
        Thread2.start()
    elif op == 2:
        dirl = filedialog.askdirectory(title="请选择文件夹")
        print("正在启动传输……")
        list_short = os.listdir(dirl)
        list_long = [dirl+"/"+x for x in list_short]
        divide(list_long)
        Thread1 = mThread(1, "FTPUP", 1)
        Thread2 = mThread(2, "ADBUP", 0)
        Thread1.start()
        Thread2.start()
        exitProgram(0)
    elif op == 3:
        exitProgram(1)


def singleUpload():
    global ftp
    print("请选择：\n[1]打开文件对话框选择文件(适用于少量文件上传)\n[2]打开文件夹添加文件(适用于大量文件上传)\n[3]退出程序")
    op = InputJudge(3)
    if op == 1:
        cur = filedialog.askopenfilenames()
        print(cur)
        for i in cur:
            # print("/AndroidToolBox/"+i)
            uploadfile(ftp, i.split("/")[-1], i)
    elif op == 2:
        os.startfile(localpath)
        input("复制完成后请按Enter继续")
        print("正在启动传输……")
        list_dir = os.listdir(localpath)
        for i in list_dir:
            print("正在传输文件：" + i)
            uploadfile(ftp, i, localpath+i)
        print("传输完成！")
        exitProgram(0)
    elif op == 3:
        exitProgram(1)


def Download():
    messagebox.showinfo("映射成功！", "请在打开的窗口中直接进行文件操作")
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
    print("########################################")
    print("")
    print("              高速文件传输")
    print("              By:LZR@BUAA")
    print("")
    print("########################################")
    cmd("adb disconnect")
    # print("*************实验性功能提醒*************")
    # input("请知悉：由于Windows系统命令行的编码问题\n以高速模式传输路径含有中文的文件可能会使程序崩溃\n按Enter继续……")
    print("程序采用FTP共享+ADB方式突破USB速率限制进行文件传输\n请打开调试和安全设置，USB连接稳定，WLAN在同一局域网下")
    while True:
        if USBConnected():
            if powerStatus():
                MobileInfo = getInfo()
                IP = getIPaddress()
                getInfo()
                print("手机连接成功！当前设备: " +
                      MobileInfo['brand'] + " " + MobileInfo['model'])
                break
            else:
                print("手机开机状态异常，是否重新开机？(Y/N)")
                if InputJudge(2):
                    cmd("adb reboot")
        # time.sleep(2)
    if cmd("adb shell pm list package").find("com.my.ftpdemo") == -1:
        print("正在安装FTP客户端 请稍候……")
        r = cmd("adb install FtpClient.apk")
        if r.find("Success"):
            print("安装成功！")
    print("正在启动FTP客户端……请在手机授权管理中授予权限")
    os.system("adb shell am start com.my.ftpdemo/.MainActivity")
    StartFTP(IP, fport, fuser, fpass)
    print("是否打开FTP界面？(Y/N)")
    if InputJudge(2):
        os.startfile("ftp://"+fuser+":"+fpass+"@"+IP+":"+str(fport))
        # messagebox.showinfo("登录信息", "服务器：" + IP + "\n端口号：" +
        #                     str(fport)+"\n账号："+fuser+"\n密码："+fpass)
        # print("登录信息\n服务器：" + IP + "\n端口号：" +
        #   str(fport)+"\n账号："+fuser+"\n密码："+fpass)
        # os.system("explorer "+"ftp://"+fuser+":"+fpass+"@"+IP+":"+str(fport))
    print("功能列表：\n[1]批量上传文件\n[2]批量下载文件\n[3]退出")
    op = InputJudge(3)
    if op == 1:
        Upload()
    elif op == 2:
        Download()
    elif op == 3:
        exitProgram(1)


if __name__ == "__main__":
    FileTransmain()
