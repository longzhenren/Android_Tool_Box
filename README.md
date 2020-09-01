# Android_Tool_Box
Android_Tool_Box
# Android Tool Box 开发文档

##提示：如需使用投屏控制功能，请下载[依赖](https://github.com/Genymobile/scrcpy/releases/download/v1.16/scrcpy-win64-v1.16.zip)并解压到程序目录！


## 一. 开发环境及工具

Windows10 2004 & Ubuntu 20.04 LTS(WSL) & Windows7 SP1

- VSCode with Python & C/C++ Extension
- Python 3.8 & Python 3.5
- Android SDK ToolKit
- 测试机型：Xiaomi Gemini (Mi5) & Redmi Raphael (K20 Pro) &Huawei ELE-AL00 (P30) & Redmi Nikel (Note4 MTK)
- MIUI（7，8，10，12）& AOSP & LineageOS 16（Nigthly） & EMUI10.1

## 二. 项目描述



## 三. 编写目的



现在的一键式刷机工具（如刷机精灵、线刷宝等）虽然能够提供简单易用的交互界面，但是存在不能保存配置以便批量刷机、刷机过程中植入广告程序和后门等缺陷；各大安卓论坛中提供的工具包分化过强，功能过于单一且与品牌、机型、版本等存在强绑定关系，无法做到工具的通用性；各厂家提供的刷机工具则高度定制化，无法修改部分预设，且各个厂家工具不互通，不能做到随心所欲；而直接调用Android SDK进行操作对于零编程基础的玩家更是非常不友好。

因此本项目结合作者八年的刷机经验，编写了基于Python的命令行程序，用户只需简单输入Y/N等操作就可以完成刷机流程，大大降低了刷机门槛，让每个用户都能充分体验到刷机的乐趣



## 四. 项目或功能背景

Android SDK 提供了相当丰富的扩展功能，基于ADB可以实现对系统底层的修改和配置，提高Android设备的可玩性。但是基于ADB的大多应用需要有较高的命令行操作和编程语言基础，对于希望深度优化安卓设备而缺乏相关经验的普通用户非常不友好。

本项目利用Python语言极强的扩展性，粘合了Linux Shell、Android Debug Bridge、

因此，本项目利用Python语言通过调用Shell脚本的方式实现了简易的交互式ADB界面，同时整合并重写部分优秀的开源安卓实用工具，自行编写了小米机型的全自动刷机工具（MTK和高通方案），以及基于Scrcpy的非华为设备多屏协同解决方案、



## 五. 模块与关系

1. ### ADBMethods.py	

   程序核心功能模块之一

   通过系统命令行调用ADBShell与设备进行各种交互

   后期可能用pyADB进行替换，便于高级调试

2. #### FastbootFlash.py

   刷机模块，提供线刷和卡刷功能

   需要调用ADBMethods和Sys

3. #### FileBackUp.py

   备份模块，可备份文件/系统

   提供Recovery模式整机镜像备份和文件备份功能

4. #### main.py

   程序主入口

   显示菜单并且按照用户操作调用各个模块的主方法

5. #### Run.c/Run.exe

   （有Bug，暂时废弃）C语言程序入口

   用于检测系统是否已经安装python环境，若无则自动安装

   pythoninstaller不可用时的临时解决方案

6. #### runincmd.bat

   powershell脚本，用于启动纯ADB/Fastboot命令行

7. #### Screen.py

   投屏模块

   调用Scrcpy项目，实现屏幕实时共享控制功能

8. #### SoftScript.py

   软件管理模块

   提供特殊软件激活、软件批量安装、软件管理等

9. #### SysMethods.py

   程序核心功能模块之一

   用于与系统Shell交互(调用命令行、获取系统路径等)

## 六. 功能和接口注释

1. ### ADBMethods.py	

   (*str*)当前连接设备的wlan0适配器的IP地址

   ##### IP = ""

   (*dict*)手机设备信息

   ##### MobileInfo = {}

   (*str*)Fastboot返回的设备连接信息 格式：SN \*t fastboot*

   ##### getFastbootConnection():

   (*bool*)有线连接状态，开启USB调试且处于正常开机状态返回True

   ##### USBConnected():

   (*bool*)BootLoader连接状态，处于Bootloader模式返回True

   ##### BLConnected():

   (*bool*)无线连接状态，远程调试已连接则返回True

   ##### WLANConnected():

   (null)重启到系统

   ##### rebootUI():

   (null)重启到Bootloader

   ##### rebootBL():

   (null)重启到Recovery

   ##### rebootRec():

   (*dict*)获取build.prop记载的手机详细信息

   ##### getInfo():

   (*bool*)获取Bootloader加锁状态

   ##### lockStatus():

   (*str*)获取电池电量

   ##### getBattery():

   (*str*)获取当前连接设备的wlan0适配器的IPV4地址

   ##### getIPaddress():

   (*bool*)获取设备开机状态

   ##### powerStatus():

   (null)传送sourcedir所指的文件或目录到设备rmpath目录下

   ##### pushFile(*sourcedir*, *rmpath*):

   (null)传送设备rmpath所指的文件或目录到本地destdir下

   ##### pullFile(*rmpath*, *destdir*):

   (null)将拖拽到窗口的文件传输到设备rmpath所指的目录下

   ##### dragtoPush(*rmpath*):

   (null)模拟点击坐标(x,y)

   ##### touchPoint(*x*, *y*):

   (null)模拟滑动,从(x1,y1)到(x2,y2)

   ##### slidePoint(*x1*, *y1*, *x2*, *y2*):

