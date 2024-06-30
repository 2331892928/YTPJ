import base64
import json
import time

import ddddocr
import js2py
import my_fake_useragent
import requests
from bs4 import BeautifulSoup
from cryptography.fernet import Fernet


class ZhiHui:
    def __init__(self, username, password):
        self.session = requests.session()
        UA = my_fake_useragent.UserAgent(family="chrome")
        # UA.random()
        self.session.headers = {
            "User-Agent": "youxiaopai"
        }
        self.username = username
        self.password = password
        # 课表 gnmkdm
        self.gnmkdm = {
            "kb": "N2151"
        }

    def login(self):
        self.session.headers = {
            "Origin": "http://ids.cqyti.com",
            "Host": "ids.cqyti.com",
            "Referer": "http://ids.cqyti.com/authserver/login?service=http%3A%2F%2Fehall.cqyti.com%2Flogin%3Fservice%3Dhttp%3A%2F%2Fehall.cqyti.com%2Fywtb-portal%2Fstandard%2Findex.html",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Gpc": "1",
            "Dnt": "1"
        }
        self.session.cookies['org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE'] = "zh_CN"
        res = self.session.get(
            "http://ids.cqyti.com/authserver/login?service=http%3A%2F%2Fehall.cqyti.com%2Flogin%3Fservice%3Dhttp%3A%2F%2Fehall.cqyti.com%2Fywtb-portal%2Fstandard%2Findex.html")
        soup = BeautifulSoup(res.content.decode(), "html.parser")
        form = soup.find("form", class_="loginFromClass")

        # execution
        execution = form.find("input", attrs={"id": "execution"}).get("value").strip()

        # 密码加密salt
        pwdEncryptSalt = form.find_next("input", attrs={"id": "pwdEncryptSalt"}).get("value").strip()

        # 密码加密
        # js2py.translate_file('ytzhmh/encrypt.js', 'ytzhmh/encrypt.py')
        # http://ids.cqyti.com/personalInfo/personCenter/encrypt.js
        from yt.encrypt import encrypt
        saltPassword = encrypt.encryptPassword(self.password, pwdEncryptSalt)
        # 是否需要验证码

        res = self.session.get(
            "http://ids.cqyti.com/authserver/checkNeedCaptcha.htl?username={}&_={}".format(self.username,
                                                                                           int(time.time() * 1000)))
        res_json = json.loads(res.content.decode())
        if res_json['isNeed']:
            self.verifySliderCaptcha()
        res = self.session.post(
            "http://ids.cqyti.com/authserver/login?service=http%3A%2F%2Fehall.cqyti.com%2Flogin%3Fservice%3Dhttp%3A%2F%2Fehall.cqyti.com%2Fywtb-portal%2Fstandard%2Findex.html",
            data={
                "cllt": "userNameLogin",
                "dllt": "generalLogin",
                "_eventId": "submit",
                "captcha": "",
                "lt": "",
                "username": self.username,
                "password": saltPassword,
                "execution": execution
            })
        soup = BeautifulSoup(res.content.decode(), "html.parser")
        try:
            showErrorTip = soup.find("span", attrs={"id": "showErrorTip"}).get_text().strip()
            return False, showErrorTip
        except:
            return True, self.session.cookies.get_dict(domain="ids.cqyti.com")

    def __del__(self):
        pass

    def logout(self):
        self.session.headers = {
            "Host": "ids.cqyti.com",
            "Referer": "http://ids.cqyti.com/personalInfo/personCenter/index.html",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Gpc": "1",
            "Dnt": "1"
        }
        self.session.get(
            "http://ids.cqyti.com/authserver/logout?service=http%3A%2F%2Fids.cqyti.com%2Fauthserver%2Findex.do")
        self.session.close()

