# coding=utf-8
from django.db import models

from authentication.models import MyUser


class Group(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(MyUser, related_name="my_groups")
    # 0是公开 1是需要申请后加入 2是不允许任何人加入
    join_group_setting = models.IntegerField(default=1)
    members = models.ManyToManyField(MyUser, through="UserGroupRelation")
    admin = models.ManyToManyField(MyUser, through="AdminGroupRelation", related_name="managed_groups")
    # 解散小组后，这一项改为False
    visible = models.BooleanField(default=True)

    @property
    def create_user_name(self):
        return self.created_by.all_name()

    @property
    def join_method(self):
        if self.join_group_setting == 0:
            return '公开'
        elif self.join_group_setting == 1:
            return '需要申请'
        elif self.join_group_setting == 2:
            return '拒绝加入'
        else:
            raise KeyError

    class Meta:
        db_table = "group"


class UserGroupRelation(models.Model):
    group = models.ForeignKey(Group)
    user = models.ForeignKey(MyUser)
    join_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_group_relation"
        unique_together = ("group", "user")


class AdminGroupRelation(models.Model):
    user = models.ForeignKey(MyUser)
    group = models.ForeignKey(Group)

    class Meta:
        db_table = "admin_group_relation"
        unique_together = ("user", "group")


class JoinGroupRequest(models.Model):
    group = models.ForeignKey(Group)
    user = models.ForeignKey(MyUser, related_name="my_join_group_requests")
    message = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    # 是否处理
    status = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)

    class Meta:
        db_table = "join_group_request"
