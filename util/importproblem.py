# encoding:UTF-8
import requests
import re
import urllib.request
from django.contrib.auth.models import User
from authentication.models import MyUser
from problem.models import Problem


# 杭电oj编码方式为gb2312，需要用urllib读取后解码  需要用gbk解码 坑啊
def get_hdu_info(problem_id):
    base_url = 'http://acm.hdu.edu.cn/showproblem.php?pid='
    url = base_url + str(problem_id)

    html = requests.get(url).text

    if 'No such problem' in html:
        ots = str(problem_id)+' : No such problem'
        print(ots)
        return False
    if 'System Message' in html:
        ots = str(problem_id) + ' : System error'
        print(ots)
        return False

    response = urllib.request.urlopen(url)
    html = response.read().decode('gbk')

    reg_title = "<h1 style='color:#1A5CC8'>(.*?)</h1>"
    title = re.findall(reg_title, html, re.S)[0]

    reg_time_limit = "Time Limit:(.*?)&nbsp;"
    time_limit = re.findall(reg_time_limit, html, re.S)[0]

    reg_memory_limit = "Memory Limit:(.*?)<br>"
    memory_limit = re.findall(reg_memory_limit, html, re.S)[0]

    # 0 1 2 3 4分别是描述，输入，输出,样例输入，样例输出
    description = {}
    # if len(description) <= 4:# 因为某些题目缺少某些区域,所以只能一个个爬取判断
    # print(str(ProblemID)+" "+str(len(description)))
    reg = "Problem Description</div> <div class=panel_content>(.*?)</div><div class=panel_bottom>"
    tmp = re.findall(reg, html, re.S)
    description[0] = tmp[0] if tmp else "无"

    reg = "Input</div> <div class=panel_content>(.*?)</div><div class=panel_bottom>"
    tmp = re.findall(reg, html, re.S)
    description[1] = tmp[0] if tmp else "无"

    reg = "Output</div> <div class=panel_content>(.*?)</div><div class=panel_bottom>"
    tmp = re.findall(reg, html, re.S)
    description[2] = tmp[0] if tmp else "无"

    reg = "Sample Input</div><div class=panel_content>(.*?)</div><div class=panel_bottom>"
    tmp = re.findall(reg, html, re.S)
    description[3] = tmp[0] if tmp else "无"

    reg = "Sample Output</div><div class=panel_content>(.*?)</div><div class=panel_bottom>"
    tmp = re.findall(reg, html, re.S)
    description[4] = tmp[0] if tmp else "无"

    base_img_url = 'http://acm.hdu.edu.cn/'
    for i in range(0, 5):
        if 'src=' in description[i]:
            if "../../" in description[i]:
                description[i] = description[i].replace("../../data/images/", base_img_url + "data/images/")
            else:
                description[i] = description[i].replace("/data/images/", base_img_url + "data/images/")
    return {'title': title, 'time_limit': time_limit, 'memory_limit': memory_limit,
            'description': description[0], 'input_description': description[1],
            'output_description': description[2], 'input': [description[3]], 'output': [description[4]]}


def get_poj_info(problem_id):
    base_url = 'http://poj.org/problem?id='
    url = base_url + str(problem_id)
    html = requests.get(url).text

    if 'Can not find problem' in html:
        ots = str(problem_id) + ' : Can not find problem'
        print(ots)
        return False
    if 'Error Occurred' in html:
        ots = str(problem_id) + ' : Error Occurred'
        print(ots)
        return False

    reg_title = '<div class="ptt" lang="en-US">(.*?)</div>'
    title = re.findall(reg_title, html, re.S)[0]

    reg_time_limit = "Time Limit:</b> (.*?)</td>"
    time_limit = re.findall(reg_time_limit, html, re.S)[0]

    reg_memory_limit = "Memory Limit:</b> (.*?)</td>"
    memory_limit = re.findall(reg_memory_limit, html, re.S)[0]

    # 0 1 2 分别是描述，输入描述，输出描述
    reg_description = '<div class="ptx" lang="en-US">(.*?)</div><p class="pst">'
    description = re.findall(reg_description, html, re.S)

    # 0 1 分别是输入，输出
    reg_in_out = '<pre class="sio">(.*?)</pre><p class="pst">'
    in_out = re.findall(reg_in_out, html, re.S)

    return {'title': title, 'time_limit': time_limit, 'memory_limit': memory_limit,
            'description': description[0], 'input_description': description[1],
            'output_description': description[2], 'input': [in_out[0]], 'output': [in_out[1]]}


