# coding:utf-8
'''
Target: Python AndroidToolBox ADB Plugin Methods Module
Author: LZR@BUAA
Date:   08/26/2020
'''
import io
import os
import re
import subprocess
import sys
import tarfile
import time
import datetime
import threading

from tkinter import Tk, filedialog, messagebox

tk = Tk()
tk.withdraw()

'''
Check Connections:
'''


def getFastbootConnection():
    cmd("fastboot devices")


def USBConnected():
    echo = cmd("adb devices").split("\n")
    return echo[1] != ''


def BLConnected():
    echo = cmd("fastboot devices").find("fastboot")
    return echo != -1


def WLANConnected():
    if powerStatus():
        IP = getIPaddress()
        r = cmd("adb devices")
        if r.find(IP) == -1:
            return False
        else:
            return True


'''
Reboot:
'''


def rebootList():
    os.system("cls")
    print("+--------------重启菜单--------------+")
    print("[1]重启到系统\n[2]重启到Recovery\n[3]重启到BootLoader\n[4]退出程序")
    print("请选择-> ", end='')
    op = InputJudge(4)
    if op == 1:
        rebootUI()
    elif op == 2:
        rebootRec()
    elif op == 3:
        rebootBL()
    elif op == 4:
        exitProgram(1)
    exitProgram(0)


def rebootUI():
    if BLConnected():
        cmd("fastboot reboot")
    if(USBConnected):
        cmd("adb reboot")


def rebootBL():
    cmd("adb reboot bootloader")


def rebootRec():
    cmd("adb reboot recovery")


'''
Get Info:
'''


def getInfo():
    MobileInfo = {}
    model = cmd("adb shell getprop ro.product.model").replace(
        '\n', '').replace('\r', '')
    manufacturer = cmd("adb shell getprop ro.product.brand").replace(
        '\n', '').replace('\r', '')
    APIver = cmd("adb shell getprop ro.build.version.sdk").replace(
        '\n', '').replace('\r', '')
    wlandevice = cmd("adb shell getprop wifi.interface").replace(
        '\n', '').replace('\r', '')
    Serial = cmd("adb shell getprop ro.boot.serialno").replace(
        '\n', '').replace('\r', '')
    version = cmd("adb shell getprop ro.build.version.release").replace(
        '\n', '').replace('\r', '')
    battery = cmd("adb shell dumpsys battery | findstr \"level\"").split(": ")[-1].replace(
        '\n', '').replace('\r', '')

    MobileInfo.update({'model': model, 'API': APIver, 'android': version,
                       'brand': manufacturer, 'Wlan': wlandevice, 'serial': Serial, 'battery': battery})

    return MobileInfo


def getIPaddress():
    netstatus = cmd("adb shell ip addr | findstr \"wlan0\"")
    IP = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", netstatus)
    return IP[0]


def powerStatus():
    PowerStat = cmd("adb shell getprop sys.boot_completed")
    if PowerStat == "\n":
        return False
    else:
        return True


'''
File Operations:
'''


def pushFile(sourcedir, rmpath):
    print(cmd("adb push " + sourcedir + " " + rmpath))


def pullFile(rmpath, destdir):
    print(cmd("adb pull " + rmpath + " " + destdir))


def touchPoint(x, y):
    cmd("adb shell input tap "+x+" "+y)


def slidePoint(x1, y1, x2, y2):
    cmd("adb shell input swipe "+x1+" "+y1+" "+x2+" "+y2)


def cmd(command):
    r = os.popen(command).read()
    return r


def unziptar(filename, dirs):
    t = tarfile.open(filename)
    t.extractall(path=dirs)
    t.close()


def InputJudge(num):
    if num == 2:
        while True:
            command = input()
            if command not in ['Y', 'y', 'N', 'n']:
                print("输入有误,请检查输入!")
            else:
                if command in ['y', 'Y']:
                    return True
                else:
                    return False
    else:
        while True:
            command = input()
            if command.isdigit():
                intput = int(command)
                if intput not in range(1, num+1):
                    print("输入有误,请检查输入!")
                else:
                    return intput
            else:
                print("输入有误,请检查输入!")


def exitProgram(num):
    if num == 0:
        print("\n操作已成功完成,程序退出中……")
        time.sleep(1)
    elif num == 1:
        print("\n用户终止操作,程序退出中……")
        time.sleep(1)
    elif num == 3:
        print("\n出现异常,程序退出中……")
        time.sleep(1)


'''
def fastbootReboot():
    cmd("fastboot reboot")


def NewProgram(pyFileName):
    os.system('cls')
    # print("Press Enter to Continue……")
    print(cmd("python "+pyFileName))


def dragtoWindowGetName():
    filedir = input("请将文件拖动到窗口,并点击窗口后按下Enter")
    return filedir


def dragtoPush(rmpath):
    dir = dragtoWindowGetName()
    pushFile(dir, rmpath)


def lockStatus():
    rebootBL()
    while True:
        if BLConnected():
            break
    r = cmd("fastboot oem device-info | findstr unlocked")
    if r.split(":")[-1].replace(" ", "") == "true":
        return True
    else:
        return False
'''
