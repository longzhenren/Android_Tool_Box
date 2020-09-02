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

MobileInfo = {}


def mainmenu():
    while True:
        os.system("cls")
        printmenu()
        op = int(input())
        while op not in range(0, 10):
            print("输入有误，请重新输入")
            op = int(input())
        if op == 1:
            printinfo()
        elif op == 2:
            Screen.Screenmain()
        elif op == 3:
            FastbootFlash.Flashmain()
        elif op == 4:
            FileTrans.FileTransmain()
        elif op == 5:
            FileBackUp.FileBackupmain()
        elif op == 6:
            SoftScript.Softmain()
        elif op == 7:
            rebootList()
        elif op == 8:
            os.startfile(os.getcwd()+"//README.html")
        elif op == 9:
            printcmd()
            exit()
        elif op == 0:
            print("感谢使用！再见！")
            exit()


def printcmd():
    print("          adb和fastbooot 工具")
    print("-----------------------------------------")
    print("         adb和fastboot命令示例")
    print(" adb命令：")
    print("	adb devices		:列出adb设备")
    print("	adb reboot		:重启设备")
    print("	adb reboot bootloader	:重启到fastboot模式")
    print("	adb reboot recovery	:重启到recovery模式")
    print("	adb reboot edl		:重启到edl模式")
    print("")
    print(" fastboot命令：")
    print("	fastboot devices			:列出fastboot设备")
    print("	fastboot reboot				:重启设备")
    print("	fastboot reboot-bootloader		:重启到fastboot模式")
    print("	fastboot flash <分区名称> <镜像文件名>	:刷写分区")
    print("	fastboot oem reboot-<模式名称> 		:重启到相应模式")
    print("	fastboot oem device-info 		:查看解锁状态")
    print("-----------------------------------------")


def printHello():
    print(cmd("type logo.txt"))
    time.sleep(2)
    os.system("cls")
    print("###############################################")
    print("            Android  Tool  Box")
    print("               安卓实用工具箱")
    print("                 Ver:1.0")
    print("              Author:LZR@BUAA")
    print("                  2020.8")
    print("###############################################")
    print("提醒:使用前请确保安卓手机的\"USB调试\"功能已开启\n仅在MIUI上测试通过 其他厂商设备不保证全部功能可用\n刷机有风险,请三思而后行!")

    # print(cmd("type mainhead.txt"))


def printinfo():
    print("手机型号："+MobileInfo['model'])
    print("制造商："+MobileInfo['brand'])
    print("安卓版本：" + MobileInfo['android']+"(API"+MobileInfo['API']+")")
    print("剩余电量："+MobileInfo['battery'])
    input("按Enter返回主菜单\n")
    # os.system("cls")


def printmenu():
    print("+-----------主菜单-----------+")
    print("[1]设备信息\t[2]投屏工具\n[3]刷机工具\t[4]文件快传\n[5]文件备份\t[6]软件工具\n[7]高级重启\t[8]关于项目\n[9]命令模式\t[0]退出程序")
    print("请选择-> ", end='')


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
    time.sleep(2)
    mainmenu()
