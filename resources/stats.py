import os
from datetime import datetime
from pprint import pprint

import numpy as np
import pandas as pd
from PyQt6.QtSql import QSqlQuery
from matplotlib import pyplot as plt
import plotly.express as px


def interactive_pie(novel, con):
    query1 = QSqlQuery(db=con)
    query2 = QSqlQuery(db=con)
    preQ = f"select chapter_num from chapters where chapter_novel = '{novel}' and chapter_status = 'complete' or chapter_status = 'WIP' order by chapter_num"
    # preQ = f"select chapter_num from chapters where chapter_novel = '{novel}' order by chapter_num"
    print(preQ)
    query1.exec_(preQ)
    chapters = []

    linked_100s = []
    linked_10s = []
    linked_chapter = []
    linked_characters = []
    linked_lines_count = []
    linked_lines_text = []
    linked_colors = []
    linked_colors_R = []
    linked_colors_G = []
    linked_colors_B = []
    while query1.next():
        chapters.append(query1.value(0))
    s10 = "0-10"
    s100 = "0-100"
    for chapter in chapters:
        preQ = f"select line_character, count(line_character),line_color " \
               f"from lines " \
               f"where line_novel = '{novel}' " \
               f"and line_chapter = '{chapter}' " \
               f"group by line_character,line_color,line_text " \
               f"order by count(line_character) DESC"
        print(preQ)
        query2.exec_(preQ)
        while query2.next():
            x = int(chapter)

            if x % 10 == 0:
                s10 = f"{x}-{x + 9}"
                if x % 100 == 0:
                    s100 = f"{x}-{x + 99}"
            linked_10s.append(s10)
            linked_100s.append(s100)

            linked_chapter.append(str(chapter))
            linked_characters.append(query2.value(0))
            linked_lines_count.append(query2.value(1))
            linked_colors.append(query2.value(2))
            # linked_lines_text.append(query2.value(3))

    df = pd.DataFrame(
        dict(s100=linked_100s,
             s10=linked_10s,
             chapters=linked_chapter,
             characters=linked_characters,
             # text=linked_lines_text,
             colors=linked_colors,
             lines=linked_lines_count)
    )
    linecolors = pd.Series(df.colors.values, index=df.characters).to_dict()
    colors1 = {"(?)": "lightgrey"}
    for x, y in linecolors.items():
        colors1[x] = y
    pprint(colors1)
    fig = px.sunburst(
        data_frame=df,
        path=["s100", 's10', "chapters", "characters"],  # Root, *branches, leaves
        values="lines",
        color="characters",
        color_discrete_map=colors1,
        maxdepth=3,
        branchvalues="total",
        title="character lines per chapters",
    )

    fig.update_traces(textinfo='label+percent parent+value')
    fig.update_traces(hovertemplate='Name: %{label}<br>lines: %{value}')
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    fig.show()


def plot(figure, pb_plot_toggle, con, cb_novel, chapter_selection, is_admin, canvas, cb_chapter):
    figure.clear()
    colors = []
    Clabel = []
    y = np.array([])
    explode = []
    labelL = []
    query = QSqlQuery(db=con)
    if pb_plot_toggle.isChecked():
        preQ = (f"select line_character, count(line_character),line_color "
                f"from lines "
                f"where line_novel = '{cb_novel.currentText()}' "
                f"and line_chapter = '{chapter_selection}' "
                f"group by line_character,line_color "
                f"order by count(line_character) DESC")
    else:
        preQ = (f"select line_character, count(line_character),line_color "
                f"from lines "
                f"where line_novel = '{cb_novel.currentText()}' "
                f"group by line_character,line_color "
                f"order by count(line_character) DESC")
    print("pie",preQ)
    query.exec_(preQ)
    while query.next():
        char_name = query.value(0)
        if pb_plot_toggle.isChecked():
            pass
        elif len(Clabel) >= 10:
            break
        if pb_plot_toggle.isChecked():
            pass
        elif char_name == "to-do" or char_name == "base character":
            continue

        if pb_plot_toggle.isChecked():
            pass
        else:
            if query.value(1) < 50:
                continue

        if query.value(1) <= 500:
            explode.append(0.01)
        elif 101 <= query.value(1) <= 1000:
            explode.append(.01)
        elif 1001 <= query.value(1) <= 10000:
            explode.append(.01)
        else:
            explode.append(0.01)
        Clabel.append(query.value(0))
        y = np.append(y, query.value(1))
        colors.append(query.value(2))
    patches, labels, pct_texts = plt.pie(y,
                                         labels=Clabel,
                                         explode=explode,
                                         rotatelabels=True,
                                         colors=colors,
                                         autopct=lambda p: f'{p:.2f}% ({p * sum(y) / 100 :.0f} lines)',
                                         pctdistance=.5,
                                         labeldistance=1.05)
    for label, pct_text, y in zip(labels, pct_texts, y):
        pct_text.set_rotation(label.get_rotation())
        labelL.append(f"{label.get_text()}, {pct_text.get_text()}")
        if pb_plot_toggle.isChecked():
            if y < 10:
                pct_text.set_text("")
                label.set_text(f"{label.get_text()} ({int(y)} lines)")
        else:
            if y < 100:
                pct_text.set_text("")
                label.set_text(f"{label.get_text()} ({int(y)} lines)")

        label.set_rotation(0)
    if pb_plot_toggle.isChecked():
        plt.legend(loc=2, bbox_to_anchor=(0, 1.35), labels=labelL, title=cb_chapter.currentText())
    else:
        plt.legend(loc=2, bbox_to_anchor=(0, 1.35), labels=labelL, title=cb_novel.currentText())
    plt.subplots_adjust(top=1.05,
                        bottom=0,
                        left=0,
                        right=.85,
                        hspace=0,
                        wspace=0)
    figure.patch.set_facecolor('#253545')
    if is_admin:
        folderName = r"H:\texte\Novels\005_image_files\stats"
        os.makedirs(os.path.dirname(f"{folderName}{cb_novel.currentText()}/"), exist_ok=True)
        if pb_plot_toggle.isChecked():
            plt.savefig(
                f"{folderName}{cb_novel.currentText()}/{cb_chapter.currentText().replace(':', ' -')}.png")
        else:
            plt.savefig(f"{folderName}{cb_novel.currentText()}/{cb_novel.currentText()}.png")

    canvas.draw()


