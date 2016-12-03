from django.test import TestCase
from submit_dispatcher.oj_submitter.poj import submit_poj


def solve(user_id, pwd, pid, lang, src):
    res = submit_poj(user_id, pwd, pid, lang, src)
    if not res:
        return {'result': 6}
    else:
        return {'result': 1, 'info': res}

