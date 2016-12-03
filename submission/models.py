from django.db import models
from util.shortcuts import rand_str
from util.models import OJ
from submission.result import OJ_submit_id_pwd,result


class Submission(models.Model):
    # local 相关
    id = models.CharField(max_length=32, default=rand_str, primary_key=True, db_index=True)
    user_id = models.IntegerField(db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)
    # 判题开始时间
    judge_start_time = models.BigIntegerField(blank=True, null=True)
    # 判题结束时间
    judge_end_time = models.BigIntegerField(blank=True, null=True)

    local_problem_id = models.IntegerField(db_index=True)
    # 是否可以分享
    public = models.BooleanField(default=False)

    # remote 相关
    # 某些OJ获取不到OJ_ID或者获取到了无法根据这个来查询 所以允许为空
    # submit need： user_id, pwd, pid, lang, src
    remote_oj_run_id = models.CharField(max_length=50, blank=True, null=True)

    remote_oj = models.ForeignKey(OJ)

    remote_oj_submit_id = models.CharField(max_length=50, default=OJ_submit_id_pwd['poj']['id'])
    remote_oj_submit_pwd = models.CharField(max_length=50, default=OJ_submit_id_pwd['poj']['pwd'])
    remote_oj_problem_id = models.CharField(max_length=50)
    language = models.IntegerField()
    code = models.TextField()
    result = models.IntegerField(default=result['local_queue'])

    # 这个字段可能存储很多数据 比如编译错误、系统错误的时候，存储错误原因字符串
    # 正常运行的时候存储判题结果，比如cpu时间内存之类的
    info = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "submission"
        ordering = ['-create_time']

    def __str__(self):
        return self.id
