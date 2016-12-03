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


def init():
    oj = [('codeforces', 1), ('poj', 1000), ('hdu', 1000)]
    for name, max_id in oj:
        noj = OJ.objects.get_or_create(name=name, max_problem_id=max_id)
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


if __name__ == '__main__':
    init()
    update_poj(1121)
    update_hdu(1100)
    update_cf(20)
    print("Done!")
