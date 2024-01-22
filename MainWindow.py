import os
import pathlib
import re
import time
import webbrowser

import pyperclip
import winsound
from PyQt6 import QtWidgets, QtWebEngineWidgets
from PyQt6.QtCore import QSettings, QSortFilterProxyModel, Qt, pyqtSlot, QPersistentModelIndex
from PyQt6.QtGui import QCloseEvent, QColor
from PyQt6.QtSql import QSqlTableModel, QSqlQuery
from PyQt6.QtWidgets import QMainWindow, QScrollBar, QAbstractScrollArea, QTableView, QMessageBox, QColorDialog
from google.cloud import texttospeech
from google.oauth2 import service_account
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from resources import credential
from resources.EditableHeaderView import EditableHeaderView
from resources.TableColorModel import TableColorModel
from resources.common import test, last_query, appname, discord1
from resources.ploting import interactive_pie
from resources.stats import plot
from resources.worker import Worker
from ui.MainWindowUI import Ui_MainWindow


class MainWindow(QMainWindow):
    count = 0
    windowTitleBarHeight = 30

    def __init__(self, app, usercomputer, DBconnection, is_admin):
        super().__init__()
        self.discord_invite = discord1
        self.app = app
        self.settings = QSettings("NovelApp", "Voice2-0")

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("MainWindow")

        self.con = DBconnection

        self.is_admin = is_admin
        self.user_computer = usercomputer

        self.lastquery = last_query

        self.scroll_bar = QScrollBar(self)
        self.ui.tv_lines.setHorizontalScrollBar(self.scroll_bar)

        self.m_output = QtWebEngineWidgets.QWebEngineView()
        self.ui.gl_stats.addWidget(self.m_output, 1, 1)

        self.credentials = service_account.Credentials.from_service_account_file("resources/"
                                                                                 "novelapp-322716-f629fcd1c568.json")
        self.client = texttospeech.TextToSpeechClient(credentials=self.credentials)

        self.novel_selection = ""
        self.chapter_selection = ""
        self.character_name = ""
        self.character_voice = ""
        self.character_color = ""
        self.character_service = ""
        self.character_name_BAK = ""
        self.character_voice_BAK = ""
        self.character_color_BAK = ""
        self.character_service_BAK = ""
        self.tts_dir = ""
        self.html_blacklist = ['[document]', 'noscript', 'header', 'html', 'meta', 'head', 'input', 'script', 'style']

        self.LselectedRows = []

        self.complete_called = False

        self.ui.prbr_TTS.setValue(0)

        self.readSettings()

        self.ui.menubar.addAction(self.ui.dw_characters.toggleViewAction())
        self.ui.menubar.addAction(self.ui.dw_progression.toggleViewAction())
        self.ui.menubar.addAction(self.ui.dw_stats.toggleViewAction())
        self.ui.menubar.addAction(self.ui.dw_info.toggleViewAction())

        self.ui.dw_tts.setVisible(not self.is_admin)
        self.ui.dw_stats.setVisible(False)
        self.ui.dw_char_mods.setVisible(False)
        self.ui.pb_show_mod.setVisible(False)

        if self.is_admin:
            self.ui.menubar.addAction(self.ui.dw_tts.toggleViewAction())
            self.ui.pb_show_mod.setVisible(True)

        self.ui.pb_show_mod.clicked.connect(lambda: self.ui.dw_char_mods.setVisible(False)
        if self.ui.dw_char_mods.isVisible()
        else self.ui.dw_char_mods.setVisible(True))

        self.workerInfoUpdate = Worker(True, self)
        self.workerInfoUpdate.finished.connect(self.workerInfoUpdate.deleteLater)
        self.workerInfoUpdate.start()

        self.workerSave = Worker(True)
        self.workerSave.finished.connect(self.workerSave.deleteLater)
        self.workerSave.progress.connect(self.save_refresh)
        self.workerSave.dataload.connect(self.load_data)
        self.workerSave.start()

        # models
        self.model_novel = QSqlTableModel(db=self.con)
        self.model_playht_voice = QSqlTableModel(db=self.con)
        self.model_importances = QSqlTableModel(db=self.con)
        self.model_all_voices = QSqlTableModel(db=self.con)
        self.model_voice = QSqlTableModel(db=self.con)
        self.model_chapter = TableColorModel(db=self.con)
        self.model_lines = TableColorModel(db=self.con)
        self.model_characters = TableColorModel(db=self.con)

        self.CharHeaderview = EditableHeaderView(self.ui.tv_characters)
        self._proxy = QSortFilterProxyModel(self)

        # pie chart setup
        self.figure2 = plt.figure(2)
        self.figure = plt.figure(1)
        self.canvas = FigureCanvas(self.figure)
        # self.toolbar = NavigationToolbar(self.canvas, self)
        # self.ui.gl_stats.addWidget(self.toolbar)
        self.ui.gl_stats.addWidget(self.canvas, 1, 0)
        # self.make_plot()
        ###########################################################################################
        # novel
        self.model_novel.setTable("novels")
        self.model_novel.select()
        self.ui.cb_novel.setModel(self.model_novel)
        self.ui.cb_novel.setModelColumn(1)

        # chapter
        self.model_chapter.setTable("chapters")
        self.model_chapter.setSort(1, Qt.SortOrder.AscendingOrder)
        self.model_chapter.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        self.model_chapter.select()
        self.ui.cb_chapter.setModel(self.model_chapter)
        self.ui.cb_chapter.setModelColumn(2)

        # characters
        self.CharHeaderview.textChanged.connect(self.on_text_changed)
        self.model_characters.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        self.ui.tv_characters.setModel(self._proxy)
        self.ui.tv_characters.setHorizontalHeader(self.CharHeaderview)
        self.ui.tv_characters.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        # character mod
        self.old_voice = ""
        self.old_name = ""
        self.old_novel = ""
        self.old_color = ""
        self.old_importance = ""
        self.old_service = ""
        # self.client = client

        self.genders = ["All"]
        self.services = ["All"]
        self.country = []  # all added later because it needs to be a index 0
        self.type = ["All"]

        self.ui.cb_char_novel.setModel(self.model_novel)
        self.ui.cb_char_novel.setModelColumn(1)
        self.model_importances.setTable("importances")
        self.model_importances.select()
        self.ui.cb_char_importances.setModel(self.model_importances)
        self.ui.cb_char_importances.setModelColumn(1)

        self.model_playht_voice.setTable("play_ht_voices")
        self.model_playht_voice.select()
        self.ui.cb_char_name.setModel(self.model_playht_voice)
        self.ui.cb_char_name.setModelColumn(4)
        self.ui.cb_char_voice_code.setModel(self.model_playht_voice)
        self.ui.cb_char_voice_code.setModelColumn(7)

        voiceoptionquery = f"select phtv_gender, phtv_language,phtv_service,phtv_voice_type from play_ht_voices"
        self.lastquery = voiceoptionquery
        query = QSqlQuery(db=self.con)
        query.exec(voiceoptionquery)
        test("query")
        while query.next():
            self.genders.append(query.value(0))
            self.country.append(query.value(1))
            self.services.append(query.value(2))
            self.type.append(query.value(3))
        self.ui.cb_char_country.insertItem(0, "All")  # need to be at index 0
        self.genders = list(dict.fromkeys(self.genders))
        self.country = list(dict.fromkeys(self.country))
        self.services = list(dict.fromkeys(self.services))
        self.type = list(dict.fromkeys(self.type))
        self.country.sort()
        self.ui.cb_char_gender.addItems(self.genders)
        self.ui.cb_char_country.addItems(self.country)
        self.ui.cb_char_service.addItems(self.services)
        self.ui.cb_char_type.addItems(self.type)
        self.ui.cb_char_country.completer().setCompletionMode(QtWidgets.QCompleter.CompletionMode.PopupCompletion)
        self.ui.cb_char_name.completer().setCompletionMode(QtWidgets.QCompleter.CompletionMode.PopupCompletion)

        self.ui.cb_char_gender.currentTextChanged.connect(self.cb_char_changed)
        self.ui.cb_char_service.currentTextChanged.connect(self.cb_char_changed)
        self.ui.cb_char_type.currentTextChanged.connect(self.cb_char_changed)
        self.ui.cb_char_country.currentTextChanged.connect(self.cb_char_changed)
        self.ui.cb_char_name.currentTextChanged.connect(self.name_changed)
        self.ui.le_char_character_name.textChanged.connect(self.name_changed)
        self.ui.cb_char_name.currentTextChanged.connect(self.name_voice_sync)
        self.ui.cb_char_voice_code.currentTextChanged.connect(self.name_voice_sync)
        self.ui.pb_char_color.clicked.connect(self.colordef)

        # lines
        self.model_lines.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.ui.tv_lines.setModel(self.model_lines)
        self.ui.tv_lines.focus_out_signal.connect(lambda: self.workerSave.Pause())
        self.ui.tv_lines.focus_in_signal.connect(lambda: self.workerSave.Resume())
        self.ui.tv_lines.focus_out_signal.connect(self.focus_out)
        self.ui.tv_lines.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.ui.tv_lines_split.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.ui.tv_lines_split.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContentsOnFirstShow)

        # clicked signal connection
        self.ui.tv_characters.selectionModel().selectionChanged.connect(self.tv_characters_clicked)
        # self.ui.tv_characters.doubleClicked.connect(self.handle_edit_character)

        self.ui.tv_lines.selectionModel().selectionChanged.connect(self.tv_lines_clicked)
        self.ui.tv_lines.doubleClicked.connect(self.pause_worker)

        self.ui.pb_Vcon_copy.clicked.connect(self.copy_paste)
        self.ui.pb_last_error_copy.clicked.connect(self.copy_paste)
        self.ui.pb_last_query_copy.clicked.connect(self.copy_paste)
        self.ui.pb_status_copy.clicked.connect(self.copy_paste)
        self.ui.pb_user_name_copy.clicked.connect(self.copy_paste)

        self.ui.cb_novel.activated.connect(self.comboboxChanged)
        self.ui.cb_chapter.activated.connect(self.comboboxChanged)

        self.ui.cb_novel.setCurrentText(self.settings.value("lastNovel"))

        self.ui.tv_lines.verticalScrollBar().valueChanged.connect(
            lambda index: self.ui.tv_lines_split.verticalScrollBar().setValue(index))
        self.ui.tv_lines_split.verticalScrollBar().setDisabled(True)

        self.ui.checkbox_complete.setChecked(False)
        self.ui.checkbox_complete.stateChanged.connect(self.complete_check)

        self.complete_check()

        self.ui.pb_complete_chapter.clicked.connect(lambda: self.status_change_chapter("complete"))
        self.ui.pb_save_chapter.clicked.connect(self.save_refresh)
        self.ui.pb_start_tts.clicked.connect(self.tts_chapter)
        self.ui.pb_delete_line.clicked.connect(self.deleteRow)
        self.ui.pb_duplicate_line.clicked.connect(self.insertRow)
        # self.ui.pb_plot_toggle.clicked.connect(self.handle_plot_toggle)
        self.ui.pb_make_todo.clicked.connect(self.pb_characters_clicked)
        self.ui.pb_revert.clicked.connect(self.pb_characters_clicked)
        self.ui.pb_interactive.clicked.connect(self.interactiveplot)
        # self.ui.pb_test.clicked.connect(self.test_clicked)

        self.ui.pb_char_add.clicked.connect(self.add_char)
        self.ui.pb_char_edit.clicked.connect(self.edit_char)
        # self.ui.pb_plot_toggle.setCheckable(True)
        self.character_mod_populate()

        if not self.is_admin:
            self.ui.pb_delete_line.hide()
            self.ui.pb_complete_chapter.hide()
            self.ui.prbr_TTS.hide()
            self.ui.pb_start_tts.hide()
            self.ui.checkbox_complete.hide()
            # self.ui.pb_test.hide()

    def test_voice(self):
        test("test voice")
        headers = {
            'Authorization': credential.secretKey,
            'X-User-ID': credential.userID,
            'Content-Type': 'application/json'
        }
        baseEndPoint = "https://play.ht/api/v1"
        text = f"Hi, my name is {self.ui.le_character_name.text()}," \
               f" and I'm a character from {self.ui.cb_novel.currentText()}."
        title = f"{self.ui.cb_voice_code.currentText()}"
        self.filename = f"temps/{title}.wav"
        if self.ui.cb_playht_voice_model.data(self.ui.cb_playht_voice_model.index(self.ui.cb_name.currentIndex(), 6)) == "gc":
            print("google tts")
            voice_name = self.ui.cb_voice_code.currentText()
            if pathlib.Path(self.filename).exists():
                winsound.PlaySound(self.filename, winsound.SND_FILENAME)
            else:
                if voice_name == "":
                    winsound.PlaySound("resources/no_voice.wav", winsound.SND_FILENAME)
                    return
                time.sleep(.25)
                language_code = "-".join(voice_name.split("-")[:2])
                text_input = texttospeech.SynthesisInput(text=text)
                voice_params = texttospeech.VoiceSelectionParams(
                    language_code=language_code, name=voice_name
                )
                audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.LINEAR16
                )
                response = self.client.synthesize_speech(
                    input=text_input, voice=voice_params, audio_config=audio_config
                )
                os.makedirs(os.path.dirname(self.filename), exist_ok=True)
                with open(self.filename, "wb") as out:
                    out.write(response.audio_content)
        else:
            print("playht tts")
            url = self.cb_playht_voice_model.data(self.cb_playht_voice_model.index(self.cb_name.currentIndex(), 5))
            p = re.compile(r"(?<=\/)([^\/]*)(mp3|wav) *")
            result = p.search(url)
            filename = result.group(0)
            webbrowser.open(url, new=2)

    def tts_chapter(self):
        # audio = generate(
        #     text="Hi! My name is Bella, nice to meet you!",
        #     voice="Bella",
        #     model='eleven_monolingual_v1'
        # )
        # save(audio,'test.wav')
        test("tts chapter")

    def handle_plot_toggle(self):
        test("handle_plot_toggle")

    def interactiveplot(self):
        interactive_pie(self.ui.cb_novel.currentText(), self.con, self.m_output)

    def make_plot(self):
        test("make_plot")
        # self.ui.tb_stats.setSource(QUrl.fromLocalFile("resources/TESTING/ttest.html"))

        # plt.figure(2)
        # self.figure2.set_size_inches(20, 20)
        # self.draw()
        # plt.savefig(self.savename, dpi=100)
        # plt.figure(1)
        # self.draw()
        plot(self.figure,
             self.ui.cbox_chapter,
             self.con,
             self.ui.cb_novel,
             self.chapter_selection,
             self.is_admin,
             self.canvas,
             self.ui.cb_chapter)

    def test_clicked(self):
        test("test_clicked")

    # region completed_function

    def add_char(self):
        novel = self.ui.cb_char_novel.currentText()
        voice = self.ui.cb_char_voice_code.currentText()
        importance = self.ui.cb_char_importances.currentText()
        name = self.ui.le_char_character_name.text()
        color = self.ui.le_char_color.text()
        service = self.model_playht_voice.data(self.model_playht_voice.index(self.ui.cb_char_name.currentIndex(), 6))
        infomessagebox = QMessageBox(self)
        infomessagebox.setWindowTitle(f"{appname} - Add Character")
        infomessagebox.setText(f"Adding {name} to the database")
        infomessagebox.setStandardButtons(QMessageBox.StandardButton.NoButton)
        infomessagebox.open()
        self.app.processEvents()

        if novel == "" or name == "" or voice == "" or color == "" or importance == "":
            QMessageBox.information(
                self,
                f"{appname} - error",
                f"error not enough information\nall field are required",
            )
            infomessagebox.done(0)
        else:
            r = self.model_characters.record()
            r.setGenerated("character_id", False)
            r.setGenerated("character_usage", False)
            r.setValue("character_name", f'{name}')
            r.setValue("character_novel", f"{novel}")
            r.setValue("character_voice", f"{voice}")
            r.setValue("character_color", f"{color}")
            r.setValue("character_voice_sys", f"{service}")
            r.setValue("character_importance", f"{importance}")

            if not self.model_characters.insertRecord(-1, r):
                infomessagebox.done(0)
                QMessageBox.critical(
                    self,
                    f"{appname} - Error!",
                    "character Error: %s" % self.model_characters.lastError().text(),
                )
            else:
                infomessagebox.done(0)
                QMessageBox.information(
                    self,
                    f"{appname} - succes",
                    f"Succes, {name} was added",
                )
                self.model_characters.select()

    def edit_char(self):
        # new_novel = self.cb_novel.currentText()
        new_voice = self.ui.cb_char_voice_code.currentText()
        new_name = self.ui.le_char_character_name.text()
        new_color = self.ui.le_char_color.text()
        new_importance = self.ui.cb_char_importances.currentText()
        new_service = self.model_playht_voice.data(
            self.model_playht_voice.index(self.ui.cb_char_name.currentIndex(), 6))
        print(new_name, new_color, new_voice, new_importance)

        if new_name == "" or new_voice == "" or new_color == "" or new_importance == "":
            QMessageBox.information(
                self,
                f"{appname} - error",
                f"error not enough information\nall field are required",
            )
        else:
            prequery = f"update characters set " \
                       f"character_name = '{new_name}'," \
                       f"character_voice = '{new_voice}'," \
                       f"character_color = '{new_color}'," \
                       f"character_voice_sys = '{new_service}'," \
                       f"character_importance = '{new_importance}'" \
                       f"where character_name = '{self.old_name}' " \
                       f"and character_novel='{self.old_novel}'"
            query = QSqlQuery(db=self.con)
            self.lastquery = prequery
            query.exec(prequery)
            self.edit_line_from_char(self.old_name, new_name, new_color, new_voice, self.old_novel)
            self.model_characters.select()
            # self.accept()

    def edit_line_from_char(self, char_old_name, char_new_name, char_color, char_voice, char_novel):
        service = self.model_playht_voice.data(self.model_playht_voice.index(self.ui.cb_char_name.currentIndex(), 6))
        query = QSqlQuery(db=self.con)
        query.exec(
            f"update lines set line_character = '{char_new_name}',"
            f"line_voice = '{char_voice}',"
            f"line_voice_sys = '{service}',"
            f"line_color = '{char_color}' "
            f"WHERE line_novel = '{char_novel}' "
            f"AND line_character = '{char_old_name}'")

    @pyqtSlot('QItemSelection', 'QItemSelection')
    def tv_characters_clicked(self, sel, desel):
        for x, indexn in enumerate(sel.indexes()):
            if x == 0:
                print(self._proxy.data(self._proxy.index(indexn.row(), 1)))
                self.character_name = self._proxy.data(self._proxy.index(indexn.row(), 1),
                                                       Qt.ItemDataRole.DisplayRole)
                self.character_voice = self._proxy.data(self._proxy.index(indexn.row(), 2),
                                                        Qt.ItemDataRole.DisplayRole)
                character_novel = self._proxy.data(self._proxy.index(indexn.row(), 3),
                                                   Qt.ItemDataRole.DisplayRole)
                self.character_color = self._proxy.data(self._proxy.index(indexn.row(), 4),
                                                        Qt.ItemDataRole.DisplayRole)
                character_importance = self._proxy.data(self._proxy.index(indexn.row(), 6),
                                                        Qt.ItemDataRole.DisplayRole)
                self.character_service = self._proxy.data(self._proxy.index(indexn.row(), 7),
                                                          Qt.ItemDataRole.DisplayRole)
                self.ui.l_character_name.setText(self.character_name)
                self.ui.l_character_name.setStyleSheet(f"background-color: {self.character_color}")

                self.character_color_BAK = self.character_color
                self.character_voice_BAK = self.character_voice
                self.character_name_BAK = self.character_name
                self.character_service_BAK = self.character_service
                self.character_mod_populate(self.character_voice, self.character_name, character_novel,
                                            self.character_color, character_importance, self.character_service)
                # self.ui.cb_char_gender.setCurrentText(self.)

    def copy_paste(self):

        if self.sender() == self.ui.pb_Vcon_copy:
            pyperclip.copy(self.ui.l_con_isValid.text())
        elif self.sender() == self.ui.pb_last_error_copy:
            pyperclip.copy(self.ui.l_con_last_error.text())
        elif self.sender() == self.ui.pb_last_query_copy:
            pyperclip.copy(self.ui.l_con_last_query.text())
        elif self.sender() == self.ui.pb_status_copy:
            pyperclip.copy(self.ui.l_con_is_admin.text())
        elif self.sender() == self.ui.pb_user_name_copy:
            pyperclip.copy(self.ui.l_con_computer_name.text())

    def colordef(self):
        dialog_color = QColorDialog.getColor(QColor(self.old_color)).name()
        if dialog_color == "#000000":
            self.ui.le_char_color.setText(self.old_color)
        else:
            self.ui.le_char_color.setText(dialog_color)

    def character_mod_populate(self, character_voice="", character_name="", character_novel="",
                               character_color="", character_importance="", character_service=""):
        self.old_voice = character_voice
        self.old_name = character_name
        self.old_novel = character_novel
        self.old_color = character_color
        self.old_importance = character_importance
        self.old_service = character_service

        self.ui.le_char_character_name.setText(self.old_name)
        self.ui.cb_char_importances.setCurrentText(self.old_importance)
        self.ui.cb_char_novel.setCurrentText(self.old_novel)
        self.ui.le_char_color.setText(self.old_color)
        if self.old_voice == "":
            test("empty voice")
        else:
            self.ui.cb_char_name.setCurrentText(self.old_name)
            self.ui.cb_char_voice_code.setCurrentText(self.old_voice)
            voiceoptionquery = f"select phtv_gender, phtv_language,phtv_service,phtv_voice_type from play_ht_voices where phtv_value = '{self.old_voice}'"
            self.lastquery = voiceoptionquery
            query = QSqlQuery(db=self.con)
            query.exec(voiceoptionquery)
            test("query")
            while query.next():
                print(query.value(0))
                self.ui.cb_char_gender.setCurrentText(query.value(0))
                self.ui.cb_char_country.setCurrentText(query.value(1))
                self.ui.cb_char_service.setCurrentText(query.value(2))
                self.ui.cb_char_type.setCurrentText(query.value(3))
        self.cb_char_changed()
        # self.ui.cb_char_voice_code.hide()

    def populate_tv_lines(self):
        Hidden = True
        notHidden = False
        self.model_lines.setTable("lines")
        self.model_lines.setHeaderData(1, Qt.Orientation.Horizontal, "#")
        self.model_lines.setHeaderData(3, Qt.Orientation.Horizontal, "Name")
        self.model_lines.setHeaderData(4, Qt.Orientation.Horizontal, "Character Voice")
        self.model_lines.setHeaderData(7, Qt.Orientation.Horizontal, "Line Text")

        Lfilter = f"line_novel = '{self.ui.cb_novel.currentText()}' AND line_chapter = '{self.chapter_selection}'"
        self.model_lines.setFilter(Lfilter)
        self.model_lines.setSort(1, Qt.SortOrder.AscendingOrder)
        self.model_lines.select()
        self.ui.tv_lines.setModel(self.model_lines)
        self.ui.tv_lines.setColumnHidden(0, Hidden)
        self.ui.tv_lines.setColumnHidden(1, Hidden)
        self.ui.tv_lines.setColumnHidden(2, Hidden)
        self.ui.tv_lines.setColumnHidden(3, Hidden)
        self.ui.tv_lines.setColumnHidden(4, Hidden)
        self.ui.tv_lines.setColumnHidden(5, Hidden)
        self.ui.tv_lines.setColumnHidden(6, Hidden)
        self.ui.tv_lines.setColumnHidden(7, notHidden)
        self.ui.tv_lines.setColumnHidden(8, Hidden)
        self.ui.tv_lines.setColumnHidden(9, Hidden)
        self.ui.tv_lines.setColumnHidden(10, Hidden)
        self.ui.tv_lines.setColumnWidth(3, 100)
        self.ui.tv_lines.setColumnWidth(4, 125)
        self.ui.tv_lines.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.ui.tv_lines.setSelectionMode(QTableView.SelectionMode.MultiSelection)

        self.ui.tv_lines_split.setModel(self.model_lines)
        self.ui.tv_lines_split.setColumnHidden(0, Hidden)
        self.ui.tv_lines_split.setColumnHidden(1, notHidden)
        self.ui.tv_lines_split.setColumnHidden(2, Hidden)
        self.ui.tv_lines_split.setColumnHidden(3, notHidden)
        self.ui.tv_lines_split.setColumnHidden(4, Hidden)
        self.ui.tv_lines_split.setColumnHidden(5, Hidden)
        self.ui.tv_lines_split.setColumnHidden(6, Hidden)
        self.ui.tv_lines_split.setColumnHidden(7, Hidden)
        self.ui.tv_lines_split.setColumnHidden(8, notHidden)
        self.ui.tv_lines_split.setColumnHidden(9, Hidden)
        self.ui.tv_lines_split.setColumnHidden(10, Hidden)
        self.ui.tv_lines_split.setColumnWidth(1, 45)
        # self.tv_split_lines.setSelectionBehavior(QTableView.NoSelection)
        self.ui.tv_lines_split.setSelectionMode(QTableView.SelectionMode.NoSelection)
        self.ui.tv_lines_split.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)

        if not self.is_admin:
            self.ui.tv_lines.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.ui.tv_lines_split.verticalHeader().setVisible(False)

    def populate_tv_characters(self):

        self.model_characters.setTable("characters")
        self.model_characters.setFilter(f"character_novel = '{self.ui.cb_novel.currentText()}'")
        # self.model_characters.setSort(5, Qt.SortOrder.AscendingOrder)
        self.model_characters.setHeaderData(1, Qt.Orientation.Horizontal, "Name")
        self.model_characters.setHeaderData(2, Qt.Orientation.Horizontal, "Voice Name")
        self.model_characters.setHeaderData(5, Qt.Orientation.Horizontal, "usage")
        self.model_characters.setHeaderData(6, Qt.Orientation.Horizontal, "importance")
        self.model_characters.setHeaderData(10, Qt.Orientation.Horizontal, "voice service")

        self.model_characters.select()
        self._proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self._proxy.setSourceModel(self.model_characters)
        self._proxy.sort(5, Qt.SortOrder.DescendingOrder)
        self.ui.tv_characters.setModel(self._proxy)
        self.ui.tv_characters.setSortingEnabled(False)

        self.CharHeaderview.setEditable(1, True)
        # self.CharHeaderview.setEditable(6, True)

        self.ui.tv_characters.setModel(self._proxy)
        self.ui.tv_characters.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.ui.tv_characters.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.ui.tv_characters.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.ui.tv_characters.setColumnHidden(0, True)
        self.ui.tv_characters.setColumnHidden(3, True)
        self.ui.tv_characters.setColumnHidden(4, True)

    def count_update(self):  # count character occurence and update veiw and plot
        asd = 0
        countUpdateQuery = (f"select line_character, count(line_character) "
                            f"from lines "
                            f"where line_novel = '{self.ui.cb_novel.currentText()}'"
                            f"group by line_character")
        self.lastquery = countUpdateQuery
        query = QSqlQuery(db=self.con)
        query.exec(countUpdateQuery)
        while query.next():
            line_character = query.value(0)
            count = query.value(1)
            if line_character == "to-do" or line_character == "base character":
                pass
            else:
                indexmin = self.model_characters.match(self.model_characters.index(0, 1), Qt.ItemDataRole.DisplayRole,
                                                       f"{line_character}")
                self.model_characters.setData(self.model_characters.index(indexmin[0].row(), 5), count,
                                              Qt.ItemDataRole.EditRole)
        # self.make_plot()
        self.complete_called = False

    def status_change_chapter(self, Statusstate="complete"):
        test(f"statuschange{Statusstate}")
        self.complete_called = True
        self.model_chapter.setData(self.model_chapter.index(self.ui.cb_chapter.currentIndex(), 3),
                                   f"{Statusstate}",
                                   Qt.ItemDataRole.EditRole)
        self.count_update()

    def pb_characters_clicked(self):
        if self.sender() == self.ui.pb_make_todo:
            self.character_name = "to-do"
            self.character_voice = "en-AU-Standard-A"
            self.character_color = "#ffffff"
            self.character_service = "none"
            self.ui.l_character_name.setText(self.character_name)
            self.ui.l_character_name.setStyleSheet(f"background-color: {self.character_color}")

        elif self.sender() == self.ui.pb_revert:
            self.character_name = self.character_name_BAK
            self.character_voice = self.character_voice_BAK
            self.character_color = self.character_color_BAK
            self.character_service = self.character_service_BAK
            self.ui.l_character_name.setText(self.character_name)
            self.ui.l_character_name.setStyleSheet(f"background-color: {self.character_color}")

    @pyqtSlot()
    def focus_out(self):  # act on line from tableview focus out
        self.LselectedRows = self.ui.tv_lines.selectionModel().selectedRows()
        self.ui.tv_lines.clearSelection()

    def cb_char_changed(self):
        test("cb changed")
        gender = self.ui.cb_char_gender.currentText()
        country = self.ui.cb_char_country.currentText()
        type = self.ui.cb_char_type.currentText()
        service = self.ui.cb_char_service.currentText()
        if gender == "All":
            gender = ""
        else:
            gender = f"and phtv_gender = '{gender}'"
        if country == "All":
            country = ""
        else:
            country = f"and phtv_language ILIKE '%{country}%'"
        if type == "All":
            type = ""
        else:
            type = f"and phtv_voice_type = '{type}'"
        if service == "All":
            service = ""
        else:
            service = f"and phtv_service = '{service}' "

        self.model_playht_voice.setFilter(f"phtv_id > 0 {gender} {country} {type} {service}")
        self.model_playht_voice.select()

    def name_changed(self):
        self.ui.pb_char_add.setText(
            f"add {self.ui.le_char_character_name.text()}\nas a new character for {self.ui.cb_char_novel.currentText()}")
        self.ui.pb_char_edit.setText(
            f"edit {self.ui.le_char_character_name.text()}\nfrom {self.ui.cb_char_novel.currentText()}")
        self.ui.pb_char_test_voice.setText(
            f"play voice sample ")

    def name_voice_sync(self):
        if self.sender() == self.ui.cb_char_name:
            self.ui.cb_char_voice_code.setCurrentIndex(self.ui.cb_char_name.currentIndex())
            # print(self.cb_voice_code.currentText())
        elif self.sender() == self.ui.cb_char_voice_code:
            self.ui.cb_char_name.setCurrentIndex(self.ui.cb_char_voice_code.currentIndex())

    @pyqtSlot('QItemSelection', 'QItemSelection')
    def tv_lines_clicked(self, selected, deselected):
        if selected:
            if self.workerSave.paused:
                self.workerSave.Resume()
            self.progressionChapter()
            for x, index in enumerate(selected.indexes()):
                if x % 10 == 0:
                    if self.character_name != "":
                        self.model_lines.setData(self.model_lines.index(index.row(), 3), f"{self.character_name}",
                                                 Qt.ItemDataRole.EditRole)
                    else:
                        self.model_lines.setData(self.model_lines.index(index.row(), 3), f"base character",
                                                 Qt.ItemDataRole.EditRole)
                    if self.character_voice != "":
                        self.model_lines.setData(self.model_lines.index(index.row(), 4), f"{self.character_voice}",
                                                 Qt.ItemDataRole.EditRole)
                    else:
                        self.model_lines.setData(self.model_lines.index(index.row(), 4), f"en-AU-Standard-A",
                                                 Qt.ItemDataRole.EditRole)
                    if self.character_color != "":
                        self.model_lines.setData(self.model_lines.index(index.row(), 8), f"{self.character_color}",
                                                 Qt.ItemDataRole.EditRole)
                    else:
                        self.model_lines.setData(self.model_lines.index(index.row(), 8), f"#ffffff",
                                                 Qt.ItemDataRole.EditRole)
                    if self.user_computer != "":
                        self.model_lines.setData(self.model_lines.index(index.row(), 9), f"{self.user_computer}",
                                                 Qt.ItemDataRole.EditRole)
                    else:
                        self.model_lines.setData(self.model_lines.index(index.row(), 9), f"user_computer",
                                                 Qt.ItemDataRole.EditRole)
                    if self.character_service != "":
                        self.model_lines.setData(self.model_lines.index(index.row(), 10), f"{self.character_service}",
                                                 Qt.ItemDataRole.EditRole)
                    else:
                        self.model_lines.setData(self.model_lines.index(index.row(), 10), f"service",
                                                 Qt.ItemDataRole.EditRole)

    def progressionChapter(self, all_count=0, to_do_count=0):  # update progress bar for chapter line completion
        chapterProgressionQuery = (f"select line_character, count(*) "
                                   f"from lines "
                                   f"where line_novel = '{self.ui.cb_novel.currentText()}'"
                                   f"and line_chapter = '{self.chapter_selection}'"
                                   f"group by line_character")
        self.lastquery = chapterProgressionQuery
        query = QSqlQuery(db=self.con)
        query.exec(chapterProgressionQuery)
        while query.next():
            name = query.value(0)
            line_count = query.value(1)
            if name == "to-do":
                all_count += line_count
                to_do_count += line_count
            else:
                all_count += line_count

        done_count = all_count - to_do_count
        self.ui.prbr_chapter.setMaximum(all_count)
        self.ui.prbr_chapter.setValue(done_count)

    def progressionNovel(self, all_count=0, to_do_count=0):  # update progress bar for novel chapter completion
        novelProgressionQuery = (f"select chapter_status, count(*) "
                                 f"from chapters "
                                 f"where chapter_novel = '{self.ui.cb_novel.currentText()}'"
                                 f"group by chapter_status")
        self.lastquery = novelProgressionQuery
        query = QSqlQuery(db=self.con)
        query.exec(novelProgressionQuery)
        while query.next():
            name = query.value(0)
            count = query.value(1)
            if name == "to-do" or name == "WIP" or name == "active":
                all_count += count
                to_do_count += count
            else:
                all_count += count

        still_count = all_count - to_do_count
        self.ui.prbr_novel.setMaximum(all_count if all_count > 0 else all_count + 1)
        self.ui.prbr_novel.setValue(still_count if still_count > 0 else still_count + 1)

    def load_chap(self, statusChapter=None):  # load chapter at start or when asked
        self.chapter_selection = self.model_chapter.data(
            self.model_chapter.index(self.ui.cb_chapter.currentIndex(), 1))
        print(self.chapter_selection)
        # print(self.cb_chapter.currentText(),statusChapter)
        if statusChapter:
            if statusChapter != "complete":
                self.model_chapter.setData(self.model_chapter.index(self.ui.cb_chapter.currentIndex(), 3), f"WIP",
                                           Qt.ItemDataRole.EditRole)

        self.populate_tv_lines()
        self.progressionChapter()

    def load_data(self, f=True):
        if f:
            self.progressionNovel()
            self.populate_tv_characters()
            self.load_chap()

    def deleteRow(self):
        if self.is_admin:
            index_list = []
            for model_index in self.LselectedRows:
                index = QPersistentModelIndex(model_index)
                index_list.append(index)
            for index in index_list:
                self.model_lines.removeRow(index.row())
            self.model_lines.submitAll()
            self.model_lines.select()
        else:
            QMessageBox.information(
                self,
                f"{appname} - forbidden",
                f"you don't have permission to delete lines",
            )

    def insertRow(self):
        if not self.is_admin:
            QMessageBox.information(
                self,
                f"{appname} - info",
                "you can't duplicate line"
                "\ntalk to Duke_archibald on the official LOTM discord to ask for that"
                f"\n{self.discord_invite}",
            )
            return

        for model_index in self.LselectedRows:
            r = self.model_lines.record()
            for z in range(self.model_lines.columnCount()):
                data = self.model_lines.data(self.model_lines.index(model_index.row(), z), Qt.ItemDataRole.DisplayRole)
                Hname = self.model_lines.record().fieldName(z)
                if z == 1:
                    data = round(data + .1, 1)
                if z == 0:
                    r.setGenerated(Hname, False)
                if z == 9:
                    r.setValue(Hname, self.user_computer)
                else:
                    r.setValue(Hname, data)
            self.model_lines.insertRecord(-1, r)

            if self.model_lines.submitAll():
                self.model_lines.select()
            else:
                QMessageBox.information(
                    self,
                    f"{appname} - error",
                    f"there was an error while adding line"
                    f"\n{self.lines_model.lastError().text()}"
                    f"\nif blank no error was reported (wierd error)",
                )

    def pause_worker(self):
        """pause worker only if user can edit line
     (line edit available only to admin and moderator user)"""
        if self.is_admin:
            self.workerSave.Pause()

    def comboboxChanged(self):
        print("001", self.model_chapter.data(
            self.model_chapter.index(self.ui.cb_chapter.currentIndex(), 1)))
        self.ui.prbr_TTS.setValue(0)
        if self.complete_called:
            test("complete called")
        else:
            if self.sender() == self.ui.cb_novel:  # update progression novel and set filter complete or not
                print("novel")
                self.progressionNovel()
                self.complete_check()
                self.model_chapter.select()
                self.load_chap()
                self.populate_tv_characters()
                self.character_mod_populate(character_novel=self.ui.cb_novel.currentText())

            elif self.sender() == self.ui.cb_chapter:
                print("002", self.model_chapter.data(
                    self.model_chapter.index(self.ui.cb_chapter.currentIndex(), 1)))
                print("chapter")
                # fetch chapter_num (3) from Chapter name/selected index (cb.currentindex)
                status = self.model_chapter.data(
                    self.model_chapter.index(self.ui.cb_chapter.currentIndex(), 3))

                if status == "complete":
                    if self.is_admin:
                        self.load_chap(status)
                    else:
                        QMessageBox.information(
                            self,
                            f"{appname} - forbidden",
                            f"this chapter is completed"
                            f"\nyou don't have access to it",
                        )
                        self.chapter_selection = ""
                        self.progressionChapter(1, 1)
                        self.populate_tv_lines()
                else:
                    self.load_chap()

        self.make_plot()

    def complete_check(self):
        self.model_chapter.setFilter(f"chapter_novel = '{self.ui.cb_novel.currentText()}' and "
                                     f"chapter_status != 'complete'")
        if self.is_admin:
            if self.ui.checkbox_complete.isChecked():
                self.model_chapter.setFilter(f"chapter_novel = '{self.ui.cb_novel.currentText()}'")
        print(self.model_chapter.filter())

    @pyqtSlot(int, str)
    def on_text_changed(self, col, text):
        self._proxy.setFilterKeyColumn(col)
        self._proxy.setFilterWildcard("*{}*".format(text) if text else "")

    def save_refresh(self, worker=False):
        print("work", worker)
        if not worker:
            self.model_lines.submitAll()
            self.model_lines.select()
            self.status_change_chapter(Statusstate="WIP")
        else:
            infomessagebox = QMessageBox(self)
            infomessagebox.setWindowTitle(f"{appname} - autoSave")
            infomessagebox.setText("auto save and sync please wait")
            infomessagebox.setStandardButtons(QMessageBox.StandardButton.NoButton)
            infomessagebox.open()
            self.app.processEvents()
            self.model_lines.submitAll()
            self.model_lines.select()
            self.status_change_chapter(Statusstate="WIP")
            infomessagebox.done(0)

        # self.make_plot()

    def readSettings(self):
        try:
            self.restoreGeometry(self.settings.value("geometry"))
            self.restoreState(self.settings.value("windowState"))
        except:
            print("new pc no setting")

    # endregion completed_function

    def closeEvent(self, a0: QCloseEvent) -> None:
        try:
            for entry in os.scandir("temps"):
                os.remove(entry.path)
        except IOError as e:
            # print(str(e))
            QMessageBox.information(self, "IO error", str(e), )

        self.settings.setValue('lastNovel', self.ui.cb_novel.currentText())
        self.settings.setValue('lastChapter', self.ui.cb_chapter.currentText())
        self.settings.setValue('geometry', self.saveGeometry())
        self.settings.setValue('windowState', self.saveState())
        self.workerSave.stopE()
        self.con.close()
