#coding:utf-8
'''
Target: Python AndroidToolBox Software Methods Module
Author: LZR@BUAA
Date:   08/26/2020
'''

from Methods import *

Apklist = []
path = os.getcwd()


def unInstallwithoutRoot(PackageName):
    cmd("adb shell pm uninstall -k --user 0" + PackageName)


def listAPKFiles(list_dir):
    num_of_APKs = 0
    for i in list_dir:
        if i.split(".")[-1] in ["apk", "APK", "Apk"]:
            Apklist.append(i)
            num_of_APKs += 1
    return num_of_APKs


def printAPKList(num):
    if num not in ["", "\n"]:
        num = len(Apklist)
    num = int(num)
    for i in range(num):
        print("[%d]\t%s", i, Apklist[i])


def inAPKList(APKname):
    if APKname in Apklist:
        return True
    else:
        return False


def askforInst(APKname):
    print("是否要安装 " + APKname + " ?(Y/N)")
    if InputJudge(2):
        print("请在手机端确认安装")
        return True
    else:
        return False


def pushApp(APKname):
    while True:
        print("APK： " + APKname + " 准备安装,请在手机端确认")
        if USBConnected():
            r = cmd("adb install " + APKname)
            print("正在安装 请稍候……")
            if r.find("Success"):
                return True
                break
            else:
                print("安装失败！")
                print("是否重试?(Y/N)")
                if InputJudge(2):
                    continue
                else:
                    break
        else:
            print("手机未连接，请检查USB连接状态！")
            print("是否重试?(Y/N)")
            if InputJudge(2):
                continue
            else:
                break


def Uninstall():
    print("**************免root软件卸载******************")
    print("请勿卸载系统关键软件！否则会导致无法开机等情况")
    applist = cmd("adb shell pm list package -f")
    tm = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    fp = open(tm+".txt", "w")
    fp.write(applist)
    print("请在打开的App列表中找到要卸载的包名")
    os.startfile(os.getcwd()+"/"+tm+".txt")
    while True:
        pack = input("请输入要卸载的包名,输入N退出...")
        if pack in ["N", "n"]:
            exitProgram(1)
        else:
            unInstallwithoutRoot(pack)
    exitProgram(0)


def installSoftware():
    print("ADB软件安装工具，By：LZR@BUAA")
    print("[1]批量安装：安装指定目录下的全部软件")
    print("[2]一般安装：选择APK文件进行安装")
    print("[3]退出程序")
    print("请输入运行模式：")
    op = InputJudge(3)
    if op == 1:
        apkdir = filedialog.askdirectory(title='选择APK目录')
        list_dir = os.listdir(apkdir)
        listAPKFiles(list_dir)
        for obj in Apklist:
            if askforInst(obj):
                pushApp(apkdir+"/"+obj)
                print(obj + "安装完成!")
    elif op == 2:
        fdir = filedialog.askopenfilenames(
            title='选择APK文件', filetypes=[('APK安装包', '*.apk'), ])
        if fdir == []:
            exitProgram(2)
        for app in fdir:
            if askforInst(app.split("/")[-1]):
                pushApp(app)
        exitProgram(0)
    elif op == 3:
        exitProgram(1)


def activeSofts():
    print("[1]冰箱Icebox激活\n[2]黑阈激活\n[3]炼妖壶激活")
    op = InputJudge(3)
    if op == 1:
        IceboxStart()
    elif op == 2:
        BreventStart()
    elif op == 3:
        IslandStart()


def IceboxStart():
    print("冰箱激活器ADB版，By：LZR@BUAA")
    print("请选择运行模式，详细区别见IceBox应用。输入数字按Enter确认")
    print("[1]设备管理员模式（需要清除账号）")
    print("[2]ADB普通模式（重启后需重新激活）")
    print("[3]返回主菜单")
    print("请选择：")
    op = InputJudge(3)
    print("正在激活冰箱IceBox功能……")
    if op == 1:
        r = cmd(
            "adb shell dpm set-device-owner com.catchingnow.icebox/.receiverDPMReceiver")
    if op == '2':
        r = cmd(
            "adb shell sh /sdcard/Android/data/com.catchingnow.icebox/files/start.sh")
    if op == 3:
        Softmain()
    exit()


def IslandStart():
    print("炼妖壶激活工具，By：LZR@BUAA")
    print("正在激活炼妖壶设备管理员功能……")
    r = cmd(
        "adb shell dpm set-device-owner com.oasisfeng.island/.IslandDeviceAdminReceiver")


def BreventStart():
    print("黑域ADB激活工具，By：LZR@BUAA")
    print("正在激活黑阈Brevent功能……")
    r = cmd("adb -d shell sh /data/data/me.piebridge.brevent/brevent.sh")


def Softmain():
    print("########################################")
    print("")
    print("            软件安装激活工具")
    print("              By:LZR@BUAA")
    print("")
    print("########################################")
    cmd("adb disconnect")
    print("欢迎使用!\n请连接手机并开启USB调试模式")
    print("请选择：\n[1]软件安装工具\n[2]软件激活器\n[3]免Root系统软件卸载(慎用)\n[4]退出程序")
    op = InputJudge(4)
    if op == 1:
        installSoftware()
    elif op == 2:
        activeSofts()
    elif op == 3:
        Uninstall()
    elif op == 4:
        exitProgram(1)


if __name__ == "__main__":
    Softmain()
