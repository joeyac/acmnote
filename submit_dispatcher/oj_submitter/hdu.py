# -*- coding: utf-8 -*-
import re
import logging
from time import sleep
from bs4 import BeautifulSoup
import urllib
import urllib.request
import urllib.parse
import http.cookiejar
import html5lib
logger = logging.getLogger('crawler_submit')


class HDU:
    # 基本信息
    URL_HOME = 'http://acm.hdu.edu.cn/'
    URL_LOGIN = URL_HOME + 'userloginex.php?action=login'
    URL_SUBMIT = URL_HOME + 'submit.php?action=submit'
    URL_STATUS = URL_HOME + 'status.php?'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Ubuntu Chromium/52.0.2743.116 Chrome/52.0.2743.116 Safari/537.36',
        'Origin': "http://acm.hdu.edu.cn",
        'Host': "acm.hdu.edu.cn",
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
    }
    # 结果信息
    INFO = ['RunID', 'Submit Time', 'Judge Status', 'Pro.ID',
            'Time', 'Memory', 'Code Len', 'Language', 'Author']
    # 语言
    LANGUAGE = {
        'G++': '0',
        'GCC': '1',
        'C++': '2',
        'C': '3',
        'PASCAL': '4',
        'JAVA': '5',
        'C#': '6',
    }

    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password
        self.run_id = ''
        self.problem_id = ''
        self.res = {}
        cj = http.cookiejar.LWPCookieJar()
        cookie_support = urllib.request.HTTPCookieProcessor(cj)
        self.opener = urllib.request.build_opener(
            cookie_support, urllib.request.HTTPHandler)
        urllib.request.install_opener(self.opener)

    def login(self):
        data = dict(
            username=self.user_id,
            userpass=self.password,
            login='Sign In'
        )
        post_data = urllib.parse.urlencode(data).encode('utf-8')
        try:
            request = urllib.request.Request(
                HDU.URL_LOGIN, post_data, HDU.headers)
            response = urllib.request.urlopen(request).read().decode('utf-8')
            if response.find('signout') > 0:
                ots = "login Successful!"
                logger.info(ots)
                print(ots)
                return True
            else:
                ots = "login Failed!"
                logger.error(ots)
                print(ots)
                return False
        except:
            ots = 'Server Error-login failed'
            logger.error(ots)
            print(ots)
            return False

    def submit(self, pid, language, src):
        self.problem_id = pid
        submit_data = dict(
            problemid=pid,
            language=HDU.LANGUAGE[language.upper()],
            usercode=src,
            check='0',
        )
        post_data = urllib.parse.urlencode(submit_data).encode('utf-8')
        try:
            request = urllib.request.Request(
                HDU.URL_SUBMIT, post_data, HDU.headers)
            response = urllib.request.urlopen(request).read().decode('gbk')
            ots = 'Submit Successful'
            logger.info(ots)
            print(ots)
            return True
        except:
            ots = 'Server Error-submit failed'
            logger.error(ots)
            print(ots)
            return False

    def result(self):
        url_data = {
            'first': '',
            'pid': self.problem_id,
            'user': self.user_id,
        }
        if self.run_id != '':
            url_data['first'] = self.run_id

        url = HDU.URL_STATUS + urllib.parse.urlencode(url_data)

        try:
            page = urllib.request.urlopen(url, timeout=5)
        except:
            ots = 'Server Error'
            logger.error(ots)
            print(ots)
            return False

        soup = BeautifulSoup(page, 'html5lib')
        table = soup.findAll('table', {'class': 'table_text'})  # 提取表格
        pattern = re.compile(r'>[-+: \w]*<')  # 正则表达式匹配需要的信息
        result = pattern.findall(str(table))
        wait = ['Queuing', 'Compiling', 'Running']
        num = [21, 23, 26, 30, 33, 35, 38, 41, 44]  # 最终结果在result序列中的位置

        try:
            if self.run_id == '':
                self.run_id = result[21][1:-1]
            for i in range(3):
                if result[26][1:-1] == wait[i] or result[26][1:-1] == '':
                    logging.info(result[26])
                    return False
            for i in range(9):
                self.res[HDU.INFO[i]] = result[num[i]][1:-1]
                print(HDU.INFO[i], ':', result[num[i]][1:-1])
            return True
        except:
            ots = 'Server Error'
            logger.error(ots)
            print(ots)
            return False


def submit_hdu(user_id, pwd, pid, lang, src):
    # lang: g++ gcc java pascal c++ c C#
    logger.info('connecting to server...')
    print('connecting to server...')
    hdu = HDU(user_id, pwd)
    if hdu.login():
        logger.info("submitting...")
        print("submitting...")
        if hdu.submit(pid, lang, src):
            logger.info('getting result...')
            print('getting result...')
            status = hdu.result()
            while not status:  # 每隔1s检测一次结果
                status = hdu.result()
                sleep(1)
    if hdu.res != {}:
        return hdu.res
    else:
        return False
