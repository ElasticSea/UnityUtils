import os
import re
import subprocess


# Adb connects to device through tcp/ip
def connect_tcpip(ip, port):
    os.system("adb tcpip " + port)
    os.system("adb connect " + ip)
    os.system("adb devices")


# Installs apk on the device uninstalls previous version and removes all data
def install_apk(apkPath):
    package = get_package_id(apkPath)

    if subprocess.call("adb -e uninstall " + package) == 0:
        print("App successfully uninstalled.")

    if subprocess.call("adb -e install " + apkPath) == 0:
        print("Apk was installed successfully.")

    subprocess.call("adb -e shell monkey -p " + package + " -c android.intent.category.LAUNCHER 1")


# Retrieves package id from apk file
def get_package_id(apkPath):
    banding = subprocess.check_output("aapt dump badging " + apkPath).decode("utf-8")
    return re.findall(r'package: name=\'(.*?)\' versionCode=', banding)[0]
