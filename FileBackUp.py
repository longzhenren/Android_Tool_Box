# coding:utf-8
'''
Target: Python AndroidToolBox FileBackup Module
Author: LZR@BUAA
Date:   08/26/2020
'''

from ftplib import FTP
from Methods import *

tk = Tk()
tk.withdraw()

wechatimage = "/sdcard/tencent/MicroMsg/WeiXin"
wechatfiles = "/sdcard/Android/data/com.tencent.mm/MicroMsg/Download/"
qqimage = "/sdcard/tencent/qq_images"
qqfiles = "/sdcard/Android/data/com.tencent.mobileqq/Tencent/QQfile_recv/"
pictures = "/sdcard/DCIM/"


def qqbackup():
    os.system("cls")
    print("+--------------QQ文件备份--------------+")
    print("[1]备份QQ图片\t[2]备份QQ文档\n[3]全部备份\t[4]退出程序")
    print("请选择-> ", end='')
    op = InputJudge(4)
    input("请选择备份目录,按Enter继续")
    backupdir = filedialog.askdirectory(title='选择备份目录')
    tm = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    if not os.path.exists(backupdir+"/QQbackup/"):
        os.mkdir(backupdir+"/QQbackup/")
    os.mkdir(backupdir+"/QQbackup/"+tm+"/")
    os.mkdir(backupdir+"/QQbackup/"+tm+"/image/")
    os.mkdir(backupdir+"/QQbackup/"+tm+"/files/")
    if op == 1:
        print("正在备份QQ图片,请稍等")
        pullFile(qqimage, backupdir+"/QQbackup/"+tm+"/image/")
        exitProgram(0)
    elif op == 2:
        print("正在备份QQ文档,请稍等")
        pullFile(qqfiles, backupdir+"/QQbackup/"+tm+"/files/")
        exitProgram(0)
    elif op == 3:
        print("正在备份QQ图片,请稍等")
        pullFile(qqfiles, backupdir+"/QQbackup/"+tm+"/files/")
        print("正在备份QQ文档,请稍等")
        pullFile(qqimage, backupdir+"/QQbackup/"+tm+"/image/")
        exitProgram(0)
    elif op == 4:
        exitProgram(1)


def wechatbackup():
    os.system("cls")
    print("+--------------微信文件备份--------------+")
    print("[1]备份微信图片\t[2]备份微信文档\n[3]全部备份\t[4]退出程序")
    print("请选择-> ", end='')
    op = InputJudge(4)
    input("请选择备份目录,按Enter继续")
    backupdir = filedialog.askdirectory(title='选择备份目录')
    tm = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    if not os.path.exists(backupdir+"/Wechatbackup/"):
        os.mkdir(backupdir+"/Wechatbackup/")
    os.mkdir(backupdir+"/Wechatbackup/"+tm+"/")
    os.mkdir(backupdir+"/Wechatbackup/"+tm+"/image/")
    os.mkdir(backupdir+"/Wechatbackup/"+tm+"/files/")
    if op == 1:
        print("正在备份微信图片,请稍等")
        pullFile(wechatimage, backupdir+"/Wechatbackup/"+tm+"/image/")
        exitProgram(0)
    elif op == 2:
        print("正在备份微信文档,请稍等")
        pullFile(wechatfiles, backupdir+"/Wechatbackup/"+tm+"/files/")
        exitProgram(0)
    elif op == 3:
        print("正在备份微信图片,请稍等")
        pullFile(wechatfiles, backupdir+"/Wechatbackup/"+tm+"/files/")
        print("正在备份微信文档,请稍等")
        pullFile(wechatimage, backupdir+"/Wechatbackup/"+tm+"/image/")
        exitProgram(0)
    elif op == 4:
        exitProgram(1)


def photobackup():
    os.system("cls")
    print("+----------------图片备份----------------+")
    print("[1]备份系统图库\t[2]仅备份相机胶卷\n[3]退出程序")
    print("请选择-> ", end='')
    op = InputJudge(3)
    input("请选择备份目录,按Enter继续")
    backupdir = filedialog.askdirectory(title='选择备份目录')
    tm = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    if not os.path.exists(backupdir+"/Imagebackup/"):
        os.mkdir(backupdir+"/Imagebackup/")
    os.mkdir(backupdir+"/Imagebackup/"+tm+"/")
    if op == 1:
        print("正在备份图库")
        pullFile(pictures, backupdir+"/Imagebackup/"+tm)
        exitProgram(0)
    elif op == 2:
        print("正在备份照片")
        pullFile(pictures+"/Camera/", backupdir+"/Imagebackup/"+tm)
        exitProgram(0)
    elif op == 3:
        exitProgram(1)


def appBackandRestore():
    print("+--------------应用备份还原--------------+")
    print("[1]备份全部App\t[2]还原全部APP\n[3]退出程序")
    print("请选择-> ", end='')
    op = InputJudge(3)
    if op == 1:
        appbackup()
    elif op == 2:
        apprestore()
    elif op == 3:
        exitProgram(1)


def apprestore():
    print("请选择备份文件")
    abdir = filedialog.askopenfilename(
        title="选择备份的.ab文件位置", filetypes=[('ADB备份文件', '*.ab'), ])
    print("正在还原备份:"+abdir[0])
    cmd("adb restore "+abdir)
    exitProgram(0)


def appbackup():
    print("请选择备份文件的保存位置")
    backupdir = filedialog.askdirectory(title='选择备份目录')
    messagebox.showinfo("提示", "请在手机端点击以确认备份")
    tm = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    print("正在备份到"+tm+".ab")
    cmd("adb backup -apk -all -f "+backupdir+"/"+tm+".ab")
    exitProgram(0)


def FileBackupmain():
    os.system("cls")
    print("########################################")
    print("")
    print("                备份工具")
    print("              By:LZR@BUAA")
    print("")
    print("########################################")
    time.sleep(1)
    while True:
        os.system("cls")
        print("+--------------备份工具--------------+")
        print("[1]一键备份照片\t[2]备份微信文档\n[3]备份QQ文档\t[4]备份手机应用\n[5]退出程序")
        print("请选择-> ", end='')
        op = InputJudge(5)
        if op == 1:
            photobackup()
        elif op == 2:
            wechatbackup()
        elif op == 3:
            qqbackup()
        elif op == 4:
            appBackandRestore()
        elif op == 5:
            break
    exitProgram(1)


if __name__ == "__main__":
    FileBackupmain()
