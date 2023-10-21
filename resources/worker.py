import asyncio
import time

from PyQt5.QtCore import pyqtSignal, QThread

from resources.common import test


class Worker(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(bool)
    dataload = pyqtSignal(bool)

    def __init__(self, n, window=None):
        super().__init__()
        self.f = True
        self.paused = False
        self.n = n
        self.window = window
        # logging.info(f"thread init")

    def stopE(self):
        print("stop")
        # logging.info(f"Thread stop")
        self.n = False

    def Pause(self):
        print("pause")
        self.paused = True

    def Resume(self):
        print("resume")
        self.paused = False

    def run(self):
        """Long-running task."""
        if self.window is None:
            while self.n:
                if self.f:
                    test("F")
                    time.sleep(.1)
                    self.dataload.emit(self.f)
                    self.f = False
                # print("thread running")
                time.sleep(20)
                if not self.paused:
                    test("e")
                    self.progress.emit(True)
        else:
            while self.n:
                self.window.ui.l_con_isValid.setText(str(self.window.con.isValid()))
                self.window.ui.l_con_last_query.setText(str(self.window.lastquery))
                self.window.ui.l_con_last_error.setText(self.window.con.lastError().text())
                self.window.ui.l_con_is_admin.setText("Admin" if self.window.is_admin else "Not Admin")
                self.window.ui.l_con_computer_name.setText(self.window.user_computer)
                time.sleep(.1)

            # logging.info(f"thread finish")
        self.finished.emit()

