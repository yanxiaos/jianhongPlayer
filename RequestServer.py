import json
import requests

URL = "http://123.207.189.27:18081/jianhong/"

# URL = "http://127.0.0.1:8000/jianhong/"


def get_token():
    try:
        with open("token.json", "r") as file:
            text = json.load(file)
            token = text["token"]
            return token
    except FileNotFoundError or Exception:
        return None


def set_token(token):
    text = {"token": token}
    text = json.dumps(text)  # 将字典转换json格式
    with open("token.json", "w") as file:
        file.write(text)


# 登录
def login(email, password):
    r = requests.post(URL + "login/", data={"email": email, "password": password})
    text = r.json()
    if text["status"] == 200:
        token = text["token"]
        set_token(token)

    return r.json()


# 退出登录
def logout():
    r = requests.get(URL + "logout/", params={"token": get_token()})
    return r.json()


# 注册
def register(username, email, password):
    r = requests.post(URL + "register/", data={"username": username, "email": email, "password": password})
    return r.json()


# 发送激活邮件
def sendActivationEmail(email):
    r = requests.get(URL + "sendActivationEmail/", params={"email": email})
    return r.json()


# 获取音乐文件
def getMusic(types, name):
    """types: play,download"""
    music = requests.get(URL + "getMusic/", params={"token": get_token(), "types": types, "name": name})
    return music


# 获取音乐列表
def getMusicList(types, name=None):
    """types: byName,byCollection,recommend"""
    """byCollection name: Default(默认收藏), Love(我喜欢)"""
    r = requests.get(URL + "getMusicList/", params={"token": get_token(), "types": types, "name": name})
    return r.json()


# 改变用户歌曲的所属收藏夹
def setMusicCollection(types, name, collection_name):
    """types: add,del"""
    """collection_name: name: Default(默认收藏), Love(我喜欢)"""
    r = requests.get(URL + "setMusicCollection/",
                     params={"token": get_token(), "types": types, "name": name, "collection_name": collection_name})
    return r.json()


# 获取用户信息
def getUserInformation():
    r = requests.get(URL + "getUserInformation/", params={"token": get_token()})
    return r.json()


if __name__ == "__main__":
    pass
