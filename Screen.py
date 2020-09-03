# coding:utf-8
'''
Target: Python AndroidToolBox ScreenProjection Module
Author: LZR@BUAA
Date:   08/26/2020
'''

from Methods import *


def configGenerator(MobileInfo):
    conf = []
    config = ""
    conf.append("scrcpy --window-title \"" +
                MobileInfo['model'] + " By:LZR@BUAA\"")
    print("关闭手机屏幕?(Y/N)")
    if InputJudge(2):
        conf.append(" -S")

    print("主界面置顶?(Y/N)")
    if InputJudge(2):
        conf.append(" --always-on-top")

    print("全屏显示?(Y/N)")
    if InputJudge(2):
        conf.append(" -f")

    pixels = ['', '', '1920', '1440', '1080']
    print("分辨率设置(原始比例):\n[1]默认 [2]1920 [3]1440 [4]1080")
    print("请选择-> ", end='')
    op = InputJudge(4)
    if op in [2, 3, 4]:
        conf.append(" -m "+pixels[int(op)])

    BitRate = ['', '20M', '10M', '8M', '4M', '2M']
    print(
        "比特率设定(数值越大画质越好,延迟越大):\n[1]20Mbps [2]10Mbps [3]8Mbps(默认) [4]4Mbps [5]2Mbps")
    print("请选择-> ", end='')
    op = InputJudge(5)
    conf.append(" -b "+BitRate[int(op)])

    print("启动屏幕录制?(Y/N)")
    if InputJudge(2):
        tm = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        conf.append(" -r "+"\""+os.path.expanduser('~') +
                    "\\ScreenRecord"+ tm + ".mp4\"")
    config = ''.join(conf)
    # print(config)
    settings = open("Scrcpy-Settings.txt", "w")
    settings.write(config)
    settings.close()
    print("当前配置已保存!")

    print("是否显示操作指南?(Y/N)")
    if InputJudge(2):
        os.startfile("tutor.png")
    return config


def initializeConfig(MobileInfo):
    if os.access("Scrcpy-Settings.txt", os.F_OK):
        settings = open("Scrcpy-Settings.txt", "r")
        if settings.read(6) == "scrcpy":
            print("检测到保存的配置,以上一次的配置启动?(Y/N)")
            settings.seek(0, 0)
            if InputJudge(2):
                config = settings.read()
                if config.find('-r') != -1:
                    # print(config[:config.find('-r')])
                    if not os.path.exists(os.path.expanduser('~') +"\\ScreenRecord\\"):
                        os.mkdir(os.path.expanduser('~') +"\\ScreenRecord\\")
                    tm = time.strftime("%Y%m%d_%H%M%S", time.localtime())
                    config = config[:config.find(
                        '-r')+3]+"\""+os.path.expanduser('~') +"\\ScreenRecord"+ tm + ".mp4\""
                return config
    else:
        print("请选择配置")
    config = configGenerator(MobileInfo)
    return config


def USBconnect(config):
    cmd(config)


def WLANconnect(config):
    IP = getIPaddress()
    if cmd("adb tcpip 5555").find("error") == -1:
        input("现在已经可以断开设备……断开连接后请按Enter")
        r = cmd("adb connect " + IP)
        if r.find("unable") == -1:
            USBconnect(config)
    else:
        print("设备连接失败!程序退出中……")
        exit()


def Screenmain():
    os.system("cls")
    print("########################################")
    print("")
    print("             Scrcpy投屏工具")
    print("              By:LZR@BUAA")
    print("")
    print("########################################")
    print("欢迎使用! 请连接手机并开启USB调试模式\nMIUI还需开启USB调试(安全设置)……")
    cmd("adb disconnect")
    MobileInfo = getInfo()
    while True:
        if USBConnected():
            if powerStatus():
                print("手机连接成功!当前设备: " +
                      MobileInfo['brand'] + " " + MobileInfo['model'])
                break
            else:
                print("手机开机状态异常,是否重新开机?(Y/N)")
                if InputJudge(2):
                    cmd("adb reboot")
        time.sleep(2)

    config = initializeConfig(MobileInfo)
    os.system("cls")
    print("+----------连接模式----------+")
    print("[1]有线连接\n[2]无线连接\n[3]退出程序")
    print("请选择-> ", end='')
    op = InputJudge(3)
    if op == 1:
        USBconnect(config)
    elif op == 2:
        WLANconnect(config)
    elif op == 3:
        exitProgram(1)
    cmd("adb disconnect")
    exitProgram(0)


if __name__ == "__main__":
    Screenmain()
