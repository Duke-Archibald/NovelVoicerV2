import getpass
import os
import pathlib
import pickle
import re
import shutil
import socket

import pyperclip
from PyQt6.QtSql import QSqlQuery
from PyQt6.QtWidgets import QMessageBox

appname = "Characters Voice Selector"
last_query = ""
test_val = 0
resourcesCon = ""
html_blacklist = ['[document]', 'noscript', 'header', 'html', 'meta', 'head', 'input', 'script', 'style']
discord1 = "https://discord.com/invite/mFFfTx5"

def banned_user(con):

    banned_user = []
    banned_query = QSqlQuery(db=con)
    banned_query_text = f"select ban_name from ban_user"

    banned_query.exec(banned_query_text)
    while banned_query.next():
        banned_user.append(banned_query.value(0))
    comp_user = getpass.getuser()
    comp_name = socket.gethostname()
    user_computer1 = f"{comp_user}-{comp_name}"
    if user_computer1 in banned_user:
        QMessageBox.information(
            None,
            f"{appname} - forbidden",
            f"you were banned from this app"
            f"\ntalk to Duke_archibald on the LOTM discord if you think this is wrong"
            f"\ninformation were copied in your clipborad(ctrl+v to paste them)",
        )
        toclip = discord1 + " " + user_computer1
        pyperclip.copy(toclip)
        return True
    return False
def admin_user(con, user_computer):
    admin_user = []
    mod_user = []

    query1 = QSqlQuery(db=con)
    admin_query_text = "select admin_name from admin_user"
    query1.exec(admin_query_text)
    while query1.next():
        admin_user.append(query1.value(0))

    query2 = QSqlQuery(db=con)
    mod_query_text = f"select mod_name from mod_user"
    query2.exec(mod_query_text)
    while query2.next():
        mod_user.append(query2.value(0))
    admin_mod_user = admin_user + mod_user
    if user_computer in admin_mod_user:
        return True
    else:
        return False
def testmatch(match):
    m1 = match.group(1)
    m2 = match.group(2)
    # print(m1,"--",m2)
    punct = "?!…"
    if m2 in punct:
        return f"{m1}"
    else:
        return f"{m1}\n{m2}"


def test(where="somewhere"):
    global test_val
    print(f"{where}-{test_val}")
    test_val += 1


def TTS_format(line):
    if toignore(line):
        return "toingnore"
    line = toreplace(line)
    # t1 = re.sub(r"(“[^”]*” *)", "\n\\1\n", line)
    t1 = re.sub(r"([“|\"][^”|\"]*[”|\"] *)", "\n\\1\n", line)
    t2 = re.sub(r"(… |\? |: |! )([^?!…])", testmatch, t1)
    t3 = re.sub(r"(…' |\.' |,' )", "\\1\n", t2)
    return t3


def invalid_tag(soup):
    # print("invalid")
    invalid_tags = ['<em>']
    for tag in invalid_tags:
        for match in soup.findAll(tag):
            match.unwrap()
    return soup


def padding(num, pad):
    num1 = str(num)
    num1 = num1.zfill(pad)
    return num1


