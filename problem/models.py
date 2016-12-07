from django.db import models

# Create your models here.
from authentication.models import MyUser


class ProblemTag(models.Model):
    # 名字
    name = models.CharField('标签', max_length=30)
    # 简称 小写字母
    abbreviation = models.CharField('简称', max_length=10, default="", unique=True)
    # 简介
    intro = models.TextField('简介', default='')
    # 创建时间
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    @property
    def get_rk(self):
        pt = ProblemTag.objects.get(id=self.id)
        p = pt.problem_set.all()
        n = len(p)
        return 200-150/(n+1)

    class Meta:
        db_table = "problem_tag"

    def __str__(self):
        return self.name


class Problem(models.Model):
    # 原始url
    origin_url = models.CharField('源url', max_length=50, default="django-you")
    # 所属OJ
    oj = models.CharField('所属OJ', max_length=30)
    # 所属OJ ID
    oj_id = models.CharField('OJ题号', max_length=30)
    # 标题
    title = models.CharField('标题', max_length=50)
    # 时间限制 考虑到用爬虫爬取题目连单位一起爬取 所以为CharField
    time_limit = models.CharField('时间限制', max_length=50)
    # 内存限制  考虑到用爬虫爬取题目连单位一起爬取 所以为CharField 连单位一起爬取
    memory_limit = models.CharField('时间限制', max_length=50)
    # 描述 富文本形式 summer_note 插件
    description = models.TextField('问题描述', max_length=30000)
    # 输入描述 富文本形式 summer_note 插件
    input_description = models.TextField('输入描述', max_length=10000, default='')
    # 输出描述 富文本形式 summer_note 插件
    output_description = models.TextField('输出描述', max_length=10000, default='')
    # 输入内容
    input = models.TextField('输入', max_length=10000, default='')
    # 输出内容
    output = models.TextField('输出', max_length=10000, default='')

    # hint
    hint = models.CharField('备注', blank=True, default="", max_length=256)
    # 创建时间
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    # 创建者
    create_by = models.ForeignKey(MyUser)
    # 最后更新时间
    last_update_time = models.DateTimeField('最后更新时间', blank=True, null=True, auto_now=True)
    # 标签
    tags = models.ManyToManyField(ProblemTag, blank=True)
    # 是否可见
    visible = models.BooleanField(default=True)

    def get_notes(self):
        notes = self.classicnote_set.all()
        return notes

    def get_note_num(self):
        notes = self.classicnote_set.all()
        return len(notes)

    @property
    def ac_user_num(self):
        notes = self.classicnote_set.all()
        cnt = 0
        for note in notes:
            if note.ac:
                cnt += 1
        return cnt

    @property
    def user_num(self):
        return self.get_note_num()

    @property
    def difficulty(self):
        notes = self.classicnote_set.all()
        total = 0.0
        cnt = 0.0
        for note in notes:
            cnt += 1.0
            if note.difficulty:
                total += note.difficulty
        if cnt == 0.0:
            # 返回一个dict
            return {'难度等级': '暂无', '难度系数': '暂无'}
        else:
            average = total/cnt
            if average < 4.0:
                return {'难度等级': u'简单', '难度系数': average}
            elif average > 7.0:
                return {'难度等级': u'困难', '难度系数': average}
            else:
                return {'难度等级': u'中等', '难度系数': average}

    @property
    def difficulty_rank(self):
        return self.difficulty['难度等级']

    @property
    def difficulty_num(self):
        return self.difficulty['难度系数']

    @property
    def get_tags_string(self):
        tg = self.tags.all()
        res = ''
        for tag in tg:
            res += tag.abbreviation
            res += ','
        if res == '':
            res = u'暂无'
        else:
            l = len(res)
            res = res[:l-1]
        return res

    @property
    def get_tags(self):
        tg = self.tags.all()
        return tg

    @property
    def oj_all(self):
        return self.oj+self.oj_id

    class Meta:
        db_table = "problem"
        unique_together = ('oj', 'oj_id')
        ordering = ['oj', 'oj_id']

    def __str__(self):
        return self.oj_all+"("+self.title+")"
