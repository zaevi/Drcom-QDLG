import login
import configparser
import os
import time


def getInput(text, warningText=None):
    cmd = input(text)
    if cmd:
        return cmd
    else:
        print(warningText) if warningText else False
        return getInput(text, warningText)


def inputUser(username=None, password=None):
    if not username:
        username = input("输入帐号: ")
        if len(username) < 9:
            print("请输入正确的帐号! ", end='')
            return inputUser()
        username = username[:9] + "@QDLG"

    if not password:
        password = input("输入密码: ")
        if len(password) < 6:
            print("请输入正确的密码! ", end='')
            return inputUser(username)

    return username, password


def toLogin():
    username, password, toSave = None, None, False

    config = configparser.ConfigParser()
    if os.path.exists('login.ini'):
        config.read('login.ini')
        if config.has_section("Login"):
            username = config.get('Login', 'username', fallback=None)
            password = config.get('Login', 'password', fallback=None)

    if username and password:
        print("使用上次登录的帐号: " + username)
    else:
        username, password = inputUser()
        toSave = True

    result, info = login.login(username, password)
    print(info)

    if result and toSave:
        if not config.has_section("Login"):
            config.add_section("Login")
        config.set('Login', 'username', username)
        config.set('Login', 'password', password)
        config.write(open('login.ini', 'w'))

if __name__ == '__main__':
    print("校园网页面登录器 by 扎易 for 青岛理工大学")
    print("======================================")
    os.system("title Drcom@QDLG-Loginer")

    logined, connected = login.checkState()
    print("网络状态: " + login.checkStateText(logined, connected))
    if logined:
        print("你已登录.")
    else:
        toLogin()

    time.sleep(3)
