__all__ = ('enable', 'disable')

import getpass
import os
import shutil
import sys
from pathlib import Path

if sys.platform == 'win32':
    def enable():
        USER_NAME = getpass.getuser()
        file_path = os.getcwd()
        bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
        with open(bat_path + '\\' + "openAiralarm.bat", "w+") as bat_file:
            bat_file.write('chcp 1251\n')
            bat_file.write('cd %s\n' % file_path)
            bat_file.write(r'start %s' % "airalarm.exe")

    def disable():
        USER_NAME = getpass.getuser()
        path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\openAiralarm.bat'
        os.remove(path % USER_NAME)
elif sys.platform == 'linux':
    APPS_PATH = Path.home() / '.local/share/applications'
    AUTOSTART_PATH = Path.home() / '.config/autostart'
    FILENAME = 'airalarm.desktop'

    def enable():
        shutil.copy(APPS_PATH / FILENAME, AUTOSTART_PATH)

    def disable():
        path = AUTOSTART_PATH / FILENAME
        path.unlink()
else:
    raise NotImplementedError()
