from django.test import TestCase
from submit_dispatcher.oj_submitter.poj import submit_poj
from submit_dispatcher.oj_submitter.hdu import submit_hdu


def solve(user_id, pwd, pid, lang, src):
    res = submit_hdu(user_id, pwd, pid, lang, src)
    if not res:
        return {'result': 6}
    else:
        return {'result': 1, 'info': res}

