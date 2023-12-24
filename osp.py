import os
import subprocess as sp

paths = {
    'notepad': "C:\\Users\\ASUS\\AppData\\Local\\Microsoft\\WindowsApps\\notepad.exe",
    'discord': "C:\\ProgramData\\ASUS\\Discord\\app-1.0.9028\\discord.exe",
    'gta': "D:\\Tanishq\\GTA\\Launcher.exe"
}


def open_cmd():
    os.system('start cmd')


def open_notepad():
    os.startfile(paths['notepad'])


def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)


def open_gta():
    os.startfile(paths['gta'])


def open_discord():
    os.startfile(paths['discord'])
