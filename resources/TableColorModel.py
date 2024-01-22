from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtSql import QSqlTableModel, QSqlRelationalTableModel


class TableColorModel(QSqlRelationalTableModel):
    def __init__(self, db):
        super(TableColorModel, self).__init__(db=db)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        color = "#000000"
        if role == Qt.ItemDataRole.DisplayRole:
            return super(TableColorModel, self).data(index, role)
        if role == Qt.ItemDataRole.EditRole:
            return super(TableColorModel, self).data(index, role)
        if role == Qt.ItemDataRole.ForegroundRole:
            if self.tableName() == "lines":
                color = QtGui.QColor(super(TableColorModel, self).data(super(TableColorModel, self)
                                                                       .index(index.row(), 8), Qt.ItemDataRole.DisplayRole))
            elif self.tableName() == "characters":
                color = QtGui.QColor(super(TableColorModel, self).data(super(TableColorModel, self)
                                                                       .index(index.row(), 4), Qt.ItemDataRole.DisplayRole))

            elif self.tableName() == "chapters":
                status = super(TableColorModel, self).data(super(TableColorModel, self)
                                                           .index(index.row(), 3), Qt.ItemDataRole.DisplayRole)
                if status == "WIP":
                    color = QColor("#979c08")
                elif status == "to-do":
                    color = QColor("#919189")
                elif status == "complete":
                    color = QColor("#00800d")

            elif self.tableName() == "novels":
                status = super(TableColorModel, self).data(super(TableColorModel, self)
                                                           .index(index.row(), 2), Qt.ItemDataRole.DisplayRole)
                if status == "WIP":
                    color = QColor("#979c08")
                elif status == "to-do":
                    color = QColor("#919189")
                elif status == "complete":
                    color = QColor("#00800d")

            return color
