# coding:utf-8
'''
Target: Python AndroidToolBox Fastboot Flash Module
Author: LZR@BUAA
Date:   08/26/2020
'''

from Methods import *

path = os.getcwd()


def directFlash(mode, file):
    print(cmd("fastboot flash "+mode+" "+file))


def fastbootWipe():
    cmd("fastboot erase userdata")
    cmd("fastboot erase cache")


def Flashmain():
    MobileInfo = getInfo()
    # os.system("COLOR A")
    os.system("cls")
    print("########################################")
    print("")
    print("                刷机工具")
    print("              By:LZR@BUAA")
    print("")
    print("########################################")
    print("欢迎使用!\n")
    os.system("cls")
    print("!!!!!!!!!!!!!!!!风险提示!!!!!!!!!!!!!!!!")
    print("不正确操作可能导致设备无法启动甚至损坏!\n作者对此不承担任何责任 请自行决定风险\n")
    print("+---------------刷机菜单---------------+")
    print("[1]卡刷(使用独立Zip/IMG安装)")
    print("[2]线刷(使用官方原版TAR安装)")
    print("[3]重启选项")
    print("[4]退出工具")
    cmd("adb disconnect")
    print("请选择-> ", end='')
    op = InputJudge(4)
    if op == 1:
        print("是否已经刷入第三方Recovery?(Y/N)")
        if InputJudge(2):
            if cmd("adb devices").find("recovery") == -1:
                input("准备重启到recovery模式,按Enter继续...")
                rebootRec()
            print("等待Recovery设备连接...")
            while True:
                if cmd("adb devices").find("recovery") != -1:
                    break
                time.sleep(2)
            input("请手动在 Recovery->高级选项 中开启\nADB Sideload / ADB线刷 功能 按Enter继续...")
            print("请选择"+MobileInfo['brand']+" " +
                  MobileInfo['model'] + " 的zip刷机文件")
            imagefile = filedialog.askopenfilenames(
                title='选择zip刷机文件', filetypes=[('zip卡刷包', '*.zip'), ])
            print("这是最后一次提示,确实要将\n"+imagefile[0].split("/")[-1]+"\n刷入" +
                  MobileInfo['brand']+" " + MobileInfo['model'] + "吗?(Y/N)")
            if InputJudge(2):
                # cmd("adb wipe ")
                messagebox.showinfo(
                    '若已知晓,点击\"确定\"继续', '如需跨版本或系统类型\n(如MIUI-->LineageOS等)\n请断开连接并在Recovery中进行双清\n否则系统可能无法启动\n')
                print("正在刷入 请在手机端查看相关信息...")
                cmd("adb sideload "+imagefile[0])
                exitProgram(0)
            else:
                exitProgram(1)
        else:
            print("是否要刷入第三方Recovery?(Y/N)")
            if InputJudge(2):
                print("请选择该机型的Recovery文件")
                recdir = filedialog.askopenfilenames(title='选择Recovery文件', filetypes=[
                                                     ('Recovery镜像', '*.img'), ])
                rebootBL()
                while True:
                    if BLConnected():
                        break
                directFlash("recovery", recdir[0])
                cmd("fastboot boot "+recdir[0])
            else:
                print("是否使用Fastboot模式进行刷机?(必须已解BL锁)(Y/N)")
                if InputJudge(2):
                    print("!!!!!!!!!!!!!!!!高风险功能警告!!!!!!!!!!!!!!!!")
                    print("警告!Fastboot刷机模式风险极高,请自行承担设备损坏等后果")
                    print("除非知道自己在做什么,否则请自行关闭程序!")
                    print("仍然要继续吗?(Y/N)")
                    if InputJudge(2):
                        rebootBL()
                        print("选择模式:\n[Y]批量刷入\n[N]逐个刷入")
                        if InputJudge(2):
                            print(
                                "请将.img或.bin格式刷机包放入打开的目录下")
                            os.startfile(".\\images\\FastbootImages")
                            input("不要修改文件名 按Enter继续")
                            IMG_list = os.listdir(
                                path+"\\images\\FastbootImages\\")
                            print("文件读取中...")
                            for img in IMG_list:
                                if os.path.splitext(img)[1] not in [".img", ".IMG", ".Img", ".bin", ".Bin", ".BIN"]:
                                    IMG_list.remove(img)
                            print("待刷入的文件列表:")
                            print(IMG_list)
                            print("请务必保持手机与电脑连接!\n最后一次确认,是否要刷入以上镜像?(Y/N)")
                            if InputJudge(2):
                                print("")
                                for img in IMG_list:
                                    print("正在刷入文件:"+img)
                                    directFlash(os.path.splitext(img)[
                                                0], path+"\\images\\FastbootImages\\"+img)
                                fastbootWipe()
                            else:
                                exitProgram(1)
                        else:
                            fdir = filedialog.askopenfilename(title="选择system.img位置", filetypes=[
                                                              ('system.img', '*.img'), ])
                            if fdir != []:
                                directFlash("system", fdir)

                            fdir = filedialog.askopenfilename(title="选择recovery.img位置", filetypes=[
                                                              ('recovery.img', '*.img'), ])
                            if fdir != []:
                                directFlash("recovery", fdir)

                            fdir = filedialog.askopenfilename(title="选择userdata.img位置", filetypes=[
                                                              ('userdata.img', '*.img'), ])
                            if fdir != []:
                                directFlash("userdata", fdir)

                            exitProgram(0)
                exitProgram(1)
    elif op == 2:
        rebootBL()
        print("正在重启到Fastboot,若进入失败请手动重启到Fastboot模式...")
        print("连接Fastboot中...")

        while True:
            if BLConnected():
                break
        print("Fastboot连接成功!")

        tardir = filedialog.askopenfilenames(title='选择Tar文件', filetypes=[
            ('TGZ压缩文件', '*.TGZ'), ])[0]
        imgdir = filedialog.askdirectory(title='选择刷机包解压目录')
        print("正在读取并解压压缩包,约30秒...请稍候")
        tm = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        unziptar(tardir, imgdir+"\\" + tm)
        tardir = os.listdir(imgdir+"\\" + tm)[0]
        print(
            "请选择工作模式:\n[1]全部擦写并清空数据\n[2]全部擦写但保留内部存储(\sdcard)\n[3]全部擦写并加BoolLoader锁(慎用)\n[4]退出程序")
        op = InputJudge(4)
        if op == 1:
            cmd(imgdir+"\\" + tm+"\\"+tardir+"\\flash_all.bat")
        elif op == 2:
            cmd(imgdir+"\\" + tm+"\\"+tardir+"\\flash_all_except_storage.bat")
        elif op == 3:
            cmd(imgdir+"\\" + tm+"\\"+tardir+"\\flash_all_lock.bat")
        elif op == 4:
            exitProgram(1)
        exitProgram(0)

    elif op == 3:
        rebootList()

    elif op == 4:
        exitProgram(1)


if __name__ == "__main__":
    Flashmain()
