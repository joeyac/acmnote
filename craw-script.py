from acmnote2.wsgi import *
from util.importproblem import *
from util.models import OJ


def test():
    user = User.objects.get_by_natural_key('xjw')
    my_user = MyUser.objects.get(user=user)

    for pid in range(1000, 1100):
        info = get_hdu_info(pid)
        if info == 'No such problem' or info == 'System error':
            print(str(pid)+":"+info)
            continue
        Problem.objects.update_or_create(
            oj='hdu',
            oj_id=str(pid),
            defaults={'title': info['title'],
                      'time_limit': info['time_limit'],
                      'memory_limit': info['memory_limit'],
                      'description': info['description'],
                      'input_description': info['input_description'],
                      'output_description': info['output_description'],
                      'input': info['input'],
                      'output': info['output'],
                      'create_by': my_user,
                      'hint': '导入功能测试'
                      },
        )
        print(str(pid)+" : success!")


def init(num1=1, num2=1000,  num3=1000):
    oj = [('codeforces', num1), ('poj', num2), ('hdu', num3)]
    for name, max_id in oj:
        noj = OJ.objects.get_or_create(name=name)
        noj[0].max_problem_id = max_id
        noj[0].save()
        print(noj)


def update_cf(up_id=None):
    name = 'codeforces'
    oj = OJ.objects.get(name=name)
    max_id = oj.max_problem_id
    res = True
    while res:
        res = import_cf(max_id, 'A')
        if not res:
            break
        chr_id = ord('A')+1
        while import_cf(max_id, chr(chr_id)):
            chr_id += 1
        max_id += 1
        if up_id and up_id <= max_id:
            break
    oj.max_problem_id = max_id
    oj.save()


def update_poj(up_id=None):
    name = 'poj'
    oj = OJ.objects.get(name=name)
    max_id = oj.max_problem_id
    res = True
    while res:
        res = import_poj(max_id)
        if not res:
            break
        max_id += 1
        if up_id and up_id <= max_id:
            break
    oj.max_problem_id = max_id
    oj.save()


def update_hdu(up_id=None):
    name = 'hdu'
    oj = OJ.objects.get(name=name)
    max_id = oj.max_problem_id
    res = True
    while res:
        res = import_hdu(max_id)
        if not res:
            break
        max_id += 1
        if up_id and up_id <= max_id:
            break
    oj.max_problem_id = max_id
    oj.save()


def up_case(s):
    cr = ord(s[0])
    if 96 < cr < 123:
        return chr(cr-32) + s[1:]
    return s


if __name__ == '__main__':
    flag = input("Need init?(Y or N): ")
    flag = up_case(flag)
    if flag[0] == 'Y':
        init()
    #update_poj(1400)
    #update_hdu(1200)
    update_cf(10)
    print("Done!")
