@echo off
title adb和fastbooot 工具    --by wzsx150

echo.          adb和fastbooot 工具
echo.-----------------------------------------
echo.         adb和fastboot命令示例
echo. adb命令：
echo.	adb devices		:列出adb设备
echo.	adb reboot		:重启设备
echo.	adb reboot bootloader	:重启到fastboot模式
echo.	adb reboot recovery	:重启到recovery模式
echo.	adb reboot edl		:重启到edl模式
echo.
echo. fastboot命令：
echo.	fastboot devices			:列出fastboot设备
echo.	fastboot reboot				:重启设备
echo.	fastboot reboot-bootloader		:重启到fastboot模式
echo.	fastboot flash ^<分区名称^> ^<镜像文件名^>	:刷写分区
echo.	fastboot oem reboot-^<模式名称^> 		:重启到相应模式
echo.	fastboot oem device-info 		:查看解锁状态
echo.-----------------------------------------
echo. 请输入adb或者fastboot命令：
echo. 
cmd /k