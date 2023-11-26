import asyncio
import faulthandler
import getpass
import os
import socket
import sys
import time


import pyperclip
import qdarkstyle
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from qasync import QEventLoop, QApplication

from resources import database_op

os.system("pyuic5 -o ui/MainWindowUI.py ui/MainWindow.ui")
# os.system("pyuic5 -o ui/MainWindowUI2.py ui/MainWindow2.ui")


from MainWindow import MainWindow
from resources.common import banned_user, admin_user

if __name__ == "__main__":
    os.makedirs(r".\temps", exist_ok=True)
    faulthandler.enable()

    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    app.setStyleSheet(dark_stylesheet + "QMessageBox { messagebox-text-interaction-flags: 5; }")
    app.setWindowIcon(QIcon('resources/bookicon.png'))

    con = database_op.DBconnect()

    comp_user = getpass.getuser()
    comp_name = socket.gethostname()
    user_computer = f"{comp_user}-{comp_name}"
    print(user_computer)

    is_admin = admin_user(con, user_computer)

    if banned_user(con):
        sys.exit()
    with loop:
        if con.isValid():
            main = MainWindow(app, user_computer, con, is_admin)
            main.show()
            loop.run_forever()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("connection error")
            msg.setInformativeText(f"Available drivers {con.drivers()}")
            msg.setWindowTitle("error")
            msg.setDetailedText("you probably need to add postgres V14 \n then go here https://www.pythonguis.com/faq/postgres-pyqt5-windows-driver-not-loaded/ the command hase been pasted in your clip board (you need to be admin)")
            msg.exec_()
            print("Available drivers", con.drivers())
            print(con.lastError().text())
            print("you probably need to add postgres V14 \n then go here https://www.pythonguis.com/faq/postgres-pyqt5-windows-driver-not-loaded/ the command hase been pasted in your clip board (you need to be admin)")
            pyperclip.copy(r"SET PATH=%PATH%;C:\Program Files\PostgreSQL\14\bin")

