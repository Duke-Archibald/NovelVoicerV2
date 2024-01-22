from PyQt6.QtWidgets import QDockWidget


class QDockWidgetTEST(QDockWidget):
    def resizeEvent(self, event):
        QDockWidget.resizeEvent(self, event)
        print("size", self.size().width(), self.size().height())

    def moveEvent(self, event):
        QDockWidget.moveEvent(self, event)
        print("pos", self.pos().y(), self.pos().x())