def toreplace(toReplace):
    toReplace = toReplace.replace("mr.", "Mr")
    toReplace = toReplace.replace("Mr.", "Mr")
    toReplace = toReplace.replace("miss.", "miss")
    toReplace = toReplace.replace("Miss.", "Miss")
    toReplace = toReplace.replace("mrs.", "mrs")
    toReplace = toReplace.replace("Mrs.", "Mrs")
    toReplace = toReplace.replace(" ms.", " ms")
    toReplace = toReplace.replace(" Ms.", " Ms")
    toReplace = toReplace.replace(" st.", " st")
    toReplace = toReplace.replace(" St.", " St")
    toReplace = toReplace.replace("b*stard", "bastard")
    toReplace = toReplace.replace("b*stards", "bastards")
    toReplace = toReplace.replace("B*stard", "Bastard")
    toReplace = toReplace.replace("B*stards", "Bastards")
    toReplace = toReplace.replace("b*st*rd", "bastard")
    toReplace = toReplace.replace("b*st*rds", "bastards")
    toReplace = toReplace.replace("B*st*rd", "Bastard")
    toReplace = toReplace.replace("B*st*rds", "Bastards")
    toReplace = toReplace.replace("grande", "grand")
    toReplace = toReplace.replace("Grande", "Grand")
    toReplace = toReplace.replace("f**k", "fuck")
    toReplace = toReplace.replace("f*ck", "fuck")
    toReplace = toReplace.replace("fu*k", "fuck")
    toReplace = toReplace.replace("F**k", "Fuck")
    toReplace = toReplace.replace("F*ck", "Fuck")
    toReplace = toReplace.replace("Fu*k", "Fuck")
    toReplace = toReplace.replace("Motherf*cker", "Motherfucker")
    toReplace = toReplace.replace("motherf*cker", "motherfucker")
    toReplace = toReplace.replace("b*tch", "bitch")
    toReplace = toReplace.replace("b*tchs", "bitchs")
    toReplace = toReplace.replace("B*tch", "Bitch")
    toReplace = toReplace.replace("B*tchs", "Bitchs")
    toReplace = toReplace.replace("f**king", "fucking")
    toReplace = toReplace.replace("F**king", "Fucking")
    toReplace = toReplace.replace("sh*t", "shit")
    toReplace = toReplace.replace("Sh*t", "Shit")
    toReplace = toReplace.replace("f*cked", "fucked")
    toReplace = toReplace.replace("F*cked", "Fucked")
    toReplace = toReplace.replace("f*ucking", "fucking")
    toReplace = toReplace.replace("F*ucking", "Fucking")
    toReplace = toReplace.replace("dogsh*t", "dogshit")
    toReplace = toReplace.replace("Dogsh*t", "Dogshit")
    toReplace = toReplace.replace("godd*mmit", "goddammit")
    toReplace = toReplace.replace("Godd*mmit", "Goddammit")
    toReplace = toReplace.replace("a**holes", "assholes")
    toReplace = toReplace.replace("A**holes", "Assholes")
    toReplace = toReplace.replace("a**", "ass")
    toReplace = toReplace.replace("A**", "Ass")
    toReplace = toReplace.replace("ret*rd", "retard")
    toReplace = toReplace.replace("ret*rds", "retards")
    toReplace = toReplace.replace("Ret*rd", "Retard")
    toReplace = toReplace.replace("Ret*rds", "Retards")
    toReplace = toReplace.replace("p*ss", "piss")
    toReplace = toReplace.replace("P*ss", "Piss")
    toReplace = toReplace.replace("bullsh*t", "bullshit")
    toReplace = toReplace.replace("Bullsh*t", "Bullshit")
    toReplace = toReplace.replace("motherf**king", "motherfucking")
    toReplace = toReplace.replace("Motherf**king", "Motherfucking")
    toReplace = toReplace.replace("~", "")
    toReplace = toReplace.replace("foock", "fuck")
    toReplace = toReplace.replace("～", "")
    toReplace = toReplace.replace("◆", "")
    toReplace = toReplace.replace("<p></p>", "")
    toReplace = toReplace.replace("<em>", "")
    toReplace = toReplace.replace("</em>", "")
    # toReplace=toReplace.replace("", "")
    # toReplace=toReplace.replace("", "")
    return toReplace


def toignore(p):
    if "Translator:" in str(p):
        return True
    elif "#StayInHome" in str(p):
        return True
    elif "Last Chapter" in str(p):
        return True
    elif "Next Chapter" in str(p):
        return True
    elif "#StayInHome" in str(p):
        return True
    elif "Audiobook" in str(p):
        return True
    elif "Novels.pl" in str(p):
        return True
    elif "YouTube Channel" in str(p):
        return True
    elif "Patreon" in str(p):
        return True
    elif "Cookie Policy" in str(p):
        return True
    elif "©" in str(p):
        return True
    elif "DCMA" in str(p):
        return True
    elif "Editor:" in str(p):
        return True
    else:
        return False


def abbrev(string):
    r = re.compile(r"(?:(?<=\s)|^)(?:[a-z]|\d+)", re.I)

    abbreviation = ''.join(r.findall(string))
    return abbreviation


def delete_temp_file(filenameTTS):
    if pathlib.Path(f"temps/{filenameTTS}").exists():
        os.remove(f"temps/{filenameTTS}")


def delete_all_temp_file():
    folder = "./temps"
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def readpkl(fileN):
    with open(f"temps/{fileN}", "rb") as file:
        out = pickle.load(file)
        print(out)
        for line_num, line_cont in out.items():
            print(f"{line_num}")
            for key in line_cont:
                print(f"\t{key}: {line_cont[key]}")


def cleaning(line):
    t2 = re.sub(r"[“|\"]([^”\"\s?!:]*)[”|\"] *", "'\\1' ", line)
    return t2
