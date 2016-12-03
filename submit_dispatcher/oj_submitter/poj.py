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


class POJ:
    # 基本信息
    URL_HOME = 'http://poj.org/'
    URL_LOGIN = URL_HOME + 'login?'
    URL_SUBMIT = URL_HOME + 'submit?'
    URL_STATUS = URL_HOME + 'status?'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Ubuntu Chromium/52.0.2743.116 Chrome/52.0.2743.116 Safari/537.36',
        'Origin': "http://poj.org",
        'Host': "poj.org",
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
    }
    # 结果信息
    # INFO = ['RunID', 'User', 'Problem', 'Result',
    # 'Memory', 'Time', 'Language', 'Code Length', 'Submit Time']
    INFO = ['RunID', 'Author', 'Pro.ID', 'Judge Status',
            'Memory', 'Time', 'Language', 'Code Length', 'Submit Time']
    # 语言
    LANGUAGE = {
        'G++': '0',
        'GCC': '1',
        'JAVA': '2',
        'PASCAL': '3',
        'C++': '4',
        'C': '5',
        'FORTRAN': '6',
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
            user_id1=self.user_id,
            password1=self.password,
            B1='login',
            url='.',
        )
        post_data = urllib.parse.urlencode(data).encode('utf-8')
        try:
            request = urllib.request.Request(
                POJ.URL_LOGIN, post_data, POJ.headers)

            response = urllib.request.urlopen(request).read().decode('utf-8')
            if response.find('loginlog') > 0:
                ots = "login successful!"
                logging.info(ots)
                print(ots)
                return True
            else:
                ots = "login failed"
                logging.info(ots)
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
            problem_id=pid,
            language=POJ.LANGUAGE[language.upper()],
            source=src,
            submit='Submit',
            encoded='0',
        )
        post_data = urllib.parse.urlencode(submit_data).encode('utf-8')
        try:
            request = urllib.request.Request(
                POJ.URL_SUBMIT, post_data, POJ.headers)
            response = urllib.request.urlopen(request).read().decode('utf-8')
            ots = 'Submit Successful'
            logger.info(ots)
            print(ots)
            return True
        except :
            ots = 'Server Error-submit failed'
            logger.error(ots)
            print(ots)
            return False

    def result(self):
        url_data = {
            'user_id': self.user_id,
            'problem_id': self.problem_id
        }
        url = POJ.URL_STATUS + urllib.parse.urlencode(url_data)
        try:
            page = urllib.request.urlopen(url, timeout=5)
        except:
            ots = 'Server Error-get result failed'
            logger.error(ots)
            print(ots)
            return False
        soup = BeautifulSoup(page, 'html5lib')
        table = soup.findAll('table', {'class': 'a'})  # 提取表格
        pattern = re.compile(r'>[-+: \w]*<')  # 正则表达式匹配需要的信息
        result = pattern.findall(str(table))
        wait = ['Running & Judging', 'Compiling', 'Waiting']
        num = [22, 25, 29, 33, 36, 38, 41, 44, 46]  # 最终结果在result序列中的位置
        try:
            for i in range(3):
                if result[33][1:-1] == wait[i] or result[33][1:-1] == '':
                    logging.info(result[33])
                    return False
            for i in range(9):
                self.res[POJ.INFO[i]] = result[num[i]][1:-1]
                print(POJ.INFO[i], ':', result[num[i]][1:-1])
            return True
        except:
            ots = 'Server Error-get result failed'
            logger.error(ots)
            print(ots)
            return False


def submit_poj(user_id, pwd, pid, lang, src):
    # lang: g++ gcc java pascal c++ c fortran
    logger.info('connecting to server...')
    print('connecting to server...')
    poj = POJ(user_id, pwd)
    if poj.login():
        logger.info("submitting...")
        print("submitting...")
        if poj.submit(pid, lang, src):
            logger.info('getting result...')
            print('getting result...')
            status = poj.result()
            while not status:  # 每隔1s检测一次结果
                status = poj.result()
                sleep(1)
    if poj.res != {}:
        return poj.res
    else:
        return False
