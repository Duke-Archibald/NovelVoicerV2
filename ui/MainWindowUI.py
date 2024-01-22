# Form implementation generated from reading ui file 'ui/MainWindow.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1192, 1010)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.hl_bottom_section = QtWidgets.QHBoxLayout()
        self.hl_bottom_section.setSpacing(0)
        self.hl_bottom_section.setObjectName("hl_bottom_section")
        self.tv_lines = QTableViewP(parent=self.centralwidget)
        self.tv_lines.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tv_lines.setObjectName("tv_lines")
        self.hl_bottom_section.addWidget(self.tv_lines)
        self.tv_lines_split = QtWidgets.QTableView(parent=self.centralwidget)
        self.tv_lines_split.setMinimumSize(QtCore.QSize(125, 0))
        self.tv_lines_split.setMaximumSize(QtCore.QSize(200, 16777215))
        self.tv_lines_split.setObjectName("tv_lines_split")
        self.hl_bottom_section.addWidget(self.tv_lines_split)
        self.gridLayout_2.addLayout(self.hl_bottom_section, 2, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.l_novel = QtWidgets.QLabel(parent=self.centralwidget)
        self.l_novel.setObjectName("l_novel")
        self.horizontalLayout_2.addWidget(self.l_novel)
        self.cb_novel = QtWidgets.QComboBox(parent=self.centralwidget)
        self.cb_novel.setMaximumSize(QtCore.QSize(400, 16777215))
        self.cb_novel.setObjectName("cb_novel")
        self.horizontalLayout_2.addWidget(self.cb_novel)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.l_chapter = QtWidgets.QLabel(parent=self.centralwidget)
        self.l_chapter.setMaximumSize(QtCore.QSize(50, 16777215))
        self.l_chapter.setObjectName("l_chapter")
        self.horizontalLayout_3.addWidget(self.l_chapter)
        self.checkbox_complete = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.checkbox_complete.setMaximumSize(QtCore.QSize(140, 16777215))
        self.checkbox_complete.setTristate(False)
        self.checkbox_complete.setObjectName("checkbox_complete")
        self.horizontalLayout_3.addWidget(self.checkbox_complete)
        self.cb_chapter = QtWidgets.QComboBox(parent=self.centralwidget)
        self.cb_chapter.setMaximumSize(QtCore.QSize(350, 16777215))
        self.cb_chapter.setObjectName("cb_chapter")
        self.horizontalLayout_3.addWidget(self.cb_chapter)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5.addLayout(self.verticalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pb_duplicate_line = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pb_duplicate_line.setObjectName("pb_duplicate_line")
        self.verticalLayout.addWidget(self.pb_duplicate_line)
        self.pb_save_chapter = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pb_save_chapter.setObjectName("pb_save_chapter")
        self.verticalLayout.addWidget(self.pb_save_chapter)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pb_delete_line = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pb_delete_line.setObjectName("pb_delete_line")
        self.verticalLayout_2.addWidget(self.pb_delete_line)
        self.pb_complete_chapter = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pb_complete_chapter.setObjectName("pb_complete_chapter")
        self.verticalLayout_2.addWidget(self.pb_complete_chapter)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.l_character_name = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        self.l_character_name.setFont(font)
        self.l_character_name.setObjectName("l_character_name")
        self.horizontalLayout.addWidget(self.l_character_name)
        self.pb_make_todo = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pb_make_todo.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pb_make_todo.setObjectName("pb_make_todo")
        self.horizontalLayout.addWidget(self.pb_make_todo)
        self.pb_revert = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pb_revert.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pb_revert.setObjectName("pb_revert")
        self.horizontalLayout.addWidget(self.pb_revert)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dw_characters = QtWidgets.QDockWidget(parent=MainWindow)
        self.dw_characters.setFloating(False)
        self.dw_characters.setObjectName("dw_characters")
        self.dockWidgetContents_3 = QtWidgets.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents_3)
        self.gridLayout.setObjectName("gridLayout")
        self.pb_show_mod = QtWidgets.QPushButton(parent=self.dockWidgetContents_3)
        self.pb_show_mod.setObjectName("pb_show_mod")
        self.gridLayout.addWidget(self.pb_show_mod, 0, 0, 1, 1)
        self.tv_characters = QtWidgets.QTableView(parent=self.dockWidgetContents_3)
        self.tv_characters.setObjectName("tv_characters")
        self.gridLayout.addWidget(self.tv_characters, 1, 0, 1, 1)
        self.dw_characters.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dw_characters)
        self.dw_stats = QtWidgets.QDockWidget(parent=MainWindow)
        self.dw_stats.setFloating(False)
        self.dw_stats.setAllowedAreas(QtCore.Qt.DockWidgetArea.AllDockWidgetAreas)
        self.dw_stats.setObjectName("dw_stats")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.dockWidgetContents_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gl_stats = QtWidgets.QGridLayout()
        self.gl_stats.setObjectName("gl_stats")
        self.pb_interactive = QtWidgets.QPushButton(parent=self.dockWidgetContents_2)
        self.pb_interactive.setObjectName("pb_interactive")
        self.gl_stats.addWidget(self.pb_interactive, 0, 0, 1, 1)
        self.cbox_chapter = QtWidgets.QCheckBox(parent=self.dockWidgetContents_2)
        self.cbox_chapter.setObjectName("cbox_chapter")
        self.gl_stats.addWidget(self.cbox_chapter, 0, 1, 1, 1)
        self.gridLayout_5.addLayout(self.gl_stats, 0, 0, 1, 1)
        self.dw_stats.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dw_stats)
        self.dw_progression = QtWidgets.QDockWidget(parent=MainWindow)
        self.dw_progression.setFloating(False)
        self.dw_progression.setObjectName("dw_progression")
        self.dockWidgetContents_4 = QtWidgets.QWidget()
        self.dockWidgetContents_4.setObjectName("dockWidgetContents_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.dockWidgetContents_4)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.prbr_chapter = QtWidgets.QProgressBar(parent=self.dockWidgetContents_4)
        self.prbr_chapter.setProperty("value", 0)
        self.prbr_chapter.setObjectName("prbr_chapter")
        self.gridLayout_4.addWidget(self.prbr_chapter, 1, 1, 1, 1)
        self.prbr_TTS = QtWidgets.QProgressBar(parent=self.dockWidgetContents_4)
        self.prbr_TTS.setProperty("value", 24)
        self.prbr_TTS.setObjectName("prbr_TTS")
        self.gridLayout_4.addWidget(self.prbr_TTS, 2, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(parent=self.dockWidgetContents_4)
        self.label_8.setObjectName("label_8")
        self.gridLayout_4.addWidget(self.label_8, 1, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(parent=self.dockWidgetContents_4)
        self.label_9.setObjectName("label_9")
        self.gridLayout_4.addWidget(self.label_9, 2, 0, 1, 1)
        self.prbr_novel = QtWidgets.QProgressBar(parent=self.dockWidgetContents_4)
        self.prbr_novel.setProperty("value", 24)
        self.prbr_novel.setObjectName("prbr_novel")
        self.gridLayout_4.addWidget(self.prbr_novel, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(parent=self.dockWidgetContents_4)
        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(self.label_6, 0, 0, 1, 1)
        self.dw_progression.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dw_progression)
        self.dw_info = QtWidgets.QDockWidget(parent=MainWindow)
        self.dw_info.setFloating(False)
        self.dw_info.setObjectName("dw_info")
        self.dockWidgetContents_5 = QtWidgets.QWidget()
        self.dockWidgetContents_5.setObjectName("dockWidgetContents_5")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.dockWidgetContents_5)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.l_con_isValid = QtWidgets.QLabel(parent=self.dockWidgetContents_5)
        self.l_con_isValid.setObjectName("l_con_isValid")
        self.gridLayout_6.addWidget(self.l_con_isValid, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.dockWidgetContents_5)
        self.label_2.setObjectName("label_2")
        self.gridLayout_6.addWidget(self.label_2, 0, 0, 1, 1)
        self.l_con_last_query = QtWidgets.QLabel(parent=self.dockWidgetContents_5)
        self.l_con_last_query.setWordWrap(True)
        self.l_con_last_query.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse|QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        self.l_con_last_query.setObjectName("l_con_last_query")
        self.gridLayout_6.addWidget(self.l_con_last_query, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=self.dockWidgetContents_5)
        self.label_3.setObjectName("label_3")
        self.gridLayout_6.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=self.dockWidgetContents_5)
        self.label_4.setObjectName("label_4")
        self.gridLayout_6.addWidget(self.label_4, 3, 0, 1, 1)
        self.l_con_last_error = QtWidgets.QLabel(parent=self.dockWidgetContents_5)
        self.l_con_last_error.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse|QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        self.l_con_last_error.setObjectName("l_con_last_error")
        self.gridLayout_6.addWidget(self.l_con_last_error, 1, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(parent=self.dockWidgetContents_5)
        self.label_7.setObjectName("label_7")
        self.gridLayout_6.addWidget(self.label_7, 4, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=self.dockWidgetContents_5)
        self.label_5.setObjectName("label_5")
        self.gridLayout_6.addWidget(self.label_5, 2, 0, 1, 1)
        self.l_con_computer_name = QtWidgets.QLabel(parent=self.dockWidgetContents_5)
        self.l_con_computer_name.setObjectName("l_con_computer_name")
        self.gridLayout_6.addWidget(self.l_con_computer_name, 4, 1, 1, 1)
        self.l_con_is_admin = QtWidgets.QLabel(parent=self.dockWidgetContents_5)
        self.l_con_is_admin.setWordWrap(False)
        self.l_con_is_admin.setObjectName("l_con_is_admin")
        self.gridLayout_6.addWidget(self.l_con_is_admin, 3, 1, 1, 1)
        self.pb_Vcon_copy = QtWidgets.QPushButton(parent=self.dockWidgetContents_5)
        self.pb_Vcon_copy.setObjectName("pb_Vcon_copy")
        self.gridLayout_6.addWidget(self.pb_Vcon_copy, 0, 2, 1, 1)
        self.pb_last_error_copy = QtWidgets.QPushButton(parent=self.dockWidgetContents_5)
        self.pb_last_error_copy.setObjectName("pb_last_error_copy")
        self.gridLayout_6.addWidget(self.pb_last_error_copy, 1, 2, 1, 1)
        self.pb_last_query_copy = QtWidgets.QPushButton(parent=self.dockWidgetContents_5)
        self.pb_last_query_copy.setObjectName("pb_last_query_copy")
        self.gridLayout_6.addWidget(self.pb_last_query_copy, 2, 2, 1, 1)
        self.pb_status_copy = QtWidgets.QPushButton(parent=self.dockWidgetContents_5)
        self.pb_status_copy.setObjectName("pb_status_copy")
        self.gridLayout_6.addWidget(self.pb_status_copy, 3, 2, 1, 1)
        self.pb_user_name_copy = QtWidgets.QPushButton(parent=self.dockWidgetContents_5)
        self.pb_user_name_copy.setObjectName("pb_user_name_copy")
        self.gridLayout_6.addWidget(self.pb_user_name_copy, 4, 2, 1, 1)
        self.dw_info.setWidget(self.dockWidgetContents_5)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dw_info)
        self.dw_tts = QtWidgets.QDockWidget(parent=MainWindow)
        self.dw_tts.setFloating(False)
        self.dw_tts.setObjectName("dw_tts")
        self.dockWidgetContents_6 = QtWidgets.QWidget()
        self.dockWidgetContents_6.setObjectName("dockWidgetContents_6")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.dockWidgetContents_6)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.pb_start_tts = QtWidgets.QPushButton(parent=self.dockWidgetContents_6)
        self.pb_start_tts.setObjectName("pb_start_tts")
        self.gridLayout_8.addWidget(self.pb_start_tts, 0, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(parent=self.dockWidgetContents_6)
        self.label_10.setObjectName("label_10")
        self.gridLayout_8.addWidget(self.label_10, 1, 0, 1, 1)
        self.tableView = QtWidgets.QTableView(parent=self.dockWidgetContents_6)
        self.tableView.setObjectName("tableView")
        self.gridLayout_8.addWidget(self.tableView, 2, 0, 1, 1)
        self.dw_tts.setWidget(self.dockWidgetContents_6)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dw_tts)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1192, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.dw_char_mods = QtWidgets.QDockWidget(parent=MainWindow)
        self.dw_char_mods.setFloating(True)
        self.dw_char_mods.setObjectName("dw_char_mods")
        self.dockWidgetContents_7 = QtWidgets.QWidget()
        self.dockWidgetContents_7.setObjectName("dockWidgetContents_7")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.dockWidgetContents_7)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtWidgets.QLabel(parent=self.dockWidgetContents_7)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 1, 0, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_25 = QtWidgets.QLabel(parent=self.dockWidgetContents_7)
        self.label_25.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_25.setObjectName("label_25")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_25)
        self.le_char_character_name = QtWidgets.QLineEdit(parent=self.dockWidgetContents_7)
        self.le_char_character_name.setText("")
        self.le_char_character_name.setObjectName("le_char_character_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.le_char_character_name)
        self.label_26 = QtWidgets.QLabel(parent=self.dockWidgetContents_7)
        self.label_26.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_26.setObjectName("label_26")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_26)
        self.cb_char_novel = QtWidgets.QComboBox(parent=self.dockWidgetContents_7)
        self.cb_char_novel.setObjectName("cb_char_novel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.cb_char_novel)
        self.label_27 = QtWidgets.QLabel(parent=self.dockWidgetContents_7)
        self.label_27.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_27.setObjectName("label_27")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_27)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.le_char_color = QtWidgets.QLineEdit(parent=self.dockWidgetContents_7)
        self.le_char_color.setObjectName("le_char_color")
        self.horizontalLayout_8.addWidget(self.le_char_color)
        self.pb_char_color = QtWidgets.QPushButton(parent=self.dockWidgetContents_7)
        self.pb_char_color.setObjectName("pb_char_color")
        self.horizontalLayout_8.addWidget(self.pb_char_color)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.horizontalLayout_8)
        self.cb_char_importances = QtWidgets.QComboBox(parent=self.dockWidgetContents_7)
        self.cb_char_importances.setObjectName("cb_char_importances")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.cb_char_importances)
        self.label_28 = QtWidgets.QLabel(parent=self.dockWidgetContents_7)
        self.label_28.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_28.setObjectName("label_28")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_28)
        self.gridLayout_3.addLayout(self.formLayout, 3, 0, 1, 1)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_20 = QtWidgets.QLabel(parent=self.dockWidgetContents_7)
        self.label_20.setObjectName("label_20")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_20)
        self.cb_char_country = QtWidgets.QComboBox(parent=self.dockWidgetContents_7)
        self.cb_char_country.setEditable(True)
        self.cb_char_country.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.NoInsert)
        self.cb_char_country.setObjectName("cb_char_country")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.cb_char_country)
        self.label_22 = QtWidgets.QLabel(parent=self.dockWidgetContents_7)
        self.label_22.setObjectName("label_22")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_22)
        self.cb_char_type = QtWidgets.QComboBox(parent=self.dockWidgetContents_7)
        self.cb_char_type.setObjectName("cb_char_type")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.cb_char_type)
        self.label_23 = QtWidgets.QLabel(parent=self.dockWidgetContents_7)
        self.label_23.setObjectName("label_23")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_23)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.cb_char_name = QtWidgets.QComboBox(parent=self.dockWidgetContents_7)
        self.cb_char_name.setEditable(True)
        self.cb_char_name.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.NoInsert)
        self.cb_char_name.setObjectName("cb_char_name")
        self.horizontalLayout_7.addWidget(self.cb_char_name)
        self.cb_char_voice_code = QtWidgets.QComboBox(parent=self.dockWidgetContents_7)
        self.cb_char_voice_code.setEnabled(True)
        self.cb_char_voice_code.setObjectName("cb_char_voice_code")
        self.horizontalLayout_7.addWidget(self.cb_char_voice_code)
        self.formLayout_2.setLayout(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.horizontalLayout_7)
        self.cb_char_gender = QtWidgets.QComboBox(parent=self.dockWidgetContents_7)
        self.cb_char_gender.setObjectName("cb_char_gender")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.cb_char_gender)
        self.cb_char_service = QtWidgets.QComboBox(parent=self.dockWidgetContents_7)
        self.cb_char_service.setObjectName("cb_char_service")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.cb_char_service)
        self.label_21 = QtWidgets.QLabel(parent=self.dockWidgetContents_7)
        self.label_21.setObjectName("label_21")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_21)
        self.label_24 = QtWidgets.QLabel(parent=self.dockWidgetContents_7)
        self.label_24.setObjectName("label_24")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_24)
        self.gridLayout_3.addLayout(self.formLayout_2, 8, 0, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pb_char_test_voice = QtWidgets.QPushButton(parent=self.dockWidgetContents_7)
        self.pb_char_test_voice.setEnabled(True)
        self.pb_char_test_voice.setObjectName("pb_char_test_voice")
        self.verticalLayout_4.addWidget(self.pb_char_test_voice)
        self.pb_char_add = QtWidgets.QPushButton(parent=self.dockWidgetContents_7)
        self.pb_char_add.setEnabled(True)
        self.pb_char_add.setObjectName("pb_char_add")
        self.verticalLayout_4.addWidget(self.pb_char_add)
        self.pb_char_edit = QtWidgets.QPushButton(parent=self.dockWidgetContents_7)
        self.pb_char_edit.setObjectName("pb_char_edit")
        self.verticalLayout_4.addWidget(self.pb_char_edit)
        self.gridLayout_3.addLayout(self.verticalLayout_4, 10, 0, 1, 1)
        self.line_3 = QtWidgets.QFrame(parent=self.dockWidgetContents_7)
        self.line_3.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout_3.addWidget(self.line_3, 5, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(parent=self.dockWidgetContents_7)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_3.addWidget(self.line_2, 9, 0, 1, 1)
        self.line_4 = QtWidgets.QFrame(parent=self.dockWidgetContents_7)
        self.line_4.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout_3.addWidget(self.line_4, 0, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(parent=self.dockWidgetContents_7)
        self.label_11.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 7, 0, 1, 1)
        self.dw_char_mods.setWidget(self.dockWidgetContents_7)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dw_char_mods)
        self.actionLines = QtGui.QAction(parent=MainWindow)
        self.actionLines.setObjectName("actionLines")
        self.actionCharacters = QtGui.QAction(parent=MainWindow)
        self.actionCharacters.setObjectName("actionCharacters")
        self.actionProgress = QtGui.QAction(parent=MainWindow)
        self.actionProgress.setObjectName("actionProgress")
        self.actionStats = QtGui.QAction(parent=MainWindow)
        self.actionStats.setObjectName("actionStats")
        self.actionTTS = QtGui.QAction(parent=MainWindow)
        self.actionTTS.setVisible(False)
        self.actionTTS.setObjectName("actionTTS")
        self.actionsdfg = QtGui.QAction(parent=MainWindow)
        self.actionsdfg.setObjectName("actionsdfg")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.l_novel.setText(_translate("MainWindow", "Novel"))
        self.l_chapter.setText(_translate("MainWindow", "Chapter"))
        self.checkbox_complete.setText(_translate("MainWindow", "show completed chapter"))
        self.pb_duplicate_line.setText(_translate("MainWindow", "Duplicate Selected(s) Line(s)"))
        self.pb_save_chapter.setText(_translate("MainWindow", "Save Chapter"))
        self.pb_delete_line.setText(_translate("MainWindow", "Delete Selected(s) line(s)"))
        self.pb_complete_chapter.setText(_translate("MainWindow", "Complete Chapter"))
        self.l_character_name.setText(_translate("MainWindow", "No Character Selected"))
        self.pb_make_todo.setText(_translate("MainWindow", "Make To-Do"))
        self.pb_revert.setText(_translate("MainWindow", "Revert to old character"))
        self.dw_characters.setWindowTitle(_translate("MainWindow", "Characters"))
        self.pb_show_mod.setText(_translate("MainWindow", "show/hide character modification/creation"))
        self.dw_stats.setWindowTitle(_translate("MainWindow", "Stats"))
        self.pb_interactive.setText(_translate("MainWindow", "PushButton"))
        self.cbox_chapter.setText(_translate("MainWindow", "CheckBox"))
        self.dw_progression.setWindowTitle(_translate("MainWindow", "Progression"))
        self.label_8.setText(_translate("MainWindow", "Chapter Progression"))
        self.label_9.setText(_translate("MainWindow", "TTS progression"))
        self.label_6.setText(_translate("MainWindow", "Novel Progression"))
        self.dw_info.setWindowTitle(_translate("MainWindow", "Connection Info"))
        self.l_con_isValid.setText(_translate("MainWindow", "TextLabel"))
        self.label_2.setText(_translate("MainWindow", "connection valid:"))
        self.l_con_last_query.setText(_translate("MainWindow", "TextLabel"))
        self.label_3.setText(_translate("MainWindow", "last error:"))
        self.label_4.setText(_translate("MainWindow", "you are:"))
        self.l_con_last_error.setText(_translate("MainWindow", "TextLabel"))
        self.label_7.setText(_translate("MainWindow", "your name:"))
        self.label_5.setText(_translate("MainWindow", "last query:"))
        self.l_con_computer_name.setText(_translate("MainWindow", "TextLabel"))
        self.l_con_is_admin.setText(_translate("MainWindow", "TextLabel"))
        self.pb_Vcon_copy.setText(_translate("MainWindow", "Copy"))
        self.pb_last_error_copy.setText(_translate("MainWindow", "Copy"))
        self.pb_last_query_copy.setText(_translate("MainWindow", "Copy"))
        self.pb_status_copy.setText(_translate("MainWindow", "Copy"))
        self.pb_user_name_copy.setText(_translate("MainWindow", "Copy"))
        self.dw_tts.setWindowTitle(_translate("MainWindow", "Text-To-Speech"))
        self.pb_start_tts.setText(_translate("MainWindow", "Start Text-to-speech convertion"))
        self.label_10.setText(_translate("MainWindow", "google/playht/eleven character numbers stats"))
        self.dw_char_mods.setWindowTitle(_translate("MainWindow", "Characters Add/Modification"))
        self.label.setText(_translate("MainWindow", "Character info"))
        self.label_25.setText(_translate("MainWindow", "character name"))
        self.label_26.setText(_translate("MainWindow", "from novel"))
        self.label_27.setText(_translate("MainWindow", "color"))
        self.pb_char_color.setText(_translate("MainWindow", "color picker"))
        self.label_28.setText(_translate("MainWindow", "importance"))
        self.label_20.setText(_translate("MainWindow", "language"))
        self.label_22.setText(_translate("MainWindow", "type"))
        self.label_23.setText(_translate("MainWindow", "name"))
        self.label_21.setText(_translate("MainWindow", "service"))
        self.label_24.setText(_translate("MainWindow", "Gender"))
        self.pb_char_test_voice.setText(_translate("MainWindow", "Test current setting Voice"))
        self.pb_char_add.setText(_translate("MainWindow", "add a new character"))
        self.pb_char_edit.setText(_translate("MainWindow", "edit selected character"))
        self.label_11.setText(_translate("MainWindow", "Voice info"))
        self.actionLines.setText(_translate("MainWindow", "Lines"))
        self.actionCharacters.setText(_translate("MainWindow", "Characters"))
        self.actionProgress.setText(_translate("MainWindow", "Progress"))
        self.actionStats.setText(_translate("MainWindow", "Stats"))
        self.actionTTS.setText(_translate("MainWindow", "TTS"))
        self.actionsdfg.setText(_translate("MainWindow", "sdfg"))
from qtableviewp import QTableViewP
