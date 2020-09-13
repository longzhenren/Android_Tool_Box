import locale
import subprocess
import tkinter
from ftplib import FTP

from main import *
from Methods import *

# from FastbootFlash import directFlash
# from tkinter import IntVar

wechatimage = "/sdcard/tencent/MicroMsg/WeiXin"
wechatfiles = "/sdcard/Android/data/com.tencent.mm/MicroMsg/Download/"
qqimage = "/sdcard/tencent/qq_images"
qqfiles = "/sdcard/Android/data/com.tencent.mobileqq/Tencent/QQfile_recv/"


Update = Tk()
Update.withdraw()
FTPlist = []
ADBlist = []
# Selectlist = []
IP = ""
path = os.getcwd()
ftp = FTP()
rmpath = "/AndroidToolBox/"


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
    ADBlist.clear()
    FTPlist.clear()
    lenl = len(list)
    # if lenl == 0:
    # messagebox.showwarning("错误","未选择文件!")
    # print("列表空!")
    # sys.exitProgram(2)
    for i in range(lenl // 2):
        FTPlist.append(list[i])
    for i in range((lenl // 2) + 1, lenl):
        ADBlist.append(list[i])


def ADBUP():
    for i in ADBlist:
        command = "adb push \""+i+"\" /sdcard"+rmpath+i.split("/")[-1]
        os.popen(command)


def FTPUP():
    global ftp
    for i in FTPlist:
        uploadfile(ftp, i.split("/")[-1], i)


def GUIInfo():
    if USBConnected():
        MobileInfo = getInfo()
        info = "+----------设备信息----------+"+"\n设备型号:\t"+MobileInfo['model']+"\n制造商:\t\t"+MobileInfo['brand'] + \
            "\n安卓版本:\t" + \
            MobileInfo['android']+"(API"+MobileInfo['API']+")" + \
            "\n剩余电量:\t"+MobileInfo['battery']
    else:
        info = "设备未连接,请检查连接状态!"
        # return
    INFOGUI = tkinter.Tk()
    INFOGUI.title("设备信息")
    INFOGUI.resizable(0, 0)
    label = tkinter.Label(INFOGUI, text=info, font=(
        "Consolas", 12), anchor="center", justify="left", bg="black", fg="green").grid()
    tkinter.Button(INFOGUI, text="返回", font=("Microsoft YaHei", 12),
                   width=10, height=1, command=INFOGUI.destroy).grid()
    INFOGUI.mainloop()


def GUIAbout():
    os.startfile(os.getcwd()+"//README.html")
    # ABGUI = tkinter.Tk()
    # ABGUI.title("关于")
    # about = tkinter.Label(ABGUI,)


# def GUIBackWXQQ():
#     backupdir = filedialog.askdirectory(title='选择备份目录')
#     tm = time.strftime("%Y%m%d_%H%M%S", time.localtime())
#     if not os.path.exists(backupdir+"/Filebackup/"):
#         os.mkdir(backupdir+"/Filebackup/")
#     os.mkdir(backupdir+"/Filebackup/"+tm+"/")
#     BPT = tkinter.Tk()
#     BPT.title("微信/QQ文件备份")
#     option = tkinter.IntVar()
#     option.set(1)


def ptbk(op,BAGUI):
    backupdir = filedialog.askdirectory(title='选择备份目录')
    # print(type(backupdir))
    if backupdir == "":
        messagebox.showwarning("错误", "选择的目录无效")
        BAGUI.title("备份工具")
        return
    tm = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    if not os.path.exists(backupdir+"/backup/"):
        os.mkdir(backupdir+"/backup/")
    os.mkdir(backupdir+"/backup/"+tm)
    # print("1")
    if op == 1:
        os.mkdir(backupdir+"/backup/"+tm+"/Images/")
        BAGUI.title("备份中,请勿关闭程序")
        if pullFile("/sdcard/DCIM/", "\""+backupdir+"/backup/"+tm+"/Images/\"").find("devices/emulators") != -1:
            messagebox.showerror("错误", "设备未连接!")
            BAGUI.title("备份工具")
            return
        else:
            messagebox.showinfo("提示", "备份成功!")
    elif op == 2:
        os.mkdir(backupdir+"/backup/"+tm+"/Camera/")
        BAGUI.title("备份中,请勿关闭程序")
        if pullFile("/sdcard/DCIM/Camera/", "\""+backupdir+"/backup/"+tm+"/Camera/\"").find("devices/emulators") != -1:
            messagebox.showerror("错误", "设备未连接!")
            BAGUI.title("备份工具")    
            return
        else:
            messagebox.showinfo("提示", "备份成功!")
    elif op == 3:
        BAGUI.title("备份中,请勿关闭程序")
        if cmd("adb shell pm list package").find("com.tencent.mobileqq") == -1:
            messagebox.showwarning("错误", "QQ未安装")
            BAGUI.title("备份工具")
            return
        os.mkdir(backupdir+"/backup/"+tm+"/QQBackup/")
        os.mkdir(backupdir+"/backup/"+tm+"/QQBackup/image/")
        if pullFile(qqimage, "\""+backupdir+"/backup/"+tm+"/QQBackup/image/\"").find("devices/emulators") != -1:
            messagebox.showerror("错误", "设备未连接!")
            BAGUI.title("备份工具")
            return
        else:
            messagebox.showinfo("提示", "备份成功!")
    elif op == 4:
        BAGUI.title("备份中,请勿关闭程序")
        if cmd("adb shell pm list package").find("com.tencent.mobileqq") == -1:
            messagebox.showwarning("错误", "QQ未安装")
            BAGUI.title("备份工具")
            return
        os.mkdir(backupdir+"/backup/"+tm+"/QQBackup/")
        os.mkdir(backupdir+"/backup/"+tm+"/QQBackup/files/")
        if pullFile(qqfiles, "\""+backupdir+"/backup/"+tm+"/QQBackup/files/\"").find("devices/emulators") != -1:
            messagebox.showerror("错误", "设备未连接!")
            BAGUI.title("备份工具")
            return
        else:
            messagebox.showinfo("提示", "备份成功!")
    elif op == 5:
        BAGUI.title("备份中,请勿关闭程序")
        if cmd("adb shell pm list package").find("com.tencent.mm") == -1:
            messagebox.showwarning("错误", "微信未安装")
            BAGUI.title("备份工具")
            return
        os.mkdir(backupdir+"/backup/"+tm+"/WXBackup/")
        os.mkdir(backupdir+"/backup/"+tm+"/WXBackup/image/")
        if pullFile(wechatimage, "\""+backupdir+"/backup/"+tm+"/WXBackup/image/\"").find("devices/emulators") != -1:
            messagebox.showerror("错误", "设备未连接!")
            BAGUI.title("备份工具")
            return
        else:
            messagebox.showinfo("提示", "备份成功!")
    elif op == 6:
        BAGUI.title("备份中,请勿关闭程序")
        if cmd("adb shell pm list package").find("com.tencent.mm") == -1:
            messagebox.showwarning("错误", "微信未安装")
            BAGUI.title("备份工具")
            return
        os.mkdir(backupdir+"/backup/"+tm+"/WXBackup/")
        os.mkdir(backupdir+"/backup/"+tm+"/WXBackup/files/")
        if pullFile(wechatfiles, "\""+backupdir+"/backup/"+tm+"/WXBackup/files/\"").find("devices/emulators") != -1:
            messagebox.showerror("错误", "设备未连接!")
            BAGUI.title("备份工具")
            return
        else:
            BAGUI.title("备份工具")
            messagebox.showinfo("提示", "备份成功!")
            


def GUIBack():
    BAGUI = tkinter.Tk()
    BAGUI.title("备份工具")
    BAGUI.resizable(0, 0)
    tkinter.Button(BAGUI, text="备份系统图库", command=lambda: ptbk(1,BAGUI), font=("Microsoft YaHei", 12)
                   ).grid(row=1, column=0, sticky="EW", ipadx=10, ipady=5, padx=20, pady=10)
    tkinter.Button(BAGUI, text="备份相机胶卷", command=lambda: ptbk(2,BAGUI), font=("Microsoft YaHei", 12)
                   ).grid(row=1, column=1, sticky="EW", ipadx=10, ipady=5, padx=20, pady=10)
    tkinter.Button(BAGUI, text="备份QQ相册", command=lambda: ptbk(3,BAGUI), font=("Microsoft YaHei", 12)
                   ).grid(row=2, column=0, sticky="EW", ipadx=10, ipady=5, padx=20, pady=10)
    tkinter.Button(BAGUI, text="备份QQ文件", command=lambda: ptbk(4,BAGUI), font=("Microsoft YaHei", 12)
                   ).grid(row=2, column=1, sticky="EW", ipadx=10, ipady=5, padx=20, pady=10)
    tkinter.Button(BAGUI, text="备份微信相册", command=lambda: ptbk(5,BAGUI), font=("Microsoft YaHei", 12)
                   ).grid(row=3, column=0, sticky="EW", ipadx=10, ipady=5, padx=20, pady=10)
    tkinter.Button(BAGUI, text="备份微信文件", command=lambda: ptbk(6,BAGUI), font=("Microsoft YaHei", 12)
                   ).grid(row=3, column=1, sticky="EW", ipadx=10, ipady=5, padx=20, pady=10)
    BAGUI.mainloop()


def GUICmd():
    os.startfile("AndroidToolBox_CommandMode.exe")
    # os.startfile("runincmd.bat")


def flsh(op):
    MobileInfo = getInfo()
    if op == 1:
        if USBConnected():
            if cmd("adb devices").find("recovery") == -1:
                if messagebox.askyesno("提示", "是否重启到recovery模式?"):
                    rebootRec()
                else:
                    return
            while True:
                if cmd("adb devices").find("recovery") != -1:
                    break
            messagebox.showinfo(
                "提示", "请手动在 Recovery->高级选项 中开启\nADB Sideload / ADB线刷 功能")
            imagefile = filedialog.askopenfilenames(
                title='选择zip刷机文件', filetypes=[('zip卡刷包', '*.zip'), ])
            if messagebox.askyesno("最后一次确认", "确实要将\n"+imagefile[0].split("/")[-1]+"\n刷入" + MobileInfo['brand']+" " + MobileInfo['model'] + "吗?"):
                cmd("adb sideload "+imagefile[0])
            messagebox.showinfo(
                '若已知晓,点击\"确定\"继续', '如需跨版本或系统类型\n(如MIUI-->LineageOS等)\n请断开连接并在Recovery中进行双清\n否则系统可能无法启动\n')
    elif op == 3:
        recdir = filedialog.askopenfilenames(title='选择Recovery文件', filetypes=[
                                             ('Recovery镜像', '*.img'), ])
        if messagebox.askyesno("请选择", "是否要刷入第三方Recovery?"):
            directFlash("recovery", recdir[0])
            cmd("fastboot boot "+recdir[0])
        messagebox.showinfo("提示", "Recovery刷入完成\n请在手机端查看")
    elif op == 2:
        if messagebox.askyesno("警告", "错误使用Fastboot刷机可能导致设备损坏和失去保修\n确定要继续吗?"):
            rebootBL()
        else:
            return
        while True:
            if BLConnected():
                break
        tardir = filedialog.askopenfilenames(title='选择Tar文件', filetypes=[
                                             ('TGZ压缩文件', '*.TGZ'), ])[0]
        imgdir = filedialog.askdirectory(title='选择刷机包解压目录')
        tm = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        unziptar(tardir, imgdir+"\\" + tm)
        tardir = os.listdir(imgdir+"\\" + tm)[0]
        if messagebox.askyesno("请选择", "是否加BL锁?"):
            cmd(imgdir+"\\" + tm+"\\"+tardir+"\\flash_all_lock.bat")
        if messagebox.askyesno("请选择", "是否清除SD卡数据?"):
            cmd(imgdir+"\\" + tm+"\\"+tardir+"\\flash_all.bat")
        else:
            cmd(imgdir+"\\" + tm+"\\"+tardir+"\\flash_all_except_storage.bat")
        messagebox.showinfo("提示", "刷入成功,设备正在重启...")


def GUIFlash():
    messagebox.showwarning("警告", "不正确操作可能导致设备无法启动甚至损坏!\n作者对此不承担任何责任 请自行决定风险")
    FLGUI = tkinter.Tk()
    FLGUI.title("刷机工具")
    FLGUI.resizable(0, 0)
    if cmd("adb disconnect").find("devices/emulators") != -1:
        messagebox.showerror("错误", "设备未连接!")
    tkinter.Button(FLGUI, text="卡刷", command=lambda: flsh(1), font=("Microsoft YaHei", 12)
                   ).grid(row=1, column=0, sticky="EW", ipadx=30, ipady=5, padx=40, pady=10)
    tkinter.Button(FLGUI, text="线刷", command=lambda: flsh(2), font=("Microsoft YaHei", 12)
                   ).grid(row=2, column=0, sticky="EW", ipadx=30, ipady=5, padx=40, pady=10)
    tkinter.Button(FLGUI, text="刷入Recovery", command=lambda: flsh(3), font=("Microsoft YaHei", 12)).grid(
        row=1, column=1, sticky="EW", ipadx=30, ipady=5, padx=40, pady=10)
    tkinter.Button(FLGUI, text="重启选项", command=GUIReboot, font=("Microsoft YaHei", 12)).grid(
        row=2, column=1, sticky="EW", ipadx=30, ipady=5, padx=40, pady=10)
    FLGUI.mainloop()


def GUIReboot():
    RBGUI = tkinter.Tk()
    RBGUI.title("重启选项")
    RBGUI.resizable(0, 0)
    tkinter.Button(RBGUI, text="重启到Bootloader", command=rebootBL, font=("Microsoft YaHei", 12)).grid(
        row=1, column=0, sticky="EW", ipadx=30, ipady=5, padx=40, pady=10)
    tkinter.Button(RBGUI, text="重启到Recovery", command=rebootRec, font=("Microsoft YaHei", 12)).grid(
        row=2, column=0, sticky="EW", ipadx=30, ipady=5, padx=40, pady=10)
    tkinter.Button(RBGUI, text="重启到系统", command=rebootUI, font=("Microsoft YaHei", 12)).grid(
        row=3, column=0, sticky="EW", ipadx=30, ipady=5, padx=40, pady=10)
    RBGUI.mainloop()


def ts(op):
    if op == 1:
        cur = filedialog.askopenfilenames(title="请选择要上传的文件")
        if cur == []:
            messagebox.showwarning("错误", "未选择文件!")
            return
        divide(cur)
        Thread1 = threading.Thread(target=ADBUP)
        Thread2 = threading.Thread(target=FTPUP)
        Thread1.start()
        Thread2.start()
    elif op == 2:
        # messagebox.showinfo("映射成功!", "请在打开的窗口中直接进行文件操作")
        os.system("explorer ftp://LZR:BUAA21@"+IP+":1921")


def StartFTP(IP, Port, User, Pass):
    # print("启动FTP服务中……")
    ftp.set_debuglevel(0)
    ftp.connect(IP, Port)
    ftp.login(User, Pass)
    ftp.set_pasv(False)
    ftp.encoding = "utf-8"
    # print(ftp.getwelcome())
    if "AndroidToolBox" not in ftp.nlst():
        ftp.mkd("/AndroidToolBox/")
    ftppath = "AndroidToolBox"
    ftp.cwd(ftppath)


def GUITrans():
    TSGUI = tkinter.Tk()
    fport = 1921
    fuser = "LZR"
    fpass = "BUAA21"
    TSGUI.title("文件快传")
    TSGUI.resizable(0, 0)
    cmd("adb disconnect")
    if cmd("adb shell pm list package").find("com.my.ftpdemo") == -1:
        if cmd("adb install FtpClient.apk").find("Success"):
            pass
    cmd("adb shell am start com.my.ftpdemo/.MainActivity")
    tkinter.Button(TSGUI, text="文件快传", command=lambda: ts(1), font=("Microsoft YaHei", 12)).grid(
        row=1, column=0, sticky="EW", ipadx=10, ipady=5, padx=20, pady=10)
    tkinter.Button(TSGUI, text="在资源管理器中打开FTP目录", command=lambda: ts(2), font=("Microsoft YaHei", 12)).grid(
        row=2, column=0, sticky="EW", ipadx=10, ipady=5, padx=20, pady=10)
    messagebox.showinfo("提示", "请在手机端授权管理开启FTPClient的读写存储权限\n并保持程序处于前台")
    StartFTP(IP, fport, fuser, fpass)
    TSGUI.mainloop()


def gls(utxt):
    # global glsc
    lst = utxt.get().split(",")
    for i in lst:
        cmd("adb shell pm uninstall -k --user 0 " + i)
        messagebox.showinfo("提示",i+"卸载成功!")
    # glsc = utxt.get()
    # print(glsc)


def avs(op):
    if op == 1:
        r = cmd(
            "adb shell dpm set-device-owner com.catchingnow.icebox/.receiverDPMReceiver")
    elif op == 2:
        r = cmd(
            "adb shell sh /sdcard/Android/data/com.catchingnow.icebox/files/start.sh")
    elif op == 3:
        r = cmd(
            "adb shell dpm set-device-owner com.oasisfeng.island/.IslandDeviceAdminReceiver")
    elif op == 4:
        r = cmd("adb -d shell sh /data/data/me.piebridge.brevent/brevent.sh")


def sfop(op):
    if op == 1:
        fdir = filedialog.askopenfilenames(
            title='选择APK文件', filetypes=[('APK安装包', '*.apk'), ])
        if fdir == []:
            messagebox.showerror("错误", "未选择安装包或选择的不是有效的安装文件!")
        for app in fdir:
            if messagebox.askyesno("请选择", "是否要安装"+app.split("/")[-1]+"?"):
                if USBConnected():
                    if cmd("adb install " + app.split("/")[-1]).find("Success") != -1:
                        messagebox.showinfo("提示", app.split("/")[-1]+"安装成功!")
                    else:
                        messagebox.showwarning(
                            "警告", app.split("/")[-1]+"安装失败!")
                else:
                    messagebox.showerror("错误", "设备未连接!")
    elif op == 2:
        # global glsc
        messagebox.showwarning("警告", "请勿卸载系统关键组件\n请在打开的App列表中找到并复制要卸载的包名\n多个包名之间用英文逗号隔开")
        applist = cmd("adb shell pm list package -f")
        tm = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        fp = open("PackageList_"+tm+".txt", "w")
        fp.write(applist)
        os.startfile(os.getcwd()+"/"+"PackageList_"+tm+".txt")
        tmpwin = tkinter.Tk()
        tkinter.Label(tmpwin,text = "请输入要卸载的软件包名,多个软件请用分号隔开").grid(row = 0,column = 0 ,sticky = "EW")
        tmpwin.title("免Root软件卸载")
        
        utext = tkinter.Entry(tmpwin)
        utext.grid(row=1, column=0, sticky="EW")
        tkinter.Button(tmpwin, text="卸载", command=lambda: gls(utext)).grid(row=2, column=0, sticky="EW")
        # text = utext.get()
        # print(glsc)
        tmpwin.mainloop()
    elif op == 3:
        backupdir = filedialog.askdirectory(title='选择备份目录')
        if backupdir == "":
            messagebox.showwarning("错误","选择的目录无效")
            return
        messagebox.showinfo("提示", "请在手机端点击以确认备份")
        tm = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        cmd("adb backup -apk -all -f "+backupdir+"/"+tm+".ab")
    elif op == 4:
        abdir = filedialog.askopenfilename(
            title="选择备份的.ab文件位置", filetypes=[('备份文件', '*.ab'), ])
        if abdir == []:
            messagebox.showwarning("错误","选择的文件无效")
        messagebox.showinfo("提示", "是否要还原"+abdir[0]+"?\n请在手机端确认")
        cmd("adb restore "+abdir)
    elif op == 5:
        tmpwin1 = tkinter.Tk()
        tmpwin1.title("软件激活工具")
        tkinter.Button(tmpwin1, text="冰箱Icebox激活(设备管理员)",
                       command=lambda: avs(1)).grid(row=1, column=0, sticky="EW")
        tkinter.Button(tmpwin1, text="冰箱Icebox激活(普通模式)", command=lambda: avs(2)).grid(
            row=2, column=0, sticky="EW")
        tkinter.Button(tmpwin1, text="炼妖壶Island激活(设备管理员)",
                       command=lambda: avs(3)).grid(row=3, column=0, sticky="EW")
        tkinter.Button(tmpwin1, text="黑阈Brevent原版激活(无补丁)",
                       command=lambda: avs(4)).grid(row=4, column=0, sticky="EW")
        tmpwin1.mainloop()


def GUISoft():
    SFGUI = tkinter.Tk()
    SFGUI.title("软件工具")
    SFGUI.resizable(0, 0)
    tkinter.Button(SFGUI, text="软件安装", command=lambda: sfop(1), font=("Microsoft YaHei", 12)
                   ).grid(row=1, column=0, sticky="EW", ipadx=10, ipady=5, padx=20, pady=10)
    tkinter.Button(SFGUI, text="软件卸载", command=lambda: sfop(2), font=("Microsoft YaHei", 12)
                   ).grid(row=1, column=1, sticky="EW", ipadx=10, ipady=5, padx=20, pady=10)
    tkinter.Button(SFGUI, text="软件备份", command=lambda: sfop(3), font=("Microsoft YaHei", 12)
                   ).grid(row=2, column=0, sticky="EW", ipadx=10, ipady=5, padx=20, pady=10)
    tkinter.Button(SFGUI, text="软件还原", command=lambda: sfop(4), font=("Microsoft YaHei", 12)
                   ).grid(row=2, column=1, sticky="EW", ipadx=10, ipady=5, padx=20, pady=10)
    tkinter.Button(SFGUI, text="软件激活", command=lambda: sfop(5), font=("Microsoft YaHei", 12)).grid(
        row=3, column=0, sticky="EW", ipadx=10, ipady=5, padx=20, pady=10)
    tkinter.Button(SFGUI, text="退出工具", command=SFGUI.destroy, font=("Microsoft YaHei", 12)).grid(
        row=3, column=1, sticky="EW", ipadx=10, ipady=5, padx=20, pady=10)

    SFGUI.mainloop()


bit = 2
pix = 0
sts = [0, 0, 0, 0, 0, 0, 0, 0, 0]


def GUIScreen():
    global bit
    global pix
    SCRGUI = tkinter.Tk()
    SCRGUI.title("投屏控制")
    SCRGUI.resizable(0, 0)

    def oper(mode, val):
        global bit
        global pix
        if mode == "bit":
            if bit == val:
                bit = 0
            else:
                bit = val
        if mode == "pix":
            if pix == val:
                pix = 0
        else:
            pix = val
        if mode == "sts":
            if sts[val] == 1:
                sts[val] = 0
            else:
                sts[val] = 1

    # Oplist = ['无边框窗口', '全屏窗口', '置顶窗口', '关闭屏幕', '显示触摸', '启用屏幕录制']
    tkinter.Label(SCRGUI, text="比特率设定", anchor="center", font=("Microsoft YaHei", 12)).grid(
        row=0, column=1, sticky="WE")
    tkinter.Label(SCRGUI, text="分辨率设定", anchor="center", font=("Microsoft YaHei", 12)).grid(
        row=0, column=2, sticky="WE")
    tkinter.Label(SCRGUI, text="基本设置", anchor="center", font=("Microsoft YaHei", 12)).grid(
        row=0, column=3, columnspan=2, sticky="WE")
    tkinter.Button(SCRGUI, text="默认", command=lambda: oper(
        "pix", 0), font=("Microsoft YaHei", 12)).grid(row=1, column=2, sticky="WE", ipadx=30, ipady=5, padx=10)
    tkinter.Button(SCRGUI, text="1920", command=lambda: oper(
        "pix", 1), font=("Microsoft YaHei", 12)).grid(row=2, column=2, sticky="WE", ipadx=30, ipady=5, padx=10)
    tkinter.Button(SCRGUI, text="1080", command=lambda: oper(
        "pix", 2), font=("Microsoft YaHei", 12)).grid(row=3, column=2, sticky="WE", ipadx=30, ipady=5, padx=10)
    tkinter.Button(SCRGUI, text="720", command=lambda: oper(
        "pix", 3), font=("Microsoft YaHei", 12)).grid(row=4, column=2, sticky="WE", ipadx=30, ipady=5, padx=10)
    # tkinter.Button(SCRGUI, text="清除设置", command=lambda: oper(
    # pix, 4)).grid(row=5, column=2,sticky = "WE")

    tkinter.Button(SCRGUI, text="20Mbps", command=lambda: oper(
        "bit", 0), font=("Microsoft YaHei", 12)).grid(row=1, column=1, sticky="WE", ipadx=30, ipady=5, padx=10)
    tkinter.Button(SCRGUI, text="10Mbps", command=lambda: oper(
        "bit", 1), font=("Microsoft YaHei", 12)).grid(row=2, column=1, sticky="WE", ipadx=30, ipady=5, padx=10)
    tkinter.Button(SCRGUI, text="8Mbps", command=lambda: oper(
        "bit", 2), font=("Microsoft YaHei", 12)).grid(row=3, column=1, sticky="WE", ipadx=30, ipady=5, padx=10)
    tkinter.Button(SCRGUI, text="4Mbps", command=lambda: oper(
        "bit", 3), font=("Microsoft YaHei", 12)).grid(row=4, column=1, sticky="WE", ipadx=30, ipady=5, padx=10)
    tkinter.Button(SCRGUI, text="2Mbps", command=lambda: oper(
        "bit", 4), font=("Microsoft YaHei", 12)).grid(row=5, column=1, sticky="WE", ipadx=30, ipady=5, padx=10)
    # tkinter.Button(SCRGUI, text="清除设置", command=lambda: oper(
    # bit, 5)).grid(row=6, column=2,sticky = "WE")
    # tkinter.Button(SCRGUI, text="清除设置", command=lambda: oper(
    #     pix, 4)).grid(row=5, column=2)

    tkinter.Button(SCRGUI, text="无边框窗口", command=lambda: oper(
        "sts", 0), font=("Microsoft YaHei", 12)).grid(row=1, column=3, sticky="WE", ipadx=30, ipady=5, padx=10)
    tkinter.Button(SCRGUI, text="全屏窗口", command=lambda: oper(
        "sts", 1), font=("Microsoft YaHei", 12)).grid(row=2, column=3, sticky="WE", ipadx=30, ipady=5, padx=10)
    tkinter.Button(SCRGUI, text="置顶窗口", command=lambda: oper(
        "sts", 2), font=("Microsoft YaHei", 12)).grid(row=3, column=3, sticky="WE", ipadx=30, ipady=5, padx=10)
    tkinter.Button(SCRGUI, text="关闭屏幕", command=lambda: oper(
        "sts", 3), font=("Microsoft YaHei", 12)).grid(row=1, column=4, sticky="WE", ipadx=30, ipady=5, padx=10)
    tkinter.Button(SCRGUI, text="显示触摸", command=lambda: oper(
        "sts", 4), font=("Microsoft YaHei", 12)).grid(row=2, column=4, sticky="WE", ipadx=30, ipady=5, padx=10)
    tkinter.Button(SCRGUI, text="启用屏幕录制", command=lambda: oper("sts", 5), font=("Microsoft YaHei", 12)).grid(
        row=3, column=4, sticky="WE", ipadx=30, ipady=5, padx=10)

    tkinter.Button(SCRGUI, text="有线启动", command=lambda: startscr(1), font=("Microsoft YaHei", 12)).grid(
        row=7, column=1, columnspan=2, sticky="WE", ipadx=30, ipady=5, padx=10)
    tkinter.Button(SCRGUI, text="无线启动", command=lambda: startscr(2), font=("Microsoft YaHei", 12)).grid(
        row=7, column=3, columnspan=2, sticky="WE", ipadx=30, ipady=5, padx=10)
    SCRGUI.mainloop()
    if sts[5] == 1:
        messagebox.showinfo("录制文件已保存到当前用户目录下!")


def startscr(op):
    global pix
    global bit
    config = ""
    conf = ["scrcpy", ""]
    print(sts)
    if sts[0] == 1:
        conf.append("--window-borderless")
    if sts[1] == 1:
        conf.append("--fullscreen")
    if sts[2] == 1:
        conf.append("--always-on-top")
    if sts[3] == 1:
        conf.append("--turn-screen-off")
    if sts[4] == 1:
        conf.append("--show-touches")
    if sts[5] == 1:
        conf.append("--record")
        tm = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        conf.append("\""+os.path.expanduser('~') +
                    "\\ScreenRecord" + tm + ".mp4\"")
    if bit == 0:
        conf.append("--bit-rate 20M")
    elif bit == 1:
        conf.append("--bit-rate 10M")
    elif bit == 2:
        conf.append("--bit-rate 8M")
    elif bit == 3:
        conf.append("--bit-rate 4M")
    elif bit == 4:
        conf.append("--bit-rate 2M")
    if pix == 1:
        conf.append("--max-size 1920")
    elif pix == 2:
        conf.append("--max-size 1080")
    elif pix == 3:
        conf.append("--max-size 720")
    # print(conf)
    config = ' '.join(conf)
    print(config)
    if op == 2:
        IP = getIPaddress()
        if cmd("adb tcpip 5555").find("error") == -1:
            messagebox.showinfo("提示", "现在可以断开手机与电脑连接")
        if cmd("adb connect " + IP).find("unable") == -1:
            os.system(config)
        else:
            messagebox.showwarning("错误", "设备连接失败!")
    else:
        os.system(config)


if __name__ == "__main__":
    messagebox.showinfo("欢迎使用!", "请用USB数据线连接安卓设备和电脑\n在设备上开启USB调试和USB安装")
    mainwindow = tkinter.Tk()
    cmd("adb disconnect")
    MobileInfo = getInfo()
    if not USBConnected():
        mainwindow.title('【设备未连接】Android ToolBox BUAA-LZR')
    else:
        mainwindow.title(
            '【' + MobileInfo['model']+'已连接】Android ToolBox BUAA-LZR')
    mainwindow.resizable(0, 0)
    # mainwindow.geometry('300x350')
    mianlist = ['设备信息', '投屏工具', '刷机工具', '文件快传',
                '备份还原', '软件工具', '高级重启', '关于项目', '命令模式', '退出程序']
    cmdlist = ['GUIInfo', 'GUIScreen', 'GUIFlash', 'GUITrans',
               'GUIBack', 'GUISoft', 'GUIReboot', 'GUIAbout', 'GUICmd', 'sys.exit']
    for i in range(len(mianlist)):
        tkinter.Button(mainwindow, text=mianlist[i], font=(
            "Microsoft YaHei", 12), height=1, command=eval(cmdlist[i])).grid(row=i//2, column=i % 2, sticky="EW", ipadx=50, ipady=5, padx=10, pady=5)
    mainwindow.mainloop()
