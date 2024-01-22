from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QInputDialog

from resources.credential import user_name1, password_user, admin_name, password_admin


def DBconnect(isAdmin=False):
    con = QSqlDatabase.addDatabase("QPSQL", "novelapp")
    con.setDatabaseName("charact1_Characters_Voice_Indicator")
    con.setHostName("www.charactersvoiceindicator.localhoost.com")
    if isAdmin:
        con.open(admin_name, password_admin)
    else:
        con.open(user_name1, password_user)
    return con