def characterStat(con, text, voice):
    month = datetime.now().strftime("%B")
    year = datetime.now().strftime("%Y")
    charactercountS = 0
    charactercountW = 0
    overW = False
    overS = False
    charcount = (len(text))
    Vtype = (voice.split("-")[2])
    # print(Vtype)
    Qpre1 = f"Select stats_char,stats_voice_type from stats where stats_month = '{month}' and stats_year = '{year}'"
    # Qpre1 = f"Select stats_char,stats_voice_type from stats where stats_month = '{month}' and stats_year = '{year}' and stats_voice_type = '{Vtype}'"
    # print(Qpre1)
    query = QSqlQuery(db=con)
    query.exec_(Qpre1)


    if query.next():
        query.first()
        x=0
        while query.next():
            x+=1
            print(Vtype,query.value(1))

            if query.value(1) == "Standard":
                if query.value(0) > 4000000:
                    overS = True
                # print("st",x,Vtype,query.value(0))
                charactercountS = query.value(0)
                if Vtype == "Standard":
                    query2 = QSqlQuery(db=con)
                    Qpre2 = f"update stats set stats_char = {query.value(0) + charcount} where stats_month = '{month}' and stats_year = '{year}' and stats_voice_type = 'Standard'"
                    # print(Qpre2)
                    query2.exec_(Qpre2)

            if query.value(1) == "Wavenet":
                if query.value(0) > 1000000:
                    overW = True
                # print("wa",x,Vtype,query.value(0))
                charactercountW = query.value(0)
                if Vtype == "Wavenet":
                    query2 = QSqlQuery(db=con)
                    Qpre2 = f"update stats set stats_char = {query.value(0) + charcount} where stats_month = '{month}' and stats_year = '{year}' and stats_voice_type = 'Wavenet'"
                    # print(Qpre2)
                    query2.exec_(Qpre2)

    else:
        query3 = QSqlQuery(db=con)
        Qpre3 = f"insert into stats (stats_month,stats_year,stats_voice_type,stats_char) values ('{month}','{year}','{Vtype}',{charcount})"
        # print(Qpre3)
        query3.exec_(Qpre3)
        # print(con.lastError().databaseText())
    return overW, charactercountW, overS, charactercountS

def characterStat2(con, text, voice):
    month = datetime.now().strftime("%B")
    year = datetime.now().strftime("%Y")
    charcount = (len(text))
    Vtype = (voice.split("-")[2])
    Qpre1 = f"Select stats_char,stats_voice_type from stats where stats_month = '{month}' and stats_year = '{year}' and stats_voice_type = '{Vtype}'"
    print(Qpre1)
    query = QSqlQuery(db=con)
    query.exec_(Qpre1)
    if query.next():
        query2 = QSqlQuery(db=con)
        Qpre2 = f"update stats set stats_char = {query.value(0) + charcount} where stats_month = '{month}' and stats_year = '{year}' and stats_voice_type = '{Vtype}'"
        # print(Qpre2)
        query2.exec_(Qpre2)

    else:
        query3 = QSqlQuery(db=con)
        Qpre3 = f"insert into stats (stats_month,stats_year,stats_voice_type,stats_char) values ('{month}','{year}','{Vtype}',{charcount})"
        # print(Qpre3)
        query3.exec_(Qpre3)
        # print(con.lastError().databaseText())