def get_cf_info(problem_id, problem_c):
    problem_id = str(problem_id)
    problem_c = str(problem_c)
    base_url = 'http://codeforces.com/problemset/problem/'
    url = base_url + problem_id + "/" + problem_c
    html = requests.get(url).text
    io = 'No such problem'
    # print(html)
    if io in html:
        print(io + ":" + problem_id + problem_c)
        return False

    reg_title = '<div class="title">(.*?)</div>'
    title = re.findall(reg_title, html, re.S)[0]
    title = title[3:]

    reg_time_limit = "time limit per test</div>(.*?)</div>"
    time_limit = re.findall(reg_time_limit, html, re.S)[0]

    reg_memory_limit = "memory limit per test</div>(.*?)</div>"
    memory_limit = re.findall(reg_memory_limit, html, re.S)[0]

    reg_description = 'output</div>(?:.+)</div></div>(.*?)<div class="input-specification">'
    description = re.findall(reg_description, html, re.S)[0]

    reg_input_description = '<div class="section-title">Input</div>(.*?)</div>'
    input_description = re.findall(reg_input_description, html, re.S)[0]

    reg_output_description = '<div class="section-title">Output</div>(.*?)</div>'
    output_description = re.findall(reg_output_description, html, re.S)[0]

    reg_input = '<div class="title">Input</div>(.*?)</div>'
    inputs = re.findall(reg_input, html, re.S)

    reg_out = '<div class="title">Output</div>(.*?)</div>'
    outputs = re.findall(reg_out, html, re.S)
    # print(outputs)
    # print(len(inputs))

    return {'title': title, 'time_limit': time_limit, 'memory_limit': memory_limit,
            'description': description, 'input_description': input_description,
            'output_description': output_description, 'input': inputs, 'output': outputs}


def import_cf(problem_id, problem_c):
    oj_name = 'codeforces'
    res = get_cf_info(problem_id, problem_c)
    if not res:
        return False
    base_url = 'http://codeforces.com/problemset/problem'
    user = User.objects.get_by_natural_key('xjw')
    my_user = MyUser.objects.get(user=user)
    pid = str(problem_id)+str(problem_c)
    _input = ''
    _output = ''
    if len(res['input']) == 1:
        _input = str(res['input'][0])
    else:
        cnt = 0
        for ins in res['input']:
            cnt += 1
            _input += "样例 " + str(cnt) + " : <br>"
            _input += str(ins)

    if len(res['output']) == 1:
        _output = str(res['output'][0])
    else:
        cnt = 0
        for ous in res['output']:
            cnt += 1
            _output += "样例 " + str(cnt) + " : <br>"
            _output += str(ous)
    Problem.objects.update_or_create(
        oj=oj_name,
        oj_id=pid,
        defaults={'title': res['title'],
                  'time_limit': res['time_limit'],
                  'memory_limit': res['memory_limit'],
                  'description': res['description'],
                  'input_description': res['input_description'],
                  'output_description': res['output_description'],
                  'input': _input,
                  'output': _output,
                  'create_by': my_user,
                  'hint': '自动导入',
                  'origin_url': base_url + '/' + str(problem_id) + '/' + str(problem_c),
                  },
    )
    print(oj_name + pid + " : success!")
    return True


def import_hdu(problem_id):
    oj_name = 'hdu'
    res = get_hdu_info(problem_id)
    if not res:
        return False
    user = User.objects.get_by_natural_key('xjw')
    base_url = 'http://acm.hdu.edu.cn/showproblem.php?pid='
    my_user = MyUser.objects.get(user=user)
    pid = str(problem_id)

    _input = ''
    _output = ''
    if len(res['input']) == 1:
        _input = str(res['input'][0])
    else:
        cnt = 0
        for ins in res['input']:
            cnt += 1
            _input += "样例 " + str(cnt) + " : <br>"
            _input += str(ins)

    if len(res['output']) == 1:
        _output = str(res['output'][0])
    else:
        cnt = 0
        for ous in res['output']:
            cnt += 1
            _output += "样例 " + str(cnt) + " : <br>"
            _output += str(ous)

    Problem.objects.update_or_create(
        oj=oj_name,
        oj_id=pid,
        defaults={'title': res['title'],
                  'time_limit': res['time_limit'],
                  'memory_limit': res['memory_limit'],
                  'description': res['description'],
                  'input_description': res['input_description'],
                  'output_description': res['output_description'],
                  'input': _input,
                  'output': _output,
                  'create_by': my_user,
                  'hint': '自动导入',
                  'origin_url': base_url + str(problem_id),
                  },
    )
    print(oj_name + pid + " : success!")
    return True


def import_poj(problem_id):
    oj_name = 'poj'
    res = get_poj_info(problem_id)
    if not res:
        return False
    user = User.objects.get_by_natural_key('xjw')
    base_url = 'http://poj.org/problem?id='
    my_user = MyUser.objects.get(user=user)
    pid = str(problem_id)

    _input = ''
    _output = ''
    if len(res['input']) == 1:
        _input = str(res['input'][0])
    else:
        cnt = 0
        for ins in res['input']:
            cnt += 1
            _input += "样例 " + str(cnt) + " : <br>"
            _input += str(ins)

    if len(res['output']) == 1:
        _output = str(res['output'][0])
    else:
        cnt = 0
        for ous in res['output']:
            cnt += 1
            _output += "样例 " + str(cnt) + " : <br>"
            _output += str(ous)

    Problem.objects.update_or_create(
        oj=oj_name,
        oj_id=pid,
        defaults={'title': res['title'],
                  'time_limit': res['time_limit'],
                  'memory_limit': res['memory_limit'],
                  'description': res['description'],
                  'input_description': res['input_description'],
                  'output_description': res['output_description'],
                  'input': _input,
                  'output': _output,
                  'create_by': my_user,
                  'hint': '自动导入',
                  'origin_url': base_url + str(problem_id),
                  },
    )
    print(oj_name + pid + " : success!")
    return True

