from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTableView


class QTableViewP(QTableView):
    focus_out_signal = pyqtSignal()
    focus_in_signal = pyqtSignal()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        print("focus_out")
        self.focus_out_signal.emit()

    def focusInEvent(self,event):
        super().focusInEvent(event)
        print("focus_in")
        self.focus_in_signal.emit()
