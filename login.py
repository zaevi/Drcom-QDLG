from urllib import request, parse, error
from http import cookiejar
import captcha
from bs4 import BeautifulSoup

userAgent = ['Mozilla/5.0 (Windows NT 10.0; WOW64)',
             'AppleWebKit/537.36 (KHTML, like Gecko) ',
             'Chrome/45.0.2454.85 Safari/537.36']
header = {
    'User-Agent': ''.join(userAgent),
    "Accept": 'image/webp,image/*,*/*;q=0.8',
    "Accept-Encoding": 'gzip, deflate, sdch',
    "Accept-Language": 'zh-CN,zh;q=0.8',
    "Cache-Control": 'max-age=0',
    "Connection": 'keep-alive',
    "Host": '192.168.3.8:8080',
    "Referer": 'http://192.168.3.8:8080/ghca/',

}

cj = cookiejar.LWPCookieJar()
pro = request.HTTPCookieProcessor(cj)
opener = request.build_opener(pro)


def openPage(url, data=None):
    if data:
        data = parse.urlencode(data).encode(encoding='UTF8')
    req = request.Request(url, data=data, headers=header)
    res = opener.open(req)
    # assert res.status == 200, ''.join([res.status, ' ', res.reason])
    return res


def checkState():
    logined, connected = True, True
    try:
        openPage("http://192.168.3.11:7001/QDHWSingle/loginlg.jsp")
    except:
        logined = False
        try:
            openPage("http://192.168.3.11:7001/QDHWSingle/successlg.jsp")
        except:
            connected = False
        else:
            logined = True
    else:
        logined = False
    finally:
        return logined, connected


def checkStateText(logined, connected):
    text = "已连接, " if connected else "未连接"
    text += "已登录" if logined else "未登录"
    return text


def login(username, password):
    logined, connected = checkState()
    if logined:
        return True, "已登录."
    elif not connected:
        return False, "未连接!"

    openPage("http://192.168.3.11:7001/QDHWSingle/loginlg.jsp")
    captchaUrl = ''.join(['http://192.168.3.11:7001/QDHWSingle/',
                          'ValidateCodeServlet?action=ShowValidateCode1'])
    validatecode = captcha.captcha(openPage(captchaUrl))

    postData = {
        'from': '1g',
        'logName': str(username),
        'logPW': str(password),
        'validatecode': validatecode,
    }

    openPage('http://192.168.3.11:7001/QDHWSingle/login.do', postData)

    if checkState() == (True, True):
        return True, "登录成功."
    else:
        return False, "登录失败!"
