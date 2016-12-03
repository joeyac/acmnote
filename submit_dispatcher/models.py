from django.db import models


class JudgeWaitingQueue(models.Model):
    submission_id = models.CharField(max_length=40)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "judge_waiting_queue"


class JudgeOJ(models.Model):
    name = models.CharField(max_length=30)
    max_instance_number = models.IntegerField()
    used_instance_number = models.IntegerField(default=0)
    token = models.CharField(max_length=30)
    # status 为 false 的时候代表不使用这个服务器
    status = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = "JudgeOJ"
