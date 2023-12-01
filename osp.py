import os
import subprocess as sp

paths = {
    'discord': "C:\\ProgramData\\ASUS\\Discord\\app-1.0.9024\\Discord++.exe",
    'gta5': ""
}


def open_cmd():
    os.system('start cmd')


def open_notepad():
    os.startfile(paths['discord'])


def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)


def open_gta():
    os.startfile(paths['gta5'])
#
# def open_calculator():
#     sp.Popen(paths['calculator'])
