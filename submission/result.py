# coding=utf-8


# 这个映射关系是前后端通用的,判题服务器提供接口,也应该遵守这个,可能需要一些转换
# <=3 说明还没出结果，TLE，MLE等信息在rejected状态下存储在submission的info中
result = {
    "local_queue": 0,
    "submitting": 1,
    "remote_queue": 2,
    "running": 3,
    "accepted": 4,
    "rejected": 5,
    "system_error": 6,
    "remote_error": 7,
}
language = {
    'c': 0,
    'c++': 1,
    'gcc': 2,
    'g++': 3,
    'java': 4,
    'python2': 5,
    'python3': 6,
}
er_language = zip(language.keys(), language.values())

language_reverse = dict(zip(language.values(), language.keys()))
re_language = zip(language.values(), language.keys())

OJ_submit_id_pwd = {
    'codeforces': {'id': 'crazyX_CN', 'pwd': 'x970307jw'},
    'poj': {'id': 'crazyX', 'pwd': 'x970307jw'},
    'hdu': {'id': 'crazyX', 'pwd': 'x970307jw'},
}

