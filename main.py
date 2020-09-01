# coding:utf-8
'''
Target: Python AndroidToolBox Main Interactive Module
Author: LZR@BUAA
Date:   08/27/2020
'''

import FastbootFlash
import FileBackUp
import FileTrans
import Screen
import SoftScript
from Methods import *


def aboutProject():
    print("本项目在Android Debug Bridge的基础上二次封装\n基本整合了刷机过程中常用的工具\n旨在为Android玩家提供更加简单便捷的体验")
    print("功能反馈：hljzhangzhibo@126.com")
    print("作者B站：https://space.bilibili.com/24644307 (Ctrl+单击打开)")
    print("\"每个男人 至死仍是少年。\"")
    print("愿你刷机半生 归来仍是MIUI(逃)")
    input("\n按Enter返回主菜单")
    print(cmd("cls"))


def mainmenu():
    while True:
        printmenu()
        op = int(input())
        if op == 1:
            printinfo()
        elif op == 2:
            Screen.Screenmain()
        elif op == 3:
            FastbootFlash.Flashmain()
        elif op == 4:
            print("[1]高速文件传输\n[2]快速资料备份\n[3]返回主菜单")
            c = InputJudge(3)
            if c == 1:
                FileTrans.FileTransmain()
            elif c ==2:
                FileBackUp.FileBackupmain()
            elif c==3:
                continue
        elif op == 5:
            SoftScript.Softmain()
        elif op == 6:
            FastbootFlash.rebootList()
        elif op == 7:
            os.startfile(".//Readme.pdf")
        elif op == 8:
            os.startfile(".//runincmd.bat")
        elif op == 9:
            aboutProject()
        elif op == 0:
            print("感谢使用！再见！")
            exit()


def printHello():
    # print(cmd("type logo.txt"))
    print(cmd("type mainhead.txt"))


def printinfo():
    print("手机型号："+MobileInfo['model'])
    print("制造商："+MobileInfo['brand'])
    print("安卓版本：" + MobileInfo['android']+"(API"+MobileInfo['API']+")")
    print("剩余电量："+MobileInfo['battery'])
    input("\n按Enter返回主菜单")
    print(cmd("cls"))


def printmenu():
    print("***********主菜单*************")
    print("[1]设备信息\t[2]投屏工具\n[3]刷机工具\t[4]传输备份\n[5]软件工具\t[6]重启选项\n[7]功能介绍\t[8]命令模式\n[9]关于项目\t[0]退出程序\n------------请选择------------")


if __name__ == "__main__":
    printHello()
    print("\n等待连接手机……")

    if BLConnected():
        print("当前为Fastboot模式，即将重启到系统……")
        rebootUI()
        time.sleep(5)

    while True:
        if USBConnected():
            MobileInfo = getInfo()
            print("设备: "+MobileInfo['brand'] + " " +
                  MobileInfo['model'] + " (API" + MobileInfo['API'] + ") 已连接")
            break
    mainmenu()
