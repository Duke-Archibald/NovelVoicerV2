import os
from pprint import pprint

import numpy as np
import pandas as pd
import plotly
from PyQt5.QtSql import QSqlQuery
import plotly.express as px
from matplotlib import pyplot as plt
from qdarkstyle.dark.palette import DarkPalette


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
    print("pie", preQ)
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
        folderName = r"D:\Novels\005_image_files\stats/"
        os.makedirs(os.path.dirname(f"{folderName}{cb_novel.currentText()}/"), exist_ok=True)
        if pb_plot_toggle.isChecked():
            plt.savefig(
                f"{folderName}{cb_novel.currentText()}/{cb_chapter.currentText().replace(':', ' -')}.png")
        else:
            plt.savefig(f"{folderName}{cb_novel.currentText()}/{cb_novel.currentText()}.png")

    canvas.draw()


def interactive_pie(novel, con, ui):
    query1 = QSqlQuery(db=con)
    query2 = QSqlQuery(db=con)
    preQ1 = (f"select chapter_num "
             f"from chapters "
             f"where chapter_novel = '{novel}' "
             f"and chapter_status in ('complete', 'WIP') "
             f"order by chapter_num")
    preQ1_1 = (f"select chapter_num "
               f"from chapters "
               f"where chapter_novel = '{novel}' "
               f"and chapter_status in ('complete', 'WIP', 'to-do') "
               f"order by chapter_num")
    query1.exec_(preQ1)
    linked_100s = []
    linked_10s = []
    linked_chapter = []
    linked_characters = []
    linked_lines_count = []
    linked_lines_text = []
    linked_colors = []

    overall_color = {}
    s10 = "1-10"
    s100 = "1-100"
    while query1.next():
        preQ2 = (f"select line_character, count(line_character),line_color "
                 f"from lines "
                 f"where line_novel = '{novel}' "
                 f"and line_chapter = '{query1.value(0)}' "
                 f"group by line_character,line_color "
                 f"order by count(line_character) DESC")
        preQ2_1 = (f"select line_character,count(line_character),line_color,line_text "
                   f"from lines "
                   f"where line_novel = '{novel}' "
                   f"and line_chapter = '{query1.value(0)}' "
                   f"group by line_character,line_color "
                   f"order by count(line_character) DESC")
        # print(preQ2)
        query2.exec_(preQ2)
        chapter_max = 0
        s10_max = 0
        s100_max = 0

        while query2.next():

            x = int(query1.value(0))
            if (x - 1) % 10 == 0:
                s10 = f"{x}-{x + 9}"
                overall_color[s10] = "#ffffff", s10_max
            if (x - 1) % 100 == 0:
                s100 = f"{x}-{x + 99}"
                overall_color[s100] = "#ffffff", s100_max

            if query2.value(0) != "Narrator":
                if query2.value(1) > chapter_max:
                    chapter_max = query2.value(1)
                    overall_color[query1.value(0)] = query2.value(2), chapter_max
                    if chapter_max > s10_max and chapter_max > overall_color[s10][1]:
                        s10_max = chapter_max
                        overall_color[s10] = query2.value(2), s10_max
                        if s10_max > s100_max and s10_max > overall_color[s100][1]:
                            s100_max = s10_max
                            overall_color[s100] = query2.value(2), s100_max

            linked_10s.append(s10)
            linked_100s.append(s100)

            linked_chapter.append(query1.value(0))
            linked_characters.append(query2.value(0))
            linked_lines_count.append(query2.value(1))
            linked_colors.append(query2.value(2))
            # linked_lines_text.append(query2.value(3)) # text option

    df = pd.DataFrame(
        dict(
            s100=linked_100s,
            s10=linked_10s,
            chapters=linked_chapter,
            characters=linked_characters,
            # text=linked_lines_text,
            colors=linked_colors,
            lines=linked_lines_count)
    )
    df.to_csv("banana.csv")
    linecolors = pd.Series(df.colors.values, index=df.characters).to_dict()
    colors1 = {"(?)": "gray"}
    for x, y in linecolors.items():
        colors1[x] = y
    overall_colors = dict((k, v[0]) for k, v in overall_color.items())
    pprint(overall_colors)
    colors2 = dict(colors1.items() | overall_colors.items())

    fig = px.sunburst(
        data_frame=df,
        path=["s100", 's10', "chapters", "characters"],  # Root, *branches, leaves
        values="lines",
        color="characters",
        color_discrete_map=colors2,
        maxdepth=3,
        branchvalues="total",
        title="character lines per chapters",
    )

    fig.update_traces(textinfo='label+percent root+percent parent+value')
    fig.update_traces(hovertemplate='Name: %{label}<br>lines: %{value}')
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.update_traces(marker_colors=[colors2[cat] for cat in fig.data[-1].labels])
    fig.update_layout({
        'plot_bgcolor': '#253545',
        'paper_bgcolor': '#253545',
    })
    ui.setHtml(fig.to_html(include_plotlyjs='cdn'))
    ui.setStyleSheet("background-color: '#253545';")
