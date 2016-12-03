# -*- coding: utf-8 -*-
import logging
from time import sleep
from robobrowser import RoboBrowser

from bs4 import BeautifulSoup
import html5lib
import urllib
import urllib.request
import warnings
warnings.filterwarnings("ignore")
logger = logging.getLogger('crawler_submit')


class CF:
    # 基本信息
    URL_HOME = 'http://codeforces.com/'
    URL_LOGIN = URL_HOME + 'enter'
    URL_SUBMIT = URL_HOME + 'problemset/submit'
    URL_STATUS = URL_HOME + 'submissions/'

    # 结果信息
    INFO = ['RunID', 'Submit Time', 'Author', 'Pro.ID', 'Language', 'Judge Status', 'Time', 'Memory']
    # 语言
    LANGUAGE = {
        'G++': '42',
        'C': '42',
        'G++11': '42',
        'G++14': '50',
        'GCC': '10',
        'GCC11': '1',
        'JAVA': '36',
        'PYTHON2': '7',
        'PYTHON3': '31',
    }
    #
    header = {
        'Accept': 'text / html, application / xhtml + xml, '
                  'application / xml;q = 0.9, image / webp, * / *;q = 0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Ubuntu Chromium/52.0.2743.116 Chrome/52.0.2743.116 Safari/537.36',
        'Origin': "http://codeforces.com",
        'Host': "codeforces.com",
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
    }

    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password
        self.browser = RoboBrowser()
        self.run_id = ''
        self.pre_id = ''
        self.res = {}

    def login(self):
        try:
            self.browser.open(CF.URL_LOGIN)
        except:
            ots = "Server Error"
            logger.error(ots)
            print(ots)
            return False
        enter_form = self.browser.get_form('enterForm')
        enter_form['handle'] = self.user_id
        enter_form['password'] = self.password

        try:
            self.browser.submit_form(enter_form)
        except:
            ots = "Server Error"
            logger.error(ots)
            print(ots)
            return False

        try:
            checks = list(map(lambda x: x.getText()[1:].strip(),
                              self.browser.select('div.caption.titled')))
            if self.user_id not in checks:
                ots = "Login Failed.. "
                logger.info(ots)
                print(ots)
                return False
        except:
            ots = "Server Error"
            logger.error(ots)
            return False
        ots = 'Login Successful!'
        logger.info(ots)
        return True

    def submit(self, pro_id, language, src):
        pro_id = str(pro_id).upper()
        try:
            language = CF.LANGUAGE[str(language).upper()]
        except:
            ots = 'language unrecognizable!'
            logger.error(ots)
            print(ots)
            return False

        try:
            self.browser.open(CF.URL_SUBMIT)
        except:
            ots = "Server Error"
            logger.error(ots)
            print(ots)
            return False

        submit_form = self.browser.get_form(class_='submit-form')
        submit_form['submittedProblemCode'] = pro_id
        submit_form['source'] = src
        submit_form['programTypeId'] = language

        self.browser.submit_form(submit_form)

        if self.browser.url[-6:] != 'status':
            ots = 'Submit Failed..(probably because you have submit the same file before.)'
            logger.info(ots)
            print(ots)
            return False
        ots = 'Submit Successful'
        logging.info(ots)
        print(ots)
        return True

    def init_id(self):
        if self.pre_id != '':
            return True
        url = CF.URL_STATUS + str(self.user_id)
        try:
            req = urllib.request.Request(url=url, headers=CF.header)
            page = urllib.request.urlopen(req, timeout=5)
        except:
            ots = "Server Error"
            logger.error(ots)
            print(ots)
            return False
        soup = BeautifulSoup(page, 'html5lib')
        tables = soup.find('table', {'class': 'status-frame-datatable'})
        tmp = []
        for row in tables.findAll('tr'):
            cols = row.findAll('td')
            cols = [ele.text.strip() for ele in cols]
            tmp = [ele.replace(u'\xa0', u' ') for ele in cols if ele]
            if len(tmp) == 8:
                break
        self.pre_id = tmp[0]
        return True

    def result(self):
        url = CF.URL_STATUS + str(self.user_id)
        try:
            page = urllib.request.urlopen(url, timeout=5)
        except:
            ots = "Server Error"
            logger.error(ots)
            print(ots)
            return False
        soup = BeautifulSoup(page, 'html5lib')

        tables = soup.find('table', {'class': 'status-frame-datatable'})
        tmp = []
        find = False
        for row in tables.findAll('tr'):
            cols = row.findAll('td')
            cols = [ele.text.strip() for ele in cols]
            tmp = [ele.replace(u'\xa0', u' ') for ele in cols if ele]
            if len(tmp) == 8:
                if tmp[0] == self.pre_id:
                    break
                if not find:
                    if self.run_id == '' or self.run_id == tmp[0]:
                        find = True
                        self.run_id = tmp[0]
            if find:
                break
        if not find:
            ots = "Can not find submissions!"
            logging.info(ots)
            print(ots)
            return True

        wait = ['Running', 'In queue']
        if tmp[5].find(wait[0]) != -1 or tmp[5].find(wait[1]) != -1:
            logging.info(tmp[5])
            return False
        for i in range(8):
            self.res[CF.INFO[i]] = tmp[i]
            print(CF.INFO[i], ':', tmp[i])
        return True


def submit_cf(user_id, pwd, pid, lang, src):
    # lang: g++ c g++11 g++14 gcc gcc11 java python2 python3
    logging.info('connecting to server...')
    print('connecting to server...')
    cf = CF(user_id, pwd)
    if cf.login():
        logging.info("submitting...")
        print("submitting...")
        status = cf.init_id()
        while not status:
            status = cf.init_id()
        if cf.submit(pid, lang, src):
            logging.info('getting result...')
            print('getting result...')
            status = cf.result()
            while not status:  # 每隔1s检测一次结果
                status = cf.result()
                sleep(1)
    if cf.res != {}:
        return cf.res
    else:
        return False
