import json
import os

myWindowOpen = False
loginWindowOpen = False


def setMyWindowOpen(w):
    """设置MyWindow是否打开"""
    global myWindowOpen
    myWindowOpen = w


def getMyWindowOpen():
    """获得MyWindow是否打开"""
    return myWindowOpen


def setLoginWindowOpen(w):
    """设置LoginWindow是否打开"""
    global loginWindowOpen
    loginWindowOpen = w


def getLoginWindowOpen():
    """获得LoginWindow是否打开"""
    return loginWindowOpen


def getDefaultEmailAndPassword():
    """获得用户上次登陆成功的用户名和密码"""
    if os.path.exists("user.json"):
        with open("user.json", "r") as file:
            text = json.load(file)
        return text["email"], text["password"]
    else:
        return "", ""


def setDefaultEmailAndPassword(email, password):
    """设置用户登陆成功的用户名和密码"""
    user = {"email": email, "password": password}
    text = json.dumps(user)
    with open("user.json", "w") as file:
        file.write(text)