2. #### FastbootFlash.py

   (list)Tar线刷包列表

   ##### TAR = []

   (str)当前路径

   ##### path = os.getcwd()

   (list)当前路径下文件列表

   ##### list_dir = os.listdir(path+"\\images\\")

   (int)全局变量，tar个数

   ##### num_of_TARs = 0

   (null)寻找tar包并存入TAR[]

   ##### findTarPacks():

   (null)从fastboot重启到UI

   ##### fastbootReboot():

   (null)重启菜单

   ##### rebootList():

   (null)强制刷入指定文件 mode为设备目标分区，file为镜像文件

   ##### directFlash(*mode*, *file*):

   (null)双清

   ##### fastbootWipe():

   (null)主程序入口

   ##### Flashmain():

3. (null)

   findTarPacks():

4. #### FileBackUp.py

   

5. #### main.py

   (null)输出菜单

   ##### printmenu():

   (null)输出手机信息

   ##### printinfo():

   (null)输出欢迎界面和Logo

   ##### printHello():

   (null)输出关于我们

   ##### aboutProject():

   (null)主菜单模块

   ##### mainmenu():

   

6. #### Screen.py

   (str)当前路径

   ##### path = os.getcwd()

   (list)参数列表，格式如：["-m 1024","-f",...]

   ##### conf = []

   (str)全局变量 参数字符串

   ##### config = ''

   (null)配置存取模块，调用外部Scrcpy-Settings.txt存取配置字符串

   ##### initializeConfig():

   (str)参数生成模块，生成config字符串

   ##### configGenerator():

   (null)以有线连接方式启动，传入config字符串

   ##### USBconnect(config):

   (null)以无线连接(远程调试)方式启动，参数同USBconnect

   ##### WLANconnect(config):

   (null)主程序入口，可从外部调用

   ##### Screenmain()：

7. #### SoftScript.py

   (list)当前目录APK列表

   ##### Apklist = []

   (str)当前路径

   ##### path = os.getcwd()

   (list)当前目录文件列表

   ##### list_dir = os.listdir(path+"\\ApkFiles\\")

   (int)全局变量，APK数量

   ##### num_of_APKs = 0

   (null)免root卸载软件 参数为apk包名

   ##### unInstallwithoutRoot(*PackageName*):

   (list)返回目录下APK列表

   ##### listAPKFiles():

   (null)格式化输出文件列表

   ##### printAPKList(*num*):

   (bool)是否存在指定文件

   ##### inAPKList(*APKname*):

   (bool)询问是否安装

   ##### askforInst(*APKname*):

   (null)安装应用

   ##### pushApp(*APKname*):

   (null)软件安装子程序入口

   ##### installSoftware():

   (null)软件激活子程序入口

   ##### activeSofts():

   (null)冰箱激活组件

   ##### IceboxStart():

   (null)炼妖壶启动组件

   ##### IslandStart():

   (null)黑阈启动组件

   ##### BreventStart():

   (null)主程序入口

   ##### Softmain():

8. #### SysMethods.py

   (str)建立管道，调用系统命令行执行command并返回stdout内容

   ##### cmd(*command*):

   (null)解压tar压缩文件，参数分别为文件名和解压路径

   ##### unziptar(*filename*, *dirs*):

   (bool/int)选项输入限定，非法选项要求重新输入，参数为选项个数

   ##### InputJudge(*num*):

   (弃用)(null)清屏并启动新的python文件

   ##### NewProgram(*pyFileName*):

   (str)引导文件拖拽并获取文件绝对路径，返回文件绝对路径

   ##### dragtoWindowGetName():

   (null)程序出口引导

   ##### exitProgram(*num*):

## 七. 参考资料

## 八. 项目进度预估

## 十五. 性能分析与优化
# Android 手机实用工具集(BUAA1921小学期作业)

## 零、总体构思

建立基于python语言的集成常用解锁、刷机、软件预装、投屏、优化和其他实用功能的一站式平台，提供Windows/Android端支持

若有精力尽量开发GUI

## 一、功能设计

### 1.各大厂商解锁工具和教程提供

### 2.Fastboot刷机实用工具

#### 	Recovery刷入

#### 	系统刷入（卡刷）

### 3.ADB相关工具

#### 	软件预装

#### 	Root权限获取

### 4.线刷工具和使用教程（争取静默操作或者提供引导教程等）

### 5.高速文件传输（无线FTP协议加有线MTP协议）

#### 	FTP协议软件包

#### 	MTP协议控制

### 6.屏幕投射（基于Scrcpy修改）

#### 	本体

#### 	操作控件和快捷键映射

### 7.系统优化和软件自动化配置

#### 	绿色守护

#### 	黑域

#### 	太极/面具等

#### 	La系统工具箱

#### 	冰箱icebox

### 8.资源下载地址整合（各机型刷机包）

#### 	各大论坛收集魔改版

#### 	原版尽量找



## 二、使用技术

### 1.python调用系统命令行

### 2.ADB、FastBoot、Recovery操作（命令行）

#### 	ADB操作：推送APP、Scrcpy交互、刷入Recovery

#### 	FastBoot&Recovery操作：命令行推送&刷入刷机包、刷入功能组件（可集成）

### 3.MTP、FTP、Samba、NFS等协议（python库）

#### 	文件传输相关指令，可以配合APP客户端使用（类似于快传）

### 4.Android Shell简单使用和各个优化软件的启动脚本优化

#### 	查阅相关软件开发者提供的接口说明文档

